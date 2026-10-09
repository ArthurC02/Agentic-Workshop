---
id: glossary
title: 詞彙表
minute: 00-90
group: open
section: 參考
---

# 詞彙表

本表整理 Runbook 中常見詞彙在本工作坊的用法：先給中文名與白話解釋，再舉今天的例子。各段任務專用的名詞，請以該段解鎖後的任務文件為準。開發人員普遍熟悉的詞（API、JSON、HTTP、Git、commit、Repo、pytest）不另收錄。「首次出現」欄是 Runbook 第一次說明這個詞的地方；詞彙表只供查詢，不取代那一步的說明。

## 階段與角色

| 詞彙 | 中文與白話解釋 | 今天的例子 | 首次出現 | 出處 |
|---|---|---|---|---|
| Tool → Teammate → Digital Worker | Agent 從工具、隊友到能獨立執行任務的數位員工；是今天依序練習的三種協作角色。今天全程人都不寫程式，三者的差別在人介入的方式，人負的責任也跟著改變。 | Greenfield 用 Tool，Time Skip 到 B2 用 Teammate，B3 用 Digital Worker。 | 歡迎與使用方式 | 本課程〈Tool → Teammate → Digital Worker比較〉 |
| Tool（工具） | 由你理解需求、決定方向、逐步下指令並每步驗收；Agent 負責寫程式、測試與文件。 | 第 7–29 分鐘，你下指令，Agent 幫你寫訂票 API。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| Teammate（隊友） | Agent 和你一起分析，由人核准計畫：各自分析、比較判斷，再整合小組共同脈絡。 | 第 33–52 分鐘，各自請 Agent 分析 B0 失敗測試，再小組比較。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| Digital Worker（數位員工，DW） | Agent 在核准範圍內主導交付；人員負責設定邊界、檢視（Review）、核准與最終責任。DW 是它的縮寫。 | B3 由 Agent 自主分析、實作、測試、寫交付摘要；人只透過三道核准關卡管 Agent，看驗收對照表與變更審查答案做決定，不看程式。 | 歡迎與使用方式；B2 開始過渡 | 本課程〈Digital Worker 操作規則〉；Anthropic Engineering〈Building effective agents〉 |
| Greenfield（新專案） | 從頭開始的新專案，沒有歷史程式包袱。 | 今天第 7–29 分鐘的個人段落：從 G0 開始完成核心訂票 MVP。 | 歡迎與使用方式 | 本課程〈Greenfield 任務：核心訂票 MVP〉 |
| Brownfield（既有專案） | 已有程式碼、文件與歷史取捨的既有專案；要先讀懂再修改。 | 今天第 29 分鐘以後：接手 B0，先個人分析、再小組整合，接著做 B1–B3。 | 歡迎與使用方式 | Michael Feathers《Working Effectively with Legacy Code》；本課程〈Brownfield 接手說明〉 |
| G0／B0／B1／B2／B3 | 各段的起點或任務代號。G0 是 Greenfield 的起始程式包；B0 是 Brownfield 的起點，也就是假設系統已上線 12 個月的既有程式；B1、B2、B3 是接在後面的三段 Brownfield 任務。 | B1 修復學生票折扣異常、B2 導入不可疊加的最有利優惠政策、B3 團體訂票。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| G1 | 完整的 Greenfield MVP 版本，B0 由它演化而來；任務卡提到的「原 G1 Regression」是那時留下、現在必須繼續通過的既有測試。 | B1 的 AC 要求原 G1 的 28 項既有測試保留正確的期待值並通過。 | B1 任務卡 | 本課程〈共同詞彙與 Domain 定義〉 |
| MVP（Minimum Viable Product） | 最小可行產品：用最少的功能做出能實際使用的版本，盡快驗證需求是否成立。本工作坊指能跑通查詢、訂票、模擬付款與查詢訂單的核心流程。 | Greenfield 的目標就是完成這個 MVP。 | 歡迎與使用方式 | Eric Ries《The Lean Startup》；本課程〈Greenfield 任務：核心訂票 MVP〉 |
| Time Skip（時間快轉） | 專案假設已開發一段時間，大家停下自己的進度，改接手統一的版本。 | 第 29 分鐘：假設 Smart Ticket 已上線 12 個月，全場改接手同一份 B0。 | 歡迎與使用方式 | 本課程〈Time Skip：12 個月後〉 |
| Coding Agent | 能讀取本機資料夾、修改檔案並執行終端指令的 AI 開發助手。本 Runbook 不要求任何特定 Agent 產品的指令或功能。 | 你今天在自己電腦上使用的 Agent。 | 歡迎與使用方式 | Anthropic Engineering〈Building effective agents〉；本課程〈Coding Agent Usage Guide〉 |
| Session（對話工作階段） | 與 Agent 的一段對話；同一個 Session 會記得先前交代的內容。 | 換到 B0 時開新的 Session，不沿用 Greenfield 的 Session，避免混入舊脈絡。 | Time Skip 檢查點 2（開新對話） | Anthropic〈Context windows〉 |
| 主要 Agent | 小組選定、代表全組執行工作的那一個 Agent，接收小組的共同脈絡；不要把所有人的 Session 原封不動拼接。 | 第 39 分鐘起，小組指定在某位成員電腦上的 Agent 為主要 Agent。 | 共同脈絡 檢查點 1 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |
| Gherkin | 用 Given（前提）／When（動作）／Then（預期結果）寫測試情境的格式，讓需求與測試能對照。 | Given 一位學生旅客、When 訂 700 元的班次、Then 票價為 525。 | Greenfield 驗收條件 | Cucumber 官方文件〈Gherkin Reference〉 |

