#!/usr/bin/env bash
set -euo pipefail

# 数二开发启动脚本：后台拉起后端(uvicorn :8302) 与前端(local_frontend_proxy :5302)。
# 端口口径：前端 5+科目代码、后端 8+科目代码（302 → 5302/8302），子域能直接推出端口。
# 前端是原生 SPA（没有 npm/vite/构建步骤），所以前端服务就是一个静态托管 + /api 反代。
# Cloudflare Tunnel 只指 5302，后端 8302 不对外。

ROOT_DIR="${STUDY_PROJECT_ROOT:-/root/sysStuByAI/302math}"
BACKEND_HOST="${STUDY_BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${STUDY_BACKEND_PORT:-8302}"
FRONTEND_HOST="${STUDY_FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${STUDY_FRONTEND_PORT:-5302}"
export STUDY_BACKEND_PORT="$BACKEND_PORT"

PY_BIN="$ROOT_DIR/backend/.venv/bin/python"
[[ -x "$PY_BIN" ]] || { echo "缺少虚拟环境 backend/.venv（用 python3 -m venv 建）" >&2; exit 1; }
[[ -f "$ROOT_DIR/frontend/index.html" ]] || { echo "缺少 frontend/index.html" >&2; exit 1; }

# 后端：server.py 的 __main__ 会读 STUDY_BACKEND_PORT。
cd "$ROOT_DIR/backend"
setsid nohup "$PY_BIN" server.py > "$ROOT_DIR/backend/server.log" 2>&1 &
echo $! > "$ROOT_DIR/backend/server.pid"

# 前端：等后端起来再拉，省得首屏那几个 /api 请求撞 502。
for _ in $(seq 1 40); do
  curl --noproxy '*' -fs -o /dev/null "http://$BACKEND_HOST:$BACKEND_PORT/api/tree" && break
  sleep 0.5
done

cd "$ROOT_DIR"
setsid nohup "$PY_BIN" scripts/local_frontend_proxy.py \
  --root "$ROOT_DIR/frontend" \
  --backend "http://$BACKEND_HOST:$BACKEND_PORT" \
  --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" \
  > "$ROOT_DIR/frontend/server.log" 2>&1 &
echo $! > "$ROOT_DIR/frontend/server.pid"

echo "math: backend http://$BACKEND_HOST:$BACKEND_PORT, frontend http://$FRONTEND_HOST:$FRONTEND_PORT/"
echo "停止：bash stop-dev.sh"
