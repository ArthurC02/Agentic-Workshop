# G0 → G1 Delta

> 讀者：主持人、驗收人員與後續教材產製 Agent。時機：G1 審查及後續系統演化之前。前置：閱讀 [G1 README](reference-solution/greenfield-reference-mvp/README.md) 及版本驗證報告。可見性：Facilitator／Evaluation／Agent Production。

## 延續與完成範圍

G0 已提供 FastAPI App、Health、Domain 模型與 Enum、Request／Response Schema、固定四筆 Trip Seed、In-Memory Store、Mock Gateway、依賴組裝及測試骨架。G1 延續這些邊界，完成下列 11 個主要 TODO 工作點：

| 工作點 | 修改區域（相對 G1 目錄） | 規則 |
|---|---|---|
| 1 查詢可售班次與篩選 | `src/smart_ticket/application/trip_service.py` | TRIP-001／002 |
| 2 訂票輸入與容量 | `src/smart_ticket/application/booking_service.py` | BOOKING-001／002／003 |
| 3 總價、座位保留與初始狀態 | 同上 | FARE-003、BOOKING-004／005 |
| 4 成人／學生個別票價 | `src/smart_ticket/domain/fare_policy.py` | FARE-001／002／004 |
| 5 付款狀態驗證 | `src/smart_ticket/application/payment_service.py` | PAYMENT-001／003 |
| 6 付款成功與唯一訂單 | 同上 | PAYMENT-002、ORDER-001／002 |
| 7 訂單查詢及不存在錯誤 | `src/smart_ticket/application/order_service.py` | ORDER-001／002 |
| 8 查詢 Router 串接 | `src/smart_ticket/api/routes.py` | TRIP-001／002 |
| 9 建立訂票 Router 串接 | 同上 | BOOKING-001／005 |
| 10 付款 Router 串接 | 同上 | PAYMENT-001、ORDER-001 |
| 11 訂單查詢 Router 串接 | 同上 | ORDER-001／002 |

其他預期差異包含 App 版本識別為 G1、錯誤狀態固定及完整文件。G0 目錄保留原 Starter 行為，不同步覆蓋為標準答案。

## 原測試與新增邊界

原 G0 8 個功能 Skip（成人票、學生票、Trip 篩選、Booking 建立、4 人上限、剩餘座位、付款流程與 Order 查詢）在 G1 移除 Skip 並執行。新增／補足 Unit 及 Integration 案例驗證 0／5 人、售罄與不足容量、混合票價 1225、付款失敗保持待付款及座位、重複付款、不存在資源、Schema 驗證與 Happy Path。Health 保持通過要求。

「完成」以實際 Code／Test 與 Validation Report 證明，不依靠本 Delta 宣稱已測試。G1 要求無 Fail、Skip 或 XFail；任何未通過結果需揭露。

## 不變與後續演化

固定 Seed、75% 學生票、1–4 人及立即保留座位不變；無前端、外部服務與真實金流。PaymentService 獨立於 BookingService 是原 G0 已存在的可理解分工。後續可新增會員、優惠、改退票、通知、座位配置及 Audit，不在 G1 提前實作。

後續演化前須盤點所有學生票直接／間接斷言與路徑；完整 Regression 與受控 Bug 的預期衝突另由決策紀錄處理，本文件不准許刪弱測試或調整失敗門檻。歷史／Tag已實際建立並以Evaluation Bundle保存；來源與快照比對見G1 docs/case-history.md，不能以版本副本冒充歷史。


## 補充分層及狀態保護差異

G1 新增 `src/smart_ticket/domain/repositories.py` 的 `TicketRepositories` Protocol，讓 Service 依賴結構契約而非具體 Infrastructure 類別；Store 為該契約的 In-Memory Adapter。`tests/unit/test_services.py` 補上 Trip／Booking／Payment／Order Service 隔離案例，並與原 Fare Policy 單元測試及 API 整合測試共同驗證。

Store 增加共享 `RLock`，Application 對訂票／付款狀態提交使用同一鎖，避免同一程序請求交錯造成容量或重複付款競態。Booking 建立以 `deepcopy` 保存旅客資料，避免呼叫者後續修改輸入物件而污染已建立交易。這些保護仍是單程序本機模型，不承諾跨程序或持久化交易。

完整 AC／Rule 對照見 [G1 Acceptance Test Map](06-acceptance-test-map.md)。

## 完成條件

可逐項核對 G0 已有能力、11 TODO、原 8 Skip 及新增邊界，文件與實際變更一致；驗證結果、來源歷史與未完成事項各有正式證據。
