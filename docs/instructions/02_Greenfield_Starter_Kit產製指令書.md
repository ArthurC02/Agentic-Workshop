# Agentic Software Development Evolution Workshop
# Greenfield Starter Kit 產製指令書

> 目標讀者：負責建立 Greenfield 階段素材與 G0 Starter Repository 的 Coding Agent
>
> 使用時機：已閱讀總控指令書與技術棧標準後，開始產製參與者在工作坊第一階段取得的完整素材。
>
> 上位規格：
>
> - `00_Agentic工作坊素材產製總控指令書.md`
> - `01_技術棧與Repository標準指令書.md`

---

## 1. 任務目標

建立 Greenfield 階段的 Starter Kit，使普通工程師能在 Coding Agent 協助下，於受限時間內完成 Smart Ticket Platform 的完整 MVP。

此階段的學習重點是讓參與者體驗 Agent 作為 **Tool**：

- 人負責理解需求。
- 人負責決定實作順序。
- 人負責拆解工作及接受結果。
- Agent 協助建立程式、測試與文件。

Starter Kit 不可直接包含完整答案，但必須提供足夠技術骨架與明確需求，避免參與者把時間浪費在環境設定、框架初始化或不必要的架構選擇。

---

## 2. Greenfield 階段時間假設

以整場工作坊 90 分鐘為上限，Greenfield 階段建議配置 **22 分鐘**：

```text
需求閱讀與任務拆解       4 分鐘
Agent 執行與人員互動     12 分鐘
測試、文件與快速驗收      4 分鐘
階段收斂與切換準備        2 分鐘
```

因此，G0 Starter Repository 必須讓參與者能在約 16 至 18 分鐘的有效操作時間內完成 G1 MVP。

此時間限制必須影響素材設計：

- 不要求參與者初始化 Python 專案。
- 不要求參與者建立 FastAPI 基礎設定。
- 不要求參與者自行處理依賴與 Import Path。
- 不要求參與者完成前端。
- 不要求參與者設計資料庫。
- 不要求參與者自行產生大量 Seed Data。
- 不要求參與者熟悉特定 Coding Agent 指令。

---

## 3. 必須產製的輸出

Coding Agent 必須建立以下目錄與內容：

```text
01-greenfield/
├── participant/
│   ├── 01-mission-brief.md
│   ├── 02-business-requirements.md
│   ├── 03-acceptance-criteria.md
│   ├── 04-agent-usage-guide.md
│   ├── 05-submission-checklist.md
│   └── starter-repository/
├── facilitator/
│   ├── 01-facilitation-guide.md
│   ├── 02-timing-and-cues.md
│   ├── 03-progressive-hints.md
│   └── 04-expected-mvp-outline.md
└── evaluation/
    ├── 01-mvp-evaluation-checklist.md
    ├── 02-rule-traceability-matrix.md
    └── 03-g0-validation-report.md
```

此階段只建立 G0 Starter Repository 與相關文件，不建立完整 G1 Reference Solution。G1 應由下一份專屬指令書產製。

---

## 4. Greenfield 故事背景

參與者取得以下簡短背景：

> Smart Ticket 是一個剛開始開發的車票預訂服務。第一個版本只需要支援查詢班次、建立訂票、模擬付款，以及查詢付款後的訂單。公司希望快速驗證完整流程，因此不需要前端、真實付款或外部交通資料。

背景只需支援任務，不要加入冗長的新創公司故事、人物設定或真實交通業者規則。

---

## 5. Greenfield MVP 功能範圍

### 5.1 查詢班次

參與者應完成：

```text
GET /trips
```

最小需求：

- 可依 `origin` 與 `destination` 篩選。
- 只回傳仍有可售座位的班次。
- 回傳班次基本資訊、票價及剩餘座位數。
- 若未提供篩選條件，可回傳所有仍有可售座位的班次。

### 5.2 建立訂票

參與者應完成：

```text
POST /bookings
```

最小需求：

- 指定 `trip_id`。
- 至少包含一位 Passenger。
- Passenger Type 支援 `ADULT` 與 `STUDENT`。
- 旅客數不得超過剩餘座位數。
- 建立後狀態為 `PENDING_PAYMENT`。
- 建立訂票時立即計算總票價。
- 成功建立後扣除可售座位。

### 5.3 模擬付款

參與者應完成：

```text
POST /bookings/{booking_id}/pay
```

最小需求：

- 只有 `PENDING_PAYMENT` 狀態可以付款。
- Mock Payment Gateway 預設成功。
- 付款成功後 Booking 變為 `PAID`。
- 付款成功後建立 Order。
- 重複付款必須被拒絕。

### 5.4 查詢訂單

