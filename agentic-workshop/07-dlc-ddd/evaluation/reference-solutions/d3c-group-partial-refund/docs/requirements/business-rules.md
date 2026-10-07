# Business Rules

Smart Ticket 目前生效的商業規則。每條規則有固定 Rule ID，程式註解與測試以此追溯。

每位旅客逐一評估所有優惠資格，採 rate 最低的單一優惠，不疊加。候選資格：成人 100%、學生 75%、提前購票（至少 14 天）85%、企業會員 95%；結果記錄 Type、Rate 與 Amount。詳見 [優惠政策](discount-overview.md)。

| Rule ID | 公開規則 |
|---|---|
| `TRIP-001` | 只可回傳仍有至少一個可售座位的班次。 |
| `TRIP-002` | Origin 與 Destination 是可選篩選條件；若提供，必須精確符合 Seed Data 中的站點名稱。 |
| `BOOKING-001` | 每筆訂票至少包含一位旅客。 |
| `BOOKING-002` | 一般訂票單筆最多 4 位旅客（團體訂票見 GROUP-001／002）。 |
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
| `ORDER-002` | Order建立時amount等於付款時Booking Total Fare；改票後保留原付款快照，不執行差額金流。有點數折抵時改為應付金額，見 PTS-009。 |
| `MEMBER-001` | Booking 可以不綁定 Member。 |
| `MEMBER-002` | 有效 Member ID 可被附加至 Booking。 |
| `MEMBER-003` | Corporate Member 具備95%優惠資格。 |
| `MEMBER-004` | 每位 Member 有點數餘額（points_balance，非負整數），可透過會員查詢取得；可於訂票時折抵（見點數折抵規則），尚無累積功能。 |
| `FARE-005` | 購票日至出發日相差至少 14 天時，具備 85% 提前購票優惠資格。 |
| `FARE-006` | 未滿 14 天不得取得提前購票優惠。 |
| `CHANGE-001` | 只有已付款 Booking 可改票。 |
| `CHANGE-002` | 新 Trip 必須有足夠座位。 |
| `CHANGE-003` | 改票成功後釋放原 Trip 座位並保留新 Trip 座位。 |
| `CHANGE-004` | 改票只記錄 Fare Difference，不執行補價或退款。 |
| `REFUND-001` | 只有已付款 Booking 可退票。 |
| `REFUND-002` | 退票後 Booking 狀態為 `REFUNDED`。 |
| `REFUND-003` | 退票成功後釋放座位。 |
| `REFUND-004` | 每次退款建立一筆新的 Refund Record（整筆退票一筆；團體部分取消每次一筆，見 PCR-007），既有紀錄不被覆寫。 |
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

固定 Seed 包含 T001 台北→台中 700／20座、T002 台北→高雄 1500／8座、T003 台中→高雄 800／0座、T004 高雄→台北 1500／12座，T005 台北→台中 750／6座、T006 台北→高雄 1400／18座、T007 台中→台北 700／10座、T008 高雄→台中 800／4座。全部出發時間為 2030-01-15 09:00（+08:00）。會員 M001 STANDARD（1,200 點）、M002 CORPORATE（5,000 點）、M003 STANDARD（0 點）；非會員可訂票。

## 團體訂票規則

| Rule ID | 規則 |
|---|---|
| `GROUP-001` | 團體訂票旅客數最少 5 人；部分取消後的有效旅客也不得少於 5 人（或全部取消，見 PCR-005）。 |
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
| `GROUP-FARE-001` | 每位 Passenger 依最有利單一優惠政策個別計價。 |
| `GROUP-FARE-002` | 團體 Total Fare 為個別 Fare 加總。 |
| `GROUP-AUDIT-001` | 團體建立、付款成功或付款失敗均留下 Audit Entry。 |
| `GROUP-NOTIFY-001` | 團體付款成功建立通知紀錄。 |
| `GROUP-NOTIFY-002` | 團體付款失敗建立取消通知紀錄。 |

## 電子發票規則

付款成功的 Order 由外部發票服務商開立電子發票。營業稅率 5%，票價為含稅價；銷售額 = 含稅總額 ÷ 1.05 四捨五入到整數元，稅額 = 含稅總額 − 銷售額。單次呼叫服務商逾時 3 秒；同一張發票最多呼叫 5 次（含第一次）。例：700 → 667＋33；3,500 → 3,333＋167；665 → 633＋32。

