---
id: greenfield
title: Greenfield 任務：核心訂票 MVP
minute: 07-29
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 任務：核心訂票 MVP

Smart Ticket 是剛開始開發的車票預訂服務。請在 **22 分鐘**內完成查詢班次、建立訂票、模擬付款與查詢付款後訂單，驗證完整流程。這是**個人**任務。

本階段 Agent 是 **Tool**：由你理解需求、決定方向、拆解工作及審查結果，Agent 協助產生程式、測試與文件。本段要練習的是**你如何掌控 Agent**，不是 Agent 多快寫完。

```callout warning
不要讓 Agent 一次做完全部
本段分成 6 個檢查點。每個檢查點結束時，Agent 必須停下來；你親自確認並填好該檢查點的「確認」表單，才交代下一段。如果 Agent 一口氣做完所有 TODO，你就跳過了本段要體驗的事情：計畫、審查與驗收都由人決定。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要貼給 Agent 的提示詞、要填的表單，全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 準備 | 07–09 | 00–02 | 下載、建環境、起始測試、建立 Git 基準 |
| 2 · 計畫 | 09–11 | 02–04 | Agent 只提計畫；你調整並核准 |
| 3 · 第一段實作 | 11–19 | 04–12 | Agent 做第一段後停下；你看測試、看 Diff、手算 1225 |
| 4 · 第二段實作 | 19–24 | 12–17 | Agent 做第二段後停下；你再看測試與 Diff |
| 5 · 驗證 | 24–27 | 17–20 | 不再加功能；補邊界測試，自己走一次完整流程 |
| 6 · 交付 | 27–29 | 20–22 | 填交付摘要；第 29 分鐘停止 |

需要時再查：[任務說明](#gf-mission)、[商業需求](#gf-requirements)、[驗收條件](#gf-acceptance)、[Starter Repository 文件](#gf-starter-docs)。

## 檢查點 1 · 準備（第 07–09 分鐘）

```download
id=g0 zip=participant-07-g0.zip label=下載 G0 Starter Repository
```

- [ ] 下載 `g0.zip`，解壓縮到短路徑，例如 `C:\work\g0`，進入 `starter-repository` 資料夾。

```cmd
# powershell
Expand-Archive -Path "$HOME\Downloads\g0.zip" -DestinationPath C:\work\g0
cd C:\work\g0\agentic-workshop\01-greenfield\participant\starter-repository
# bash
unzip ~/Downloads/g0.zip -d ~/work/g0
cd ~/work/g0/agentic-workshop/01-greenfield/participant/starter-repository
```

- [ ] 建立 venv、安裝依賴並執行 `pytest -q`，確認起始結果為 `1 passed, 8 skipped`（以實際輸出為準）。

```cmd
# powershell
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
# bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

- [ ] 建立 Git 基準。G0 不是 Git Repository；先記下起始狀態，之後才能用 `git diff` 看到 Agent 實際改了什麼。

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

- [ ] 在 `starter-repository` 開啟你的 Agent。

```callout tip
常見狀況
- Git 要求設定姓名或 Email：執行 `git config user.name "你的名字"` 與 `git config user.email "you@example.com"`（不加 `--global` 時只寫入本資料夾），再重新 Commit。電腦沒有 Git 時，改用 Agent 或編輯器內建的變更檢視，並在交付摘要註明。
- 需求文件在 `starter-repository` 的**上一層**（`..\02-business-requirements.md`、`..\03-acceptance-criteria.md`）。Agent 讀不到上一層時，把這兩份複製到 `starter-repository\docs\`。
- G0 的四個業務 API 回應 501，初始 Skip 代表功能尚未實作，不是完成。
- App 啟動、Health 檢查與其他疑難排解見 [環境準備](#environment)。
```

