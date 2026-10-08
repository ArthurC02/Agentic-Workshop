---
id: time-skip
title: Time Skip：12 個月後
minute: 29-33
group: timeskip
section: Time Skip
---

# Time Skip：12 個月後

這是 Time Skip（時間快轉：專案假設已開發一段時間）：Smart Ticket 已上線 12 個月。請在 **4 分鐘**內停止自己的 Greenfield（從頭開始的新專案）開發，改為接手主持人統一提供的 **B0 - Brownfield Baseline**，建好環境、跑過測試。Brownfield 是已有程式碼的既有專案；B0 是它的起點版本，之後的 B1、B2、B3 是接在 B0 上的三段任務代號。Agent 的角色從 **Tool**（工具）轉為 **Teammate**（隊友）：先各自分析、比較判斷，再整合成小組的共同脈絡（Shared Context：小組整理出的共同事實）。

```callout warning
本段只接手，不修改
本段只做停手、下載、建環境、跑測試。**不要修改 B0 的程式**，也先不要叫 Agent 開始分析；個人分析從第 33 分鐘開始。全場使用同一份 B0，不要用自己的 Greenfield 成果代替。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要填的表單，全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 停手 | 29–30 | 00–01 | 停止 Greenfield、保留現況，讀時間快轉公告 |
| 2 · 取得 B0 | 30–31 | 01–02 | 下載 B0、解壓到短路徑，開新的 Agent Session |
| 3 · 環境與版本 | 31–32 | 02–03 | 建 venv、安裝，確認版本是 B0、Health 正常 |
| 4 · 測試與基準 | 32–33 | 03–04 | 跑 `pytest -q` 保留輸出、建立 Git 基準，讀交接說明 |

接下來：第 33–39 分鐘用自己的 Agent [個人分析](#individual-analysis)（先讀 [B0 系統 Context](#b0-context)）→ 第 39–44 分鐘小組整理 [Shared Context](#shared-context) → 第 44–52 分鐘依發放的任務與核准計畫工作。

## 檢查點 1 · 停手（第 29–30 分鐘）

- [ ] 停止修改自己的 Greenfield Repository，保留現況，不要刪除或覆寫。
- [ ] 在自己啟動 Server 的終端機按 `Ctrl+C` 停止 G0（Greenfield 起始包）的 App。
- [ ] 讀下方時間快轉公告與公司成長摘要。

### 時間快轉公告

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md
```

### 公司與系統成長摘要

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/02-company-growth-summary.md
```

```form
{"id":"ts-cp1","title":"檢查點 1 確認","fields":[
{"id":"stopped","label":"已停止修改 Greenfield、保留現況，G0 的 App 已停止","type":"checkbox"}
]}
```

## 檢查點 2 · 取得 B0（第 30–31 分鐘）

```download
id=b0 zip=participant-29-b0.zip label=下載 B0 Repository
```

- [ ] 下載 `b0.zip`，解壓縮到短路徑，例如 `C:\work\b0`（依實際下載位置調整指令中的路徑）。
- [ ] 進入 `smart-ticket-b0` 資料夾（含 `README.md` 與 `requirements.txt`）。

```cmd
# powershell
Expand-Archive -Path "$HOME\Downloads\b0.zip" -DestinationPath C:\work\b0
cd C:\work\b0\agentic-workshop\03-brownfield\participant\repository\smart-ticket-b0
# bash
unzip ~/Downloads/b0.zip -d ~/work/b0
cd ~/work/b0/agentic-workshop/03-brownfield/participant/repository/smart-ticket-b0
```

- [ ] 在 `smart-ticket-b0` 開啟**新的** Agent Session（與 Agent 的對話工作階段）。先不要交代任何工作。

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到 `C:\work\b0` 這類短路徑，不要放在深層的同步資料夾或桌面子資料夾，避免 Windows 路徑長度限制導致檔案不完整。
```

```callout info
B0 是一份新的 Repository
B0 不是你的 Greenfield 成果延伸。請在新的資料夾開啟 B0，並為它重新建立 Agent Session 與 Context，不要沿用 Greenfield 的 Session。
```

```form
{"id": "ts-cp2", "title": "檢查點 2 確認","fields":[
{"id": "path", "label": "B0 的資料夾路徑", "type": "text", "hint": "例如：C:\\work\\b0\\…\\smart-ticket-b0", "suggestions": [{"label": "路徑範本", "text": "C:\\work\\b0\\〈…〉\\smart-ticket-b0"}]},
{"id": "session", "label": "已在 B0 資料夾開啟新的 Agent Session（沒有沿用 Greenfield 的 Session）", "type": "checkbox"}
]}
```