| Rule ID | 規則 |
|---|---|
| `EINV-001` | 一般與團體訂票付款成功後，各為該 Order 開立一張發票；團體整團一張。 |
| `EINV-002` | 發票開立失敗不影響付款結果：付款仍成功、Booking 為 `PAID`、Order 已建立且金額不變。 |
| `EINV-003` | 發票總額等於 Order.amount，銷售額與稅額依上述公式以整數計算。 |
| `EINV-004` | 品項一行：「{起站}-{迄站} 車票」、數量為旅客數、金額為 Order.amount、單價為金額 ÷ 數量向下取整。 |
| `EINV-005` | 一筆 Order 至多一張已開立發票；以 order_id 作為商家訂單編號，重試或重複觸發不得產生第二張。 |
| `EINV-006` | 發票狀態為 `PENDING`、`ISSUED`、`FAILED`，可依 order_id 查詢；`ISSUED` 時含發票號碼。 |
| `EINV-007` | 暫時失敗（服務商忙碌、逾時、連線失敗）維持 `PENDING`，記錄呼叫次數與最後錯誤；可觸發重試開立。 |
| `EINV-008` | 累計呼叫 5 次仍未成功轉為 `FAILED`。 |
| `EINV-009` | 永久失敗（欄位格式錯誤、統編檢核失敗）直接轉為 `FAILED` 並記錄錯誤代碼。 |
| `EINV-010` | 服務商回覆「已開立過」視為成功，以原發票號碼標為 `ISSUED`。 |
| `EINV-011` | `ISSUED` 發票號碼不可變更；`ISSUED` 與 `FAILED` 發票重試不呼叫服務商，直接回傳原結果。 |
| `EINV-012` | 付款時可選填統編（含公司名稱）或手機條碼載具，二者擇一；皆未提供時開立一般個人發票。 |
| `EINV-013` | 統編非 8 位數字、手機條碼不符格式（`/` 加 7 碼 `0-9 A-Z . + -`）、同時提供兩者、或統編缺公司名稱時，付款被拒（422 `INVALID_INVOICE_INFO`），不扣款、不建立 Order。 |
| `EINV-014` | 開立成功記錄 Audit 與通知 `INVOICE_ISSUED`；轉為 `FAILED` 記錄 Audit `INVOICE_FAILED`（detail 含錯誤代碼）；`PENDING` 的失敗不通知。 |

發票作廢、折讓（退票、改票、部分取消）不在本期範圍；改票不改 Order.amount，不另開發票。設計見 [ADR 005](../adr/005-issue-e-invoices-through-a-port.md)。

## 點數折抵規則

會員訂票時可用點數折抵票款。1 點 = 新台幣 1 元；單筆至少 100 點、必須是 100 的倍數、不得超過優惠後總額（Booking Total Fare）的 30%（向下取整）。應付金額 = 優惠後總額 − 折抵點數。例（非提前購票）：M001 成人 1 位 700 → 最多 200、應付 500；M002 企業成人 665 → 上限 199、最多 100、應付 565；M001 成人 5 位團體 3,500 → 最多 1,000、應付 2,500；M001 成人＋學生 1,225 → 最多 300、應付 925。這些規則與商業數字的唯一出處是 `domain/members.py`。

| Rule ID | 規則 |
|---|---|
| `PTS-001` | 一般與團體訂票可選填 `redeemed_points`；不填或 0 表示不使用，行為與現行相同。 |
| `PTS-002` | 未綁定會員卻要求折抵，409 `POINTS_MEMBER_REQUIRED`。 |
| `PTS-003` | 折抵點數小於 100 或不是 100 的倍數（含負數），409 `POINTS_INVALID_AMOUNT`。 |
| `PTS-004` | 折抵點數超過可用點數，409 `POINTS_INSUFFICIENT`。 |
| `PTS-005` | 折抵點數超過優惠後總額 30%（向下取整），409 `POINTS_EXCEED_LIMIT`。同時違反多條時依 PTS-002、003、004、005 順序回報第一個；這些檢查在既有的班次、人數、座位、會員檢查之後。 |
| `PTS-006` | 點數折抵不是優惠，不參與 FARE-007／008；`total_fare` 與 `applied_discounts` 不因折抵改變。 |
| `PTS-007` | Booking 回應含 `total_fare`（優惠後總額）、`redeemed_points`、`payable_amount`（`total_fare` − 折抵點數，改票後依新的 `total_fare` 計算）。 |
| `PTS-008` | 建立成功時立即預留（扣除）點數；任何檢查失敗都不建立 Booking、不保留座位、不扣點數。 |
| `PTS-009` | 付款向閘道扣款應付金額，Order.amount 等於應付金額；電子發票金額因此也是應付金額。 |
| `PTS-010` | 團體付款失敗（`CANCELLED`）時歸還全部預留點數。 |
| `PTS-011` | 一般付款失敗維持 `PENDING_PAYMENT`，點數繼續預留。 |
| `PTS-012` | 整筆退票退款金額為 Order.amount（實付金額，未折抵的訂票亦同），並歸還全部折抵點數。 |
| `PTS-013` | 改票不退不補點數；Fare Difference 仍為新舊 `total_fare` 相減。 |
| `PTS-014` | 會員可用點數不得為負；同一會員同時建立多筆訂票，合計預留不超過原餘額（全域鎖內檢查並扣除）。 |
| `PTS-015` | 預留與歸還記錄 Audit `POINTS_RESERVED`、`POINTS_RESTORED`，detail 為 `points=<點數>`。 |

