# G1 - Greenfield Reference MVP

> 讀者：主持人、驗收人員與教材產製 Agent。時機：核對完整 MVP 或作為後續演化起點。前置：Python 3.13，於本目錄操作。可見性：Evaluation／Agent Production，不提供學員整份答案。

Smart Ticket 的標準 MVP：查詢班次、1–4 人訂票、模擬付款及訂單查詢。採本機固定 Seed、In-Memory 資料與可控制的 Mock Payment Gateway，不連線外部 API。

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

測試必須實際執行並保留報告，G1 要求無 Fail、Skip 或 XFail；本 README 不代表驗證已通過。

## API

| API | 成功行為 |
|---|---|
| `GET /health` | 200，`{"status":"ok"}`。 |
| `GET /trips` | 200，有可售座位班次；可選起訖站精確篩選。 |
| `POST /bookings` | 201，保留座位、逐位計價，建立 `PENDING_PAYMENT` Booking。 |
| `POST /bookings/{booking_id}/pay` | 200，狀態 `PAID`，建立唯一 Order。 |
| `GET /orders/{order_id}` | 200，訂單與付款資訊。 |

資源不存在回傳 404；商業規則衝突（人數、容量、付款狀態、付款失敗）回傳 409；Pydantic 請求格式或類型驗證回傳 422。Domain／HTTP 錯誤採 `{"error":{"code":"...","message":"..."}}`；422 保留 FastAPI `detail` 格式。

## 目錄與資料重置

- `src/smart_ticket/api/`：HTTP 路由與依賴組裝。
- `application/`：查詢、訂票、付款與訂單 Use Case。
- `domain/`：模型、狀態與票價政策。
- `infrastructure/`：In-Memory Store、Seed 及模擬付款。
- `schemas/`：Request／Response Contract。
- `tests/`：單元、整合及 Health 測試；`docs/`：架構、規則與 API 範例。

重啟程序重建 Seed，訂票及訂單不持久化。測試透過 `reset_state()` 重置 Store 與 Gateway，各案例使用乾淨狀態；重置不提供對外管理 API。

## 已知範圍限制

無前端、登入、會員、多優惠、改退票、團體訂票或真實付款。金額使用整數；學生票為 75%。付款失敗不建立 Order，Booking 維持 `PENDING_PAYMENT` 且保留原座位；此版本不增加失敗取消或退款流程。In-Memory 模型不提供跨程序資料一致性或正式產品的持久化保障。

文件：[架構](docs/architecture.md)、[商業規則](docs/business-rules.md)、[API 範例](docs/api-examples.md)、[版本歷史](docs/version-history.md)。

## 完成條件

安裝、啟動、Health、OpenAPI、核心流程及完整測試具實際證據，16 項規則可追溯，文件與程式一致；驗收結論以獨立 Validation Report 為準。
