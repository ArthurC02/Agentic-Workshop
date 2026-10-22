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
| MVP（最小可行產品） | 用最少的力氣做出、能拿給真實使用者驗證想法的版本；重點是學到東西，不只是功能少。今天指查班次、訂票、模擬付款與查訂單。 | Eric Ries《The Lean Startup》；本課程〈Greenfield 任務：核心訂票 MVP〉 |
| Agent（Coding Agent） | 由 AI 模型自己決定步驟、使用工具（讀寫檔案、執行指令與測試）完成任務的程式；Coding Agent 專做軟體開發。聊天式助手只回文字，Agent 會自己動手、看結果再決定下一步。 | Anthropic Engineering〈Building effective agents〉；Claude Code 官方文件〈Glossary〉 |
| 主要 Agent | 小組選定、代表全組執行工作的那一個 Agent。 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |
| Shared Context（共同脈絡） | 小組整理出的共同事實、分歧與待決事項，由 Agent 寫成 `notes/shared-context.md`。 | 本課程〈Shared Context：把共識寫成檔案給 Agent〉 |

## 證據

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Rule ID（規則編號） | 商業規則的編號，例如 `FARE-002`：學生為基礎票價的 75%。 | 本課程〈Greenfield Business Requirements〉 |
| AC（驗收條件） | Acceptance Criteria，功能要被使用者或客戶接受前必須滿足、能判定符合與否的條件，例如 `AC-B1-001`。 | ISTQB〈Glossary〉；本課程〈Greenfield Acceptance Criteria〉 |
| 驗收對照表 | Agent 回報測試結果的表：每條驗收條件一列，寫編號、白話內容、通過／失敗／未驗證、依據的測試名稱；最後一行是通過、失敗、跳過各幾個。 | 本課程〈Greenfield Acceptance Criteria〉 |
| 變更審查 | 你不讀程式的修改內容（Diff），改請 Agent 回答固定的審查問題，這些回答就是審查答案。Greenfield 用白話答四題並建議放不放行，B1 起照審查準則逐題答「是／否／不確定」；由你判斷要不要放行。 | Google Engineering Practices〈Google's Code Review Guidelines〉；本課程〈Coding Agent Usage Guide〉 |
| 審查準則 | `AGENTS.md` 裡的一節，由人定：變更審查要答哪三題、哪些算「重要」、哪些是小問題（最多報 5 條）或不用報。寫程式的 Agent 和另開對話的審查者都照這一份。 | Anthropic〈The AI-native SDLC playbook〉；本課程〈Shared Context：把共識寫成檔案給 Agent〉 |
| 審查紀錄 | 交付時另開一個只讀的對話當審查者，照審查準則檢查修改，把「重要／小問題」和「建議放行／不建議放行」寫進 `notes/b3.md`；寫程式的 Agent 不核准自己的成果。 | Anthropic〈The AI-native SDLC playbook〉；本課程〈Delivery Summary 與交付〉 |
| Skip／XFail | Skip 是略過測試；XFail 是把測試標成預期會失敗。兩者都不代表功能完成，不得用來隱藏失敗。 | pytest 官方文件〈How to use skip and xfail to deal with tests that cannot succeed〉 |
| Regression（回歸問題） | 修改後，原本正常的功能被改壞。既有測試要保留並通過；因規則改變而過時的期待值，要附規則編號並經人核准才更新。 | ISTQB〈Glossary〉 |
| Git／Commit | Git 記錄專案每一版的變化；Commit 是存下的一版，例如「G0 baseline」「B3 起點」。之後拿它比對「改了什麼」，也能還原。 | Pro Git〈About Version Control〉；Git 官方文件〈git-commit〉 |
| PASS／FAIL／NOT VERIFIED | 通過／失敗／未驗證。沒有實際執行就只能寫未驗證。 | 本課程〈Digital Worker Delivery Summary〉 |
| /docs | 伺服器啟動後，在瀏覽器開的 API 測試頁。點開 API，按「Try it out」，貼範例，再按「Execute」看狀態碼：200 或 201 是成功，404 是找不到，409 是不符商業規則或和目前狀態衝突，422 是輸入格式錯誤。 | FastAPI 官方文件〈First Steps〉；IETF〈RFC 9110 HTTP Semantics〉 |
| notes 資料夾 | Agent 把分析、計畫、核准決策與驗收紀錄寫成檔案的地方；你只做決定與核對。 | 本課程〈歡迎與使用方式〉 |
| SHA256 雜湊 | 檔案的指紋：只要改一個位元組，值就不同；用來確認下載的復原包是原版。 | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |
| 復原包（Recovery） | 進度落後時改用的接續版本，已完成前一段；使用它不算小組自行完成前段。 | 本課程〈B1 Recovery：第 52 分鐘，必要時才切換〉 |

