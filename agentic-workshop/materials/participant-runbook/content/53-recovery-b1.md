---
id: recovery-b1
title: B1 Recovery 切換
minute: 52-63
group: recovery-b1
section: Brownfield｜Teammate
---

# B1 Recovery：52 分鐘按需切換

本頁是 Recovery（復原包：進度落後時改用的接續基線）。B1（修復學生票折扣異常）沒做完、但要接著做 B2 的小組，經主持人確認後，才會個別拿到本頁解鎖碼；一般 B2 解鎖碼打不開本頁。復原包只含 B1 該完成的修改，不含之後任務的內容；使用復原包不代表本組自己完成了 B1。

```download
id=recovery-52-b1 zip=recovery-52-b1.zip label=下載受控 B1 Recovery
```

## 保存與切換

- [ ] 先保存原本的 Repo、Diff、測試輸出、退出碼（exit code）、核准關卡（Gate）紀錄與未完成事項，不要覆蓋原成果。
- [ ] 解壓縮到新目錄，核對下載卡上的 SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同），並看包內 README 與 docs/context.md，確認這是 B1 完成後的版本。
- [ ] 在原本啟動 Server 的終端機按 Ctrl+C，停止自己啟動的服務；不要停止別人的服務。
- [ ] 在新目錄安裝並執行完整測試，預期 44 passed；結果不符就停止切換，請主持人確認。

```cmd
# powershell
# 在 ZIP 所在目錄；新目錄名稱尚未使用
Expand-Archive -LiteralPath .\recovery-52-b1.zip -DestinationPath .\resume-b1-52
Set-Location .\resume-b1-52\recovery-b1
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
# 在 ZIP 所在目錄；新目錄名稱尚未使用
unzip recovery-52-b1.zip -d resume-b1-52
cd resume-b1-52/recovery-b1
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

另開一個終端機確認 `/health` 有回應。版本要用包內說明文件（README、docs/context.md）、B1 的修改是否存在與測試結果一起確認，不能只看 Health 檢查。

```cmd
# powershell
Invoke-RestMethod http://127.0.0.1:8000/health
# bash
curl --fail http://127.0.0.1:8000/health
```

開一個新的 Agent 對話（Session），或在原對話中明確告訴 Agent：現在接手的是哪個版本、原成果還有哪些未完成、已確認的規則，以及 B2 已核准的範圍；更新共同脈絡（Shared Context）後，接續 [B2](#b2)。本頁不提供 B3 的起點。

```form
{"id": "recovery-b1-record", "title": "B1 Recovery 紀錄","fields":[
{"id": "decision", "label": "切換原因／核准的主持人／時間／復原包來源", "type": "textarea", "suggestions": [{"label": "觸發範本", "text": "觸發：〈B1 未完成的原因〉\n主持核准人：〈姓名〉；時間：第〈 〉分鐘\n提供來源：recovery-52-b1.zip"}]},
{"id": "preserved", "label": "原成果保存路徑／Diff／Gate 狀態／未完成事項", "type": "textarea", "suggestions": [{"label": "保存範本", "text": "原成果路徑：〈路徑〉\nDiff：〈已保存／路徑〉\nGate：〈狀態〉\n未完成：〈…〉"}]},
{"id": "verification", "label": "新目錄／確認是 B1 版本的證據／安裝、44 項測試與 Health 的實際結果及退出碼", "type": "textarea", "suggestions": [{"label": "驗證範本", "text": "新目錄：〈路徑〉\nB1 版本證據：〈SHA256／README／docs/context.md〉\n安裝：〈結果〉，退出碼〈 〉\npytest -q：〈 〉 passed，退出碼〈 〉\nHealth：〈實際回應〉"}]},
{"id": "context", "label": "新對話（Session）或重新提供的背景／接續的核准範圍／哪些不是本組自己完成的", "type": "textarea", "suggestions": [{"label": "接續範本", "text": "〈新 Session／重新輸入 Context〉\n接續核准範圍：〈B2 範圍〉\n非自行完成：B1 能力由 Recovery 提供"}]}
]}
```
