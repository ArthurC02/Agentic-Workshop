---
id: recovery-d1
title: D1 Recovery 切換
minute: 35-60
group: dlc-rec-d1
section: D1｜共同語言與邊界
---

# D1 Recovery：視需要接續

Recovery 是起始 Repo 加上已確認的來源與一組 D1 候選。原 Repo 保留不動；Agent 會如實記錄這段由 Recovery 提供。

```download
id=recovery-dlc-d1 zip=recovery-dlc-d1.zip label=下載 D1 Recovery
```

## 步驟 1 · 保存原成果並解出 Recovery

- [ ] 按上方按鈕下載 `recovery-dlc-d1.zip`（存到「下載」資料夾）。
- [ ] 把下方提示詞貼給**原本**的 Agent：

```text
我要改用 D1 Recovery 接續。不要修改或刪除目前這個 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我：現在是第幾分鐘、主要卡在哪裡、自己完成到 D1 第幾個檢查點。先記在對話裡，不要寫進目前這個 Repo。
2. 把 Recovery 解到 C:\dlc-rec\d1，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d1（和原 Repo 同一層，..\..\tools 才會指向學員包的工具）；原 Repo 有 notes 與 docs\handoffs 資料夾時一併複製過去，後面的段落要讀。這一步不碰 Git。下面的指令要在原 Repo 根目錄開始執行，任何一行失敗都會自動停下：
PowerShell：
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
if (Test-Path .\resume-d1) { throw "resume-d1 already exists: delete C:\dlc-rec\d1 and resume-d1, then rerun" }
Expand-Archive -Force -LiteralPath "$HOME\Downloads\recovery-dlc-d1.zip" -DestinationPath C:\dlc-rec\d1
$b = (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d1
foreach ($d in 'notes', 'docs\handoffs') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-d1\$d" } }
Git Bash：
( set -e
orig=$(git rev-parse --show-toplevel)
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
[ ! -e ./resume-d1 ] || { echo "resume-d1 already exists: delete /c/dlc-rec/d1 and resume-d1, then rerun" >&2; exit 1; }
mkdir -p /c/dlc-rec/d1
unzip -o -q ~/Downloads/recovery-dlc-d1.zip -d /c/dlc-rec/d1
rec=$(find /c/dlc-rec/d1 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-d1
for d in notes docs/handoffs; do if [ -d "$orig/$d" ]; then cp -r "$orig/$d" "./resume-d1/$d"; fi; done
)
3. 在 resume-d1 的 notes/d1.md 檔尾加上「改用 Recovery 前的狀態」：第 1 步的回答、兩個指令的結果與原 Repo 的完整路徑，註明「D1 的成果由 Recovery 提供，不是自己完成」。不要覆蓋從原 Repo 複製過來的內容。
4. 用白話告訴我 resume-d1 的完整路徑、從原 Repo 複製了哪些資料夾，以及原 Repo 是否原封不動。做完停下。
```

**看到什麼算過關**：`resume-d1` 已建立，`notes/` 已複製進去，`notes/d1.md` 有「改用 Recovery 前的狀態」；原 Repo 沒有被改動。

**如果卡住**（步驟 1 中途失敗、要重跑）：

```text
步驟 1 中途失敗了。重跑前先刪除 C:\dlc-rec\d1 與 repository 資料夾裡的 resume-d1（只刪這兩個，原 Repo 不動），再重跑第 2 步同一組指令；仍失敗就停下貼出錯誤。
```

## 步驟 2 · 在 resume-d1 開新的 Agent 對話，還原並驗證

- [ ] 結束目前的 Agent 對話，在 `resume-d1` 資料夾重新開啟 Agent。
- [ ] 先貼 [開場與環境](#environment) 的工作規則，再貼下方提示詞：

```text
這是 D1 Recovery 起點，Repo 根目錄是 resume-d1：Domain Memory 在 domain-memory/，裡面全部是候選。不要 git add 或 commit domain-memory/。依終端機選一組，在「同一次執行」裡依序跑（rec 變數要在同一次執行內才有值），任何一步失敗就停下：
PowerShell：
$ErrorActionPreference = 'Stop'
$b = (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
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
Git Bash：
( set -e
rec=$(find /c/dlc-rec/d1 -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
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
)
用白話告訴我：git status 列了什麼、pytest 最後一行、validate 結果、verify-evidence 的 stale／missing／invalid 各幾個。把結果寫進 notes/recovery-d1.md，開頭註明「D1 的成果由 Recovery 提供；原 Repo 的狀態記在 notes/d1.md」。不要 commit，做完停下。
```

**看到什麼算過關**

- `git status` 只列出未追蹤的 `?? domain-memory/`、`?? notes/`（可能還有 `?? docs/handoffs/`），這是正確的。
- pytest 全部 `passed`；`Registry is valid.`；`verify-evidence` 的 stale、missing、invalid 都是 0。

完成後回到 [D2](#d2)：夥伴在 `resume-d1` 另開終端機與自己的 Agent 對話。
