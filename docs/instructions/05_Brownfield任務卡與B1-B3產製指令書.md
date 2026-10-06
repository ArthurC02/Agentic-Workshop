# Agentic Software Development Evolution Workshop
# Brownfield 任務卡與 B1-B3 Reference Solution 產製指令書

> 目標讀者：負責產製 Brownfield 任務卡、階段版本、標準答案、驗證腳本及主持素材的 Coding Agent
>
> 使用時機：B0 Brownfield Repository 已完成，且 `01-b0-validation-report.md` 的 Final Decision 為 `PASS AS BROWNFIELD BASELINE` 後。
>
> 上位規格：
>
> - `00_Agentic工作坊素材產製總控指令書.md`
> - `01_技術棧與Repository標準指令書.md`
> - `02_Greenfield_Starter_Kit產製指令書.md`
> - `03_G1_Greenfield_Reference_MVP產製指令書.md`
> - `04_B0_Brownfield_Repository演化產製指令書.md`

---

## 已核准變更：2026-10-05 B0／B1 測試語意（方案 A）

使用者於 2026-10-05 以原文「套用」核准 [B0 Regression Gate 修正提案](../planning/b0-regression-gate-proposal.md) 的方案 A。本指令書同步 B0 為一個受控 Bug、多項已核實 Manifest 失敗、零非預期失敗；B1 修復後全部 28 項原 G1 Regression 與全部 B0 新增測試通過。28 是原 G1 數量，不是 B1 全套數；不刪弱斷言、不改期待值、不用 Skip／XFail。

B0 的 Evaluation 隔離診斷副本僅供原因驗證，不等同本階段正式 B1 交付，也不得給學員作答案。未來 B1 仍需獨立版本、文件、完整測試及驗證報告。

## 1. 任務目標

以 B0 Brownfield Repository 為起點，產製三張依序揭露的任務卡，以及對應的 B1、B2、B3 Reference Solution。

三項任務形成漸進式難度：

```text
B1：Bug Fix
    ↓
B2：Business Rule Change
    ↓
B3：New Feature
```

其作用不是讓參與者同時承受三項壓力，而是讓他們逐步經歷：

```text
找出問題
  ↓
分析跨模組影響
  ↓
讓 Agent 主導完整交付
```

任務卡必須依工作坊節奏分批揭露，不得一開始全部發放。

---

## 2. 工作坊時間配置

Brownfield 整體建議配置 **51 分鐘**：

```text
Time Skip 與重新分組              4 分鐘
個人 Agent 獨立分析 B0            6 分鐘
小組比較結果並建立 Shared Context  5 分鐘
B1 Bug Fix                        8 分鐘
B2 Rule Change                   11 分鐘
B3 Group Booking                 13 分鐘
交付摘要與階段收斂                4 分鐘
```

總工作坊時間參考：

```text
開場與說明               7 分鐘
Greenfield               22 分鐘
Time Skip + Brownfield   51 分鐘
回顧與組織導入收斂       10 分鐘
總計                     90 分鐘
```

後續 Runbook 可微調 1 至 2 分鐘，但不得壓縮 Brownfield 至無法完成 A → B → C 的演化體驗。

---

## 3. 必須產製的輸出

```text
03-brownfield/
├── participant/
│   └── task-cards/
│       ├── 01-b1-student-fare-bug.md
│       ├── 02-b2-discount-policy-change.md
│       └── 03-b3-group-booking.md
├── facilitator/
│   ├── 04-task-reveal-sequence.md
│   ├── 05-task-progressive-hints.md
│   ├── 06-timebox-and-stop-rules.md
│   └── 07-expected-participant-behavior.md
└── evaluation/
    ├── 05-b1-expected-impact-analysis.md
    ├── 06-b2-expected-impact-analysis.md
    ├── 07-b3-expected-impact-analysis.md
    ├── 08-b1-acceptance-test-map.md
    ├── 09-b2-acceptance-test-map.md
    ├── 10-b3-acceptance-test-map.md
    ├── 11-b0-to-b3-version-matrix.md
    └── reference-solutions/
        ├── b1-student-fare-fixed/
        ├── b2-best-discount-policy/
        └── b3-group-booking/
```