參與者應完成：

```text
GET /orders/{order_id}
```

最小需求：

- 可查詢付款後建立的 Order。
- 回傳 Booking ID、金額及付款狀態。
- 找不到 Order 時回傳 404。

### 5.5 健康檢查

G0 已提供且參與者不需修改：

```text
GET /health
```

---

## 6. Greenfield 商業規則

以下規則在所有 Participant、Facilitator、Evaluation、Code、Test 與 Documentation 中必須一致。

### Trip

- `TRIP-001`：只可回傳仍有至少一個可售座位的班次。
- `TRIP-002`：Origin 與 Destination 是可選篩選條件；若提供，必須精確符合 Seed Data 中的站點名稱。

### Booking

- `BOOKING-001`：每筆訂票至少包含一位旅客。
- `BOOKING-002`：單筆 Greenfield 訂票最多 4 位旅客。
- `BOOKING-003`：旅客數不得超過班次剩餘座位數。
- `BOOKING-004`：成功建立訂票後立即保留對應座位數。
- `BOOKING-005`：建立後狀態為 `PENDING_PAYMENT`。

### Fare

- `FARE-001`：成人票為 Base Fare 的 100%。
- `FARE-002`：學生票為 Base Fare 的 75%。
- `FARE-003`：每位旅客個別計價後加總為 Booking Total Fare。
- `FARE-004`：所有金額以整數表示，不處理小數與幣別換算。

### Payment / Order

- `PAYMENT-001`：只有 `PENDING_PAYMENT` Booking 可以付款。
- `PAYMENT-002`：付款成功後 Booking 狀態改為 `PAID`。
- `PAYMENT-003`：同一 Booking 不得重複付款。
- `ORDER-001`：付款成功後建立唯一 Order。
- `ORDER-002`：Order Amount 必須等於 Booking Total Fare。

### 工作坊版本注意事項

Greenfield 對學生票的正確規則是 **75%**。Brownfield 後續將以受控方式注入錯誤，但不可在 Greenfield Participant 素材中預告。

---

## 7. Seed Data 規格

G0 必須提供固定、簡單且可重複使用的班次資料。

至少建立以下 4 筆資料，日期採相對固定且不影響測試的範例時間，不依賴工作坊當天日期：

```text
T001：台北 → 台中，Base Fare 700，可售座位 20
T002：台北 → 高雄，Base Fare 1,500，可售座位 8
T003：台中 → 高雄，Base Fare 800，可售座位 0
T004：高雄 → 台北，Base Fare 1,500，可售座位 12
```

要求：

- T003 用於驗證 `TRIP-001`，不得出現在一般可售查詢結果。
- 時間欄位使用合法 ISO 8601 DateTime。
- Arrival Time 必須晚於 Departure Time。
- Seed Data 不得包含真實車次名稱或真實營運資料。
- 測試每次執行前必須重置資料。

---

## 8. G0 Starter Repository 完成程度

G0 必須是「可啟動、可測試、但 MVP 尚未完成」的骨架。

### 8.1 G0 必須已完成

- `requirements.txt`。
- `pyproject.toml`。
- `.gitignore`。
- FastAPI App initialization。
- `GET /health`。
- 統一錯誤回應的基本 Handler。
- 基本 Domain Enum。
- 基本 Domain Model 或明確的 Model Skeleton。
- In-Memory Store 初始化及 Reset 機制。
- 固定 Seed Data。
- Mock Payment Gateway Skeleton。
- Test Fixture 與 Test Client。
- 至少一個通過的 Health Check Test。
- README 的安裝、啟動與測試說明。
- TODO 標記與任務對應關係。

### 8.2 G0 必須留給參與者與 Agent 完成

- Trip Query Use Case 與 Router。
- Booking Creation Use Case 與 Router。
- Fare Policy。
- Payment Use Case 與 Router。
- Order Query Use Case 與 Router。
- 對應 Unit Test。
- 對應 Integration Test。
- `docs/business-rules.md` 的完整內容。
- `docs/api-examples.md` 的完整內容。

### 8.3 不可留白過多

不要只建立空目錄及空檔案。每個 Skeleton 必須包含：

- 明確型別。
- 方法簽章。
- 必要依賴。
- 簡短 TODO。
- 可以被 Coding Agent 理解的上下文。

例如可提供：

```python
class FarePolicy:
    def calculate(self, base_fare: int, passenger_type: PassengerType) -> int:
        """Calculate fare for one passenger. Implement FARE-001 and FARE-002."""
        raise NotImplementedError
```

但不可直接提供完整判斷與答案。

---

## 9. 預期 G0 Repository 結構

建議建立：

