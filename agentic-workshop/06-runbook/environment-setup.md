# 環境準備

> 讀者：主持人與環境準備人員。時機：活動前。前置：取得本次受控來源與可用的通用Coding Agent。可見性：Facilitator；需另產學員版，不直接分享含內部定位的本檔。

統一Python3.13（已驗收3.13.15）、venv／pip、FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1；以各版requirements.txt為準。不需要前端、外部DB、真實金流／交通API。本機案例不依賴外部API；Agent服務或本機工具的可用性須另確認，不以案例Health代替Agent可用。

## 學員電腦：由Agent代為準備

全程人不碰程式：學員不自己打下列指令。學員在Agent對話貼上Runbook標準文字A（建.venv、安裝requirements.txt、跑pytest -q並白話回報；背景啟動8000埠伺服器、確認/health、給出/docs網址），由Agent代做；學員只在瀏覽器開/docs試API。主持事前要在每台學員電腦實測這條路徑可行（見[Preflight](preflight-checklist.md)），包括Agent有權限執行指令、能在背景啟動伺服器、瀏覽器能連到127.0.0.1。下列手動指令只供主持／環境準備人員驗證與排錯用。

## 每版獨立準備

在已核對來源的版本根目錄操作，不共用可變Store或跨版本Import。下列是待執行步驟，不代表本輪已安裝或Preflight。

PowerShell：

```powershell
python --version
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

一般shell：

```bash
python --version
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

pyproject的pytest設定包含src Import Path；啟動用`--app-dir src`。單獨Import或TestClient明確使用本版venv及src路徑。

PowerShell：

```powershell
$env:PYTHONPATH='src'
& '.\.venv\Scripts\python.exe' -c 'from smart_ticket.main import app; print(app.title, app.version)'
```

一般shell：

```bash
PYTHONPATH=src .venv/bin/python -c 'from smart_ticket.main import app; print(app.title, app.version)'
```

另一終端以`curl.exe http://127.0.0.1:8000/health`（PowerShell）或`curl`檢查200及status=ok，並檢查`/openapi.json`與App版本。切版先以Ctrl+C停止自己啟動的Server（學員電腦則請Agent停止它啟動的伺服器），確認新版本正常啟動，避免讀到舊程序；不終止其他人的程序。Port佔用時改未使用Port並記錄。

## 主持來源與學員發放

G0為`01-greenfield/participant/starter-repository/`，B0為`03-brownfield/participant/repository/smart-ticket-b0/`。G1與B1–B3位於Evaluation，只供主持驗證；學員只取得按[Recovery](recovery-plan.md)整理的受控版本，不能取得作者Repo或Bundle。

事前完成依賴下載／安裝與Agent操作確認；若網路不可用且依賴未備妥，改用事先已驗證環境或分析降級，不在90分鐘中臨時更換技術棧。各版venv不進交付包。資料固定種子、可控Clock／Gateway與In-Memory，重啟會重置；先保存學員成果再復原。

完成條件：逐版Python／依賴／Import／Health／OpenAPI及版本Gate真實證據完整、學員受控来源與Agent可用，且每台學員電腦的Agent能代為建環境、啟動伺服器，瀏覽器能開/docs；填[Preflight](preflight-checklist.md)，未執行項不勾選。
