# Agentic Software Development Evolution Workshop
# B0 Brownfield Repository 演化產製指令書

> 目標讀者：負責將 G1 Greenfield Reference MVP 演化為 B0 Brownfield Repository 的 Coding Agent
>
> 使用時機：G1 已完成、Validation Report 為 PASS，且準備建立 Time Skip 後的統一 Brownfield 素材。
>
> 上位規格：
>
> - `00_Agentic工作坊素材產製總控指令書.md`
> - `01_技術棧與Repository標準指令書.md`
> - `02_Greenfield_Starter_Kit產製指令書.md`
> - `03_G1_Greenfield_Reference_MVP產製指令書.md`

---

## 已核准變更：2026-10-05 B0 Regression Gate（方案 A）

使用者於 2026-10-05 以原文「套用」核准 [B0 Regression Gate 修正提案](../planning/b0-regression-gate-proposal.md) 的方案 A。本指令書據此取代原「精確一項測試失敗／全部 G1 在 B0 通過」門檻：一個受控 Bug，可造成多項已核實的測試失敗；完整實測失敗集合須與 Intentional Failure Manifest 完全一致，零非預期失敗。保留全部 28 項原 G1 Regression 與正確斷言，B1 修復後全部原 G1 及 B0 新增測試恢復通過。28 是原 G1 案例數，不是 B0／B1 全套數。

本變更不代表 B0 已建立、測試或驗收，亦不核准其他商業規則變更。診斷修復副本、Manifest 與完整因果證據僅供 Evaluation／Agent Production 使用，不發入 Participant。
## 1. 任務目標

將正確且穩定的 G1 Greenfield Reference MVP，演化為可供所有參與者共同接手的 **B0 Brownfield Repository**。

B0 必須讓參與者清楚感受到：

```text
這仍然是 Greenfield 階段的 Smart Ticket Platform
        ↓
但已經經過一段時間的功能增加與多人維護
        ↓
系統不再能只靠快速閱讀少數檔案理解
        ↓
開始需要 Repository Understanding、Impact Analysis 與 Shared Context
```

B0 的目的不是製造混亂，而是提供一個：

- 規模適中。
- 可以啟動。
- 大部分測試通過。
- 有合理歷史演進。
- 含少量受控技術債。
- 含有限文件落差。
- 足以支援 Bug、規則變更及新功能任務。

的中型 Brownfield 專案。

---

## 2. B0 在工作坊中的角色

Time Skip 後，所有參與者停止使用自己的 Greenfield Repository，統一取得 B0。

B0 用於兩個成熟度階段：

### Teammate 階段

每位成員使用自己的 Agent 獨立分析：

- Repository 結構。
- 商業規則。
- 可能的影響範圍。
- 文件與程式落差。
- 風險與資訊缺口。

小組再比較不同 Agent 的結果，建立 Shared Context。

### Digital Worker 階段

小組選定主要 Agent，在人員 Review、Approve、Reject 與 Challenge 下執行修改。

因此 B0 必須同時支援：

- 個人獨立分析。
- 小組結果比較。
- Agent 主導修改。
- 人員治理與驗證。

---

## 3. 產製輸出

Coding Agent 必須建立：

```text
02-time-skip/
├── participant/
│   ├── 01-time-skip-announcement.md
│   ├── 02-company-growth-summary.md
│   └── 03-brownfield-handover.md
└── facilitator/
    ├── 01-transition-script.md
    └── 02-repository-delta-explanation.md

03-brownfield/
├── participant/
│   ├── repository/
│   │   └── smart-ticket-b0/
│   ├── 01-system-context.md
│   ├── 02-known-constraints.md
│   ├── 03-individual-analysis-sheet.md
│   └── 04-shared-context-template.md
├── facilitator/
│   ├── 01-b0-facilitation-notes.md
│   ├── 02-progressive-repository-hints.md
│   └── 03-controlled-debt-map.md
└── evaluation/
    ├── 01-b0-validation-report.md
    ├── 02-g1-to-b0-delta.md
    ├── 03-b0-module-map.md
    ├── 04-b0-rule-traceability.md
    └── reference-baseline/
        └── smart-ticket-b0-clean-copy/
```

