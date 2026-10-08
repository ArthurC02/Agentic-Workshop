# Agentic Software Development Evolution Workshop
# Digital Worker 治理與操作規則產製指令書

> 目標讀者：負責建立 Digital Worker 階段 Participant、Facilitator 與 Evaluation 素材的 Coding Agent
>
> 使用時機：B0、B1、B2、B3 任務與 Reference Solution 規格已確立後，開始建立 B3 執行時的人機治理機制。
>
> 上位規格：
>
> - `00_Agentic工作坊素材產製總控指令書.md`
> - `01_技術棧與Repository標準指令書.md`
> - `04_B0_Brownfield_Repository演化產製指令書.md`
> - `05_Brownfield任務卡與B1-B3產製指令書.md`

---

> 2026-10-09 已核准變更：學員不寫、不讀程式；本文中人員「審查 Diff」改為請 Agent 以白話回答固定審查問題並逐條核對驗收對照表；Gate 回報、Review、Delivery 與 Audit 由 Agent 依格式寫進 `notes/`，學員只在表單記錄決定。見 [00 總控指令書 §1](00_Agentic工作坊素材產製總控指令書.md#1-專案目標)。

## 1. 任務目標

建立 Digital Worker 階段的操作規則，使 B3 團體訂票任務不只是「讓 Agent 自動寫程式」，而是一次可控、可審查、可追溯的 Agent 主導交付實驗。

本階段必須呈現以下轉變：

```text
Greenfield / Tool
人決定、人拆解、Agent 協助執行

Brownfield / Teammate
人與 Agent 共同分析及決策

Digital Worker
Agent 主導分析、設計、實作、測試與文件
人負責設定邊界、核准、挑戰、驗證與承擔責任
```

Digital Worker 不代表 Agent 擁有無限制自主權，也不代表人員可以完全不理解結果。

---

## 2. 必須產製的輸出

```text
04-digital-worker/
├── participant/
│   ├── 01-operating-rules.md
│   ├── 02-agent-work-order.md
│   ├── 03-approval-gates.md
│   ├── 04-review-checklist.md
│   ├── 05-delivery-template.md
│   └── 06-exception-response-card.md
├── facilitator/
│   ├── 01-governance-observation-guide.md
│   ├── 02-approval-gate-cues.md
│   ├── 03-exception-injection.md
│   ├── 04-intervention-rules.md
│   └── 05-digital-worker-debrief-notes.md
└── evaluation/
    ├── 01-autonomy-and-governance-rubric.md
    ├── 02-approval-evidence-checklist.md
    ├── 03-digital-worker-audit-template.md
    └── 04-exception-reference-answer.md
```

本指令書只產製治理與操作素材，不修改 B3 商業需求或 Reference Solution。

---

## 3. Digital Worker 固定原則

所有素材必須遵循以下原則：

1. **Agent 主導執行，但不得自行擴大任務。**
2. **人員不直接修改程式碼，但必須理解並審查重要決策。**
3. **所有重大動作必須對應明確 Approval Gate。**
4. **Agent 必須以證據支持結論，不能只提供自信敘述。**
5. **測試通過不是唯一驗收條件，還要驗證規則、範圍、文件與未完成事項。**
6. **Agent 遇到衝突、資訊不足或超出權限時必須停止並升級。**
7. **Agent 不得掩飾失敗、刪除測試或改寫需求來讓結果看似成功。**
8. **最終提交責任仍由人員承擔。**

---

## 4. Participant Operating Rules

建立 `01-operating-rules.md`，內容必須簡潔且可在 2 分鐘內讀完。

### 4.1 人員可以做的事

- 提供需求、Context、Rule 與限制。
- 要求 Agent 解釋理解與假設。
- Challenge Agent 的分析及方案。
- 核准或拒絕執行計畫。
- 審查 Diff、測試、文件與交付摘要。
- 要求 Agent 補充證據或修正。
- 在發現風險時中止 Agent。

### 4.2 人員不可做的事

- 直接修改程式碼。
- 直接替 Agent 補上測試。
- 跳過 Approval Gate。
- 因時間壓力而接受未驗證結果。
- 將 Agent 未確認的說法視為事實。

### 4.3 Agent 可以做的事

- 掃描 Repository。
- 分析需求及影響範圍。
- 提出設計選項。
- 依核准計畫修改程式。
- 建立及執行測試。
- 更新文件。
- 產生交付摘要與未完成事項。

### 4.4 Agent 不可做的事

- 修改核准範圍外的模組。
- 變更既有 API Contract，除非已核准。
- 加入外部服務、資料庫或第三方規則引擎。
- 刪除或弱化既有測試。
- 自行改變商業規則。
- 宣稱未執行的測試已通過。
- 在 Gate 未核准前進入下一階段。

---

## 5. Agent Work Order

建立 `02-agent-work-order.md`，作為小組交給主要 Agent 的正式工作命令。

固定結構：

```markdown
# Digital Worker Work Order

## Mission

## Approved Requirements

## Business Rules

## Approved Context

## Allowed Change Scope

## Prohibited Change Scope

## Required Deliverables

## Required Tests

## Approval Gates

## Stop and Escalate Conditions

## Timebox
```

Work Order 必須引用：

- `TASK-B3-001`
- `GROUP-*`
- `GROUP-PAY-*`
- `GROUP-FARE-*`
- `GROUP-AUDIT-*`
- `GROUP-NOTIFY-*`

Work Order 不可直接內嵌 Reference Solution。

---

## 6. Approval Gate 設計

建立 `03-approval-gates.md`。B3 固定採三個 Gate。

### Gate 1：Requirement Understanding

Agent 必須提交：

- 需求摘要。
- 規則清單。
- 關鍵假設。
- 資訊缺口。
- Out of Scope。
- 需要人員決定的問題。

人員檢查：

- 是否遺漏 5 至 20 人邊界。
- 是否理解同車廂連續座位。
- 是否理解付款失敗整筆取消。
- 是否理解不得部分成功。
- 是否維持 B2 個別旅客優惠政策。

核准選項：

```text
APPROVE
APPROVE WITH CONDITIONS
REJECT AND REVISE
```

### Gate 2：Impact and Design

Agent 必須提交：

- 受影響模組。
- 不受影響模組。
- API Contract。
- Domain Model 變更。
- Seat Assignment 方案。
- Atomicity / Compensation 方案。
- 測試策略。
- 文件更新清單。
- 主要風險。
- 預計修改檔案。

人員檢查：

- 是否避免全面重寫。
- 是否處理建立失敗與付款失敗。
- 是否考慮座位釋放。
- 是否保留 Regression。
- 是否有未核准外部依賴。
- 修改範圍是否合理。

核准後 Agent 才能修改程式。

### Gate 3：Delivery Review

Agent 必須提交：

- 修改摘要。
- 實際修改檔案。
- 測試指令與實際結果。
- Acceptance Criteria 對照。
- Rule Traceability。
- 文件更新。
- 未完成事項。
- 已知風險。
- 建議是否交付。

人員檢查：

- Agent 是否超出範圍。
- 測試結果是否可驗證。
- 是否有 Skip、XFail 或未知失敗。
- 付款失敗補償是否完整。
- 文件是否與程式一致。
- Agent 是否誠實揭露未完成事項。

---

## 7. Gate 回覆短格式

為避免 13 分鐘 B3 任務被長篇討論消耗，每個 Gate 使用短格式：

```markdown
## Gate Decision

Decision: APPROVE | APPROVE WITH CONDITIONS | REJECT AND REVISE

Evidence Reviewed:
- 

Conditions / Required Corrections:
- 

Approver:

Timestamp / Workshop Minute:
```

不要求真實電子簽章。

---

## 8. Stop and Escalate Conditions

Agent 發現以下任一情況時必須停止，不能自行猜測後繼續：

- Requirement 與 Rule ID 衝突。
- Participant 文件與程式行為衝突，且無法由 Test 判定。
- 需要修改核准範圍外的 API Contract。
- 需要新增外部服務或套件。
- 需要移除既有 Regression Test。
- 無法確認付款失敗後的正確狀態。
- 找不到同時滿足座位與 Atomicity 的可行方案。
- 執行測試出現與任務無關的新失敗。
- 修改檔案數量顯著超過 Gate 2 預估。
- 時間不足以完成承諾交付。

Agent 升級時使用：

```markdown
# Escalation

## Trigger

## Evidence

## Impact

## Options

## Recommendation

## Decision Needed
```

---

## 9. Participant Review Checklist

建立 `04-review-checklist.md`，採簡短勾選表。

### Requirement

- [ ] 5 至 20 人邊界已處理。
- [ ] 不允許部分成功。
- [ ] 同車廂連續座位已處理。
- [ ] 付款失敗整筆取消已處理。
- [ ] B2 優惠規則仍適用。

### Scope

- [ ] 未新增外部資料庫或服務。
- [ ] 未全面重寫一般 Booking。
- [ ] 未修改不相關 API。
- [ ] 修改檔案與 Gate 2 計畫一致。

### Quality

- [ ] 建立失敗不保留座位。
- [ ] 付款失敗釋放全部座位。
- [ ] 付款失敗不建立 Order。
- [ ] 成功只建立一筆 Order。
- [ ] Audit 與 Notification 行為符合規則。

### Evidence

- [ ] Agent 提供實際測試結果。
- [ ] 無 Skip、XFail 或未知失敗。
- [ ] Acceptance Criteria 可追溯至 Test。
- [ ] 文件與實作同步。
- [ ] 未完成事項已揭露。

---

## 10. Delivery Template

建立 `05-delivery-template.md`：

```markdown
# Digital Worker Delivery Summary

## Mission Result

## Completion Level

- Level 1: Analysis Complete
- Level 2: Core Flow Complete
- Level 3: Delivery Complete

## Implemented Scope

## Not Implemented

## Files Changed

## Business Rules Covered

## Acceptance Criteria Results

## Test Command and Actual Result

## Documentation Updated

## Risks and Limitations

## Deviations from Approved Plan

## Recommended Decision

APPROVE | CONDITIONAL APPROVAL | REJECT
```

Agent 必須根據實際完成度填寫，不得自動勾選 Level 3。

---

## 11. 例外事件設計

工作坊只有 90 分鐘，因此 Digital Worker 階段只注入 **一個** 例外事件，不能同時加入多個事件。

固定例外：

```text
EXCEPTION-DW-001：主要 Agent 在 Gate 2 提議新增 SQLite，以簡化座位交易與 Rollback。
```

此提議與既定 Constraint 衝突：

```text
本次工作坊必須維持 In-Memory Repository，不可新增外部資料庫。
```

例外事件的目的：

- 測試人員是否真的審查 Agent 方案。
- 測試 Agent 是否遵守 Constraint。
- 呈現「Agent 提出的方案看似合理，但仍可能超出授權」。
- 練習 Reject 或 Approve With Conditions。

主持人只在以下情況注入：

- Agent 自己已提出超範圍方案，主持人直接要求小組處理。
- 若 Agent 未提出，主持人在 Gate 2 後以事件卡詢問：「若 Agent 建議 SQLite，你們是否核准？」

不得真的要求參與者安裝 SQLite 套件或修改技術棧。

---

## 12. Exception Response Card

建立 `06-exception-response-card.md`，要求 Participant 回答：

```markdown
# Exception Response

Exception ID: EXCEPTION-DW-001

## Is the proposal within approved scope?

YES | NO | UNCLEAR

## Evidence

## Risk

## Decision

APPROVE | APPROVE WITH CONDITIONS | REJECT

## Instruction Back to the Agent
```

標準合理決策為 Reject，並要求 Agent 使用現有 In-Memory Repository 設計補償流程。

Participant 若提出其他不新增外部依賴的受控方案，也可接受。

---

## 13. Facilitator Governance Observation Guide

建立 `01-governance-observation-guide.md`，觀察下列行為：

### Agent 行為

- 是否先確認需求。
- 是否揭露假設。
- 是否提出證據。
- 是否等待 Gate 核准。
- 是否超出修改範圍。
- 是否執行測試。
- 是否更新文件。
- 是否揭露未完成事項。

### Human 行為

- 是否先審查再核准。
- 是否 Challenge Agent。
- 是否要求測試證據。
- 是否辨識 SQLite 超範圍提議。
- 是否只看摘要而未看 Diff。
- 是否因時間壓力跳過 Gate。
- 是否能區分「Agent 完成」與「成果可接受」。

### 系統治理需求

主持人同步記錄工作坊暴露的未來平台需求：

- Agent 權限範圍。
- Rule Enforcement。
- Approval Workflow。
- Audit Log。
- Test Evidence。
- Context Versioning。
- Agent Session 管理。
- 成本與執行時間觀測。

---

## 14. Facilitator Approval Gate Cues

建立 `02-approval-gate-cues.md`，以工作坊分鐘為基準。

B3 13 分鐘建議：

```text
00:00 發放 B3 與 Operating Rules
00:01 Agent 開始 Gate 1
00:03 Gate 1 決策
00:03 Agent 開始 Gate 2
00:06 Gate 2 決策及例外事件
00:07 Agent 開始執行
00:11 要求停止擴充並執行測試
00:12 Gate 3 Review
00:13 產生 Delivery Summary
```

若 Agent 在 Gate 回覆過長，主持人提醒使用短格式。

---

## 15. Facilitator Exception Injection

建立 `03-exception-injection.md`，內容包括：

- 事件 ID。
- 注入時機。
- 主持人口播文字。
- 預期 Participant 反應。
- 可接受反應。
- 不可接受反應。
- 何時停止討論。

主持人口播範例：

> 主要 Agent 建議加入 SQLite，認為這樣可以更容易處理座位保留及付款失敗 Rollback。請依照已核准的 Constraint，在 60 秒內做出 Gate 決策並回覆 Agent。

預期：

- 找出與 In-Memory Constraint 衝突。
- Reject 或要求改用現有 Repository 補償流程。
- 不進行長篇資料庫架構討論。

---

## 16. Facilitator Intervention Rules

建立 `04-intervention-rules.md`。

### 可以介入

- Agent 未等待 Gate 即修改程式。
- 人員直接 Coding。
- Agent 刪除測試。
- 小組核准 SQLite。
- 小組無視付款失敗補償。
- Agent 宣稱測試通過但無證據。
- 時間到仍持續擴充。

### 不應介入

- 類別或方法命名不同。
- Agent 提出不同但合理的 In-Memory 設計。
- 小組選擇 Level 1 或 Level 2 完成度。
- 小組拒絕不必要重構。
- Agent 的文件表達風格不同但內容正確。

### 介入方式

優先順序：

```text
提醒既定 Rule
  ↓
要求提出證據
  ↓
要求回到 Approval Gate
  ↓
發放 Hint
  ↓
切換 Recovery Baseline
```

主持人不得直接提供完整解答 Code。

---

## 17. Autonomy and Governance Rubric

建立 `01-autonomy-and-governance-rubric.md`。

評估分為五個面向，每項 0 至 3 分。

### A. Requirement Understanding

- 0：未分析需求即修改。
- 1：只重述需求。
- 2：辨識主要規則與假設。
- 3：完整辨識規則、缺口、範圍及風險。

### B. Plan and Scope Control

- 0：無計畫或大幅超出範圍。
- 1：有計畫但範圍不清楚。
- 2：計畫合理且大致遵守。
- 3：計畫、修改與偏差均可追溯。

### C. Evidence and Quality

- 0：無測試證據。
- 1：只有部分測試或口頭說明。
- 2：主要測試及 Diff 可驗證。
- 3：Acceptance、Regression、文件及風險均有證據。

### D. Human Oversight

- 0：人員未審查即接受。
- 1：形式性核准。
- 2：有 Challenge、Review 與條件式核准。
- 3：能辨識超範圍方案並做出有證據的決策。

### E. Transparency

- 0：掩飾或未揭露失敗。
- 1：只回報成功內容。
- 2：回報未完成及已知限制。
- 3：完整回報偏差、風險、證據與建議決策。

總分只用於回顧，不作為競賽排名。

---

## 18. Approval Evidence Checklist

建立 `02-approval-evidence-checklist.md`，每個 Gate 至少記錄：

```text
Gate ID
Agent Submission
Evidence Reviewed
Human Decision
Conditions
Observed Deviation
Final Status
```

不要求詳細會議紀錄，只要能證明 Gate 不是形式動作。

---

## 19. Digital Worker Audit Template

建立 `03-digital-worker-audit-template.md`：

```markdown
# Digital Worker Audit Record

## Session ID

## Work Order ID

## Agent / Tool Used

## Approved Context Version

## Approved Rules

## Gate Decisions

## Files Changed

## Commands Executed

## Tests Executed

## Exceptions Raised

## Human Interventions

## Final Delivery Decision

## Unresolved Risks
```

此範本不要求平台真的具備 Audit 功能，但用來萃取未來 Agent Platform 需求。

---

## 20. Exception Reference Answer

建立 `04-exception-reference-answer.md`，標準回應至少包含：

- SQLite 提議超出核准技術範圍。
- 本次工作坊的 Persistence 固定為 In-Memory。
- 應 Reject 方案，不是 Reject 整個任務。
- 要求 Agent 使用 Seat Reservation 與 Compensation 完成 Atomicity 模擬。
- 若現有架構不足，可在核准範圍內新增 In-Memory Snapshot、Reservation Token 或明確 Rollback Method。
- 不需建立通用 Transaction Framework。

此文件不得提供給 Participant。

---

## 21. Digital Worker Debrief Notes

建立 `05-digital-worker-debrief-notes.md`，主持人用以下問題收斂：

- Agent 主導後，人員的工作是否真的減少，還是轉為 Review 與治理？
- 哪一個 Gate 最有價值？
- 哪一個 Gate 容易變成形式？
- 若沒有人發現 SQLite 超範圍提議，代表缺少什麼治理能力？
- 測試通過是否足以核准交付？
- 哪些資訊應由平台自動留下 Audit Log？
- 哪些 Rule 可以 Machine-Enforce？
- 哪些決策仍必須由人員判斷？
- 從 Tool 到 Digital Worker，責任是否消失，或只是重新分配？

---

## 22. 工具中立要求

所有文件不得使用特定產品專屬詞彙作為必要流程。

可寫：

- Coding Agent。
- Agent Session。
- Plan。
- Diff。
- Test Result。
- Approval Gate。

不可要求：

- 特定產品的 Plan Mode。
- 特定廠商設定檔。
- 特定 CLI 指令。
- 特定 Subagent 功能。

若 Participant 使用的工具不支援自動修改，仍可以由 Agent 產生 Patch，再由環境套用，但人員不得自行補寫程式。

---

## 23. 時間與壓力控制

Digital Worker 階段不得因治理素材過多而失去實作體驗。

Participant 必讀文件限於：

1. Operating Rules。
2. Work Order。
3. Approval Gates。
4. B3 Task Card。

Review Checklist、Delivery Template 與 Exception Card 在需要時使用。

每個 Gate 應控制在 1 至 3 分鐘內。

若時間不足：

- 優先保留 Gate 1 與 Gate 2。
- Gate 3 至少完成測試證據及未完成事項審查。
- 不追求 Level 3。
- 不刪除例外事件，但可縮短為 30 秒口頭判斷。

---

## 24. 一致性檢查

Coding Agent 產製後必須確認：

- B3 Rule ID 與任務指令書一致。
- Gate 內容與 B3 Acceptance Criteria 一致。
- SQLite 例外確實違反技術棧規格。
- Participant 文件沒有例外標準答案。
- Facilitator 文件沒有進入 Participant Package。
- Evaluation Rubric 不把完成程式量當成唯一成功指標。
- Level 1、2、3 完成度仍適用。
- Agent 主導不等於跳過人員核准。
- 人員不 Coding 不等於人員不必理解。

---

## 25. Coding Agent 最終回報格式

```markdown
# Digital Worker 治理素材產製結果

## 建立的檔案

## Operating Rules 摘要

## Approval Gates

## Stop and Escalate Conditions

## Exception Event

## Governance Rubric

## Participant / Facilitator / Evaluation 隔離檢查

## B3 規則一致性檢查

## Timebox 適配檢查

## 已知限制

## Final Decision
```

Final Decision 僅可為：

- PASS FOR GOVERNED DIGITAL WORKER EXERCISE
- FAIL

---

## 26. 完成條件

本階段只有在以下條件均成立時才算完成：

- Digital Worker 的人機責任邊界明確。
- 人員不得直接 Coding 的規則已寫入 Participant 文件。
- Agent 的允許與禁止行為已定義。
- 三個 Approval Gate 已具備 Input、Review、Decision 與 Evidence。
- Stop and Escalate Conditions 已定義。
- Work Order 可直接交給工具中立的 Coding Agent。
- Delivery Template 可表達 Level 1 至 Level 3。
- 只注入一個 SQLite 超範圍例外事件。
- Participant 能在 60 秒內對例外做出治理決策。
- Autonomy and Governance Rubric 已完成。
- Audit Template 能支援後續平台需求萃取。
- 所有素材符合 13 分鐘 B3 Timebox。
- Participant、Facilitator、Evaluation 已隔離。
- 與 B3 任務規則一致，沒有新增或改寫商業需求。
- Final Decision 為 `PASS FOR GOVERNED DIGITAL WORKER EXERCISE`。
