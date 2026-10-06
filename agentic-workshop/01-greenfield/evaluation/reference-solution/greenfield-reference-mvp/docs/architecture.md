# G1 Architecture

> 讀者：主持人、驗收人員及教材產製 Agent。時機：理解 MVP 與後續演化邊界。前置：閱讀 [README](../README.md)。可見性：Evaluation／Agent Production。

## 分層與依賴

HTTP Router 使用 Request／Response Schema 與 Application Service；Application 協調 Domain Policy、Store 與 Mock Gateway。Domain 不依賴 FastAPI 或 HTTP。Infrastructure 提供資料與模擬付款。API 依賴組裝集中處理，不把票價或座位邏輯放入 Router。

```text
HTTP Request → API / Schema → Application → Domain Model / FarePolicy
                                  ↓
                          InMemoryStore / MockPaymentGateway
```

`DomainResponse` 從 Domain 屬性建立 Response，避免直接把可變 Domain Object 曝露為 HTTP 合約。付款採獨立 `PaymentService`，與 G0 相同拆分，便於測試與後續擴充。

## 核心流程

1. Trip Query 讀取固定 Seed，過濾售罄班次及可選精確起訖站。
2. Booking 驗證 Trip、1–4 人及剩餘座位，依各 Passenger 類型計價後加總，建立待付款交易並保留座位。
3. Payment 驗證待付款狀態，呼叫可控制 Gateway；成功改為已付款並建立唯一 Order。失敗維持待付款與已保留座位，不產生 Order。
4. Order Query 讀取訂單，提供 Booking ID、金額與付款狀態；不存在報錯。

Application 報告 Domain Error，API 統一映射為 HTTP 錯誤；Pydantic 處理格式與 Enum 驗證。測試重置 Store 與 Gateway，不依賴執行順序。

## 為何採 In-Memory

方便一般工程師在短時間理解模組、重置資料及測試，不需要資料庫、外部服務或真實個資。程序重啟資料消失，未提供正式交易資料庫、跨程序鎖或高併發承諾。

## 演化邊界

可在現有 Fare Policy、Application 及 Infrastructure 擴充會員、提前購票、改退票、通知、座位配置與 Audit；這些功能目前均不屬 G1，不提前加入優惠疊加或團體策略。後續版本需保留可追溯的 G1 行為與測試。

## 完成條件

分層與實際模組一致，Domain 不依賴 HTTP，Trip／Booking／Payment／Order 關係可辨識，限制與未實作範圍已明示。
