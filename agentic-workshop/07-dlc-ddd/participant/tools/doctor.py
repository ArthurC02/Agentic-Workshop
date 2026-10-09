"""環境健檢：逐項檢查 DLC 會踩到的 Windows 陷阱，並印出修正方式。在 Repo 根目錄執行：

  py -3.13 -X utf8 ../../tools/doctor.py

[OK] 通過、[!!] 必須修正、[--] 提醒。任何 [!!] 時 exit 1。
"""
from __future__ import annotations

import argparse
import json
import locale
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402

PLUGIN_VERSION = "0.2.2"


def run(*command: str) -> tuple[int, str]:
    try:
        done = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError as error:
        return 127, str(error)
    return done.returncode, (done.stdout + done.stderr).strip()


def version_tuple(text: str) -> tuple[int, ...]:
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(part or 0) for part in match.groups()) if match else ()


def key_checks(repo: Path) -> list[tuple[str, str, str]]:
    """金鑰必須在 Repo 外（預設 ~/.dlc-keys）；Repo 內出現金鑰就警告。"""
    keys = dmlib.key_dir().resolve()
    found = [p for p in (repo / ".dlc-keys").rglob("*") if p.is_file()] if (repo / ".dlc-keys").is_dir() else []
    # Plugin 的金鑰檔名是 signing-key（不是 id_*）；以 git 設定的簽章金鑰位置為準。
    code, signing = run("git", "-C", str(repo), "config", "user.signingkey")
    if code == 0 and signing and not signing.startswith("key::") and Path(repo, signing).resolve().is_relative_to(repo.resolve()):
        found.append(Path(signing))
    if found:
        return [("!!", "金鑰在 Repo 外", f"Repo 內有金鑰：{found[0]}。請移到 {dmlib.key_dir()} 並從 Repo 刪除（scan-secrets 會掃到）。")]
    return [("OK", "金鑰在 Repo 外", f"預設金鑰資料夾 {keys}")]


def checks(plugin: str | None) -> list[tuple[str, str, str]]:
    """回傳 (等級, 項目, 說明或修正)；等級為 OK、!!、--。"""
    results = []
    if os.name == "nt":
        code, out = run("py", "-3.13", "-c", "import sys; print(sys.version)")
        results.append(("OK", "Python 3.13（py launcher）", out.splitlines()[0]) if code == 0 else
                       ("!!", "Python 3.13（py launcher）", "安裝 Python 3.13（python.org 安裝程式，勾選 py launcher）。"))
    else:
        ok = sys.version_info[:2] == (3, 13)
        results.append(("OK" if ok else "!!", "Python 3.13", sys.version.split()[0] if ok else
                        "請用 Python 3.13 執行（起始 Repo 要求 >=3.13,<3.14）。"))
    if sys.flags.utf8_mode:
        results.append(("OK", "UTF-8 模式（-X utf8）", "本次以 -X utf8 執行"))
    else:
        level = "!!" if locale.getpreferredencoding(False).lower() in ("cp950", "big5", "mbcs") else "--"
        results.append((level, "UTF-8 模式（-X utf8）",
                        "所有 Plugin 指令請經 tools/dm.ps1 或 dm.sh（已固定 -X utf8），否則 cp950 會 UnicodeDecodeError。"))
    python = shutil.which("python")
    if python is None or "WindowsApps" in python:
        results.append(("!!", "PATH 上的 python（pre-push hook 會呼叫）",
                        f"目前是 {python or '找不到'}。push 前先啟用 .venv：PowerShell `.\\.venv\\Scripts\\Activate.ps1`；"
                        "Git Bash `source .venv/Scripts/activate`。"))
    else:
        code, out = run(python, "--version")
        results.append(("OK" if code == 0 else "!!", "PATH 上的 python（pre-push hook 會呼叫）", f"{python} → {out}"))
    code, out = run("git", "--version")
    git_ok = code == 0 and version_tuple(out) >= (2, 34)
    results.append(("OK" if git_ok else "!!", "git ≥ 2.34（SSH 簽章）", out if git_ok else
                    f"目前：{out or '找不到 git'}。請安裝 Git for Windows 2.34 以上。"))
    keygen = shutil.which("ssh-keygen")
    results.append(("OK", "ssh-keygen", f"{keygen}（同一組全程用同一個 shell）") if keygen else
                   ("!!", "ssh-keygen", "找不到。啟用 Windows「OpenSSH 用戶端」功能，或改在 Git Bash 執行。"))
    try:
        root = dmlib.plugin_root(plugin)
        manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        version = manifest.get("version")
        results.append(("OK" if version == PLUGIN_VERSION else "!!", "domain-memory Plugin",
                        f"{root}（版本 {version}）" if version == PLUGIN_VERSION else
                        f"{root} 版本是 {version}，本課程固定 {PLUGIN_VERSION}。"))
    except (SystemExit, OSError, ValueError) as error:
        results.append(("!!", "domain-memory Plugin", str(error)))
    if Path(".git").exists():
        results.extend(key_checks(Path.cwd()))
        attrs = Path(".gitattributes")
        has_rule = attrs.exists() and "* -text" in attrs.read_text(encoding="utf-8", errors="replace").splitlines()
        results.append(("OK", ".gitattributes 含 `* -text`", "換行不被轉換，簽章與雜湊穩定") if has_rule else
                       ("!!", ".gitattributes 含 `* -text`", "在 .gitattributes 加一行 `* -text`，避免 CRLF 轉換破壞簽章／雜湊。"))
        for key in ("user.name", "user.email"):
            code, out = run("git", "config", key)
            results.append(("OK", f"git {key}", out) if code == 0 and out else
                           ("!!", f"git {key}", f"在本 Repo 設定：git config --local {key} \"...\"（不要改 global）"))
    else:
        results.append(("--", "git repo", "目前目錄不是 git repo；D2 前請 git init 並 commit 起始程式。"))
    venv = Path(".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python")
    results.append(("OK", ".venv", str(venv)) if venv.exists() else
                    ("--", ".venv", "尚未建立：py -3.13 -m venv .venv，再 pip install -r requirements.txt"))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="檢查 DLC 的 Windows 環境陷阱並列出修正方式。",
                                     epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plugin", help="Plugin 資料夾（預設 DOMAIN_MEMORY_PLUGIN 或 vendor/domain-memory）")
    args = parser.parse_args(argv)
    results = checks(args.plugin)
    for level, item, detail in results:
        print(f"[{level}] {item}：{detail}")
    failed = sum(level == "!!" for level, _, _ in results)
    print("全部必要項目通過。" if not failed else f"{failed} 項必須修正。")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
