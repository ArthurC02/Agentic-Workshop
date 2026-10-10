---
id: glossary
title: 詞彙表
minute: 00-90
group: open
section: 參考
---

# 詞彙表

只在卡住時查。每個詞第一次用到時，頁面上都有說明。

## 階段與角色

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Tool → Teammate → Digital Worker | Agent 從工具、隊友到在核准範圍內自己做事的數位員工；三者差在人介入的方式：逐步下指令、核准計畫、只在 Gate 做決定。 | 本課程〈歡迎與使用方式〉；Anthropic Engineering〈Building effective agents〉 |
| Greenfield／Brownfield | Greenfield 是從頭開始的新專案；Brownfield 是已有程式碼與文件的既有專案，要先讀懂再修改。 | 本課程〈Greenfield 任務：核心訂票 MVP〉；Michael Feathers《Working Effectively with Legacy Code》 |
| G0／G1／B0／B1／B2／B3 | G0 是 Greenfield 的起始程式包；G1 是完整的 Greenfield 版本（任務卡的「原 G1 Regression」指當時留下、現在仍要通過的測試）；B0 是假設已上線 12 個月的既有程式；B1–B3 是接著的三段任務。 | 本課程〈歡迎與使用方式〉 |
| MVP（最小可行產品） | 用最少的功能做出能實際使用的版本。今天指查班次、訂票、模擬付款與查訂單。 | Eric Ries《The Lean Startup》；本課程〈Greenfield 任務：核心訂票 MVP〉 |
| 主要 Agent | 小組選定、代表全組執行工作的那一個 Agent。 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |
| Shared Context（共同脈絡） | 小組整理出的共同事實、分歧與待決事項，由 Agent 寫成 `notes/shared-context.md`。 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |

## 證據

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Rule ID（規則編號） | 商業規則的編號，例如 `FARE-002`：學生為基礎票價的 75%。 | 本課程〈Greenfield Business Requirements〉 |
| AC（驗收條件） | Acceptance Criteria，功能必須符合的要求，例如 `AC-B1-001`。 | ISTQB〈Glossary〉；本課程〈Greenfield Acceptance Criteria〉 |
| 驗收對照表 | Agent 回報測試結果的表：每條驗收條件一列，寫編號、白話內容、通過／失敗／未驗證、依據的測試名稱；最後一行是通過、失敗、跳過各幾個。 | 本課程〈Greenfield Acceptance Criteria〉 |
| 變更審查 | 你不讀程式的修改內容（Diff），改請 Agent 對固定問題回答「是／否／不確定」；全部「是」才放行。 | Google Engineering Practices〈Google's Code Review Guidelines〉；本課程〈Coding Agent Usage Guide〉 |
| Skip／XFail | Skip 是略過測試；XFail 是把測試標成預期會失敗。兩者都不代表功能完成，不得用來隱藏失敗。 | pytest 官方文件〈How to use skip and xfail to deal with tests that cannot succeed〉 |
| Regression（回歸問題） | 修改後，原本正常的功能被改壞。既有測試要保留並通過；因規則改變而過時的期待值，要附規則編號並經人核准才更新。 | ISTQB〈Glossary〉 |
| PASS／FAIL／NOT VERIFIED | 通過／失敗／未驗證。沒有實際執行就只能寫未驗證。 | 本課程〈Digital Worker Delivery Summary〉 |
| /docs | 伺服器啟動後在瀏覽器開的 API 測試頁：點開 API →「Try it out」→ 貼範例 →「Execute」→ 看狀態碼。201 成功、404 找不到、409 不符商業規則或和目前狀態衝突、422 輸入資料格式錯誤。 | FastAPI 官方文件〈First Steps〉；IETF〈RFC 9110 HTTP Semantics〉 |
| notes 資料夾 | Agent 把分析、計畫、核准決策與驗收紀錄寫成檔案的地方；你只做決定與核對。 | 本課程〈歡迎與使用方式〉 |
| SHA256 雜湊 | 檔案的指紋：只要改一個位元組，值就不同；用來確認下載的復原包是原版。 | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |
| 復原包（Recovery） | 進度落後時改用的接續版本，已完成前一段；使用它不算小組自行完成前段。 | 本課程〈B1 Recovery：第 52 分鐘，必要時才切換〉 |

## Agent 技巧

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Agent 工作規則 | Agent 在整段對話都要遵守的約定：誰負責什麼、什麼時候停下、怎麼回報。 | Claude Code 官方文件〈Best practices for Claude Code〉 |
| Prompt 結構 | 好的提示詞有五個部分：目標、背景／要讀的檔、限制、輸出格式、停止條件。 | Anthropic〈Prompting best practices〉；OpenAI〈Prompt engineering〉 |
| Structured Output（結構化輸出） | 要求 Agent 用固定格式回報（固定欄位的表格或固定標題），人看得快、能比對。 | Anthropic〈Structured outputs〉；OpenAI〈Structured model outputs〉 |
| Skill | 把反覆要用的做法寫成 Markdown 檔放在 `skills/`，之後只說「請先讀 skills/… 並照做」。 | Anthropic〈Agent Skills〉 |
| Token 與節費 | Token 是 Agent 讀寫文字的計費與記憶單位。節費：一個任務一個新對話、只讀指定的檔、要摘要不要整段輸出、把共識寫成檔案。 | Anthropic〈Context windows〉；Anthropic〈Token counting〉 |
| 模型選擇 | 機械性的工作用快速、便宜的模型；分析陌生程式、比較取捨、自主執行用較強的模型。 | Anthropic〈Choosing the right model〉 |
| 推論強度（Reasoning Effort） | 同一個模型「想多深」：分析、比較方案調高，小步修改調低。工具沒有這個設定時，提示詞寫「先仔細想過再回答」。 | Anthropic〈Effort〉；OpenAI〈Reasoning models〉 |

## B3 用語

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Gate（核准關卡） | Agent 交出資料後停下、由人做決定的檢查點；核准是決策，不等於通過驗收。 | 本課程〈B3 人員核准 Gate〉；Anthropic Engineering〈Building effective agents〉 |
| APPROVE／APPROVE WITH CONDITIONS／REJECT | 核准／附條件核准（條件解除後才可續行）／拒絕；REJECT AND REVISE 是退回修正。 | 本課程〈B3 人員核准 Gate〉 |
| Work Order（工作單） | 交給 Agent 的整件任務說明：範圍、禁止事項、停止條件與回報格式；B3 存成 `skills/b3-work-order.md`。 | 本課程〈Digital Worker Work Order〉 |
| Escalation（升級處理） | Agent 遇到停止條件時停下，附證據與選項，交給人決定。 | 本課程〈Digital Worker Work Order〉 |
| Atomicity／Compensation | Atomicity：一組動作要嘛全部完成、要嘛全部不做。Compensation：失敗時把已做的部分還原，例如團體付款失敗就釋放全部座位。 | 本課程〈B3 任務卡 TASK-B3-001〉 |
| Level（完成等級） | Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付；依證據擇一，不自動選 Level 3。 | 本課程〈B3 任務卡 TASK-B3-001〉 |
