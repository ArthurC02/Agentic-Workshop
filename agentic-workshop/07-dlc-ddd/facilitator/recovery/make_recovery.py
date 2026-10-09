"""Regenerate one DLC Recovery source folder: facilitator/recovery/<seg>/ (spec 11 section 3.2).

    py -3.13 -X utf8 make_recovery.py d1|d2|d3a|d3b|d3c [--plugin <domain-memory folder>]

Output (the folder is deleted and rebuilt; it is what build_delivery_dlc.py packs as recovery-dlc-<seg>):
    smart-ticket-dlc-base/   working tree, no .git (the package builder refuses .git)
    repo.bundle              git history of that tree (branch main); restore with init + fetch + reset
    keys/maintainer.allowed_signers   public only (d2 and later)
    RECOVERY.md              the Runbook recovery-page steps (save, partner signing takeover, verify)

Sources: participant starting repo, evaluation/reference-registry (bundle tag dlc-d2-reviewed, d1 inputs),
evaluation/reference-solutions/<solution> minus evidence/ and SOLUTION-NOTES.md. Nothing else from
evaluation/ is copied. Commits use fixed identities and dates, so repo.bundle is reproducible for d2+;
d1's domain-memory/ carries plugin timestamps (the plugin has no clock override), so it differs per run.
"""
from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DLC = HERE.parents[1]
BASE = DLC / "participant/repository/smart-ticket-dlc-base"
TOOLS = DLC / "participant/tools"
REGISTRY = DLC / "evaluation/reference-registry"
SOLUTIONS = DLC / "evaluation/reference-solutions"
REVIEWED_TAG = "dlc-d2-reviewed"
# segment -> (reference solution folder or None, commit message)
SEGMENTS = {
    "d1": (None, None),
    "d2": (None, None),
    "d3a": ("d3a-e-invoice", "D3a：電子發票（Recovery 參考實作）"),
    "d3b": ("d3b-points-redemption", "D3b：點數折抵（Recovery 參考實作）"),
    "d3c": ("d3c-group-partial-refund", "D3c：團體部分退款（Recovery 參考實作）"),
}
CACHES = shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__", ".pytest_cache", "*.pyc", "*.pyo",
                                ".dlc-keys", "domain-memory", "records")
SOLUTION_SKIP = shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__", ".pytest_cache", "*.pyc", "*.pyo",
                                       ".dlc-keys", "evidence", "SOLUTION-NOTES.md", ".gitignore",
                                       "domain-memory")  # ponytail: recovery = reviewed Registry + solution code; D3 candidates stay in evaluation
PROPOSER = ("DLC Proposer", "proposer@example.com")
DATE = "2026-10-07T12:00:00+08:00"


def run(cmd: list[str], cwd: Path, env: dict | None = None) -> str:
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env={**os.environ, "PYTHONUTF8": "1", **(env or {})})
    if done.returncode != 0:
        raise SystemExit(f"FAILED ({done.returncode}): {' '.join(cmd)}\n{done.stdout}{done.stderr}")
    return done.stdout


def git(cwd: Path, *args: str) -> str:
    # ponytail: fixed identity/date + no signing/eol conversion so the commit hash is reproducible.
    env = {"GIT_AUTHOR_NAME": PROPOSER[0], "GIT_AUTHOR_EMAIL": PROPOSER[1], "GIT_AUTHOR_DATE": DATE,
           "GIT_COMMITTER_NAME": PROPOSER[0], "GIT_COMMITTER_EMAIL": PROPOSER[1], "GIT_COMMITTER_DATE": DATE}
    return run(["git", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", "-c", "pack.threads=1",
                *args], cwd, env)


def dm(repo: Path, plugin: str | None, *args: str) -> str:
    extra = ["--plugin", plugin] if plugin else []
    return run([sys.executable, "-X", "utf8", str(TOOLS / "dmlib.py"), *extra, *args], repo)


