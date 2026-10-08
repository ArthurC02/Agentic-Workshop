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

- [ ] 電腦已安裝 Python **3.13**（已驗收版本 3.13.15）；版本由 Agent 在準備環境時幫你確認。
- [ ] 一個可用的通用 Coding Agent，能讀取本機資料夾、修改檔案並執行終端指令。今天所有指令都由 Agent 執行，你不需要自己打指令。
- [ ] 已安裝 Git，Agent 會用它記錄起始狀態並回報實際修改了什麼；沒有 Git 時，請 Agent 改用它內建的變更檢視，並在交付摘要註明。
- [ ] 已用瀏覽器開啟這份 `runbook.html`。

套件由各版 `requirements.txt` 指定：FastAPI 0.115.12、Uvicorn 0.34.2、Pydantic 2.11.4、pytest 8.3.5、httpx 0.28.1。不需要前端、外部資料庫、真實金流或交通 API。

## 你會在什麼時候拿到程式碼

| 分鐘 | 取得內容 | 取得方式 |
|---:|---|---|
| 07 | G0 Starter Repository（Greenfield 起始程式包） | 主持人公布解鎖碼後，在 [Greenfield 任務](#greenfield) 頁面下載 |
| 29 | B0 Repository（Brownfield 起點：假設已上線 12 個月的既有程式） | 主持人公布解鎖碼後，在 Time Skip（時間快轉）章節下載 |

兩份程式碼都以 ZIP 形式內嵌在本 Runbook 中。每一版都請 Agent 在該版自己的資料夾內**獨立**建立環境（venv），不共用環境，也不混用不同版本的程式。

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到短路徑，例如 `C:\work\g0`、`C:\work\b0`，避免 Windows 路徑長度限制導致檔案解壓縮不完整。不要解壓縮到深層的同步資料夾或桌面子資料夾。
```

## 每一版的準備步驟

解壓縮後，在該版 Repository 的根目錄（含 `requirements.txt` 的資料夾）開啟你的 Agent，先貼上該段的「Agent 工作規則」，再依序貼上下面兩段提示詞：

- [ ] 請 Agent 準備環境並執行起始測試，記下它回報的測試結果

```text
請幫我準備這個專案的執行環境：確認 Python 版本是 3.13，在專案資料夾建立 .venv 虛擬環境並安裝 requirements.txt，接著執行 pytest -q。用白話告訴我：環境是否建好、測試有幾個通過／失敗／跳過，以及下一步要做什麼。遇到錯誤時先說明原因，不要自行修改程式。
```

- [ ] 請 Agent 啟動 App，確認健康檢查正常並取得 `/docs` 網址

```text
請在背景啟動這個專案的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 回傳 status=ok，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
```

- [ ] 用瀏覽器開 Agent 給你的 `/docs` 網址，看得到 API 清單就代表 App 正常運作。

### 備用：手動指令

只有 Agent 無法執行指令、且主持人請你手動處理時才使用：

```cmd
# powershell
python --version
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
python --version
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

## 疑難排解

```callout tip
Agent 回報無法啟用 venv
Windows 的 PowerShell 可能因執行原則限制無法啟用 venv。請 Agent 不要啟用，直接用 `.venv` 裡的 Python 執行即可。
```

```callout tip
Port 8000 已被佔用
請 Agent 改用其他未使用的埠號（Port，例如 8001），告訴你新的 `/docs` 網址；在交付紀錄中寫下實際使用的 Port。
```

```callout warning
切換版本前先停止舊的 Server
從 G0 換到 B0 前，先請 G0 的 Agent 停止它啟動的伺服器，再請 B0 的 Agent 啟動新版本並確認正常，避免讀到舊程序。不要終止其他人的程序。
```

```callout info
資料重啟會重置
案例使用固定的 Seed Data（系統預設的測試資料）、可控的時鐘與付款模擬，資料存在記憶體中（In-Memory），重啟 App 就會回到初始狀態。這是設計行為，不是錯誤。
```

```callout danger
依賴無法安裝時
若網路不可用或 Agent 回報套件安裝失敗，請立即告知主持人，不要在活動中臨時更換 Python 版本或技術棧。
```
