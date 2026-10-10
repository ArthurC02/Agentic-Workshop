# 共同詞彙與 Domain 定義

> 目標讀者：主持人、評估者、維護者與素材產製 Agent。
> 使用時機：撰寫需求、資料模型、測試、教材與交接紀錄時。
> 前置條件：閱讀[Manifest](workshop-manifest.md)及適用版本的正式規格。
> 版本：P1 治理基線，2026-10-05；尚無程式驗證結果。
> 可見性：Facilitator／Evaluation／Agent Production；含後續版本資訊，不整份發給學員。

## 1. Domain 詞彙

| 英文 | 中文／定義 | 邊界與適用版本 |
|---|---|---|
| Trip | 班次：可供查詢與預訂的特定行程，包含起訖點、出發／抵達時間、基礎票價與可售座位 | G0／G1 起；不是 Booking 或真實營運車次 |
| Passenger | 搭乘者：訂票中的個別旅客，具有 ID、名稱與 Passenger Type | G1 起逐位計價，不等同購票會員 |
| Passenger Type | 旅客類型：`ADULT`／`STUDENT` | 學生資格與會員、提前購票資格分開評估 |
| Booking | 訂票交易：指定 Trip、旅客、Total Fare 與交易狀態 | 建立後 `PENDING_PAYMENT` 並保留座位；不等同付款後的 Order |
| Booking Status | 訂票狀態：`PENDING_PAYMENT`、`PAID`、`CANCELLED`，B0 增加 `REFUNDED` | 精確轉換依各版規則；不能將 G1 一般付款失敗與 B3 團體取消視為同一規則 |
| Order | 訂單：付款成功後建立、關聯 Booking 的付款交易資訊，含 Amount 與 Payment Status | G1 起付款成功唯一建立；付款失敗不得建立成功 Order |
| Payment／Mock Payment Gateway | 模擬付款流程與可控制結果的本機付款介面 | 不連線真實金流；成功／失敗可由測試注入，不隨機 |
| Payment Status | Order 的付款狀態 | 不等同 Booking Status；具體值按正式 Schema 與版本規格，本文不新增狀態 |
| Base Fare | 班次的成人基礎票價 | 固定 Seed 金額；不包含幣別換算 |
| Fare／Fare Result | 個別旅客的計價結果 | 金額為整數；B2 記錄選用 Discount Type、Rate 與 Amount |
| Total Fare | Booking 內所有 Passenger Fare 的合計 | 每位旅客先獨立評估再加總，不對整團只套一個共同優惠 |
| Member／Member Type | 可選擇附加於 Booking 的會員；`STANDARD`／`CORPORATE` | B0 起；非會員仍可訂票，不要求登入或會員申請 |
| Discount | 符合條件的票價優惠 | 學生、提前購票與企業會員資格；B0／B1 的既有順序與 B2 最有利政策不同 |
| Discount Type／Rate | 優惠種類及折扣率 | 75% 是支付基礎票價的 75%，不是減免 75%；B2 取最低符合資格的單一率，不疊乘 |
| Applied Discount | 實際選用的優惠 | B2 起與 Fare Result 留存，便於證明旅客計價政策 |
| Advance Purchase | 提前購票資格：購票日至出發日相差至少 14 天 | 依固定／可注入 Clock 計算；未滿 14 天不適用，85% 資格依原規格 |
| Available Seats | 班次當時仍可售的座位數 | 成功保留後減少，正確釋放後恢復；須與座位分配一致 |
| Seat／Seat Assignment | 座位及旅客獲分配的唯一 Seat ID | B0 起同 Trip 不重複；一般訂票不保證相鄰 |
| Carriage／Consecutive Seats | 車廂及同車廂排序後連續的 Seat Position 區段 | B3 必須找到足以容納整團的完整空位區段；不跨車廂、不處理走道或真實布局 |
| Group Booking | 團體訂票：5–20 人、同 Trip、同車廂連續座位的單筆 Booking | B3 才新增；不拆筆、不部分成功、不候補 |
| Atomicity／Compensation | 整筆成立或整筆失敗的意圖，以及失敗時修復已保留狀態的補償流程 | B3 建立失敗不保留座位；付款失敗轉 `CANCELLED`、釋放全座位且不建 Order；In-Memory 模擬，不要求交易框架 |
| Booking Change／Fare Difference | 簡化改票與新舊計價差額的紀錄 | B0 起已付款才可改票，調整座位；只記錄差額，不執行真實補價或退款 |
| Refund／Refund Record | 簡化退票與唯一退票紀錄 | B0 起已付款才可退票，轉 `REFUNDED` 並釋放座位；不連金流 |
| Notification Record | 本機通知紀錄 | 不寄 Email／簡訊；付款、改票、退票與團體付款結果依版本規則建立 |
| Audit Entry | 案例系統對業務事件留下的本機紀錄 | 不等同 Agent 操作稽核；事件涵蓋 Booking／Payment／Change／Refund，B3 加團體結果 |
| Agent Audit Record | Agent Session、核准、命令、檔案、測試與交付的操作證據 | 治理層紀錄；與案例 Audit Entry 分開 |

