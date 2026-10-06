---
id: time-skip
title: Time Skip：12 個月後
minute: 29-33
group: timeskip
section: Time Skip
---

# Time Skip：12 個月後

Smart Ticket 已上線 12 個月。從現在開始，請停止自己的 Greenfield 開發，改為接手主持人統一提供的 **B0 - Brownfield Baseline**。Agent 的角色從 **Tool** 轉為 **Teammate**：先各自分析、比較判斷，再整合成小組 Shared Context。

| 分鐘 | 你要做什麼 |
|---:|---|
| 29–33 | 閱讀公告與交接說明，下載 B0，建立環境並執行測試 |
| 33–39 | 用自己的 Agent 個人分析 B0，填寫 [個人 Agent 分析表](#individual-analysis) |
| 39–44 | 小組比較分析，整理 [Shared Context](#shared-context) |
| 44–52 | 依發放的任務與核准計畫工作 |

## 時間快轉公告

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md
```

## 公司與系統成長摘要

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/02-company-growth-summary.md
```

## Brownfield 接手說明

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/03-brownfield-handover.md
```

## 步驟 1：停止 Greenfield 開發

- [ ] 停止修改自己的 Greenfield Repository，保留現況，不要刪除或覆寫。
- [ ] 在自己啟動 Server 的終端機按 `Ctrl+C` 停止 G0 的 App。

```callout info
B0 是一份新的 Repository
B0 不是你的 Greenfield 成果延伸。請在新的資料夾開啟 B0，並為它重新建立 Agent Session 與 Context，不要沿用 Greenfield 的 Session。
```

## 步驟 2：下載並解壓縮 B0 Repository

```download
id=b0 zip=participant-29-b0.zip label=下載 B0 Repository
```

- [ ] 下載 `b0.zip`。
- [ ] 解壓縮到短路徑，例如 `C:\work\b0`（依實際下載位置調整指令中的路徑）。
- [ ] 進入 `smart-ticket-b0` 資料夾（含 `README.md` 與 `requirements.txt`）。

```cmd
# powershell
Expand-Archive -Path "$HOME\Downloads\b0.zip" -DestinationPath C:\work\b0
cd C:\work\b0\agentic-workshop\03-brownfield\participant\repository\smart-ticket-b0
# bash
unzip ~/Downloads/b0.zip -d ~/work/b0
cd ~/work/b0/agentic-workshop/03-brownfield/participant/repository/smart-ticket-b0
```

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到 `C:\work\b0` 這類短路徑，不要放在深層的同步資料夾或桌面子資料夾，避免 Windows 路徑長度限制導致檔案不完整。
```

## 步驟 3：建立環境並執行測試

依 B0 的 `README.md`，在 `smart-ticket-b0` 資料夾內**獨立**建立 venv，不要沿用 G0 的環境。

- [ ] 建立 venv 並安裝依賴，執行 `pip check`。
- [ ] 執行 `pytest -q`，保留實際輸出，供個人分析使用。
- [ ] 確認版本：App 版本為 `B0`。
- [ ] 啟動 App，確認 `GET /health` 回傳 `{"status":"ok"}`。

```cmd
# powershell
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\python.exe' -m pytest -q
$env:PYTHONPATH='src'
& '.\.venv\Scripts\python.exe' -c 'from smart_ticket.main import app; print(app.title, app.version)'
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -c 'from smart_ticket.main import app; print(app.title, app.version)'
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

App 啟動後，另開一個終端機確認 Health：

```cmd
# powershell
curl.exe http://127.0.0.1:8000/health
# bash
curl http://127.0.0.1:8000/health
```

```callout warning
目前有若干測試失敗
目前有若干測試失敗，需要小組分析是否具有共同原因。**請先不要修改程式**，各自使用自己的 Agent 完成分析；保留測試輸出、規則來源與推論依據。
```

```callout tip
環境問題
Port 被佔用、venv 無法啟用或依賴無法安裝時，處理方式請見 [環境準備](#environment)。環境無法啟動時請立即告知主持人；請使用主持人提供的同一份 B0，不要改用其他版本。
```

## 完成檢核

- [ ] 已切換到同一份 B0，並確認版本為 B0 - Brownfield Baseline。
- [ ] 理解安裝與測試方法，已保留 `pytest -q` 的實際輸出。
- [ ] 尚未直接修改程式，準備進入 [B0 系統 Context](#b0-context) 與個人分析。
