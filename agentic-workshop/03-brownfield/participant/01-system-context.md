# B0 系統 Context

> 讀者：參與者與其 Agent。時機：第33–39分鐘個人分析。前置：閱讀接手說明及 Repository README。可見性：Participant。

Smart Ticket 提供查詢、訂票、付款、訂單與售後操作。原核心流程延續，新增會員、提前購票優惠、改退票、通知、個別座位與 Audit。

分層為 API／Schemas→Application→Domain；Infrastructure 提供 In-Memory Repository、固定 Seed、Clock 與模擬付款。查詢讀 Trip；訂票驗證旅客與容量、計價並保留座位；付款建立 Order；改退票協調班次容量與紀錄；相關事件留下通知及 Audit。

請閱讀架構與 ADR 理解歷史取捨，再用公開規則、測試與程式驗證關鍵結論。不要只列檔名：要說明模組責任、依賴與可能影響。

## 完成條件

取得系統與模組摘要、證據來源及資訊缺口，準備填寫個人分析表；此階段不修改程式。
