# G1 Acceptance and Rule Test Map

> 讀者：主持人、驗收人員與教材產製 Agent。時機：G1 驗收及後續 Regression 規劃。前置：閱讀 [學員 AC](../participant/03-acceptance-criteria.md) 與 [G1 規則](reference-solution/greenfield-reference-mvp/docs/business-rules.md)。可見性：Evaluation／Agent Production，不發入學員包。

本表將實際 G1 測試案例對應驗收與規則；列出案例不等於執行通過，結果以 G1 Validation Report 為準。下表路徑相對 `reference-solution/greenfield-reference-mvp/`；`I::` 表示 `tests/integration/test_features.py::`，`H::` 表示 `tests/test_health.py::`。程式區域位於 `src/smart_ticket/`；文件位於 `docs/`。

## 15 項 Acceptance Criteria

Test File 相對 G1 目錄；`tests/integration/test_features.py` 使用完整案例名，不以縮寫代替權威 Test Name。

| Acceptance Criteria ID | Rule ID | Test File | Test Name | Expected Result | Validation Type |
|---|---|---|---|---|---|
| AC-G-001 | TRIP-001 | tests/integration/test_features.py | test_sellable_trips | HTTP 200；只列 T001／T002／T004，座位皆 >0；T003 不出現。 | Integration／API |
| AC-G-002 | TRIP-002 | tests/integration/test_features.py | test_exact_trip_filters；test_empty_trip_query | 起台北→T001／T002；訖台中→T001；台北到台中→T001；部分站名與不存在站名回傳空陣列，HTTP 200。 | Integration／API |
| AC-G-003 | BOOKING-001、FARE-001 | tests/integration/test_features.py | test_adult_booking | HTTP 201；一位成人 T001 總價 700，旅客欄位與請求一致。 | Integration／API |
| AC-G-004 | FARE-002 | tests/integration/test_features.py | test_student_booking | HTTP 201；一位學生 T001 總價 525，即 Base Fare 75%。 | Integration／API |
| AC-G-005 | FARE-003、FARE-004 | tests/integration/test_features.py | test_mixed_booking_reserves_seats | 成人加學生總價 1225，total_fare 型別為 int，HTTP 201。 | Integration／API |
| AC-G-006 | BOOKING-001 | tests/integration/test_features.py | test_zero_passengers_rejected | 0 人 HTTP 409／INVALID_PASSENGER_COUNT；T001 座位仍20，未建立 Booking。 | Integration／API＋狀態 |
| AC-G-007 | BOOKING-002 | tests/integration/test_features.py | test_more_than_four_rejected | 5 人 HTTP 409／INVALID_PASSENGER_COUNT，座位仍20且無 Booking；4 人 HTTP 201。 | Integration／API＋邊界 |
| AC-G-008 | BOOKING-003 | tests/integration/test_features.py | test_insufficient_seats_rejected | 剩1座要求2人 HTTP 409／INSUFFICIENT_SEATS，仍1座且無 Booking；售罄T003同為409且維持0座。 | Integration／API＋狀態 |
| AC-G-009 | BOOKING-004、BOOKING-005 | tests/integration/test_features.py | test_mixed_booking_reserves_seats | HTTP 201、PENDING_PAYMENT；T001 座位20→18，後續查詢也回傳18。 | Integration／API＋狀態 |
| AC-G-010 | PAYMENT-001、PAYMENT-002、ORDER-001、ORDER-002 | tests/integration/test_features.py | test_happy_path_and_paid_order_query | 付款HTTP 200；Booking為PAID；只有一筆Order，amount=Booking Total=700、payment_status=SUCCESS。 | Integration／API＋狀態 |
| AC-G-011 | PAYMENT-001、PAYMENT-003、ORDER-001 | tests/integration/test_features.py | test_payment_then_duplicate_rejected | 首次付款200；再次付款409／BOOKING_NOT_PAYABLE；Order數維持1。 | Integration／API＋狀態 |
| AC-G-012 | ORDER-001、ORDER-002 | tests/integration/test_features.py | test_happy_path_and_paid_order_query | 訂單查詢HTTP 200，回應等於付款時Order，Booking ID、amount=700、payment_status=SUCCESS一致。 | Integration／API |
| AC-G-013 | API 資源不存在行為 | tests/integration/test_features.py | test_missing_resources | 不存在Trip、Booking、Order均404，Code各為TRIP_NOT_FOUND／BOOKING_NOT_FOUND／ORDER_NOT_FOUND；T001維持20座且無Booking。 | Integration／API＋錯誤 |
| AC-G-014 | PAYMENT-002、ORDER-001 | tests/integration/test_features.py | test_failed_payment_preserves_pending | 付款失敗409／PAYMENT_FAILED，無Order、Booking維持PENDING_PAYMENT、T001保留後19座；再模擬成功可付款200。 | Integration／API＋失敗狀態 |
| AC-G-015 | 核心流程／Health | tests/integration/test_features.py；tests/test_health.py | test_happy_path_and_paid_order_query；test_health | Health 200／status=ok；班次查詢200→訂票201→付款200→Order查詢200，完整流程金額與狀態一致。 | Integration／End-to-End |

