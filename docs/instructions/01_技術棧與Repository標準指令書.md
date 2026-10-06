# Agentic Software Development Evolution Workshop
# 技術棧與 Repository 標準指令書

> 目標讀者：負責產製工作坊程式素材的 Coding Agent
>
> 使用時機：完成總控指令書閱讀後，開始建立 Greenfield Starter Repository、Greenfield Reference MVP 與 Brownfield Repository 之前。
>
> 上位規格：`00_Agentic工作坊素材產製總控指令書.md`

> 已核准變更（2026-10-05）：使用者允許改用 Python 3.13 或 3.14；本套素材採 Python 3.13 作統一基線，原 Python 3.12 要求由此取代。其餘技術與商業規則不變。

---

## 1. 任務目標

依照本指令書建立 Smart Ticket Platform 的統一技術基線，使後續 G0、G1、B0、B1、B2、B3 各版本能使用相同技術棧、執行方式、測試方式及程式設計原則。

本文件只定義技術棧與 Repository 標準，不要求立即完成所有工作坊版本。

若本文件與總控指令書衝突，除非本文件明確標示為「已核准變更」，否則以總控指令書為準。

---

## 2. 固定技術棧

使用以下技術棧，不得任意替換：

- Language：Python 3.13
- Web Framework：FastAPI
- API Schema：FastAPI 原生 OpenAPI
- Data Validation：Pydantic 2
- Test Framework：pytest
- API Test Client：FastAPI TestClient 或 httpx 相容測試方式
- Persistence：In-Memory Repository
- Package / Environment：`venv` + `pip`
- Dependency Declaration：`requirements.txt`
- Application Server：Uvicorn
- Documentation：Markdown
- Source Control：Git

禁止加入：

- 外部資料庫。
- Docker 作為必要前置條件。
- Kubernetes。
- Message Broker。
- 真實付款服務。
- 外部交通資料 API。
- 前端框架。
- 付費套件或付費雲端服務。

Docker 可以在最終素材中作為選用項目，但工作坊核心流程不得依賴 Docker。

---

## 3. 技術選擇原則

此技術基線必須支援以下工作坊需求：

1. 普通工程師能快速理解。
2. Coding Agent 能快速掃描 Repository。
3. 核心商業邏輯可單元測試。
4. API 行為可整合測試。
5. Repository 可離線執行。
6. 不需要建立外部基礎設施。
7. 可自然演化為 30 至 50 個程式與測試檔案。
8. 可植入合理且可控的 Brownfield 技術債。
9. 每個教學版本均可獨立啟動及測試。

---

## 4. 架構風格

採用輕量分層架構，不使用完整 Clean Architecture 或複雜 DDD Framework。

標準資料流：

```text
API Router
    ↓
Application Service
    ↓
Domain Model / Domain Policy
    ↓
Repository Interface
    ↓
In-Memory Repository
```

各層責任如下。

### 4.1 API Layer

負責：

- HTTP Request / Response。
- Pydantic Schema 驗證。
- HTTP Status Code。
- 將 Application Error 轉換為 API Error。

不得負責：

- 票價計算。
- 座位配置。
- 優惠判斷。
- 訂單狀態轉換規則。

### 4.2 Application Layer

負責：

- Use Case 流程編排。
- 呼叫 Domain Policy。
- 呼叫 Repository。
- 管理交易式流程的概念邊界。

在 In-Memory 實作下不需要建立真實 Transaction Manager，但應讓「全部成功或全部失敗」的意圖可被測試。

### 4.3 Domain Layer

負責：

- Entity、Value Object、Enum。
- Fare Policy。
- Booking Rule。
- Payment / Order 狀態規則。
- Group Booking 的核心限制。

不得依賴 FastAPI、HTTP 或測試框架。

### 4.4 Infrastructure Layer

負責：

- In-Memory Repository。
- Seed Data。
- Mock Payment Gateway。
- 時間或識別碼等可替換依賴。

不得呼叫外部 API。

---

## 5. Repository 標準結構

G1 Reference MVP 建議使用以下基礎結構：

```text
smart-ticket-platform/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── business-rules.md
│   └── api-examples.md
├── src/
│   └── smart_ticket/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── trips.py
│       │   ├── bookings.py
│       │   └── orders.py
│       ├── application/
│       │   ├── __init__.py
│       │   ├── trip_service.py
│       │   ├── booking_service.py
│       │   └── order_service.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── enums.py
│       │   ├── errors.py
│       │   └── fare_policy.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── repositories.py
│       │   ├── payment_gateway.py
│       │   └── seed_data.py
│       └── schemas/
│           ├── __init__.py
│           ├── trip.py
│           ├── booking.py
│           └── order.py
└── tests/
    ├── unit/
    │   ├── test_fare_policy.py
    │   └── test_booking_service.py
    ├── integration/
    │   ├── test_trip_api.py
    │   ├── test_booking_api.py
    │   └── test_order_api.py
    └── conftest.py
```

G0 Starter Repository 可以少於上述檔案，但必須保留清楚的擴充方向。

B0 Brownfield Repository 應由此結構自然成長，不得改成完全不同的架構。可以增加：