每個 Reference Solution 必須是獨立可執行 Repository，並保留前一版本的完整能力。

---

## 4. 任務揭露原則

### 4.1 不可一次發放全部任務

揭露順序固定為：

```text
完成 Shared Context
  ↓
揭露 B1
  ↓
B1 通過或時間到
  ↓
揭露 B2
  ↓
B2 通過或時間到
  ↓
切換 Digital Worker Operating Rules
  ↓
揭露 B3
```

### 4.2 任務卡內容分層

每張 Participant 任務卡僅包含：

- 業務情境。
- 任務目標。
- 新增或修正規則。
- 交付項目。
- 不可修改範圍。
- 完成條件。
- 人與 Agent 的合作模式。

不得包含：

- 解答檔案位置。
- 標準實作方式。
- Reference Solution 結構。
- 完整 Impact Analysis。
- 主持人提示。

### 4.3 每張任務卡必須可獨立識別

固定 ID：

```text
TASK-B1-001
TASK-B2-001
TASK-B3-001
```

Acceptance Criteria 固定前綴：

```text
AC-B1-xxx
AC-B2-xxx
AC-B3-xxx
```

---

# Part A：B1 Bug Fix

## 5. B1 任務定位

### 任務名稱

```text
TASK-B1-001：修復學生票折扣異常
```

### Agent 成熟度

```text
Teammate
```

此階段 Agent 應參與分析及提出修正方案，但人員仍負責：

- 比較不同 Agent 的分析。
- 核對規則證據。
- 核准修改範圍。
- 審查 Diff。
- 決定是否接受修正。

### 目的

- 熟悉 B0 Repository。
- 驗證個人分析與 Shared Context。
- 建立以 Test、Rule、Code 交叉驗證的習慣。
- 避免只靠全文搜尋修改常數。

---

## 6. B1 Participant 任務內容

業務回報：

> 客服發現學生旅客的票價可能計算錯誤。已知公開規則仍為 Base Fare 的 75%，但目前自動測試中有若干相關案例失敗，可能具有共同原因。請確認根因、影響範圍並完成修復。

參與者必須：

1. 先比較小組成員各自的 Agent 分析。
2. 找出可驗證的規則來源。
3. 說明可能根因與受影響範圍。
4. 核准主要 Agent 的修正計畫。
5. 由主要 Agent 修改程式及必要測試或文件。
6. 執行完整測試。
7. 產生簡短修復摘要。

不可：

- 移除或弱化失敗測試。
- 將測試期待值改成 85%。
- 全面重寫 Discount / Fare 模組。
- 修改不相關 API Contract。

---

## 7. B1 固定規則

- `FARE-002`：學生票為 Base Fare 的 75%。
- `FARE-003`：每位旅客個別計價後加總。
- `BUG-B0-001`：B0 將學生票錯誤設定為 85%。

B1 不改變：

- 成人票 100%。
- 提前購票 85%。
- Corporate Member 95%。
- B0 既有優惠選擇順序。

多優惠最有利政策留到 B2。

---

## 8. B1 Acceptance Criteria

至少建立：

- `AC-B1-001`：單一學生旅客票價為 Base Fare 的 75%。
- `AC-B1-002`：成人票計價不受影響。
- `AC-B1-003`：成人加學生的 Booking Total 正確。
- `AC-B1-004`：全部 28 項原 G1 Regression Tests 保留正確斷言並恢復通過；28 不代表 B1 全套數量。
- `AC-B1-005`：B0 Manifest 中所有學生票 Bug 對應失敗測試均轉為通過，包括受影響的 G1 與 B0 新增案例。
- `AC-B1-006`：全部原 G1 與全部 B0 新增測試完整執行且通過，零失敗、無 Skip、無 XFail；不得用診斷副本結果代替本版驗證。
- `AC-B1-007`：Business Rules 文件仍記載 75%，且與程式一致。

---

## 9. B1 Reference Solution 要求

B1 應採最小安全修正：

- 修正 Fare / Discount Policy 中錯誤的學生票率。
- 不進行不必要重構。
- 若文件本來正確，不要無意義改寫。
- 若測試已能揭露錯誤，不要重寫整個測試套件。

