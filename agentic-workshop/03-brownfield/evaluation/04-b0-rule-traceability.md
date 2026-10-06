# B0 Rule 追溯矩陣

> 讀者：Evaluation、Facilitator、Agent Production。時機：B0 驗收／B1 恢復檢查。
> 前置：完整 B0 測試輸出及 [Failure Manifest](06-intentional-failure-manifest.md)。可見性：Evaluation 內部，不放 Participant Package。

36 項規則＝G1 16＋B0 新增 20。路徑相對 [B0 Repository](../participant/repository/smart-ticket-b0/)；Code 前綴 `src/smart_ticket/`、Test 前綴 `tests/`。所有 Documentation 指向該 Repository 的 `docs/business-rules.md`（規則）及 `docs/api-examples.md`（HTTP）；結構見 `docs/architecture.md`。PASS 表示本次既有測試已通過，不宣稱一條測試覆蓋所有子情境。

| Rule ID | Requirement | Code Area／Symbol | Test File | Test Name | Documentation | State |
|---|---|---|---|---|---|---|
| TRIP-001 | G1 §4.2／5 | `application/trip_service.py::query` | `integration/test_features.py` | `test_sellable_trips` | docs/business-rules.md；docs/api-examples.md | PASS |
| TRIP-002 | G1 §4.2／5 | `application/trip_service.py::query` | `integration/test_features.py` | `test_exact_trip_filters` | docs/business-rules.md；docs/api-examples.md | PASS |
| BOOKING-001 | G1 §4.3／5 | `application/booking_service.py::create` | `unit/test_services.py` | `test_zero_passengers_rejected_without_mutating_store` | docs/business-rules.md；docs/api-examples.md | PASS |
| BOOKING-002 | G1 §4.3／5 | `application/booking_service.py::create` | `unit/test_services.py` | `test_four_passengers_are_accepted / test_five_passengers_rejected_without_mutating_store` | docs/business-rules.md；docs/api-examples.md | PASS |
| BOOKING-003 | G1 §4.3／5 | `application/booking_service.py::create` | `unit/test_services.py` | `test_insufficient_seats_rejected_atomically` | docs/business-rules.md；docs/api-examples.md | PASS |
| BOOKING-004 | G1 §4.3／5 | `application/booking_service.py::create` | `unit/test_services.py` | `test_four_passengers_are_accepted` | docs/business-rules.md；docs/api-examples.md | PASS；混合案例另受 Bug 影響 |
| BOOKING-005 | G1 §4.3／5 | `application/booking_service.py::create` | `unit/test_services.py` | `test_successful_mixed_booking_reserves_seats_and_starts_pending` | docs/business-rules.md；docs/api-examples.md | 預期失敗；pending 斷言先通過，金額失敗 |
| FARE-001 | G1 §5 | `domain/fare_policy.py::calculate` | `unit/test_fare_policy.py` | `test_adult_fare_is_full_base_fare` | docs/business-rules.md；docs/api-examples.md | PASS |
| FARE-002 | G1 §5 | `domain/fare_policy.py::calculate` | `unit/test_fare_policy.py` | `test_student_fare_is_seventy_five_percent` | docs/business-rules.md；docs/api-examples.md | 預期失敗，正確 75% 保留 |
| FARE-003 | G1 §5 | `application/booking_service.py::create` | `unit/test_fare_policy.py` | `test_mixed_passenger_fares_sum_as_integers` | docs/business-rules.md；docs/api-examples.md | 預期失敗，正確總額保留 |
| FARE-004 | G1 §5 | `domain/fare_policy.py::calculate` | `unit/test_fare_policy.py` | `test_mixed_passenger_fares_sum_as_integers` | docs/business-rules.md；docs/api-examples.md | 整數斷言通過；總額預期失敗 |
| PAYMENT-001 | G1 §4.4／5 | `application/payment_service.py::pay` | `unit/test_services.py` | `test_duplicate_payment_rejected_without_second_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| PAYMENT-002 | G1 §4.4／5 | `application/payment_service.py::pay` | `unit/test_services.py` | `test_payment_success_marks_paid_and_creates_one_matching_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| PAYMENT-003 | G1 §4.4／5 | `application/payment_service.py::pay` | `unit/test_services.py` | `test_duplicate_payment_rejected_without_second_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| ORDER-001 | G1 §4.5／5 | `application/payment_service.py::pay` | `unit/test_services.py` | `test_payment_success_marks_paid_and_creates_one_matching_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| ORDER-002 | G1 §4.5／5 | `application/order_service.py::get` | `unit/test_services.py` | `test_payment_success_marks_paid_and_creates_one_matching_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| MEMBER-001 | B0 §6.1／12 | `application/booking_service.py::create` | `integration/test_members.py` | `test_optional_and_standard_member_preserve_adult_fare` | docs/business-rules.md；docs/api-examples.md | PASS |
| MEMBER-002 | B0 §6.1／12 | `application/member_service.py::get` | `integration/test_members.py` | `test_optional_and_standard_member_preserve_adult_fare` | docs/business-rules.md；docs/api-examples.md | PASS |
| MEMBER-003 | B0 §6.1／12 | `domain/discounts.py::calculate` | `integration/test_members.py` | `test_corporate_member_discount_and_invalid_member_atomic` | docs/business-rules.md；docs/api-examples.md | PASS |
| FARE-005 | B0 §6.2／12 | `domain/discounts.py::calculate` | `integration/test_advance.py` | `test_advance_purchase_thirteen_fourteen_and_fifteen_day_boundary` | docs/business-rules.md；docs/api-examples.md | PASS |
| FARE-006 | B0 §6.2／12 | `domain/discounts.py::calculate` | `integration/test_advance.py` | `test_advance_purchase_thirteen_fourteen_and_fifteen_day_boundary` | docs/business-rules.md；docs/api-examples.md | PASS |
| CHANGE-001 | B0 §6.3／12 | `application/change_booking_service.py::change` | `integration/test_changes.py` | `test_change_rejects_pending_missing_and_insufficient_target_atomically` | docs/business-rules.md；docs/api-examples.md | PASS |
| CHANGE-002 | B0 §6.3／12 | `application/change_booking_service.py::change` | `integration/test_changes.py` | `test_change_rejects_pending_missing_and_insufficient_target_atomically` | docs/business-rules.md；docs/api-examples.md | PASS |
| CHANGE-003 | B0 §6.3／12 | `application/change_booking_service.py::change` | `integration/test_changes.py` | `test_paid_change_transfers_seats_and_records_fare_difference` | docs/business-rules.md；docs/api-examples.md | PASS |
| CHANGE-004 | B0 §6.3／12 | `application/change_booking_service.py::change` | `integration/test_changes.py` | `test_paid_change_transfers_seats_and_records_fare_difference` | docs/business-rules.md；docs/api-examples.md | PASS |
| REFUND-001 | B0 §6.4／12 | `application/refund_service.py::refund` | `integration/test_refunds.py` | `test_pending_refund_is_rejected_without_releasing_reservation` | docs/business-rules.md；docs/api-examples.md | PASS |
| REFUND-002 | B0 §6.4／12 | `application/refund_service.py::refund` | `integration/test_refunds.py` | `test_refund_releases_capacity_once_and_preserves_original_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| REFUND-003 | B0 §6.4／12 | `application/refund_service.py::refund` | `integration/test_refunds.py` | `test_refund_releases_capacity_once_and_preserves_original_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| REFUND-004 | B0 §6.4／12 | `application/refund_service.py::refund` | `integration/test_refunds.py` | `test_refund_releases_capacity_once_and_preserves_original_order` | docs/business-rules.md；docs/api-examples.md | PASS |
| NOTIFY-001 | B0 §12 Notification | `application/payment_service.py::pay` | `integration/test_records.py` | `test_booking_and_payment_append_queryable_audit_events` | docs/business-rules.md；docs/api-examples.md | PASS（補足事件斷言後重驗） |
| NOTIFY-002 | B0 §12 Notification | `application/change_booking_service.py::change` | `integration/test_changes.py` | `test_paid_change_transfers_seats_and_records_fare_difference` | docs/business-rules.md；docs/api-examples.md | PASS（補足事件斷言後重驗） |
| NOTIFY-003 | B0 §12 Notification | `application/refund_service.py::refund` | `integration/test_records.py` | `test_refund_creates_notification_and_audit_records` | docs/business-rules.md；docs/api-examples.md | PASS |
| SEAT-001 | B0 §12 Seat | `application/seat_service.py::plan` | `integration/test_seats.py` | `test_seat_ids_are_unique_and_capacity_failure_leaves_no_assignment` | docs/business-rules.md；docs/api-examples.md | PASS |
| SEAT-002 | B0 §12 Seat | `application/seat_service.py::plan` | `integration/test_seats.py` | `test_seat_ids_are_unique_and_capacity_failure_leaves_no_assignment` | docs/business-rules.md；docs/api-examples.md | 僅驗證唯一；不承諾相鄰（Code／文件審查） |
| AUDIT-001 | B0 §12 Audit | `application/booking_service.py::create` | `integration/test_records.py` | `test_booking_and_payment_append_queryable_audit_events` | docs/business-rules.md；docs/api-examples.md | PASS |
| AUDIT-002 | B0 §12 Audit | `application/payment_service.py::pay、change_booking_service.py::change、refund_service.py::refund` | `integration/test_records.py、test_changes.py` | `test_booking_and_payment_append_queryable_audit_events / test_paid_change_transfers_seats_and_records_fare_difference / test_refund_creates_notification_and_audit_records` | docs/business-rules.md；docs/api-examples.md | PASS（付款／改票／退票事件均有斷言且重驗） |

28 項原 G1 測試 body／assert 保留；只在 `tests/conftest.py` 適配原 T001–T004 Seed、固定非提前優惠 Clock 與無會員上下文，正式學生計價仍走 B0 Bug。新增 16 項使用完整 8 Trip／3 Member Seed。完整測試共 44；正式 B0 首次結果 5 failed／39 passed／1 warning（1.57 秒），隔離副本只修一行學生率後 44 passed／1 warning（0.68 秒）。三項通知／改票 Audit 事件斷言補入新增兩個測試，總數不變，最終重驗正式5 failed／39 passed／1 warning（0.44秒）、診斷44 passed／1 warning（0.32秒），詳見 [Validation Report](01-b0-validation-report.md) 為準。

來源：[G1 指令](../../../docs/instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)、[B0 指令](../../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[已核准方案 A](../../../docs/planning/b0-regression-gate-proposal.md)。

完成條件：36 Rule ID、真實 Code／Test 名稱及文件可核對，5 項預期失敗完整揭露，事件斷言重驗證據補齊；B1 全部原 28 項及 B0 新增測試恢復通過，不刪／弱化／Skip／XFail。