Domain 來源：[技術標準](../../docs/instructions/01_技術棧與Repository標準指令書.md)、[G0](../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)、[G1](../../docs/instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)、[B0](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[B1–B3](../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。

## 2. 協作與交付詞彙

| 詞彙 | 定義與用途 |
|---|---|
| Goal | 本次任務要達成的最終成果 |
| Story | 從業務／使用者角度描述需求與價值 |
| Task／Task Breakdown | 可執行工作項目及其依賴、輸入、輸出與完成條件 |
| Prompt | 單次要求 Agent 工作的指令，不是永久規格來源 |
| Context | 完成目前任務所需的最小充分背景；結論需交叉驗證 |
| Shared Context | 小組比較獨立分析後整理的共同事實、證據、分歧、範圍與測試；任務揭露後才核准修改計畫 |
| Session | 特定工作期間的互動脈絡；結束前轉成可交接摘要 |
| Memory | 經確認且跨 Session 有價值的知識；不存未驗證推論或敏感資訊 |
| Rule／Rule ID | 持續遵守的限制與標準及其固定識別碼；不是實作建議 |
| Skill | 可重複完成某類工作的能力／方法；執行仍受 Rule 約束 |
| Artifact | 可審查、交接與追溯的成果，例如分析、程式、測試、文件與決策紀錄 |
| Repository Understanding | 對實際 Repository 結構、模組責任、資料流與依賴的理解 |
| Impact Analysis | 任務對規則、模組、API、測試與文件的影響與風險分析 |
| Handover Package | 目標、完成內容、決策、測試、問題、未完成與下一步的交接資訊 |
| Acceptance Criteria／AC ID | 可判定的驗收條件與其固定識別碼，不是 Demo 外觀印象 |
| Checkpoint／Human Approval Gate | 人員審查與決策節點；B3 分需求、設計、交付三關 |
| Production Acceptance Gate | 產製者對文件／版本／包的驗收，包含實際證據；與活動 Human Gate 分開 |
| Work Order | 將 Mission、Rules、核准 Context、邊界、交付物、測試、Gate 與升級條件交給主要 Agent 的命令 |
| Review／Challenge | 審查證據與變更／挑戰假設和方案；不能只接受 Agent 自信摘要 |
| Approve／Reject／Escalation | 依證據核准／要求修正或拒絕／遇到缺口、衝突、越界時提交待決策問題 |
| Reference Solution | 完整且驗證過的標準實作；學員可有合理變體，不等於只能照抄 |
| Baseline／Recovery Baseline | 任務開始的固定版本／主持人視需要提供的續接版本；Recovery 不計為學員自行完成 |
| Validation Report | 實際執行環境、命令、結果與限制的證據；預期值不等於已驗證 |
| Participant／Facilitator／Evaluation／Agent Production | 學員／主持／評估／素材產製的不同受眾與可見性，依 Manifest 分包 |

協作來源：[核心概念](../../docs/contents/02_核心概念與共同語言.md)、[B0 Shared Context](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[Digital Worker 治理](../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)。

## 3. 成熟度、版本與完成度

Tool 由人主導理解與拆解，Agent 協助執行；Teammate 由人與 Agent 共同分析、比較與決策；Digital Worker 由 Agent 在核准範圍主導交付，人員負責邊界、Review、核准與最終責任。

G0 為 Starter、G1 為完整 MVP、B0 為 12 個月成長基線、B1 為學生票修復、B2 為最有利單一優惠、B3 為團體訂票。學員 B3 Level 1（分析）、Level 2（核心流程）、Level 3（完整交付）與 Reference 的完整驗收是不同對象；不能把分析完成寫成程式驗收通過。

## 4. 用詞與規格差異

新增詞彙同步本表及來源與適用版本。O-03 已於 P2 完成編號對齊，`BOOKING-002` 專指一般最多 4 人、`BOOKING-003` 專指座位容量，見[Rule Registry](rule-traceability-baseline.md)。其他差異狀態見[決策清單](../../docs/planning/decisions-and-open-issues.md)，不由本詞彙表新增狀態或改變政策。

## 完成條件

Domain 與協作詞彙具一致定義、版本範圍與來源。實際需求、程式、測試與文件須依[一致性規則](consistency-rules.md)追溯，並由[Acceptance Gates](acceptance-gates.md)判定；目前只完成文件基線，沒有程式執行證據。