## Context 與證據

| 詞彙 | 中文與白話解釋 | 今天的例子 | 首次出現 | 出處 |
|---|---|---|---|---|
| Context（背景資料） | 交給 Agent 參考的資料，例如文件、規則與先前結論。文件可作 Context，但不保證全部敘述與程式完全同步；重要結論請 Agent 用程式、測試與公開規則交叉驗證。 | B0 的 README、架構文件與 ADR。 | Time Skip（公司與系統成長摘要） | Anthropic〈Context windows〉；Anthropic Engineering〈Effective context engineering for AI agents〉 |
| Shared Context（共同脈絡） | 小組整理出的共同事實：比較各自分析後，記錄共同事實、分歧與待決事項；任務揭露後仍須另外取得範圍與計畫的核准。 | 第 39–44 分鐘由 Agent 寫成的 `notes/shared-context.md`。 | 共同脈絡 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |
| Approved Context（已核准的背景資料） | 經人確認、可以交給 Agent 當依據的背景資料。 | B3 開始時 Agent 寫進 `notes/b3.md` 的版本與已確認假設。 | B3 工作單 | 本課程〈Digital Worker Work Order〉 |
| Seed Data（預設測試資料） | 系統啟動時就放好的固定資料，用來開發與測試。 | Greenfield 需求文件中的固定班次與站名。 | 環境準備 | 本課程〈Greenfield Business Requirements〉 |
| Rule ID（規則編號） | 商業規則的編號。交付時列出商業規則與驗收條件的對應，逐項核對。 | `FARE-002`：學生為基礎票價的 75%。 | Greenfield 檢查點 2（一句帶過，給 Agent 對照用） | 本課程〈Rule Traceability Baseline〉 |
| AC（Acceptance Criteria，驗收條件） | 說明功能必須符合什麼要求；AC ID 是其編號。每項以 API 或核心邏輯測試提供證據。 | `AC-B1-001`：單一學生旅客票價為基礎票價 75%。 | Greenfield 檢查點 2（一句帶過，給 Agent 對照用） | ISTQB〈Glossary〉；本課程〈Greenfield Acceptance Criteria〉 |
| Rule Traceability（規則追溯） | 每條規則都能對到哪段程式、哪個測試與哪份文件。 | B3 的 Gate 3 Input 要列出規則對照。 | B3 檢查點 4 | ISTQB〈Glossary〉；本課程〈Rule Traceability Baseline〉 |
| ADR（Architecture Decision Record，架構決策紀錄） | 說明採用某項設計的原因與取捨。 | B0 的 `docs/adr/001-use-in-memory-repositories.md`。 | B0 系統 Context | Michael Nygard〈Documenting Architecture Decisions〉 |
| Diff（變更內容） | 修改前後的差異。你不用自己讀；改請 Agent 回答變更審查問題，用白話說明改了什麼。 | Agent 用 `git diff` 檢查後，告訴你改了哪些檔案。 | Greenfield 檢查點 3（結構化輸出小卡） | Git 官方文件〈git-diff〉；Google Engineering Practices〈Google's Code Review Guidelines〉 |
| Git 基準 | 修改前先請 Agent Commit 一次，之後 Agent 才說得出這次改了什麼。 | 請 Agent 把目前所有檔案 Commit 成「B0 baseline」。 | Greenfield 檢查點 1（由 Agent 代做） | Pro Git〈About Version Control〉；Git 官方文件〈git-commit〉 |
| Skip／XFail | Agent 回報中可能出現的詞：Skip 是略過測試；XFail 是把測試標成預期會失敗。兩者都不代表功能已完成，不得用來隱藏失敗。 | G0 初始的 Skip 代表功能尚未實作。 | Greenfield 檢查點 1（Skip）、檢查點 3（XFail） | pytest 官方文件〈How to use skip and xfail to deal with tests that cannot succeed〉 |
| Regression（回歸問題） | 修改後，原本正常的功能被改壞。Regression 測試就是確認既有功能沒被改壞：不移除既有測試，也不把正確的期待值改掉；因規則改變而過時的期待值，須列出規則編號（Rule ID）並經人核准後才更新。 | B1 修好學生票後，成人票相關測試仍要通過。 | B1 任務卡 | ISTQB〈Glossary〉 |
| PASS／FAIL／NOT VERIFIED | 通過／失敗／未驗證。沒有實際執行就只能寫未驗證，不能寫 PASS。 | 交付摘要的驗收結果欄。 | B3 三道 Gate | 本課程〈Digital Worker Delivery Summary〉 |
| 驗收對照表 | Agent 用來回報測試結果的表：每條驗收條件或規則一列，寫編號、白話內容、通過／失敗／未驗證，以及依據的測試名稱；最後一行是通過、失敗、跳過各幾個。你看這張表判斷結果，不看原始輸出或程式。 | B3 第 74 分鐘請 Agent 把驗收對照表寫進 `notes/b3.md`。 | Greenfield 檢查點 3 | 本課程〈Greenfield Acceptance Criteria〉 |
| 變更審查 | 取代自己讀變更內容（Diff）：請 Agent 用白話說明改了哪些檔案與原因，並以「是／否／不確定」回答三題：改的檔案都在核准範圍內？測試數沒有變少也沒有新增跳過？沒有刪測試，改過的期待值都附規則編號與核准紀錄？任何一題是「否」或「不確定」就不核准。 | B3 Gate 3 前的變更審查三題。 | Greenfield 檢查點 3 | Google Engineering Practices〈Google's Code Review Guidelines〉；本課程〈Coding Agent Usage Guide〉 |
| /docs（Swagger 介面） | 伺服器啟動後在瀏覽器開 `http://127.0.0.1:8000/docs` 看到的 API 測試頁面：點開 API → 按「Try it out」→ 在 Request body 貼上範例 → 按「Execute」→ 看 Response 的狀態碼和內容。不用打指令就能試 API。狀態碼 201 是成功、404 找不到、422 輸入資料驗證失敗（FastAPI 預設）；不符商業規則時，Greenfield 依它的提示詞約定回 400（例如人數 0 人或超過 4 人），既有的 Smart Ticket 程式（B0 起，B3 團體訂票沿用）則回 409，與「和目前狀態衝突」同一個碼（例如團體人數不在 5–20 人）。 | B3 Gate 3 前在 /docs 試團體訂票。 | Greenfield 檢查點 4 | FastAPI 官方文件〈First Steps〉；IETF〈RFC 9110 HTTP Semantics〉 |
| notes 資料夾（紀錄檔） | 學員 Repo 裡的 `notes/` 資料夾，由 Agent 把分析、計畫、核准決策原文、驗收對照表與交付摘要寫成檔案；你只做決定與核對，不用把內容抄進表單。 | `notes/b1.md`、`notes/b3.md`、`notes/delivery.md`。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| SHA256 雜湊 | 檔案的指紋：檔案只要有一個位元組被改，算出的值就不同；用來確認下載的檔案是原版、沒有損壞。 | 使用復原包時，核對下載卡上的 SHA256。 | B1 Recovery | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |

