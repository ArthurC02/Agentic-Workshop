# B3 Business Rules

> 讀者：主持人、驗收人員與教材產製Agent。時機：B3規則驗收。前置：閱讀README與架構。可見性：Evaluation／Agent Production。

以下是公開正確商業規則，不代表目前程式的每個案例均已通過。一般訂票保留既有邊界；B2逐位評估全部優惠資格並採最低rate單一優惠，不疊加。成人100%、學生75%、提前至少14天85%、企業95%為候選資格，實際結果記錄Type、Rate與Amount。

| Rule ID | 公開規則 |
|---|---|
| `TRIP-001` | 只可回傳仍有至少一個可售座位的班次。 |
| `TRIP-002` | Origin 與 Destination 是可選篩選條件；若提供，必須精確符合 Seed Data 中的站點名稱。 |
| `BOOKING-001` | 每筆訂票至少包含一位旅客。 |
| `BOOKING-002` | 單筆 Greenfield 訂票最多 4 位旅客。 |
| `BOOKING-003` | 旅客數不得超過班次剩餘座位數。 |
| `BOOKING-004` | 成功建立訂票後立即保留對應座位數。 |
| `BOOKING-005` | 建立後狀態為 `PENDING_PAYMENT`。 |
| `FARE-001` | 成人 Base Fare 100%；仍評估其他可用優惠資格。 |
| `FARE-002` | 學生資格對應 Base Fare 75%，由最有利單一優惠政策決定實際結果。 |
| `FARE-003` | 每位旅客個別計價後加總為 Booking Total Fare。 |
| `FARE-004` | 所有金額以整數表示，不處理小數與幣別換算。 |
| `PAYMENT-001` | 只有 `PENDING_PAYMENT` Booking 可以付款。 |
| `PAYMENT-002` | 付款成功後 Booking 狀態改為 `PAID`。 |
| `PAYMENT-003` | 同一 Booking 不得重複付款。 |
| `ORDER-001` | 付款成功後建立唯一 Order。 |
| `ORDER-002` | Order建立時amount等於付款時Booking Total Fare；改票後保留原付款快照，不執行差額金流。 |
| `MEMBER-001` | Booking 可以不綁定 Member。 |
| `MEMBER-002` | 有效 Member ID 可被附加至 Booking。 |
| `MEMBER-003` | Corporate Member 具備95%優惠資格。 |
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
| `FARE-007` | 多項優惠不可疊加。 |
| `FARE-008` | 同時符合多項優惠時採數值最低的單一折扣率。 |
| `FARE-009` | 每位Passenger獨立決定優惠。 |
| `FARE-010` | Fare Result記錄實際Discount Type及Rate，並包含Amount。 |

退票釋放原座位並建立Refund Record；一般付款失敗不取消訂票，仍為PENDING_PAYMENT且保留座位。改票使用最新票價，Fare Difference=new-old，Order保留原付款。通知與Audit僅本機紀錄。

固定Seed包含T001–T004及T005台北→台中750／6座、T006台北→高雄1400／18座、T007台中→台北700／10座、T008高雄→台中800／4座。會員M001/M003 STANDARD、M002 CORPORATE；非會員可訂票。

## B3團體新增規則

| Rule ID | 規則 |
|---|---|
| `GROUP-001` | 團體訂票旅客數最少 5 人。 |
| `GROUP-002` | 團體訂票旅客數最多 20 人。 |
| `GROUP-003` | 所有 Passenger 必須搭乘同一 Trip。 |
| `GROUP-004` | 必須配置同一車廂內連續座位。 |
| `GROUP-005` | 無法完整配置時不得建立 Booking。 |
| `GROUP-006` | 建立成功後一次保留全部座位。 |
| `GROUP-007` | 團體建立失敗時不得保留任何座位。 |
| `GROUP-PAY-001` | 團體付款成功後整筆 Booking 轉為 `PAID`。 |
| `GROUP-PAY-002` | 團體付款失敗後 Booking 轉為 `CANCELLED`。 |
| `GROUP-PAY-003` | 付款失敗後釋放全部團體座位。 |
| `GROUP-PAY-004` | 付款失敗不得建立 Order。 |
| `GROUP-PAY-005` | 團體付款成功只建立一筆 Order。 |
| `GROUP-FARE-001` | 每位 Passenger 依 B2 政策個別計價。 |
| `GROUP-FARE-002` | 團體 Total Fare 為個別 Fare 加總。 |
| `GROUP-AUDIT-001` | 團體建立、付款成功或付款失敗均留下 Audit Entry。 |
| `GROUP-NOTIFY-001` | 團體付款成功建立通知紀錄。 |
| `GROUP-NOTIFY-002` | 團體付款失敗建立取消通知紀錄。 |

## 適用範圍補充

BOOKING-002的一般上限4人保留，GROUP-001／002為團體5–20；單一團體不同Trip不成立。一般付款失敗pending／保留座位維持；GROUP付款失敗CANCELLED／全釋放／無Order。Group建立／付款成功／付款失敗留Audit，付款成功與取消留通知。Group改票明確不支援409，已付款Group退款沿用全釋放，原一般Change功能保留。

## 完成條件

規則來源、Rule ID與測試／程式可交叉核對；衝突與不確定事項列為資訊缺口，不擅自更改公開規則。
