# Agentic Software Development Evolution Workshop
# 素材產製總控指令書

> 本文件的目標讀者是 Coding Agent，不是工作坊參與者。
>
> 你的任務是依照本指令書，逐步產製一套可在 90 分鐘內執行的 Agentic Software Development Evolution Workshop 素材。除非後續指令書明確要求，請勿自行擴大範圍、改變故事線或替換核心案例。

---

## 1. 專案目標

建立一套以 **Smart Ticket Platform** 為案例的工作坊素材，使參與者能在 90 分鐘內親身經歷 Agent 在軟體開發中的角色演化：

```text
Tool
  ↓
Teammate
  ↓
Digital Worker
```

本工作坊的主要目標依優先順序為（2026-10-09 已核准變更，原順序為 SDLC 體驗 → 組織導入 → Agent 操作）：

1. 練習通用的 Agentic Coding 技巧：每段明確標示一個技巧，學員實際用上並看到效果。
2. 體驗 Agentic Software Development Lifecycle（Tool → Teammate → Digital Worker）。
3. 萃取組織導入 Agentic Development 的方法、控制點與平台需求；證據由 Agent 寫進學員 Repo 的 `notes/` 檔，不靠學員填表。

設計規則：每段頁首有「現在在做什麼」卡（情境、目標、技巧、完成的樣子）；檢查點每段最多 3 個（Greenfield、B3 最多 4 個）；表單每段最多一張、最多 4 欄，只記錄人的決定。全程人不寫、不讀程式，以行為與證據驗收。2026-10-09 追加（主課與 DLC 都適用）：每個檢查點讓學員複製一段提示詞即可完成，指令由 Agent 執行；學員只用短回覆做決定，表單以下拉／勾選為主；討論用口頭提示，不用表格；修改時刪除不再需要或矛盾的內容。教學順序（主課與 DLC 都適用）：由淺入深；每個知識點在學員第一次需要時才介紹（開場只給路線圖），不得要求學員使用尚未介紹的知識點；技巧類知識點附「延伸閱讀」官方出處名稱（學員頁不放外部網址）。

本工作坊不是：

- 特定 Coding Agent 產品教學。
- 角色扮演型團隊活動。
- Coding 速度競賽。
- 完整產品開發專案。
- 對真實鐵路、高鐵或客運業務規則的模擬。

---

## 2. 固定條件

以下條件已確定，不得任意修改。

### 2.1 時間與參與者

- 工作坊總長度：90 分鐘。
- 參與者：主要為工程師。
- 參與者開發能力：普通，不應假設具備高階架構或演算法能力。
- Greenfield 階段：一人一組。
- Brownfield 階段：多人一組。
- Brownfield 採混合模式：個人先使用自己的 Agent 分析，再由小組整合結果，最後由主要 Agent 執行。

### 2.2 工具中立

全部素材必須保持工具中立，不可綁定特定產品。

不得要求只適用於以下任一產品的專屬功能：

- Claude Code
- GitHub Copilot
- Cursor
- Gemini CLI
- OpenAI Codex
- 其他特定 Coding Agent

若需要描述操作，請使用通用語言，例如：

- 將需求與 Context 提供給 Coding Agent。
- 要求 Agent 先提出計畫。
- 要求 Agent 分析 Repository。
- 審查 Agent 產生的 Diff。
- 要求 Agent 執行測試並說明結果。

2026-10-09 已核准變更：主課須帶到六項通用 Agentic Coding 技巧──Prompt 結構、Structured Output（結構化輸出）、Skill（寫成 Markdown 檔、以「請先讀 skills/…」使用的可重複工作說明）、Token 節費、模型選擇、推論強度，並對應 Tool → Teammate → Digital Worker 三階段埋入既有步驟。以通用概念描述；工具若有對應功能（Skill、模型選單、推論強度設定）可順帶使用，但不得成為完成任務的前提，也不寫特定產品名稱或設定路徑。

### 2.3 核心案例

案例名稱：**Smart Ticket Platform**

概念範圍：

- 車票查詢。
- 訂票。
- 付款。
- 訂單查詢。
- 系統成長後可加入會員、優惠、改票、退票、通知等能力。

