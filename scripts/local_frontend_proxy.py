#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import hmac
import http.client
import html
import mimetypes
import posixpath
import re
import sys
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlparse


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}
FORWARDED_HEADERS = {"x-forwarded-for", "x-forwarded-proto", "x-real-ip"}
SENSITIVE_HEADERS = {"authorization", "cookie"}
MAX_REQUEST_BODY = 1_048_576
MAX_DRAFT_REQUEST_BODY = 12_001_024
PHONE_UPLOAD_PATH = re.compile(r"/api/draft-upload/[A-Za-z0-9_-]{43}")
DRAFT_IMAGE_POST_PATH = re.compile(r"/api/questions/[1-9][0-9]*/drafts")
ACCESS_COOKIE = "math_access"
ACCESS_SESSION_SECONDS = 14 * 24 * 60 * 60


def build_proxy_headers(incoming_headers, peer: str) -> dict[str, str]:
    headers = {}
    for key, value in incoming_headers.items():
        lowered = key.lower()
        if (lowered in HOP_BY_HOP_HEADERS or lowered in FORWARDED_HEADERS
                or lowered in SENSITIVE_HEADERS or lowered == "host"):
            continue
        headers[key] = value
    headers["Host"] = incoming_headers.get("Host", "")
    headers["X-Real-IP"] = peer
    headers["X-Forwarded-For"] = peer
    headers["X-Forwarded-Proto"] = "http"
    return headers


