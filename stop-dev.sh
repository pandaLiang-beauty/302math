#!/usr/bin/env bash
set -euo pipefail

# 只停止这个项目自己启动的进程；绝不按泛化的 “server.py” 误杀其他项目。

ROOT_DIR="${STUDY_PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}"
PY_BIN="$ROOT_DIR/backend/.venv/bin/python"
stopped_pids=" "

stop_pid_file() {
  local pid_file="$1" expected_prefix="$2" pid args
  [[ -s "$pid_file" ]] || return 0
  pid="$(tr -cd '0-9' < "$pid_file")"
  if [[ -n "$pid" ]] && args="$(ps -p "$pid" -o args= 2>/dev/null)" && [[ "$args" == "$expected_prefix"* ]]; then
    kill "$pid" 2>/dev/null || true
    stopped_pids+="$pid "
    echo "stopped $pid"
  elif [[ -n "$pid" ]]; then
    echo "忽略不匹配的 pid 文件：$pid_file（pid $pid 不属于 302math）" >&2
  fi
  rm -f "$pid_file"
}

stop_pid_file "$ROOT_DIR/backend/server.pid" "$PY_BIN server.py"
stop_pid_file "$ROOT_DIR/frontend/server.pid" "$PY_BIN scripts/local_frontend_proxy.py --root $ROOT_DIR/frontend"

# pid 文件丢失时仅匹配本项目的绝对解释器路径和前端根目录。
while read -r pid args; do
  [[ "$stopped_pids" == *" $pid "* ]] && continue
  if [[ "$args" == "$PY_BIN server.py"* ]] || [[ "$args" == "$PY_BIN scripts/local_frontend_proxy.py --root $ROOT_DIR/frontend"* ]]; then
    kill "$pid" 2>/dev/null || true
    echo "stopped $pid (recovered)"
  fi
done < <(ps -eo pid=,args=)

for _ in $(seq 1 30); do
  still_running=0
  while read -r _pid args; do
    if [[ "$args" == "$PY_BIN server.py"* ]] || [[ "$args" == "$PY_BIN scripts/local_frontend_proxy.py --root $ROOT_DIR/frontend"* ]]; then
      still_running=1
      break
    fi
  done < <(ps -eo pid=,args=)
  [[ "$still_running" -eq 0 ]] && break
  sleep 0.1
done

echo "math dev 已停止。"
