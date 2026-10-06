# EXCEPTION-DW-001：SQLite越界提議

> 讀者：主持人。時機：Gate2相對第6–7分鐘／活動69–70分鐘。前置：既定In-Memory Constraint可查。可見性：Facilitator，事件內容按時機口頭發放。

唯一例外為主要Agent提議以SQLite簡化座位交易與Rollback，與「本次維持In-Memory、不可新增資料庫」衝突。只評估提議，不真正安裝、啟用或改寫SQLite，也不修改技術棧。

若Agent已自行提出SQLite，直接以此為唯一EXCEPTION-DW-001，記錄原提議與時間，不再發第二事件。若未提出，Gate2後以假設事件卡詢問，不冒稱Agent已做此提議：

> 假設主要Agent建議加入SQLite，認為能簡化座位保留與付款失敗Rollback。請依已核准Constraint，在60秒內做Gate決策並回覆Agent。

這60秒包含於相對6–7分鐘，不額外延長；時間不足縮為30秒，不刪事件、不再注入。到時停止長篇資料庫架構討論，留下可追查決策。

| 回應 | 判定與後續 |
|---|---|
| Reject SQLite proposal | 可接受。只拒絕越界提議，不是拒絕整個團體任務；要求改回In-Memory與可理解補償方案。 |
| Approve With Conditions | 只有明確剔除SQLite／資料庫、改In-Memory並核對新方案後才可執行。 |
| 直接Approve SQLite | 不可接受。提醒Rule，要求回Gate並撤回越界方案。 |
| 含糊條件後開始Coding | 不可接受；條件未解除先停工補證。 |
| 長篇討論或實際安裝 | 不可接受，立即停止並回既定範圍。 |

預期人員核對Constraint，Reject或有條件改回現有Repository補償；Agent調整方案且等待核准。記錄原提議／假設卡來源、證據、風險、Decision、Conditions、Approver、時間與回覆Agent內容；若已有自然例外，不重複記成兩件。

## 完成條件

恰好一件例外、無真實資料庫變更、範圍與條件處理有證據，回到核准In-Memory任務且不越過未解除條件。
