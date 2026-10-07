# API Examples

範例base URL為http://127.0.0.1:8000；Windows使用curl.exe。下列ID佔位符應換成回應所得值，回應內容以實際執行為準。

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/trips"
curl --get "http://127.0.0.1:8000/trips" --data-urlencode "origin=台北" --data-urlencode "destination=台中"
curl "http://127.0.0.1:8000/members/M002"
```

Member回應為 `{"member_id":"M002","member_type":"CORPORATE","points_balance":5000}`。班次回傳Trip基本欄位、Base Fare與剩餘座位。

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

member_id可省略或null。訂票201回傳booking_id/trip_id/passengers/total_fare/status/member_id/seat_ids/fare_difference；付款200回傳order_id/booking_id/amount/payment_status。預設Clock下上述STANDARD成人T001為700，成功付款PAID且唯一Order。另可使用STUDENT；學生票為Base Fare 75%。

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

以上改票需先付款，200回傳更新Booking：total_fare為新票價、fare_difference=new-old，原班次座位釋放、新班次座位保留；Order.amount仍是原付款。上述成人例新價750、差額50，不實際補價／退款。退票200回傳refund_id/booking_id/amount/passenger_ids/fee/created_at（整筆退票 fee 為 0、passenger_ids 為全部旅客），Booking變REFUNDED且釋放座位。

通知為陣列，元素含notification_id/booking_id/event/created_at；Audit陣列含audit_id/booking_id/event/created_at/detail。僅建立紀錄，不發送外部訊息。

錯誤範例：不存在Order回傳404及 `{"error":{"code":"ORDER_NOT_FOUND","message":"Order not found"}}`；其他不存在資源同404、非法人數／容量／狀態等商業衝突409、格式或Enum錯誤422。message文字以實作為準。

## 會員點數折抵

POST /bookings 與 POST /group-bookings 可選填 `redeemed_points`（需 member_id）：

```json
{"trip_id":"T001","member_id":"M001","redeemed_points":200,"passengers":[{"passenger_id":"P001","name":"Demo Adult","passenger_type":"ADULT"}]}
```

201 回應多 `redeemed_points` 與 `payable_amount`，例如 `{"total_fare":700,"redeemed_points":200,"payable_amount":500,...}`；M001 點數立刻變為 1,000。付款 Order.amount 為 500，電子發票 500 → 銷售額 476＋稅額 24。不填或 0 時 `redeemed_points` 為 0、`payable_amount` 等於 `total_fare`。錯誤皆 409：`POINTS_MEMBER_REQUIRED`、`POINTS_INVALID_AMOUNT`、`POINTS_INSUFFICIENT`、`POINTS_EXCEED_LIMIT`。團體付款失敗與退票會歸還點數（Audit `POINTS_RESTORED`）；退款金額為 Order.amount。

## 電子發票

付款時可選填發票資訊（擇一）；不帶 body 則開立一般個人發票：

```json
{"invoice":{"business_id":"12345678","company_name":"範例股份有限公司"}}
```

```json
{"invoice":{"mobile_barcode":"/AB+.-12"}}
```

```bash
curl -X POST "http://127.0.0.1:8000/bookings/<booking_id>/pay" -H "Content-Type: application/json" --data-binary @invoice.json
curl "http://127.0.0.1:8000/orders/<order_id>/invoice"
curl -X POST "http://127.0.0.1:8000/orders/<order_id>/invoice/retry"
```

發票回應含order_id/booking_id/status/invoice_number/attempts/last_error。預設模擬服務商立即開立，付款後即為ISSUED，例如 `{"status":"ISSUED","invoice_number":"AB10000001","attempts":1,"last_error":null}`。統編非8位數字、條碼格式不符、兩者同時提供或統編缺公司名稱回422 `INVALID_INVOICE_INFO`，不扣款。服務商失敗只反映在發票狀態，付款仍200。

## Applied Discount 回應與代表組合

Booking建立／查詢／改票回應根層含 `applied_discounts`，`passengers` 維持三欄。每個明細含passenger_id／discount_type／rate／amount。T001（700）在非提前購票、STANDARD會員情境，成人與學生各一位：

```json
{"total_fare":1225,"applied_discounts":[{"passenger_id":"P001","discount_type":"ADULT","rate":100,"amount":700},{"passenger_id":"P002","discount_type":"STUDENT","rate":75,"amount":525}]}
```

此片段只展示部分欄位，完整回應仍保留既有Booking欄位。企業成人無提前採CORPORATE95%，企業且提前採ADVANCE85%，學生與提前／企業同時符合仍STUDENT75%，不疊乘。提前資格以可注入Clock控制，預設2030-01-14距2030-01-15僅1天，不應把預設請求當作提前案例。

Change重新計價、更新Applied Discounts並記錄new-old差額；Order維持原付款金額。Clock只能在測試中調整，沒有公開的切換端點。

## 團體建立與付款

POST /group-bookings Request同BookingRequest，member_id可選、passengers保持passenger_id/name/passenger_type三欄，實際需5–20位：

```json
{"trip_id":"T006","member_id":"M002","passengers":[{"passenger_id":"GP1","name":"Group Passenger 1","passenger_type":"ADULT"},{"passenger_id":"GP2","name":"Group Passenger 2","passenger_type":"STUDENT"},{"passenger_id":"GP3","name":"Group Passenger 3","passenger_type":"ADULT"},{"passenger_id":"GP4","name":"Group Passenger 4","passenger_type":"ADULT"},{"passenger_id":"GP5","name":"Group Passenger 5","passenger_type":"ADULT"}]}
```

201回傳既有Booking欄位、booking_type=GROUP、applied_discounts，以及assigned_seats陣列；每筆包含booking_id/passenger_id/trip_id/seat_id/carriage_id/row_number/seat_number/position。查詢沿用GET /bookings/{id}。一般Booking type=INDIVIDUAL，原passengers合約不變。

POST /group-bookings/{id}/pay成功200、PAID、唯一Order；模擬失敗409、CANCELLED、全釋放、無Order。通用POST /bookings/{id}/pay遇GROUP也執行相同補償；專用group/pay遇一般Booking回409 BOOKING_NOT_GROUP。付款失敗由測試設定模擬閘道產生，沒有公開切換端點。

4／21人409 INVALID_GROUP_SIZE，容量不足409 INSUFFICIENT_SEATS，無同車廂完整區段409 CONSECUTIVE_SEATS_UNAVAILABLE。不存在資源404、Schema422。Group改票409 GROUP_CHANGE_NOT_SUPPORTED；已付款Group退票可用原refund入口（尚未部分取消過時）。

Group建立Audit GROUP_BOOKING_CREATED，付款成功Audit／Notify GROUP_PAYMENT_COMPLETED，付款失敗Audit GROUP_PAYMENT_FAILED與Notify GROUP_BOOKING_CANCELLED。失敗仍留必要本機紀錄，不發外部訊息。

## 團體部分取消

已付款、未折抵點數的團體可取消部分旅客：

```json
{"passenger_ids":["P0"]}
```

```bash
curl -X POST "http://127.0.0.1:8000/group-bookings/<booking_id>/cancel-passengers" -H "Content-Type: application/json" --data-binary @cancel.json
curl "http://127.0.0.1:8000/bookings/<booking_id>/refunds"
```

200 回傳這次的退款紀錄，例如 6 位成人（T001，Order.amount 4,200）在預設 Clock（出發前 1 天，30%）取消 1 位：`{"refund_id":"...","booking_id":"...","passenger_ids":["P0"],"fee":210,"amount":490,"created_at":"2030-01-14T09:00:00+08:00"}`。Booking 查詢多 `cancelled_passenger_ids`；`passengers`、`applied_discounts`、`total_fare` 不變（仍是原付款內容），`seat_ids`／`assigned_seats` 只剩有效旅客，其他人座位不變。`GET /bookings/{id}/refunds` 依時間列出該訂票全部退款紀錄（含整筆退票）。

錯誤：一般訂票或有點數折抵 409 `PARTIAL_CANCEL_NOT_SUPPORTED`；非 `PAID` 409 `BOOKING_NOT_REFUNDABLE`；出發當日或之後 409 `REFUND_WINDOW_CLOSED`；旅客不屬於此訂票 404 `PASSENGER_NOT_FOUND`；已取消 409 `PASSENGER_ALREADY_CANCELLED`；剩 1–4 人 409 `GROUP_BELOW_MINIMUM`；清單為空或重複 422 `INVALID_PASSENGER_IDS`。任何錯誤都不留下變更。部分取消過的團體不可再用整筆退票（409 `BOOKING_NOT_REFUNDABLE`）。成功時 Audit 與通知 `PASSENGERS_CANCELLED`，detail 例如 `passenger_ids=P0 refund=490 fee=210`。不呼叫付款閘道、不開立折讓。
