---
id: greenfield
title: Greenfield 任務：核心訂票 MVP
minute: 07-29
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 任務：核心訂票 MVP

Smart Ticket 是剛開始開發的車票預訂服務，屬於 Greenfield（從頭開始的新專案）。請在 **22 分鐘**內完成 MVP（Minimum Viable Product，最小可行產品）：查詢班次、建立訂票、模擬付款與查詢付款後訂單，驗證完整流程。這是**個人**任務。

本階段 Agent 是 **Tool（工具）**：由你理解需求、逐步下指令，每一步用證據驗收；程式、測試與指令操作全部交給 Agent，你不寫也不讀程式。本段要練習的是**你如何掌控 Agent**，不是 Agent 多快寫完。

```callout warning
不要讓 Agent 一次做完全部
本段分成 6 個檢查點。每個檢查點結束時，Agent 必須停下來；你親自確認並填好該檢查點的「確認」表單，才交代下一段。如果 Agent 一口氣做完所有 TODO，你就跳過了本段要體驗的事情：計畫、審查與驗收都由人決定。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要貼給 Agent 的提示詞、要填的表單，全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 先貼給 Agent：工作規則

開啟 Agent 後，第一件事是把下面整段貼給它；之後如果開了新的 Agent 對話，也要重新貼一次。這段是給 Agent 的，不需要看懂。

```text
以下是這次工作的規則，請在整段對話中遵守：
1. 你負責所有程式、測試與指令操作；我不會自己修改程式，也不會自己讀程式，請用白話向我說明。
2. 每次修改前先提出計畫，等我核准；只做核准的步驟，做完就停下來等我。
3. 商業規則放在 domain／application，Router 只做輸入輸出轉換；不新增套件、不改 Seed 資料、不動 /health。
4. 功能完成才移除對應的 skip；不得修改或刪除既有測試的斷言，不得用 skip／xfail 隱藏失敗。
5. 每次做完都執行 pytest -q，並用「驗收對照表」回報：每條驗收條件或規則一列，寫通過／失敗／未驗證，以及依據的測試名稱。不要只貼原始輸出。
6. 每次修改後用白話說明：改了哪些檔案、各改了什麼、為什麼，以及有沒有超出我核准的範圍。
7. 你沒有實際執行的事情，一律標「未驗證」。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 準備 | 07–09 | 00–02 | 下載、貼工作規則；請 Agent 建環境、跑起始測試、建立 Git 基準 |
| 2 · 計畫 | 09–11 | 02–04 | Agent 只提計畫；你調整並核准 |
| 3 · 第一段實作 | 11–19 | 04–12 | Agent 做第一段後停下；你看驗收對照表、做變更審查、手算票價 1225 |
| 4 · 第二段實作 | 19–24 | 12–17 | Agent 做第二段後停下；你再看驗收對照表、做變更審查 |
| 5 · 驗證 | 24–27 | 17–20 | 不再加功能；請 Agent 補邊界測試，你在 /docs 走一次完整流程 |
| 6 · 交付 | 27–29 | 20–22 | 填交付摘要；第 29 分鐘停止 |

