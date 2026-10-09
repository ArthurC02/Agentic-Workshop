# D1 Recovery

內容：起始 Repo（`smart-ticket-dlc-base/`）、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。`repo.bundle` 只有一個未簽章、不含 `domain-memory/` 的「起始 Repo」commit：依流程 D1 不 commit Registry，`domain-memory/` 還原後是未追蹤，等 D2 夥伴設好簽章後才 commit。D1 沒有簽章，所以兩步都由提案者的 Agent 執行，沒有任何 commit。

使用 Recovery 不算自己完成 D1。學員照 Runbook「D1 Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。

## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit，什麼都不寫進原 Repo。Agent 在原 Repo 執行 `git status`、`git log --oneline -3` 並問學員進度，再把 Recovery 複製成和原 Repo 同一層的 `resume-d1`（`..\..\tools` 才會指向學員包的工具），原 Repo 有 `notes/`、`docs/handoffs/` 時一併複製過去（後面的段落要讀）。最後把學員的回答、兩個指令的結果與原 Repo 的完整路徑附加到 `resume-d1` 的 `notes/d1.md`（標題「改用 Recovery 前的狀態」）。下面的指令任何一行失敗就停下（PowerShell 用 `$ErrorActionPreference` 與 `$LASTEXITCODE`，Git Bash 用 `set -e`）。

```powershell
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d1.zip" -DestinationPath C:\dlc-rec\d1
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) { throw "repo.bundle not found" }
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d1
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d1\$d" } }
```

```bash
set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
mkdir -p /c/dlc-rec/d1
unzip -q ~/Downloads/recovery-dlc-d1.zip -d /c/dlc-rec/d1
rec=$(find /c/dlc-rec/d1 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || exit 1
cp -r "$rec/smart-ticket-dlc-base" ./resume-d1
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d1/$d"; fi; done
```

## 2. 還原並驗證（提案者在 `resume-d1` 新開的 Agent 對話）

```powershell
$ErrorActionPreference = 'Stop'
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) { throw "repo.bundle not found" }
git init -q -b main; if ($LASTEXITCODE) { throw "git init failed" }
git fetch -q "$rec\repo.bundle" main; if ($LASTEXITCODE) { throw "git fetch failed" }
git reset -q FETCH_HEAD; if ($LASTEXITCODE) { throw "git reset failed" }
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv; if ($LASTEXITCODE) { throw "venv failed" }
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt; if ($LASTEXITCODE) { throw "pip install failed" }
& '.\.venv\Scripts\python.exe' -m pytest -q; if ($LASTEXITCODE) { throw "pytest failed" }
..\..\tools\dm.ps1 validate; if ($LASTEXITCODE) { throw "validate failed" }
..\..\tools\dm.ps1 verify-evidence
```

```bash
set -e
rec=$(find /c/dlc-rec/d1 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || exit 1
git init -q -b main
git fetch -q "$rec/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
../../tools/dm.sh validate
../../tools/dm.sh verify-evidence
```

**看到什麼算成功**：`git status --short` 只有 `?? domain-memory/` 與從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；pytest 全部 passed；`Registry is valid.`；verify-evidence 的 stale、missing、invalid 都是 0。結果寫進 `notes/recovery-d1.md`，開頭寫「D1 的成果由 Recovery 提供」。

## 接續 D2

從 Runbook D2 檢查點 1 開始，夥伴在 `resume-d1` 開自己的 Agent 對話。簽章必須在第一個 Registry commit 之前設好：**不要讓 Agent 先 `git add domain-memory`**。
