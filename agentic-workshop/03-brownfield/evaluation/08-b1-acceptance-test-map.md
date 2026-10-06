# B1 Acceptance Test Map

> 讀者：Evaluation、Facilitator、Agent Production。時機：B1 完整驗收。
> 前置：[影響分析](05-b1-expected-impact-analysis.md)、正式 B1 獨立測試輸出。可見性：Evaluation 內部，不放 Participant Package。

本表映射 [B1 指令 §8](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md) 七項 AC，已依正式B1獨立環境實測与檔案比對取得證據，完整結果見12-b1-validation-report.md。Code／Test 路徑相對 [B1 Repository](reference-solutions/b1-student-fare-fixed/)。

| AC ID | Requirement／Rule | Code／Document | Test File／Function 或核對範圍 | 驗收狀態 |
|---|---|---|---|---|
| AC-B1-001 | 單一學生 75%；FARE-002 | src/smart_ticket/domain/fare_policy.py::calculate | tests/unit/test_fare_policy.py::test_student_fare_is_seventy_five_percent；tests/integration/test_features.py::test_student_booking，700→525 | PASS（正式B1實測恢復） |
| AC-B1-002 | 成人不受影響；FARE-001 | FarePolicy.calculate／BookingService.create | tests/unit/test_fare_policy.py::test_adult_fare_is_full_base_fare；tests/integration/test_features.py::test_adult_booking；tests/unit/test_services.py::test_four_passengers_are_accepted | PASS（正式B1實測） |
| AC-B1-003 | 成人＋學生總額；FARE-003／004 | DiscountPolicy.calculate／BookingService.create | tests/unit/test_fare_policy.py::test_mixed_passenger_fares_sum_as_integers；tests/unit/test_services.py::test_successful_mixed_booking_reserves_seats_and_starts_pending；tests/integration/test_features.py::test_mixed_booking_reserves_seats，合計1225 | PASS（正式B1實測恢復） |
| AC-B1-004 | 原 28 G1 正確斷言保留並恢復 | tests/conftest.py；原 test body／assert 比對 | tests/unit/test_fare_policy.py 3＋test_services.py 10＋tests/integration/test_features.py 14＋tests/test_health.py 1＝28 | PASS（原28全通過且body／assert不變） |
| AC-B1-005 | Manifest 全部恢復 | 唯一學生率常數；[Manifest JSON](06-intentional-failure-manifest.json) | 上列學生2＋混合3，五 node ID 全為 passed；不存在額外 B0 新增預期失敗 | PASS（五node均passed） |
| AC-B1-006 | 全套 G1＋B0、零失敗、無Skip／XFail | 本版 requirements／pytest／Fixture | 原28＋新增16＝44；完整 output、退出碼0；禁止用診斷副本代替 | PASS（正式B1實測） |
| AC-B1-007 | 文件75%且與程式一致 | docs/business-rules.md FARE-002／src/smart_ticket/domain/fare_policy.py | 文件與常數／呼叫路徑審查，並交叉核對 AC-B1-001 | PASS（文件75%与正式Source／測試一致） |

新增 16 項原 B0 Regression：以下八檔各兩函數，全部延續且必須通過。`tests/integration/test_members.py`、`test_advance.py`、`test_changes.py`、`test_refunds.py`、`test_records.py`、`test_seats.py`、`test_b0_api.py`、`test_seed.py`。真實函數與 B0 Rule 對應見[36 Rule 矩陣](04-b0-rule-traceability.md)。B1 不增加新政策、不改 `test_corporate_first_match_precedes_more_favorable_advance` 的665第一匹配期待值。

28 是 G1 Regression 數，44 是目前 B1 完整套件數；pytest warnings 另記原因與接受範圍，不能只以總數推定 AC。App版本、獨立環境及API Smoke證據亦須本版取得。

完成條件：七項 AC 均可對到真實 Code／Test／文件與正式 B1 證據；五 Manifest node ID 全恢復、完整44通過，未驗證項不可寫 PASS。
