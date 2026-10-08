# Greenfield Acceptance Criteria

> 讀者：參與者與其 Coding Agent。時機：計畫、測試及交付核對。前置：閱讀 [需求](02-business-requirements.md)，使用乾淨 Seed 狀態。可見性：Participant。

每項以 API 或核心邏輯測試提供證據；測試開始前重置資料，付款失敗由測試可控制的模擬結果觸發。

| AC ID | Given／When／Then 或明確檢核條件 | 規則 |
|---|---|---|
| AC-G-001 | 無篩選查詢班次，回傳 T001／T002／T004 的基本資訊、票價及剩餘座位；不得回傳售罄 T003。 | TRIP-001 |
| AC-G-002 | 以台北、台中精確篩選，只得到 T001；不符合 Seed 的站名不匹配。 | TRIP-002 |
| AC-G-003 | T001 一位成人成功訂票，總價 700。 | BOOKING-001、FARE-001 |
| AC-G-004 | T001 一位學生成功訂票，總價 525（75%）。 | FARE-002 |
| AC-G-005 | T001 成人與學生各一位，總價 1225；金額為整數。 | FARE-003、FARE-004 |
| AC-G-006 | 0 位旅客被拒絕，無訂票及座位消耗。 | BOOKING-001 |
| AC-G-007 | 5 位旅客被拒絕；4 位旅客且容量足夠可建立。 | BOOKING-002 |
| AC-G-008 | 可用座位僅剩 1 時要求 2 位旅客，被拒絕且座位不變；售罄班次不得訂票。 | BOOKING-003 |
| AC-G-009 | T001 兩位旅客訂票成功，狀態為 `PENDING_PAYMENT`，剩餘座位由 20 變 18，後續查詢反映更新。 | BOOKING-004、BOOKING-005 |
| AC-G-010 | 待付款 Booking 模擬付款成功，狀態變 `PAID`，建立一筆 Order，金額等於訂票總價。 | PAYMENT-001、PAYMENT-002、ORDER-001、ORDER-002 |
| AC-G-011 | 已付款 Booking 再付款被拒絕，不建立第二筆 Order。 | PAYMENT-001、PAYMENT-003、ORDER-001 |
| AC-G-012 | 付款後以 Order ID 查詢，取得正確 Booking ID、金額及付款狀態。 | ORDER-001、ORDER-002 |
| AC-G-013 | 不存在的 Booking 付款與不存在的 Order 查詢，均回傳 404；不存在 Trip 訂票回傳明確錯誤，不消耗座位。 | API 錯誤行為 |
| AC-G-014 | 模擬付款失敗，不建立 Order，也不將 Booking 誤改為 `PAID`。 | PAYMENT-002、ORDER-001 |
| AC-G-015 | 查詢班次→建立訂票→成功付款→查詢 Order 的完整流程可執行；既有 `/health` 保持正常。 | 核心流程 |

## 完成條件

已逐項核對 AC 與 Rule ID（請 Agent 整理成驗收對照表：每條一列，寫通過／失敗／未驗證與依據的測試），保留執行指令、實際結果及未完成項目。不以未執行測試或仍被 Skip 的功能宣稱完成。
