# 改票與團體適用範圍

一般已付款 Booking 可 POST /bookings/{id}/change，body 為 target_trip_id；目標班次容量足夠才釋放原座位、保留新座位，更新 Booking total 與 Applied Discounts，記錄 new-old Fare Difference，不實際補款／退款。Order.amount 維持原付款快照。

團體改票目前不支援，回 409 GROUP_CHANGE_NOT_SUPPORTED，避免一般流程拆散或破壞團體連續座位；已付款團體退票仍支援並釋放全部座位；也可只取消部分旅客（手續費依出發前天數），部分取消過後不可再整筆退票，見 PCR 規則。

相關規則：CHANGE-001 至 CHANGE-004、REFUND-001 至 REFUND-004，見 [Business Rules](business-rules.md)。