點數累積、到期、一般訂票 PENDING 逾時釋放、付款前修改折抵點數、有折抵團體的部分取消均不在本期範圍。設計見 [ADR 006](../adr/006-membership-owns-points-redemption.md)。

## 團體部分取消規則

已付款的團體訂票可以只取消部分旅客，依出發前天數 D（班次出發日的台灣日期 − Clock 今天）收手續費後退款。手續費率：D ≥ 14 為 10%、7 ≤ D ≤ 13 為 20%、1 ≤ D ≤ 6 為 30%、D ≤ 0 不受理。手續費 = 該旅客 `applied_discounts` 金額 × 費率 ÷ 100 向下取整，逐位計算後加總；退款 = 票價 − 手續費。例：預設 Clock（D = 1）成人 700 → 手續費 210、退款 490；學生 525 → 157、368；兩位學生同時取消 → 314、736（不是 1,050 × 30% = 315）。2030-01-01 購買的提前票 595：D = 14 → 59、536；D = 7 → 119、476。費率與門檻的唯一出處是 `domain/cancellation.py`，團體人數下限是 `domain/models.py` 的 `MIN_GROUP_SIZE`。

| Rule ID | 規則 |
|---|---|
| `PCR-001` | 只有 `PAID` 的團體訂票可部分取消。一般訂票、有點數折抵的團體回 409 `PARTIAL_CANCEL_NOT_SUPPORTED`；非 `PAID` 回 409 `BOOKING_NOT_REFUNDABLE`。 |
| `PCR-002` | 以 passenger_id 指定一位或多位旅客。不屬於此訂票 404 `PASSENGER_NOT_FOUND`；已取消 409 `PASSENGER_ALREADY_CANCELLED`；清單為空或重複 422 `INVALID_PASSENGER_IDS`。 |
| `PCR-003` | D ≤ 0 回 409 `REFUND_WINDOW_CLOSED`。 |
| `PCR-004` | 手續費與退款逐位以該旅客票價計算，不以 total_fare 平均；金額皆為整數。 |
| `PCR-005` | 取消後有效旅客須 ≥ 5 人或 0 人；剩 1–4 人時整個請求 409 `GROUP_BELOW_MINIMUM`。 |
| `PCR-006` | 只釋放被取消旅客的座位，班次可售座位數增加相同數量；其他旅客保留原座位，不重新配位、不再要求連續。 |
| `PCR-007` | 每次成功產生一筆新的退款紀錄（refund_id、booking_id、passenger_ids、fee、amount、created_at）。 |
| `PCR-008` | Σ 退款 + Σ 手續費 + Σ 有效旅客票價 = Order.amount，任何時刻成立；Order.amount 與 `total_fare` 不變。整筆退票視為全部旅客取消、手續費 0。 |
| `PCR-009` | 仍有有效旅客時維持 `PAID`；最後一位取消後轉 `REFUNDED`。 |
| `PCR-010` | Booking 回應 `cancelled_passenger_ids` 列出已取消旅客；`GET /bookings/{id}/refunds` 列出全部退款紀錄。 |
| `PCR-011` | 任一條件不成立時整個請求失敗，不留下座位、退款紀錄或狀態變更。 |
| `PCR-012` | 部分取消過的團體不可整筆退票（409 `BOOKING_NOT_REFUNDABLE`）；從未部分取消的團體整筆退票維持全額。 |
| `PCR-013` | 成功時記錄 Audit 與通知 `PASSENGERS_CANCELLED`，detail 為 `passenger_ids=<以逗號分隔> refund=<退款合計> fee=<手續費合計>`。 |
| `PCR-014` | 只建立本機退款紀錄，不呼叫付款閘道。 |

同時違反多條時的回報順序：PCR-001（類型／點數 → 狀態）→ 清單格式 → PCR-003 → PCR-002（依清單順序逐位）→ PCR-005。一般訂票部分取消、團體改票、整筆退票收手續費、閘道退款與發票折讓不在本期範圍。設計見 [ADR 007](../adr/007-group-booking-owns-passenger-cancellation.md)。

## 適用範圍補充

一般訂票上限 4 人（BOOKING-002），團體為 5–20 人（GROUP-001／002）；單一團體不同Trip不成立。一般付款失敗pending／保留座位維持；GROUP付款失敗CANCELLED／全釋放／無Order。Group建立／付款成功／付款失敗留Audit，付款成功與取消留通知。Group改票明確不支援409，已付款Group退款沿用全釋放（尚未部分取消過時），一般改票不受影響。