本指令只建立 B0 與 Time Skip 素材，不建立 B1、B2、B3 的解答。

---

## 4. Time Skip 設定

故事時間快轉設定為：

```text
G1 上線後 12 個月
```

選擇 12 個月而不是模糊的「一段時間」，以便所有素材使用一致背景。

在這 12 個月中，Smart Ticket Platform 經歷：

- 使用人數增加。
- 從單純購票擴充至會員、優惠、改票、退票與通知。
- 不同工程師陸續修改程式。
- 商業規則增加。
- 測試及文件持續累積。
- 部分設計決策已過時，但尚未全面重構。

Time Skip 文件不可聲稱系統已達正式生產等級，也不可引入真實營運數據。

---

## 5. B0 規模要求

B0 應包含約 **35 至 45 個具實質內容的 Python 與測試檔案**。

不計入：

- 空白 `__init__.py`。
- Markdown 文件。
- 設定檔。
- 無內容占位檔案。

建議範圍：

```text
Production Python Files：22 至 28
Test Files：13 至 17
總實質程式與測試檔案：35 至 45
```

完整 `pytest` 目標執行時間仍應小於 8 秒。

不得為了達成檔案數量而切成大量只有數行的檔案。

---

## 6. B0 功能範圍

B0 必須保留 G1 全部功能，並新增以下已存在的能力。

### 6.1 Member

支援：

- 一般會員 `STANDARD`。
- 企業會員 `CORPORATE`。
- 會員 ID 可附加於 Booking。
- 非會員仍可訂票。

B0 初始企業會員優惠為 95%，但此優惠在 B0 的套用方式可以先保持簡單。

### 6.2 Advance Purchase Discount

支援：

- 出發日前至少 14 天購票，可套用 85% 提前購票優惠。
- B0 以固定 Clock 或可注入 Today Provider 計算，測試不得依賴真實當日。

### 6.3 Booking Change

支援簡化改票：

- 僅限已付款 Booking。
- 可改至另一路線相同旅客數的 Trip。
- 目標 Trip 必須有足夠座位。
- 不處理補價或退款，僅記錄 Fare Difference。
- 改票成功後調整原班次與新班次座位。

### 6.4 Refund

支援簡化退票：

- 僅限已付款 Booking。
- 退票後 Booking 狀態為 `REFUNDED`。
- 釋放原保留座位。
- 建立 Refund Record。
- 不連接真實金流。

### 6.5 Notification

支援：

- 付款成功通知。
- 改票成功通知。
- 退票成功通知。
- 只建立 Notification Record，不實際寄送 Email 或簡訊。

### 6.6 Seat Assignment

支援簡化座位配置：

- 一般訂票為每位旅客指派唯一 Seat ID。
- Seat ID 可以使用固定編號序列。
- 一般訂票不保證相鄰座位。
- B0 尚未支援團體相鄰座位。

### 6.7 Audit Log

記錄：

- Booking Created。
- Payment Completed。
- Booking Changed。
- Booking Refunded。

Audit Log 只需 In-Memory，不需要使用者身分驗證。

---

## 7. B0 不可提前實作的能力

B0 不得實作：

- 團體訂票 5 至 20 人規則。
- 相鄰座位保證。
- 團體付款失敗整筆 Rollback 的完整新流程。
- 多個優惠不可疊加且採最有利優惠的正式政策。
- B2、B3 的標準答案。

B0 可以具備足以讓後續任務擴充的介面與模組，但不可直接完成任務。

---

## 8. B0 Domain 擴充

至少新增或擴充以下 Domain 概念：

