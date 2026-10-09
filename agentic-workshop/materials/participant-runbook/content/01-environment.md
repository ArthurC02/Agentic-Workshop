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

- **第 07 分鐘**：G0 Starter Repository（Greenfield 起始程式包）。主持人公布解鎖碼後，在 [Greenfield 任務](#greenfield) 頁面下載。
- **第 29 分鐘**：B0 Repository（Brownfield 起點：假設已上線 12 個月的既有程式）。主持人公布解鎖碼後，在 Time Skip（時間快轉）章節下載。

兩份程式碼都以 ZIP 形式內嵌在本 Runbook 中。每一版都請 Agent 在該版自己的資料夾內**獨立**建立環境（venv），不共用環境，也不混用不同版本的程式。

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到短路徑，例如 `C:\work\g0`、`C:\work\b0`，避免 Windows 路徑長度限制導致檔案解壓縮不完整。不要解壓縮到深層的同步資料夾或桌面子資料夾。
```

## 每一版的準備步驟

現在還沒有程式碼，不用做任何準備。建環境、跑起始測試的提示詞在 [Greenfield 任務](#greenfield) 檢查點 1，啟動伺服器的提示詞在檢查點 4；B0 的準備在 Time Skip 章節。到時候照該頁貼給 Agent 即可，這裡只放出錯時用的疑難排解。

## 疑難排解

遇到任何錯誤，先把錯誤訊息交給 Agent，請它用白話說明，不要自己動手修：

```text
剛才的步驟出錯了。請先不要修改任何檔案，用白話告訴我：錯誤訊息是什麼意思、可能的原因、你建議怎麼處理（列 1–2 個做法），然後停下等我決定。
```

```callout tip
venv 一律不啟用，直接呼叫裡面的 Python
Starter 的 README 寫的 `source .venv/bin/activate` 在 Windows 不適用（Windows 是 `.venv\Scripts`），啟用失敗時套件會裝進電腦上其他版本的 Python。檢查點 1 的提示詞已要求 Agent 用 `py -3.13 -m venv .venv` 建立環境，之後直接呼叫 `.venv\Scripts\python.exe`（Git Bash 寫 `.venv/Scripts/python.exe`），不照 README 啟用；Python 不是 3.13 時 Agent 會停下，請告知主持人。
```

```callout tip
/docs 頁面一片空白
/docs 的畫面要從網路載入，沒有網路時會是空白頁。請 Agent 改用 Python 的 httpx 實際呼叫同一組 API，把每一步的狀態碼和回應重點列給你看，並在 notes 註明「/docs 無法載入，改由 Agent 呼叫 API」。
```

```callout tip
Git 回報檔名太長（Filename too long）
多半是解壓縮的路徑太深。請 Agent 只在這個專案設定 `core.longpaths` 為 true（不要用 --global），或把 ZIP 重新解壓縮到更短的路徑，例如 `C:\work\g0`。
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
