---
id: recovery-d3b
title: D3b Recovery 切換
minute: 125-155
group: dlc-rec-d3b
section: D3｜受治理的變更
---

# D3b Recovery：按需接續

主持人揭曉之後，才會個別提供本頁解鎖碼；一般解鎖碼不會開啟本頁。內容是：D3b 完成後的 Repo 與 Registry（含點數折抵的實作與測試）。使用 Recovery **不代表你們自己完成了 D3b**，Agent 會在紀錄中如實寫明。

```download
id=recovery-dlc-d3b zip=recovery-dlc-d3b.zip label=下載 D3b Recovery
```

切換分三步，和 D2 的分工一樣：提案者的 Agent 搬檔案、建環境；**金鑰、簽章與 commit 只在夥伴自己的 Agent 對話**。原本的 Repo 不改名、不覆寫、不刪除。

```callout info
新概念：Recovery 怎麼保住簽章規則
Recovery 附上 Git 歷史（`repo.bundle`）：Registry 的 commit 都由 Maintainer 金鑰簽章，所以 D2「第一個含 `domain-memory/` 的 commit 必須簽章」在新資料夾仍然成立。包裡只有可公開的 Maintainer 公鑰（讓 Git 驗得了舊簽章），沒有私鑰；之後的 commit 由夥伴用自己的金鑰接手：像 D2 檢查點 2 一樣把自己的金鑰加入授權，再做一個簽章 commit。
📖 延伸閱讀：Git 官方文件〈git-commit〉的 -S 選項說明；學員包 `tools/README.md`（金鑰位置與 pre-push hook）。
```

## 步驟 1 · 【提案者】保存原成果並解出 Recovery

- [ ] 按上方按鈕下載 `recovery-dlc-d3b.zip`，存到「下載」資料夾。
- [ ] 如果有自己啟動的 Server，在它的終端機按 `Ctrl+C` 停止；不要停止別人的程序。
- [ ] 在**原本**的提案者 Agent 對話貼：

```text
我們要改用 D3b Recovery 接續。不要修改或刪除目前的 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我們：D3b 做到第幾個檢查點、為什麼沒完成。先記在對話裡，不要寫進目前這個 Repo。
2. 把 Recovery 解到 C:\dlc-rec\d3b，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d3b（和原 Repo 同一層，..\..\tools 才會指向學員包的工具）；原 Repo 有 notes 與 docs\handoffs 資料夾時一併複製過去，後面的段落要讀。這一步不碰 Git。下面的指令要在原 Repo 根目錄開始執行，任何一行失敗都會自動停下：
PowerShell：
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
if (Test-Path .\resume-d3b) { throw "resume-d3b already exists: delete C:\dlc-rec\d3b and resume-d3b, then rerun" }
Expand-Archive -Force -LiteralPath "$HOME\Downloads\recovery-dlc-d3b.zip" -DestinationPath C:\dlc-rec\d3b
$b = (Get-ChildItem C:\dlc-rec\d3b -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d3b
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d3b\$d" } }
Git Bash：
( set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
[ ! -e ./resume-d3b ] || { echo "resume-d3b already exists: delete /c/dlc-rec/d3b and resume-d3b, then rerun" >&2; exit 1; }
mkdir -p /c/dlc-rec/d3b
unzip -o -q ~/Downloads/recovery-dlc-d3b.zip -d /c/dlc-rec/d3b
rec=$(find /c/dlc-rec/d3b -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d3b
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d3b/$d"; fi; done
)
3. 在 resume-d3b 的 notes/d3b.md 檔尾加上「改用 Recovery 前的狀態」：第 1 步的回答、兩個指令的結果與原 Repo 的完整路徑，註明「D3b 的成果由 Recovery 提供，不是我們自己完成」。不要覆蓋從原 Repo 複製過來的內容。
4. 用白話告訴我 resume-d3b 的完整路徑、從原 Repo 複製了哪些資料夾，以及原 Repo 是否原封不動。做完停下。
```

**看到什麼算過關**：`resume-d3b` 已建立，原 Repo 的 `notes/`（與 `docs/handoffs/`，如果有）已複製進去，`resume-d3b` 的 `notes/d3b.md` 有「改用 Recovery 前的狀態」；原 Repo 沒有被改動。複製來的 `notes/` 提到的候選 id 是原 Repo 的，Recovery 的 Registry 不一定有，之後查不到是預期。

**如果卡住**（步驟 1 中途失敗、要重跑）：

```text
步驟 1 中途失敗了。重跑前先刪除 C:\dlc-rec\d3b 與 repository 資料夾裡的 resume-d3b（只刪這兩個，原 Repo 不動），再重跑第 2 步同一組指令；仍失敗就停下貼出錯誤。
```

## 步驟 2 · 【夥伴】在 resume-d3b 開新的 Agent 對話，接手簽章

