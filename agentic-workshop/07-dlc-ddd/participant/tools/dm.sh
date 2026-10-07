#!/usr/bin/env sh
# domain-memory 命令前綴（Git Bash / macOS / Linux）。在 Repo 根目錄執行：
#   ../tools/dm.sh readiness
#   ../tools/dm.sh validate            # 自動補 --registry-root domain-memory --repo-root .
# 固定以 Python 3.13 加 -X utf8 執行，避免 cp950 UnicodeDecodeError。
DIR=$(cd "$(dirname "$0")" && pwd)
if command -v py >/dev/null 2>&1; then
  exec py -3.13 -X utf8 "$DIR/dmlib.py" "$@"
fi
exec python3 -X utf8 "$DIR/dmlib.py" "$@"