## Agent 技巧

| 詞彙 | 中文與白話解釋 | 今天的例子 | 首次出現 | 出處 |
|---|---|---|---|---|
| Agent 工作規則 | Agent 在整段對話都要遵守的約定：誰負責什麼、什麼時候停下、怎麼回報。先整段貼給 Agent，之後存成 Skill 檔，只說「先讀它」。 | Greenfield 與 Time Skip 貼的 7 條規則，共同脈絡段存進 `skills/team-rules.md`。 | Greenfield（先貼給 Agent：工作規則） | Claude Code 官方文件〈Best practices for Claude Code〉 |
| Prompt 結構（提示詞結構） | 好的提示詞有五個部分：目標、背景／要讀的檔、限制、輸出格式、停止條件（做完停下等我）。 | Runbook 每段可複製的提示詞都照這五部分寫。 | Greenfield 檢查點 2 | Anthropic〈Prompting best practices〉；OpenAI〈Prompt engineering〉 |
| Structured Output（結構化輸出） | 要求 Agent 用固定格式回報（固定欄位的表格、固定標題或 JSON），人看得快、能比對，也能交給下一個 Agent 或程式處理。今天是用提示詞要求格式，Agent 仍可能漏欄，要檢查；官方文件中的 Structured Outputs 是程式呼叫模型時，用 JSON Schema 強制輸出格式的功能。 | 驗收對照表、B2 方案比較表、B3 Gate 回報格式、交付摘要十二欄。 | Greenfield 檢查點 3 | Anthropic〈Structured outputs〉；OpenAI〈Structured model outputs〉 |
| Skill（可重複使用的工作說明） | 把一套反覆要用的做法寫成 Markdown 檔，之後只要說「請先讀 skills/… 並照做」。這裡的 Skill 是一般 Markdown 檔，靠你在提示詞說「先讀它」才會用到；工具內建的 Skill 功能（例如 Agent Skills）有固定的資料夾、檔名與開頭欄位，放對位置後 Agent 會在相關時自動讀取。 | `skills/team-rules.md`、`skills/fix-bug-with-test.md`、B3 的 `skills/b3-work-order.md`。 | 共同脈絡 檢查點 2 | Anthropic〈Agent Skills〉 |
| Token（詞元）與節費 | Token 是 Agent 讀寫文字的計費與記憶單位；對話越長、貼越多，越貴也越容易忘。節費做法：一個任務一個新對話、只讀指定的檔、要摘要不要整段輸出、把共識寫成檔案。 | B1 只讀 `skills/team-rules.md` 與任務卡；B3 細節寫進 `notes/b3.md`，對話只回摘要。 | Time Skip 檢查點 2 | Anthropic〈Context windows〉；Anthropic〈Token counting〉 |
| 模型選擇 | 簡單、機械性的工作（跑測試、整理格式、改文字）用快速、便宜的模型；分析陌生程式、設計取捨、自主執行用推理能力較強的模型。 | 個人分析陌生程式時選較強的模型；B3 自主執行時，主要 Agent 也選較強的模型。 | 個人分析 檢查點 1 | Anthropic〈Choosing the right model〉 |
| 推論強度（Reasoning Effort） | 同一個模型可以調「想多深」：計畫、找 Bug 根因、比較方案、Gate 審查調高；小步、明確的修改調低。想越深越慢、越耗 Token。工具沒有這個設定時，在提示詞寫「先仔細想過再回答，列出你考慮過的可能」。 | 個人分析時調高；B2 比較方案時調高，核准後實作調回低。 | 個人分析 檢查點 1 | Anthropic〈Effort〉；OpenAI〈Reasoning models〉 |

