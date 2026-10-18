# D2 Recovery

內容：起始 Repo 加上已審查、簽章並套用的 Registry（Change Package `CP-CORE-001`，proposer：Proposer，reviewer：Maintainer；`CP-CORE-002` 修正兩筆詞彙的標籤，由第二把 Maintainer 金鑰簽章），以及它的 Git 歷史 `repo.bundle` 與兩把 Maintainer 公鑰 `keys/maintainer.allowed_signers`。Policy 為 `scm-verified`／`git-signed-commit`／`git-push`。

使用 Recovery 不算自己完成 D2。學員照 Runbook「D2 Recovery 切換」頁貼提示詞，由 Agent 執行下面的指令；本檔是給 Agent 與主持人核對的同一份步驟。

## macOS

`bash` 區塊是 Windows Git Bash 的寫法。macOS 用同一組 bash 指令（一樣包在 `( set -e … )`），只換下面幾處；完整的 macOS 提示詞在 Runbook「D2 Recovery 切換」頁的 macOS 分頁。

- Python：`py -3.13` 換成 `python3.13`；`.venv/Scripts/python.exe` 換成 `.venv/bin/python`；`source .venv/Scripts/activate` 換成 `source .venv/bin/activate`。
- 找不到 `~/Downloads/recovery-dlc-d2.zip`：Safari 可能已自動解壓並刪掉 zip，到 Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」，再重新下載。
- `dm.sh` 出現 permission denied：先執行 `chmod +x ../../tools/dm.sh`（只開執行權限）。

## 1. 保存原成果並解出 Recovery（提案者原本的 Agent 對話）

原 Repo 不改名、不覆寫、不刪除，也不 commit，什麼都不寫進原 Repo。Agent 在原 Repo 執行 `git status`、`git log --oneline -3` 並問學員進度，再把 Recovery 複製成和原 Repo 同一層的 `resume-d2`（`..\..\tools` 才會指向學員包的工具），原 Repo 有 `notes/`、`docs/handoffs/` 時一併複製過去（後面的段落要讀）。最後把學員的回答、兩個指令的結果與原 Repo 的完整路徑附加到 `resume-d2` 的 `notes/d2.md`（標題「改用 Recovery 前的狀態」）。複製來的 `notes/` 提到的候選 id 是原 Repo 的，Recovery 的 Registry 不一定有，之後查不到是預期。下面的指令任何一行失敗就停下（PowerShell 用 `$ErrorActionPreference` 與 `$LASTEXITCODE`；Git Bash 整段包在 `( set -e … )` 子 shell 裡，失敗只結束這一段，不會關掉 Agent 的終端機）。中途失敗要重跑時，重跑前先刪除學員包裡的 `recovery-d2` 與 `resume-d2`（只刪這兩個）。

```powershell
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location (Split-Path $orig)
if (Test-Path .\resume-d2) { throw "resume-d2 already exists: delete ..\recovery-d2 and resume-d2, then rerun" }
$dl = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').'{374DE290-123F-4565-9164-39C4925E467B}'; if (-not $dl) { $dl = "$HOME\Downloads" }
Expand-Archive -Force -LiteralPath "$dl\recovery-dlc-d2.zip" -DestinationPath ..\recovery-d2
$b = (Get-ChildItem ..\recovery-d2 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d2
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d2\$d" } }
```

```bash
( set -e
orig=$(git rev-parse --show-toplevel)
cd "$orig/.."
[ ! -e ./resume-d2 ] || { echo "resume-d2 already exists: delete ../recovery-d2 and resume-d2, then rerun" >&2; exit 1; }
mkdir -p ../recovery-d2
dl=$(cygpath -u "$(powershell.exe -NoProfile -Command "(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').'{374DE290-123F-4565-9164-39C4925E467B}'" 2>/dev/null | tr -d '\r')" 2>/dev/null) || dl=~/Downloads
unzip -o -q "$dl/recovery-dlc-d2.zip" -d ../recovery-d2
rec=$(find ../recovery-d2 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d2
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d2/$d"; fi; done
)
```