本案例以一般生活中的車票訂購經驗為基礎，但不得複製任何真實運輸業者的完整規則、品牌、API 或介面。

---

## 3. 工作坊故事線

### Act 1：Greenfield / Tool

參與者個別取得同一份 Greenfield Starter Kit，從 Starter Repository 建立完整 MVP。

MVP 至少包含：

- 查詢班次。
- 建立訂票。
- 模擬付款。
- 查詢訂單。
- 基本測試。
- 基本文件。

此階段由人主導：

- 人理解需求。
- 人決定設計方向。
- 人拆解工作。
- Agent 協助產生程式、測試與文件。

Agent 的定位是 **Tool**。

### Act 2：Time Skip

主持人宣布時間快轉。Smart Ticket Platform 已執行一段時間，功能及程式規模均已成長。

參與者停止使用自己的 Greenfield Repository，改為接手主持人統一提供的 Brownfield Repository。

Brownfield Repository 必須在概念與設計上明顯延續 Greenfield MVP，但已加入：

- 更多功能及模組。
- 30 至 50 個具實質內容的原始碼與測試檔案。
- 歷史設計決策。
- 部分技術債。
- 部分文件落差。
- 足以支援影響分析的測試與依賴關係。

### Act 3：Brownfield / Teammate

多人組成小組，每位成員先使用自己的 Agent 獨立分析同一份 Brownfield Repository。

每位成員至少分析：

- 系統結構。
- 新任務涉及的模組。
- 可能的影響範圍。
- 風險與資訊缺口。
- 建議處理順序。

小組比較不同 Agent 的結果，形成 Shared Context、共同方案及核准後的執行計畫。

Agent 的定位是 **Teammate**。

### Act 4：Brownfield / Digital Worker

由小組選定一個主要 Agent，依照核准後的 Shared Context、Rule 與工作計畫主導執行。

Agent 應完成：

- 需求分析。
- Repository 理解。
- Impact Analysis。
- Task Breakdown。
- 程式修改。
- 測試建立與執行。
- 文件更新。
- 交付摘要。

人員不得直接修改程式碼，只能：

- Challenge。
- Review。
- Approve 或 Reject。
- 要求補充證據。
- 要求 Agent 修正。

Agent 的定位是 **Digital Worker**。

---

## 4. Brownfield 任務難度

Brownfield 採混合型任務，但不可一次施加過多壓力。

任務應符合以下學習曲線：

```text
Greenfield 經驗可支援大部分理解
        +
少量新的系統複雜度
        +
明確但不直接給答案的提示
        =
參與者需要思考，但可在時間內達成
```

建議的三層任務如下。

### 4.1 暖身：Bug Fix

範例：學生票折扣計算錯誤。

- 正確規則：學生票 75 折。
- 現有錯誤：系統計算為 85 折。
- 目的：讓參與者熟悉 Repository、測試與 Agent 分析方式。

### 4.2 主任務：Business Rule Change

規則範例：

- 提前 14 天購票：85 折。
- 企業會員：95 折。
- 學生票：75 折。
- 多個優惠不可疊加，只採對旅客最有利的單一優惠。

目的：要求 Agent 找出 Pricing、Booking、Member、Test 及 Documentation 等影響範圍。

### 4.3 進階：New Feature

功能範例：團體訂票。

- 一次預訂 5 至 20 張票。
- 座位應盡量相鄰。
- 付款失敗時整筆取消，不得部分成立。

目的：要求 Agent 進行需求澄清、方案設計、Task Breakdown、實作、測試及文件同步。

上述內容是基準方向。後續任務指令書可以進一步調整細節，但不得失去「Bug + 規則變更 + 新功能」的混合結構。

---

## 5. 產製原則

### 5.1 可執行優先

所有 Repository 必須：

- 可在乾淨環境完成安裝。
- 可啟動。
- 可執行測試。
- 不依賴付費服務。
- 不依賴外部 API 才能完成核心流程。
- 不需真實付款、身分驗證或交通資料。

必要資料應使用本機 Fixture、Seed Data、Mock 或 In-Memory 實作。

### 5.2 控制技術複雜度

- 不使用微服務。
- 不使用 Kubernetes。
- 不要求雲端帳號。
- 不加入與學習目標無關的基礎設施。
- 不以複雜 UI 作為工作坊重點。
- 不設計需要高階演算法才能完成的座位配置。

