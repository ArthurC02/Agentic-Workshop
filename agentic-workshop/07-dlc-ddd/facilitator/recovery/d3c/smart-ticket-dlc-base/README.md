# Smart Ticket Platform

Smart Ticket 是一套台灣城際列車訂票後端服務，已上線約 12 個月。目前提供班次查詢、一般訂票（1–4 人）、團體訂票（5–20 人、同車廂連續座位）、模擬付款與 Order、會員與優惠、改票、退票、座位配置、通知紀錄與稽核紀錄。

## 安裝、啟動與測試

需要 Python 3.13。在本目錄操作：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn smart_ticket.main:app --app-dir src --reload
pytest -q
```

Windows PowerShell：`.\.venv\Scripts\Activate.ps1`；若無法啟用 venv，可直接執行 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`、`.\.venv\Scripts\python.exe -m uvicorn smart_ticket.main:app --app-dir src --reload` 與 `.\.venv\Scripts\python.exe -m pytest -q`。

本專案不需要 `pip install -e .`；測試透過 `pyproject.toml` 的 `pythonpath = ["src"]` 載入程式。測試應全部通過，沒有警告。

## API 一覽

| API | 用途 |
|---|---|
| GET /health | 健康檢查 |
| GET /trips | 可售班次，可依起訖站精確篩選 |
| POST /bookings | 一般 1–4 人訂票；member_id 可選；會員可選填 redeemed_points 折抵 |
| POST /bookings/{booking_id}/pay | 付款；body 可選填發票資訊 `{"invoice": {...}}` |
| GET /bookings/{booking_id} | 訂票與最新狀態 |
| GET /orders/{order_id} | 付款 Order 查詢 |
| GET /members/{member_id} | 會員資料（含點數餘額） |
| POST /bookings/{booking_id}/change | 已付款改票，body 為 target_trip_id |
| POST /bookings/{booking_id}/refund | 已付款退票（整筆全額；部分取消過的團體不可） |
| GET /bookings/{booking_id}/refunds | 該訂票的全部退款紀錄 |
| POST /group-bookings | 團體 5–20 人、同車廂完整連續座位；可選填 redeemed_points |
| POST /group-bookings/{booking_id}/pay | 團體付款；失敗時取消並釋放全部座位 |
| POST /group-bookings/{booking_id}/cancel-passengers | 已付款團體取消部分旅客，依出發前天數收手續費後退款 |
| GET /orders/{order_id}/invoice | 電子發票狀態（PENDING／ISSUED／FAILED、發票號碼） |
| POST /orders/{order_id}/invoice/retry | 重試開立電子發票（排程或維運使用） |
| GET /bookings/{booking_id}/notifications | 通知紀錄 |
| GET /bookings/{booking_id}/audit-log | 稽核紀錄 |

不存在的資源回 404、違反商業規則回 409、格式驗證錯誤回 422。操作範例見 [API 範例](docs/api-examples.md)，商業規則見 [Business Rules](docs/requirements/business-rules.md)。

## 文件

- [商業規則](docs/requirements/business-rules.md)
- [優惠政策](docs/requirements/discount-overview.md)
- [改票與團體適用範圍](docs/requirements/change-booking-guide.md)
- [架構](docs/architecture.md)
- [API 範例](docs/api-examples.md)
- [產品演進](docs/version-history.md)
- 架構決策：[docs/adr/](docs/adr/)

## 資料與限制

資料全部存在記憶體，重啟即重置；測試之間也會重置 Booking、Order、座位、Refund、Notification、Audit、Clock 與 Gateway。

- 八個班次的出發日固定為 2030-01-15；系統 Clock 的「今天」預設為 2030-01-14，可在測試中調整（`clock` fixture），不依賴實際日期。
- 會員：M001（STANDARD，點數 1,200）、M002（CORPORATE，點數 5,000）、M003（STANDARD，點數 0）。訂票時可用點數折抵（1 點 = 1 元，100 點起、100 點為單位、不超過優惠後總額 30%）；尚無累積方式。
- 付款透過本機模擬閘道（`MockPaymentGateway`）。
- 電子發票透過 `InvoiceIssuer` Port 開立；目前接的是不連網的模擬服務商（`SimulatedEInvoiceProvider`），測試可排入任意回應代碼、逾時與停機。發票失敗不影響付款。
- 金額一律為整數（新台幣元）。
- 改票記錄 Fare Difference，但不補款也不退差額；Order.amount 保留原付款金額。
- 整筆退票的退款金額為 Order.amount（實付金額），折抵的點數歸還會員，建立一筆本機 Refund Record。已付款且未折抵點數的團體可以部分取消旅客（手續費 10%／20%／30% 依出發前天數，有效旅客須 ≥ 5 人或全部取消），每次建立一筆 Refund Record；部分取消過就不能再整筆退票。退款都不呼叫付款閘道。
- 通知只建立紀錄，不寄送 Email／簡訊；Audit 不驗證使用者身分。
- 一般訂票不保證相鄰座位；一般訂票付款失敗時維持 PENDING_PAYMENT 並保留座位，團體付款失敗則取消並釋放全部座位。
- 座位 S001–S020 對應車廂 C001 的 Position 1–20（5 排 × 4 座），S021 起為下一車廂。T001 有 20 座、T006 有 18 座。
- 團體訂票不支援改票（409 GROUP_CHANGE_NOT_SUPPORTED）；已付款團體可整筆退票或部分取消。
