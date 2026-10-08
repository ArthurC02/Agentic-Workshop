---
id: recovery-d1
title: D1 Recovery 切換
minute: 35-60
group: dlc-rec-d1
section: D1｜共同語言與邊界
---

# D1 Recovery：按需接續

主持人確認需要接續時，才會個別提供本頁解鎖碼；一般解鎖碼不會開啟本頁。內容是：起始 Repo，加上已確認的來源與一組 D1 候選（仍是候選，尚未審查）。使用 Recovery **不代表你們自己完成了 D1**，請在下方表單如實記錄。

```download
id=recovery-dlc-d1 zip=recovery-dlc-d1.zip label=下載 D1 Recovery
```

## 保存原成果

- [ ] 不要覆寫或刪除原本的 Repo。在原 Repo 執行 `git status` 與 `git log --oneline -3`，把結果記在下方表單。

## 切換到 Recovery

- [ ] 在原 Repo 的**上一層**（`repository` 資料夾）執行。指令會把 ZIP 解到 `C:\dlc-rec\d1`，找出含 `requirements.txt` 的資料夾，複製成 `resume-d1`，讓 `..\..\tools` 仍然指向學員包的工具：

```cmd
# powershell
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d1.zip" -DestinationPath C:\dlc-rec\d1
$src = Split-Path (Get-ChildItem C:\dlc-rec\d1 -Recurse -Filter requirements.txt | Select-Object -First 1).FullName
Copy-Item -Recurse $src .\resume-d1
Set-Location .\resume-d1
# bash
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
unzip -q ~/Downloads/recovery-dlc-d1.zip -d /c/dlc-rec/d1
src=$(dirname "$(find /c/dlc-rec/d1 -name requirements.txt | head -1)")
cp -r "$src" ./resume-d1
cd resume-d1
```

- [ ] 在 `resume-d1` 建 venv、安裝依賴、跑全部測試：

```cmd
# powershell
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
# bash
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
```

**看到什麼算成功**：全部 `passed`，沒有 `failed` 或 `error`。結果不符就停止切換，請主持人確認。

- [ ] 建立 Git 起點（第一個 commit 刻意不含 `domain-memory/`，原因見下方），並驗證 Registry：

```cmd
# powershell
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git rm -r -q --cached domain-memory
git commit -m "D1 Recovery 起點（不含 Registry）"
Set-ExecutionPolicy -Scope Process Bypass -Force
..\..\tools\dm.ps1 validate
..\..\tools\dm.ps1 verify-evidence
# bash
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git rm -r -q --cached domain-memory
git commit -m "D1 Recovery 起點（不含 Registry）"
../../tools/dm.sh validate
../../tools/dm.sh verify-evidence
```

**看到什麼算成功**：`Registry is valid.`；`verify-evidence` 的過期（stale）、不存在（missing）、格式錯誤（invalid）都是 0。

第一個 commit **刻意不含** `domain-memory/`：D2 要先設定簽章，第一個包含 Registry 的 commit 必須是簽章 commit。`git status` 會看到 `domain-memory/` 是未追蹤，這是正確的。

- [ ] 在 `resume-d1` 開一個**新的** Agent Session（結束目前的 Agent 對話，在 `resume-d1` 重新啟動 Agent），告訴它：這是 Recovery 起點、Domain Memory 在 `domain-memory/`、只能用 `..\..\tools\dm.ps1`（Git Bash：`../../tools/dm.sh`）做唯讀查詢。然後回到 [D2](#d2) 接續。

```form
{"id": "recovery-d1-record", "title": "D1 Recovery 紀錄","fields":[
{"id": "trigger", "label": "觸發原因／提供的時間", "type": "textarea", "suggestions": [{"label": "觸發範本", "text": "原因：〈D1 未完成的原因〉\n提供時間：第〈 〉分鐘\n來源：recovery-dlc-d1.zip"}]},
{"id": "preserved", "label": "原成果保存位置與狀態", "type": "textarea", "suggestions": [{"label": "保存範本", "text": "原 Repo：〈路徑〉\ngit log 最新：〈 〉\n自己完成到：〈檢查點 〉"}]},
{"id": "verification", "label": "新目錄的測試與 Registry 驗證（實際輸出）", "type": "textarea", "suggestions": [{"label": "驗證範本", "text": "新目錄：〈路徑〉\npytest -q：〈 〉 passed，〈 〉 failed\nvalidate：〈 〉\nverify-evidence：〈 〉"}]},
{"id": "not-own", "label": "非自行完成的部分", "type": "text", "suggestions": ["D1 的成果由 Recovery 提供"]}
]}
```