- `MemberType`
- `Member`
- `DiscountType`
- `DiscountResult`
- `SeatAssignment`
- `RefundRecord`
- `NotificationRecord`
- `AuditEntry`
- `BookingStatus.REFUNDED`

建議新模組：

```text
src/smart_ticket/domain/
├── members.py
├── discounts.py
├── seats.py
├── refunds.py
├── notifications.py
└── audit.py
```

可以因合理設計合併少數模組，但不得將所有新增能力塞回原本 `models.py`。

---

## 9. B0 Application 擴充

至少新增：

- `MemberService`
- `ChangeBookingService`
- `RefundService`
- `NotificationService`
- `SeatService`
- `AuditService`

Discount 計算可以採：

- 擴充 `FarePolicy`。
- 或新增 `DiscountPolicy` 並由 Fare Policy 使用。

選擇必須記錄於 Architecture Decision Record。

---

## 10. B0 API 擴充

除 G1 API 外，至少加入：

```text
GET  /members/{member_id}
POST /bookings/{booking_id}/change
POST /bookings/{booking_id}/refund
GET  /bookings/{booking_id}/notifications
GET  /bookings/{booking_id}/audit-log
```

可加入：

```text
GET /bookings/{booking_id}
```

B0 不需要建立會員申請或登入 API，Member 使用 Seed Data。

---

## 11. B0 Seed Data 擴充

保留 G1 的 T001 至 T004，並新增至少 4 個 Trip，使系統具有更多路線及座位情境。

建議新增：

```text
T005：台北 → 台中，Base Fare 750，可售座位 6
T006：台北 → 高雄，Base Fare 1,400，可售座位 18
T007：台中 → 台北，Base Fare 700，可售座位 10
T008：高雄 → 台中，Base Fare 800，可售座位 4
```

新增固定 Member Seed：

```text
M001：STANDARD
M002：CORPORATE
M003：STANDARD
```

所有日期、購票時間及出發時間必須固定並可測試。

不得依賴目前系統日期。

---

## 12. 新增商業規則

### Member

- `MEMBER-001`：Booking 可以不綁定 Member。
- `MEMBER-002`：有效 Member ID 可被附加至 Booking。
- `MEMBER-003`：Corporate Member 的企業優惠率為 95%。

### Advance Purchase

- `FARE-005`：購票日至出發日相差至少 14 天時，具備 85% 提前購票優惠資格。
- `FARE-006`：未滿 14 天不得取得提前購票優惠。

### Change Booking

- `CHANGE-001`：只有已付款 Booking 可改票。
- `CHANGE-002`：新 Trip 必須有足夠座位。
- `CHANGE-003`：改票成功後釋放原 Trip 座位並保留新 Trip 座位。
- `CHANGE-004`：B0 只記錄 Fare Difference，不執行補價或退款。

### Refund

- `REFUND-001`：只有已付款 Booking 可退票。
- `REFUND-002`：退票後 Booking 狀態為 `REFUNDED`。
- `REFUND-003`：退票成功後釋放座位。
- `REFUND-004`：退票建立唯一 Refund Record。

### Notification

- `NOTIFY-001`：付款成功建立通知紀錄。
- `NOTIFY-002`：改票成功建立通知紀錄。
- `NOTIFY-003`：退票成功建立通知紀錄。

### Seat

- `SEAT-001`：同一 Trip 內 Seat ID 不可重複配置。
- `SEAT-002`：一般 Booking 不保證相鄰座位。

### Audit

- `AUDIT-001`：Booking Created 必須留存 Audit Entry。
- `AUDIT-002`：Payment、Change、Refund 成功後必須留存 Audit Entry。

---

## 13. B0 的受控折扣設計

B0 的折扣處理刻意保留「歷史演變痕跡」。

### B0 現況

- 成人票：100%。
- 學生票：預期應為 75%，但 B0 程式中受控注入為 85%。
- 提前購票：85%。
- Corporate Member：95%。

