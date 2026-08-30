#!/usr/bin/env bash
set -euo pipefail

# 停止数二的后端(:8302) 与前端(:5302)。不用 set -e 的严格模式挡住清理：允许部分本就没起。

ROOT_DIR="${STUDY_PROJECT_ROOT:-/root/sysStuByAI/302math}"
BACKEND_PORT="${STUDY_BACKEND_PORT:-8302}"
FRONTEND_PORT="${STUDY_FRONTEND_PORT:-5302}"

for pid_file in "$ROOT_DIR/backend/server.pid" "$ROOT_DIR/frontend/server.pid"; do
  if [[ -s "$pid_file" ]]; then
    pid="$(tr -cd '0-9' < "$pid_file")"
    if [[ -n "$pid" ]] && ps -p "$pid" >/dev/null 2>&1; then
      kill "$pid"
      echo "stopped $pid"
    fi
    rm -f "$pid_file"
  fi
done

# 兜底：pid 文件丢了也能按命令行特征清掉。
pkill -f "[.]venv/bin/python server.py" 2>/dev/null || true
pkill -f "[l]ocal_frontend_proxy.py .*--port $FRONTEND_PORT" 2>/dev/null || true

echo "math dev 已停止 (backend :$BACKEND_PORT, frontend :$FRONTEND_PORT)。"