版本識別：

```text
B1 - Student Fare Fixed
```

Git Tag：

```text
b1-student-fare-fixed
```

B1 預期測試：

```text
All tests pass.
No skip.
No xfail.
```

---

# Part B：B2 Business Rule Change

## 10. B2 任務定位

### 任務名稱

```text
TASK-B2-001：導入不可疊加的最有利優惠政策
```

### Agent 成熟度

```text
Teammate → Digital Worker 過渡
```

此階段 Agent 應：

- 分析規則交互作用。
- 找出跨模組影響。
- 提出 2 至 3 個可行方案。
- 說明取捨。
- 在人員核准後主導實作。

人員應：

- Challenge Agent 的假設。
- 選擇方案。
- 核准 Task Breakdown。
- 審查規則、測試與文件一致性。

---

## 11. B2 Participant 任務內容

新商業規則：

```text
成人票：100%
學生票：75%
提前 14 天購票：85%
Corporate Member：95%
```

新增核心政策：

> 多個優惠條件同時符合時，不可疊加，只採用對該旅客最有利的單一優惠。

範例：

- 學生且提前 14 天購票：採 75%，不是 75% × 85%。
- Corporate Member 且提前 14 天購票：採 85%，不是 95% × 85%。
- 學生、Corporate Member 且提前 14 天購票：採 75%。
- 成人且無任何優惠資格：採 100%。

每位 Passenger 必須獨立評估優惠，再加總 Booking Total。

---

## 12. B2 新增與更新規則

保留：

- `FARE-001`：成人 Base Fare 100%。
- `FARE-002`：學生資格對應 75%。
- `FARE-003`：逐位旅客計價後加總。
- `FARE-004`：金額使用整數。
- `FARE-005`：提前至少 14 天具備 85% 優惠資格。
- `MEMBER-003`：Corporate Member 具備 95% 優惠資格。

新增：

- `FARE-007`：多項優惠不可疊加。
- `FARE-008`：同時符合多項優惠時，採數值最低、對旅客最有利的單一折扣率。
- `FARE-009`：每位 Passenger 獨立決定適用優惠。
- `FARE-010`：Fare Result 必須記錄實際採用的 Discount Type 及 Rate。

---

## 13. B2 必須進行的 Impact Analysis

Agent 至少應分析：

- Fare / Discount Policy。
- Passenger Fare Calculation。
- Member Lookup。
- Booking Creation。
- Booking Change 的重新計價。
- API Response 是否應揭露 Applied Discount。
- Unit Tests。
- Integration Tests。
- `docs/business-rules.md`。
- `docs/discount-overview.md`。
- API Examples。

Agent 必須指出：

- 哪些是一定要改。
- 哪些可能受影響但不一定要改。
- 哪些不應修改。
- 既有 `DEBT-001` 是否要局部改善。

---

## 14. B2 可接受設計

Reference Solution 建議採簡單可組合候選優惠方式：

```text
收集該 Passenger 符合的 Discount Candidate
  ↓
加入 FULL_FARE 100% 作為預設
  ↓
選擇 Rate 最低的 Candidate
  ↓
計算 Fare
  ↓
回傳 Applied Discount Type / Rate / Amount
```

可接受：

- 簡單 Candidate List。
- 小型 Strategy Class。
- 明確 Policy Function。

不可接受：

- 建立複雜 Rule Engine。
- 加入第三方規則套件。
- 將所有條件寫入 Router。
- 使用優惠疊乘。
- 對整筆 Booking 只選一個共同優惠，導致不同 Passenger 無法個別計價。

---

## 15. B2 Acceptance Criteria

至少建立：

- `AC-B2-001`：成人且無優惠為 100%。
- `AC-B2-002`：學生為 75%。
- `AC-B2-003`：提前購票成人為 85%。
- `AC-B2-004`：Corporate Member 成人為 95%。
- `AC-B2-005`：學生加提前購票採 75%。
- `AC-B2-006`：Corporate Member 加提前購票採 85%。
- `AC-B2-007`：學生、Corporate Member、提前購票同時符合時採 75%。
- `AC-B2-008`：優惠不疊加。
- `AC-B2-009`：不同 Passenger 可套用不同優惠。
- `AC-B2-010`：Fare Result 記錄採用的 Discount Type 與 Rate。
- `AC-B2-011`：Booking Change 重新計價遵循相同政策。
- `AC-B2-012`：B1 及 G1 Regression Tests 通過。
- `AC-B2-013`：折扣文件與程式同步。