def build_d1(work: Path, plugin: str | None, tmp: Path) -> None:
    shutil.copytree(BASE, work, ignore=CACHES)
    git(work, "init", "-q", "-b", "main")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "起始 Repo")
    # Same commands as runbook D1 checkpoints 2-3; D1 never commits domain-memory/ (signing comes first in D2).
    dm(work, plugin, "init-domain-memory", "--output", "domain-memory", "--source", "docs/requirements",
       "--source", "docs/adr", "--source", "src", "--source", "tests", "--exclude", "**/__pycache__/**",
       "--storage-mode", "tracked", "--data-classification", "internal", "--review-mode", "local-draft-only",
       "--source-authority", "DLC Proposer <proposer@example.com>")
    dm(work, plugin, "confirm-sources", "--confirmed-by", "DLC Proposer <proposer@example.com>")
    records = tmp / "d1-records.json"
    shutil.copyfile(REGISTRY / "inputs/d1-records.json", records)
    extra = ["--plugin", plugin] if plugin else []
    run([sys.executable, "-X", "utf8", str(TOOLS / "make_record.py"), "--batch", str(records),
         "--out-dir", str(tmp / "records"), "--upsert", *extra], work)
    dm(work, plugin, "validate")


def build_reviewed(work: Path, solution: str | None, message: str | None) -> None:
    run(["git", "clone", "-q", "--no-checkout", str(REGISTRY / "smart-ticket-dlc-reference.bundle"), str(work)],
        work.parent)
    git(work, "checkout", "-q", "-B", "main", REVIEWED_TAG)
    git(work, "remote", "remove", "origin")
    if solution is None:
        return
    source = SOLUTIONS / solution
    crlf = {}  # tracked file -> had CRLF; the overlay keeps each file's line endings (D3 work rule 9)
    for name in git(work, "ls-files", "-z").split("\0"):
        if name and not name.startswith("domain-memory/") and name not in (".gitignore", ".gitattributes"):
            crlf[name] = b"\r\n" in (work / name).read_bytes()
            (work / name).unlink()
    shutil.copytree(source, work, ignore=SOLUTION_SKIP, dirs_exist_ok=True)
    for name, was_crlf in crlf.items():
        path = work / name
        if path.exists():
            data = path.read_bytes().replace(b"\r\n", b"\n")
            path.write_bytes(data.replace(b"\n", b"\r\n") if was_crlf else data)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", message)


# Same commands as the Runbook "<SEG> Recovery 切換" pages (19/29/39/49/59-recovery-*.md); keep both in sync.
# ponytail: str.format templates, so literal braces in commands/outputs are doubled.
# ponytail: PowerShell stops on cmdlet errors via $ErrorActionPreference and on native exit codes via $LASTEXITCODE;
# Git Bash runs each block as one ( set -e ... ) subshell, so a failure stops the block without killing the Agent's
# persistent shell. Run from the original Repo, so $orig/orig is its root (notes/ and docs/handoffs/ get copied).
SAVE_PS = r"""$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) {{ throw "not in the original Repo" }}
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
if (Test-Path .\resume-{seg}) {{ throw "resume-{seg} already exists: delete C:\dlc-rec\{seg} and resume-{seg}, then rerun" }}
Expand-Archive -Force -LiteralPath "$HOME\Downloads\recovery-dlc-{seg}.zip" -DestinationPath C:\dlc-rec\{seg}
$b = (Get-ChildItem C:\dlc-rec\{seg} -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) {{ throw "repo.bundle not found" }}; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-{seg}
foreach ($d in 'notes', 'docs\handoffs') {{ if (Test-Path "$orig\$d") {{ Copy-Item -Recurse "$orig\$d" ".\resume-{seg}\$d" }} }}"""

SAVE_SH = r"""orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
[ ! -e ./resume-{seg} ] || {{ echo "resume-{seg} already exists: delete /c/dlc-rec/{seg} and resume-{seg}, then rerun" >&2; exit 1; }}
mkdir -p /c/dlc-rec/{seg}
unzip -o -q ~/Downloads/recovery-dlc-{seg}.zip -d /c/dlc-rec/{seg}
rec=$(find /c/dlc-rec/{seg} -name repo.bundle -exec dirname {{}} \; | head -1)
[ -n "$rec" ] || {{ echo "repo.bundle not found" >&2; exit 1; }}
cp -r "$rec/smart-ticket-dlc-base" ./resume-{seg}
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-{seg}/$d"; fi; done"""


def subshell(body: str) -> str:
    """A Git Bash block as one ( set -e ... ) subshell: any failing line stops the block, the Agent's shell survives."""
    return "( set -e\n" + body + "\n)"


