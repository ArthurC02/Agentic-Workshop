# B3 Architecture

> 讀者：參與者與Agent。時機：Repository理解及影響分析。前置：閱讀README。可見性：Evaluation／Agent Production。

API／Schemas處理HTTP Contract，Application協調Use Case，Domain提供模型、Fare／Discount與座位規則，Infrastructure提供本機Repository、Seed、固定Clock與Mock Gateway。Domain不依賴FastAPI；Repository Protocol保持Service與Adapter邊界。共享RLock保護單程序狀態更新，旅客輸入複製避免外部修改污染Booking。

核心流程：Trip Query過濾可售班次；Booking驗證1–4人、容量及可選member，逐位計價並配置唯一座位；Payment成功更新PAID並建立唯一Order；Order保存付款當時金額。一般付款失敗仍pending、保留座位，不建立Order。

Change僅處理已付款Booking，檢查目標容量後釋放原座位、保留新座位，更新班次與票價，記錄new-old Fare Difference，不執行補款／退款；Order仍是原付款快照。Refund更新REFUNDED、釋放座位及建立唯一Refund Record。Notification同步建立本機事件紀錄，Audit記錄建立及成功付款／改退票事件。

八班固定Seed、可注入Clock與可控制Gateway便於重現測試；In-Memory不提供持久化或跨程序交易保證。歷史決策見ADR：本機Repository、Discount Policy與同步通知；重要結論需交叉核對程式與測試。

## B2計價演化

Discount Policy收集各Passenger符合的候選，加入ADULT全額預設，再選rate最低的單一優惠；Fare Result包含Type／Rate／Amount。Booking建立與Change使用同一路徑，個別金額加總且回傳根層Applied Discounts；Schemas保留原Passenger三欄。DEBT-001以簡單候選政策改善，不導入Rule Engine；同步Notification仍保留，非計價服務不重寫。

## B3 Group流程與Atomicity

Group API與Service沿用Repository、Clock、B2優惠政策及個別旅客合約。Seat Geometry提供carriage／row／seat／position，Policy尋找同車廂連續可用區段；以既有固定容量為上限，不以幾何布局虛增庫存。

建立先驗完整人數、班次、容量及區段，成功一次保留／建立；任何不成立無Booking／Order／座位殘留。Group付款失敗以可理解補償取消Booking、全釋放、無Order、Audit與通知；共用付款入口也依Booking Type處理，避免繞過Group補償。一般付款語意不變，不建通用Transaction Engine。

## 完成條件

能說明模組責任、依賴與核心狀態流，辨識變更影響及需要驗證的假設。
