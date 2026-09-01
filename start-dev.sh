#!/usr/bin/env bash
set -euo pipefail

# 数二开发启动：后端 :8302、前端代理 :5302。前端代理是唯一对 Tunnel 暴露的入口。

ROOT_DIR="${STUDY_PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}"
BACKEND_HOST="${STUDY_BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${STUDY_BACKEND_PORT:-8302}"
FRONTEND_HOST="${STUDY_FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${STUDY_FRONTEND_PORT:-5302}"
PY_BIN="$ROOT_DIR/backend/.venv/bin/python"
ENV_FILE="$ROOT_DIR/backend/.env.local"
AUTH_FILE="$ROOT_DIR/backend/.access-password"
export STUDY_BACKEND_PORT="$BACKEND_PORT"

[[ -x "$PY_BIN" ]] || { echo "缺少虚拟环境 backend/.venv（用 python3 -m venv 建）" >&2; exit 1; }
[[ -f "$ROOT_DIR/frontend/index.html" ]] || { echo "缺少 frontend/index.html" >&2; exit 1; }

read_env_value() {
  local key="$1" line
  [[ -f "$ENV_FILE" ]] || return 1
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "$line" || "$line" == "#"* ]] && continue
    if [[ "$line" == "$key="* ]]; then
      printf '%s' "${line#*=}"
      return 0
    fi
  done < "$ENV_FILE"
  return 1
}

ACCESS_PASSWORD="${STUDY_ACCESS_PASSWORD:-$(read_env_value STUDY_ACCESS_PASSWORD || true)}"
generated_password=0
if [[ -z "$ACCESS_PASSWORD" && -s "$AUTH_FILE" ]]; then
  ACCESS_PASSWORD="$(< "$AUTH_FILE")"
fi
if [[ -z "$ACCESS_PASSWORD" ]]; then
  umask 077
  ACCESS_PASSWORD="$("$PY_BIN" -c 'import secrets; print(secrets.token_urlsafe(24))')"
  generated_password=1
fi
umask 077
printf '%s\n' "$ACCESS_PASSWORD" > "$AUTH_FILE"

if curl --noproxy '*' -fs -o /dev/null "http://$BACKEND_HOST:$BACKEND_PORT/api/health"; then
  echo "后端 $BACKEND_HOST:$BACKEND_PORT 已在运行；请先执行 bash stop-dev.sh。" >&2
  exit 1
fi
if curl --noproxy '*' -fs -o /dev/null "http://$FRONTEND_HOST:$FRONTEND_PORT/healthz"; then
  echo "前端 $FRONTEND_HOST:$FRONTEND_PORT 已在运行；请先执行 bash stop-dev.sh。" >&2
  exit 1
fi

cd "$ROOT_DIR/backend"
setsid nohup "$PY_BIN" server.py > "$ROOT_DIR/backend/server.log" 2>&1 &
backend_pid=$!
echo "$backend_pid" > "$ROOT_DIR/backend/server.pid"

backend_ready=0
for _ in $(seq 1 40); do
  if curl --noproxy '*' -fs -o /dev/null "http://$BACKEND_HOST:$BACKEND_PORT/api/health"; then
    backend_ready=1
    break
  fi
  sleep 0.5
done
if [[ "$backend_ready" -ne 1 ]]; then
  kill "$backend_pid" 2>/dev/null || true
  rm -f "$ROOT_DIR/backend/server.pid"
  echo "后端启动失败；查看 $ROOT_DIR/backend/server.log" >&2
  exit 1
fi

cd "$ROOT_DIR"
setsid nohup "$PY_BIN" scripts/local_frontend_proxy.py --root "$ROOT_DIR/frontend" --backend "http://$BACKEND_HOST:$BACKEND_PORT" --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" --auth-password-file "$AUTH_FILE" > "$ROOT_DIR/frontend/server.log" 2>&1 &
frontend_pid=$!
echo "$frontend_pid" > "$ROOT_DIR/frontend/server.pid"

frontend_ready=0
cookie_jar="$(mktemp)"
trap 'rm -f "$cookie_jar"' EXIT
for _ in $(seq 1 20); do
  if curl --noproxy '*' -fsS -c "$cookie_jar" --data-urlencode "password=$ACCESS_PASSWORD" "http://$FRONTEND_HOST:$FRONTEND_PORT/login" -o /dev/null \
    && curl --noproxy '*' -fsS -b "$cookie_jar" "http://$FRONTEND_HOST:$FRONTEND_PORT/api/health" | grep -q '"ok":true'; then
    frontend_ready=1
    break
  fi
  sleep 0.25
done
if [[ "$frontend_ready" -ne 1 ]]; then
  kill "$frontend_pid" "$backend_pid" 2>/dev/null || true
  rm -f "$ROOT_DIR/frontend/server.pid" "$ROOT_DIR/backend/server.pid"
  echo "前端代理启动失败；查看 $ROOT_DIR/frontend/server.log" >&2
  exit 1
fi

echo "math: frontend http://$FRONTEND_HOST:$FRONTEND_PORT/（只需输入访问密码）"
if [[ "$generated_password" -eq 1 ]]; then
  echo "首次访问密码已生成：$ACCESS_PASSWORD"
  echo "密码保存在 $AUTH_FILE（已被 Git 忽略）；也可在 backend/.env.local 设置 STUDY_ACCESS_PASSWORD 固定它。"
fi
echo "停止：bash stop-dev.sh"