系統應足以呈現模組邊界、依賴、測試、文件與技術債，但必須讓普通工程師能在 Agent 協助下理解。

### 5.3 保持真實但可控

Brownfield 中的問題必須是刻意設計且可被發現的，不可依靠隨機失敗。

技術債與文件落差應：

- 有學習價值。
- 可透過 Repository、測試、Commit History 或提示找出。
- 不應造成環境無法啟動。
- 不應同時出現太多無關問題。
- 應有標準答案或可接受答案範圍。

### 5.4 不把答案直接寫進學員素材

素材分為不同可見性：

- Participant：參與者可直接取得。
- Facilitator：僅主持人可取得。
- Evaluation：標準答案、評分依據及驗證方式。
- Agent Production：供後續 Coding Agent 產製使用。

不得將 Facilitator 或 Evaluation 內容混入 Participant 素材。

---

## 6. 預定素材結構

後續 Coding Agent 應依各階段指令書，建立以下目錄結構。現階段只建立規劃，不要自行產製全部內容。

```text
agentic-workshop/
├── 00-governance/
│   ├── workshop-manifest.md
│   ├── glossary.md
│   ├── consistency-rules.md
│   └── acceptance-gates.md
├── 01-greenfield/
│   ├── participant/
│   │   ├── mission-brief.md
│   │   ├── business-requirements.md
│   │   ├── acceptance-criteria.md
│   │   ├── agent-usage-guide.md
│   │   └── starter-repository/
│   ├── facilitator/
│   │   ├── facilitation-guide.md
│   │   ├── timing-and-cues.md
│   │   └── expected-mvp.md
│   └── evaluation/
│       ├── mvp-checklist.md
│       └── reference-solution/
├── 02-time-skip/
│   ├── participant/
│   │   ├── time-skip-announcement.md
│   │   ├── company-growth-summary.md
│   │   └── brownfield-handover.md
│   └── facilitator/
│       ├── transition-script.md
│       └── repository-delta-explanation.md
├── 03-brownfield/
│   ├── participant/
│   │   ├── repository/
│   │   ├── system-context.md
│   │   ├── known-constraints.md
│   │   ├── individual-analysis-sheet.md
│   │   ├── shared-context-template.md
│   │   └── task-cards/
│   │       ├── 01-bug-fix.md
│   │       ├── 02-rule-change.md
│   │       └── 03-group-booking.md
│   ├── facilitator/
│   │   ├── facilitation-guide.md
│   │   ├── progressive-hints.md
│   │   ├── intervention-rules.md
│   │   └── reveal-sequence.md
│   └── evaluation/
│       ├── expected-impact-analysis.md
│       ├── expected-code-changes.md
│       ├── expected-tests.md
│       └── reference-solution/
├── 04-digital-worker/
│   ├── participant/
│   │   ├── operating-rules.md
│   │   ├── approval-gates.md
│   │   ├── review-checklist.md
│   │   └── delivery-template.md
│   ├── facilitator/
│   │   ├── governance-observation-guide.md
│   │   └── exception-injection.md
│   └── evaluation/
│       └── autonomy-and-governance-rubric.md
├── 05-retrospective/
│   ├── participant/
│   │   ├── reflection-sheet.md
│   │   └── maturity-comparison.md
│   └── facilitator/
│       ├── debrief-guide.md
│       └── organization-adoption-prompts.md
└── 06-runbook/
    ├── workshop-runbook.md
    ├── environment-setup.md
    ├── preflight-checklist.md
    └── recovery-plan.md
```

---

## 7. 全域一致性規則

所有後續產製內容必須通過以下一致性檢查。

### 7.1 Domain 一致性

同一名詞在所有素材中必須使用相同意義。例如：

- Trip：可供旅客查詢及預訂的班次。
- Booking：一次訂票交易。
- Passenger：搭乘者。
- Order：付款及交易狀態的聚合資訊。
- Fare：票價計算結果。

正式詞彙以後續 `glossary.md` 為準。若需要新增詞彙，必須同步更新 Glossary。

### 7.2 規則一致性

