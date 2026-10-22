---
name: dlc-recovery
description: 改用某一段的 Recovery（復原包）接續：保存原 Repo 的狀態、把 Recovery 解成 resume-<段落>，再照包裡的 RECOVERY.md 還原與驗證。使用者說「改用 D2 Recovery」「切換到 Recovery」時使用。
---

# dlc-recovery：改用 Recovery 接續

下面的 `SEG` 換成這次的段落：`d1`、`d2`、`d3a`、`d3b`、`d3c`。Recovery 的 zip 是 `recovery-dlc-SEG.zip`，在使用者的「下載」資料夾。

## 步驟 1：保存原成果並解出 Recovery（提案者原本的對話，在原 Repo）

原 Repo 不改名、不覆寫、不刪除，也不 commit，什麼都不寫進原 Repo。

1. 在原 Repo 執行 `git status` 和 `git log --oneline -3`，問使用者：這段做到第幾個檢查點、為什麼沒完成。先記在對話裡。
2. 從原 Repo 根目錄執行下面這段，整段原樣執行，任何一行失敗都會停下。它把 Recovery 解到學員包的 `recovery-SEG`，複製成和原 Repo 同一層的 `resume-SEG`（`../../tools` 才找得到），並把原 Repo 的 `notes/`、`docs/handoffs/`、`AGENTS.md` 一起帶過去。
   - Windows PowerShell（不要加 `2>&1` 或 `*>&1`）：

```powershell
$ErrorActionPreference = 'Stop'
$orig = git rev-parse --show-toplevel; if ($LASTEXITCODE) { throw "not in the original Repo" }
Set-Location (Split-Path $orig)
if (Test-Path .\resume-SEG) { throw "resume-SEG already exists: delete ..\recovery-SEG and resume-SEG, then rerun" }
$dl = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').'{374DE290-123F-4565-9164-39C4925E467B}'; if (-not $dl) { $dl = "$HOME\Downloads" }
Expand-Archive -Force -LiteralPath "$dl\recovery-dlc-SEG.zip" -DestinationPath ..\recovery-SEG
$b = (Get-ChildItem ..\recovery-SEG -Recurse -Filter repo.bundle | Select-Object -First 1).FullName; if (-not $b) { throw "repo.bundle not found" }; $rec = Split-Path $b
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-SEG
foreach ($d in 'notes', 'docs\handoffs', 'AGENTS.md') { if (Test-Path "$orig\$d") { Copy-Item -Recurse "$orig\$d" ".\resume-SEG\$d" } }
```

   - Windows Git Bash 與 macOS（同一段；macOS 找不到 zip 時，請使用者到 Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」再重新下載）：

```bash
( set -e
orig=$(git rev-parse --show-toplevel)
cd "$orig/.."
[ ! -e ./resume-SEG ] || { echo "resume-SEG already exists: delete ../recovery-SEG and resume-SEG, then rerun" >&2; exit 1; }
mkdir -p ../recovery-SEG
dl=$(cygpath -u "$(powershell.exe -NoProfile -Command "(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').'{374DE290-123F-4565-9164-39C4925E467B}'" 2>/dev/null | tr -d '\r')" 2>/dev/null) || dl=~/Downloads
unzip -o -q "$dl/recovery-dlc-SEG.zip" -d ../recovery-SEG
rec=$(find ../recovery-SEG -name repo.bundle -exec dirname {} \; | head -1)
[ -n "$rec" ] || { echo "repo.bundle not found" >&2; exit 1; }
cp -r "$rec/smart-ticket-dlc-base" ./resume-SEG
for d in notes docs/handoffs AGENTS.md; do if [ -e "$orig/$d" ]; then cp -r "$orig/$d" "./resume-SEG/$d"; fi; done
)
```

3. 再把原 Repo 裡放 Skill 的資料夾（AGENTS.md「Skill」一節寫的位置），原樣複製到 `resume-SEG` 的同一路徑；新對話才會自動載入。
4. 在 `resume-SEG` 的 `notes/SEG.md` 檔尾加上「改用 Recovery 前的狀態」：使用者的回答、兩個指令的結果、原 Repo 的完整路徑，註明「SEG 的成果由 Recovery 提供，不是我們自己完成」。不覆蓋複製過來的內容。複製來的 notes 提到的候選 id 是原 Repo 的，Recovery 不一定有，之後查不到是預期。
5. 用白話回報：`resume-SEG` 的完整路徑、帶過去了哪些資料夾與檔案、原 Repo 是否原封不動。停下。

中途失敗要重跑：先刪除學員包裡的 `recovery-SEG` 和 `repository` 裡的 `resume-SEG`（只刪這兩個，原 Repo 不動），再重跑第 2 步。

## 步驟 2、3：在 resume-SEG 開新的對話

`../../recovery-SEG/recovery-dlc-SEG/RECOVERY.md` 寫著這個 Recovery 的內容、接下來的指令和「看到什麼算成功」，照它做：

- D1：提案者在 `resume-d1` 開新對話，做 RECOVERY.md 第 2 節。
- D2 起：**夥伴**在 `resume-SEG` 開自己的新對話，做第 2 節（接手簽章；commit 前停下給夥伴看檔案清單，等「同意」）；**提案者**在 `resume-SEG` 開自己的新對話，做第 3 節（建環境並驗證）。

每段指令一樣整段在同一次執行裡跑，任何一步失敗就停下貼出錯誤，不改設定、不換寫法。結果寫進 `notes/recovery-SEG.md`。
