# D3 決策卡（實作 Handoff）

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員。使用時機：D3a（需求卡 01）、D3b（需求卡 02）、D3c（需求卡 03）每段的檢查點 2–3（步驟見 Runbook（課堂操作手冊） 各段頁面）；每個需求卡各寫一張。

這張卡是交給 Coding Agent 的**決策紀錄**，不是程式提示詞。下方英文段名沿用 Plugin 的交接單格式，括號內是中文說明。由你們依 Domain Memory 的查詢結果與需求卡做決定；Agent 讀它、提計畫、照它實作。每段把它存成 `docs/handoffs/<段落>.md`（例如 `docs/handoffs/d3a-e-invoice.md`）。

```text
需求卡：〈01 電子發票／02 點數折抵／03 團體部分退款〉

Domain facts（領域事實；只寫查得到的 id，格式為「類別:id」，例如 rules:FARE-005）：
- reviewed（已審查）：〈asset:id〉、〈asset:id〉
- 只是候選（不可當成事實）：〈asset:id〉
- 查不到（知識缺口）：〈名詞〉

Owner Context（負責這個需求的 Context）與理由：
- 〈context id 或新 Context 名稱〉：〈為什麼是它，不是另一個〉

不變量（每條都要能寫成會失敗的測試）：
- INV-1：〈 〉
- INV-2：〈 〉

邊界與協作：
- 〈誰呼叫誰、交換什麼資料、同步或事後觸發、誰負責翻譯〉
- 禁止的依賴：〈例如：domain（領域程式）不得 import infrastructure（外部連線程式）〉

外部系統（沒有就刪掉這段）：
- 〈系統〉：domain 要它做什麼；domain 必須分辨的結果：〈成功／重複／永久失敗／暫時失敗〉

Unknowns（未知事項；不得由 Agent 自行補值）：
- 〈問題〉：〈暫定做法或「停下來問」〉

Proof obligations（要通過的檢查，寫成可觀察的測試；AC＝驗收條件、INV＝不變量）：
- 〈AC 或 INV id〉 → 〈測試檔與測試名稱〉

Counterfactual check（反事實檢查：故意改壞一處程式，確認測試會失敗；每條新規則一次）：
- 〈規則 id〉：改壞〈檔案中的唯一字串〉→ 預期〈測試〉失敗 → 必須看到 killed

這一段不做：
- 〈需求卡「不在本期範圍」中與本段相關的項目〉
```
