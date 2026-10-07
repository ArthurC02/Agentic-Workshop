# D3 決策卡（實作 Handoff）

> 讀者：DDD 延伸課程學員。使用時機：D3a、D3b、D3c 每段的檢查點 2–3；每個需求卡各寫一張。

這張卡是交給 Coding Agent 的**決策紀錄**，不是程式提示詞。由你們依 Domain Memory 的查詢結果與需求卡做決定；Agent 讀它、提計畫、照它實作。每段把它存成 `docs/handoffs/<段落>.md`（例如 `docs/handoffs/d3a-e-invoice.md`）。

```text
需求卡：〈01 電子發票／02 點數折抵／03 團體部分退款〉

Domain facts（只寫查得到的 id）：
- reviewed：〈asset:id〉、〈asset:id〉
- 只是候選（不可當成事實）：〈asset:id〉
- 查不到（知識缺口）：〈名詞〉

Owner Context 與理由：
- 〈context id 或新 Context 名稱〉：〈為什麼是它，不是另一個〉

不變量（每條都要能寫成會失敗的測試）：
- INV-1：〈 〉
- INV-2：〈 〉

邊界與協作：
- 〈誰呼叫誰、交換什麼資料、同步或事後觸發、誰負責翻譯〉
- 禁止的依賴：〈例如：domain 不得 import infrastructure〉

外部系統（沒有就刪掉這段）：
- 〈系統〉：domain 要它做什麼；domain 必須分辨的結果：〈成功／重複／永久失敗／暫時失敗〉

Unknowns（不得由 Agent 自行補值）：
- 〈問題〉：〈暫定做法或「停下來問」〉

Proof obligations（可觀察的測試）：
- 〈AC 或 INV id〉 → 〈測試檔與測試名稱〉

Counterfactual check（每條新規則一次）：
- 〈規則 id〉：改壞〈檔案中的唯一字串〉→ 預期〈測試〉失敗 → 必須看到 killed

這一段不做：
- 〈需求卡「不在本期範圍」中與本段相關的項目〉
```
