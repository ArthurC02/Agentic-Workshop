#!/usr/bin/env sh
# domain-memory 命令前綴（Git Bash / macOS / Linux）。在 Repo 根目錄執行：
#   ../../tools/dm.sh readiness
#   ../../tools/dm.sh validate            # 自動補 --registry-root domain-memory --repo-root .
# 固定以 Python 3.13 加 -X utf8 執行，避免 cp950 UnicodeDecodeError。
# 順序：py -3.13（Git Bash）→ python3.13（macOS／Linux）→ python3（最後才用；macOS 內建的是 3.9，不夠新）。
DIR=$(cd "$(dirname "$0")" && pwd)
if command -v py >/dev/null 2>&1 && py -3.13 -c "" >/dev/null 2>&1; then
  exec py -3.13 -X utf8 "$DIR/dmlib.py" "$@"
fi
command -v python3.13 >/dev/null 2>&1 && exec python3.13 -X utf8 "$DIR/dmlib.py" "$@"
exec python3 -X utf8 "$DIR/dmlib.py" "$@"