需要時再查：[任務說明](#gf-mission)、[商業需求](#gf-requirements)、[驗收條件](#gf-acceptance)、[Starter Repository 文件](#gf-starter-docs)。

## 檢查點 1 · 準備（第 07–09 分鐘）

```download
id=g0 zip=participant-07-g0.zip label=下載 G0 Starter Repository
```

- [ ] 下載 `g0.zip`，解壓縮到短路徑，例如 `C:\work\g0`（Windows：在檔案上按右鍵選「全部解壓縮」；macOS：點兩下解壓縮）。
- [ ] 在解壓後的 `agentic-workshop\01-greenfield\participant\starter-repository` 資料夾開啟你的 Agent。
- [ ] 貼上上方的「工作規則」。
- [ ] 請 Agent 準備環境並執行起始測試。確認它回報的起始結果為 `1 passed, 8 skipped`（1 個通過、8 個跳過；以實際輸出為準）。

```text
請幫我準備這個專案的執行環境：確認 Python 版本是 3.13，在專案資料夾建立 .venv 虛擬環境並安裝 requirements.txt，接著執行 pytest -q。用白話告訴我：環境是否建好、測試有幾個通過／失敗／跳過，以及下一步要做什麼。遇到錯誤時先說明原因，不要自行修改程式。
```

- [ ] 請 Agent 建立 Git 基準。G0（Greenfield 起始程式包）不是 Git Repository；先記下起始狀態，之後 Agent 才能回報它實際改了什麼。

```text
請在這個資料夾建立 Git 基準：初始化 Git，把目前所有檔案 Commit 成「G0 baseline」。如果 Git 要求姓名或 Email，只在本資料夾設定（不要用 --global），名字用「workshop」、Email 用「you@example.com」。完成後用白話告訴我結果。
```

```callout tip
常見狀況
- 電腦沒有 Git：請 Agent 改用它內建的變更檢視，並在交付摘要註明。
- 需求文件在 `starter-repository` 的**上一層**（`02-business-requirements.md`、`03-acceptance-criteria.md`）。Agent 讀不到上一層時，請它把這兩份複製到 `starter-repository\docs\`。
- G0 的四個業務 API 一開始都還不能用（回應 501），被略過（Skip）的測試代表功能尚未實作，不是完成。
- 環境安裝、App 啟動與其他疑難排解見 [環境準備](#environment)。
```

```form
{"id": "gf-cp1", "title": "檢查點 1 確認","fields":[
{"id": "pytest", "label": "Agent 回報的起始測試結果", "type": "text", "hint": "例如：1 passed, 8 skipped", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "安裝失敗", "text": "未執行：〈錯誤訊息〉"}]},
{"id": "git", "label": "Agent 已建立 Git 基準（或已註明改用其他變更檢視）", "type": "checkbox"}
]}
```

## 檢查點 2 · 計畫（第 09–11 分鐘）

這一步 Agent **只提計畫，不改任何檔案**。

- [ ] 把下方提示詞貼給 Agent。

```text
先不要修改。請閱讀上一層資料夾的商業需求（02-business-requirements.md）與驗收條件（03-acceptance-criteria.md），以及這個專案的說明文件，找出所有標示 `TODO(GREENFIELD` 的待完成工作，提出 5 至 8 步計畫。每一步用白話說明完成後使用者能做什麼，並標出對應的規則編號（Rule ID）與驗收條件（AC）。列出需要我決定的問題，等待我確認。
```

Agent 的計畫合格時，應該：回報找到 11 個 `TODO(GREENFIELD` 待完成工作、每一步標出規則編號（Rule ID）、列出需要你決定的問題。若它沒讀到需求文件、跳過 Rule ID 或已經開始修改，請要求它重做計畫。

- [ ] 核對計畫：每一步都對應到 Rule ID 或 AC（Acceptance Criteria，驗收條件）；沒有前端、登入、會員、優惠、改退票、新套件等範圍外項目。
- [ ] 決定實作順序，並決定**第一段做到哪裡**。建議第一段做到能驗證 1225 為止：票價 → 班次查詢 → 建立訂票；第二段再做付款 → 查詢訂單。
- [ ] 確認計畫沒有違反工作規則（例如新增套件、改 Seed 資料、動到 /health）。看不出來時，請 Agent 對照工作規則逐條說明。
- [ ] 回答 Agent 列出的每個問題。先查下方「需求澄清」與需求文件；查不到時舉手問主持人，不要讓 Agent 自行假設。

```callout info
需求澄清（全場一致）
下列項目需求文件沒有逐字寫明，以此為準：
- **付款失敗**：Booking 維持 `PENDING_PAYMENT`，已保留的座位不釋放，不建立 Order；之後仍可再次付款。
- **錯誤回應**：找不到 Trip／Booking／Order 回 404；人數、座位不足、重複付款、付款失敗等規則衝突回 4xx，代碼由你決定，請 Agent 寫進 `docs/api-examples.md`；輸入格式錯誤可沿用系統預設的 422。錯誤內容沿用既有格式 `{"error":{"code":"...","message":"..."}}`。
- **付款失敗怎麼測**：測試中要能指定付款失敗，不使用隨機結果（給 Agent 的提示：把 `MockPaymentGateway.next_result` 設為 `PaymentStatus.FAILED`）。
```

- [ ] 用下方格式回覆 Agent。`〈 〉` 的內容由你填寫：

```text
計畫核准，順序如下：
〈依你決定的順序列出步驟〉

我的決定：
- 〈Agent 問題 1〉：〈你的決定與依據〉
- 〈Agent 問題 2〉：〈你的決定與依據〉

這一次只做第 1 到 〈N〉 步。做完依工作規則回報驗收對照表，然後停下等我確認，不要繼續下一步。
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

- [ ] Agent 停下後，貼上「變更審查」提示詞，請它用白話回答：

```text
不要再修改。請用白話回答下列審查問題，每題附上你實際執行的指令與輸出：
1. 這次改了哪些檔案？每個檔案改了什麼、為什麼？有沒有不在核准計畫裡的檔案？
2. 測試總數和上一次比有沒有變少？有沒有新增 skip 或 xfail？
3. 有沒有刪除測試，或修改既有測試的期待值？（請用 git diff 檢查 tests 資料夾後回答）
4. 列出驗收對照表。
```

- [ ] 看驗收對照表：減少的跳過（Skip）正好是這一段的功能，結果是 Agent **實際執行**得到的。
- [ ] 從 Agent 的白話說明中挑一處主要變更，用自己的話說出它讓系統能做什麼、對應哪個 Rule ID 與 AC。說不出來就請 Agent 再解釋。
- [ ] 手算一次：班次 T001 成人 700 ＋ 學生 525 ＝ **1225**，跟驗收對照表中 AC-G-005 的結果對照。
- [ ] 填下方表單的審查卡。任何一題是「否」或「不確定」→ 不核准，請 Agent 解釋或修正並重跑測試。
- [ ] 沒問題就請 Agent 記錄這一段：

```text
這一段我核准了。請把目前的變更 Commit 成「第一段」，完成後告訴我結果，然後停下等我。
```

```form
{"id": "gf-cp3", "title": "檢查點 3 確認","fields":[
{"id": "pytest", "label": "第一段的測試結果（驗收對照表最後一行）", "type": "text", "hint": "例如：5 passed, 4 skipped", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}]},
{"id": "diff", "label": "我看懂的一處主要變更", "type": "textarea", "hint": "依 Agent 的白話說明：哪個檔案、它讓系統能做什麼、對應的 Rule ID 與 AC。", "suggestions": [{"label": "變更說明", "text": "〈檔案〉：〈它讓系統能做什麼〉；對應 Rule 〈Rule ID〉、AC 〈AC ID〉"}]},
{"id": "fare", "label": "1225 核對結果", "type": "text", "hint": "手算 1225，驗收對照表或實際操作的結果是多少？", "suggestions": [{"label": "一致", "text": "一致：手算 1225，程式結果 〈金額〉"}, {"label": "不一致", "text": "不一致：手算 1225，程式結果 〈金額〉，已要求修正"}, {"label": "未驗證", "text": "未驗證：〈原因〉"}]},
{"id": "fixes", "label": "我要求 Agent 修正的地方", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "修正項目", "text": "〈問題〉：要求 Agent〈修正方式〉，重跑結果〈…〉"}, {"label": "超出範圍", "text": "Agent 改了計畫外的〈檔案〉，要求還原"}]},
{"id": "review-scope", "label": "審查卡 1：改的檔案都在核准計畫裡嗎？", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "review-count", "label": "審查卡 2：測試數沒有變少、沒有新增跳過？", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "review-tests", "label": "審查卡 3：沒有刪除測試或改既有期待值？", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "review-open", "label": "審查卡 4：驗收對照表裡還有哪些失敗或未驗證？", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "未通過項目", "text": "〈AC ID〉：〈失敗／未驗證〉，原因：〈…〉"}]},
{"id": "review-unclear", "label": "審查卡 6：有沒有看不懂、要 Agent 再解釋的地方？", "type": "textarea", "hint": "沒有就寫「沒有」。審查卡 5（在 /docs 實際試用）在檢查點 5 做。", "suggestions": ["沒有", {"label": "請 Agent 解釋", "text": "〈看不懂的地方〉：已請 Agent 解釋，答覆：〈…〉"}]}
]}
```

## 檢查點 4 · 第二段實作（第 19–24 分鐘）

- [ ] 交代第二段：

```text
第一段我看過了。接著做第 〈N+1〉 到 〈M〉 步。付款失敗依我先前的決定處理。做完依工作規則回報驗收對照表，列出還有哪些測試被跳過，然後停下等我。
```

- [ ] Agent 停下後，同樣貼上「變更審查」提示詞：

```text
不要再修改。請用白話回答下列審查問題，每題附上你實際執行的指令與輸出：
1. 這次改了哪些檔案？每個檔案改了什麼、為什麼？有沒有不在核准計畫裡的檔案？
2. 測試總數和上一次比有沒有變少？有沒有新增 skip 或 xfail？
3. 有沒有刪除測試，或修改既有測試的期待值？（請用 git diff 檢查 tests 資料夾後回答）
4. 列出驗收對照表。
```

- [ ] 在驗收對照表中特別核對付款：只有 `PENDING_PAYMENT`（待付款）能付款、成功後 `PAID` 並建立唯一 Order、重複付款被拒、付款失敗不建立 Order。
- [ ] 填下方表單的審查卡。任何一題是「否」或「不確定」→ 不核准，請 Agent 解釋或修正。
- [ ] 沒問題就請 Agent 記錄這一段：

```text
這一段我核准了。請把目前的變更 Commit 成「第二段」，完成後告訴我結果，然後停下等我。
```

```callout tip
時間不夠時
第 24 分鐘還沒做到付款，就停在已完成的部分，直接進入檢查點 5 驗證已做的功能。未完成的列入交付摘要，不要硬趕。
```

```form
{"id": "gf-cp4", "title": "檢查點 4 確認","fields":[
{"id": "pytest", "label": "第二段的測試結果（驗收對照表最後一行）", "type": "text", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}, {"label": "未做到付款", "text": "時間不夠，停在〈步驟〉：〈pytest 結果〉"}]},
{"id": "diff", "label": "我看懂的一處付款或訂單變更", "type": "textarea", "hint": "依 Agent 的白話說明：哪個檔案、它讓系統能做什麼、對應的 Rule ID 與 AC。", "suggestions": [{"label": "變更說明", "text": "〈檔案〉：〈它讓系統能做什麼〉；對應 Rule 〈Rule ID〉、AC 〈AC ID〉"}]},
{"id": "tests-intact", "label": "審查卡 3：Agent 的審查答案確認沒有刪除測試或改既有期待值", "type": "checkbox"},
{"id": "review-scope", "label": "審查卡 1：改的檔案都在核准計畫裡嗎？", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "review-count", "label": "審查卡 2：測試數沒有變少、沒有新增跳過？", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "review-open", "label": "審查卡 4：驗收對照表裡還有哪些失敗或未驗證？", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "未通過項目", "text": "〈AC ID〉：〈失敗／未驗證〉，原因：〈…〉"}]},
{"id": "review-unclear", "label": "審查卡 6：有沒有看不懂、要 Agent 再解釋的地方？", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "請 Agent 解釋", "text": "〈看不懂的地方〉：已請 Agent 解釋，答覆：〈…〉"}]}
]}
```

## 檢查點 5 · 驗證（第 24–27 分鐘）

**不再加新功能。**

- [ ] 要求 Agent 補邊界測試並執行：

```text
不要再加新功能。請替下列情境補上測試並執行：
- 成人＋學生 1225
- 0 人、5 人被拒；4 人可建立
- 座位不足被拒且座位不變
- 不存在的 Booking／Order 回 404
- 付款失敗不建立 Order、不變成 PAID
- 重複付款被拒
然後依實際結果更新 README、docs/business-rules.md、docs/api-examples.md。
```

- [ ] Agent 做完後，請它整理驗收對照表：

```text
請整理驗收對照表：每條驗收條件（或規則）一列，欄位是「編號、白話內容、結果（通過／失敗／未驗證）、依據的測試名稱」。最後一行寫測試總數：通過幾個、失敗幾個、跳過幾個。附上你實際執行的指令。
```

- [ ] 自己走一次完整流程。先請 Agent 啟動 App：

```text
請在背景啟動這個專案的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 回傳 status=ok，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
```

在瀏覽器開 `http://127.0.0.1:8000/docs` → 點開要試的 API → 按「Try it out」→ 在 Request body 貼上 Runbook 提供的範例（或使用預設範例）→ 按「Execute」→ 看 Response 的狀態碼（例如 201 成功、400 輸入錯誤、404 找不到）和內容。依序試：

