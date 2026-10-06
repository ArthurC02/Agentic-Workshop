# B3 改票與團體適用範圍

> 讀者：主持人、驗收人員與產製Agent。時機：核對售後操作與B3邊界。前置：閱讀主要規則及API。可見性：Evaluation／Agent Production。

一般已付款Booking仍可POST /bookings/{id}/change，body為target_trip_id；目標容量足夠才釋放原座位、保留新座位，更新Booking total與B2 Applied Discounts，記錄new-old Fare Difference，不實際補款／退款。Order.amount維持原付款快照。

團體改票本版明確不支援，409 GROUP_CHANGE_NOT_SUPPORTED，不能走一般流程拆散或破壞團體座位；已付款Group退票仍支援並全釋放。B3因新增Type邊界同步此指南，消除原未描述Fare Difference的舊落差，不改一般改票商業語意。

## 完成條件

一般Change保留、Group Change明確拒絕、Group Refund可用，金額與座位狀態具實際測試與文件證據。