STEP_SAVE = r"""## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit，什麼都不寫進原 Repo。Agent 在原 Repo 執行 `git status`、`git log --oneline -3` 並問學員進度，再把 Recovery 複製成和原 Repo 同一層的 `resume-{seg}`（`..\..\tools` 才會指向學員包的工具），原 Repo 有 `notes/`、`docs/handoffs/` 時一併複製過去（後面的段落要讀）。最後把學員的回答、兩個指令的結果與原 Repo 的完整路徑附加到 `resume-{seg}` 的 `notes/{seg}.md`（標題「改用 Recovery 前的狀態」）。複製來的 `notes/` 提到的候選 id 是原 Repo 的，Recovery 的 Registry 不一定有，之後查不到是預期。下面的指令任何一行失敗就停下（PowerShell 用 `$ErrorActionPreference` 與 `$LASTEXITCODE`；Git Bash 整段包在 `( set -e … )` 子 shell 裡，失敗只結束這一段，不會關掉 Agent 的終端機）。中途失敗要重跑時，重跑前先刪除 `C:\dlc-rec\{seg}` 與 `resume-{seg}`（只刪這兩個）。

```powershell
""" + SAVE_PS + r"""
```

```bash
""" + subshell(SAVE_SH) + r"""
```
"""

RESTORE_PS = r"""$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem C:\dlc-rec\{seg} -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) {{ throw "repo.bundle not found" }}; $rec = Split-Path $b
git init -q -b main; if ($LASTEXITCODE) {{ throw "git init failed" }}
git fetch -q "$rec\repo.bundle" main; if ($LASTEXITCODE) {{ throw "git fetch failed" }}
git reset -q FETCH_HEAD; if ($LASTEXITCODE) {{ throw "git reset failed" }}
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short"""

RESTORE_SH = r"""rec=$(find /c/dlc-rec/{seg} -name repo.bundle -exec dirname {{}} \; | head -1)
[ -n "$rec" ] || {{ echo "repo.bundle not found" >&2; exit 1; }}
git init -q -b main
git fetch -q "$rec/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short"""

STEP_TAKEOVER = r"""## 2. 還原簽章歷史並接手簽章（夥伴在 `resume-{seg}` 新開的 Agent 對話）

`repo.bundle` 是 Recovery 的 Git 歷史：Registry 的 commit 都由 Maintainer 金鑰簽章，所以「第一個含 `domain-memory/` 的 commit 是簽章 commit」在新資料夾仍然成立。`keys/maintainer.allowed_signers` 只有**公鑰**，讓 Git 驗得了這些簽章；私鑰不在包裡。所以由夥伴用自己的金鑰（已有 D2 金鑰就沿用，沒有就新建，一律放在 Repo 外的 `.dlc-keys\maintainer\`）接手：加入授權、裝回 pre-push hook，讀過回報、回「同意」後做一個簽章 commit。金鑰、簽章與 commit 只在夥伴自己的 Agent 對話執行；提案者的 Agent 不碰。

```powershell
""" + RESTORE_PS + r"""
..\..\tools\dm.ps1 init-signing-key --principal maintainer@example.com --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit --save "$env:USERPROFILE\.dlc-keys\maintainer\signing.json"; if ($LASTEXITCODE) {{ throw "init-signing-key failed" }}
Get-Content "$rec\keys\maintainer.allowed_signers" | Add-Content (git config --local gpg.ssh.allowedSignersFile)
git log --format='%h %G? %GS %s'
$old = (Get-Content domain-memory\domain-memory-policy.json -Raw | ConvertFrom-Json).review_governance.authorized_signers -join ','
$fp = (Get-Content "$env:USERPROFILE\.dlc-keys\maintainer\signing.json" -Raw | ConvertFrom-Json).fingerprint
..\..\tools\dm.ps1 amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"; if ($LASTEXITCODE) {{ throw "amend-policy failed" }}
..\..\tools\dm.ps1 install-git-hitl-hook; if ($LASTEXITCODE) {{ throw "install-git-hitl-hook failed" }}
..\..\tools\dm.ps1 governance-readiness
```

```bash
""" + subshell(RESTORE_SH + r"""
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/maintainer/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/maintainer/signing.json"
cat "$rec/keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
git log --format='%h %G? %GS %s'
old=$(py -3.13 -c "import json;print(','.join(json.load(open('domain-memory/domain-memory-policy.json',encoding='utf-8'))['review_governance']['authorized_signers']))")
fp=$(py -3.13 -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['fingerprint'])" "$HOME/.dlc-keys/maintainer/signing.json")
../../tools/dm.sh amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness""") + r"""
```

Agent 把結果寫進 `notes/recovery-{seg}.md` 的「簽章接手」（fingerprint 只寫前 12 碼），夥伴回「同意」後：

```powershell
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "{up} Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
```

（Git Bash 把 `..\..\tools\dm.ps1` 換成 `../../tools/dm.sh`。`git add` 的 `docs` 只會加入從原 Repo 複製來的 `docs/handoffs/`，沒有就什麼都不加；commit 後 `git status --short` 是空的。）

**看到什麼算成功**：`git status --short` 只列出從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；`git log` 中 Registry 的三個 commit 為 `G maintainer@example.com`{log_note}；`amend-policy` 回報 `authorized_signers` 從一個 fingerprint 變成兩個；`governance-readiness` 為 `{{"status": "ready", "blocks": []}}`；簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid.`。

- 附加 Maintainer 公鑰那一行不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 指向只含夥伴金鑰的檔案，少了它，歷史上 Maintainer 簽的 commit 就驗不過，之後 push 會被 hook 以「Git commit signature is invalid」拒絕。
- 之後 D3、D4 的 commit 照 Runbook 由夥伴的對話簽章。私鑰永遠不要 commit、不要放進 ZIP 或截圖。
"""

