---
id: recovery-d2
title: D2 Recovery 切換
minute: 45-70
group: dlc-rec-d2
section: D2｜審查與核准
---

# D2 Recovery：視需要接續

Recovery 的內容是起始 Repo，加上已經審查、簽章並套用的 Registry（全部是已審查事實）。原 Repo 保留不動；Agent 會如實記錄這段由 Recovery 提供。

```download
id=recovery-dlc-d2 zip=recovery-dlc-d2.zip label=下載 D2 Recovery
```

## 步驟 1 · 【提案者】保存原成果並解出 Recovery

- [ ] 按上方按鈕下載 `recovery-dlc-d2.zip`，存到「下載」資料夾。
- [ ] 在**原本**的提案者 Agent 對話貼：

```text
我們要改用 D2 Recovery 接續。不要修改或刪除目前的 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我們：D2 做到第幾個檢查點、為什麼沒完成。先記在對話裡，不要寫進目前這個 Repo。
2. 把 Recovery 解到 C:\dlc-rec\d2，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d2（和原 Repo 同一層，..\..\tools 才會指向學員包的工具）；原 Repo 有 notes 與 docs\handoffs 資料夾時一併複製過去，後面的段落要讀。這一步不碰 Git。下面的指令要在原 Repo 根目錄開始執行，任何一行失敗都會自動停下：
PowerShell：
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
if (Test-Path .\resume-d2) { throw "resume-d2 already exists: delete C:\dlc-rec\d2 and resume-d2, then rerun" }
Expand-Archive -Force -LiteralPath "$HOME\Downloads\recovery-dlc-d2.zip" -DestinationPath C:\dlc-rec\d2
$b = (Get-ChildItem C:\dlc-rec\d2 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d2
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d2\$d" } }
Git Bash：
( set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
[ ! -e ./resume-d2 ] || { echo "resume-d2 already exists: delete /c/dlc-rec/d2 and resume-d2, then rerun" >&2; exit 1; }
mkdir -p /c/dlc-rec/d2
unzip -o -q ~/Downloads/recovery-dlc-d2.zip -d /c/dlc-rec/d2
rec=$(find /c/dlc-rec/d2 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d2
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d2/$d"; fi; done
)
3. 在 resume-d2 的 notes/d2.md 檔尾加上「改用 Recovery 前的狀態」：第 1 步的回答、兩個指令的結果與原 Repo 的完整路徑，註明「D2 的成果由 Recovery 提供，不是我們自己完成」。不要覆蓋從原 Repo 複製過來的內容。
4. 用白話告訴我 resume-d2 的完整路徑、從原 Repo 複製了哪些資料夾，以及原 Repo 是否原封不動。做完停下。
```

**看到什麼算過關**：`resume-d2` 已建立，原 Repo 的 `notes/`（與 `docs/handoffs/`，如果有）已複製進去，`notes/d2.md` 有「改用 Recovery 前的狀態」；原 Repo 沒有被改動。

**如果卡住**（步驟 1 中途失敗、要重跑）：

```text
步驟 1 中途失敗了。重跑前先刪除 C:\dlc-rec\d2 與 repository 資料夾裡的 resume-d2（只刪這兩個，原 Repo 不動），再重跑第 2 步同一組指令；仍失敗就停下貼出錯誤。
```

## 步驟 2 · 【夥伴】在 resume-d2 開新的 Agent 對話，接手簽章

- [ ] 夥伴結束原 Repo 裡自己的 Agent 對話，在 `resume-d2` 另開一個終端機，啟動自己的**新**對話。
- [ ] 先貼 [D2](#d2)「開始前」的【夥伴】規則，再貼下方提示詞（給 Agent 的，不需要看懂）。

```text
【夥伴的 Agent】這是 D2 Recovery，Repo 根目錄現在是 resume-d2。依終端機選一組，在「同一次執行」裡依序跑（rec、old、fp 變數要在同一次執行內才有值），參數一字不改；任何一步失敗就停下貼出錯誤，不要自己改設定或換寫法：
PowerShell：
$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem C:\dlc-rec\d2 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
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
rec=$(find /c/dlc-rec/d2 -name repo.bundle -exec dirname {} \; | head -1)
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
用白話回報：git status 列了什麼（應該只有從原 Repo 複製來的 ?? notes/，原 Repo 有 docs/handoffs/ 時還有 ?? docs/handoffs/）；金鑰是沿用還是新建（signing.json 的 source）、fingerprint 前 12 碼；git log 每個 commit 的簽章狀態（G 或 N）；amend-policy 的舊值 → 新值；governance-readiness 的 status 與 blocks。不要讀取或顯示私鑰檔 signing-key。把結果寫進 notes/recovery-d2.md 的「簽章接手」，列出這次要 commit 的檔案，停下等我回「同意」。
我同意後執行（Git Bash 把 ..\..\tools\dm.ps1 換成 ../../tools/dm.sh；git add 裡的 docs 照寫：它只會加入從原 Repo 複製來的 docs/handoffs/，沒有複製就不會多加檔案）：
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D2 Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
回報 commit 編號、簽章那一行、verify-git-governance 的結果，以及 commit 後的 git status --short（應該是空的），然後停下。commit 後的回報只顯示在對話，不要再寫入 notes/（下一段會一起 commit）。
```

**看到什麼算過關**

- `git log` 裡碰到 Registry 的三個 commit 是 `G maintainer@example.com`（簽章有效），其他是 `N`（未簽章，它們不碰 Registry，允許）。
- `authorized_signers` 從一個金鑰指紋變成兩個；`governance-readiness` 是 `{"status": "ready", "blocks": []}`。
- 簽章 commit 有 `Good "git" signature for maintainer@example.com`，接著 `Git governance is valid.`；commit 後 `git status --short` 是空的。

**這個夥伴對話開到課程結束**：D3a–D3c 檢查點 5 與 D4 的簽章 commit 都在這裡執行。

## 步驟 3 · 【提案者】在 resume-d2 開新的 Agent 對話，建環境並驗證

- [ ] 結束原本的提案者 Agent 對話，在 `resume-d2` 重新啟動 Agent，開一個**新的**對話。
- [ ] 先貼 [開場與環境](#environment) 的工作規則，再貼：

```text
這是 D2 Recovery 起點，Repo 根目錄是 resume-d2。D2 的成果由 Recovery 提供；夥伴已在自己的對話還原簽章歷史並接手簽章（見 notes/recovery-d2.md）。依序做，任何一步失敗就停下：
1. 建 venv、安裝相依套件、跑全部測試：
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
3. 用白話回報：pytest 最後一行；validate 結果；verify-audit 的 status；verify-evidence 的 current、stale、missing、invalid 各幾個。寫進 notes/recovery-d2.md 的「環境與驗證」，最後一行寫「D2 的成果由 Recovery 提供，不是我們自己完成」。不要 commit，做完停下。
```

**看到什麼算過關**

- 測試全部 `passed`。結果不符就停止切換，請主持人確認。
- `Registry is valid.`；`verify-audit` 回 `"status": "valid"`。
- `verify-evidence` 的 stale、missing、invalid 都是 0。
看到這些後，回到 [D3a](#d3a) 接續。