```form
{"id": "gf-cp1", "title": "檢查點 1 確認","fields":[
{"id": "pytest", "label": "起始 pytest -q 結果", "type": "text", "hint": "例如：1 passed, 8 skipped", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "安裝失敗", "text": "未執行：〈錯誤訊息〉"}]},
{"id": "git", "label": "已建立 Git 基準（或已註明改用其他變更檢視）", "type": "checkbox"}
]}
```

## 檢查點 2 · 計畫（第 09–11 分鐘）

這一步 Agent **只提計畫，不改任何檔案**。

- [ ] 把下方提示詞貼給 Agent。

```text
先不要修改程式。請閱讀 `../02-business-requirements.md` 與 `../03-acceptance-criteria.md`，以及本 Repository 的 README.md 與 docs/architecture.md，搜尋 `TODO(GREENFIELD`，整理待完成工作、規則對應與風險，提出 5 至 8 步計畫。每一步標出對應的 Rule ID。列出需要我決定的問題，等待我確認。
```

Agent 的計畫合格時，應該：找到 11 個 `TODO(GREENFIELD`、每一步標出 Rule ID、列出需要你決定的問題。若它沒讀到需求文件、跳過 Rule ID 或已經開始修改，請要求它重做計畫。

- [ ] 核對計畫：每一步都對應到 Rule ID 或 AC；沒有前端、登入、會員、優惠、改退票、新套件等範圍外項目。
- [ ] 決定實作順序，並決定**第一段做到哪裡**。建議第一段做到能驗證 1225 為止：票價 → 班次查詢 → 建立訂票；第二段再做付款 → 查詢訂單。
- [ ] 確認規則的位置：商業規則放在 `domain/` 或 `application/`，`api/routes.py` 只負責轉換請求與回應。
- [ ] 回答 Agent 列出的每個問題。先查下方「需求澄清」與需求文件；查不到時舉手問主持人，不要讓 Agent 自行假設。

```callout info
需求澄清（全場一致）
下列項目需求文件沒有逐字寫明，以此為準：
- **付款失敗**：Booking 維持 `PENDING_PAYMENT`，已保留的座位不釋放，不建立 Order；之後仍可再次付款。
- **錯誤回應**：找不到 Trip／Booking／Order 回 404；人數、座位不足、重複付款、付款失敗等規則衝突回 4xx，代碼由你決定並寫進 `docs/api-examples.md`；Request 格式錯誤可保留 FastAPI 的 422。錯誤內容沿用既有的 `{"error":{"code":"...","message":"..."}}`。
- **付款失敗怎麼測**：在測試中把 `MockPaymentGateway.next_result` 設為 `PaymentStatus.FAILED`，不使用隨機結果。
```

- [ ] 用下方格式回覆 Agent。`〈 〉` 的內容由你填寫：

```text
計畫核准，順序如下：
〈依你決定的順序列出步驟〉

我的決定：
- 〈Agent 問題 1〉：〈你的決定與依據〉
- 〈Agent 問題 2〉：〈你的決定與依據〉

限制：商業規則放在 domain／application，Router 只做轉換；不新增依賴、不改 Seed、不動 /health；功能完成才移除對應的 skip，不得修改或刪除既有斷言。

這一次只做第 1 到 〈N〉 步。做完執行 pytest -q，貼出實際輸出，然後停下等我確認，不要繼續下一步。
```

```form
{"id": "gf-cp2", "title": "檢查點 2 確認","fields":[
{"id": "changes", "label": "我對 Agent 計畫做了哪些調整", "type": "textarea", "hint": "例如：調整順序、刪掉範圍外項目、要求補 Rule ID。完全沒改時，寫出你為什麼同意。", "suggestions": [{"label": "調整順序", "text": "把〈步驟〉移到〈步驟〉之後，理由：〈…〉"}, {"label": "刪範圍外", "text": "刪掉〈項目〉，理由：不在需求範圍內"}, {"label": "要求補 Rule", "text": "要求 Agent 補上〈步驟〉對應的 Rule ID"}, {"label": "同意原計畫", "text": "沒有調整，同意的理由：〈…〉"}]},
{"id": "decisions", "label": "我對 Agent 問題的決定與依據", "type": "textarea", "hint": "至少一項。依據寫需求、AC 或需求澄清的哪一條。", "suggestions": [{"label": "決定與依據", "text": "〈Agent 問題〉：〈我的決定〉（依據：〈Rule ID／AC／需求澄清〉）"}, {"label": "問主持人", "text": "〈問題〉：需求文件查不到，已問主持人，答覆：〈…〉"}]},
{"id": "slice1", "label": "第一段讓 Agent 做到第幾步", "type": "text", "suggestions": [{"label": "做到第 N 步", "text": "第 1 到 〈N〉 步（〈最後一步的內容〉）"}]}
]}
```

## 檢查點 3 · 第一段實作（第 11–19 分鐘）

Agent 依核准計畫做第一段，做完停下。**它停下後，換你做下面的確認**，確認前不要讓它繼續。

- [ ] 確認 Agent 貼的是**實際執行**的 `pytest -q` 輸出，且減少的 Skip 正好是這一段的功能。
- [ ] 看 Diff（步驟見下方「如何看 Diff」）：改動有沒有超出這一段？規則是否放在 `domain/` 或 `application/`？
- [ ] 挑一個主要變更，用自己的話說出它做什麼、對應哪個 Rule ID 與 AC。
- [ ] 手算一次：T001 成人 700 ＋ 學生 525 ＝ **1225**，跟程式或測試結果對照。
- [ ] 有問題就要求 Agent 修正並重跑測試；沒問題就 Commit 這一段：`git add -A`、`git commit -m "第一段"`。

```callout info
如何看 Diff
1. `git diff --stat`：列出改了哪些檔案、各改多少行。看有沒有計畫外的檔案。
2. `git diff -- src`：看程式變更。
3. `git diff -- tests`：確認只有「移除 skip」與「新增測試」，沒有刪除或放寬既有斷言。

`git diff` 畫面按 `q` 離開。每段結束都 Commit 時，`git diff` 只會顯示新一段的變更；`git log -p` 可查看全部變更。
```

```form
{"id": "gf-cp3", "title": "檢查點 3 確認","fields":[
{"id": "pytest", "label": "第一段的 pytest -q 結果", "type": "text", "hint": "例如：5 passed, 4 skipped", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}]},
{"id": "diff", "label": "我看過的一處主要變更", "type": "textarea", "hint": "檔案／函式、它做什麼、對應的 Rule ID 與 AC。", "suggestions": [{"label": "變更說明", "text": "〈檔案〉的〈函式〉：〈它做什麼〉；對應 Rule 〈Rule ID〉、AC 〈AC ID〉"}]},
{"id": "fare", "label": "1225 核對結果", "type": "text", "hint": "手算 1225，程式結果是多少？", "suggestions": [{"label": "一致", "text": "一致：手算 1225，程式結果 〈金額〉"}, {"label": "不一致", "text": "不一致：手算 1225，程式結果 〈金額〉，已要求修正"}, {"label": "未驗證", "text": "未驗證：〈原因〉"}]},
{"id": "fixes", "label": "我要求 Agent 修正的地方", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "修正項目", "text": "〈問題〉：要求 Agent〈修正方式〉，重跑結果〈…〉"}, {"label": "超出範圍", "text": "Agent 改了計畫外的〈檔案〉，要求還原"}]}
]}
```

## 檢查點 4 · 第二段實作（第 19–24 分鐘）

- [ ] 交代第二段：

```text
第一段我看過了。接著做第 〈N+1〉 到 〈M〉 步。付款失敗依我先前的決定處理。做完執行 pytest -q，貼出實際輸出，列出還剩哪些 skip，然後停下等我。
```

- [ ] Agent 停下後，同樣確認：實際的測試輸出、`git diff --stat`、`git diff -- src`、`git diff -- tests`。
- [ ] 特別核對付款：只有 `PENDING_PAYMENT` 能付款、成功後 `PAID` 並建立唯一 Order、重複付款被拒、付款失敗不建立 Order。
- [ ] 沒問題就 Commit：`git add -A`、`git commit -m "第二段"`。

```callout tip
時間不夠時
第 24 分鐘還沒做到付款，就停在已完成的部分，直接進入檢查點 5 驗證已做的功能。未完成的列入交付摘要，不要硬趕。
```

```form
{"id": "gf-cp4", "title": "檢查點 4 確認","fields":[
{"id": "pytest", "label": "第二段的 pytest -q 結果", "type": "text", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}, {"label": "未做到付款", "text": "時間不夠，停在〈步驟〉：〈pytest 結果〉"}]},
{"id": "diff", "label": "我看過的一處付款或訂單變更", "type": "textarea", "hint": "檔案／函式、對應的 Rule ID 與 AC。", "suggestions": [{"label": "變更說明", "text": "〈檔案〉的〈函式〉：〈它做什麼〉；對應 Rule 〈Rule ID〉、AC 〈AC ID〉"}]},
{"id": "tests-intact", "label": "git diff -- tests 沒有刪除或放寬既有斷言", "type": "checkbox"}
]}
```

## 檢查點 5 · 驗證（第 24–27 分鐘）

**不再加新功能。**

- [ ] 要求 Agent 補邊界測試並執行：

```text
不要再加新功能。請補這些邊界測試並執行 pytest -q，貼出實際輸出：
- 成人＋學生 1225
- 0 人、5 人被拒；4 人可建立
- 座位不足被拒且座位不變
- 不存在的 Booking／Order 回 404
- 付款失敗不建立 Order、不變成 PAID
- 重複付款被拒
然後依實際結果更新 README、docs/business-rules.md、docs/api-examples.md。
```

- [ ] 自己走一次完整流程。啟動 App，用瀏覽器開啟 App 內建的 API 測試頁 `http://127.0.0.1:8000/docs`：

```cmd
# powershell
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
# bash
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

1. `GET /trips`：按「Try it out」→「Execute」，確認沒有 T003。
2. `POST /bookings`：貼上下方內容，確認 `total_fare` 為 1225、`status` 為 `PENDING_PAYMENT`，記下 `booking_id`。
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

App 重啟後資料會重置，這是設計行為。

```form
{"id": "gf-cp5", "title": "檢查點 5 確認","fields":[
{"id": "pytest", "label": "最後一次 pytest -q 結果", "type": "text", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}]},
{"id": "flow", "label": "我自己走過的完整流程", "type": "checklist", "items": ["查班次沒有 T003", "訂票金額 1225、PENDING_PAYMENT", "付款成功並取得 Order", "查 Order 金額 1225", "重複付款被拒"], "hint": "只勾實際走過且結果正確的項目。"},
{"id": "skipped", "label": "仍被 Skip 或未完成的項目", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "Skip 測試", "text": "〈測試名稱〉仍被 Skip：〈原因〉"}, {"label": "未完成功能", "text": "〈功能〉未完成：〈完成到哪裡〉"}]}
]}
```

## 檢查點 6 · 交付（第 27–29 分鐘）

- [ ] 要求 Agent 整理交付摘要：

```text
請整理交付摘要：修改檔案、Rule ID 與 AC 對應、最後一次 pytest -q 的指令與完整輸出、文件更新、未完成項目與風險。沒有實際執行過的項目標為「未驗證」。
```

- [ ] 對照你在檢查點 1–5 的確認紀錄，核對 Agent 的摘要；不一致時以你的實際確認為準。
- [ ] 到 [提交清單與交付摘要](#gf-submission) 填寫交付摘要並匯出。「人和 Agent 各做什麼」請自己寫，可直接引用檢查點 2–5 的紀錄。

```callout warning
第 29 分鐘停止修改
未完成時如實說明：記錄當前完成度與未完成項目後提交，不把部分完成描述為完整交付。遇到環境問題請告知主持人，並記錄耗時。
```
