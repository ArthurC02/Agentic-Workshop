# D3b Recovery

內容：D2 的 reviewed Registry，加上 D3b 參考實作（程式、測試、文件）作為一個未簽章、未碰 Registry 的 commit「D3b：點數折抵（Recovery 參考實作）」，以及 Git 歷史 `repo.bundle` 與 Maintainer 公鑰 `keys/maintainer.allowed_signers`。Registry 沒有新增候選：下一段的新事實由學員同意後，Agent 依 Runbook 檢查點 5 的提示詞以 `make_record.py --allow-unclassified --upsert` 登記為候選；`verify-evidence` 回報的 stale 引用是實作改動了已審查事實所引用的檔案，留到 D4 以新的候選更新。

使用 Recovery 不算自己完成 D3b。學員照 Runbook「D3b Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。

## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit，什麼都不寫進原 Repo。Agent 在原 Repo 執行 `git status`、`git log --oneline -3` 並問學員進度，再把 Recovery 複製成和原 Repo 同一層的 `resume-d3b`（`..\..\tools` 才會指向學員包的工具），原 Repo 有 `notes/`、`docs/handoffs/` 時一併複製過去（後面的段落要讀）。最後把學員的回答、兩個指令的結果與原 Repo 的完整路徑附加到 `resume-d3b` 的 `notes/d3b.md`（標題「改用 Recovery 前的狀態」）。下面的指令任何一行失敗就停下（PowerShell 用 `$ErrorActionPreference` 與 `$LASTEXITCODE`，Git Bash 用 `set -e`）。

```powershell
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d3b.zip" -DestinationPath C:\dlc-rec\d3b
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d3b -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) { throw "repo.bundle not found" }
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d3b
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d3b\$d" } }
```

```bash
set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
mkdir -p /c/dlc-rec/d3b
unzip -q ~/Downloads/recovery-dlc-d3b.zip -d /c/dlc-rec/d3b
rec=$(find /c/dlc-rec/d3b -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || exit 1
cp -r "$rec/smart-ticket-dlc-base" ./resume-d3b
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d3b/$d"; fi; done
```

## 2. 還原簽章歷史並接手簽章（夥伴在 `resume-d3b` 新開的 Agent 對話）

`repo.bundle` 是 Recovery 的 Git 歷史：Registry 的 commit 都由 Maintainer 金鑰簽章，所以「第一個含 `domain-memory/` 的 commit 是簽章 commit」在新資料夾仍然成立。`keys/maintainer.allowed_signers` 只有**公鑰**，讓 Git 驗得了這些簽章；私鑰不在包裡。所以由夥伴用自己的金鑰（已有 D2 金鑰就沿用，沒有就新建，一律放在 Repo 外的 `.dlc-keys\maintainer\`）接手：加入授權、裝回 pre-push hook，讀過回報、回「同意」後做一個簽章 commit。金鑰、簽章與 commit 只在夥伴自己的 Agent 對話執行；提案者的 Agent 不碰。

```powershell
$ErrorActionPreference = 'Stop'
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d3b -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
if (-not $rec) { throw "repo.bundle not found" }
git init -q -b main; if ($LASTEXITCODE) { throw "git init failed" }
git fetch -q "$rec\repo.bundle" main; if ($LASTEXITCODE) { throw "git fetch failed" }
git reset -q FETCH_HEAD; if ($LASTEXITCODE) { throw "git reset failed" }
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
..\..\tools\dm.ps1 init-signing-key --principal maintainer@example.com --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit --save "$env:USERPROFILE\.dlc-keys\maintainer\signing.json"; if ($LASTEXITCODE) { throw "init-signing-key failed" }
Get-Content "$rec\keys\maintainer.allowed_signers" | Add-Content (git config --local gpg.ssh.allowedSignersFile)
git log --format='%h %G? %GS %s'
$old = (Get-Content domain-memory\domain-memory-policy.json -Raw | ConvertFrom-Json).review_governance.authorized_signers -join ','
$fp = (Get-Content "$env:USERPROFILE\.dlc-keys\maintainer\signing.json" -Raw | ConvertFrom-Json).fingerprint
..\..\tools\dm.ps1 amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"; if ($LASTEXITCODE) { throw "amend-policy failed" }
..\..\tools\dm.ps1 install-git-hitl-hook; if ($LASTEXITCODE) { throw "install-git-hitl-hook failed" }
..\..\tools\dm.ps1 governance-readiness
```

```bash
set -e
rec=$(find /c/dlc-rec/d3b -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || exit 1
git init -q -b main
git fetch -q "$rec/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/maintainer/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/maintainer/signing.json"
cat "$rec/keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
git log --format='%h %G? %GS %s'
old=$(py -3.13 -c "import json;print(','.join(json.load(open('domain-memory/domain-memory-policy.json',encoding='utf-8'))['review_governance']['authorized_signers']))")
fp=$(py -3.13 -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['fingerprint'])" "$HOME/.dlc-keys/maintainer/signing.json")
../../tools/dm.sh amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness
```

Agent 把結果寫進 `notes/recovery-d3b.md` 的「簽章接手」（fingerprint 只寫前 12 碼），夥伴回「同意」後：

```powershell
git add domain-memory notes
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D3b Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
```

（Git Bash 把 `..\..\tools\dm.ps1` 換成 `../../tools/dm.sh`。）

**看到什麼算成功**：`git status --short` 只列出從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；`git log` 中 Registry 的三個 commit 為 `G maintainer@example.com`，最上面的「D3b：點數折抵（Recovery 參考實作）」為 `N`（未簽章，不碰 Registry，hook 允許）；`amend-policy` 回報 `authorized_signers` 從一個 fingerprint 變成兩個；`governance-readiness` 為 `{"status": "ready", "blocks": []}`；簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid.`。

- 附加 Maintainer 公鑰那一行不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 指向只含夥伴金鑰的檔案，少了它，歷史上 Maintainer 簽的 commit 就驗不過，之後 push 會被 hook 以「Git commit signature is invalid」拒絕。
- 之後 D3、D4 的 commit 照 Runbook 由夥伴的對話簽章。私鑰永遠不要 commit、不要放進 ZIP 或截圖。

## 3. 建環境並驗證（提案者在 `resume-d3b` 新開的 Agent 對話）

```powershell
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
..\..\tools\dm.ps1 validate --require-reviewed
..\..\tools\dm.ps1 verify-audit
..\..\tools\dm.ps1 verify-evidence
```

（Git Bash 用 `.venv/Scripts/python.exe` 與 `../../tools/dm.sh`。）

**看到什麼算成功**：pytest 全部 passed；`Registry is valid.`（帶 `--require-reviewed`：全部是已審查事實）；verify-audit `"status": "valid"`；verify-evidence 多數 `current`，實作改動過的檔案顯示 `stale`、exit 1，屬預期，留到 D4 處理。結果寫進 `notes/recovery-d3b.md` 的「環境與驗證」，最後一行寫「D3b 的成果由 Recovery 提供，不是我們自己完成」；不 commit（下一次由夥伴的對話一起 commit）。
