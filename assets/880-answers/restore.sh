#!/usr/bin/env bash
# 把 part.* 分卷还原成原始 PDF（放回 302math 项目根目录）并校验 sha256。
# 用途：《27版880参考答案》原件 232M，超过 Gitee 单文件 100M 上限，故拆分入库。
set -euo pipefail
cd "$(dirname "$0")"

OUT="../../【PDF】27版880参考答案(1).pdf"

if ! ls part.* >/dev/null 2>&1; then
  echo "✗ 当前目录没有 part.* 分卷，确认已完整 clone/pull" >&2
  exit 1
fi

cat part.* > "$OUT"
echo "已还原：$(cd ../.. && pwd)/【PDF】27版880参考答案(1).pdf"

expected="$(cut -d' ' -f1 SHA256SUMS.txt)"
actual="$(sha256sum "$OUT" | cut -d' ' -f1)"
if [ "$expected" = "$actual" ]; then
  echo "✓ sha256 校验通过，与服务器上的原件完全一致"
else
  echo "✗ sha256 不一致（期望 $expected，实际 $actual），分卷可能不完整" >&2
  exit 1
fi
