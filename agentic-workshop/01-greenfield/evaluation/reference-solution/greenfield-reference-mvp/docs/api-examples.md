# G1 API Examples

> 讀者：主持人、驗收人員與教材產製 Agent。時機：API Smoke Test 與示範。前置：App 在 `http://127.0.0.1:8000` 啟動、資料為乾淨 Seed。可見性：Evaluation／Agent Production。

以下為操作及預期範例，不是已執行驗證結果。請從回應取得實際 Booking／Order ID，不使用範例佔位符作為真實 ID。

## 查詢班次

```bash
curl "http://127.0.0.1:8000/trips"
curl --get "http://127.0.0.1:8000/trips" --data-urlencode "origin=台北" --data-urlencode "destination=台中"
```

第二個請求只回傳 T001；第一個不回傳 T003。回應為 Trip 陣列，含 `trip_id`、起訖站、出發／抵達時間、`base_fare` 及 `available_seats`。

## 成人加學生訂票

`POST /bookings`，Content-Type 為 `application/json`：

```json
{
  "trip_id": "T001",
  "passengers": [
    {"passenger_id": "P001", "name": "Demo Adult", "passenger_type": "ADULT"},
    {"passenger_id": "P002", "name": "Demo Student", "passenger_type": "STUDENT"}
  ]
}
```

```bash
curl -X POST "http://127.0.0.1:8000/bookings" -H "Content-Type: application/json" --data-binary @booking.json
```

先把上述 JSON 儲存為 UTF-8 `booking.json`。Windows PowerShell 使用 `curl.exe` 避免別名差異。

預期 201，`total_fare` 1225、`status` 為 `PENDING_PAYMENT`，含新 `booking_id` 與旅客；T001 座位由 20 變 18。

## 模擬付款與查詢 Order

```bash
curl -X POST "http://127.0.0.1:8000/bookings/<booking_id>/pay"
curl "http://127.0.0.1:8000/orders/<order_id>"
```

付款預期 200，回傳 `order_id`、`booking_id`、`amount: 1225`、`payment_status: "SUCCESS"`。接著以回傳 Order ID 查詢，資訊相同；再對同一 Booking 付款應回傳 409，不建立另一筆 Order。

## 錯誤範例

```bash
curl "http://127.0.0.1:8000/orders/DOES-NOT-EXIST"
```

預期 404，結構如下；`message` 文字以實際實作為準：

```json
{"error":{"code":"ORDER_NOT_FOUND","message":"Order not found"}}
```

不存在 Trip／Booking 同為 404；0／5 人、容量不足、重複付款或模擬付款失敗為 409。缺少必要欄位或不支援的 `passenger_type` 為 422，採 FastAPI `detail` 回應。付款失敗由可注入 Mock 測試，不提供生產付款或任意外部切換端點。

## 完成條件

核心 Happy Path、查詢篩選、金額、座位與錯誤狀態均以實際呼叫核對，ID 從真實回應取得，證據存入驗證報告。