1. `GET /trips`：按「Try it out」→「Execute」，確認沒有 T003。
2. `POST /bookings`：把下方範例貼到 /docs 的 Request body，確認 `total_fare` 為 1225、`status` 為 `PENDING_PAYMENT`，記下 `booking_id`。
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
{"id": "pytest", "label": "最後一次測試結果（驗收對照表最後一行）", "type": "text", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed, 〈數字〉 skipped"}, {"label": "有失敗", "text": "〈數字〉 passed, 〈數字〉 failed, 〈數字〉 skipped"}]},
{"id": "flow", "label": "我自己走過的完整流程", "type": "checklist", "items": ["查班次沒有 T003", "訂票金額 1225、PENDING_PAYMENT", "付款成功並取得 Order", "查 Order 金額 1225", "重複付款被拒"], "hint": "只勾你在 /docs 實際走過且結果正確的項目。"},
{"id": "skipped", "label": "仍被 Skip 或未完成的項目", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "Skip 測試", "text": "〈測試名稱〉仍被 Skip：〈原因〉"}, {"label": "未完成功能", "text": "〈功能〉未完成：〈完成到哪裡〉"}]}
]}
```

## 檢查點 6 · 交付（第 27–29 分鐘）

- [ ] 要求 Agent 整理交付摘要：

```text
請整理交付摘要：修改檔案、Rule ID 與 AC 對應、最後一次 pytest -q 的指令與驗收對照表、文件更新、未完成項目與風險。沒有實際執行過的項目標為「未驗證」。
```

- [ ] 對照你在檢查點 1–5 的確認紀錄與審查卡，核對 Agent 的摘要；不一致時以你的實際確認為準。
- [ ] 到 [提交清單與交付摘要](#gf-submission) 填寫交付摘要並匯出。「人和 Agent 各做什麼」請自己寫，可直接引用檢查點 2–5 的紀錄。

```callout warning
第 29 分鐘停止修改
未完成時如實說明：記錄當前完成度與未完成項目後提交，不把部分完成描述為完整交付。遇到環境問題請告知主持人，並記錄耗時。
```
