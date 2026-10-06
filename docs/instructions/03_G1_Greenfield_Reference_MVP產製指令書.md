# Agentic Software Development Evolution Workshop
# G1 Greenfield Reference MVP 產製指令書

> 目標讀者：負責建立完整 Greenfield 標準實作、驗證素材，以及 Brownfield 演化基線的 Coding Agent
>
> 使用時機：G0 Greenfield Starter Kit 已完成並通過驗證後，開始建立 G1 Reference MVP。
>
> 上位規格：
>
> - `00_Agentic工作坊素材產製總控指令書.md`
> - `01_技術棧與Repository標準指令書.md`
> - `02_Greenfield_Starter_Kit產製指令書.md`

---

## 1. 任務目標

建立 Smart Ticket Platform 的 **G1 Greenfield Reference MVP**，作為以下用途的唯一正式基線：

1. 驗證 G0 Starter Kit 是否能產生合理完整的 MVP。
2. 提供 Facilitator 在 Greenfield 階段快速判斷成果的參考。
3. 提供 Evaluation 自動驗證及規則追溯的標準版本。
4. 作為後續 Brownfield B0 Repository 的演化起點。
5. 作為工作坊環境故障時的 Recovery Repository。

G1 必須是完整、可執行、可測試、可閱讀的標準實作，但不得直接提供給參與者作為 Greenfield 解答。

G1 不是唯一可接受的實作方式。參與者可以採用不同類別、方法或檔案配置，只要符合 API Contract、商業規則與驗收條件。

---

## 2. 可見性與存放位置

G1 屬於 Facilitator / Evaluation / Agent Production 可見內容。

不得放置於 Greenfield Participant 可直接取得的目錄。

建議目錄：

```text
01-greenfield/
├── facilitator/
│   └── 04-expected-mvp-outline.md
└── evaluation/
    ├── reference-solution/
    │   └── greenfield-reference-mvp/
    ├── 04-g1-validation-report.md
    ├── 05-g0-to-g1-delta.md
    └── 06-acceptance-test-map.md
```

Recovery Package 可以在最終打包階段複製 G1，但必須保留權限及目錄隔離，避免工作坊一開始被參與者看到。

---

## 3. 版本識別

G1 必須在以下位置清楚標示版本：

- Repository README。
- `docs/version-history.md`。
- Git Tag 或交付目錄名稱。
- Validation Report。

固定版本名稱：

```text
G1 - Greenfield Reference MVP
```

版本目的：

```text
完整實作查詢班次、建立訂票、模擬付款及查詢訂單的第一版 Smart Ticket Platform。
```

---

## 4. G1 必須完成的功能

### 4.1 Health Check

```text
GET /health
```

預期：

- 回傳 HTTP 200。
- 回傳 `{"status": "ok"}`。
- 不依賴 Repository 狀態或外部服務。

### 4.2 Trip Query

```text
GET /trips
```

支援：

- 無篩選條件查詢。
- `origin` 篩選。
- `destination` 篩選。
- 同時使用 `origin` 與 `destination`。
- 排除 `available_seats == 0` 的班次。

不得：

- 回傳售罄班次。
- 在 Router 內直接操作 Store。
- 將固定 Seed Data 寫死於 Router。

### 4.3 Booking Creation

```text
POST /bookings
```

必須：

- 驗證 Trip 存在。
- 驗證至少一位 Passenger。
- 驗證最多 4 位 Passenger。
- 驗證剩餘座位足夠。
- 依 Passenger Type 個別計價。
- 建立 `PENDING_PAYMENT` Booking。
- 成功後立即保留座位。
- 回傳 Booking ID、狀態、總票價及旅客資訊。

失敗時不得部分扣除座位。

### 4.4 Payment

```text
POST /bookings/{booking_id}/pay
```

必須：

- 驗證 Booking 存在。
- 驗證狀態為 `PENDING_PAYMENT`。
- 呼叫 Mock Payment Gateway。
- 付款成功後將 Booking 改為 `PAID`。
- 建立唯一 Order。
- 回傳 Order 資訊或可供查詢的 Order ID。
- 阻擋重複付款。

Greenfield 的 Mock Payment Gateway 預設成功。測試時必須可注入失敗結果，用於驗證狀態不應被錯誤更新。

### 4.5 Order Query

```text
GET /orders/{order_id}
```

必須：

- 回傳有效 Order。
- 回傳 Booking ID。
- 回傳 Amount。
- 回傳 Payment Status。
- 不存在時回傳 404 及統一錯誤格式。

---