B0 尚未正式定義多優惠同時符合時的最有利政策。

為避免 B0 在主任務揭露前就完全失效：

- 現有流程採「依既有條件順序選擇第一個符合的優惠」。
- 文件對優惠優先順序描述不完整。
- 程式可正常執行。
- 大部分測試通過。
- 學生票錯誤可被一項或多項明確測試揭露；所有受影響失敗須列入已核實的 Intentional Failure Manifest。

此設計用於後續：

1. B1 修復學生票錯誤。
2. B2 導入「不可疊加、採最有利單一優惠」政策。

---

## 14. 受控 Bug 注入

B0 必須注入且只注入一個主任務要求的明確功能 Bug：

```text
BUG-B0-001：學生票折扣被錯誤設定為 85%，正確應為 75%。
```

要求：

- Bug 必須位於 Fare / Discount Policy 的合理位置。
- 不得在 Router 中硬編碼。
- 不得同時在多處重複 85% 造成無謂搜尋。
- 至少有一個失敗測試可揭露錯誤；同一 Bug 導致的所有失敗均須逐項列明，不能限定只允許一項。
- 失敗測試名稱不可直接寫出修正程式碼，但可表達正確規則。
- 其他不相關測試必須通過。

建議 B0 初始測試結果：

```text
N failed（N = 已核實 Manifest 項目數且 N >= 1）, 其餘通過；零非預期失敗
```

不得使用 Skip、XFail 或隱藏失敗。

---

## 15. 受控技術債

B0 應包含 **3 項** 受控技術債，不多不少。

### DEBT-001：Discount Policy 成長痕跡

- 原本簡單 Fare Policy 已因新增優惠而出現條件順序。
- 仍可閱讀及測試。
- 尚未抽象為可組合規則引擎。
- B2 可要求 Agent 改善，但不強制全面重構。

### DEBT-002：Notification 使用同步呼叫

- Payment、Change、Refund Service 直接呼叫 Notification Service。
- 對目前規模可接受。
- 產生一些依賴耦合。
- 不要求參與者導入 Message Queue。

### DEBT-003：文件中的 Change Booking 金額處理略落後

- 程式已記錄 Fare Difference。
- 一份非核心文件仍描述「改票不處理金額差異」。
- 主要 Business Rule 文件必須正確。
- 這是刻意的有限文件落差，用於 Context Verification。

技術債不得造成多人無法理解系統，也不得要求在本次工作坊全部解決。

---

## 16. 文件落差

只允許 **2 項** 受控文件落差：

1. `docs/change-booking-guide.md` 未更新 Fare Difference 記錄行為。
2. `docs/discount-overview.md` 未清楚定義多優惠符合時的優先順序。

不得讓以下文件錯誤：

- README 的啟動及測試方式。
- API Contract。
- Greenfield 核心規則。
- B0 主要 Business Rules 清單。
- Participant Handover 的已知限制。

Participant 不應一開始被直接告知哪兩份文件有落差，只能被提醒：

> 文件可作為 Context，但重要結論應由程式與測試交叉驗證。

Facilitator 與 Evaluation 必須擁有完整落差清單。

---

## 17. Architecture Decision Records

B0 至少建立 3 份 ADR：

```text
docs/adr/001-use-in-memory-repositories.md
docs/adr/002-introduce-discount-policy.md
docs/adr/003-record-notifications-synchronously.md
```

每份 ADR 包含：

- Context。
- Decision。
- Consequences。
- Status。

ADR 不應直接告訴參與者後續任務答案，但應提供合理歷史脈絡。

---

## 18. Git History 規格

若可建立 Git Repository，B0 必須延續 G1 History，而非重新初始化。

建議 Commit：

```text
feat: add member profiles to bookings
feat: add advance purchase discounts
feat: support booking changes
feat: support refunds and notifications
feat: assign seats to bookings
feat: add booking audit entries
docs: record platform evolution decisions
refactor: consolidate fare and discount calculation
```