- `members`
- `discounts`
- `refunds`
- `changes`
- `notifications`
- `seats`
- `audit`

但應維持整體命名與分層一致。

---

## 6. Python 專案設定

### 6.1 Import Path

採 `src` layout。

測試及啟動方式必須能正確找到：

```text
smart_ticket
```

可以透過 `pyproject.toml` 設定 pytest 的 `pythonpath`，避免要求參與者進行複雜安裝。

### 6.2 requirements.txt

只加入必要依賴，建議範圍：

```text
fastapi
uvicorn
pydantic
pytest
httpx
```

應固定相容版本範圍，避免工作坊當天因 major version 改版失敗。

不得加入與核心任務無關的套件。

### 6.3 pyproject.toml

至少設定：

- pytest test path。
- Python import path。
- 基本 pytest options。

不要引入複雜 build backend，除非後續實際驗證需要。

---

## 7. 啟動與測試標準

### 7.1 環境建立

README 必須提供適用於一般 Shell 的簡潔步驟：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows 啟用方式可另外列出，但不得讓 README 變得冗長。

### 7.2 啟動應用

標準指令：

```bash
uvicorn smart_ticket.main:app --app-dir src --reload
```

### 7.3 執行測試

標準指令：

```bash
pytest
```

### 7.4 健康檢查

所有可執行版本至少提供：

```text
GET /health
```

預期回應：

```json
{
  "status": "ok"
}
```

---

## 8. API 設計標準

### 8.1 Greenfield MVP 最小 API

至少包含：

```text
GET  /health
GET  /trips
POST /bookings
POST /bookings/{booking_id}/pay
GET  /orders/{order_id}
```

可選擇加入：

```text
GET /bookings/{booking_id}
```

不得建立過多 API，避免 Greenfield 階段工作量失控。

### 8.2 API 行為原則

- 使用明確的 Request / Response Schema。
- 使用一致的錯誤格式。
- 找不到資源時使用 404。
- 商業規則不成立時使用適當的 4xx 回應。
- 不回傳 Python Exception Stack Trace。
- ID 可以使用 UUID 字串，但測試必須可穩定驗證。

### 8.3 錯誤回應格式

統一採簡單格式：

```json
{
  "error": {
    "code": "BOOKING_NOT_FOUND",
    "message": "Booking not found"
  }
}
```

所有版本應維持格式相容，除非工作坊任務明確要求修改。

---

## 9. Greenfield MVP Domain 基線

以下是 G1 必須具備的最小 Domain 概念。

### 9.1 Trip

至少包含：

- `trip_id`
- `origin`
- `destination`
- `departure_time`
- `arrival_time`
- `base_fare`
- `available_seats`

### 9.2 Passenger

至少包含：

- `passenger_id`
- `name`
- `passenger_type`

Greenfield 可先支援：

- `ADULT`
- `STUDENT`

### 9.3 Booking

至少包含：

- `booking_id`
- `trip_id`
- `passengers`
- `total_fare`
- `status`

建議狀態：

- `PENDING_PAYMENT`
- `PAID`
- `CANCELLED`

### 9.4 Order

至少包含：

- `order_id`
- `booking_id`
- `amount`
- `payment_status`

### 9.5 Payment

使用 Mock Payment Gateway。

付款結果必須可在測試中控制，不可隨機成功或失敗。

---

## 10. 商業規則追溯標準

每項商業規則使用固定識別碼。

Greenfield 基線至少包含：

- `TRIP-001`：只可查詢有可售座位的班次。
- `TRIP-002`：Origin 與 Destination 為可選且精確比對的篩選條件。
- `BOOKING-001`：訂票至少要有一位旅客。
- `BOOKING-002`：一般單筆 Greenfield 訂票最多 4 位旅客；後續一般訂票沿用，團體訂票另依 `GROUP-*` 規則。
- `BOOKING-003`：旅客數不得超過班次剩餘座位數。
- `BOOKING-004`：成功建立 Booking 後立即保留座位。
- `BOOKING-005`：新 Booking 狀態為 `PENDING_PAYMENT`。
- `FARE-001`：成人票採全額票價。
- `FARE-002`：學生票為 Base Fare 的 75%。
- `FARE-003`：逐位旅客計價後加總為 Booking Total Fare。
- `FARE-004`：金額使用整數，不處理小數與幣別換算。
- `PAYMENT-001`：只有待付款訂票可以付款。
- `PAYMENT-002`：付款成功後訂票狀態改為已付款。
- `PAYMENT-003`：同一 Booking 不得重複付款。
- `ORDER-001`：付款成功後建立唯一 Order。
- `ORDER-002`：Order Amount 等於 Booking Total Fare。

2026-10-05 P2 編號對齊：沿用 G0／G1 已固定的規則內容。原本 `BOOKING-002` 的剩餘座位限制改引用 `BOOKING-003`，`BOOKING-002` 專指一般單筆最多 4 人；同步列齊已存在的 Greenfield 規則，不改變商業語意。追溯基線見 `agentic-workshop/00-governance/rule-traceability-baseline.md`（Repo 根目錄相對路徑）。

每項規則必須能對應至：

