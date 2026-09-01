import http.cookiejar
import http.server
import importlib.util
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROXY_PATH = ROOT / 'scripts' / 'local_frontend_proxy.py'
SPEC = importlib.util.spec_from_file_location('local_frontend_proxy', PROXY_PATH)
proxy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proxy)


class JsonBackend(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        payload = json.dumps({'path': self.path}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_):
        pass


class ProxyTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        Path(self.tmpdir.name, 'index.html').write_text('<h1>math</h1>', encoding='utf-8')
        Path(self.tmpdir.name, 'style.css').write_text('body{color:#123}', encoding='utf-8')

        self.backend = http.server.ThreadingHTTPServer(('127.0.0.1', 0), JsonBackend)
        self.backend_thread = threading.Thread(target=self.backend.serve_forever, daemon=True)
        self.backend_thread.start()

        proxy.FrontendProxyHandler.static_root = Path(self.tmpdir.name).resolve()
        proxy.FrontendProxyHandler.backend_host = '127.0.0.1'
        proxy.FrontendProxyHandler.backend_port = self.backend.server_port
        proxy.FrontendProxyHandler.backend_scheme = 'http'
        proxy.FrontendProxyHandler.base_path = ''
        proxy.FrontendProxyHandler.auth_password = 'password'
        self.frontend = http.server.ThreadingHTTPServer(('127.0.0.1', 0), proxy.FrontendProxyHandler)
        self.frontend_thread = threading.Thread(target=self.frontend.serve_forever, daemon=True)
        self.frontend_thread.start()
        self.base_url = 'http://127.0.0.1:%d' % self.frontend.server_port

    def tearDown(self):
        self.frontend.shutdown()
        self.backend.shutdown()
        self.frontend.server_close()
        self.backend.server_close()
        self.tmpdir.cleanup()

    def test_default_base_path_preserves_api_path_after_password_only_login(self):
        with urllib.request.urlopen(self.base_url + '/api/tree') as response:
            page = response.read().decode()
        self.assertIn('name="password"', page)
        self.assertNotIn('name="username"', page)

        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        request = urllib.request.Request(
            self.base_url + '/login',
            data=b'password=password&next=%2Fapi%2Ftree',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        with opener.open(request) as response:
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertEqual(json.loads(response.read()), {'path': '/api/tree'})
        self.assertTrue(any(cookie.name == proxy.ACCESS_COOKIE and cookie.has_nonstandard_attr('HttpOnly') for cookie in jar))
        with opener.open(self.base_url + '/style.css') as response:
            self.assertEqual(response.headers['Content-Type'], 'text/css')
            self.assertEqual(response.headers['Cache-Control'], 'no-store')

    def test_bad_password_is_rejected(self):
        request = urllib.request.Request(
            self.base_url + '/login',
            data=b'password=wrong',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        with self.assertRaises(urllib.error.HTTPError) as rejected:
            urllib.request.urlopen(request)
        self.assertEqual(rejected.exception.code, 401)

    def test_health_check_stays_available_without_credentials(self):
        with urllib.request.urlopen(self.base_url + '/healthz') as response:
            self.assertEqual(response.read(), b'ok\n')


if __name__ == '__main__':
    unittest.main()
