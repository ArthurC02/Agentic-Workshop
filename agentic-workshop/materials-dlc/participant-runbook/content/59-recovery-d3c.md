---
id: recovery-d3c
title: D3c Recovery 切換
minute: 155-165
group: dlc-rec-d3c
section: D3｜受治理的變更
---

# D3c Recovery：視需要接續

Recovery 的內容是 D2 的已審查 Registry，加上 D3a～D3c 參考實作（電子發票、點數折抵與團體部分退款的程式、測試與 ADR；會取代你們自己的 D3a～D3c 程式）。原 Repo 保留不動；Agent 會如實記錄這段由 Recovery 提供。

```download
id=recovery-dlc-d3c zip=recovery-dlc-d3c.zip label=下載 D3c Recovery
```

## 步驟 1 · 【提案者】保存原成果並解出 Recovery

① 為什麼做這一步

先記下原 Repo 做到哪裡，再把 Recovery 解成和原 Repo 同一層的 `resume-d3c`，原 Repo 不動。按上方按鈕下載 `recovery-dlc-d3c.zip`，存到「下載」資料夾，再把下方提示詞貼到**原本**的提案者 Agent 對話。

② 貼給 Agent

```prompt
# windows
我們要改用 D3c Recovery 接續。不要修改或刪除目前的 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我們：D3c 做到第幾個檢查點、為什麼沒完成。先記在對話裡，不要寫進目前這個 Repo。
2. 把 Recovery 解到 C:\dlc-rec\d3c，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d3c（和原 Repo 同一層，學員包的 tools 才找得到）；原 Repo 有 notes 與 docs/handoffs 資料夾時一併複製過去，後面的段落要讀。這一步不碰 Git。下面的指令要在原 Repo 根目錄開始執行，任何一行失敗都會自動停下：
PowerShell（整段原樣執行，不要加 2>&1 或 *>&1，否則 dm 的提示訊息會被當成錯誤）：
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
if (Test-Path .\resume-d3c) { throw "resume-d3c already exists: delete C:\dlc-rec\d3c and resume-d3c, then rerun" }
Expand-Archive -Force -LiteralPath "$HOME\Downloads\recovery-dlc-d3c.zip" -DestinationPath C:\dlc-rec\d3c
$b = (Get-ChildItem C:\dlc-rec\d3c -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d3c
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d3c\$d" } }
Git Bash：
( set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
[ ! -e ./resume-d3c ] || { echo "resume-d3c already exists: delete /c/dlc-rec/d3c and resume-d3c, then rerun" >&2; exit 1; }
mkdir -p /c/dlc-rec/d3c
unzip -o -q ~/Downloads/recovery-dlc-d3c.zip -d /c/dlc-rec/d3c
rec=$(find /c/dlc-rec/d3c -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d3c
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d3c/$d"; fi; done
)
3. 在 resume-d3c 的 notes/d3c.md 檔尾加上「改用 Recovery 前的狀態」：第 1 步的回答、兩個指令的結果與原 Repo 的完整路徑，註明「D3c 的成果由 Recovery 提供，不是我們自己完成」。不要覆蓋從原 Repo 複製過來的內容。
4. 用白話告訴我 resume-d3c 的完整路徑、從原 Repo 複製了哪些資料夾，以及原 Repo 是否原封不動。做完停下。
# macos
我們要改用 D3c Recovery 接續。不要修改或刪除目前的 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我們：D3c 做到第幾個檢查點、為什麼沒完成。先記在對話裡，不要寫進目前這個 Repo。
2. 把 Recovery 解到 ~/dlc-rec/d3c，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d3c（和原 Repo 同一層，學員包的 tools 才找得到）；原 Repo 有 notes 與 docs/handoffs 資料夾時一併複製過去，後面的段落要讀。這一步不碰 Git。下面的指令要在原 Repo 根目錄開始執行，任何一行失敗都會自動停下：
( set -e
orig=$(git rev-parse --show-toplevel)
cd "$orig/.."
[ ! -e ./resume-d3c ] || { echo "resume-d3c already exists: delete ~/dlc-rec/d3c and resume-d3c, then rerun" >&2; exit 1; }
mkdir -p "$HOME/dlc-rec/d3c"
unzip -o -q ~/Downloads/recovery-dlc-d3c.zip -d "$HOME/dlc-rec/d3c"
rec=$(find "$HOME/dlc-rec/d3c" -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d3c
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d3c/$d"; fi; done
)
3. 在 resume-d3c 的 notes/d3c.md 檔尾加上「改用 Recovery 前的狀態」：第 1 步的回答、兩個指令的結果與原 Repo 的完整路徑，註明「D3c 的成果由 Recovery 提供，不是我們自己完成」。不要覆蓋從原 Repo 複製過來的內容。
4. 用白話告訴我 resume-d3c 的完整路徑、從原 Repo 複製了哪些資料夾，以及原 Repo 是否原封不動。做完停下。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. repository 資料夾裡已有 resume-d3c，原 Repo 的 notes/（與 docs/handoffs/，如果有）已複製進去。
2. resume-d3c 的 notes/d3c.md 有「改用 Recovery 前的狀態」。
3. 原 Repo 的 git status 和第 1 步記下的一樣，沒有被改動。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時（中途失敗、要重跑）：

```prompt
# windows
步驟 1 中途失敗了。重跑前先刪除 C:\dlc-rec\d3c 與 repository 資料夾裡的 resume-d3c（只刪這兩個，原 Repo 不動），再重跑第 2 步同一組指令；仍失敗就停下貼出錯誤。
# macos
步驟 1 中途失敗了。重跑前先刪除 ~/dlc-rec/d3c 與 repository 資料夾裡的 resume-d3c（只刪這兩個，原 Repo 不動），再重跑第 2 步同一組指令；仍失敗就停下貼出錯誤。
```

## 步驟 2 · 【夥伴】在 resume-d3c 開新的 Agent 對話，接手簽章

① 為什麼做這一步

Recovery 的簽章歷史來自另一把金鑰；夥伴還原歷史後用自己的金鑰接手簽章，之後的 commit 才通得過推送檢查。夥伴結束原 Repo 裡自己的 Agent 對話，在 `resume-d3c` 另開一個終端機，啟動自己的**新**對話，先貼 [D2](#d2)「開始前」的【夥伴】規則，再貼下方提示詞（給 Agent 的，不需要看懂）。讀過回報、確認要 commit 的檔案後回「同意」。

② 貼給 Agent

```prompt
# windows
【夥伴的 Agent】這是 D3c Recovery，Repo 根目錄現在是 resume-d3c。依終端機選一組，在「同一次執行」裡依序跑（rec、old、fp 變數要在同一次執行內才有值），參數一字不改；任何一步失敗就停下貼出錯誤，不要自己改設定或換寫法：
PowerShell（整段原樣執行，不要加 2>&1 或 *>&1，否則 dm 的提示訊息會被當成錯誤）：
$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem C:\dlc-rec\d3c -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
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
rec=$(find /c/dlc-rec/d3c -name repo.bundle -exec dirname {} \; | head -1)
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
用白話回報：git status 列了什麼（應該只有從原 Repo 複製來的 ?? notes/，原 Repo 有 docs/handoffs/ 時還有 ?? docs/handoffs/）；金鑰是沿用還是新建（signing.json 的 source）、fingerprint 前 12 碼；git log 每個 commit 的簽章狀態（G 或 N）；amend-policy 的舊值 → 新值；governance-readiness 的 status 與 blocks。不要讀取或顯示私鑰檔 signing-key。把結果寫進 notes/recovery-d3c.md 的「簽章接手」，列出這次要 commit 的檔案，停下等我回「同意」。
我同意後執行（Git Bash 把 ..\..\tools\dm.ps1 換成 ../../tools/dm.sh；git add 裡的 docs 照寫：它只會加入從原 Repo 複製來的 docs/handoffs/，沒有複製就不會多加檔案）：
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D3c Recovery：授權本組金鑰"
git log --show-signature -1
..\..\tools\dm.ps1 verify-git-governance --commit HEAD
回報 commit 編號、簽章那一行、verify-git-governance 的結果，以及 commit 後的 git status --short（應該是空的），然後停下。commit 後的回報只顯示在對話，不要再寫入 notes/（下一段會一起 commit）。
# macos
【夥伴的 Agent】這是 D3c Recovery，Repo 根目錄現在是 resume-d3c。在「同一次執行」裡依序跑（rec、old、fp 變數要在同一次執行內才有值），參數一字不改；任何一步失敗就停下貼出錯誤，不要自己改設定或換寫法：
( set -e
rec=$(find "$HOME/dlc-rec/d3c" -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
git init -q -b main
git fetch -q "$rec/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
python3.13 -m venv .venv
source .venv/bin/activate
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/maintainer/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/maintainer/signing.json"
cat "$rec/keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
git log --format='%h %G? %GS %s'
old=$(python -c "import json;print(','.join(json.load(open('domain-memory/domain-memory-policy.json',encoding='utf-8'))['review_governance']['authorized_signers']))")
fp=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['fingerprint'])" "$HOME/.dlc-keys/maintainer/signing.json")
../../tools/dm.sh amend-policy --field authorized_signers --value "$old,$fp" --reason "Recovery 後由本組金鑰接手簽章"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness
)
用白話回報：git status 列了什麼（應該只有從原 Repo 複製來的 ?? notes/，原 Repo 有 docs/handoffs/ 時還有 ?? docs/handoffs/）；金鑰是沿用還是新建（signing.json 的 source）、fingerprint 前 12 碼；git log 每個 commit 的簽章狀態（G 或 N）；amend-policy 的舊值 → 新值；governance-readiness 的 status 與 blocks。不要讀取或顯示私鑰檔 signing-key。把結果寫進 notes/recovery-d3c.md 的「簽章接手」，列出這次要 commit 的檔案，停下等我回「同意」。
我同意後執行（git add 裡的 docs 照寫：它只會加入從原 Repo 複製來的 docs/handoffs/，沒有複製就不會多加檔案）：
git add domain-memory notes docs
git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "D3c Recovery：授權本組金鑰"
git log --show-signature -1
source .venv/bin/activate && ../../tools/dm.sh verify-git-governance --commit HEAD
回報 commit 編號、簽章那一行、verify-git-governance 的結果，以及 commit 後的 git status --short（應該是空的），然後停下。commit 後的回報只顯示在對話，不要再寫入 notes/（下一段會一起 commit）。
```

③ 確認結果（貼到夥伴的對話）

```text
請只檢查，不要修改任何檔案，也不要讀取私鑰檔：
1. git log --format='%h %G? %GS %s' 裡碰到 Registry 的 commit 是 G maintainer@example.com，其他是 N（它們不碰 Registry，允許）。
2. governance-readiness 是 {"status": "ready", "blocks": []}；authorized_signers 有兩個金鑰指紋。
3. git log --show-signature -1 有 Good "git" signature for maintainer@example.com，verify-git-governance --commit HEAD 是 Git governance is valid.，git status --short 是空的。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請用白話解釋剛才的錯誤訊息是什麼意思、是哪一個前提沒做到（例如金鑰、政策、HEAD 指向哪個 commit），以及建議的下一步。不要自己修改設定、不要重做 commit、不要繞過 hook，說明完停下等我。
```

④ 補充

**這個夥伴對話開到課程結束**：D4 的簽章 commit 在這裡執行。

## 步驟 3 · 【提案者】在 resume-d3c 開新的 Agent 對話，建環境並驗證

① 為什麼做這一步

提案者在 `resume-d3c` 建好環境，確認測試、Registry 與稽核紀錄都可用，才接續下一段。結束原本的提案者 Agent 對話，在 `resume-d3c` 重新啟動 Agent，開一個**新的**對話，先貼 [開場與環境](#environment) 的工作規則，再貼 [D3a](#d3a) 的「Agent 工作規則」，最後貼下方提示詞。

② 貼給 Agent

```prompt
# windows
這是 D3c Recovery 起點，Repo 根目錄是 resume-d3c。D3c 的成果由 Recovery 提供；夥伴已在自己的對話還原簽章歷史並接手簽章（見 notes/recovery-d3c.md）。依序做，任何一步失敗就停下：
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
3. 用白話回報：pytest 最後一行；validate 結果；verify-audit 的 status；verify-evidence 的 current、stale、missing、invalid 各幾個（Recovery 的參考實作改過部分已審查事實所引用的那幾行，那些證據出現 stale 與 exit 1 是預期，留到 D4，不要修）。寫進 notes/recovery-d3c.md 的「環境與驗證」，最後一行寫「D3c 的成果由 Recovery 提供，不是我們自己完成」。不要 commit，做完停下。
# macos
這是 D3c Recovery 起點，Repo 根目錄是 resume-d3c。D3c 的成果由 Recovery 提供；夥伴已在自己的對話還原簽章歷史並接手簽章（見 notes/recovery-d3c.md）。依序做，任何一步失敗就停下：
1. 建 venv、安裝相依套件、跑全部測試：
     python3.13 -m venv .venv
     .venv/bin/python -m pip install -r requirements.txt
     .venv/bin/python -m pytest -q
