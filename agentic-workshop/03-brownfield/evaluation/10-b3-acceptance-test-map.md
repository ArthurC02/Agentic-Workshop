# B3 Acceptance Test Map 與 Rule 追溯

> 讀者：Evaluation、Facilitator、Agent Production。時機：正式B3驗收。
> 前置：[影響分析](07-b3-expected-impact-analysis.md)、[B3指令 §25](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。可見性：Evaluation內部，不能放Participant Package。

路徑相對[B3 Repository](reference-solutions/b3-group-booking/)。`C`＝tests/integration/test_group_creation.py，`P`＝tests/integration/test_group_payment.py。以下19AC已有完整正式實測 `75 passed, 1 warning in 0.58s`，零failed／skip／xfail，包含第二車廂搜尋；結果以[18報告](18-b3-validation-report.md)／[19JSON](19-b3-validation-evidence.json)為準。

| AC ID | Requirement | 真實Test File／Function | 實際或最終驗收證據 |
|---|---|---|---|
| AC-B3-001 | 4人拒絕 | C::test_group_size_boundaries[four-rejected] | 409 INVALID_GROUP_SIZE，完整ledger snapshot不變 |
| AC-B3-002 | 5人成功 | C::test_group_size_boundaries[five-accepted] | 201 GROUP／pending／5連續席 |
| AC-B3-003 | 20人成功 | C::test_group_size_boundaries[twenty-accepted] | T001全部20席一次保留 |
| AC-B3-004 | 21人拒絕 | C::test_group_size_boundaries[twenty-one-rejected] | 409，無部分寫入 |
| AC-B3-005 | 同車廂連續 | C::test_contiguous_seats_can_cross_rows_inside_one_carriage；test_contiguous_global_ids_cannot_cross_carriage；test_group_searches_second_carriage_when_first_is_full | 同C001 positions3–7可跨row；19–23跨carriage拒；C002精確1–5搜尋成功 |
| AC-B3-006 | 無完整區段整筆拒 | C::test_fragmented_free_seats_do_not_create_partial_group；test_contiguous_global_ids_cannot_cross_carriage | 有足夠總量仍拒無完整區段 |
| AC-B3-007 | 建立失敗不保留 | C::test_group_insufficient_total_capacity_is_atomic；test_group_missing_trip_is_atomic；test_group_invalid_member_is_atomic；碎片／跨車廂與邊界案例 | Booking／Order／Seat／Refund／Audit／Notify／容量snapshot相同 |
| AC-B3-008 | 一次全保留 | C::test_group_size_boundaries[five-accepted]／[twenty-accepted] | 席數與Passenger等量，全同Trip |
| AC-B3-009 | 逐人B2 | C::test_group_mixed_fares_apply_b2_policy_per_passenger | 成人ADVANCE85／學生STUDENT75，三資格不疊加 |
| AC-B3-010 | 個別總和 | 同AC-B3-009 | 595×3＋525×2＝2835，根Applied Discount逐人一致 |
| AC-B3-011 | 成功整筆PAID | P::test_group_success_creates_unique_order_and_rejects_repeat | PAID／全席保留 |
| AC-B3-012 | 唯一Order | 同AC-B3-011 | 一筆3500Order，重複付款409仍一筆 |
| AC-B3-013 | 失敗CANCELLED | P::test_group_failure_cancels_releases_every_seat_and_creates_no_order；test_generic_payment_route_cannot_bypass_group_compensation | group及generic route均取消；取消後retry不成立 |
| AC-B3-014 | 全release | 同AC-B3-013；P::test_cancelled_group_cannot_retry_or_double_release | T001恢復20、無Seat ledger／seat_ids，不重複增加 |
| AC-B3-015 | 失敗無Order | 同AC-B3-013 | orders為空；generic route無繞過 |
| AC-B3-016 | 必要Audit | P::test_group_success_and_failure_record_audit_and_result_notifications | GROUP_BOOKING_CREATED＋success/failure事件 |
| AC-B3-017 | 結果Notification | 同AC-B3-016 | success GROUP_PAYMENT_COMPLETED／failure GROUP_BOOKING_CANCELLED |
| AC-B3-018 | G1/B1/B2全Regression | 原55tests逐檔字節比對＋完整pytest | 原28G1保留；55原＋20新增＝75，完整75passed |
| AC-B3-019 | 文件／API／規則更新 | docs/business-rules.md、api-examples.md、architecture.md／版本與來源；57Rule集合核對 | 數值、同車廂跨row定義、group補償／generic防繞過與程式一致 |

額外防護真實案例：P::test_group_payment_endpoint_rejects_ordinary_booking（BOOKING_NOT_GROUP／不變）、test_paid_group_refund_releases_all_seats_and_group_change_is_rejected（團體change拒409，paid退款全free）、test_reset_restores_group_ledgers_capacity_clock_and_gateway（reset各ledger／capacity／Clock／gateway）。

## 57 Rule 的 Code／Test／Document 定位

原40＝[B0矩陣](04-b0-rule-traceability.md)原36＋[B2 AC Map](09-b2-acceptance-test-map.md)FARE-007–010；沿用B3相同檔案／符號／測試定位，不重編。FARE-007／008→DiscountPolicy.calculate與test_best_discount_policy.py七組；FARE-009／010→test_best_discount_api.py逐人Type／Rate／Amount及改票。原一般Payment失敗保留pending，僅GROUP採取消，不將兩種語意混為一條。

下列新增17項，Code前綴src/smart_ticket/，全部Documentation為本版docs/business-rules.md與api-examples.md；座位／補償結構另見architecture.md。

| Rule ID | Code Area／Symbol | 真實 Test File／Function |
|---|---|---|
| GROUP-001 | application/group_booking_service.py::create | C::test_group_size_boundaries[four-rejected]／[five-accepted] |
| GROUP-002 | 同上 | C::test_group_size_boundaries[twenty-accepted]／[twenty-one-rejected] |
| GROUP-003 | 同上；api/routes.py | C::test_group_size_boundaries[five-accepted]，assigned_seats全同T001 |
| GROUP-004 | application/seat_service.py::plan_group／assignment | C::test_contiguous_seats_can_cross_rows_inside_one_carriage；test_contiguous_global_ids_cannot_cross_carriage；test_group_searches_second_carriage_when_first_is_full |
| GROUP-005 | GroupBookingService.create／SeatService.plan_group | C::test_fragmented_free_seats_do_not_create_partial_group |
| GROUP-006 | GroupBookingService.create／SeatService.reserve | C::test_group_size_boundaries[twenty-accepted] |
| GROUP-007 | GroupBookingService.create | C::test_group_insufficient_total_capacity_is_atomic；missing／invalid／fragment／跨carriage案例 |
| GROUP-PAY-001 | application/payment_service.py::pay／pay_group | P::test_group_success_creates_unique_order_and_rejects_repeat |
| GROUP-PAY-002 | 同上 | P::test_group_failure_cancels_releases_every_seat_and_creates_no_order |
| GROUP-PAY-003 | PaymentService.pay／SeatService.release | 同上；P::test_cancelled_group_cannot_retry_or_double_release |
| GROUP-PAY-004 | PaymentService.pay | P::test_group_failure_cancels_releases_every_seat_and_creates_no_order；test_generic_payment_route_cannot_bypass_group_compensation |
| GROUP-PAY-005 | PaymentService.pay | P::test_group_success_creates_unique_order_and_rejects_repeat |
| GROUP-FARE-001 | GroupBookingService.create／domain/discounts.py::calculate | C::test_group_mixed_fares_apply_b2_policy_per_passenger |
| GROUP-FARE-002 | GroupBookingService.create | 同上，精確2835＝明細總和 |
| GROUP-AUDIT-001 | GroupBookingService.create／PaymentService.pay／AuditService.record | P::test_group_success_and_failure_record_audit_and_result_notifications |
| GROUP-NOTIFY-001 | PaymentService.pay／application/notification_service.py::record | 同上success分支 |
| GROUP-NOTIFY-002 | PaymentService.pay／NotificationService.record | 同上failure分支 |

完成條件：19AC與57Rule在實際程式、測試、文件可定位；正式75包含第二車廂搜尋已通過，零failed／skip／xfail、Warning已記錄，來源／字節保留見[20案例證據](20-b3-case-history-and-delta.md)。本表本身不代替各Gate實測或人員Review。
