# Greenfield Rule Traceability Matrix

> 目標讀者：主持人、評估者與產製 Agent。
> 使用時機：G0 檢查與學員 MVP 驗收。
> 前置條件：閱讀 Participant 需求與 Acceptance Criteria。
> 可見性：Evaluation，不發入 Participant Package。

G0 只有 Health 已完成。下表的 Code Area 與 Test 為後續實作／補測試要求；現有 Feature Skip 不代表功能通過。AC ID 使用 AC-G-001 至 AC-G-015。

| Rule ID | Requirement Section | Expected Code Area | Expected Test | Expected Documentation | Validation Method |
|---|---|---|---|---|---|
| TRIP-001 | 需求／Trip | trip_service、routes | 可售／售罄查詢（AC-G-001） | business-rules、api-examples | pytest／API |
| TRIP-002 | 需求／Trip | trip_service、routes | 起訖精確篩選（AC-G-002） | business-rules、api-examples | pytest／API |
| BOOKING-001 | 需求／Booking | booking_service、contracts | 0人拒絕（AC-G-006） | business-rules | pytest／狀態比對 |
| BOOKING-002 | 需求／Booking | booking_service、contracts | 4人成功／5人拒絕（AC-G-007） | business-rules | pytest／API |
| BOOKING-003 | 需求／Booking | booking_service、store | 超容量且不扣座位（AC-G-008） | business-rules | pytest／狀態比對 |
| BOOKING-004 | 需求／Booking | booking_service、store | 成功保留座位（AC-G-009） | business-rules | pytest／狀態比對 |
| BOOKING-005 | 需求／Booking | booking_service、models | PENDING_PAYMENT（AC-G-009） | business-rules | pytest／API |
| FARE-001 | 需求／Fare | fare_policy | 成人全額（AC-G-003） | business-rules | Unit Test |
| FARE-002 | 需求／Fare | fare_policy | 學生75%（AC-G-004） | business-rules | Unit Test |
| FARE-003 | 需求／Fare | booking_service、fare_policy | 成人學生混合總額（AC-G-005） | business-rules | Unit／API |
| FARE-004 | 需求／Fare | fare_policy、contracts | 整數金額（AC-G-005） | business-rules | Unit／API |
| PAYMENT-001 | 需求／Payment | payment_service | 僅待付款可付（AC-G-010／011） | business-rules、api-examples | Unit／API |
| PAYMENT-002 | 需求／Payment | payment_service、gateway | 成功轉PAID、失敗不轉（AC-G-010／014） | business-rules | Unit／狀態比對 |
| PAYMENT-003 | 需求／Payment | payment_service | 重複付款拒絕（AC-G-011） | business-rules | API |
| ORDER-001 | 需求／Order | payment_service、order_service | 成功唯一Order、失敗無Order（AC-G-010／011／014） | business-rules、api-examples | Unit／API |
| ORDER-002 | 需求／Order | payment_service、contracts | Order Amount一致（AC-G-010／012） | business-rules、api-examples | Unit／API |

AC-G-013 驗證資源不存在／404，AC-G-015驗證端到端與Health。完成後補上實際測試檔與名稱，不以本矩陣代替測試紀錄。

## 完成條件

16項規則有需求、預期程式、測試、文件與驗證方法；學員完成實作後逐項取得實際證據，未完成與Skip如實記錄。