---

## 16. B2 Reference Solution 要求

版本識別：

```text
B2 - Best Single Discount Policy
```

Git Tag：

```text
b2-best-single-discount
```

要求：

- 修正 `DEBT-001` 至足以清楚表達政策，但不做過度重構。
- 保留 `DEBT-002` 同步 Notification 呼叫。
- 更新 `docs/discount-overview.md`，消除其中一項受控文件落差。
- 不必處理 `docs/change-booking-guide.md` 的歷史落差，除非修改涉及該行為。
- 測試涵蓋所有優惠組合的代表案例。
- 所有測試通過。
- 不提前實作團體訂票。

---

# Part C：B3 New Feature

## 17. B3 任務定位

### 任務名稱

```text
TASK-B3-001：新增團體訂票能力
```

### Agent 成熟度

```text
Digital Worker
```

進入 B3 前，主持人必須宣布操作規則改變：

> 人員不再直接修改程式碼。主要 Agent 負責分析、設計、實作、測試、文件及交付摘要；人員只進行 Challenge、Review、Approve、Reject 與要求補充證據。

B3 的重點不是完成最多程式碼，而是觀察：

- Agent 是否能在 Rule 與 Approval Gate 下主導交付。
- 人員能否辨識風險及缺口。
- Agent 是否同步更新 Test 與 Documentation。
- Agent 自主執行是否仍可追溯及驗證。

---

## 18. B3 Participant 任務內容

新增團體訂票：

- 單筆團體訂票人數為 5 至 20 人。
- 所有人搭乘同一 Trip。
- 座位應盡量安排在同一車廂且連續相鄰。
- 若無法提供完整相鄰座位，不得自動拆散成立，應回報無法滿足。
- 團體 Booking 建立後仍為 `PENDING_PAYMENT`。
- 付款成功時整筆成立。
- 付款失敗時整筆取消。
- 付款失敗後不得保留任何座位。
- 付款失敗後不得建立 Order。
- 團體內每位 Passenger 仍依 B2 的最有利單一優惠政策個別計價。
- 團體 Booking 的 Total Fare 為所有 Passenger Fare 加總。

---

## 19. B3 範圍澄清

固定假設：

- 不提供部分成功。
- 不拆成多筆 Booking。
- 不處理候補。
- 不跨 Trip。
- 不跨車廂。
- 不提供特定座位偏好。
- 不新增前端。
- 不新增外部資料庫。
- 不新增真實付款。
- 不處理分次付款。

「盡量相鄰」在本工作坊中固定解釋為：

> 必須找到同一車廂內足以容納整個團體的連續空位區段；找不到時即拒絕建立團體 Booking。

此定義可避免高階最佳化演算法。

---

## 20. B3 新增規則

### Group Booking

- `GROUP-001`：團體訂票旅客數最少 5 人。
- `GROUP-002`：團體訂票旅客數最多 20 人。
- `GROUP-003`：所有 Passenger 必須搭乘同一 Trip。
- `GROUP-004`：必須配置同一車廂內連續座位。
- `GROUP-005`：無法完整配置時不得建立 Booking。
- `GROUP-006`：建立成功後一次保留全部座位。
- `GROUP-007`：團體建立失敗時不得保留任何座位。

### Group Payment

- `GROUP-PAY-001`：團體付款成功後整筆 Booking 轉為 `PAID`。
- `GROUP-PAY-002`：團體付款失敗後 Booking 轉為 `CANCELLED`。
- `GROUP-PAY-003`：付款失敗後釋放全部團體座位。
- `GROUP-PAY-004`：付款失敗不得建立 Order。
- `GROUP-PAY-005`：團體付款成功只建立一筆 Order。

### Fare

- `GROUP-FARE-001`：每位 Passenger 依 B2 政策個別計價。
- `GROUP-FARE-002`：團體 Total Fare 為個別 Fare 加總。