- [ ] 夥伴結束原 Repo 裡自己的 Agent 對話，在 `resume-d3b` 另開一個終端機，啟動自己的**新**對話。
- [ ] 先貼 [D2](#d2)「開始前」的【夥伴】規則，再貼下方提示詞。這段的指令是給 Agent 的，不需要看懂；你只看回報與「看到什麼算過關」。

```text
【夥伴的 Agent】這是 D3b Recovery，Repo 根目錄現在是 resume-d3b。依終端機選一組，在「同一次執行」裡依序跑（rec、old、fp 變數要在同一次執行內才有值），參數一字不改；任何一步失敗就停下貼出錯誤，不要自己改設定或換寫法：
PowerShell：
$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem C:\dlc-rec\d3b -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
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
Git Bash：
( set -e
rec=$(find /c/dlc-rec/d3b -name repo.bundle -exec dirname {} \; | head -1)
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
用白話回報：git status 列了什麼（應該只有從原 Repo 複製來的 ?? notes/，原 Repo 有 docs/handoffs/ 時還有 ?? docs/handoffs/）；金鑰是沿用還是新建（signing.json 的 source）、fingerprint 前 12 碼；git log 每個 commit 的簽章狀態（G 或 N）；amend-policy 的舊值 → 新值；governance-readiness 的 status 與 blocks。不要讀取或顯示私鑰檔 signing-key。把結果寫進 notes/recovery-d3b.md 的「簽章接手」，列出這次要 commit 的檔案，停下等我回「同意」。
我同意後執行（Git Bash 把 ..\..\tools\dm.ps1 換成 ../../tools/dm.sh；docs 只會加入從原 Repo 複製來的 docs/handoffs/，沒有就不加）：
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D3b Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
回報 commit 編號、簽章那一行、verify-git-governance 的結果，以及 commit 後的 git status --short（應該是空的），然後停下。
```

**看到什麼算過關**：

- `git status` 只列出從原 Repo 複製來的 `?? notes/`（原 Repo 有 `docs/handoffs/` 時還有 `?? docs/handoffs/`）；`git log` 中 Registry 的三個 commit 是 `G maintainer@example.com`，最上面的「D3b：點數折抵（Recovery 參考實作）」與最下面的「Smart Ticket DLC base」（起始程式）是 `N`（未簽章、不碰 Registry，允許）。
- `amend-policy` 的 `authorized_signers` 從一個 fingerprint 變成兩個；`governance-readiness` 是 `{"status": "ready", "blocks": []}`。
- 簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid.`；commit 後 `git status --short` 是空的（複製來的 `notes/` 與 `docs/handoffs/` 都已 commit）。

這個夥伴對話開到課程結束：之後檢查點 5 與 D4 的簽章 commit 都在這裡執行。

## 步驟 3 · 【提案者】在 resume-d3b 開新的 Agent 對話，建環境並驗證

- [ ] 結束原本的提案者 Agent 對話，在 `resume-d3b` 重新啟動 Agent，開一個**新的**對話。
- [ ] 先貼 [D3a](#d3a) 的「Agent 工作規則」，再貼：

```text
這是 D3b Recovery 起點，Repo 根目錄是 resume-d3b。D3b 的成果由 Recovery 提供；夥伴已在自己的對話還原簽章歷史並接手簽章（見 notes/recovery-d3b.md）。依序做，任何一步失敗就停下：
1. 建 venv、安裝依賴、跑全部測試：
   PowerShell：
     py -3.13 -m venv .venv
     & '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
     & '.\.venv\Scripts\python.exe' -m pytest -q
   Git Bash：
     py -3.13 -m venv .venv
     .venv/Scripts/python.exe -m pip install -r requirements.txt
     .venv/Scripts/python.exe -m pytest -q
2. 驗證 Registry（Git Bash 把 ..\..\tools\dm.ps1 換成 ../../tools/dm.sh）：
   ..\..\tools\dm.ps1 validate --require-reviewed
   ..\..\tools\dm.ps1 verify-audit
   ..\..\tools\dm.ps1 verify-evidence
3. 用白話回報：pytest 最後一行；validate 結果；verify-audit 的 status；verify-evidence 的 current、stale、missing、invalid 各幾個（Recovery 的參考實作改過部分被引用的檔案，出現 stale 與 exit 1 是預期，留到 D4，不要修）。寫進 notes/recovery-d3b.md 的「環境與驗證」，最後一行寫「D3b 的成果由 Recovery 提供，不是我們自己完成」。不要 commit，做完停下。
```

**看到什麼算過關**

- 測試全部 `passed`，沒有 `failed` 或 `error`。結果不符就停止切換，請主持人確認。
- `Registry is valid.`（帶 `--require-reviewed`：Recovery 裡全部是已審查事實）；`verify-audit` 回 `"status": "valid"`。
- `notes/recovery-d3b.md` 寫明 D3b 的成果由 Recovery 提供。看到這些後，回到 [D3c](#d3c) 接續。
