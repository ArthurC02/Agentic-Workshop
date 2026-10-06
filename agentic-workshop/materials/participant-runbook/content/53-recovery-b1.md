---
id: recovery-b1
title: B1 Recovery 切換
minute: 52-63
group: recovery-b1
section: Brownfield｜Teammate
---

# B1 Recovery：52 分鐘按需切換

主持確認 B1 未完成且需接續 B2 後，才個別提供本頁解鎖碼。一般 B2 解鎖不會開啟本頁。只提供已結束階段的 B1 能力，不含後續能力；使用 Recovery 不代表本組自行完成 B1。

```download
id=recovery-52-b1 zip=recovery-52-b1.zip label=下載受控 B1 Recovery
```

## 保存與切換

- [ ] 保存原 Repo、Diff、測試輸出、退出碼、Gate 與未完成事項，不覆寫原成果。
- [ ] 在新目錄解壓，核對下載卡 SHA256 與包內 README、docs/context.md，確認起點 B1。
- [ ] 在舊 Server 的終端按 Ctrl+C 停止自己啟動的服務；不可停止他人服務。
- [ ] 在新目錄安裝並執行完整測試，預期 44 passed；結果不符停止切換並請主持確認。

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

另開終端驗證 Health；包內 Context、B1 能力與測試結果共同確認版本，不能只憑 Health 判定。

```cmd
# powershell
Invoke-RestMethod http://127.0.0.1:8000/health
# bash
curl --fail http://127.0.0.1:8000/health
```

建立新 Agent Session，或明確重新輸入接手版本、原成果未完成事項、已確認規則與 B2 核准範圍；更新 Shared Context 後接續 [B2](#b2)。不提供 B3 實作起點。

```form
{"id":"recovery-b1-record","title":"B1 Recovery 紀錄","fields":[{"id":"decision","label":"觸發／主持核准人／時間／提供來源","type":"textarea"},{"id":"preserved","label":"原成果保存路徑／Diff／Gate／未完成","type":"textarea"},{"id":"verification","label":"新目錄／B1版本證據／安裝、44項測試及Health實際結果與退出碼","type":"textarea"},{"id":"context","label":"新Session或Context／接續核准範圍／非自行完成能力","type":"textarea"}]}
```
