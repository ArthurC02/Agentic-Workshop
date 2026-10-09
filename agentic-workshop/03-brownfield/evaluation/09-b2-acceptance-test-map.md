# B2 Acceptance Test Map

> 讀者：Evaluation、Facilitator、Agent Production。時機：B2 完整驗收。
> 前置：[影響分析](06-b2-expected-impact-analysis.md)及正式B2測試輸出。可見性：Evaluation內部，不發Participant。

來源：[B2 指令 §15](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。路徑相對 [B2 Repository](reference-solutions/b2-best-discount-policy/)。2026-10-05正式B2實測 `55 passed, 1 warning in 1.21s`，零failed／skip／xfail；以下測試映射已有實際通過證據，詳見[驗證報告](15-b2-validation-report.md)及[JSON證據](16-b2-validation-evidence.json)。

`U`＝`tests/unit/test_best_discount_policy.py::test_selects_best_single_candidate`，七個param ID逐一列出；`I`＝`tests/integration/test_best_discount_api.py`。Domain Code為`src/smart_ticket/domain/discounts.py::DiscountPolicy.calculate`，Booking／Change Code為`application/booking_service.py::create`／`change_booking_service.py::change`。

| AC ID | Requirement／Rule | 真實 Test File／Function | 期待值／證據 |
|---|---|---|---|
| AC-B2-001 | 成人無優惠100%；FARE-001 | U[adult]；tests/integration/test_features.py::test_adult_booking | ADULT／100／700 |
| AC-B2-002 | 學生75%；FARE-002 | U[student]；tests/unit/test_fare_policy.py::test_student_fare_is_seventy_five_percent | STUDENT／75／525 |
| AC-B2-003 | 提前成人85%；FARE-005 | U[advance]；tests/integration/test_advance.py::test_advance_purchase_thirteen_fourteen_and_fifteen_day_boundary | ADVANCE／85／595，13/14/15天邊界 |
| AC-B2-004 | Corporate成人95%；MEMBER-003 | U[corporate]；tests/integration/test_members.py::test_corporate_member_discount_and_invalid_member_atomic | CORPORATE／95／665 |
| AC-B2-005 | 學生＋提前75%；FARE-008 | U[student-advance] | STUDENT／75／525，不疊乘85% |
| AC-B2-006 | Corporate＋提前85%；FARE-008 | U[corporate-advance]；tests/integration/test_advance.py::test_corporate_advance_uses_best_single_discount | ADVANCE／85／595；此一項由舊第一匹配測試遷移 |
| AC-B2-007 | 三者同時符合75%；FARE-008 | U[all-three]；I::test_mixed_triple_eligibility_exposes_per_passenger_discount_without_stacking | 學生75／525，成人85／595 |
| AC-B2-008 | 不疊加；FARE-007 | U全部七組；I::test_mixed_triple_eligibility_exposes_per_passenger_discount_without_stacking | amount＝Base Fare×單一rate整除100；總額1120 |
| AC-B2-009 | 逐Passenger獨立；FARE-009 | I::test_mixed_triple_eligibility_exposes_per_passenger_discount_without_stacking；I::test_corporate_student_selects_student_rate_even_without_advance | 成人ADVANCE／學生STUDENT；Corporate學生無提前仍75% |
| AC-B2-010 | Fare Result type／rate；FARE-010 | U全部七組；I::test_mixed_triple_eligibility_exposes_per_passenger_discount_without_stacking | Domain三欄與API根層每人四欄精確核對，原Passenger不改 |
| AC-B2-011 | 改票同步政策 | I::test_change_reprices_each_passenger_with_same_policy_and_preserves_paid_order；I::test_failed_change_preserves_fare_discount_and_all_ledgers_atomically | 750基價成人637＋學生562＝1199，差額−26，Order仍1225；失敗無部分變更 |
| AC-B2-012 | B1／G1 Regression通過 | 原28 G1；其餘B1／B0測試；唯一政策遷移見AC-B2-006 | 原28未改body／assert；原44僅一項新規則遷移，新增7＋4＝55；完整實測55 passed，零failed／skip／xfail |
| AC-B2-013 | 折扣文件與Code同步 | docs/business-rules.md、discount-overview.md、api-examples.md、architecture.md／ADR；Code／文件Diff審查 | 政策／規則集合已核對；原文件FULL_FARE名稱誤文未被舊審查發現，依[勘誤](22-b2-documentation-errata.md)採ADULT，不宣稱凍結文件完全同步 |

所有對應檔案與函式已核對，AC Map引用的10個不同函式均存在；Unit七個param ID亦一致。B2 business-rules.md含40個唯一Rule ID，集合完全等於B0原36＋FARE-007–010，AC-B2-013的文件規則集合檢查通過。本表交叉引用正式實測證據，不因param總數推定規則通過。資料Fixture延續固定Clock、完整B0Seed與原G1限定上下文；原本正確學生75%期待不改。既有相容性Warning記於本版報告。

完成條件：13 AC均有真實測試或文件審查證據，正式B2完整執行、收集數與結果可核對，唯一政策遷移可追溯、B1快照保持凍結。AC-B2-013規則集合通過不等於所有文字無誤；本輪以外置勘誤修正使用說明，保留原文件／Tag／Hash。