### Audit and Notification

- `GROUP-AUDIT-001`：團體建立、付款成功或付款失敗均留下 Audit Entry。
- `GROUP-NOTIFY-001`：團體付款成功建立通知紀錄。
- `GROUP-NOTIFY-002`：團體付款失敗建立取消通知紀錄。

---

## 21. B3 API Contract

Reference Solution 至少加入：

```text
POST /group-bookings
POST /group-bookings/{booking_id}/pay
```

可以沿用一般 Booking 查詢 API。

### 建立 Group Booking Request

至少包含：

```json
{
  "trip_id": "T006",
  "member_id": "M002",
  "passengers": [
    {
      "passenger_id": "P001",
      "name": "Passenger 1",
      "passenger_type": "ADULT"
    }
  ]
}
```

實際 Request 必須有 5 至 20 位 Passenger。

### Response 至少包含

- Booking ID。
- Booking Type。
- Status。
- Total Fare。
- Applied Fare 明細。
- Assigned Seats。

不得在 Participant 任務卡提供完整 Response 答案，只需說明最低欄位需求。

---

## 22. B3 Seat Model 擴充

B0 的 Seat ID 必須演化為可支援連續座位判斷的結構。

建議 Value：

```text
carriage_id
row_number
seat_number
seat_id
```

簡化 Seed Layout 建議：

```text
每個 Trip：2 個 Carriage
每個 Carriage：5 排
每排：4 個連續 Seat
每個 Carriage 共 20 個 Seat
```

連續座位固定以同一車廂中排序後相鄰的 Seat Position 判斷。

不要求處理走道、靠窗、方向或真實車廂布局。

Agent 可以選擇：

- Sliding Window。
- 連續可用座位掃描。

不可引入複雜最佳化套件。

---

## 23. B3 Atomicity 模擬

由於使用 In-Memory Repository，仍必須清楚模擬 Atomicity。

### 建立失敗

若團體人數、座位或其他規則不成立：

- 不建立 Booking。
- 不保留任何座位。
- 不建立 Order。
- 可留下失敗 Audit Entry，但不得影響核心狀態。

### 付款失敗

若 Mock Payment Gateway 回傳失敗：

- Booking 轉為 `CANCELLED`。
- 全部座位釋放。
- 不建立 Order。
- 建立付款失敗 Audit Entry。
- 建立取消通知紀錄。

Reference Solution 應採可理解的補償流程，不需建立通用 Transaction Framework。

---

## 24. B3 Human Approval Gates

Agent 不得一次從需求直接改完所有程式。Participant Operating Rules 必須要求以下 Gate：

### Gate 1：Requirement Understanding

Agent 提交：

- 需求摘要。
- 假設。
- 資訊缺口。
- Out of Scope。

人員核准後才能進入設計。

### Gate 2：Impact and Design

Agent 提交：

- 影響模組。
- API 方案。
- Seat Assignment 方案。
- Atomicity 方案。
- 測試策略。
- 風險。

人員核准後才能修改程式。

### Gate 3：Code and Test Review

Agent 提交：

- Diff 摘要。
- 測試結果。
- 規則追溯。
- 文件更新。
- 未完成事項。

人員決定 Approve、Reject 或要求修正。

因時間有限，Gate 回覆應採短格式，不進行長會議。

---

## 25. B3 Acceptance Criteria

至少建立：

- `AC-B3-001`：4 位旅客不符合團體訂票。
- `AC-B3-002`：5 位旅客可建立團體 Booking。
- `AC-B3-003`：20 位旅客可建立團體 Booking。
- `AC-B3-004`：21 位旅客被拒絕。
- `AC-B3-005`：座位必須在同一車廂且連續。
- `AC-B3-006`：無完整連續座位時整筆拒絕。
- `AC-B3-007`：建立失敗不保留座位。
- `AC-B3-008`：成功建立後一次保留全部座位。
- `AC-B3-009`：每位旅客依 B2 規則個別計價。
- `AC-B3-010`：Total Fare 為個別票價加總。
- `AC-B3-011`：付款成功後整筆轉為 `PAID`。
- `AC-B3-012`：付款成功只建立一筆 Order。
- `AC-B3-013`：付款失敗後整筆轉為 `CANCELLED`。
- `AC-B3-014`：付款失敗後釋放全部座位。
- `AC-B3-015`：付款失敗不建立 Order。
- `AC-B3-016`：成功與失敗均留下必要 Audit Entry。
- `AC-B3-017`：付款結果建立對應 Notification Record。
- `AC-B3-018`：G1、B1、B2 Regression Tests 全部通過。
- `AC-B3-019`：文件、API Example 與 Business Rules 已更新。