## 2. 還原簽章歷史並接手簽章（夥伴在 `resume-d2` 新開的 Agent 對話）

`repo.bundle` 是 Recovery 的 Git 歷史：Registry 的 commit 都由 Maintainer 金鑰簽章，所以「第一個含 `domain-memory/` 的 commit 是簽章 commit」在新資料夾仍然成立。`keys/maintainer.allowed_signers` 只有**公鑰**，讓 Git 驗得了這些簽章；私鑰不在包裡。所以由夥伴用自己的金鑰（已有 D2 金鑰就沿用，沒有就新建，一律放在 Repo 外的 `.dlc-keys\maintainer\`）接手：加入授權、裝回 pre-push hook，讀過回報、回「同意」後做一個簽章 commit。金鑰、簽章與 commit 只在夥伴自己的 Agent 對話執行；提案者的 Agent 不碰。

```powershell
$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem ..\..\recovery-d2 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
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
( set -e
rec=$(find ../../recovery-d2 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
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
)
```

Agent 把結果寫進 `notes/recovery-d2.md` 的「簽章接手」（fingerprint 只寫前 12 碼），夥伴回「同意」後：

```powershell
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D2 Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
```

（Git Bash 與 macOS 把 `..\..\tools\dm.ps1` 換成 `../../tools/dm.sh`。`git add` 的 `docs` 只會加入從原 Repo 複製來的 `docs/handoffs/`，沒有就什麼都不加；commit 後 `git status --short` 是空的。）

**看到什麼算成功**：`git status --short` 只列出從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；`git log` 中 Registry 的七個 commit（最上面一個是改存 OKF 版面）為 `G maintainer@example.com`，最下面的「Smart Ticket DLC base」（起始程式）為 `N`（未簽章，不碰 Registry，hook 允許）；`amend-policy` 回報 `authorized_signers` 從兩個 fingerprint 變成三個；`governance-readiness` 為 `{"status": "ready", "blocks": []}`；簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid for 1 commit.`。

- 附加 Maintainer 公鑰那一行不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 指向只含夥伴金鑰的檔案，少了它，歷史上 Maintainer 簽的 commit 就驗不過，之後 push 會被 hook 以「Git commit signature is invalid」拒絕。
- 之後 D3、D4 的 commit 照 Runbook 由夥伴的對話簽章。私鑰永遠不要 commit、不要放進 ZIP 或截圖。

## 3. 建環境並驗證（提案者在 `resume-d2` 新開的 Agent 對話）

```powershell
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
..\..\tools\dm.ps1 validate --require-reviewed
..\..\tools\dm.ps1 verify-audit
..\..\tools\dm.ps1 verify-evidence
```

（Git Bash 用 `.venv/Scripts/python.exe` 與 `../../tools/dm.sh`；macOS 用 `python3.13`、`.venv/bin/python` 與 `../../tools/dm.sh`。）

**看到什麼算成功**：pytest 全部 passed；`Registry is valid.`（帶 `--require-reviewed`：全部是已審查事實）；verify-audit `"status": "valid"`；verify-evidence 全部 `current`。結果寫進 `notes/recovery-d2.md` 的「環境與驗證」，最後一行寫「D2 的成果由 Recovery 提供，不是我們自己完成」；不 commit（下一次由夥伴的對話一起 commit）。


## 4. （選做）push 檢查（夥伴的 Agent 對話，步驟 3 建好 `.venv` 之後）

Recovery 沒有 CP-D2-001，D2 檢查點 6 的 push 在這裡補做；hook 一次檢查所有碰到 Registry 的 commit。不 commit。

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

**看到什麼算成功**：hook 印出一行 `Git governance is valid for 8 commits.`（Recovery 歷史裡碰到 Registry 的七個 commit，加上步驟 2 的簽章 commit），最後 `* [new branch] HEAD -> main`。被拒時不要用 `--no-verify` 繞過。
