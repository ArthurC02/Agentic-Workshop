# 預期 Greenfield MVP 輪廓

> 讀者：Facilitator。時機：答疑、進度觀察及快速驗收。
> 前置：閱讀 Participant 需求／AC 與 [G0 指令](../../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)。
> 可見性：Facilitator 內部，不提供參考解答或完整實作。

| API | 核心行為 |
|---|---|
| `GET /health` | 200，`{"status":"ok"}` |
| `GET /trips` | 僅可售座位大於零；Origin／Destination 可選、精確符合 Seed 站名 |
| `POST /bookings` | 1–4 人且座位足夠；成功立即保留座位、PENDING_PAYMENT、逐人計價加總 |
| `POST /bookings/{booking_id}/pay` | 僅 PENDING_PAYMENT 可付；成功 PAID 且唯一 Order，重複付款拒絕 |
| `GET /orders/{order_id}` | 讀取已建立 Order；金額等於 Booking 總額 |

分層：API 處理 HTTP／Schema／錯誤轉換；Application 串接 Trip 查詢、Booking、Payment、Order 使用案例；Domain 提供 PassengerType、BookingStatus、PaymentStatus、Trip／Booking／Order 與 Fare Policy；Infrastructure 提供 In-Memory Repository、固定 Seed／Reset 與 Mock Payment。Domain 不依賴 FastAPI 或測試框架。

預期測試：Health、Fare 單元測試（成人 100%、學生 75%、混合加總）、Booking 人數／座位邊界、可售 Trip／篩選、建立與付款至 Order 的整合流程、重複付款、不存在 ID，以及建立／付款失敗的狀態與座位一致性。每個測試前 Reset；不以改測試預期換取通過。

可接受的簡化：固定範例日期、整數金額、In-Memory 儲存、Mock 付款、無身份驗證與前端；依標準輕量分層，不為工作坊增加複雜架構。不可偏離：學生 75%、每筆最多 4 人、成功保留座位、付款狀態、唯一 Order、精確站名篩選及錯誤一致性；不得加入會員、早鳥、團體或其他後續功能。

快速驗收順序：

1. 請學員的 Agent 啟動伺服器，瀏覽器開 /health 與 /docs；看 Agent 附上的測試指令與驗收對照表。
2. Reset 後在 /docs 查可售 Trip：T003 不出現；站名篩選符合 Seed。
3. T001 成人加學生總額應為 1,225；建立後保留 2 座、狀態 PENDING_PAYMENT。
4. 成功付款後為 PAID，唯一 Order 金額 1,225；重複付款不新增 Order。
5. 在驗收對照表找 0／5 人、座位不足及付款失敗的列，或在 /docs 試；未跑項目記未驗證，不推定成功。
6. 對照業務規則、API 範例，以及 `notes/greenfield.md` 裡的每步變更審查答案與人機分工摘要。

G0 是可啟動但未完成的骨架，Feature Skip 須有原因與 TODO。學員提交的完整 MVP 應移除已完成 Feature Skip；部分交付依實測標示完成度，不以 G0 骨架通過代表 MVP 已完成。

完成條件：主持能核對 API、分層、測試與允許簡化；Quick Check 不更改需求，結果與證據一致，未完成／未驗證項明確。分層與測試結構是主持判斷用，不要求學員讀程式說明。