## 常用工作術語

| 詞彙 | 中文與白話解釋 | 今天的例子 | 首次出現 | 出處 |
|---|---|---|---|---|
| Root Cause（根因） | 問題真正的原因；尚未驗證的說法應標為假設。 | B1 請 Agent 找出學生票折扣錯在哪裡，並用白話說明。 | B1 任務卡 | ISTQB〈Glossary〉 |
| Impact Analysis（影響分析） | 區分必須修改、可能受影響與不應修改的範圍。 | B2 請 Agent 比較方案時列出的影響範圍。 | B2 任務卡 | ISTQB〈Glossary〉 |
| Task Breakdown（工作拆解） | 把方案拆成可逐步核准、逐步執行的步驟。 | Greenfield 的 5–8 步計畫，一次只放行一小步。 | B2 檢查點 1 | 本課程〈TASK-B2-001：導入不可疊加的最有利優惠政策〉；Claude Code 官方文件〈Best practices for Claude Code〉 |
| Gate（核准關卡） | 人員做決定的檢查點；核准是決策，不等於功能已通過驗收。 | B3 的 Gate 1 需求理解、Gate 2 影響分析與設計、Gate 3 交付審查。 | 歡迎與使用方式（預告）；B3 | 本課程〈B3 人員核准 Gate〉；Anthropic Engineering〈Building effective agents〉 |
| APPROVE／APPROVE WITH CONDITIONS／REJECT | 核准／附條件核准／拒絕（REJECT AND REVISE 是退回修正）。附條件核准時，條件解除後才可續行。 | Gate 決策與例外回應表單的選項。 | B3 流程 | 本課程〈B3 人員核准 Gate〉 |
| Review（檢視） | 審查實際證據，核對需求、範圍與未完成事項。 | 看驗收對照表、變更審查答案與文件是否一致。 | Agent 工作方式與安全規則 | Google Engineering Practices〈Google's Code Review Guidelines〉 |
| Delivery（交付）／Delivery Summary（交付摘要） | 把成果與證據整理成可審查的摘要交出去；交付不等於完整軟體上線。 | 第 76–80 分鐘請 Agent 把交付摘要寫進 `notes/delivery.md`，人核對證據。 | 交付 | 本課程〈Digital Worker Delivery Summary〉 |
| Level（完成等級） | B3 的完成程度：Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付。依證據擇一，不自動選 Level 3。 | 只完成 Gate 1／2 的分析與設計時，如實交付 Level 1。 | B3 檢查點 4 | 本課程〈B3 人員核准 Gate〉 |
| Work Order（工作命令） | 交給 Agent 的正式工作說明，含範圍、限制與停止條件；就是給 Agent 的 Skill。 | B3 第 63 分鐘交給主要 Agent，存成 `skills/b3-work-order.md`。 | B3 | 本課程〈Digital Worker Work Order〉 |
| Escalation（升級處理） | Agent 遇到停止條件時停下，提出證據與選項，交給人決定。 | Agent 想加入外部資料庫時，停下來請人決定。 | B3 例外回應卡 | 本課程〈Exception Response 與 Escalation〉 |
| Exception Response（例外回應） | 主持人宣布例外事件時，Agent 先停下整理提議與證據，人判斷是否在核准範圍內並回一句決定。 | 第 69–70 分鐘的例外事件。 | B3 檢查點 3 | 本課程〈Exception Response 與 Escalation〉 |
| 提示詞清單 | 把今天用過的技巧寫成可直接貼給 Agent 的提示詞，會變的部分用〈 〉標出，並寫明做完要看什麼證據。 | 回顧時每人請 Agent 寫進 `notes/my-prompts.md` 的 3 段提示詞，最常用的一段另存成 Skill 檔。 | 回顧 | 本課程〈回顧：把今天的技巧變成自己的提示詞清單〉 |
| 段落經過時間 | 從當段開始計算；與全場經過時間分開標示。 | B3 段內第 3 分鐘＝全場第 66 分鐘。 | B3 工作單 | 本課程〈Digital Worker Work Order〉 |

