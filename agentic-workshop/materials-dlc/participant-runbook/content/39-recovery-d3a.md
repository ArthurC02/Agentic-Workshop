---
id: recovery-d3a
title: D3a Recovery 切換
minute: 95-125
group: dlc-rec-d3a
section: D3｜受治理的變更
---

# D3a Recovery：按需接續

主持人揭曉之後，才會個別提供本頁解鎖碼；一般解鎖碼不會開啟本頁。內容是：D3a 完成後的 Repo 與 Registry（含電子發票的實作與測試）。使用 Recovery **不代表你們自己完成了 D3a**，請在下方表單如實記錄。

```download
id=recovery-dlc-d3a zip=recovery-dlc-d3a.zip label=下載 D3a Recovery
```

## 保存原成果

- [ ] 不要覆寫或刪除原本的 Repo。在原 Repo 執行 `git status` 與 `git log --oneline -3`，把結果記在下方表單。
- [ ] 若有自己啟動的 Server，在它的終端機按 `Ctrl+C` 停止；不要停止別人的程序。

## 切換到 Recovery

- [ ] 在原 Repo 的**上一層**（`repository` 資料夾）執行。指令會把 ZIP 解到 `C:\dlc-rec\d3a`，找出含 `requirements.txt` 的資料夾，複製成 `resume-d3a`，讓 `..\..\tools` 仍然指向學員包的工具：

```cmd
# powershell
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d3a.zip" -DestinationPath C:\dlc-rec\d3a
$src = Split-Path (Get-ChildItem C:\dlc-rec\d3a -Recurse -Filter requirements.txt | Select-Object -First 1).FullName
Copy-Item -Recurse $src .\resume-d3a
Set-Location .\resume-d3a
# bash
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
unzip -q ~/Downloads/recovery-dlc-d3a.zip -d /c/dlc-rec/d3a
src=$(dirname "$(find /c/dlc-rec/d3a -name requirements.txt | head -1)")
cp -r "$src" ./resume-d3a
cd resume-d3a
```

- [ ] 在 `resume-d3a` 建 venv、安裝依賴、跑全部測試：

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

- [ ] 建立 Git 起點，並驗證 Registry：

```cmd
# powershell
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git commit -m "D3a Recovery 起點"
Set-ExecutionPolicy -Scope Process Bypass -Force
..\..\tools\dm.ps1 validate
..\..\tools\dm.ps1 verify-audit
# bash
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git commit -m "D3a Recovery 起點"
../../tools/dm.sh validate
../../tools/dm.sh verify-audit
```

**看到什麼算成功**：`Registry is valid.`（Registry 含候選，所以不帶 `--require-reviewed`）；`verify-audit` 回 `"status": "valid"`。

這個新 Repo 沒有簽章設定也沒有 pre-push hook，之後的 commit 不會簽章、也不需要 push；本段只登記候選，不再做核准。

- [ ] 在 `resume-d3a` 開一個**新的** Agent Session，告訴它：這是 Recovery 起點、Domain Memory 在 `domain-memory/`、只能用 `..\..\tools\dm.ps1`（Git Bash：`../../tools/dm.sh`）做唯讀查詢。然後回到 [D3b](#d3b) 接續。

```form
{"id": "recovery-d3a-record", "title": "D3a Recovery 紀錄","fields":[
{"id": "trigger", "label": "觸發原因／提供的時間", "type": "textarea", "suggestions": [{"label": "觸發範本", "text": "原因：〈D3a 未完成的原因〉\n提供時間：第〈 〉分鐘\n來源：recovery-dlc-d3a.zip"}]},
{"id": "preserved", "label": "原成果保存位置與狀態", "type": "textarea", "suggestions": [{"label": "保存範本", "text": "原 Repo：〈路徑〉\ngit log 最新：〈 〉\n自己完成到：〈檢查點 〉"}]},
{"id": "verification", "label": "新目錄的測試與 Registry 驗證（實際輸出）", "type": "textarea", "suggestions": [{"label": "驗證範本", "text": "新目錄：〈路徑〉\npytest -q：〈 〉 passed，〈 〉 failed\nvalidate：〈 〉\nverify-audit：〈 〉"}]},
{"id": "not-own", "label": "非自行完成的部分", "type": "text", "suggestions": ["D3a 的成果由 Recovery 提供"]}
]}
```