## 5. 固定商業規則

G1 必須完整實作以下規則，且不得自行修改數值或語意。

### Trip Rules

- `TRIP-001`：只回傳至少有一個可售座位的班次。
- `TRIP-002`：Origin 與 Destination 為可選且精確比對的篩選條件。

### Booking Rules

- `BOOKING-001`：每筆訂票至少包含一位旅客。
- `BOOKING-002`：單筆 Greenfield 訂票最多 4 位旅客。
- `BOOKING-003`：旅客數不得超過班次剩餘座位數。
- `BOOKING-004`：成功建立 Booking 後立即保留座位。
- `BOOKING-005`：新 Booking 狀態為 `PENDING_PAYMENT`。

### Fare Rules

- `FARE-001`：成人票為 Base Fare 的 100%。
- `FARE-002`：學生票為 Base Fare 的 75%。
- `FARE-003`：個別旅客票價加總為 Booking Total Fare。
- `FARE-004`：金額使用整數，不處理小數及幣別換算。

### Payment and Order Rules

- `PAYMENT-001`：只有 `PENDING_PAYMENT` Booking 可付款。
- `PAYMENT-002`：付款成功後 Booking 改為 `PAID`。
- `PAYMENT-003`：同一 Booking 不得重複付款。
- `ORDER-001`：付款成功後建立唯一 Order。
- `ORDER-002`：Order Amount 等於 Booking Total Fare。

---

## 6. 固定 Seed Data

G1 必須沿用 G0 Seed Data，不可更改 ID、路線、票價及初始座位：

```text
T001：台北 → 台中，Base Fare 700，可售座位 20
T002：台北 → 高雄，Base Fare 1,500，可售座位 8
T003：台中 → 高雄，Base Fare 800，可售座位 0
T004：高雄 → 台北，Base Fare 1,500，可售座位 12
```

時間欄位必須：

- 合法且固定。
- Arrival Time 晚於 Departure Time。
- 不依賴目前日期。

每個測試必須取得乾淨的 Repository 狀態。

---

## 7. Reference Architecture

G1 採以下依賴方向：

```text
FastAPI Router
  ↓
Application Service
  ↓
Domain Model / Fare Policy
  ↓
Repository Abstraction
  ↓
In-Memory Implementation
```

### 7.1 必要 Domain 類型

至少包含：

- `PassengerType`
- `BookingStatus`
- `PaymentStatus`
- `Trip`
- `Passenger`
- `Booking`
- `Order`
- `FarePolicy`

可以使用 dataclass、Pydantic-independent class 或簡單 Python class，但 Domain 不得依賴 FastAPI。

### 7.2 必要 Application Service

至少包含：

- `TripService`
- `BookingService`
- `OrderService`

Payment 流程可位於 `BookingService` 或獨立 `PaymentService`。若獨立，必須說明此差異不影響 G0 到 G1 的可理解性。

### 7.3 必要 Infrastructure

至少包含：

- Trip Repository。
- Booking Repository。
- Order Repository。
- Mock Payment Gateway。
- Seed Data Loader。
- Test Reset Mechanism。

### 7.4 API Schema

Request / Response Schema 與 Domain Model 分離。

不得直接將可變 Domain Object 暴露為 API Response。

---

## 8. 錯誤處理標準

至少定義下列錯誤碼：

```text
TRIP_NOT_FOUND
BOOKING_NOT_FOUND
ORDER_NOT_FOUND
INVALID_PASSENGER_COUNT
INSUFFICIENT_SEATS
BOOKING_NOT_PAYABLE
PAYMENT_FAILED
```

統一格式：

```json
{
  "error": {
    "code": "BOOKING_NOT_FOUND",
    "message": "Booking not found"
  }
}
```

建議狀態碼：

- Resource Not Found：404。
- 商業規則不成立：409 或 422，整個 G1 必須採一致策略。
- Pydantic Request Validation：FastAPI 標準 422 可以保留。
- Payment Failure：409 或 502 皆可，但必須在文件中固定並測試。

不可回傳 Stack Trace 或內部例外名稱。

---

## 9. 測試套件要求

G1 不得保留任何 Greenfield Feature Test Skip。

### 9.1 Unit Tests

至少包含：

#### Fare Policy

- 成人票為 100%。
- 學生票為 75%。
- T001 一位成人加一位學生總價為 1,225。

#### Booking Service

- 至少一位 Passenger。
- 最多 4 位 Passenger。
- 不足座位時拒絕。
- 建立成功後座位正確扣除。
- 建立失敗時座位不得扣除。
- 新 Booking 狀態正確。

