# Rule Traceability Baseline

> 目標讀者：教材產製 Agent、Repo 維護者、主持人及驗收人員。
> 使用時機：P2 技術基線確認、各版本需求／程式／測試產製及驗收之前。
> 前置條件：閱讀 [共同詞彙](glossary.md)、[一致性規則](consistency-rules.md)、[技術基線](technical-baseline.md) 與 [版本驗證要求](version-validation-requirements.md)。
> 可見性：Facilitator／Evaluation／Agent Production；包含版本答案，不整份提供 Participant。
> 日期：2026-10-05。本表是預期追溯規格，不代表程式或測試已建立或驗證通過。

## 1. 來源與追溯使用方式

- Greenfield 規則：[G0 規格 §6](../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)；實作與驗證依 [G1 規格](../../docs/instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)。
- B0 新增規則：[B0 規格 §12](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)。
- B2／B3 規則：[任務與標準實作規格 §12、§20](../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。
- 全域要求：[總控規格 §7.2](../../docs/instructions/00_Agentic工作坊素材產製總控指令書.md) 與 [技術標準 §10](../../docs/instructions/01_技術棧與Repository標準指令書.md)。

每個 Rule ID 後續須連至 Requirement、實際 Code、實際 Test、Documentation 與 Evaluation。下表 Code Area 與驗證意圖只描述預期；實際檔案、測試名稱、執行指令和結果必須於該版本建立後補入版本追溯文件，不能用此表替代驗證報告。G0 的規則是待實作要求，並非 G0 必須已有全部功能。

## 2. 編號映射與版本語意

本輪依階段規格對齊 `BOOKING-002` 為一般單筆最多 4 位旅客、`BOOKING-003` 為不得超過剩餘座位。舊 [技術標準 §10](../../docs/instructions/01_技術棧與Repository標準指令書.md) 中座位限制的 `BOOKING-002` 引用須映射為 `BOOKING-003`；最多 4 人的商業語意與座位限制均不變。B3 團體端點採 `GROUP-001`／`GROUP-002` 的 5–20 人範圍，一般訂票上限保留，不能把 4 人改成 20 人套用所有 Booking。技術標準已同步此映射，O-03 的處理依據與文件驗證在決策紀錄留證；本表仍不代表實際程式已建立。

學生票正式規則一律 75%；B0 的 85% 是受控 Bug，不是合法折扣政策。B1 修復為 75%，B2 才加入逐位旅客、最有利單一優惠且不得疊加的政策；不得提前在 B0／B1 實作 B2。B3 沿用 B2 計價。所有金額仍採整數，具體演算法與取整行為依來源規格及後續測試固定，不由此表新增。

## 3. 完整 Rule Registry

下列「驗證意圖」均為待建立的驗證，不是已有測試結果。基本規則於 G0 是需求；G1 起是實作要求。B0 起／B2 起／B3 分別表示後續版本持續保留，另有版本差異時以 §2 說明為準。

| Rule ID | 規則語意 | 適用版本 | 預期 Code Area／驗證意圖 |
|---|---|---|---|
| `TRIP-001` | 只可回傳仍有至少一個可售座位的班次。 | G0需求／G1–B3 | Trip Query／篩選及可售座位邊界；逐項依本列規則斷言。 |
| `TRIP-002` | Origin 與 Destination 是可選篩選條件；若提供，必須精確符合 Seed Data 中的站點名稱。 | G0需求／G1–B3 | Trip Query／篩選及可售座位邊界；逐項依本列規則斷言。 |
| `BOOKING-001` | 每筆訂票至少包含一位旅客。 | G0需求／G1–B3 | Booking Domain/Application／人數、座位保留與初始狀態；逐項依本列規則斷言。 |
| `BOOKING-002` | 一般單筆訂票最多 4 位旅客，團體端點另依 GROUP 規則。 | G0需求／G1–B3一般訂票 | Booking Domain/Application／人數、座位保留與初始狀態；逐項依本列規則斷言。 |
| `BOOKING-003` | 旅客數不得超過班次剩餘座位數。 | G0需求／G1–B3 | Booking Domain/Application／人數、座位保留與初始狀態；逐項依本列規則斷言。 |
| `BOOKING-004` | 成功建立訂票後立即保留對應座位數。 | G0需求／G1–B3 | Booking Domain/Application／人數、座位保留與初始狀態；逐項依本列規則斷言。 |
| `BOOKING-005` | 建立後狀態為 `PENDING_PAYMENT`。 | G0需求／G1–B3 | Booking Domain/Application／人數、座位保留與初始狀態；逐項依本列規則斷言。 |
| `FARE-001` | 成人票為 Base Fare 的 100%。 | G0需求／G1–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-002` | 學生票為 Base Fare 的 75%。 | G0需求／G1–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-003` | 每位旅客個別計價後加總為 Booking Total Fare。 | G0需求／G1–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-004` | 所有金額以整數表示，不處理小數與幣別換算。 | G0需求／G1–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `PAYMENT-001` | 只有 `PENDING_PAYMENT` Booking 可以付款。 | G0需求／G1–B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `PAYMENT-002` | 付款成功後 Booking 狀態改為 `PAID`。 | G0需求／G1–B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `PAYMENT-003` | 同一 Booking 不得重複付款。 | G0需求／G1–B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `ORDER-001` | 付款成功後建立唯一 Order。 | G0需求／G1–B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `ORDER-002` | Order Amount 必須等於 Booking Total Fare。 | G0需求／G1–B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `MEMBER-001` | Booking 可以不綁定 Member。 | B0–B3 | Member Repository/Application／選填與會員識別有效性；逐項依本列規則斷言。 |
| `MEMBER-002` | 有效 Member ID 可被附加至 Booking。 | B0–B3 | Member Repository/Application／選填與會員識別有效性；逐項依本列規則斷言。 |
| `MEMBER-003` | Corporate Member 的企業優惠率為 95%。 | B0–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-005` | 購票日至出發日相差至少 14 天時，具備 85% 提前購票優惠資格。 | B0–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-006` | 未滿 14 天不得取得提前購票優惠。 | B0–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `CHANGE-001` | 只有已付款 Booking 可改票。 | B0–B3 | Change Booking／狀態、目標容量及原新座位一致性；逐項依本列規則斷言。 |
| `CHANGE-002` | 新 Trip 必須有足夠座位。 | B0–B3 | Change Booking／狀態、目標容量及原新座位一致性；逐項依本列規則斷言。 |
| `CHANGE-003` | 改票成功後釋放原 Trip 座位並保留新 Trip 座位。 | B0–B3 | Change Booking／狀態、目標容量及原新座位一致性；逐項依本列規則斷言。 |
| `CHANGE-004` | B0 只記錄 Fare Difference，不執行補價或退款。 | B0–B3 | Change Booking／狀態、目標容量及原新座位一致性；逐項依本列規則斷言。 |
| `REFUND-001` | 只有已付款 Booking 可退票。 | B0–B3 | Refund Application／狀態、釋放座位及唯一紀錄；逐項依本列規則斷言。 |
| `REFUND-002` | 退票後 Booking 狀態為 `REFUNDED`。 | B0–B3 | Refund Application／狀態、釋放座位及唯一紀錄；逐項依本列規則斷言。 |
| `REFUND-003` | 退票成功後釋放座位。 | B0–B3 | Refund Application／狀態、釋放座位及唯一紀錄；逐項依本列規則斷言。 |
| `REFUND-004` | 退票建立唯一 Refund Record。 | B0–B3 | Refund Application／狀態、釋放座位及唯一紀錄；逐項依本列規則斷言。 |
| `NOTIFY-001` | 付款成功建立通知紀錄。 | B0–B3 | Notification／對應事件的本機紀錄；逐項依本列規則斷言。 |
| `NOTIFY-002` | 改票成功建立通知紀錄。 | B0–B3 | Notification／對應事件的本機紀錄；逐項依本列規則斷言。 |
| `NOTIFY-003` | 退票成功建立通知紀錄。 | B0–B3 | Notification／對應事件的本機紀錄；逐項依本列規則斷言。 |
| `SEAT-001` | 同一 Trip 內 Seat ID 不可重複配置。 | B0–B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `SEAT-002` | 一般 Booking 不保證相鄰座位。 | B0–B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `AUDIT-001` | Booking Created 必須留存 Audit Entry。 | B0–B3 | Audit／必要事件紀錄及結果；逐項依本列規則斷言。 |
| `AUDIT-002` | Payment、Change、Refund 成功後必須留存 Audit Entry。 | B0–B3 | Audit／必要事件紀錄及結果；逐項依本列規則斷言。 |
| `FARE-007` | 多項優惠不可疊加。 | B2–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-008` | 同時符合多項優惠時，採數值最低、對旅客最有利的單一折扣率。 | B2–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-009` | 每位 Passenger 獨立決定適用優惠。 | B2–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `FARE-010` | Fare Result 必須記錄實際採用的 Discount Type 及 Rate。 | B2–B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `GROUP-001` | 團體訂票旅客數最少 5 人。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-002` | 團體訂票旅客數最多 20 人。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-003` | 所有 Passenger 必須搭乘同一 Trip。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-004` | 必須配置同一車廂內連續座位。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-005` | 無法完整配置時不得建立 Booking。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-006` | 建立成功後一次保留全部座位。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-007` | 團體建立失敗時不得保留任何座位。 | B3 | Seat/Group Booking／容量、連續區段及失敗無殘留；逐項依本列規則斷言。 |
| `GROUP-PAY-001` | 團體付款成功後整筆 Booking 轉為 `PAID`。 | B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `GROUP-PAY-002` | 團體付款失敗後 Booking 轉為 `CANCELLED`。 | B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `GROUP-PAY-003` | 付款失敗後釋放全部團體座位。 | B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `GROUP-PAY-004` | 付款失敗不得建立 Order。 | B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `GROUP-PAY-005` | 團體付款成功只建立一筆 Order。 | B3 | Payment/Order Application／狀態、唯一性及失敗不建立訂單；逐項依本列規則斷言。 |
| `GROUP-FARE-001` | 每位 Passenger 依 B2 政策個別計價。 | B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `GROUP-FARE-002` | 團體 Total Fare 為個別 Fare 加總。 | B3 | Fare/Discount Policy／資格、折扣結果及逐位加總；逐項依本列規則斷言。 |
| `GROUP-AUDIT-001` | 團體建立、付款成功或付款失敗均留下 Audit Entry。 | B3 | Audit／必要事件紀錄及結果；逐項依本列規則斷言。 |
| `GROUP-NOTIFY-001` | 團體付款成功建立通知紀錄。 | B3 | Notification／對應事件的本機紀錄；逐項依本列規則斷言。 |
| `GROUP-NOTIFY-002` | 團體付款失敗建立取消通知紀錄。 | B3 | Notification／對應事件的本機紀錄；逐項依本列規則斷言。 |

## 4. 版本差異與尚未解除的事項

`FARE-001` 的成人 100% 是 Base Fare，B2／B3 仍須評估該旅客的提前購票與企業會員資格；不是成人永遠不享優惠。`MEMBER-003` 與 `FARE-005` 在 B2 表達優惠資格，再由 `FARE-007` 至 `FARE-010` 決定實際結果。`CHANGE-004` 的不補價／不退款及記錄 Fare Difference 是 B0 的簡化改票要求；後續版本不得無依據擴大真實金流範圍。

[待協調紀錄](../../docs/planning/decisions-and-open-issues.md) 的 O-04 至 O-07 依核准及實際證據追蹤，不因建立此表推定通過：

- O-04：2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)，規格衝突解除，B0已按方案A實測驗收。僅一個 `BUG-B0-001`；全部 28 項 G1 正確斷言保留，失敗 node ID 集合與已核實 Intentional Failure Manifest 完全一致、零非預期，其餘全通過，無 Skip／XFail／未知 Warning。Manifest 逐項追溯 Rule／AC、Diff／呼叫路徑與修復驗證；B1 全部 G1 及 B0 新增測試恢復通過。不刪測試、不弱化斷言、不繞過 Bug。
- O-05：G1 案例歷史／Tag 與 Bundle 已建立；B0 仍須延續來源、獨立快照與交付包隔離證據。
- O-06：B0 clean-copy已實際建立，52檔清單／內容／SHA256一致，乾淨副本仍保留受控 Bug。
- O-07：G1 已 PASS，B0 前置滿足；含已記錄限制的通過不等同 PASS 的一般門檻保留，B0已驗收，後續B1仍待產製。

本次僅對齊規則識別與預期追溯；未核准折扣、訂票、付款語意或測試門檻變更，亦未開始程式、學員任務卡及打包工具。後續階段進入條件依 [Acceptance Gates](acceptance-gates.md) 與 [版本驗證要求](version-validation-requirements.md)。

## 完成條件

- G0／G1、B0、B2、B3 的每個來源 Rule ID 均在 Registry；B1 明確是學生票修復版本。
- 一般與團體訂票人數適用範圍分明，舊 BOOKING-002 座位語意有映射紀錄。
- Code Area 及驗證意圖清楚標為預期，不宣稱已有程式或測試成果。
- 商業語意、來源連結及版本差異可追溯，O-04 規格核准與 O-05／O-07 現有證據明確，B0實測与O-06已依各自Gate驗收，後續版本仍須獨立證據。

2026-10-05 P5實測紀錄：B0為38實質Python／測試檔、44項測試；正式5failed／39passed符合完整manifest且零非預期，隔離一行學生率修復44passed。52檔clean-copy雜湊一致、B0 Tag392d920與Bundle續G1，已知相容Warning保留。詳見[B0 Validation Report](../03-brownfield/evaluation/01-b0-validation-report.md)。B1正式版本、真實學員與90分鐘演練仍未完成。
