# Greenfield Business Requirements

> 讀者：參與者與其 Coding Agent。時機：Plan 與需求核對。前置：閱讀 [任務](01-mission-brief.md)，已取得 Starter Repository。可見性：Participant。

## MVP 與 API

| API | 要求 |
|---|---|
| `GET /trips` | 可選 `origin`、`destination` 精確篩選；未提供時列出所有有可售座位班次。回傳班次基本資訊、票價、剩餘座位。 |
| `POST /bookings` | 指定 `trip_id` 及 1–4 位旅客，支援 `ADULT`／`STUDENT`；驗證班次存在與容量，逐位計價並建立待付款訂票、保留座位。 |
| `POST /bookings/{booking_id}/pay` | 使用預設成功的 Mock Payment Gateway；成功改為已付款並建立唯一 Order；拒絕重複付款。 |
| `GET /orders/{order_id}` | 回傳 Booking ID、金額及付款狀態；不存在回傳 404。 |

`GET /health` 已提供，不需修改。不存在的 Booking 應回傳 404；無效請求回傳明確錯誤。付款測試可控制失敗結果，不使用隨機失敗；失敗不得建立 Order 或錯誤標為已付款。

## 商業規則

| Rule ID | 規則 |
|---|---|
| TRIP-001 | 只回傳至少有一個可售座位的班次。 |
| TRIP-002 | 起訖站篩選可選；提供時精確符合 Seed 站名。 |
| BOOKING-001 | 至少一位旅客。 |
| BOOKING-002 | 單筆最多 4 位旅客。 |
| BOOKING-003 | 旅客數不得超過班次剩餘座位。 |
| BOOKING-004 | 成功建立後立即保留對應座位數。 |
| BOOKING-005 | 新訂票狀態為 `PENDING_PAYMENT`。 |
| FARE-001 | 成人為 Base Fare 的 100%。 |
| FARE-002 | 學生為 Base Fare 的 75%。 |
| FARE-003 | 逐位旅客計價後加總為 Booking Total Fare。 |
| FARE-004 | 所有金額採整數，不處理小數與幣別換算。 |
| PAYMENT-001 | 只有 `PENDING_PAYMENT` Booking 可付款。 |
| PAYMENT-002 | 成功後狀態為 `PAID`。 |
| PAYMENT-003 | 同一 Booking 不得重複付款。 |
| ORDER-001 | 付款成功後建立唯一 Order。 |
| ORDER-002 | Order Amount 等於 Booking Total Fare。 |

## 固定 Seed Data

| Trip ID | 起站 | 訖站 | Base Fare | 初始可售座位 |
|---|---|---|---:|---:|
| T001 | 台北 | 台中 | 700 | 20 |
| T002 | 台北 | 高雄 | 1500 | 8 |
| T003 | 台中 | 高雄 | 800 | 0 |
| T004 | 高雄 | 台北 | 1500 | 12 |

範例時間固定，不依賴活動當日。測試須有乾淨狀態，不互相消耗座位。

## 範圍與完成條件

使用本機資料及模擬付款；不需要前端、登入、會員、額外優惠、改退票、外部 API、雲端或真實個資。保留現有分層，商業規則不寫在處理 API 請求的入口層。

完成核心四 API、[驗收條件](03-acceptance-criteria.md)、測試與文件；未完成項目需如實記錄於交付摘要。