受控 Bug 可自然存在於最後一個 Refactor Commit 中，但 Commit Message 不可寫「introduce bug」。

建立 Tag：

```text
b0-brownfield-baseline
```

若無法建立 Git History，產生：

```text
docs/history/commit-timeline.md
```

並明確標示為模擬歷史，不得聲稱為真實 Git Commit。

---

## 19. B0 測試策略

B0 應有約 30 至 45 個測試，包括：

- 全部 28 項原 G1 Regression Tests；保留原測試 body／assert 與正確商業斷言。
- Member Tests。
- Advance Purchase Tests。
- Change Booking Tests。
- Refund Tests。
- Notification Tests。
- Seat Assignment Tests。
- Audit Tests。
- API Integration Tests。

初始執行結果必須符合：

- 所有失敗均為 `BUG-B0-001` 已核實 Manifest 所列 node ID，實測集合完全相等。
- 其餘測試通過。
- 無 Skip。
- 無 XFail。
- 無未知 Warning。

失敗測試建議名稱：

```python
def test_student_fare_uses_the_published_student_rate():
    ...
```

測試斷言可以驗證 75%，但不得直接指出程式檔案或行號。

---

### 19.1 Intentional Failure Manifest 與完整套件判定

Manifest 必須逐項包含：完整 pytest node ID、Rule ID／AC、正確 expected value、Bug 下 actual value、因果證據（Diff、共用計價呼叫路徑及只修學生率後的結果）。原 G1 已證實有五項受影響案例；B0 新增案例若受影響，交付前須用實際結果追加，不能把任何學生相關失敗自動接受為預期。

正式 B0 執行完整套件，記錄所有 passed／failed／skipped／xfailed／warnings、traceback、exit code，並以實測 failed node ID 集合與已核實 Manifest 做雙向相等比對。所有不在集合內的測試通過，無 Skip／XFail／未知 Warning；失敗數不要求精確一項。不能只確認每個實際失敗都在清單，而忽略清單中的預期失敗未出現。

### 19.2 G1 上下文適配與隔離診斷修復驗證

原 28 項測試 body／assert 與正確商業期待值保留。允許 fixture／依賴組裝適配，須留 Diff 與理由：原 G1 測試使用 T001–T004 Seed、非提前優惠的固定 Clock、member 預設 None，但學生仍走正式 B0 計價，不繞過 Bug、不另設正確計價分支。新增 B0 能力另以完整 Seed、會員與優惠邊界驗證；保留原精確班次集合與容量斷言。

Evaluation 必須另建隔離診斷副本，從同一正式 B0 快照複製，**只修正學生率 85%→75%**，不得修改測試或其他政策。用相同套件證明原 28 項 G1 Regression 與全部 B0 新增測試通過，記錄唯一修復 Diff、指令、輸出及與 Manifest 的因果對照。診斷副本不作為本階段 B1 交付物，不提供學員；正式 Participant B0 與要求的 clean-copy 保留 Bug，不被診斷修復覆蓋。

若只修學生率後仍有失敗，視為存在非預期問題，不得驗收；完成診斷後重新核對正式 B0 仍具相同 Bug 及 Manifest 失敗集合。B1 後續正式產製再執行完整修復驗收，不以診斷副本冒充 B1 已完成。

## 20. Time Skip Participant 文件

### 20.1 `01-time-skip-announcement.md`

控制在約 300 字內，內容：

- 時間已經過 12 個月。
- 系統與團隊規模成長。
- 個人 Greenfield 成果停止使用。
- 全員接手同一 B0。
- Agent 角色從 Tool 升級為 Teammate。

### 20.2 `02-company-growth-summary.md`

列出：

- 新增會員、優惠、改退票、通知、座位及 Audit。
- 系統從少數檔案增加至中型 Repository。
- 文件與歷史決策均可作為 Context。
- 不保證所有文件與程式完全同步。

