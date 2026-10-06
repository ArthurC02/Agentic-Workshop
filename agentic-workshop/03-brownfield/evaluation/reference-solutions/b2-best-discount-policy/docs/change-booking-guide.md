# 改票使用指南

> 讀者：參與者與Agent。時機：了解一般改票。前置：已付款Booking與目標Trip存在。可見性：Evaluation／Agent Production。

以POST /bookings/{booking_id}/change提供target_trip_id。一般改票保留旅客數，目標需有足夠座位；成功時釋放原班次座位、保留新班次座位。此本機示例不處理金額差異，不執行補款或退款。

改票限已付款交易，無效狀態或容量不足回傳商業錯誤；可透過Booking、Notification及Audit紀錄查閱結果。

## 完成條件

能執行改票並查閱交易狀態；重要行為另以規則、測試與程式交叉確認。
