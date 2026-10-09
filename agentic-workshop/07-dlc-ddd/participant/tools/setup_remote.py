"""建立本機 bare remote，讓 pre-push hook 有地方可以 push（不需要 GitHub）。

  py -3.13 -X utf8 ../../tools/setup_remote.py                # 建 ../<repo 名>-remote.git 並設為 origin
  py -3.13 -X utf8 ../../tools/setup_remote.py --path D:/x.git --name origin

之後：先啟用 .venv（hook 會呼叫裸 python），再 `git push -u origin HEAD`。
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def git(*args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def setup(path: Path, name: str) -> Path:
    top = git("rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise SystemExit("目前目錄不是 git repo；請在 Repo 根目錄執行。")
    if not (path / "HEAD").exists():
        done = git("init", "--bare", "--quiet", str(path))
        if done.returncode != 0:
            raise SystemExit(f"建立 bare repo 失敗：{done.stderr.strip()}")
    url = path.resolve().as_posix()
    existing = git("remote", "get-url", name)
    done = git("remote", "set-url" if existing.returncode == 0 else "add", name, url)
    if done.returncode != 0:
        raise SystemExit(f"設定 remote {name} 失敗：{done.stderr.strip()}")
    return path.resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="建立本機 bare remote 並設定為 git remote。",
                                     epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", help="bare repo 位置（預設 ../<repo 名>-remote.git）")
    parser.add_argument("--name", default="origin", help="remote 名稱（預設 origin）")
    args = parser.parse_args(argv)
    path = Path(args.path) if args.path else Path("..") / f"{Path.cwd().name}-remote.git"
    remote = setup(path, args.name)
    print(f"remote {args.name} → {remote}")
    print(f"下一步：啟用 .venv 後 git push -u {args.name} HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