### 20.3 `03-brownfield-handover.md`

只提供參與者接手所需資訊：

- 安裝與測試方式。
- B0 版本 ID。
- 主要功能清單。
- 目前有若干測試失敗，需要小組分析是否具有共同原因；不預告錯誤數、根因、位置或完整影響矩陣。
- 先不要直接修改程式。
- 先完成個人 Agent 分析。

不可揭露：

- Bug 根因。
- Bug 檔案位置。
- 兩項文件落差的具體位置。
- B2、B3 任務答案。

---

## 21. Brownfield Participant Context 文件

### 21.1 `01-system-context.md`

包含：

- 系統目的。
- 主要模組。
- 分層架構。
- 核心資料流。
- 新增功能概覽。
- 查閱 ADR 與測試的建議。

不要列出所有檔案，也不要提供任務解答。

### 21.2 `02-known-constraints.md`

包含：

- In-Memory only。
- 不可加入外部服務。
- API 相容性應維持。
- 不應全面重寫系統。
- 優先以現有測試與模組完成修改。
- 文件必須與最終行為同步。

### 21.3 `03-individual-analysis-sheet.md`

要求每位參與者與自己的 Agent 產出：

```text
系統模組摘要
失敗測試解讀
可能根因
受影響檔案
相關規則
資訊缺口
建議調查順序
風險
```

此階段禁止直接修改程式。

### 21.4 `04-shared-context-template.md`

小組整合個人分析，形成：

```text
共同事實
仍有分歧的判斷
已驗證證據
任務範圍
核准修改區域
不可修改區域
測試計畫
主要 Agent 執行計畫
Human Approval Gate
```

---

## 22. Facilitator 專用素材

### 22.1 B0 Facilitation Notes

包含：

- B0 的正確架構摘要。
- Bug 根因。
- 技術債清單。
- 文件落差清單。
- 預期 Agent 可能產生的錯誤判斷。
- 哪些差異可接受。

### 22.2 Progressive Repository Hints

為以下問題準備三級提示：

- 不知道從哪裡開始。
- 只看文件不看測試。
- 只修測試不修程式。
- 找到 85% 但不確定正確規則。
- Agent 建議全面重寫 Fare 模組。
- 小組分析結果互相矛盾。

三級提示原則：

```text
Hint 1：方向提示
Hint 2：證據來源提示
Hint 3：模組或檔案群組提示
```

不得直接提供修正 Code。

### 22.3 Controlled Debt Map

欄位：

```text
Debt ID
Location
Historical Reason
Learning Purpose
Participant Visibility
Must Fix Now
Acceptable Handling
```

---

## 23. G1 到 B0 Delta

建立 `02-g1-to-b0-delta.md`，至少包含：

- 新增 Domain。
- 新增 Service。
- 新增 API。
- 新增 Test。
- 新增文件。
- 商業規則變更。
- 技術債。
- 文件落差。
- Bug 注入。
- G1 Regression 結果。

此文件屬 Evaluation，不可交給 Participant。

---

## 24. B0 Module Map

建立完整模組地圖：

```text
Module
Responsibility
Upstream Dependency
Downstream Dependency
Primary Rules
Primary Tests
Related Documentation
Expected Future Change
```

用於評估 Agent 的 Repository Understanding 是否正確。

---

## 25. B0 自動驗證

Coding Agent 必須實際執行：

```bash
python --version
pip install -r requirements.txt
pytest -q
python -c "from smart_ticket.main import app; print(app.title)"
```

並使用 TestClient 驗證：

- G1 Happy Path 仍可執行。
- Corporate Member Booking 可建立。
- Advance Purchase 行為可執行。
- Change Booking 可執行。
- Refund 可執行。
- Notification Record 可查詢。
- Audit Log 可查詢。

預期 Test Result：

