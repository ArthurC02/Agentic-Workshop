---
id: environment
title: 環境準備
minute: 00-07
group: open
section: 開始之前
---

# 環境準備

工作坊時間要用來體驗 Agent 協作，不是處理安裝問題。請在開場時確認下列項目，有問題立即告知主持人。

## 前置需求

- [ ] Python **3.13**（已驗收版本 3.13.15），可使用 `venv` 與 `pip`。
- [ ] 一個可用的通用 Coding Agent，能讀取本機資料夾、修改檔案並執行終端指令。
- [ ] 可開啟 PowerShell 或 bash 終端機。
- [ ] 已安裝 Git（`git --version` 有回應），用來查看 Agent 的實際修改；沒有 Git 時，改用 Agent 或編輯器內建的變更檢視。
- [ ] 已用瀏覽器開啟這份 `runbook.html`。

套件由各版 `requirements.txt` 指定：FastAPI 0.115.12、Uvicorn 0.34.2、Pydantic 2.11.4、pytest 8.3.5、httpx 0.28.1。不需要前端、外部資料庫、真實金流或交通 API。

```cmd
# powershell
python --version
# bash
python --version
```

## 你會在什麼時候拿到程式碼

| 分鐘 | 取得內容 | 取得方式 |
|---:|---|---|
| 07 | G0 Starter Repository | 主持人公布解鎖碼後，在 [Greenfield 任務](#greenfield) 頁面下載 |
| 29 | B0 Repository | 主持人公布解鎖碼後，在 Time Skip 章節下載 |

兩份程式碼都以 ZIP 形式內嵌在本 Runbook 中。每一版都要在自己的資料夾內**獨立**建立 venv，不共用環境，也不跨版本 Import。

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到短路徑，例如 `C:\work\g0`、`C:\work\b0`，避免 Windows 路徑長度限制導致檔案解壓縮不完整。不要解壓縮到深層的同步資料夾或桌面子資料夾。
```

## 每一版的準備步驟

在該版 Repository 的根目錄（含 `requirements.txt` 的資料夾）執行：

- [ ] 建立 venv 並安裝依賴
- [ ] 執行 `pip check` 與 `pytest -q`，記錄實際輸出
- [ ] 啟動 App 並確認 `GET /health`

```cmd
# powershell
python --version
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
python --version
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

`pyproject.toml` 的 pytest 設定已包含 `src` Import Path；啟動 App 時使用 `--app-dir src`。

### 確認 Health

App 啟動後，另開一個終端機檢查 `/health` 回傳 200 且 `status` 為 `ok`：

```cmd
# powershell
curl.exe http://127.0.0.1:8000/health
# bash
curl http://127.0.0.1:8000/health
```

預期回應為 `{"status":"ok"}`。也可以用同樣方式檢查 `/openapi.json`，確認 API 清單與 App 版本。

### 選用：確認 Import

單獨 Import 或使用 TestClient 時，請明確使用本版 venv 及 `src` 路徑：

```cmd
# powershell
$env:PYTHONPATH='src'
& '.\.venv\Scripts\python.exe' -c 'from smart_ticket.main import app; print(app.title, app.version)'
# bash
PYTHONPATH=src .venv/bin/python -c 'from smart_ticket.main import app; print(app.title, app.version)'
```

## 疑難排解

```callout tip
PowerShell 無法啟用 venv
若 `.\.venv\Scripts\Activate.ps1` 受執行原則限制，不需要啟用 venv，直接用 `.\.venv\Scripts\python.exe -m ...` 執行，例如上方的指令區塊。
```

```callout tip
Port 8000 已被佔用
改用其他未使用的 Port（例如 `--port 8001`），並在 Health 檢查與交付紀錄中寫下實際使用的 Port。
```

```callout warning
切換版本前先停止舊的 Server
從 G0 換到 B0 前，先在自己啟動 Server 的終端機按 `Ctrl+C` 停止，再確認新版本正常啟動，避免讀到舊程序。不要終止其他人的程序。
```

```callout info
資料重啟會重置
案例使用固定 Seed、可控的時鐘與付款模擬，資料存在記憶體中（In-Memory），重啟 App 就會回到初始狀態。這是設計行為，不是錯誤。
```

```callout danger
依賴無法安裝時
若網路不可用或 `pip install` 失敗，請立即告知主持人，不要在活動中臨時更換 Python 版本或技術棧。
```