同一商業規則不可在 Requirement、Code、Test、Document 及 Evaluation 中出現不同版本。

每項規則應有唯一識別碼，例如：

```text
FARE-001
BOOKING-002
PAYMENT-003
```

需求、程式註解、測試名稱或評估表可引用規則識別碼，以利追溯。

### 7.3 版本一致性

至少定義以下版本：

- G0：Starter Repository。
- G1：Greenfield Reference MVP。
- B0：Brownfield 初始版本。
- B1：完成 Bug Fix。
- B2：完成 Business Rule Change。
- B3：完成 Group Booking。

每個版本必須能獨立 Build 與 Test。

### 7.4 難度一致性

- Greenfield 必須可由普通工程師在 Agent 協助下完成。
- Brownfield 必須需要 Repository Understanding 與 Impact Analysis，但不可依賴隱晦知識。
- 提示應漸進揭露，不應第一時間給出檔案位置或完整答案。
- 最終任務應具有挑戰，但不得要求參與者在 90 分鐘內完成不合理的大量程式碼。

### 7.5 評估一致性

每個任務都必須具備：

- 明確目的。
- Participant Input。
- Expected Artifact。
- Acceptance Criteria。
- Facilitator Hint。
- Reference Answer 或可接受答案範圍。
- 自動化或人工驗證方式。

---

## 8. 文件撰寫規則

- 預設使用繁體中文。
- 程式識別字、API、類別與技術名詞可使用英文。
- Participant 文件文字應簡潔、可操作，不揭露答案。
- Facilitator 文件必須包含時間點、觀察項目、提示條件及中止條件。
- Evaluation 文件必須明確列出判定標準，不可只寫主觀描述。
- 每份文件開頭說明目標讀者、使用時機及前置條件。
- 每份文件結尾列出產出物或完成條件。
- 不得用大量背景故事稀釋任務。

---

## 9. 程式碼品質規則

後續產製 Repository 時必須遵循：

- 採清楚、普通工程師容易理解的分層或模組化設計。
- 避免過度抽象及過度設計。
- 核心商業邏輯必須可被單元測試。
- API 或應用入口必須可被整合測試。
- 測試名稱應能表達商業規則。
- 不得把所有邏輯集中在單一檔案。
- 不得刻意製造難以閱讀的程式碼作為 Brownfield 難度來源。
- 技術債應是合理的歷史演變結果，不是低品質程式碼堆疊。
- 所有錯誤注入必須有對應的修復方式與驗證測試。

---

## 10. 安全與資料規則

- 不使用真實個人資料。
- 不使用真實信用卡資料。
- 不使用真實運輸業者的內部資料。
- 不包含任何帳密、Token、API Key 或私密憑證。
- 付款只能使用模擬狀態。
- Participant 不應需要連線至外部服務才能完成工作坊。

---

## 11. 後續產製順序

除非另有指令，後續應依以下順序產製，不可一次建立全部素材：

1. Workshop Manifest、Glossary、Consistency Rules。
2. 技術棧與 Repository 標準。
3. Greenfield Starter Kit 指令書。
4. Greenfield Reference MVP 指令書。
5. Brownfield Evolution 指令書。
6. Brownfield Task Cards 指令書。
7. Digital Worker Governance 素材指令書。
8. Facilitator Runbook 指令書。
9. Evaluation 與 Reference Solution 指令書。
10. 全域驗證、時間演練及打包指令書。

每個階段完成後，必須先執行一致性檢查，再進入下一階段。

---

## 12. 本指令書的完成條件

Coding Agent 閱讀本文件後，應能正確說明：

- 工作坊要呈現何種 Agent 成熟度演化。
- Greenfield 與 Brownfield 的關係。
- 為什麼 Greenfield 是個人活動、Brownfield 是混合式小組活動。
- 為什麼 Brownfield 任務採 Bug、規則變更及新功能的混合設計。
- 哪些內容屬於 Participant、Facilitator、Evaluation 與 Agent Production。
- 為什麼不可綁定特定 Coding Agent 產品。
- 為什麼素材必須在 90 分鐘工作坊限制下保持可執行、可理解及可驗證。

若後續局部指令與本文件衝突，除非局部指令明確標示為「已核准變更」，否則應以本文件為準並回報衝突。
