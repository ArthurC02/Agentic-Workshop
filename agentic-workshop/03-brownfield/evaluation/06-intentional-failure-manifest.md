# B0 Intentional Failure Manifest

> 讀者：Evaluation、Facilitator、Agent Production。時機：正式 B0 驗收與 B1 修復後驗證。
> 前置：完整 pytest node ID／traceback、正式與隔離修復副本 Diff。可見性：Evaluation 內部；不得放 Participant Repository／Participant Package。

唯一主任務 Bug：`BUG-B0-001`。學生正確率仍為 75%；正式 B0 的 `src/smart_ticket/domain/fare_policy.py` 單一常數 `STUDENT_FARE_RATE = 85` 造成多層失敗，不是五個 Bug。2026-10-05 使用者「套用」核准[方案 A](../../../docs/planning/b0-regression-gate-proposal.md)：失敗集合完整一致、零非預期，其餘全通過；B1 全部恢復。

## 完整失敗集合

node ID 相對 [B0 Repository](../participant/repository/smart-ticket-b0/)。[機器可讀清單](06-intentional-failure-manifest.json) 為僅含以下五個 node ID 的 JSON 陣列；用集合比對，不只比數量。

| Node ID | Rule／AC | 保留的正確斷言 | 正式 B0 實際值 |
|---|---|---|---|
| `tests/unit/test_fare_policy.py::test_student_fare_is_seventy_five_percent` | FARE-002／AC-G-004 | 學生 700 × 75%＝525 | 595 |
| `tests/unit/test_fare_policy.py::test_mixed_passenger_fares_sum_as_integers` | FARE-003／004、AC-G-005 | 成人＋學生整數合計 1225 | 1295 |
| `tests/unit/test_services.py::test_successful_mixed_booking_reserves_seats_and_starts_pending` | FARE-003、BOOKING-004／005、AC-G-005／009 | 混合 Booking 總額 1225 | 1295 |
| `tests/integration/test_features.py::test_student_booking` | FARE-002／AC-G-004 | HTTP 201，total_fare 525 | HTTP 201，595 |
| `tests/integration/test_features.py::test_mixed_booking_reserves_seats` | FARE-003／004、BOOKING-004／005、AC-G-005／009 | HTTP 201，混合 total_fare 1225 | HTTP 201，1295 |

## 因果與修復證據

1. 直接 Unit：`FarePolicy.calculate` 學生分支以唯一 `STUDENT_FARE_RATE` 計算，成人 700 不受影響。
2. Service：`DiscountPolicy.calculate` 按 member → advance → student → adult 第一匹配；原 G1 fixture 為 member None／出發前一天，因此學生分支呼叫同一 FarePolicy。BookingService.create 逐人加總，525 變 595，混合多 70。
3. HTTP：`api/routes.py::create_booking` → BookingService → DiscountPolicy → FarePolicy；BookingResponse 只序列化總額，不另外計價。兩層 API 金額斷言揭露同一原因。
4. 隔離修復副本只將該常數一行 85 改 75；未修改正式 B0、原 28 項 G1 body／assert 或計價呼叫路徑。44 項全通過，證明全部 Manifest 失敗共同恢復；此副本是因果診斷，不是發放 B1 答案。

主代理提供的首次實測：正式 B0 `5 failed, 39 passed, 1 warning in 1.57s`，pytest exit 1；隔離修復副本 `44 passed, 1 warning in 0.68s`，pytest exit 0。Warning 為既有 AnyIO BlockingPortal alias deprecated 相容警告，須在 Validation Report 記錄。於兩個新增測試補足三個 notification／audit 事件斷言，test 數仍 44；最終重驗及證據以 [B0 Validation Report](01-b0-validation-report.md) 為準。

28 原 G1 測試保留正確斷言；`tests/conftest.py` 只適配原 Seed／固定 Clock／可選 Member，學生仍走正式 Bug。另 16 項測試使用完整 B0 資料，不以 fixture 另設正確學生分支。Source／tests 差異與測試輸出由主代理留存，未將內部影響清單放入 Participant。

## 驗收判定

只在唯一 Bug、實測 failed node ID 集合等於此 JSON 陣列、其餘全部通過、零非預期且其他 Gate 符合時，才能 `PASS AS BROWNFIELD BASELINE`。pytest exit 1 本身不等於通過；任何新增失敗或預期項消失均須重新查因，不能把任意「學生相關」失敗自動接受。新增受影響測試須逐項證明並更新 Manifest。

B1 修復後全部 28 原 G1＋全部 B0 新增測試通過，Manifest 五項全部恢復；無 Skip／XFail，不刪測試、不改正確商業期待值。28 是 Regression 數，44 是目前完整 B0 套件數。

完成條件：JSON／表格 node ID 相同，完整 pytest failed 集合完全一致，單一常數因果及只改一行的全恢復證據可核對，素材保持 Evaluation 隔離。
