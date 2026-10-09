# B3 - Group Booking

> 讀者：主持人、驗收人員與教材產製 Agent。時機：驗證B3團體、連續座位及付款補償。前置：Python 3.13，閱讀已核准B3任務與已驗收B2。可見性：Evaluation／Agent Production，不供 Participant。

Smart Ticket上線12個月後，延續查詢、訂票、付款及Order，新增會員、提前優惠、改退票、通知、座位與Audit。本版本延續B2逐旅客最有利單一優惠，新增5–20人團體、同車廂完整連續區段與付款失敗補償，原一般能力保留。

## 安裝、啟動與測試

在本目錄操作，建議使用 Python 3.13。先建立並啟用虛擬環境（venv）：

- macOS／Linux：`python3.13 -m venv .venv`，再 `source .venv/bin/activate`。
- Windows：建議用 `py -3.13 -m venv .venv` 建立。Git Bash 用 `source .venv/Scripts/activate` 啟用；PowerShell 用 `.venv\Scripts\Activate.ps1` 啟用。

啟用後執行：

```bash
python --version
python -m pip install -r requirements.txt
python -m uvicorn smart_ticket.main:app --app-dir src --reload
python -m pytest -q
```

也可以跳過啟用，直接呼叫虛擬環境裡的 Python（PowerShell 執行原則擋下啟用時也這樣做）：Windows 用 `.venv\Scripts\python.exe -m pytest -q`（Git Bash 寫 `.venv/Scripts/python.exe`），macOS／Linux 用 `.venv/bin/python -m pytest -q`；安裝與啟動指令同理，把開頭的 `python` 換掉即可。

本版本完整測試預期全部通過、無 Skip／XFail 或未知失敗；實際結果與 exit code 以 B3 Validation Report 為準。既有Starlette／AnyIO相容性Warning需保留紀錄；如有其他Warning也應核實原因。不得刪弱測試、改正確期待值或以Skip／XFail隱藏。

## API 一覽

| API | 用途 |
|---|---|
| POST /group-bookings | 團體5–20人、完整連續區段才建立 |
| POST /group-bookings/{booking_id}/pay | 團體付款成功唯一Order；失敗取消與全釋放 |
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

Booking回應根層新增 `applied_discounts`，每筆包含 `passenger_id`、`discount_type`、`rate`、`amount`；原 `passengers` 三欄保持不變。折扣文件已同步最低rate政策，同步通知仍保留，已新增5–20人團體訂票與同車廂連續座位。

## 資料與限制

In-Memory only，重啟重置全部資料；測試重置亦清除Booking、Order、座位、Refund、Notification、Audit、Clock與Gateway。八班Seed出發日固定2030-01-15，Clock.today預設2030-01-14且可注入，不依賴實際當日；會員M001/M003為STANDARD、M002為CORPORATE。

無前端、登入、外部服務或真實金流。一般座位配置不保證相鄰；金額整數。改票記錄Fare Difference但不補款／退款，Order.amount保留原付款快照；退款只建立本機紀錄。通知不寄Email／簡訊，Audit不要求驗證使用者身分。

文件與ADR提供Context，重要結論仍需程式與測試交叉驗證。閱讀 [架構](docs/architecture.md) 與 [版本歷史](docs/version-history.md) 核對B2→B3團體能力與既有政策保留。

## B3座位與交易邊界

Booking回應含booking_type（INDIVIDUAL／GROUP）、assigned_seats幾何明細及原applied_discounts。Group建立201；付款成功200、PAID與單一Order，失敗409、CANCELLED、全釋放且無Order。通用付款入口遇GROUP也遵守補償；一般訂票付款失敗仍pending保留座位。

維持B2八班容量，S001–S020映射C001 Position1–20（5排×4座）；沒有將所有班次改為40可售座。T00120座可容20人，T00618座不足20人。Group改票409 GROUP_CHANGE_NOT_SUPPORTED；已付款團體退票仍支援且全釋放。

## 完成條件

確認逐旅客最有利、不疊加、Applied Discount明細、改票一致且完整Regression通過；保留其餘商業規則、API 與既有能力，誠實記錄實際驗證與限制。