#### Payment Flow

- 待付款 Booking 可付款。
- 付款成功後狀態為 `PAID`。
- 付款成功後建立唯一 Order。
- 重複付款被拒絕。
- 付款失敗時不得建立 Order，也不得將 Booking 改為 `PAID`。

### 9.2 Integration Tests

至少包含：

#### Trip API

- 無條件查詢排除 T003。
- 台北 → 台中只回傳 T001。
- 無符合資料時回傳空陣列，而不是 404。

#### Booking API

- 建立一位成人 Booking。
- 建立成人加學生 Booking 並驗證總價。
- 0 位 Passenger 被拒絕。
- 5 位 Passenger 被拒絕。
- 超過剩餘座位被拒絕。
- 不存在的 Trip 被拒絕。

#### Payment / Order API

- 完整 Happy Path：查詢班次 → 訂票 → 付款 → 查詢 Order。
- 重複付款被拒絕。
- 不存在 Booking 回傳 404。
- 不存在 Order 回傳 404。

### 9.3 測試數量

G1 預期至少 18 個有效測試，建議控制在 18 至 28 個。

不要用大量細碎測試虛增數量。

### 9.4 測試效能

完整 `pytest` 應在一般筆記型電腦上快速完成，目標小於 5 秒，不得依賴網路。

---

## 10. 文件要求

### 10.1 README.md

必須包含：

- G1 版本識別。
- 專案用途。
- Python 版本。
- 安裝、啟動、測試指令。
- API 一覽。
- 主要目錄。
- In-Memory 資料重置說明。
- 已知限制。

### 10.2 `docs/architecture.md`

必須包含：

- 分層責任。
- 依賴方向。
- Trip、Booking、Payment、Order 的主要流程。
- 為何選擇 In-Memory Repository。
- 後續可演化但目前未實作的範圍。

### 10.3 `docs/business-rules.md`

必須完整列出所有 Greenfield Rule ID、規則內容及 G1 適用狀態。

### 10.4 `docs/api-examples.md`

至少提供：

- 查詢班次範例。
- 建立成人加學生的 Booking 範例。
- 付款範例。
- 查詢 Order 範例。
- 一個錯誤回應範例。

### 10.5 `docs/version-history.md`

至少記錄：

```text
G0 - Starter Repository
G1 - Greenfield Reference MVP
```

需說明 G1 完成哪些 TODO，但不需要逐行列出程式差異。

---

## 11. G0 到 G1 Delta 文件

建立 `05-g0-to-g1-delta.md`，供 Facilitator 與後續 Brownfield 產製 Agent 使用。

必須包含：

- G0 已提供的能力。
- G1 完成的能力。
- 已移除的 Skip。
- 已完成的 TODO。
- 新增或修改的檔案。
- 規則追溯結果。
- 哪些 G1 結構後續會演化為 Brownfield 模組。

此文件不得提供給 Greenfield Participant。

---

## 12. Acceptance Test Map

建立 `06-acceptance-test-map.md`，將 Participant Acceptance Criteria 對應至 G1 Test。

必要欄位：

```text
Acceptance Criteria ID
Rule ID
Test File
Test Name
Expected Result
Validation Type
```

Acceptance Criteria 必須使用固定 ID，例如：

```text
AC-G-001
AC-G-002
...
```

若 G0 Participant 文件尚未使用 AC ID，產製 G1 前必須回補並確認不改變語意。

---

## 13. G1 與參與者成果的關係

G1 是標準實作，不是唯一答案。

Facilitator 評估參與者成果時，優先順序如下：

1. 商業規則是否正確。
2. API Contract 是否符合。
3. 測試是否可重複並涵蓋核心流程。
4. 程式是否有基本責任分離。
5. 文件是否和實作一致。
6. Agent 使用過程是否包含 Plan、Execute、Test、Explain。

不應因以下差異判定失敗：

- 類別名稱不同。
- 方法名稱不同。
- Payment 使用獨立 Service。
- Repository 使用單一 In-Memory Store 或多個 Repository Class。
- Response 欄位順序不同。

如果參與者成果能滿足需求但結構不同，應記錄為可接受變體。

---

## 14. G1 作為 Brownfield 演化起點

G1 必須預留自然演化能力，但不能提前加入 Brownfield 功能。

後續 B0 預計增加：

- Member。
- Corporate Member。
- Advance Purchase Discount。
- Change Booking。
- Refund。
- Notification。
- Seat Assignment。
- Audit Log。

