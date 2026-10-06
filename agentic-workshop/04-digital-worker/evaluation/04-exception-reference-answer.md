# SQLite 例外參考回應

> 讀者：Evaluation、Facilitator。時機：Gate 2例外判讀及回顧。
> 前置：Work Order固定In-Memory Constraint與Gate 2提案。可見性：Evaluation答案，禁止交Participant。
> 來源：[治理指令 §11–12／20](../../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)。

唯一注入事件EXCEPTION-DW-001：主要Agent在Gate 2提議SQLite簡化座位交易／Rollback。SQLite超出已核准Persistence＝In-Memory；即使SQLite可由標準函式庫使用，仍是未核准資料庫變更。不能安裝、實作或把SQLite寫進Conditional Approval。

標準短回應（範例，不是真實核准紀錄）：

```text
Decision: REJECT AND REVISE
Evidence Reviewed: Work Order Persistence＝In-Memory；Gate 2 SQLite提案與此限制衝突。
Conditions / Required Corrections: 拒絕SQLite方案，保留團體任務；重提In-Memory Seat Reservation與Compensation方案，說明完整連續區段、建立atomic、付款失敗CANCELLED／全release／無Order的實測計畫。
Approver: 真實人員待填
Timestamp / Workshop Minute: 實際時間待填
```

允許的修正方向：使用現有Repository、先完整Plan再Reserve，付款失敗明確Compensation；若現有架構不足，可在核准範圍內新增In-Memory Snapshot、Reservation Token或明確Rollback Method。這些是可選設計，不強制全部採用，不要求通用Transaction Framework；仍須提出Diff／Test／風險並取得Gate 2核准。

Reject的是超範圍方案，不是整個任務。若改提案尚缺證據，可APPROVE WITH CONDITIONS，但只針對符合In-Memory邊界的方案；前置條件須由人員確認閉環後才能Coding。不得因13分鐘壓力先做再補核准。找不到可行atomic／補償設計，應停止、說明阻擋並升級。

判讀證據：Participant是否指出Constraint、Challenge提議、選擇Reject／重提、要求全團體補償與測試，保留Decision／Approver／時間／Context；不要求Participant說出此參考答案原文，不提供完整Code。

完成條件：單一事件、拒絕SQLite方案且保留任務、In-Memory可選補償方向明確、條件閉環才開工；真實演練未執行，沒有實際例外核准紀錄。
