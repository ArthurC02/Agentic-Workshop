---
id: recovery-d1
title: D1 Recovery 切換
minute: 35-60
group: dlc-rec-d1
section: D1｜共同語言與邊界
---

# D1 Recovery：按需接續

主持人確認需要接續時，才會個別提供本頁解鎖碼；一般解鎖碼不會開啟本頁。內容是：起始 Repo，加上已確認的來源與一組 D1 候選（仍是候選，尚未審查）。使用 Recovery **不代表你們自己完成了 D1**，下方提示詞會請 Agent 如實記錄：拿到 Recovery 的分鐘、原因、自己完成到哪裡。本頁沒有表單。

切換分兩步：先在原本的 Agent 對話保存成果並解出 Recovery，再到新資料夾開一個新的 Agent 對話接續。原本的 Repo 不改名、不覆寫、不刪除。D1 還沒有簽章，兩步都沒有 commit：Recovery 附上的 Git 歷史只有一個不含 `domain-memory/` 的「起始 Repo」commit，`domain-memory/` 還原後仍未追蹤，留給 D2 先設好簽章再 commit。

```download
id=recovery-dlc-d1 zip=recovery-dlc-d1.zip label=下載 D1 Recovery
```

## 步驟 1 · 保存原成果並解出 Recovery

- [ ] 按上方按鈕下載 `recovery-dlc-d1.zip`（存到「下載」資料夾）。
- [ ] 把下方提示詞貼給**原本**的 Agent：

```text
我要改用 D1 Recovery 接續。不要修改或刪除目前這個 Repo，也不要 git commit；任何一步失敗就停下，不要自己繞過：
1. 在目前 Repo 執行 git status 與 git log --oneline -3，然後問我：現在是第幾分鐘、主要卡在哪裡、自己完成到 D1 第幾個檢查點。把回答、這兩個指令的結果與目前 Repo 的完整路徑寫進 notes/d1.md 的「改用 Recovery 前的狀態」，註明「D1 的成果由 Recovery 提供，不是自己完成」。
2. 把 Recovery 解到 C:\dlc-rec\d1，再把裡面的 smart-ticket-dlc-base 複製成 repository 資料夾裡的 resume-d1（和原 Repo 同一層，..\..\tools 才會指向學員包的工具）。這一步不碰 Git：
PowerShell：
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d1.zip" -DestinationPath C:\dlc-rec\d1
$rec = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter repo.bundle | Select-Object -First 1).FullName
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .\resume-d1
Git Bash：
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
unzip -q ~/Downloads/recovery-dlc-d1.zip -d /c/dlc-rec/d1
rec=$(dirname "$(find /c/dlc-rec/d1 -name repo.bundle | head -1)")
cp -r "$rec/smart-ticket-dlc-base" ./resume-d1
3. 用白話告訴我 resume-d1 的完整路徑，以及原 Repo 是否原封不動。做完停下。
```

**看到什麼算過關**：原 Repo 的 `notes/d1.md` 有「改用 Recovery 前的狀態」；`resume-d1` 已建立，原 Repo 沒有被改動。

## 步驟 2 · 在 resume-d1 開新的 Agent 對話，還原並驗證

- [ ] 結束目前的 Agent 對話，在 `resume-d1` 資料夾重新開啟 Agent。
- [ ] 先貼 [開場與環境](#environment) 的工作規則，再貼下方提示詞：

```text
這是 D1 Recovery 起點，Repo 根目錄是 resume-d1：Domain Memory 在 domain-memory/，裡面全部是候選。不要 git add 或 commit domain-memory/。依終端機選一組，在「同一次執行」裡依序跑（rec 變數要在同一次執行內才有值），任何一步失敗就停下：
PowerShell：
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
Git Bash：
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
用白話告訴我：git status 列了什麼、pytest 最後一行、validate 結果、verify-evidence 的 stale／missing／invalid 各幾個。把結果寫進 notes/recovery-d1.md，開頭註明「D1 的成果由 Recovery 提供；原 Repo 的狀態記在原 Repo 的 notes/d1.md」。不要 commit，做完停下。
```

**看到什麼算過關**：

- `git status` 只列出 `?? domain-memory/`（未追蹤，這是正確的）。
- pytest 全部 `passed`，沒有 `failed` 或 `error`。
- `Registry is valid.`；`verify-evidence` 的過期（stale）、不存在（missing）、格式錯誤（invalid）都是 0。

完成後回到 [D2](#d2) 接續：D2 開始時，夥伴在 `resume-d1` 另開終端機與自己的 Agent 對話。