2. 驗證 Registry：
   source .venv/bin/activate && ../../tools/dm.sh validate --require-reviewed
   source .venv/bin/activate && ../../tools/dm.sh verify-audit
   source .venv/bin/activate && ../../tools/dm.sh verify-evidence
3. 用白話回報：pytest 最後一行；validate 結果；verify-audit 的 status；verify-evidence 的 current、stale、missing、invalid 各幾個（Recovery 的參考實作改過部分已審查事實所引用的那幾行，那些證據出現 stale 與 exit 1 是預期，留到 D4，不要修）。寫進 notes/recovery-d3c.md 的「環境與驗證」，最後一行寫「D3c 的成果由 Recovery 提供，不是我們自己完成」。不要 commit，做完停下。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. 用 .venv 裡的 python 執行 pytest -q 全部 passed。
2. validate --require-reviewed 是 Registry is valid.；verify-audit 是 "status": "valid"。
3. verify-evidence 約 99 個 current、約 63 個 stale（參考實作改過引用的那幾行，結束碼 1 是預期），missing 與 invalid 都是 0。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時（測試結果不符就停止切換，請主持人確認）：

```text
請不要修改程式或 domain-memory/，也不要 commit。用白話說明是哪一行指令失敗、錯誤訊息是什麼意思，列出建議的處理方式，等我們和主持人決定。
```

完成後回到 [D4](#d4) 接續。
