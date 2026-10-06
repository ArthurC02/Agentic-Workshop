---
id: greenfield
title: Greenfield 任務：核心訂票 MVP
minute: 07-29
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 任務：核心訂票 MVP

Smart Ticket 是剛開始開發的車票預訂服務。請在 **22 分鐘**內完成查詢班次、建立訂票、模擬付款與查詢付款後訂單，驗證完整流程。這是**個人**任務。

本段的 MVP（Minimum Viable Product）指能跑通上述核心流程的最小可行產品；AC（Acceptance Criteria）是逐項判定功能是否符合要求的驗收條件；Rule ID 是商業規則編號。

本階段 Agent 是 **Tool**：由你理解需求、決定方向、拆解工作及審查結果，Agent 協助產生程式、測試與文件。先閱讀需求並核准計畫，再讓 Agent 修改。

| 本段文件 | 用途 |
|---|---|
| [Mission Brief](#gf-mission) | 任務、時間分配、交付與完成條件 |
| [Business Requirements](#gf-requirements) | 四個 API、16 條商業規則、固定 Seed Data |
| [Acceptance Criteria](#gf-acceptance) | 15 項驗收條件 |
| [Agent Usage Guide](#gf-agent-guide) | Plan／Execute／Test／Explain 與通用起始提示 |
| [Submission Checklist](#gf-submission) | 提交清單與交付摘要表單 |
| [Starter Repository 文件](#gf-starter-docs) | README、架構、規則與 API 範例待填表 |

## 步驟 1：下載並解壓縮 G0 Starter Repository

```download
id=g0 zip=participant-07-g0.zip label=下載 G0 Starter Repository
```

- [ ] 下載 `g0.zip`。
- [ ] 解壓縮到短路徑，例如 `C:\work\g0`（依實際下載位置調整指令中的路徑）。
- [ ] 進入 `starter-repository` 資料夾。

```cmd
# powershell
Expand-Archive -Path "$HOME\Downloads\g0.zip" -DestinationPath C:\work\g0
cd C:\work\g0\agentic-workshop\01-greenfield\participant\starter-repository
# bash
unzip ~/Downloads/g0.zip -d ~/work/g0
cd ~/work/g0/agentic-workshop/01-greenfield/participant/starter-repository
```

```callout info
ZIP 內容
ZIP 內除了 `starter-repository/`，還有本頁連結的五份 Greenfield 參與者文件（`01-mission-brief.md` 至 `05-submission-checklist.md`）。內容與本 Runbook 的參考頁相同，可交給你的 Agent 閱讀。
```

## 步驟 2：建立環境並執行起始測試

- [ ] 建立 venv、安裝依賴並執行 `pytest -q`。
- [ ] 確認起始結果為 `1 passed, 8 skipped`（實際結果以執行輸出為準）。
- [ ] 啟動 App，確認 `GET /health` 回傳 `{"status":"ok"}`。

```cmd
# powershell
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

```callout info
起始狀態不是完成狀態
G0 提供框架、固定資料與 Health；四個業務 API 回應 501，核心 Use Case 尚未實作。功能測試的 Skip 原因對應 Rule ID；初始 Skip 不代表完成 MVP。
```

Health 檢查與疑難排解請見 [環境準備](#environment)。

## 步驟 3：找出 `TODO(GREENFIELD`

- [ ] 搜尋 `TODO(GREENFIELD`，找出 11 個主要實作點。

```cmd
# powershell
Get-ChildItem -Path src -Recurse -Filter *.py | Select-String -SimpleMatch 'TODO(GREENFIELD'
# bash
grep -rn "TODO(GREENFIELD" src
```

也可以在編輯器中全域搜尋，或讓 Agent 在起始提示中自行搜尋。

## 步驟 4：Plan（約 4 分鐘）

- [ ] 閱讀 [需求](#gf-requirements) 與 [驗收條件](#gf-acceptance)。
- [ ] 把下方通用起始提示交給你的 Agent，要求 5 至 8 步計畫，**先不要修改程式**。
- [ ] 核對計畫的範圍、規則與風險，回答 Agent 列出的問題，確認後才核准執行。

通用起始提示：

```text
先不要修改程式。請閱讀我提供的需求與驗收條件，掃描 Starter Repository，搜尋 `TODO(GREENFIELD`，整理待完成工作、規則對應與風險，提出 5 至 8 步計畫。列出需要我決定的問題，等待我確認。
```

## 步驟 5：Execute（約 12 分鐘）

- [ ] 依你核准的計畫讓 Agent 完成 TODO，先完成一段能測試的核心流程。
- [ ] 由你決定設計方向與優先順序；遇到疑問先請 Agent 說明假設，由你確認。
- [ ] 限制修改於 MVP，不任意增加外部依賴或改需求；保留現有分層，不把商業規則集中到 API Router。

## 步驟 6：Test（約 4 分鐘）

- [ ] 要求 Agent 執行 `pytest -q`，記錄指令和實際結果。
- [ ] 核對驗收條件，補足失敗與邊界案例；完成功能後移除對應 Skip。
- [ ] 辨識仍被 Skip 的測試；不刪除或弱化斷言掩蓋失敗。
- [ ] 核對完整 API 流程（查詢→訂票→模擬付款→查詢 Order）與 `/health`。

## 步驟 7：Explain 與提交（約 2 分鐘）

- [ ] 要求 Agent 列出修改檔案、商業規則與驗收條件的對應、測試結果、文件更新、風險與未完成項目。
- [ ] 由你審查主要 Diff，確認與核准計畫一致；不要只看摘要或通過數量。
- [ ] 依 [Submission Checklist](#gf-submission) 核對並填寫交付摘要。

## 時間提示

| 分鐘 | 主持人口令 |
|---:|---|
| 07 | 請確認任務、需求、驗收條件及程式庫（Repository）可開啟。 |
| 09 | 請 Agent 先讀需求、掃 TODO、提出計畫，先不要修改。 |
| 11 | 確認計畫後，先完成一段能測試的核心流程。 |
| 19 | 還有 10 分鐘。請查看主要 Diff，確認對應規則及目前測試。 |
| 24 | 請優先測試既有變更、補文件與記錄未完成項。 |
| 27 | 列完成／未完成、測試結果、限制，以及人和 Agent 各做什麼。 |
| 29 | 停止修改，保存並提交現況；不再延長實作。 |

```callout warning
22 分鐘到即停止擴充
未完成時如實說明：記錄當前完成度與未完成項目後提交，不把部分完成描述為完整交付。遇到環境問題請告知主持人，並記錄耗時。
```