STEP_VERIFY = r"""## 3. 建環境並驗證（提案者在 `resume-{seg}` 新開的 Agent 對話）

```powershell
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
..\..\tools\dm.ps1 validate --require-reviewed
..\..\tools\dm.ps1 verify-audit
..\..\tools\dm.ps1 verify-evidence
```

（Git Bash 用 `.venv/Scripts/python.exe` 與 `../../tools/dm.sh`。）

**看到什麼算成功**：pytest 全部 passed；`Registry is valid.`（帶 `--require-reviewed`：全部是已審查事實）；verify-audit `"status": "valid"`；{evidence_note}。結果寫進 `notes/recovery-{seg}.md` 的「環境與驗證」，最後一行寫「{up} 的成果由 Recovery 提供，不是我們自己完成」；不 commit（下一次由夥伴的對話一起 commit）。
"""

INTRO = {
    "d2": """# D2 Recovery

內容：起始 Repo 加上已審查、簽章並套用的 Registry（Change Package `CP-CORE-001`，proposer：Proposer，reviewer：Maintainer），以及它的 Git 歷史 `repo.bundle` 與 Maintainer 公鑰 `keys/maintainer.allowed_signers`。Policy 為 `scm-verified`／`git-signed-commit`／`git-push`。""",
}
INTRO_SOLUTION = """# {up} Recovery

內容：D2 的 reviewed Registry，加上 {up} 參考實作（程式、測試、文件）作為一個未簽章、未碰 Registry 的 commit「{message}」，以及 Git 歷史 `repo.bundle` 與 Maintainer 公鑰 `keys/maintainer.allowed_signers`。Registry 沒有新增候選：下一段的新事實由學員同意後，Agent 依 Runbook 檢查點 5 的提示詞以 `make_record.py --allow-unclassified --upsert` 登記為候選；`verify-evidence` 回報的 stale 是已審查事實所引用的那幾行被實作改過，留到 D4 以新的候選更新。"""

USAGE = """使用 Recovery 不算自己完成 {up}。學員照 Runbook「{up} Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。"""

STEP_PUSH = r"""## 4. （選做）push 檢查（夥伴的 Agent 對話，步驟 3 建好 `.venv` 之後）

Recovery 沒有 CP-D2-001，D2 檢查點 6 的 push 在這裡補做；hook 逐一檢查碰到 Registry 的 commit。不 commit。

```powershell
py -3.13 -X utf8 ..\..\tools\setup_remote.py
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = '1'
git push -u origin HEAD
```

```bash
py -3.13 -X utf8 ../../tools/setup_remote.py
source .venv/Scripts/activate
export PYTHONUTF8=1
git push -u origin HEAD
```

**看到什麼算成功**：hook 共印出四行 `Git governance is valid.`（Recovery 歷史裡碰到 Registry 的三個 commit，加上步驟 2 的簽章 commit），最後 `* [new branch] HEAD -> main`。被拒時不要用 `--no-verify` 繞過。
"""

D1_INTRO = """# D1 Recovery

內容：起始 Repo（`smart-ticket-dlc-base/`）、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。`repo.bundle` 只有一個未簽章、不含 `domain-memory/` 的「起始 Repo」commit：依流程 D1 不 commit Registry，`domain-memory/` 還原後是未追蹤，等 D2 夥伴設好簽章後才 commit。D1 沒有簽章，所以兩步都由提案者的 Agent 執行，沒有任何 commit。"""