```text
One controlled bug: BUG-B0-001. All failed node IDs exactly match the verified Intentional Failure Manifest. Zero unexpected failures.
All other tests pass.
No skip.
No xfail.
```

若出現任何不在已核實 Manifest 中的失敗、Manifest 項目未實際失敗或缺少因果證據，不得交付。pytest 因預期失敗回傳非零 exit，必須如實記錄；不得冒稱完整套件一般 PASS。

---

## 26. B0 Validation Report

建立 `01-b0-validation-report.md`：

```markdown
# B0 Validation Report

## Version

## Environment

## File Count

## Dependency Installation

## Application Import

## Test Summary

## Intentional Failure Verification

## Intentional Failure Manifest and Set Equality

## Isolated Diagnostic Repair Verification

## API Smoke Tests

## G1 Regression

## Rule Traceability

## Controlled Technical Debt

## Controlled Documentation Gaps

## Participant Leakage Check

## Final Decision
```

Final Decision 僅可為：

- PASS AS BROWNFIELD BASELINE
- FAIL

只有受控 Bug 數為一、完整套件失敗 node ID 集合與已核實 Manifest 完全一致、零非預期失敗、隔離診斷修復副本完整通過，且其他 Gate 全部符合，才能判定 `PASS AS BROWNFIELD BASELINE`。這是預期失敗基線的 Evaluation 決策，不代表正式 B0 pytest exit 為零。

---

## 27. 難度與時間校正

在正式交付前，Coding Agent 必須評估普通工程師搭配 Coding Agent 是否能：

- 3 分鐘內啟動並執行測試。
- 5 分鐘內取得初步 Repository Summary。
- 5 分鐘內找出學生票問題的合理候選區域。
- 經過提示後，在 8 分鐘內完成 B1 修復與驗證。

若需要閱讀大量不相關檔案才能完成，應降低複雜度。

若 Agent 一次搜尋就直接得到完整答案，仍可接受作為暖身 Bug，但小組分析素材必須要求提出證據、影響範圍與規則追溯，而不只是修改常數。

---

## 28. Coding Agent 最終回報格式

```markdown
# B0 Brownfield Repository 產製結果

## G1 → B0 演化摘要

## 新增功能與模組

## 實質檔案數量

## 新增商業規則

## Intentional Bug

## Controlled Technical Debt

## Controlled Documentation Gaps

## Test Result

## API Smoke Test

## G1 Regression Result

## Participant / Facilitator / Evaluation 隔離檢查

## 難度與時間校正

## Final Decision
```

不得隱藏額外失敗，也不得將未執行的驗證標示為通過。

---

## 29. 完成條件

B0 只有在以下條件全部成立時才算完成：

- 從 G1 自然演化，而非重建無關專案。
- 保留 G1 API 與核心行為相容性。
- 實質 Python 與 Test 檔案約 35 至 45 個。
- 新增會員、提前購票、改票、退票、通知、座位及 Audit。
- 尚未實作團體訂票與最有利優惠政策。
- 僅注入 `BUG-B0-001` 一項主任務 Bug。
- 僅包含 3 項受控技術債。
- 僅包含 2 項受控文件落差。
- 完整套件所有失敗與已核實 Intentional Failure Manifest 完全一致，僅由一個受控 Bug 造成，零非預期失敗。
- 全部 28 項原 G1 Regression 保留正確斷言；正式 B0 的受影響失敗逐項揭露，其餘通過；Evaluation 隔離診斷修復副本中全部 28 項及 B0 新增測試均通過。
- 無 Skip、無 XFail、無未知 Warning。
- Participant 不知道錯誤位置及答案。
- Facilitator 與 Evaluation 具備完整地圖。
- 個人分析與 Shared Context 範本已完成。
- B0 可支援後續 B1、B2、B3 任務。
- Final Decision 為 `PASS AS BROWNFIELD BASELINE`。
