# D1 Recovery

內容：起始 Repo（`smart-ticket-dlc-base/`）、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。`repo.bundle` 只有一個未簽章、不含 `domain-memory/` 的「起始 Repo」commit：依流程 D1 不 commit Registry，`domain-memory/` 還原後是未追蹤，等 D2 夥伴設好簽章後才 commit。D1 沒有簽章，所以兩步都由提案者的 Agent 執行，沒有任何 commit。

使用 Recovery 不算自己完成 D1。學員照 Runbook「D1 Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。

## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit。Agent 先把原 Repo 的 `git status`、`git log --oneline -3` 與學員回答的進度寫進原 Repo 的 `notes/d1.md`（標題「改用 Recovery 前的狀態」），再把 Recovery 複製成和原 Repo 同一層的 `resume-d1`（`..\..\tools` 才會指向學員包的工具）。

```powershell
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d1.zip" -DestinationPath C:\dlc-rec\d1
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d1
```

```bash
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
unzip -q ~/Downloads/recovery-dlc-d1.zip -d /c/dlc-rec/d1
rec=$(dirname "$(find /c/dlc-rec/d1 -name repo.bundle | head -1)")
cp -r "$rec/smart-ticket-dlc-base" ./resume-d1
```

## 2. 還原並驗證（提案者在 `resume-d1` 新開的 Agent 對話）

```powershell
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
git init -q -b main
git fetch -q "$rec\repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
..\..\tools\dm.ps1 validate
..\..\tools\dm.ps1 verify-evidence
```

```bash
rec=$(dirname "$(find /c/dlc-rec/d1 -name repo.bundle | head -1)")
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

**看到什麼算成功**：`git status --short` 只有 `?? domain-memory/`；pytest 全部 passed；`Registry is valid.`；verify-evidence 的 stale、missing、invalid 都是 0。結果寫進 `notes/recovery-d1.md`，開頭寫「D1 的成果由 Recovery 提供」。

## 接續 D2

從 Runbook D2 檢查點 1 開始，夥伴在 `resume-d1` 開自己的 Agent 對話。簽章必須在第一個 Registry commit 之前設好：**不要讓 Agent 先 `git add domain-memory`**。
