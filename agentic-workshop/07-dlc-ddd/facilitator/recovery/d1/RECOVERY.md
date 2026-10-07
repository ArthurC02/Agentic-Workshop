# D1 Recovery

內容：起始 Repo、已確認的 source map（`--review-mode local-draft-only`）、一組 D1 候選（5 Contexts、21 詞、16 規則等），全部為候選，沒有任何 reviewed 事實。依流程 D1 不 commit Registry：`repo.bundle` 只有一個未簽章的「起始 Repo」commit，`domain-memory/` 在工作目錄中尚未追蹤，等 D2 設好簽章後才 commit。

使用 Recovery 不算自己完成 D1，請在 Runbook 表單如實記錄。

## 1. 還原（約 3 分鐘）

先保存自己的成果：關掉開在舊 Repo 的編輯器，終端機 `deactivate` 後離開舊 Repo。以下在 `participant/repository/`（舊 Repo 的上一層）執行，`<REC>` 換成本包解壓後 `recovery-dlc-d1` 資料夾的完整路徑。

```powershell
$rec = "<REC>"
Rename-Item smart-ticket-dlc-base smart-ticket-dlc-base-mine-d1
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .
Set-Location smart-ticket-dlc-base
git init -q -b main
git fetch -q "$rec\repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

```bash
REC="<REC>"
mv smart-ticket-dlc-base smart-ticket-dlc-base-mine-d1
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

**看到什麼算成功**：`git status --short` 只顯示 `?? domain-memory/`；pytest 全部 passed。

## 2. 檢查 Registry

```powershell
..\..\tools\dm.ps1 validate
..\..\tools\dm.ps1 verify-evidence
..\..\tools\dm.ps1 verify-sources
..\..\tools\dm.ps1 coverage
```

（Git Bash 改用 `../../tools/dm.sh`。）**看到什麼算成功**：`Registry is valid.`；verify-evidence 全部 `current`；verify-sources `current`／`developer-confirmed`。

## 3. 接續 D2

從 Runbook D2 檢查點 1（`init-signing-key --sign-every-commit`）開始照做。簽章必須在第一個 Registry commit 之前設好：**還原後不要先 `git add domain-memory`**。