```text
starter-repository/
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
│       │   ├── error_handlers.py
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
    ├── conftest.py
    ├── unit/
    │   ├── test_fare_policy.py
    │   └── test_booking_service.py
    └── integration/
        ├── test_health_api.py
        ├── test_trip_api.py
        ├── test_booking_api.py
        └── test_order_api.py
```

G0 建議維持約 25 至 30 個檔案，其中部分是輕量 `__init__.py`。不可用大量無內容檔案虛增規模。

---

## 10. TODO 設計規則

每個 TODO 必須可追溯至商業規則或 Acceptance Criteria。

建議格式：

```python
# TODO(GREENFIELD, FARE-002): Apply the student fare rate.
```

要求：

- TODO 數量應控制在 10 至 16 個主要實作點。
- 不要將每一行都標記為 TODO。
- TODO 必須集中在核心工作，避免參與者同時處理格式化或框架問題。
- TODO 不可直接揭露完整程式碼答案。
- Participant 文件應提醒學員可要求 Agent 搜尋 `TODO(GREENFIELD`。

---

## 11. Participant 文件規格

### 11.1 `01-mission-brief.md`

內容必須簡短，至多約 500 字，包含：

- 故事背景。
- 本階段 Agent 角色為 Tool。
- 參與者應主導需求理解與任務拆解。
- 22 分鐘時間限制。
- 交付項目。
- 不需要完成的項目。

不得包含詳細答案或建議檔案位置。

### 11.2 `02-business-requirements.md`

包含：

- MVP 範圍。
- Trip、Booking、Fare、Payment、Order 規則。
- API 行為要求。
- 商業規則識別碼。
- Out of Scope。

文字必須完整而不冗長，可直接交給 Coding Agent 作為 Context。

### 11.3 `03-acceptance-criteria.md`

以 Given / When / Then 或明確檢核條件表達，至少涵蓋：

- 有座位班次可被查詢。
- 售罄班次不出現。
- 成人票計價正確。
- 學生票 75% 計價正確。
- 超過剩餘座位時拒絕訂票。
- 成功訂票後保留座位。
- 待付款訂票可付款。
- 已付款訂票不可重複付款。
- 成功付款後可查詢 Order。
- 不存在的 Booking / Order 回傳正確錯誤。

### 11.4 `04-agent-usage-guide.md`

保持工具中立，採以下四步：

```text
1. Plan：要求 Agent 先閱讀需求與 Repository，提出 5 至 8 步計畫。
2. Execute：依核准計畫完成 TODO，不要任意改變需求。
3. Test：執行測試，補足失敗案例。
4. Explain：說明修改檔案、規則對應及未完成項目。
```

提供一組通用起始提示範本，但不要提供完整解題 Prompt。

起始提示應要求 Agent：

- 先不要修改程式。
- 閱讀 Participant Requirements。
- 掃描 G0 Repository。
- 找出 TODO。
- 說明計畫及風險。

### 11.5 `05-submission-checklist.md`

包含：

- App 可載入。
- `/health` 正常。
- 核心 API 可呼叫。
- `pytest` 已執行。
- 測試結果有紀錄。
- 文件已更新。
- Agent 已提供修改摘要。
- 參與者已審查主要 Diff。

---

## 12. Facilitator 文件規格

### 12.1 `01-facilitation-guide.md`

必須包含：

- 本階段學習目標。
- 開場說法。
- 哪些問題可以回答。
- 哪些問題不應直接揭露。
- 如何觀察 Agent 是否仍只是 Tool。
- 何時介入。
- 何時要求參與者停止。

### 12.2 `02-timing-and-cues.md`

使用分鐘級節奏：

```text
00:00 發放 Starter Kit
00:02 要求開始閱讀與拆解
00:04 Agent 可開始修改
00:12 第一次時間提醒
00:17 要求停止擴充，優先測試
00:20 要求產生交付摘要
00:22 結束 Greenfield
```

### 12.3 `03-progressive-hints.md`

建立三級提示，不可第一時間給完整答案。

範例：

- Hint 1：請先搜尋 Greenfield TODO 與規則識別碼。
- Hint 2：票價規則應位於 Domain Policy，而不是 API Router。
- Hint 3：指出相關檔案群組，但不提供完整程式碼。

每個主要卡點至少準備三級提示：

- 找不到入口。
- Fare 計算不正確。
- Test Fixture 無法重置。
- Payment 與 Order 關係不清楚。
- 時間不足。

### 12.4 `04-expected-mvp-outline.md`

只供 Facilitator 使用，包含：

- 預期 API。
- 預期 Domain 元件。
- 預期測試類型。
- 可接受的簡化。
- 不可接受的偏離。
- 快速判斷是否達到 G1 的方法。

