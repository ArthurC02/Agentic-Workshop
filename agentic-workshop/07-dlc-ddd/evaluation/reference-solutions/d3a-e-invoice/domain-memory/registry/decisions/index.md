# Decisions

- [ADR-001](/decisions/ADR-001) — 採本機 In-Memory Adapter 與 Repository Protocol、固定 Seed 與共用 RLock；重啟即清除資料，不提供持久化或跨程序交易保證。.
- [ADR-002](/decisions/ADR-002) — 以 Domain Discount Policy 處理優惠資格；後續決策改為全部資格候選取最低 rate、逐旅客評估、不疊加，建立與改票共用。.
- [ADR-003](/decisions/ADR-003) — Application 同步呼叫 Notification Service，只新增 In-Memory 紀錄，不導入 Queue 或外部發送。.
- [ADR-004](/decisions/ADR-004) — 團體需同車廂完整連續空位、一次保留；團體付款失敗以取消、全釋放、無 Order 及紀錄補償；團體改票拒絕、已付款團體退票保留。不引入資料庫或通用交易 Framework。.
- [ADR-005](/decisions/ADR-005) — 新增 Invoicing Context 與 Domain 端 Port InvoiceIssuer（三種結果 ISSUED／REJECTED／UNAVAILABLE，不拋例外）；服務商欄位、代碼與 3 秒逾時只在 Adapter；付款在鎖內建立 PENDING 發票、鎖外第一次開立，失敗不回滾付款；重試以同一 or….
- [ASIS-001](/decisions/ASIS-001) — 現況觀察（非已核准決策）：座位庫存有三份資料——Trip.available_seats 計數器、seat_assignments、seat_capacity——沒有單一擁有者守住一致性，只靠服務層同步與全域 RLock。改動座位的變更必須同時處理三者。.
- [ASIS-002](/decisions/ASIS-002) — 現況觀察（非已核准決策）：計價迴圈在一般建立、團體建立、改票三處複製；新增計價規則必須三處一起改，否則路徑間不一致。文件說由 Fare Policy 協調，實際只走 DiscountPolicy，FarePolicy.calculate 只剩單元測試使用。.
- [ASIS-003](/decisions/ASIS-003) — 現況觀察（非已核准決策）：PaymentService 直接依賴具體 MockPaymentGateway（無 Port），閘道只有 charge；團體補償、Booking 狀態改寫都寫在 PaymentService 內。.
- [ASIS-004](/decisions/ASIS-004) — 現況觀察（非已核准決策）：退款紀錄以 booking_id 為鍵且金額固定為總票價，結構上一筆訂票只能有一筆全額退款；部分退款需要先改變這個結構。.
