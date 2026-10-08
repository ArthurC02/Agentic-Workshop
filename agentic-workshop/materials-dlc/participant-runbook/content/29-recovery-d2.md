---
id: recovery-d2
title: D2 Recovery 切換
minute: 45-70
group: dlc-rec-d2
section: D2｜審查與核准
---

# D2 Recovery：按需接續

主持人確認需要接續時，才會個別提供本頁解鎖碼；一般解鎖碼不會開啟本頁。內容是：起始 Repo，加上已審查、簽章並套用的 Registry（全部是已審查（reviewed）事實）。使用 Recovery **不代表你們自己完成了 D2**，請在下方表單如實記錄。

```download
id=recovery-dlc-d2 zip=recovery-dlc-d2.zip label=下載 D2 Recovery
```

## 保存原成果

- [ ] 不要覆寫或刪除原本的 Repo。在原 Repo 執行 `git status` 與 `git log --oneline -3`，把結果記在下方表單。

## 切換到 Recovery

- [ ] 在原 Repo 的**上一層**（`repository` 資料夾）執行。指令會把 ZIP 解到 `C:\dlc-rec\d2`，找出含 `requirements.txt` 的資料夾，複製成 `resume-d2`，讓 `..\..\tools` 仍然指向學員包的工具：

```cmd
# powershell
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository
Expand-Archive -LiteralPath "$HOME\Downloads\recovery-dlc-d2.zip" -DestinationPath C:\dlc-rec\d2
$src = Split-Path (Get-ChildItem C:\dlc-rec\d2 -Recurse -Filter requirements.txt | Select-Object -First 1).FullName
Copy-Item -Recurse $src .\resume-d2
Set-Location .\resume-d2
# bash
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository
unzip -q ~/Downloads/recovery-dlc-d2.zip -d /c/dlc-rec/d2
src=$(dirname "$(find /c/dlc-rec/d2 -name requirements.txt | head -1)")
cp -r "$src" ./resume-d2
cd resume-d2
```

- [ ] 在 `resume-d2` 建 venv、安裝依賴、跑全部測試：

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
git commit -m "D2 Recovery 起點"
Set-ExecutionPolicy -Scope Process Bypass -Force
..\..\tools\dm.ps1 validate --require-reviewed
..\..\tools\dm.ps1 verify-audit
# bash
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git commit -m "D2 Recovery 起點"
../../tools/dm.sh validate --require-reviewed
../../tools/dm.sh verify-audit
```

**看到什麼算成功**：`Registry is valid.`（帶 `--require-reviewed`，表示全部是 reviewed）；`verify-audit` 回 `"status": "valid"`。

這個新 Repo 沒有簽章設定也沒有 pre-push hook（push 前 Git 自動執行的檢查腳本），之後的 commit 不會簽章、也不需要 push；本段只登記候選，不再做核准。

- [ ] 在 `resume-d2` 開一個**新的** Agent Session（結束目前的 Agent 對話，在 `resume-d2` 重新啟動 Agent），告訴它：這是 Recovery 起點、Domain Memory 在 `domain-memory/`、只能用 `..\..\tools\dm.ps1`（Git Bash：`../../tools/dm.sh`）做唯讀查詢。然後回到 [D3a](#d3a) 接續。

```form
{"id": "recovery-d2-record", "title": "D2 Recovery 紀錄","fields":[
{"id": "trigger", "label": "觸發原因／提供的時間", "type": "textarea", "suggestions": [{"label": "觸發範本", "text": "原因：〈D2 未完成的原因〉\n提供時間：第〈 〉分鐘\n來源：recovery-dlc-d2.zip"}]},
{"id": "preserved", "label": "原成果保存位置與狀態", "type": "textarea", "suggestions": [{"label": "保存範本", "text": "原 Repo：〈路徑〉\ngit log 最新：〈 〉\n自己完成到：〈檢查點 〉"}]},
{"id": "verification", "label": "新目錄的測試與 Registry 驗證（實際輸出）", "type": "textarea", "suggestions": [{"label": "驗證範本", "text": "新目錄：〈路徑〉\npytest -q：〈 〉 passed，〈 〉 failed\nvalidate --require-reviewed：〈 〉\nverify-audit：〈 〉"}]},
{"id": "not-own", "label": "非自行完成的部分", "type": "text", "suggestions": ["D2 的成果由 Recovery 提供"]}
]}
```
