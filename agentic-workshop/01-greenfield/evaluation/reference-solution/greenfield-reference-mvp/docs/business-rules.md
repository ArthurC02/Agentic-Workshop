# G1 Business Rules

> 讀者：主持人、驗收人員及教材產製 Agent。時機：需求核對與 Rule Traceability。前置：閱讀 [架構](architecture.md)。可見性：Evaluation／Agent Production。

以下 16 項規則在 G1 全部適用，要求完整實作；「適用」不等於此文件宣稱測試已通過。實際 Code／Test 對應與驗收證據由 Evaluation Matrix 與 Validation Report 記錄。

| Rule ID | G1 規則 | 適用狀態 |
|---|---|---|
| TRIP-001 | 查詢只回傳至少一個可售座位的班次。 | 適用 |
| TRIP-002 | 起訖站可選篩選，提供時精確符合 Seed 站名。 | 適用 |
| BOOKING-001 | 至少一位旅客。 | 適用 |
| BOOKING-002 | 單筆最多 4 位旅客。 | 適用 |
| BOOKING-003 | 旅客數不超過班次剩餘座位。 | 適用 |
| BOOKING-004 | 建立成功立即保留座位。 | 適用 |
| BOOKING-005 | 新訂票為 `PENDING_PAYMENT`。 | 適用 |
| FARE-001 | 成人 Base Fare 100%。 | 適用 |
| FARE-002 | 學生 Base Fare 75%。 | 適用 |
| FARE-003 | 個別票價加總為 Booking Total Fare。 | 適用 |
| FARE-004 | 金額採整數，不處理小數或幣別換算。 | 適用 |
| PAYMENT-001 | 只有待付款訂票可付款。 | 適用 |
| PAYMENT-002 | 成功後改為 `PAID`。 | 適用 |
| PAYMENT-003 | 同一訂票不重複付款。 | 適用 |
| ORDER-001 | 付款成功建立唯一 Order。 | 適用 |
| ORDER-002 | Order Amount 等於訂票總價。 | 適用 |

Seed：T001 台北→台中 700／20 座、T002 台北→高雄 1500／8 座、T003 台中→高雄 800／0 座、T004 高雄→台北 1500／12 座。T003 不出現在可售查詢。T001 成人＋學生總價 1225；學生一人 525。

付款失敗不建立 Order、不改為 `PAID`；保留待付款與原保留座位。Mock 結果由測試控制，不採隨機成功／失敗。不存在資源 404，商業規則衝突 409，Request 型別／Enum 錯誤 422。

## 完成條件

16 Rule ID 語意一致，實作與測試對照可追查；任何差異須揭露，不以此規則表取代實際驗證。