G1 應做到：

- Fare Policy 可被擴充。
- Booking Service 不與 FastAPI 耦合。
- Repository 可加入更多資料類型。
- Payment Gateway 可控制結果。
- Order 與 Booking 關係清楚。

G1 不得做到：

- 預先實作上述 Brownfield 功能。
- 預先加入團體訂票。
- 預先加入優惠疊加政策。
- 預埋 Brownfield 學生票錯誤。

G1 必須保持正確且一致，Brownfield 問題應在 B0 演化指令中刻意建立。

---

## 15. Git History 建議

若 Coding Agent 可建立 Git Repository，建議使用以下 Commit：

```text
chore: initialize smart ticket starter repository
feat: implement trip search
feat: implement booking and fare calculation
feat: implement payment and order query
test: complete greenfield acceptance coverage
docs: complete greenfield MVP documentation
```

要求：

- Commit 順序要反映合理開發歷程。
- 不要建立數十個無意義 Commit。
- G1 最終建立 Tag：`g1-greenfield-reference`。

若執行環境不允許建立 Git History，應產生 `docs/commit-plan.md` 說明預期 Commit，不得假裝已建立。

---

## 16. 自動驗證程序

Coding Agent 必須在 G1 Repository 根目錄實際執行驗證。

### 16.1 環境

```bash
python --version
pip install -r requirements.txt
```

### 16.2 Test

```bash
pytest -q
```

預期：

- 所有測試通過。
- 無 Skip。
- 無 XFail。
- 無 Warning，或僅有已記錄且不影響執行的相容性 Warning。

### 16.3 Import

```bash
python -c "from smart_ticket.main import app; print(app.title)"
```

### 16.4 API Smoke Test

使用 TestClient 執行：

```text
GET /health
GET /trips
POST /bookings
POST /bookings/{booking_id}/pay
GET /orders/{order_id}
```

Smoke Test 必須完成一條端到端 Happy Path。

### 16.5 Rule Traceability

逐項確認所有 Rule ID 至少對應：

- Requirement。
- Code Area。
- Test。
- Business Rules Document。

---

## 17. G1 Validation Report

建立 `04-g1-validation-report.md`，內容必須記錄實際結果，而不是預期結果。

固定結構：

```markdown
# G1 Validation Report

## 驗證環境

## Dependency Installation

## Application Import

## Test Result

## API Smoke Test

## Rule Traceability

## Skip / XFail / Warning

## Known Limitations

## G0 Consistency Check

## Brownfield Readiness Check

## Final Decision
```

Final Decision 僅可為：

- PASS
- PASS WITH DOCUMENTED LIMITATION
- FAIL

若為 FAIL，不得進入 Brownfield 演化產製。

---

## 18. Reference Solution 隔離規則

必須防止 G1 解答意外進入 Participant Package。

提交前檢查：

- Participant Starter Repository 不含 G1 Commit。
- Participant 文件不連到 Reference Solution。
- Participant README 不提及 Evaluation 目錄。
- 壓縮檔或分享路徑分離。
- Progressive Hint 不含完整 Code Snippet。
- Starter Tests 不洩漏完整演算法。

可以在 Facilitator Recovery Plan 中指出 G1 的位置，但不得在活動開始時顯示給參與者。

---

## 19. Coding Agent 最終回報格式

完成後必須回報：

```markdown
# G1 Greenfield Reference MVP 產製結果

## 建立及修改的檔案

## 完成功能

## API Contract

## 商業規則實作摘要

## 測試結果

## API Smoke Test 結果

## Rule Traceability 結果

## G0 → G1 Delta

## Reference Solution 隔離檢查

## Brownfield 演化準備度

## 已知限制

## Final Decision
```

不得聲稱未執行的驗證已完成。

---

## 20. 完成條件

G1 只有在以下條件全部成立時才算完成：

- 所有 Greenfield MVP API 均已實作。
- 所有 Greenfield 商業規則均正確。
- 學生票確實為 75%。
- Happy Path 可端到端執行。
- Payment Failure 不會產生 Order 或錯誤更新 Booking。
- 完整測試全部通過。
- 無 Skip 與 XFail。
- 文件與實作一致。
- Acceptance Criteria 與 Test 可追溯。
- G0 到 G1 Delta 已記錄。
- G1 未提前加入 Brownfield 功能。
- G1 可作為後續 B0 演化的穩定起點。
- Reference Solution 與 Participant Package 已隔離。
- Validation Report 的 Final Decision 為 PASS，或只有不影響工作坊的已記錄限制。
