# B0 Business Rules

> 讀者：參與者與Agent。時機：規則查證及測試分析。前置：閱讀README與架構。可見性：Participant。

以下是公開正確商業規則，不代表目前程式的每個案例均已通過。一般訂票保留Greenfield語意；多個優惠符合時的歷史政策需以程式與測試核對，不把新的最有利政策自行加入。

| Rule ID | 公開規則 |
|---|---|
| `TRIP-001` | 只可回傳仍有至少一個可售座位的班次。 |
| `TRIP-002` | Origin 與 Destination 是可選篩選條件；若提供，必須精確符合 Seed Data 中的站點名稱。 |
| `BOOKING-001` | 每筆訂票至少包含一位旅客。 |
| `BOOKING-002` | 單筆 Greenfield 訂票最多 4 位旅客。 |
| `BOOKING-003` | 旅客數不得超過班次剩餘座位數。 |
| `BOOKING-004` | 成功建立訂票後立即保留對應座位數。 |
| `BOOKING-005` | 建立後狀態為 `PENDING_PAYMENT`。 |
| `FARE-001` | 成人票為 Base Fare 的 100%。 |
| `FARE-002` | 學生票為 Base Fare 的 75%。 |
| `FARE-003` | 每位旅客個別計價後加總為 Booking Total Fare。 |
| `FARE-004` | 所有金額以整數表示，不處理小數與幣別換算。 |
| `PAYMENT-001` | 只有 `PENDING_PAYMENT` Booking 可以付款。 |
| `PAYMENT-002` | 付款成功後 Booking 狀態改為 `PAID`。 |
| `PAYMENT-003` | 同一 Booking 不得重複付款。 |
| `ORDER-001` | 付款成功後建立唯一 Order。 |
| `ORDER-002` | Order建立時amount等於付款時Booking Total Fare；改票後保留原付款快照，不執行差額金流。 |
| `MEMBER-001` | Booking 可以不綁定 Member。 |
| `MEMBER-002` | 有效 Member ID 可被附加至 Booking。 |
| `MEMBER-003` | Corporate Member 的企業優惠率為 95%。 |
| `FARE-005` | 購票日至出發日相差至少 14 天時，具備 85% 提前購票優惠資格。 |
| `FARE-006` | 未滿 14 天不得取得提前購票優惠。 |
| `CHANGE-001` | 只有已付款 Booking 可改票。 |
| `CHANGE-002` | 新 Trip 必須有足夠座位。 |
| `CHANGE-003` | 改票成功後釋放原 Trip 座位並保留新 Trip 座位。 |
| `CHANGE-004` | B0 只記錄 Fare Difference，不執行補價或退款。 |
| `REFUND-001` | 只有已付款 Booking 可退票。 |
| `REFUND-002` | 退票後 Booking 狀態為 `REFUNDED`。 |
| `REFUND-003` | 退票成功後釋放座位。 |
| `REFUND-004` | 退票建立唯一 Refund Record。 |
| `NOTIFY-001` | 付款成功建立通知紀錄。 |
| `NOTIFY-002` | 改票成功建立通知紀錄。 |
| `NOTIFY-003` | 退票成功建立通知紀錄。 |
| `SEAT-001` | 同一 Trip 內 Seat ID 不可重複配置。 |
| `SEAT-002` | 一般 Booking 不保證相鄰座位。 |
| `AUDIT-001` | Booking Created 必須留存 Audit Entry。 |
| `AUDIT-002` | Payment、Change、Refund 成功後必須留存 Audit Entry。 |

退票釋放原座位並建立Refund Record；一般付款失敗不取消訂票，仍為PENDING_PAYMENT且保留座位。改票使用最新票價，Fare Difference=new-old，Order保留原付款。通知與Audit僅本機紀錄。

固定Seed包含T001–T004及T005台北→台中750／6座、T006台北→高雄1400／18座、T007台中→台北700／10座、T008高雄→台中800／4座。會員M001/M003 STANDARD、M002 CORPORATE；非會員可訂票。

## 完成條件

規則來源、Rule ID與測試／程式可交叉核對；衝突與不確定事項列為資訊缺口，不擅自更改公開規則。
