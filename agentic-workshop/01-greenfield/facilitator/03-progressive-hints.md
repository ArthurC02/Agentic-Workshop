# Greenfield 三級提示

> 讀者：Facilitator。時機：學員已描述卡點並嘗試後，逐級提供。
> 前置：閱讀需求／AC、[主持指南](01-facilitation-guide.md)及 [G0 指令](../../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)。
> 可見性：Facilitator 內部；一次只口頭提供一級，不整表發放。

每次提示後請學員說明下一步並自行操作；不得直接給完整程式碼或完整解題 Prompt。

| 卡點 | Hint 1：引導搜尋 | Hint 2：引導責任 | Hint 3：指出檔案群組／檢查方向 |
|---|---|---|---|
| 找不到入口 | 搜尋 Greenfield TODO、Rule ID，閱讀 README 啟動入口。 | 從 API 請求追到 Application，再找 Domain／Repository。 | 查看 `src/smart_ticket/main.py`、`api/`、`application/` 與對應 TODO 群組，請學員畫出呼叫方向。 |
| Fare 不正確 | 比對 FARE-001–004，用固定 Seed 的成人與學生例子手算。 | 每位旅客先計價再加總；學生 75%；票價規則在 Domain Policy。 | 查看 `domain/` 的 Fare Policy、Booking 用例及 Fare 單元測試，檢查乘率、整數與總額。 |
| Fixture 無法重置 | 單獨重跑失敗測試，問結果是否依賴執行順序。 | 每個測試前重置 In-Memory Store，避免共享可變狀態。 | 查看 `tests/conftest.py`、Store／Seed／Reset 群組，檢查 fixture scope 與 App 使用的實例是否一致。 |
| Payment／Order 關係 | 對照 PAYMENT-001–003、ORDER-001–002，描述成功與重複付款。 | 付款用例負責狀態轉移及唯一 Order；Order 查詢讀取既有結果。 | 查看付款用例、Mock Gateway、Booking／Order Repository 及整合測試；檢查失敗是否產生 Order 或誤轉 PAID。 |
| 時間不足 | 列出已完成、未驗證與尚未開始項目，回到核心 AC。 | 停止擴充，先驗證已做流程，再補最少文件與限制。 | 17 分鐘收斂、20 分鐘摘要、22 分鐘停止；用提交清單整理 Plan／Diff／Test，未完成如實標記。 |

環境問題可直接協助確認 Python、Import、依賴與測試命令；商業實作仍由人員主導。記錄卡點與已給級別，以便交接而不重複洩漏更多提示。

完成條件：五項卡點皆具三級提示，逐級使用且無完整解答；學員仍能說明需求、自己決定修改並接受測試結果。