## Runbook 操作

| 詞彙 | 中文與白話解釋 | 今天的例子 | 首次出現 | 出處 |
|---|---|---|---|---|
| 活動解鎖碼 | 主持人在各段開始時向全場公布，於鎖頭章節輸入；大小寫、空白與連字號不影響輸入。 | 第 44 分鐘輸入 B1 的解鎖碼。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| Recovery（復原包） | 進度落後時改用的接續基線：一份已完成前一段的程式，讓小組能接著做下一段。使用復原包不算小組自行完成前段任務。 | B1 沒完成時，B2 改從 B1 復原包開始。 | 歡迎與使用方式 | 本課程〈B1 Recovery：52 分鐘按需切換〉 |
| 復原基線碼（Recovery） | 下載復原包用的解鎖碼。主持人只於52／63分鐘按需核准後個別提供；與B2／B3活動碼分開，不算小組自行完成前段任務。 | 第 52 分鐘向主持人申請 B1 復原包。 | 歡迎與使用方式 | 本課程〈B1 Recovery：52 分鐘按需切換〉 |
| 步驟勾選 | 用來追蹤進度；勾選只代表你已實際確認。 | 頁面上的勾選清單。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| 複製按鈕 | 提示詞區塊右上角的「複製」把整段提示詞複製下來；文件上方的「複製 Markdown」把整份文件複製下來，接在提示詞後面一起貼給 Agent。你不用自己打字。 | B3 檢查點 1 把任務卡、操作規則、工作單與三道 Gate 接在交辦提示詞後面。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
| 匯出 Markdown | 瀏覽器允許本機儲存時，表單內容會自動暫存；可下載 `.md` 檔，或用「複製 Markdown」貼到主持人指定的交付位置。 | 第 89–90 分鐘一次匯出所有表單。 | 歡迎與使用方式 | 本課程〈歡迎與使用方式〉 |
