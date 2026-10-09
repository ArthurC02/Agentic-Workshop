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
    for name in git(work, "ls-files", "-z").split("\0"):
        if name and not name.startswith("domain-memory/") and name not in (".gitignore", ".gitattributes"):
            (work / name).unlink()
    shutil.copytree(source, work, ignore=SOLUTION_SKIP, dirs_exist_ok=True)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", message)


# Same commands as the Runbook "<SEG> Recovery 切換" pages (19/29/39/49/59-recovery-*.md); keep both in sync.
# ponytail: str.format templates, so literal braces in commands/outputs are doubled.
STEP_SAVE = r"""## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit。Agent 先把原 Repo 的 `git status`、`git log --oneline -3` 與學員回答的進度寫進原 Repo 的 `notes/{seg}.md`（標題「改用 Recovery 前的狀態」），再把 Recovery 複製成和原 Repo 同一層的 `resume-{seg}`（`..\..\tools` 才會指向學員包的工具）。

```powershell
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-{seg}.zip" -DestinationPath C:\dlc-rec\{seg}
$rec = Split-Path (Get-ChildItem C:\dlc-rec\{seg} -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) {{ throw "repo.bundle not found" }}
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-{seg}
```

```bash
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
mkdir -p /c/dlc-rec/{seg}
unzip -q ~/Downloads/recovery-dlc-{seg}.zip -d /c/dlc-rec/{seg}
rec=$(find /c/dlc-rec/{seg} -name repo.bundle -exec dirname {{}} \; | head -1)
[ -n "$rec" ] || exit 1
cp -r "$rec/smart-ticket-dlc-base" ./resume-{seg}
```
"""

RESTORE_PS = r"""$rec = Split-Path (Get-ChildItem C:\dlc-rec\{seg} -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) {{ throw "repo.bundle not found" }}
git init -q -b main
git fetch -q "$rec\repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short"""

RESTORE_SH = r"""rec=$(find /c/dlc-rec/{seg} -name repo.bundle -exec dirname {{}} \; | head -1)
[ -n "$rec" ] || exit 1
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
..\..\tools\dm.ps1 init-signing-key --principal maintainer@example.com --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit --save "$env:USERPROFILE\.dlc-keys\maintainer\signing.json"
Get-Content "$rec\keys\maintainer.allowed_signers" | Add-Content (git config --local gpg.ssh.allowedSignersFile)
git log --format='%h %G? %GS %s'
$old = (Get-Content domain-memory\domain-memory-policy.json -Raw | ConvertFrom-Json).review_governance.authorized_signers -join ','
$fp = (Get-Content "$env:USERPROFILE\.dlc-keys\maintainer\signing.json" -Raw | ConvertFrom-Json).fingerprint
..\..\tools\dm.ps1 amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"
..\..\tools\dm.ps1 install-git-hitl-hook
..\..\tools\dm.ps1 governance-readiness
```

```bash
""" + RESTORE_SH + r"""
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/maintainer/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/maintainer/signing.json"
cat "$rec/keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
git log --format='%h %G? %GS %s'
old=$(py -3.13 -c "import json;print(','.join(json.load(open('domain-memory/domain-memory-policy.json',encoding='utf-8'))['review_governance']['authorized_signers']))")
fp=$(py -3.13 -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['fingerprint'])" "$HOME/.dlc-keys/maintainer/signing.json")
../../tools/dm.sh amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness
```

Agent 把結果寫進 `notes/recovery-{seg}.md` 的「簽章接手」（fingerprint 只寫前 12 碼），夥伴回「同意」後：

```powershell
git add domain-memory notes
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "{up} Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
```

（Git Bash 把 `..\..\tools\dm.ps1` 換成 `../../tools/dm.sh`。）

**看到什麼算成功**：`git status --short` 沒有輸出；`git log` 中 Registry 的三個 commit 為 `G maintainer@example.com`{log_note}；`amend-policy` 回報 `authorized_signers` 從一個 fingerprint 變成兩個；`governance-readiness` 為 `{{"status": "ready", "blocks": []}}`；簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid.`。

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

內容：D2 的 reviewed Registry，加上 {up} 參考實作（程式、測試、文件）作為一個未簽章、未碰 Registry 的 commit「{message}」，以及 Git 歷史 `repo.bundle` 與 Maintainer 公鑰 `keys/maintainer.allowed_signers`。Registry 沒有新增候選：下一段的新事實由學員同意後，Agent 依 Runbook 檢查點 5 的提示詞以 `make_record.py --allow-unclassified --upsert` 登記為候選；`verify-evidence` 回報的 stale 引用是實作改動了已審查事實所引用的檔案，留到 D4 以新的候選更新。"""

USAGE = """使用 Recovery 不算自己完成 {up}。學員照 Runbook「{up} Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。"""

D1_INTRO = """# D1 Recovery

內容：起始 Repo（`smart-ticket-dlc-base/`）、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。`repo.bundle` 只有一個未簽章、不含 `domain-memory/` 的「起始 Repo」commit：依流程 D1 不 commit Registry，`domain-memory/` 還原後是未追蹤，等 D2 夥伴設好簽章後才 commit。D1 沒有簽章，所以兩步都由提案者的 Agent 執行，沒有任何 commit。"""

D1_RESTORE = r"""## 2. 還原並驗證（提案者在 `resume-d1` 新開的 Agent 對話）

```powershell
""" + RESTORE_PS.format(seg="d1") + r"""
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
..\..\tools\dm.ps1 validate
..\..\tools\dm.ps1 verify-evidence
```

```bash
""" + RESTORE_SH.format(seg="d1") + r"""
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
../../tools/dm.sh validate
../../tools/dm.sh verify-evidence
```

**看到什麼算成功**：`git status --short` 只有 `?? domain-memory/`；pytest 全部 passed；`Registry is valid.`；verify-evidence 的 stale、missing、invalid 都是 0。結果寫進 `notes/recovery-d1.md`，開頭寫「D1 的成果由 Recovery 提供」。

## 接續 D2

從 Runbook D2 檢查點 1 開始，夥伴在 `resume-d1` 開自己的 Agent 對話。簽章必須在第一個 Registry commit 之前設好：**不要讓 Agent 先 `git add domain-memory`**。
"""


def recovery_md(seg: str, solution: str | None, message: str | None) -> str:
    up = seg.capitalize()
    usage = USAGE.format(up=up)
    if seg == "d1":
        return "\n\n".join([D1_INTRO, usage, STEP_SAVE.format(seg=seg) + "\n" + D1_RESTORE])
    intro = INTRO.get(seg) or INTRO_SOLUTION.format(up=up, message=message)
    log_note = ("，最上面的「" + message + "」為 `N`（未簽章，不碰 Registry，hook 允許）") if solution else ""
    evidence_note = ("verify-evidence 多數 `current`，實作改動過的檔案顯示 `stale`、exit 1，屬預期，留到 D4 處理"
                     if solution else "verify-evidence 全部 `current`")
    return "\n\n".join([intro, usage, STEP_SAVE.format(seg=seg) + "\n"
                        + STEP_TAKEOVER.format(seg=seg, up=up, log_note=log_note) + "\n"
                        + STEP_VERIFY.format(seg=seg, up=up, evidence_note=evidence_note)])


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
            shutil.rmtree(out)
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
