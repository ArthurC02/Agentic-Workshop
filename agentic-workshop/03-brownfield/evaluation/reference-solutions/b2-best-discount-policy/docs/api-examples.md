# B2 API Examples

> 讀者：參與者與Agent。時機：操作驗證與Contract查證。前置：本機App已啟動、乾淨Seed。可見性：Evaluation／Agent Production。

範例base URL為http://127.0.0.1:8000；Windows使用curl.exe。下列ID佔位符應換成回應所得值，範例不是已執行結果。

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/trips"
curl --get "http://127.0.0.1:8000/trips" --data-urlencode "origin=台北" --data-urlencode "destination=台中"
curl "http://127.0.0.1:8000/members/M002"
```

Member回應為 `{"member_id":"M002","member_type":"CORPORATE"}`。班次回傳Trip基本欄位、Base Fare與剩餘座位。

POST /bookings，JSON存為UTF-8 booking.json：

```json
{"trip_id":"T001","member_id":"M001","passengers":[{"passenger_id":"P001","name":"Demo Adult","passenger_type":"ADULT"}]}
```

```bash
curl -X POST "http://127.0.0.1:8000/bookings" -H "Content-Type: application/json" --data-binary @booking.json
curl -X POST "http://127.0.0.1:8000/bookings/<booking_id>/pay"
curl "http://127.0.0.1:8000/orders/<order_id>"
curl "http://127.0.0.1:8000/bookings/<booking_id>"
```

member_id可省略或null。訂票201回傳booking_id/trip_id/passengers/total_fare/status/member_id/seat_ids/fare_difference；付款200回傳order_id/booking_id/amount/payment_status。預設Clock下上述STANDARD成人T001為700，成功付款PAID且唯一Order。另可使用STUDENT；公開學生票規則為Base Fare75%，分析時核對實際值與規則。

POST /bookings/{booking_id}/change，JSON存為change.json：

```json
{"target_trip_id":"T005"}
```

```bash
curl -X POST "http://127.0.0.1:8000/bookings/<booking_id>/change" -H "Content-Type: application/json" --data-binary @change.json
curl "http://127.0.0.1:8000/bookings/<booking_id>/notifications"
curl "http://127.0.0.1:8000/bookings/<booking_id>/audit-log"
curl -X POST "http://127.0.0.1:8000/bookings/<booking_id>/refund"
```

以上改票需先付款，200回傳更新Booking：total_fare為新票價、fare_difference=new-old，原班次座位釋放、新班次座位保留；Order.amount仍是原付款。上述成人例新價750、差額50，不實際補價／退款。退票200回傳refund_id/booking_id/amount，Booking變REFUNDED且釋放座位。

通知為陣列，元素含notification_id/booking_id/event/created_at；Audit陣列含audit_id/booking_id/event/created_at/detail。僅建立紀錄，不發送外部訊息。

錯誤範例：不存在Order回傳404及 `{"error":{"code":"ORDER_NOT_FOUND","message":"Order not found"}}`；其他不存在資源同404、非法人數／容量／狀態等商業衝突409、格式或Enum錯誤422。message文字以實作為準。

## B2 Applied Discount回應與代表組合

Booking建立／查詢／改票回應根層增加 `applied_discounts`，原 `passengers` 不擴充。每個明細含passenger_id／discount_type／rate／amount。T001（700）在非提前購票、STANDARD會員情境，成人與學生各一位：

```json
{"total_fare":1225,"applied_discounts":[{"passenger_id":"P001","discount_type":"FULL_FARE","rate":100,"amount":700},{"passenger_id":"P002","discount_type":"STUDENT","rate":75,"amount":525}]}
```

此片段只展示新增欄位，完整回應仍保留既有Booking欄位。企業成人無提前採CORPORATE95%，企業且提前採ADVANCE85%，學生與提前／企業同時符合仍STUDENT75%，不疊乘。提前資格以可注入Clock控制，預設2030-01-14距2030-01-15僅1天，不應把預設請求當作提前案例。

Change重新計價、更新Applied Discounts並記錄new-old差額；Order維持原付款金額。驗證代表組合須使用乾淨狀態與可控制Clock，不能另增公開切Clock端點。

## 完成條件

可核對API方法、Request／Response欄位、狀態與金流限制，實際輸出作為分析證據，不用範例代替驗證。