---

## 26. B3 Reference Solution 要求

版本識別：

```text
B3 - Group Booking
```

Git Tag：

```text
b3-group-booking
```

建議新增：

- Group Booking Schema。
- Group Booking Router。
- Group Booking Service。
- Consecutive Seat Policy 或 Seat Service 擴充。
- Group Payment Flow。
- Unit Tests。
- Integration Tests。
- Business Rules 更新。
- API Examples 更新。

不得：

- 拆成微服務。
- 導入外部資料庫。
- 建立通用 Workflow Engine。
- 全面重寫一般 Booking。
- 移除 B0 既有 Change、Refund、Notification、Audit 功能。

---

## 27. 參與者完成度分級

由於 B3 僅有約 13 分鐘，不要求所有小組一定完成完整 Reference Solution。

### Level 1：Analysis Complete

- Gates 1 與 2 完成。
- Impact Analysis 合理。
- Test Strategy 完整。
- 未完成 Code。

### Level 2：Core Flow Complete

- Group Booking 建立及連續座位完成。
- 主要 Unit Tests 通過。
- 付款補償或文件尚未完整。

### Level 3：Delivery Complete

- 建立、付款成功、付款失敗補償均完成。
- Regression Tests 通過。
- 文件與交付摘要完成。

工作坊不應只以 Level 3 為成功。重點是 Agent 是否依 Gate 受控執行，以及人員是否能有效治理。

---

## 28. Facilitator Reveal Sequence

建立 `04-task-reveal-sequence.md`，至少包含：

```text
Brownfield 分組完成
  ↓
個人 Agent 分析 6 分鐘
  ↓
Shared Context 5 分鐘
  ↓
揭露 B1，8 分鐘
  ↓
揭露 B2，11 分鐘
  ↓
宣布 Digital Worker 規則
  ↓
揭露 B3，13 分鐘
  ↓
交付摘要 4 分鐘
```

每階段標示：

- 開始 cue。
- 時間提醒。
- 停止條件。
- 延遲時的降級策略。
- 何時發放 Hint。

---

## 29. Progressive Hints

### B1 提示

- Hint 1：從失敗測試、Rule ID 與 Discount Policy 三者交叉驗證。
- Hint 2：確認問題是規則實作還是測試期待值錯誤。
- Hint 3：指出 Fare / Discount 模組，不給修正 Code。

### B2 提示

- Hint 1：先列出每位旅客可能符合的所有 Candidate。
- Hint 2：折扣率數值越低，對旅客越有利。
- Hint 3：確認 Booking Change 是否共用相同計價政策。

### B3 提示

- Hint 1：先確認人數、座位與付款三個 Atomic Boundary。
- Hint 2：連續座位可使用同一車廂排序後掃描。
- Hint 3：付款失敗需要釋放座位且不可建立 Order。

每項還必須提供「時間不足提示」，協助小組停止擴充並完成可展示產出。

---

## 30. Timebox 與停止規則

### B1

時間到仍未修復：

- 發 Hint 3。
- 允許小組只完成 Root Cause、Impact Analysis 及修正計畫。
- 主持人可切換到 B1 Recovery Baseline，再進入 B2。

### B2

時間到仍未完成：

- 要求保留 Policy Design、Test Cases 及文件更新清單。
- 切換到 B2 Recovery Baseline，再進入 B3。

### B3

時間到：

- 立即停止新增功能。
- Agent 產生 Delivery Summary。
- 標示完成度 Level 1、2 或 3。
- 記錄未完成項目，不強行修完。

工作坊流程優先於個別小組把所有 Code 完成。

---

## 31. Reference Solution 測試策略