不要放完整 Reference Code。

---

## 13. Evaluation 文件規格

### 13.1 `01-mvp-evaluation-checklist.md`

分為四類：

- Functional。
- Test。
- Documentation。
- Agentic Behavior。

Agentic Behavior 至少檢查：

- 參與者是否先要求 Agent Plan。
- 是否審查過 Agent 的主要變更。
- 是否要求 Agent 執行 Test。
- 是否能說明人做了什麼、Agent 做了什麼。

此階段不評估 Agent 自主程度高低。

### 13.2 `02-rule-traceability-matrix.md`

建立以下欄位：

```text
Rule ID
Requirement Section
Expected Code Area
Expected Test
Expected Documentation
Validation Method
```

不得在 Participant 文件中提供此完整矩陣。

### 13.3 `03-g0-validation-report.md`

記錄 Coding Agent 對 G0 的實際驗證結果：

- Python 版本。
- Dependencies 安裝結果。
- App Import 結果。
- `/health` 結果。
- `pytest` 結果。
- 預期尚未完成的測試或 TODO。
- 未知錯誤為零。

---

## 14. G0 測試設計策略

G0 必須可以執行 `pytest`，但不能因大量 NotImplementedError 讓參與者難以判讀。

建議採用：

- Health Test 預設通過。
- 尚未實作功能的 Acceptance Tests 以明確的 `skip` 標示。
- 每個 Skip Reason 引用規則識別碼或功能名稱。
- Participant 完成功能後，Agent 需移除對應 Skip 並使測試通過。

禁止：

- 讓所有測試直接失敗並輸出大量 Stack Trace。
- 使用 `xfail(strict=False)` 隱藏未知錯誤。
- 將完整答案寫在測試中。
- 讓 Skip 永久保留在 G1 Reference MVP。

G0 初始測試結果應容易理解，例如：

```text
1 passed, 8 skipped
```

實際數量可略作調整，但必須在 G0 Validation Report 中固定。

---

## 15. 可接受的參與者成果差異

因 Greenfield 為個人活動，不同參與者的實作可以不同，只要：

- 符合 API Contract。
- 商業規則正確。
- 測試可重複。
- 沒有加入外部服務。
- 沒有將全部邏輯塞入 Router。
- 文件足以說明規則與呼叫方式。

不要求：

- 類別及方法名稱完全相同。
- 檔案結構與 Reference Solution 完全一致。
- 100% Test Coverage。
- 生產等級資安或效能。
- 真實座位號配置。

---

## 16. Out of Scope

Greenfield 不包含：

- 會員。
- 企業會員。
- 優惠券。
- 提前購票優惠。
- 改票。
- 退票。
- 通知。
- 團體訂票。
- 相鄰座位。
- 真實付款。
- 使用者登入。
- 資料庫。
- 前端。

Coding Agent 不得「順便」加入上述功能。

---

## 17. G0 自動驗證要求

產製完成後，Coding Agent 必須實際執行：

```bash
python --version
pip install -r requirements.txt
pytest
python -c "from smart_ticket.main import app; print(app.title)"
```

必要時可使用符合專案 `src` layout 的環境設定，但 README 與 CI 驗證方式必須一致。

另外使用 Test Client 驗證：

```text
GET /health → 200
Response → {"status": "ok"}
```

驗證完成後才可交付 G0。

---

## 18. Coding Agent 最終回報格式

完成產製後，回報內容必須包含：

```markdown
# Greenfield Starter Kit 產製結果

## 建立的檔案

## G0 已完成能力

## 留給參與者的 TODO

## 初始測試結果

## 啟動驗證結果

## 商業規則追溯檢查

## Participant / Facilitator / Evaluation 隔離檢查

## 與上位規格的一致性檢查

## 已知限制
```

不得只提供檔案清單，也不得聲稱未執行的測試已通過。

---

## 19. 完成條件

Greenfield Starter Kit 只有在以下條件全部成立時才算完成：

- Participant、Facilitator、Evaluation 素材已分離。
- G0 Repository 可安裝、可啟動、可執行測試。
- `/health` 正常。
- Seed Data 固定且可重置。
- MVP 需求與 Acceptance Criteria 完整。
- 商業規則使用固定 Rule ID。
- G0 提供足夠骨架，但未包含完整 MVP 答案。
- 主要 TODO 控制在 10 至 16 個實作點。
- 初始測試結果明確且無未知錯誤。
- 學生票規則在 Greenfield 固定為 75%。
- 普通工程師能在 Coding Agent 協助下於約 22 分鐘內完成核心 MVP。
- 沒有加入 Brownfield 才需要的功能。
- 所有素材保持工具中立。
