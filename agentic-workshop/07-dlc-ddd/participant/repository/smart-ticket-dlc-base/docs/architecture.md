# Architecture

API／Schemas 處理 HTTP Contract，Application 協調 Use Case，Domain 提供模型、Fare／Discount 規則，Infrastructure 提供 In-Memory Store、Seed、固定 Clock 與模擬付款閘道。Domain 不依賴 FastAPI。`TicketRepositories` Protocol 描述 Trip、Booking、Order 的存取邊界。共享 RLock 保護單程序狀態更新，旅客輸入會複製，避免外部修改污染 Booking。

核心流程：Trip Query 過濾可售班次；Booking 驗證 1–4 人、容量及可選 member，逐位計價並配置唯一座位；Payment 成功更新 PAID 並建立唯一 Order；Order 保存付款當時金額。一般付款失敗仍 pending、保留座位，不建立 Order。

Change 僅處理已付款 Booking，檢查目標容量後釋放原座位、保留新座位，更新班次與票價，記錄 new-old Fare Difference，不執行補款／退款；Order 仍是原付款快照。Refund 更新 REFUNDED、釋放座位及建立唯一 Refund Record。Notification 同步建立本機事件紀錄，Audit 記錄建立及成功付款／改退票事件。

八班固定 Seed、可注入 Clock 與可控制 Gateway 便於重現測試；In-Memory 不提供持久化或跨程序交易保證。歷史決策見 [ADR](adr/)。

## 計價

Discount Policy 收集各 Passenger 符合的候選，加入 ADULT 全額預設，再選 rate 最低的單一優惠；結果包含 Type／Rate／Amount。Booking 建立、團體建立與改票都使用此政策，個別金額加總並回傳根層 Applied Discounts；Schemas 保留原 Passenger 三欄。規則見 [優惠政策](requirements/discount-overview.md)。

## 團體訂票與座位

Group API 與 Service 沿用 Store、Clock、優惠政策及個別旅客合約。座位幾何提供 carriage／row／seat／position，尋找同車廂連續可用區段；以既有固定容量為上限，不以幾何布局虛增庫存。

建立前先驗證完整人數、班次、容量及區段，成功時一次保留／建立；任何不成立都不留下 Booking／Order／座位。團體付款失敗以補償取消 Booking、全釋放、無 Order，並記錄 Audit 與通知；共用付款入口也依 Booking Type 處理，避免繞過團體補償。一般付款語意不變，未建立通用 Transaction Engine。
