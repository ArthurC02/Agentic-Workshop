"""Regenerate one DLC Recovery source folder: facilitator/recovery/<seg>/ (spec 11 section 3.2).

    py -3.13 -X utf8 make_recovery.py d1|d2|d3a|d3b|d3c [--plugin <domain-memory folder>]

Output (the folder is deleted and rebuilt; it is what build_delivery_dlc.py packs as recovery-dlc-<seg>):
    smart-ticket-dlc-base/   working tree, no .git (the package builder refuses .git)
    repo.bundle              git history of that tree (branch main); restore with init + fetch + reset
    keys/maintainer.allowed_signers   public only (d2 and later)
    RECOVERY.md              restore / continue commands for participants

Sources: participant starting repo, evaluation/reference-registry (bundle tag dlc-d2-reviewed, d1 inputs),
evaluation/reference-solutions/<solution> minus evidence/ and SOLUTION-NOTES.md. Nothing else from
evaluation/ is copied. Commits use fixed identities and dates, so repo.bundle is reproducible for d2+;
d1's domain-memory/ carries plugin timestamps (the plugin has no clock override), so it differs per run.
"""
from __future__ import annotations

import argparse
import json
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
ATTESTED_COMMIT = "5538b6dbcba9e5c4468ceddec72b75b231f9688d"
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


def maintainer_fingerprint() -> str:
    policy = json.loads((REGISTRY / "domain-memory/domain-memory-policy.json").read_text(encoding="utf-8"))
    return policy["review_governance"]["authorized_signers"][0]


RESTORE = """## 1. 還原（約 3 分鐘）

先保存自己的成果：關掉開在舊 Repo 的編輯器，終端機 `deactivate` 後離開舊 Repo。以下在 `participant/repository/`（舊 Repo 的上一層）執行，`<REC>` 換成本包解壓後 `recovery-dlc-{seg}` 資料夾的完整路徑。

```powershell
$rec = "<REC>"
Rename-Item smart-ticket-dlc-base smart-ticket-dlc-base-mine-{seg}
Copy-Item -Recurse "$rec\\smart-ticket-dlc-base" .
Set-Location smart-ticket-dlc-base
git init -q -b main
git fetch -q "$rec\\repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\Activate.ps1
python -m pytest -q
```

```bash
REC="<REC>"
mv smart-ticket-dlc-base smart-ticket-dlc-base-mine-{seg}
cp -r "$REC/smart-ticket-dlc-base" .
cd smart-ticket-dlc-base
git init -q -b main
git fetch -q "$REC/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
source .venv/Scripts/activate
python -m pytest -q
```

**看到什麼算成功**：{status}；pytest 全部 passed。
"""

SIGNERS = """
## 2. 讓 Git 能驗證歷史簽章

Registry commit 由 Maintainer 金鑰簽章；本包只附**公鑰**（`keys/maintainer.allowed_signers`），沒有私鑰。

```powershell
New-Item -ItemType Directory -Force "$HOME\\.dlc-keys" | Out-Null
Copy-Item "$rec\\keys\\maintainer.allowed_signers" "$HOME\\.dlc-keys\\"
git config --local gpg.format ssh
git config --local gpg.ssh.allowedSignersFile "$HOME\\.dlc-keys\\maintainer.allowed_signers"
git log --format='%h %G? %GS %s'
```

```bash
mkdir -p "$HOME/.dlc-keys" && cp "$REC/keys/maintainer.allowed_signers" "$HOME/.dlc-keys/"
git config --local gpg.format ssh
git config --local gpg.ssh.allowedSignersFile "$HOME/.dlc-keys/maintainer.allowed_signers"
git log --format='%h %G? %GS %s'
```

**看到什麼算成功**：三個 Registry commit 為 `G maintainer@example.com`；{log_note}

## 3. 檢查 Registry

```powershell
..\\..\\tools\\dm.ps1 validate --require-reviewed
..\\..\\tools\\dm.ps1 verify-evidence
..\\..\\tools\\dm.ps1 verify-sources
..\\..\\tools\\dm.ps1 verify-audit
..\\..\\tools\\dm.ps1 verify-git-governance --commit {attested}
```

（Git Bash 改用 `../../tools/dm.sh`。）**看到什麼算成功**：`Registry is valid.`；{evidence_note}；verify-audit `valid`；`Git governance is valid.`。

## 4. 接續簽章與 push（之後要 commit Registry 時才需要）

歷史只授權 Maintainer 的 fingerprint `{fp}`，你們沒有那把私鑰。持鑰夥伴建立**本組自己的**金鑰並把它加入授權（金鑰放在 Repo 外的 `~/.dlc-keys/`；已經有 D2 金鑰的組也請另建一把，避免覆蓋）：

```powershell
..\\..\\tools\\dm.ps1 init-signing-key --principal maintainer@example.com --key-file "$HOME\\.dlc-keys\\recovery-{seg}\\signing-key" --sign-every-commit --save "$HOME\\.dlc-keys\\recovery-{seg}\\signing.json"
Get-Content "$HOME\\.dlc-keys\\recovery-{seg}\\signing.json"     # 記下 fingerprint（SHA256:…）
..\\..\\tools\\dm.ps1 amend-policy --field authorized_signers --value "{fp},<新 fingerprint>" --reason "Recovery 後由本組接手簽章"
Get-Content "$HOME\\.dlc-keys\\maintainer.allowed_signers" | Add-Content (git config --local gpg.ssh.allowedSignersFile)
..\\..\\tools\\dm.ps1 install-git-hitl-hook
..\\..\\tools\\dm.ps1 governance-readiness
git add domain-memory
git commit -m "接手 Recovery：授權本組金鑰"
```

```bash
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/recovery-{seg}/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/recovery-{seg}/signing.json"
cat "$HOME/.dlc-keys/recovery-{seg}/signing.json"
../../tools/dm.sh amend-policy --field authorized_signers --value "{fp},<新 fingerprint>" --reason "Recovery 後由本組接手簽章"
cat "$HOME/.dlc-keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness
git add domain-memory
git commit -m "接手 Recovery：授權本組金鑰"
```

- 第四行（把 Maintainer 公鑰附加到新的 allowed signers）不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 改指向只含新金鑰的檔案，歷史上 Maintainer 簽的 commit 就驗不過，push 會被 hook 以「Git commit signature is invalid」拒絕。
- `governance-readiness` 應為 ready。要 push 時先啟用 `.venv`（hook 呼叫裸 `python`），再 `py -3.13 -X utf8 ../../tools/setup_remote.py` 與 `git push -u origin HEAD`。
- 私鑰永遠不要 commit、不要放進 ZIP 或截圖。
"""