## 檢查點 3 · 環境與版本（第 31–32 分鐘）

依 B0 的 `README.md`，在 `smart-ticket-b0` 資料夾內**獨立**建立 venv（Python 虛擬環境），不要沿用 G0 的環境。

- [ ] 建立 venv 並安裝依賴，執行 `pip check`。
- [ ] 確認版本：App 版本為 `B0`。
- [ ] 啟動 App，另開一個終端機確認 `GET /health` 回傳 `{"status":"ok"}`。

```cmd
# powershell
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
$env:PYTHONPATH='src'
& '.\.venv\Scripts\python.exe' -c 'from smart_ticket.main import app; print(app.title, app.version)'
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
PYTHONPATH=src .venv/bin/python -c 'from smart_ticket.main import app; print(app.title, app.version)'
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

App 啟動後，另開一個終端機確認 Health（健康檢查端點，用來確認服務有正常啟動）：

```cmd
# powershell
curl.exe http://127.0.0.1:8000/health
# bash
curl http://127.0.0.1:8000/health
```

```callout tip
環境問題
Port 被佔用、venv 無法啟用或依賴無法安裝時，處理方式請見 [環境準備](#environment)。環境無法啟動時請立即告知主持人；請使用主持人提供的同一份 B0，不要改用其他版本。
```

```form
{"id": "ts-cp3", "title": "檢查點 3 確認","fields":[
{"id": "version", "label": "版本輸出", "type": "text", "hint": "貼上 print(app.title, app.version) 的實際輸出", "suggestions": [{"label": "輸出範本", "text": "〈app.title〉 〈app.version〉"}]},
{"id": "health", "label": "GET /health 回傳 {\"status\":\"ok\"}", "type": "checkbox"},
{"id": "env-issue", "label": "環境問題與耗時", "type": "text", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "問題與耗時", "text": "〈問題〉：〈處理方式〉，耗時約 〈分鐘〉 分鐘"}]}
]}
```

## 檢查點 4 · 測試與基準（第 32–33 分鐘）

- [ ] 在 `smart-ticket-b0` 執行 `pytest -q`，保留**實際輸出**，個人分析時要用。
- [ ] 建立 Git 基準。B0 不是 Git Repository；先記下起始狀態，之後才能用 `git diff` 看到 Agent 實際改了什麼。
- [ ] 讀下方 Brownfield 接手說明。

```cmd
# powershell
& '.\.venv\Scripts\python.exe' -m pytest -q
git init
git add -A
git commit -m "B0 baseline"
# bash
.venv/bin/python -m pytest -q
git init
git add -A
git commit -m "B0 baseline"
```

```callout warning
目前有若干測試失敗
目前有若干測試失敗，需要小組分析是否具有共同原因。**請先不要修改程式**，各自使用自己的 Agent 完成分析；保留測試輸出、規則來源與推論依據。文件是線索，重要結論要用程式、測試與公開規則交叉驗證。
```

```callout tip
常見狀況
- Git 要求設定姓名或 Email：執行 `git config user.name "你的名字"` 與 `git config user.email "you@example.com"`（不加 `--global` 時只寫入本資料夾），再重新 Commit。電腦沒有 Git 時，改用 Agent 或編輯器內建的變更檢視。
- `.venv`、`__pycache__`、`.pytest_cache` 已列在 B0 的 `.gitignore`，不會進入基準。
```

### Brownfield 接手說明

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/03-brownfield-handover.md
```

```form
{"id": "ts-cp4", "title": "檢查點 4 確認","fields":[
{"id": "pytest", "label": "B0 的 pytest -q 結果", "type": "text", "hint": "貼上最後一行摘要，以實際輸出為準。", "suggestions": [{"label": "結果範本", "text": "〈數字〉 failed, 〈數字〉 passed"}, {"label": "未執行", "text": "未執行：〈原因〉"}]},
{"id": "done", "label": "完成檢核", "type": "checklist", "items": ["已切換到同一份 B0，版本為 B0 - Brownfield Baseline", "已保留 pytest -q 的實際輸出", "已建立 Git 基準（或已註明改用其他變更檢視）", "尚未直接修改程式"], "hint": "只勾實際完成的項目。"}
]}
```

下一步（第 33 分鐘）：[B0 系統 Context](#b0-context)，接著 [個人 Agent 分析](#individual-analysis)。
