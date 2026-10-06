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
ZIP 內除了 `starter-repository/`，還有本頁連結的五份 Greenfield 參與者文件（`01-mission-brief.md` 至 `05-submission-checklist.md`），放在 `starter-repository` 的**上一層**（`..\`）。內容與本 Runbook 的參考頁相同，可交給你的 Agent 閱讀。
```

```callout tip
Agent 從哪個資料夾開啟
請在 `starter-repository` 開啟你的 Agent，讓它能直接執行測試。若 Agent 無法讀取上一層資料夾，把 `..\02-business-requirements.md` 與 `..\03-acceptance-criteria.md` 複製到 `starter-repository\docs\` 再交給它。
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

### 建立 Git 基準，之後才看得到 Diff

G0 不是 Git Repository。請在讓 Agent 修改任何檔案**之前**，先記下起始狀態；之後隨時可用 `git diff` 查看 Agent 實際改了什麼，不必只依賴 Agent 的摘要。

- [ ] 在 `starter-repository` 執行下列指令，建立起始 Commit。

```cmd
# powershell
git init
git add -A
git commit -m "G0 baseline"
# bash
git init
git add -A
git commit -m "G0 baseline"
```

若出現要求設定姓名或 Email 的訊息，先執行 `git config user.name "你的名字"` 與 `git config user.email "you@example.com"`（不加 `--global` 時只寫入本資料夾），再重新 Commit。電腦沒有安裝 Git 時，改用你的 Agent 或編輯器內建的變更檢視，並在交付摘要註明。

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

- [ ] 閱讀 [需求](#gf-requirements) 與 [驗收條件](#gf-acceptance)，先記住幾個核對用的數字：成人 700、學生 525、成人＋學生 1225；每筆 1–4 人；T003 已售完。
- [ ] 把下方起始提示交給你的 Agent，要求 5 至 8 步計畫，**先不要修改程式**。
- [ ] 依下方「核准前檢查」核對計畫，回答 Agent 列出的問題，再用「核准回覆」格式回覆。

起始提示（已填入本案例的文件位置）：

```text
先不要修改程式。請閱讀 `../02-business-requirements.md` 與 `../03-acceptance-criteria.md`，以及本 Repository 的 README.md 與 docs/architecture.md，搜尋 `TODO(GREENFIELD`，整理待完成工作、規則對應與風險，提出 5 至 8 步計畫。每一步標出對應的 Rule ID。列出需要我決定的問題，等待我確認。
```

Agent 的計畫合格時，應該：找到 11 個 `TODO(GREENFIELD`、每一步標出 Rule ID、列出需要你決定的問題。若它沒讀到需求文件、跳過 Rule ID 或已經開始修改，請要求它重做計畫。

### 核准前檢查

- [ ] 每一步都對應到 Rule ID 或 AC；沒有前端、登入、會員、優惠、改退票、新套件等範圍外項目。
- [ ] 實作順序由你決定。建議先做能獨立測試的部分，例如票價 → 班次查詢 → 建立訂票 → 付款 → 查詢訂單。
- [ ] 商業規則放在 `domain/` 或 `application/`，`api/routes.py` 只負責轉換請求與回應。
- [ ] Agent 列出的每個問題都有你的決定。答案先查下方「需求澄清」與需求文件；查不到時舉手問主持人，不要讓 Agent 自行假設。

```callout info
需求澄清（全場一致）
下列項目需求文件沒有逐字寫明，以此為準：
- **付款失敗**：Booking 維持 `PENDING_PAYMENT`，已保留的座位不釋放，不建立 Order；之後仍可再次付款。
- **錯誤回應**：找不到 Trip／Booking／Order 回 404；人數、座位不足、重複付款、付款失敗等規則衝突回 4xx，代碼由你決定並寫進 `docs/api-examples.md`；Request 格式錯誤可保留 FastAPI 的 422。錯誤內容沿用既有的 `{"error":{"code":"...","message":"..."}}`。
- **付款失敗怎麼測**：在測試中把 `MockPaymentGateway.next_result` 設為 `PaymentStatus.FAILED`，不使用隨機結果。
```

### 核准回覆

用以下格式回覆 Agent。`〈 〉` 的內容由你填寫：

```text
計畫核准，順序如下：
〈依你決定的順序列出步驟〉

我的決定：
- 〈Agent 問題 1〉：〈你的決定與依據〉
- 〈Agent 問題 2〉：〈你的決定與依據〉

限制：商業規則放在 domain／application，Router 只做轉換；不新增依賴、不改 Seed、不動 /health；功能完成才移除對應的 skip，不得修改或刪除既有斷言。

先做第 1 到 〈N〉 步，做完執行 pytest -q 給我看實際輸出，然後停下等我。
```

## 步驟 5：Execute（約 12 分鐘）

一次只讓 Agent 做一段，每段都**測試、看 Diff、再繼續**，不要讓它一口氣完成全部 TODO。

- [ ] Agent 完成一段後，確認它回報的是**實際執行**的 `pytest -q` 輸出，且減少的 Skip 正好是這一段的功能。
- [ ] 執行 `git diff --stat` 看改了哪些檔案，再用 `git diff` 看主要檔案（說明見步驟 7 的「如何審查 Diff」）。確認改動沒有超出這一段。
- [ ] 沒問題再交代下一段，例如：

```text
這一段看過了。接著做第 〈N+1〉 到 〈M〉 步，做完執行 pytest -q，列出還剩哪些 skip，然後停下等我。
```

- [ ] 你可以每段結束時 `git add -A` 加 `git commit -m "說明"`，之後 `git diff` 只會顯示新一段的變更。
- [ ] 遇到疑問先請 Agent 說明它的假設，由你確認；不要讓它改需求或新增範圍外功能。

## 步驟 6：Test（約 4 分鐘）

- [ ] 要求 Agent 補足邊界測試並執行 `pytest -q`，記錄指令和實際結果。至少包含：0 人與 5 人被拒、4 人可建立、座位不足被拒且座位不變、成人＋學生 1225、不存在的 Booking／Order 回 404、付款失敗不建立 Order 也不變成 `PAID`、重複付款被拒。
- [ ] 辨識仍被 Skip 的測試，列入未完成項目。
- [ ] 執行 `git diff -- tests`，確認只有「移除 skip」與「新增測試」，沒有刪除或放寬既有斷言。
- [ ] 自己走一次完整流程：查班次 → 建立訂票 → 付款 → 查詢 Order，並確認 `/health` 正常。

最簡單的手動驗證方式是用瀏覽器開啟 App 內建的 API 測試頁 `http://127.0.0.1:8000/docs`（App 需先啟動）：

1. `GET /trips`：按「Try it out」→「Execute」，確認沒有 T003。
2. `POST /bookings`：貼上下方內容，確認 `total_fare` 為 1225、狀態為 `PENDING_PAYMENT`，記下 `booking_id`。
3. `POST /bookings/{booking_id}/pay`：填入 `booking_id`，確認回傳 Order，記下 `order_id`。
4. `GET /orders/{order_id}`：確認 `amount` 為 1225、`payment_status` 為 `SUCCESS`、`booking_id` 正確。
5. 再付款一次同一個 `booking_id`，確認被拒絕。

```text
{
  "trip_id": "T001",
  "passengers": [
    {"passenger_id": "P1", "name": "測試旅客一", "passenger_type": "ADULT"},
    {"passenger_id": "P2", "name": "測試旅客二", "passenger_type": "STUDENT"}
  ]
}
```

回應欄位名稱以你實作的 Schema 為準。把實際呼叫結果整理進 `docs/api-examples.md`。App 重啟後資料會重置，這是設計行為。

## 步驟 7：Explain 與提交（約 2 分鐘）

- [ ] 要求 Agent 整理交付摘要：

```text
請整理交付摘要：修改檔案、Rule ID 與 AC 對應、最後一次 pytest -q 的指令與完整輸出、文件更新、未完成項目與風險。沒有實際執行過的項目標為「未驗證」。
```

- [ ] 由你審查主要 Diff，確認與核准計畫一致；不要只看摘要或通過數量。
- [ ] 依 [Submission Checklist](#gf-submission) 核對，逐欄確認後才填寫交付摘要。「人和 Agent 各做什麼」請自己寫。

### 如何審查 Diff

1. `git diff --stat`：列出改了哪些檔案、各改多少行。看有沒有計畫外的檔案。
2. `git diff -- src`：看程式變更。挑一個主要變更，用自己的話說出它做什麼、對應哪個 Rule ID 與 AC、由哪個測試驗證。
3. `git diff -- tests`：確認沒有刪除或放寬斷言。

若你在步驟 5 每段都有 Commit，用 `git diff HEAD~〈段數〉` 或 `git log -p` 查看全部變更。`git diff` 畫面按 `q` 離開。

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