- Requirement。
- Domain 或 Application Code。
- Test。
- Documentation。

不得只存在於 Prompt 或口頭說明。

---

## 11. 測試標準

### 11.1 測試層次

至少包含：

- Domain / Policy Unit Test。
- Application Service Unit Test。
- API Integration Test。

### 11.2 測試特性

測試必須：

- 可重複執行。
- 不依賴測試執行順序。
- 不連線外部服務。
- 不使用隨機結果。
- 執行時間短。
- 測試名稱可理解商業意圖。

### 11.3 測試命名

建議使用：

```python
def test_student_passenger_receives_expected_discount():
    ...
```

若引用規則識別碼，可在 docstring 或測試註解中標示，不要讓函式名稱過長。

### 11.4 Brownfield 錯誤注入

B0 中預埋的學生票折扣錯誤必須符合：

- 應用可正常啟動。
- 大部分測試可通過。
- 至少有一個測試可揭露錯誤，或由任務要求參與者補出失敗測試。
- Facilitator / Evaluation 素材必須明確記錄錯誤位置、根因及驗證方式。

最終採哪種揭露方式，由後續 Brownfield 任務指令書決定。

---

## 12. 文件標準

每個完整版本至少包含：

### README.md

- 專案用途。
- 環境需求。
- 安裝方式。
- 啟動方式。
- 測試方式。
- 主要目錄說明。

### docs/architecture.md

- 分層說明。
- 主要模組。
- 核心依賴方向。
- 不應包含過度複雜的圖形語法。

### docs/business-rules.md

- 規則識別碼。
- 規則內容。
- 適用版本。

### docs/api-examples.md

- 核心 API 範例。
- 範例不得依賴真實個資。

Brownfield 可以刻意存在受控文件落差，但 Evaluation 必須知道正確狀態，且落差不得破壞 Greenfield 階段。

---

## 13. Coding Style

- 使用 type hints。
- 公開 Service、Policy 與 Repository 方法使用清楚命名。
- 避免過長函式。
- 避免全域可變狀態散落各處。
- In-Memory Store 應集中管理並可在測試間重置。
- 使用 Enum 表達狀態與類型。
- Domain Error 使用明確例外類別。
- API Layer 統一處理 Domain / Application Error。
- 不需要加入大量註解，應讓程式結構與命名表達意圖。

---

## 14. Brownfield 成長規則

B0 Repository 必須從 G1 合理演化，而不是重新建立另一套程式。

成長時可加入：

- 會員資料與企業會員類型。
- 優惠與票價政策。
- 改票與退票流程。
- 通知紀錄。
- 座位配置。
- Audit Log。
- 更多 API 與測試。

應保留部分 G1 的核心結構及名詞，使參與者可將 Greenfield 經驗帶入 Brownfield。

Brownfield 的複雜度來源應是：

- 功能增加。
- 模組依賴增加。
- 規則交互作用。
- 文件與程式的有限落差。
- 合理歷史決策。

複雜度來源不得是：

- 故意混亂命名。
- 大量重複程式碼。
- 無法啟動的環境。
- 不相關的框架。
- 隱藏且無提示的陷阱。

---

## 15. 版本驗證 Gate

每次建立 G0、G1、B0、B1、B2 或 B3 後，Coding Agent 都必須執行以下檢查。

### Gate A：檔案與依賴

- 必要檔案存在。
- Import 可解析。
- 依賴可安裝。
- 無外部憑證需求。

### Gate B：啟動

- FastAPI App 可載入。
- `/health` 回應正確。
- OpenAPI 可產生。

### Gate C：測試

- 執行 `pytest`。
- 結果符合該版本預期。
- 除刻意設計的教學失敗外，不得有未知失敗。

### Gate D：規則追溯

- Requirement、Code、Test、Document 的規則一致。
- 新增規則已加入規則清單。
- 移除或修改規則已留下版本說明。

### Gate E：工作坊適配

- 普通工程師能在 Agent 協助下理解。
- 不要求外部服務。
- 不揭露 Participant 不應看到的答案。
- 任務量符合 90 分鐘總限制。

---

## 16. Coding Agent 執行輸出

當 Coding Agent 依本文件實際建立 Repository 基線時，必須提供：

1. 建立或修改的檔案清單。
2. 技術架構摘要。
3. 啟動指令。
4. 測試指令。
5. 測試結果。
6. 規則追溯清單。
7. 已知限制。
8. 與上位總控指令的一致性檢查結果。

不得只回答「已完成」。

---

## 17. 完成條件

本技術規格只有在下列條件均成立時才算被正確採用：

- 使用 Python 3.13、FastAPI、Pydantic 2 與 pytest。
- 核心流程不依賴外部 API 或資料庫。
- 採輕量分層架構。
- Greenfield 與 Brownfield 採相同的核心架構與詞彙。
- Repository 能從小型 MVP 自然成長至 30 至 50 個程式及測試檔案。
- 每個版本均有可重複的啟動與測試方式。
- 商業規則可以從 Requirement 追溯至 Code、Test 與 Document。
- 技術複雜度服務於 Agentic SDLC 學習目的，而不是成為額外負擔。