class FrontendProxyHandler(BaseHTTPRequestHandler):
    static_root: Path
    backend_host: str
    backend_port: int
    backend_scheme: str
    newpoints_host: str = "127.0.0.1"
    newpoints_port: int = 8312
    base_path: str
    auth_password: str

    server_version = "ProStudyLocalFrontend/1.0"

    def do_GET(self) -> None:
        self.dispatch()

    def do_HEAD(self) -> None:
        self.dispatch(head_only=True)

    def do_POST(self) -> None:
        self.dispatch()

    def do_PUT(self) -> None:
        self.dispatch()

    def do_PATCH(self) -> None:
        self.dispatch()

    def do_DELETE(self) -> None:
        self.dispatch()

    def do_OPTIONS(self) -> None:
        self.dispatch()

    def dispatch(self, *, head_only: bool = False) -> None:
        parsed = urlparse(self.path)
        path = self.strip_base_path(parsed.path)
        if path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            if not head_only:
                self.wfile.write(b"ok\n")
            return
        if path == "/login":
            if self.command in {"GET", "HEAD"}:
                self.serve_login_page(parsed.query, head_only=head_only)
            elif self.command == "POST":
                self.login(parsed.query)
            else:
                self.send_error(405, "method not allowed")
            return
        if path == "/logout":
            self.logout(parsed.query)
            return
        # This exact route uses a short-lived, single-upload token instead of
        # the site's password cookie. All photo reads and token issuance stay private.
        if PHONE_UPLOAD_PATH.fullmatch(path) and self.command in {"GET", "HEAD", "POST"}:
            self.proxy_to_backend(backend_path=path, head_only=head_only)
            return
        if not self.authorized():
            self.redirect_to_login()
            return
        if path == "/newpoints" or path.startswith("/newpoints/"):
            backend_path = path + (f"?{parsed.query}" if parsed.query else "")
            self.proxy_to_newpoints(backend_path=backend_path, head_only=head_only)
            return
        if path.startswith("/api/"):
            backend_path = path + (f"?{parsed.query}" if parsed.query else "")
            self.proxy_to_backend(backend_path=backend_path, head_only=head_only)
            return
        self.serve_static(path, head_only=head_only)

    def strip_base_path(self, raw_path: str) -> str:
        if not self.base_path:
            return raw_path or "/"
        if raw_path == self.base_path:
            return "/"
        if raw_path.startswith(f"{self.base_path}/"):
            return raw_path[len(self.base_path):] or "/"
        return raw_path

    def authorized(self) -> bool:
        """Password-only gate at the public boundary; backend stays loopback-only."""
        if not self.auth_password:
            return True
        try:
            cookies = SimpleCookie(self.headers.get("Cookie", ""))
            token = cookies.get(ACCESS_COOKIE)
        except (CookieError, ValueError):
            return False
        return bool(token and hmac.compare_digest(token.value, self.access_token()))

    def access_token(self) -> str:
        return hmac.new(
            self.auth_password.encode("utf-8"),
            b"302math password-only access session v1",
            hashlib.sha256,
        ).hexdigest()

    def public_path(self, path: str) -> str:
        return (self.base_path or "") + path

    def safe_next_path(self, raw: str) -> str:
        candidate = raw.strip()
        if candidate.startswith("/") and not candidate.startswith("//") and "\r" not in candidate and "\n" not in candidate:
            return candidate
        return self.public_path("/")

    def redirect_to_login(self) -> None:
        location = self.public_path("/login") + "?" + urlencode({"next": self.path})
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def serve_login_page(self, query: str, *, head_only: bool = False, error: str = "") -> None:
        next_path = self.safe_next_path(parse_qs(query).get("next", [self.public_path("/")])[0])
        page = """<!doctype html><html lang=\"zh-CN\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>数二 · 解锁</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f6f7f9;color:#1f2328;font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",\"PingFang SC\",\"Microsoft YaHei\",sans-serif}.card{width:min(360px,calc(100vw - 40px));box-sizing:border-box;background:#fff;border:1px solid #e5e8ec;border-radius:14px;padding:28px 26px;box-shadow:0 8px 30px #1f232812}h1{font-size:20px;margin:0 0 8px}p{color:#656d76;font-size:14px;margin:0 0 20px}.error{color:#cf222e;margin:-8px 0 12px;font-size:13px}input,button{width:100%;box-sizing:border-box;border-radius:8px;font:inherit}input{border:1px solid #d0d7de;padding:10px 12px;font-size:16px}button{margin-top:12px;border:1px solid #2f6feb;background:#2f6feb;color:#fff;padding:10px 12px;cursor:pointer;font-weight:600}</style><main class=\"card\"><h1>数二 · 题型体系</h1><p>输入访问密码后继续。</p>__ERROR__<form method=\"post\" action=\"__ACTION__\"><input type=\"hidden\" name=\"next\" value=\"__NEXT__\"><input name=\"password\" type=\"password\" autocomplete=\"current-password\" placeholder=\"访问密码\" aria-label=\"访问密码\" autofocus required><button type=\"submit\">进入</button></form></main></html>"""
        page = page.replace("__ERROR__", "<div class=\"error\">密码不正确，请重试。</div>" if error else "")
        page = page.replace("__ACTION__", html.escape(self.public_path("/login"), quote=True))
        page = page.replace("__NEXT__", html.escape(next_path, quote=True)).encode("utf-8")
        self.send_response(401 if error else 200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(page)

    def read_request_body(self, *, max_length: int = MAX_REQUEST_BODY) -> bytes | None:
        content_length = self.headers.get("Content-Length")
        if not content_length:
            return b""
        try:
            length = int(content_length)
        except ValueError:
            self.send_error(400, "invalid Content-Length")
            return None
        if length < 0 or length > max_length:
            self.send_error(413, "request body too large")
            return None
        return self.rfile.read(length)

    def login(self, query: str) -> None:
        body = self.read_request_body()
        if body is None:
            return
        try:
            form = parse_qs(body.decode("utf-8"), keep_blank_values=True)
        except UnicodeDecodeError:
            self.serve_login_page(query, error="invalid")
            return
        next_path = self.safe_next_path(form.get("next", parse_qs(query).get("next", [self.public_path("/")]))[0])
        password = form.get("password", [""])[0]
        if not self.auth_password or not hmac.compare_digest(password, self.auth_password):
            self.serve_login_page(urlencode({"next": next_path}), error="invalid")
            return
        cookie_path = self.base_path or "/"
        self.send_response(303)
        self.send_header("Location", next_path)
        self.send_header(
            "Set-Cookie",
            f"{ACCESS_COOKIE}={self.access_token()}; Max-Age={ACCESS_SESSION_SECONDS}; Path={cookie_path}; HttpOnly; SameSite=Lax",
        )
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def logout(self, query: str) -> None:
        next_path = self.safe_next_path(parse_qs(query).get("next", [self.public_path("/")])[0])
        self.send_response(303)
        self.send_header("Location", next_path)
        self.send_header("Set-Cookie", f"{ACCESS_COOKIE}=; Max-Age=0; Path={self.base_path or '/'}; HttpOnly; SameSite=Lax")
        self.end_headers()

    def proxy_to_backend(self, *, backend_path: str, head_only: bool = False) -> None:
        path = urlparse(backend_path).path
        is_draft_upload = self.command == "POST" and (
            PHONE_UPLOAD_PATH.fullmatch(path) or DRAFT_IMAGE_POST_PATH.fullmatch(path)
        )
        body = self.read_request_body(max_length=MAX_DRAFT_REQUEST_BODY if is_draft_upload else MAX_REQUEST_BODY)
        if body is None:
            return

        headers = build_proxy_headers(self.headers, self.client_address[0])

        conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=120)
        started = False
        try:
            conn.request(self.command, backend_path, body=body, headers=headers)
            resp = conn.getresponse()
            self.send_response(resp.status, resp.reason)
            for key, value in resp.getheaders():
                if key.lower() in HOP_BY_HOP_HEADERS:
                    continue
                self.send_header(key, value)
            self.end_headers()
            started = True
            if not head_only:
                while chunk := resp.read(65536):
                    self.wfile.write(chunk)
        except (OSError, http.client.HTTPException) as exc:
            if not started:
                self.send_error(502, "backend is temporarily unavailable")
            else:
                self.log_error("backend stream ended: %s", type(exc).__name__)
                self.close_connection = True
        finally:
            conn.close()

    def proxy_to_newpoints(self, *, backend_path: str, head_only: bool = False) -> None:
        """Independent app; allow photos and stream original books / backups."""
        body = self.read_request_body(max_length=9 * 1024 * 1024)
        if body is None:
            return
        headers = build_proxy_headers(self.headers, self.client_address[0])
        conn = http.client.HTTPConnection(self.newpoints_host, self.newpoints_port, timeout=120)
        started = False
        try:
            conn.request(self.command, backend_path, body=body, headers=headers)
            response = conn.getresponse()
            self.send_response(response.status, response.reason)
            for key, value in response.getheaders():
                if key.lower() not in HOP_BY_HOP_HEADERS:
                    self.send_header(key, value)
            self.end_headers()
            started = True
            if not head_only:
                while chunk := response.read(65536):
                    self.wfile.write(chunk)
        except (OSError, http.client.HTTPException) as exc:
            if not started:
                self.send_error(502, "newpoints is temporarily unavailable")
            else:
                self.log_error("newpoints stream ended: %s", type(exc).__name__)
                self.close_connection = True
        finally:
            conn.close()

    def serve_static(self, raw_path: str, *, head_only: bool = False) -> None:
        path = self.resolve_static_path(raw_path)
        is_asset_request = raw_path.startswith("/assets/")
        if not path.is_file():
            if is_asset_request:
                self.send_error(404)
                return
            path = self.static_root / "index.html"
        if not path.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = b"" if head_only else path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(path.stat().st_size if head_only else len(data)))
        if raw_path.startswith("/assets/"):
            self.send_header("Cache-Control", "public, max-age=2592000, immutable")
        else:
            # The app shell, CSS and JS must move together.  Caching one old
            # file while the password gate serves a new one produces a raw,
            # half-loaded page after a deployment.
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if data:
            self.wfile.write(data)

    def resolve_static_path(self, raw_path: str) -> Path:
        path = posixpath.normpath(unquote(raw_path.split("?", 1)[0]))
        if path in {"", "."}:
            path = "/"
        parts = [part for part in path.split("/") if part and part not in {".", ".."}]
        return self.static_root.joinpath(*parts).resolve()

    def log_message(self, fmt: str, *args) -> None:
        message = re.sub(r"(/api/draft-upload/|%2Fapi%2Fdraft-upload%2F)[A-Za-z0-9_-]+",
                         r"\1[redacted]", fmt % args, flags=re.IGNORECASE)
        sys.stderr.write("%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), message))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="数二前端服务:静态托管 frontend/ 并把 /api 反代到后端(无 Docker/nginx)。前端是原生 SPA,没有构建步骤。")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--backend", default="http://127.0.0.1:8302")
    parser.add_argument("--newpoints-backend", default="http://127.0.0.1:8312")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5302)
    parser.add_argument("--base-path", default="")
    parser.add_argument("--auth-password", default="")
    parser.add_argument("--auth-password-file", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    static_root = args.root.expanduser().resolve()
    if not (static_root / "index.html").is_file():
        raise SystemExit(f"frontend index.html not found under {static_root}")
    backend = urlparse(args.backend)
    if backend.scheme not in {"http", ""}:
        raise SystemExit("Only http backend URLs are supported")
    host = backend.hostname or "127.0.0.1"
    port = backend.port or 8302
    newpoints = urlparse(args.newpoints_backend)
    if newpoints.scheme not in {"http", ""} or newpoints.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("Newpoints backend must use loopback HTTP")
    auth_password = args.auth_password
    if args.auth_password_file:
        try:
            auth_password = args.auth_password_file.read_text(encoding="utf-8").rstrip("\r\n")
        except OSError as exc:
            raise SystemExit(f"cannot read auth password file: {exc}") from exc
    if args.auth_password and args.auth_password_file:
        raise SystemExit("use only one of --auth-password or --auth-password-file")
    FrontendProxyHandler.static_root = static_root
    FrontendProxyHandler.backend_host = host
    FrontendProxyHandler.backend_port = port
    FrontendProxyHandler.backend_scheme = backend.scheme or "http"
    FrontendProxyHandler.newpoints_host = newpoints.hostname
    FrontendProxyHandler.newpoints_port = newpoints.port or 8312
    base_path = "/" + args.base_path.strip("/") if args.base_path.strip("/") else ""
    FrontendProxyHandler.base_path = base_path
    FrontendProxyHandler.auth_password = auth_password
    server = ThreadingHTTPServer((args.host, args.port), FrontendProxyHandler)
    auth_state = "enabled" if auth_password else "disabled (local-only development)"
    print(f"serving {static_root} on {args.host}:{args.port}, base {base_path or '/'}; proxying /api to {host}:{port}; auth {auth_state}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