額外 Request 型別／Enum 驗證由 `I::test_request_validation` 對應 `schemas/contracts.py` 與 API 範例 422 行為；不以 Request Validation 取代商業規則 409。單元層另補直接 Service／Policy 的隔離驗證，Unit 與 Integration 均須完整執行。

## 16 項 Rule Traceability

| Rule ID | Requirement | Code | Test | Documentation | Validation Method |
|---|---|---|---|---|---|
| TRIP-001 | AC-G-001 | application/trip_service.py | I::test_sellable_trips | business-rules.md、api-examples.md | 可售／售罄結果 |
| TRIP-002 | AC-G-002 | application/trip_service.py | I::test_exact_trip_filters、I::test_empty_trip_query | business-rules.md、api-examples.md | 精確匹配與空結果 |
| BOOKING-001 | AC-G-003／006 | application/booking_service.py | I::test_adult_booking、I::test_zero_passengers_rejected | business-rules.md | 1 人成功／0 人拒絕 |
| BOOKING-002 | AC-G-007 | application/booking_service.py | I::test_more_than_four_rejected | business-rules.md | 4 人成功／5 人拒絕 |
| BOOKING-003 | AC-G-008 | application/booking_service.py | I::test_insufficient_seats_rejected | business-rules.md | 容量不足無殘留 |
| BOOKING-004 | AC-G-009 | application/booking_service.py、infrastructure/store.py | I::test_mixed_booking_reserves_seats | business-rules.md、architecture.md | 座位立即減少 |
| BOOKING-005 | AC-G-009 | application/booking_service.py、domain/models.py | I::test_mixed_booking_reserves_seats | business-rules.md | 初始 PENDING_PAYMENT |
| FARE-001 | AC-G-003 | domain/fare_policy.py | I::test_adult_booking | business-rules.md | 成人全額 |
| FARE-002 | AC-G-004 | domain/fare_policy.py | I::test_student_booking | business-rules.md | 學生 75% |
| FARE-003 | AC-G-005 | application/booking_service.py | I::test_mixed_booking_reserves_seats | business-rules.md、api-examples.md | 逐位加總 1225 |
| FARE-004 | AC-G-005 | domain/fare_policy.py、schemas/contracts.py | I::test_mixed_booking_reserves_seats | business-rules.md | 整數型別 |
| PAYMENT-001 | AC-G-010／011 | application/payment_service.py | I::test_happy_path_and_paid_order_query、I::test_payment_then_duplicate_rejected | business-rules.md | 待付款限定 |
| PAYMENT-002 | AC-G-010／014 | application/payment_service.py | I::test_happy_path_and_paid_order_query、I::test_failed_payment_preserves_pending | business-rules.md | 成功 PAID／失敗 pending |
| PAYMENT-003 | AC-G-011 | application/payment_service.py | I::test_payment_then_duplicate_rejected | business-rules.md | 重複付款拒絕 |
| ORDER-001 | AC-G-010／011／014 | application/payment_service.py、application/order_service.py | I::test_happy_path_and_paid_order_query、I::test_payment_then_duplicate_rejected、I::test_failed_payment_preserves_pending | business-rules.md | 成功唯一／失敗無訂單 |
| ORDER-002 | AC-G-010／012 | application/payment_service.py、schemas/contracts.py | I::test_happy_path_and_paid_order_query | business-rules.md、api-examples.md | 訂票與訂單金額相同 |

## 完成條件

15 AC 與 16 Rule ID 均有實際 Code／Test／Document 對應；在 G1 目錄執行完整測試並將指令、結果與限制寫入 Validation Report。測試對照表不宣稱尚未執行的 PASS。
