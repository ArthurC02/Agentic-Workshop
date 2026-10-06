# G0 架構

> 讀者：參與者與 Coding Agent。
> 使用時機：提出計畫前。
> 前置條件：閱讀任務需求與 README。

`src/smart_ticket/main.py` 建立 App、Health 與錯誤 Handler；`api/` 接收 HTTP 與依賴組裝，`schemas/` 定義 Request／Response，`application/` 描述 Use Case，`domain/` 定義模型與票價 Policy，`infrastructure/` 提供本機資料與付款模擬。Domain 不依賴 FastAPI。

資料狀態集中於 InMemoryStore，包含 Trip、Booking、Order。`reset_state()` 重置 Store 與 Gateway；每個測試前後都呼叫，避免互相污染。Seed 日期固定，不依賴今日日期；資料僅供虛構案例。

依賴方向為 API → Application → Domain；Application 注入輕量 In-Memory adapter。MockPaymentGateway 預設成功，測試可設定 `next_result` 為 `PaymentStatus.FAILED`；付款 Use Case 仍待實作。

四個業務 Router 明確回應 501，Service 以 NotImplementedError 標示未完成。請依需求完成服務並建立映射，保持 Router 輕量。

## 完成條件

說明模組責任與資料生命週期，保持輕量分層、固定本機資料及可重複測試。