INTRO = {
    "d1": """# D1 Recovery

內容：起始 Repo、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。依流程 D1 不 commit Registry：`repo.bundle` 只有一個未簽章的「起始 Repo」commit，`domain-memory/` 在工作目錄中尚未追蹤，等 D2 設好簽章後才 commit。

使用 Recovery 不算自己完成 D1，請在 Runbook 表單如實記錄。""",
    "d2": """# D2 Recovery

內容：已審查、簽章並套用的 Registry（Change Package `CP-CORE-001`，proposer：Proposer，reviewer：Maintainer）。Policy 為 `scm-verified`／`git-signed-commit`／`git-push`。

使用 Recovery 不算自己完成 D2，請在 Runbook 表單如實記錄。改用它之後，先對它執行 `validate --require-reviewed` 與 `verify-audit`（第 3 節），再觀看主持人示範簽章段落。""",
}
INTRO_SOLUTION = """# {up} Recovery

內容：D2 的 reviewed Registry，加上 {up} 參考實作（程式、測試、文件）作為一個未簽章、未碰 Registry 的 commit「{message}」。Registry 沒有新增候選：{up} 的新事實請依 Runbook 以 `make_record.py --allow-unclassified --upsert` 自行登記為候選；`verify-evidence` 回報的 stale 引用是實作改動了已審查事實所引用的檔案，留到 D4 以 `upsert-candidate` 更新。

使用 Recovery 不算自己完成 {up}，請在 Runbook 表單如實記錄。"""

D1_CHECK = """
## 2. 檢查 Registry

```powershell
..\\..\\tools\\dm.ps1 validate
..\\..\\tools\\dm.ps1 verify-evidence
..\\..\\tools\\dm.ps1 verify-sources
..\\..\\tools\\dm.ps1 coverage
```

（Git Bash 改用 `../../tools/dm.sh`。）**看到什麼算成功**：`Registry is valid.`；verify-evidence 全部 `current`；verify-sources `current`／`developer-confirmed`。

## 3. 接續 D2

從 Runbook D2 檢查點 1（`init-signing-key --sign-every-commit`）開始照做。簽章必須在第一個 Registry commit 之前設好：**還原後不要先 `git add domain-memory`**。
"""


def recovery_md(seg: str, solution: str | None, message: str | None) -> str:
    if seg == "d1":
        return "\n\n".join([INTRO["d1"], RESTORE.format(seg=seg, status="`git status --short` 只顯示 `?? domain-memory/`")
                            + D1_CHECK]).rstrip() + "\n"
    intro = INTRO.get(seg) or INTRO_SOLUTION.format(up=seg.capitalize(), message=message)
    log_note = ("最上面的「" + message + "」為 `N`（未簽章，不碰 Registry，hook 允許）。") if solution else "沒有其他 commit。"
    evidence_note = ("verify-evidence 多數 `current`，實作改動過的檔案（如 `payment_service.py`、`store.py`）顯示 `stale`，"
                     "exit 1 屬預期；verify-sources 同理回報 `stale`（來源快照已變），留到 D4 處理") if solution else "verify-evidence 全部 `current`"
    return "\n\n".join([intro, RESTORE.format(seg=seg, status="`git status --short` 沒有輸出")
                        + SIGNERS.format(seg=seg, fp=maintainer_fingerprint(), attested=ATTESTED_COMMIT,
                                         log_note=log_note, evidence_note=evidence_note)])


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