## Agent 技巧

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Agent 工作規則 | Agent 在整段對話都要遵守的約定：誰負責什麼、什麼時候停下、怎麼回報。今天寫在 `AGENTS.md` 的「工作規則」。 | Claude Code 官方文件〈Best practices for Claude Code〉 |
| AGENTS.md | 放在專案根目錄、給 Coding Agent 看的說明：怎麼跑、工作規則、審查準則。多數 Coding Agent 開新對話會自動讀它；它是提醒，不是強制。同一個錯犯第二次，就加一行。 | OpenAI〈AGENTS.md〉；Claude Code 官方文件〈How Claude remembers your project〉 |
| Prompt 結構 | 像交辦工作一樣，說清楚這次要什麼、為什麼、完成的樣子、素材在哪；每次都要的規則放在 `AGENTS.md`，不用重寫。 | Anthropic〈Prompting best practices〉；OpenAI〈Prompt engineering〉 |
| Structured Output（結構化輸出） | 要求 Agent 用固定格式回報（固定欄位的表格或固定標題），人看得快、能比對。API 的同名功能則用 JSON 結構定義強制格式，今天不需要。 | Anthropic〈Structured outputs〉；OpenAI〈Structured model outputs〉 |
| Skill | 一套可重複使用的做法：一個資料夾裡的 `SKILL.md`，開頭 `name`、`description` 寫它叫什麼、什麼時候用。工具平常只讀名稱與說明，任務符合時才讀全文；放在工具會自動載入專案 Skill 的位置。今天有 `check`、`fix-bug-with-test`、`b3-work-order`。 | agentskills.io〈Agent Skills Overview〉；Anthropic〈Agent Skills〉 |
| Token 與節費 | Token 是模型讀寫文字的最小單位：計費和模型一次回答能參考多少內容（Context Window，脈絡視窗，包含整段對話與它正在寫的回答），都用它計算。節費：一個任務一個新對話、只讀指定的檔、要摘要不要整段輸出、把共識寫成檔案。 | Anthropic〈Context windows〉；Anthropic〈Token counting〉 |
| 模型選擇 | 機械性的工作用快速、便宜的模型；分析陌生程式、比較取捨、自主執行用較強的模型。 | Anthropic〈Choosing the right model〉 |
| 領先指標／落後指標 | 檢查一項做法有沒有效的兩個數字，每項做法各有自己的一組：領先指標是很快就會動的過程數字（例如規則檔：Agent 重犯同一個錯的次數），落後指標是要等一段時間的結果（例如新人第一次把修改合併進主線要多久）。 | Anthropic〈The AI-native SDLC playbook〉；本課程〈工作坊回顧〉 |
| 推論強度（Reasoning Effort） | 同一個模型「想多深」、花多少 Token：分析、比較方案調高，小步修改調低。工具沒有這個設定時，提示詞寫「先仔細想過再回答」。 | Anthropic〈Effort〉；OpenAI〈Reasoning models〉 |

## B3 用語

| 詞彙 | 白話解釋 | 出處 |
|---|---|---|
| Gate（核准關卡） | Agent 交出資料後停下、由人做決定的檢查點；核准是決策，不等於通過驗收。 | 本課程〈B3 工作單（Work Order）〉；Anthropic Engineering〈Building effective agents〉 |
| 核准／附條件／退回（APPROVE／APPROVE WITH CONDITIONS／REJECT AND REVISE） | 你在 Gate 卡上回的三種決定：核准；附條件（條件解除後才可續行）；退回修正。例外事件用「拒絕」（REJECT）。 | 本課程〈B3 工作單（Work Order）〉 |
| Work Order（工作單） | 交給 Agent 的整件任務說明：範圍、禁止事項、停止條件與回報格式；B3 存成 `b3-work-order` Skill。 | 本課程〈B3 工作單（Work Order）〉 |
| Escalation（升級處理） | Agent 遇到停止條件時停下，附證據與選項，交給人決定。 | 本課程〈B3 工作單（Work Order）〉 |
| Atomicity／Compensation | Atomicity：一組動作要嘛全部完成、要嘛全部不做。Compensation：失敗時把已做的部分還原，例如團體付款失敗就釋放全部座位。 | 本課程〈TASK-B3-001：新增團體訂票能力〉 |
| Level（完成等級） | Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付；依證據擇一，不自動選 Level 3。 | 本課程〈TASK-B3-001：新增團體訂票能力〉 |