D1_RESTORE = r"""## 2. 還原並驗證（提案者在 `resume-d1` 新開的 Agent 對話）

```powershell
""" + RESTORE_PS.format(seg="d1") + r"""
py -3.13 -m venv .venv; if ($LASTEXITCODE) { throw "venv failed" }
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt; if ($LASTEXITCODE) { throw "pip install failed" }
& '.\.venv\Scripts\python.exe' -m pytest -q; if ($LASTEXITCODE) { throw "pytest failed" }
..\..\tools\dm.ps1 validate; if ($LASTEXITCODE) { throw "validate failed" }
..\..\tools\dm.ps1 verify-evidence
```

```bash
""" + subshell(RESTORE_SH.format(seg="d1") + r"""
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
../../tools/dm.sh validate
../../tools/dm.sh verify-evidence""") + r"""
```

**看到什麼算成功**：`git status --short` 只有 `?? domain-memory/` 與從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；pytest 全部 passed；`Registry is valid.`；verify-evidence 的 stale、missing、invalid 都是 0。結果寫進 `notes/recovery-d1.md`，開頭寫「D1 的成果由 Recovery 提供」。

## 接續 D2

從 Runbook D2 檢查點 1 開始，夥伴在 `resume-d1` 開自己的 Agent 對話。簽章必須在第一個 Registry commit 之前設好：**不要讓 Agent 先 `git add domain-memory`**。
"""


def recovery_md(seg: str, solution: str | None, message: str | None) -> str:
    up = seg.capitalize()
    usage = USAGE.format(up=up)
    if seg == "d1":
        return "\n\n".join([D1_INTRO, usage, STEP_SAVE.format(seg=seg) + "\n" + D1_RESTORE])
    intro = INTRO.get(seg) or INTRO_SOLUTION.format(up=up, message=message)
    base_note = "最下面的「Smart Ticket DLC base」（起始程式）"
    log_note = ("，最上面的「" + message + "」與" + base_note + "為 `N`（未簽章，不碰 Registry，hook 允許）"
                if solution else "，" + base_note + "為 `N`（未簽章，不碰 Registry，hook 允許）")
    evidence_note = ("verify-evidence 多數 `current`，引用行內容被實作改過的證據顯示 `stale`、exit 1，屬預期，留到 D4 處理"
                     if solution else "verify-evidence 全部 `current`")
    return "\n\n".join([intro, usage, STEP_SAVE.format(seg=seg) + "\n"
                        + STEP_TAKEOVER.format(seg=seg, up=up, log_note=log_note) + "\n"
                        + STEP_VERIFY.format(seg=seg, up=up, evidence_note=evidence_note)]
                       + ([STEP_PUSH] if seg == "d2" else []))


def _writable_retry(func, path, _exc) -> None:
    """OneDrive marks folders read-only; clear the flag and retry the delete."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def generate(seg: str, plugin: str | None) -> Path:
    solution, message = SEGMENTS[seg]
    out = HERE / seg
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        work = tmp / "smart-ticket-dlc-base"
        if seg == "d1":
            build_d1(work, plugin, tmp)
        else:
            build_reviewed(work, solution, message)
        if out.exists():
            shutil.rmtree(out, onexc=_writable_retry)
        out.mkdir(parents=True)
        git(work, "bundle", "create", "-q", str(out / "repo.bundle"), "main")
        shutil.copytree(work, out / "smart-ticket-dlc-base", ignore=shutil.ignore_patterns(".git"))
    if seg != "d1":
        (out / "keys").mkdir()
        shutil.copyfile(REGISTRY / "keys/maintainer.allowed_signers", out / "keys/maintainer.allowed_signers")
    (out / "RECOVERY.md").write_text(recovery_md(seg, solution, message), encoding="utf-8", newline="\n")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("segment", help="d1, d2, d3a, d3b, d3c (dlc-rec- prefix accepted)")
    parser.add_argument("--plugin", help="domain-memory plugin folder (default: DOMAIN_MEMORY_PLUGIN or vendor/)")
    args = parser.parse_args()
    seg = args.segment.removeprefix("dlc-rec-")
    if seg not in SEGMENTS:
        parser.error(f"unknown segment {args.segment}")
    print(generate(seg, args.plugin))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