### B1

- 延續 B0 測試。
- 將唯一受控 Bug 造成的 Manifest 全部失敗修正為通過；全部 28 項原 G1 Regression 與全部 B0 新增測試均須通過。
- 不增加大量新測試。

### B2

新增代表性組合測試，至少涵蓋：

- 無優惠。
- 學生。
- 提前購票。
- Corporate。
- 學生 + 提前。
- Corporate + 提前。
- 三項同時符合。
- 混合 Passenger Booking。
- Change Booking 重新計價。

### B3

新增：

- 人數邊界。
- 連續座位成功及失敗。
- 建立時 Atomicity。
- 付款成功。
- 付款失敗補償。
- Fare Policy Regression。
- Audit / Notification。
- API Integration。

B3 全部測試建議控制在 55 至 75 個以內，避免無意義膨脹。

完整測試執行目標仍小於 10 秒。

---

## 32. 版本矩陣

建立 `11-b0-to-b3-version-matrix.md`：

必要欄位：

```text
Capability / Rule
B0
B1
B2
B3
Primary Tests
Primary Documents
```

必須清楚表示：

- B0 學生票錯誤。
- B1 修復學生票。
- B2 導入最有利單一優惠。
- B3 加入團體訂票及付款補償。

此矩陣不可放入 Participant Package。

---

## 33. 自動驗證要求

每個版本都必須獨立執行：

```bash
python --version
pip install -r requirements.txt
pytest -q
python -c "from smart_ticket.main import app; print(app.title)"
```

### B1 預期

```text
All tests pass.
Student fare = 75%.
All 28 original G1 regression tests and all B0-added tests pass; every manifest failure is restored.
No skip.
No xfail.
```

### B2 預期

```text
All tests pass.
No discount stacking.
Best single discount selected per passenger.
No skip.
No xfail.
```

### B3 預期

```text
All tests pass.
Group booking boundaries pass.
Consecutive seat rules pass.
Payment failure compensation passes.
All regressions pass.
No skip.
No xfail.
```

另需使用 TestClient 完成各版本主要 API Smoke Test。

---

## 34. Participant Leakage Check

交付前，Coding Agent 必須確認：

- 任務卡不含解答檔案位置。
- 任務卡不含完整 Impact Analysis。
- B2 任務卡不含實作演算法。
- B3 任務卡只提供業務定義，不提供完整 Seat Algorithm。
- Participant Package 不含 B1、B2、B3 Reference Solution。
- Participant Package 不含 Acceptance Test Map 完整答案。
- Facilitator Hint 與 Evaluation 文件分離。

---

## 35. Coding Agent 最終回報格式

```markdown
# Brownfield 任務卡與 B1-B3 產製結果

## 產製檔案

## 任務揭露順序

## B1 摘要與驗證結果

## B2 摘要與驗證結果

## B3 摘要與驗證結果

## Regression Test 結果

## Acceptance Criteria Traceability

## Timebox 校正

## Participant Leakage Check

## 與 B0 及上位規格的一致性檢查

## 已知限制

## Final Decision
```

Final Decision 僅可為：

- PASS FOR WORKSHOP USE
- FAIL

---

## 36. 完成條件

本階段只有在以下條件全部成立時才算完成：

- 三張 Participant 任務卡已分別完成。
- 任務依 B1、B2、B3 漸進揭露。
- B1 為最小安全 Bug Fix。
- B2 正確實作不可疊加、逐位旅客採最有利單一優惠。
- B3 正確實作 5 至 20 人團體訂票。
- B3 只接受同一車廂連續座位完整區段。
- B3 建立及付款失敗均不留下不完整狀態。
- B1、B2、B3 均有獨立 Reference Solution。
- 每個版本均可安裝、啟動及測試。
- 各版本 Regression Tests 皆通過。
- 無 Skip、無 XFail、無未知失敗。
- Participant、Facilitator、Evaluation 內容已隔離。
- Timebox 與 Recovery Baseline 已定義。
- B3 允許 Level 1 至 Level 3 的不同完成度。
- Agent 從 Teammate 自然演化為 Digital Worker。
- Final Decision 為 `PASS FOR WORKSHOP USE`。
