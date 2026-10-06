# B0 - Brownfield Baseline

> 讀者：工作坊參與者與Coding Agent。時機：統一接手系統與分析。前置：Python 3.13，已取得本版本。可見性：Participant。

Smart Ticket上線12個月後，延續查詢、訂票、付款及Order，新增會員、提前優惠、改退票、通知、座位與Audit。先理解與分析，不立即修改。

## 安裝、啟動與測試

在本目錄操作：

```bash
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn smart_ticket.main:app --app-dir src --reload
pytest -q
```

Windows PowerShell：`.\.venv\Scripts\Activate.ps1`；啟用受限時可直接執行 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`、`.\.venv\Scripts\python.exe -m uvicorn smart_ticket.main:app --app-dir src --reload` 與 `.\.venv\Scripts\python.exe -m pytest -q`。

目前有若干測試失敗，需分析是否具有共同原因；記錄真實失敗與非零exit，不把它描述為全套通過。既有Starlette／AnyIO相容性Warning需保留紀錄；如有其他Warning也應核實原因。不得刪弱測試、改正確期待值或以Skip／XFail隱藏。

## API 一覽

| API | 用途 |
|---|---|
| GET /health | 健康檢查 |
| GET /trips | 可售班次及精確起訖篩選 |
| POST /bookings | 一般1–4人訂票；member_id可選 |
| POST /bookings/{booking_id}/pay | 模擬付款 |
| GET /orders/{order_id} | 付款Order查詢 |
| GET /bookings/{booking_id} | 訂票與最新狀態 |
| GET /members/{member_id} | 固定會員資料 |
| POST /bookings/{booking_id}/change | 已付款改票，body為target_trip_id |
| POST /bookings/{booking_id}/refund | 已付款退票 |
| GET /bookings/{booking_id}/notifications | 本機通知紀錄 |
| GET /bookings/{booking_id}/audit-log | 本機稽核紀錄 |

不存在資源404、商業規則409、Pydantic格式驗證422。操作範例見 [API](docs/api-examples.md)，規則見 [Business Rules](docs/business-rules.md)。

## 資料與限制

In-Memory only，重啟重置全部資料；測試重置亦清除Booking、Order、座位、Refund、Notification、Audit、Clock與Gateway。八班Seed出發日固定2030-01-15，Clock.today預設2030-01-14且可注入，不依賴實際當日；會員M001/M003為STANDARD、M002為CORPORATE。

無前端、登入、外部服務或真實金流。一般座位配置不保證相鄰；金額整數。改票記錄Fare Difference但不補款／退款，Order.amount保留原付款快照；退款只建立本機紀錄。通知不寄Email／簡訊，Audit不要求驗證使用者身分。

文件與ADR提供Context，重要結論仍需程式與測試交叉驗證。閱讀 [架構](docs/architecture.md) 與 [版本歷史](docs/version-history.md) 後完成個人分析與小組Shared Context。

## 完成條件

確認版本、環境、模組與測試證據，形成可追查分析；後續僅依已發放任務及核准計畫修改。
