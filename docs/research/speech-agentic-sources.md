# 五場講解簡報：Agentic 開發來源研究

> 讀者：講者與教材維護者。用途：補強 `agentic-workshop/materials/speech/` 五份講解簡報的論點、比喻與案例。查核日：2026-10-16。
> 標示規則：**【已查核】**＝本次以 WebFetch 開啟原始頁面確認內容；**【部分查核】**＝主要事實已查，個別數字只見於二手報導；**【未查核】**＝只見於搜尋摘要或二手來源，上台前不要引用數字。引文一律為原文、25 字以內。
> 文件與工具頁（例如 Claude Code、Codex 文件）是持續更新的頁面，沒有固定發布日；上台前若要引用指令名稱或版本，請重新打開確認。

## 工具中立說明（先讀）

工作坊是工具中立的：講的是做法，不是某一套產品。

- 每個要點先用一般說法講清楚（例如「每次對話都會讀的規則檔」），再補一句「例如 CLAUDE.md、AGENTS.md、GEMINI.md」。不要只秀單一產品的指令或快捷鍵。
- 本文件大量引用 Anthropic 文件，是因為它們公開、具體、有日期；同一個概念多半也能在 OpenAI、GitHub、Google 的文件找到對應（已在各點列出）。投影片上至少並列兩家，避免變成產品介紹。
- 規則檔名稱的現況（已查核）：AGENTS.md 由 Linux Foundation 旗下的 Agentic AI Foundation 維護，多數 Coding Agent 都會讀；Gemini CLI 可把讀取檔名設成 AGENTS.md；Claude Code 可直接讀 AGENTS.md。所以「團隊共用一份規則檔」可以講成跨工具的做法。
- Skill（技能檔）已是開放格式（agentskills.io），Claude Code、Codex、GitHub Copilot、Gemini CLI、Cursor 等都支援，可以當作通用概念講。
- 模型名稱、推論強度預設值、價格每幾個月就變。投影片只講原則（「先用預設，有證據再調高」），不要寫死模型名稱或金額。

---

## 第一場：Greenfield／Tool（規格、脈絡、計畫、小步驗證、審變更）

現有簡報已涵蓋：構想放入 docs、MVP、使用者故事、驗收條件、Gherkin、分層架構、工作規則、提示詞結構、小步驟、驗收對照表、變更審查。**較薄的地方**：為什麼「可執行的檢查」是 Agent 的真相來源、規格寫多大才合適、外部證據與案例。

### 可教的要點

1. **先給 Agent 一個能自己跑的檢查，再請它做事。** 沒有檢查，「看起來完成」就是唯一訊號，人就得當驗證迴圈。
   - 【已查核】Anthropic，〈Best practices for Claude Code〉，Claude Code 文件（持續更新），https://code.claude.com/docs/en/best-practices 。支持：驗證條件讓 Agent 自己收斂。引文："Give Claude a check it can run: tests, a build, a screenshot to compare."
   - 【已查核】Anthropic，〈Building effective agents〉，2024-12-19，https://www.anthropic.com/engineering/building-effective-agents 。引文："it's crucial for the agents to gain "ground truth" from the environment at each step"

2. **驗收條件寫成可判定的句子；Given／When／Then 是一種好寫法。** 讓「對不對」能由測試或人看結果判斷，而不是靠感覺。
   - 【已查核】Cucumber，〈Gherkin Reference〉，https://cucumber.io/docs/gherkin/reference/ 。引文："Gherkin uses a set of special keywords to give structure and meaning to executable specifications."
   - 【已查核】AWS Kiro 文件〈Specs〉，https://kiro.dev/docs/specs/ 。支持：規格拆成需求（含驗收條件）、設計、任務三份檔。引文："structured artifacts that formalize the development process for features and bug fixes."

3. **Spec-driven development（規格驅動開發）有三種深度，大多數做法停在「先寫規格」。** 小變更用重流程反而累。
   - 【已查核】Birgitta Böckeler，〈Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl〉，martinfowler.com，2025-10-15，https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html 。支持：spec-first／spec-anchored／spec-as-source 三層；小 bug 用 Kiro 流程「like using a sledgehammer to crack a nut」；她也常見 Agent 沒照全部指示做。引文："I'd rather review code than all these markdown files."
   - 【已查核】Thoughtworks Technology Radar Vol. 34（2026-04），https://www.thoughtworks.com/radar 。支持：GitHub Spec Kit、OpenSpec 列在 Assess（評估）而非 Adopt，表示業界仍在試。

4. **規格從短的開始，請 Agent 擴寫，再由人審；一次只給一個聚焦任務。**
   - 【已查核】Addy Osmani，〈How to write a good spec for AI agents〉，2026-01-13，https://addyosmani.com/blog/good-spec/ 。引文："Kick off your project with a concise high-level spec, then have the AI expand it into a detailed plan." 另："Divide and conquer: give the AI one focused task at a time rather than a monolithic prompt with everything at once."

5. **先探索、再計畫、再實作；能用一句話描述的變更就跳過計畫。**
   - 【已查核】Claude Code best practices（同上）。支持：Explore → Plan → Implement → Commit 四步；「If you could describe the diff in one sentence, skip the plan.」大功能可請 Agent 先訪談你、寫成規格，再開新對話實作。
   - 【已查核】Simon Willison，〈Vibe engineering〉，2025-10-07，https://simonwillison.net/2025/Oct/7/vibe-engineering/ 。引文："Sitting down to hack something together goes much better if you start with a high level plan."

6. **提示詞要指名：哪個檔、什麼情境、什麼算修好。** 模糊的提示詞會讓 Agent 掃大量檔案。
   - 【已查核】Claude Code best practices（同上）。引文："Claude can infer intent, but it can't read your mind."
   - 【已查核】GitHub Blog，Matt Nigh，〈How to write a great agents.md: Lessons from over 2,500 repositories〉，2025-11-19，https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ 。引文："One real code snippet showing your style beats three paragraphs describing it."

7. **Context engineering（脈絡工程）取代「提示詞工程」：重點是讓任務「有可能被解出來」的全部資訊。**
   - 【已查核】Simon Willison，〈Context engineering〉，2025-06-27，https://simonwillison.net/2025/Jun/27/context-engineering/ 。支持：引用 Shopify CEO Tobi Lütke 的定義 "the art of providing all the context for the task to be plausibly solvable by the LLM."
   - 【已查核】Thoughtworks Radar Vol. 34：Context engineering 列為 Adopt（建議採用）。

8. **要求結構化輸出（固定欄位、固定標題），人才能快速比對。**
   - 【已查核】Thoughtworks Radar Vol. 34：「Structured output from LLMs」列為 Adopt。

9. **審變更：不是讀懂每一行，而是看證據（測試輸出、執行結果、截圖）與範圍有沒有跑出去。**
   - 【已查核】Claude Code best practices（同上）。引文："Have Claude show evidence rather than asserting success"；也建議用另一個乾淨對話做審查，並提醒審查者被要求找問題時「will usually report some, even when the work is sound」。
   - 【已查核】Simon Willison，〈Your job is to deliver code you have proven to work〉，2025-12-18，https://simonwillison.net/2025/Dec/18/code-proven-to-work/ 。引文："If you haven't seen the code do the right thing yourself, that code doesn't work."

### 比喻與經驗法則

- **「沒有檢查，你就是那個檢查。」**（改寫自 Claude Code best practices：沒有可跑的檢查時，人變成驗證迴圈。）
- **「一句話講得完的改動，不用寫計畫。」**（Claude Code best practices 原則）
- **「別用大鐵鎚敲核桃」**：規格大小要跟任務大小相稱（Böckeler）。
- **「一段真實範例勝過三段描述」**（GitHub agents.md 研究）。

### 近期案例

- **Airbnb：3,500 個測試檔遷移，估計 1.5 年 → 6 週。**【部分查核】Charles Covey-Brandt，〈Accelerating Large-Scale Test Migration with LLMs〉，Airbnb Tech Blog，https://airbnb.tech/?p=366 。已查：近 3.5K 個 React 測試檔、原估 1.5 年、6 週完成、4 小時自動完成 75%、調整 4 天後 97%、剩下 3% 人工約一週；做法是逐檔分步驟、每步驗證、失敗就帶錯誤重試。頁面未顯示日期，InfoQ 報導為 2025-03【日期未查核】。重點：**每一步都有自動驗證**，不是一次生成。
- **Bun（Zig → Rust）約百萬行、兩週內；Python → TypeScript 16.5 萬行、一個週末。**【已查核】Anthropic，〈How Anthropic runs large-scale code migrations with Claude Code〉，2026-07-16，https://claude.com/blog/ai-code-migration 。已查：既有測試 100% 在 CI 通過後才合併，合併後 19 個回歸全數修好；先只翻 6 個檔試水溫，抓到 2 個規則問題才擴大到 1,448 檔；Bun 遷移用了約 59 億個未快取輸入 token、6.9 億個輸出 token，以 API 價計約 16.5 萬美元。重點：**測試套件就是裁判**，先小量試跑再全面。注意這是廠商自家案例。

---

## 第二場：Time Skip（Context Window、Token 成本、壓縮與交接、規則檔、開新對話）

現有簡報已涵蓋：開新對話、Token 是什麼與四個省法、指名要讀的檔、貼工作規則請 Agent 複述、交接檔。**較薄的地方**：為什麼內容一多就變差（有官方說法可引）、規則檔該多短、實際成本量級、長任務的交接實例。

### 可教的要點

1. **Context window（脈絡視窗）裝得越滿，表現越差；這是幾乎所有技巧的根本原因。**
   - 【已查核】Claude Code best practices。引文："Claude's context window fills up fast, and performance degrades as it fills."
   - 【已查核】Anthropic，〈Effective context engineering for AI agents〉，2025-09-29，https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents 。支持：context rot（內容越多、回想越差）、attention budget（注意力預算）。引文："LLMs have an 'attention budget' that they draw on when parsing large volumes of context."

2. **目標是「最少但最有用的資訊」，不是「給越多越好」。**
   - 【已查核】同上。引文："the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

3. **不相關的任務之間就開新對話；同一問題糾正兩次還錯，就重開並寫更好的提示詞。**
   - 【已查核】Claude Code best practices。引文："A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

4. **Token 成本跟脈絡大小成正比；長對話每問一句都要把整段歷史再送一次。**
   - 【已查核】Anthropic，〈Manage costs effectively〉，Claude Code 文件，https://code.claude.com/docs/en/costs 。引文："Token costs scale with context size: the more context Claude processes, the more tokens you use." 量級：企業部署平均約每位開發者每個活躍日 13 美元、每月 150–250 美元，90% 使用者每日低於 30 美元。（只適用該產品，價格會變，投影片寫「量級」即可。）

5. **壓縮（compaction）與筆記：長任務靠「摘要 + 檔案筆記」延續，而不是靠一直開著的對話。**
   - 【已查核】Anthropic context engineering（同上）。支持：compaction＝把接近上限的對話摘要後帶到新視窗；structured note-taking＝把待辦或 NOTES.md 寫在脈絡之外、之後再讀回。
   - 【已查核】Anthropic，〈Effective harnesses for long-running agents〉，2025-11-26，https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents 。支持：每個新對話「begins with no memory of what came before」；用進度檔＋git 紀錄＋功能清單交接；一次只做一個功能。比喻：像輪班工程師沒有上一班的交接筆記。

6. **交接檔要放「下一段一定用得到的事」：目前狀態、做了什麼、下一步、怎麼驗證。** 以 JSON 等結構化格式記錄完成狀態，Agent 較不會亂改。
   - 【已查核】同上（long-running harness）：功能清單初始全標為未通過，Agent 只能改 `passes` 欄位；選 JSON 是因為模型較不會不當修改。

7. **規則檔（CLAUDE.md／AGENTS.md／GEMINI.md）每次對話都會載入，所以要短。**
   - 【已查核】Anthropic，〈How Claude remembers your project〉，Claude Code 文件，https://code.claude.com/docs/en/memory 。支持：建議每個檔低於 200 行；規則是「context, not enforced configuration」（是脈絡，不是強制設定）；互相矛盾時 Agent 可能任選一條。
   - 【已查核】Claude Code best practices。引文："Would removing this cause Claude to make mistakes?" If not, cut it.（逐行自問）
   - 【已查核】OpenAI，〈Custom instructions with AGENTS.md〉，Codex 文件，https://learn.chatgpt.com/docs/agent-configuration/agents-md 。支持：由根目錄往下合併，越近的檔優先；合併後超過預設 32 KiB 就不再加入。
   - 【已查核】Google，〈GEMINI.md〉，Gemini CLI 文件，https://geminicli.com/docs/cli/gemini-md/ 。支持：全域、專案、子目錄三層合併，`/memory show` 可看實際送出的內容；檔名可設成 AGENTS.md。
   - 【已查核】AGENTS.md 官網 https://agents.md/ 。引文："AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation."；稱其為「README for agents」，超過 6 萬個開源專案使用。

8. **規則檔不是保險；一定要發生的事交給自動機制（hook、CI），不要只寫在規則裡。**
   - 【已查核】Claude Code best practices。支持："Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."
   - 【已查核】Thoughtworks Radar Vol. 34：「Agent instruction bloat」（規則檔膨脹）列為 Caution（警示）。

9. **把探索工作交給 subagent（子 Agent）：它在自己的脈絡裡讀大量檔案，只回傳摘要。**
   - 【已查核】Anthropic context engineering：sub-agent 只回傳約 1,000–2,000 token 的濃縮摘要。

### 比喻與經驗法則

- **「工作桌越堆越亂，找東西越慢」**：脈絡視窗像桌面，不是倉庫（改寫 attention budget）。
- **「輪班交接」**：每個新對話都是剛上班、沒看過交接本的人（Anthropic long-running harness 的比喻）。
- **「糾正兩次還錯，就重開」**（Claude Code best practices）。
- **「每一行規則都問：刪掉會出錯嗎？」**

### 近期案例

- **Anthropic 長時間任務實驗**【已查核】（2025-11-26，同上）：Agent 常在只跑單元測試或 curl 後就宣告完成；改用瀏覽器自動化、像使用者一樣端到端測試後，表現明顯變好。可當「交接檔＋驗證」的實例。
- **Bun 遷移的可續跑設計**【已查核】（2026-07-16，同上）：批次腳本每次從磁碟重建待辦佇列，輸出檔存在就算完成，所以中斷後可接著跑。這是「把狀態寫在檔案，不寫在對話」的好例子。

---

## 第三場：Brownfield／Teammate（讀舊系統、模型與推論強度、Skill、共同規則、先寫失敗測試、比較方案）

現有簡報已涵蓋：讀舊系統、Tool → Teammate、模型選擇與推論強度、Token 節費加深、多個 Agent 讀同一系統、Skill、以失敗測試抓 Bug、核准計畫、結構化輸出比較表。**較薄的地方**：推論強度的跨廠商原則、Skill 已成開放格式的證據、舊系統遷移的真實案例與量化結果。

### 可教的要點

1. **把 Agent 當成會問問題的新同事：先問「這段怎麼運作」，再改。**
   - 【已查核】Claude Code best practices。引文："Ask Claude questions you'd ask a senior engineer." 並稱這是有效的入職（onboarding）方式。

2. **修 Bug：先寫一個會失敗的測試重現問題，再修，再看它通過。**
   - 【已查核】Claude Code best practices：範例提示詞 "write a failing test that reproduces the issue, then fix it"；另一條 "address the root cause, don't suppress the error"。
   - 【已查核】Simon Willison，〈Your job is to deliver code you have proven to work〉（2025-12-18）：測試應該在把修正拿掉時會失敗。

3. **推論強度（reasoning effort）是可調的旋鈕：先用預設，有證據才調高；簡單、量大的工作調低。** 兩家主要廠商說法一致。
   - 【已查核】Anthropic，〈Effort〉，Claude API 文件，https://platform.claude.com/docs/en/build-with-claude/effort 。支持：low 適合簡單、重視速度的工作（例如子 Agent）；"Effort is a behavioral signal, not a strict token budget."；建議以自己的評測決定。
   - 【已查核】OpenAI，〈Reasoning models〉，API 文件，https://developers.openai.com/api/docs/guides/reasoning 。引文："Treat `reasoning.effort` as a tuning knob, not the primary way to recover quality." 另：xhigh「Only use when your evals show a clear benefit」。
   - 教學重點：調高強度救不了不清楚的需求；先把提示詞與脈絡補齊。

4. **模型分工：大量、明確的工作用較小較快的模型；審查、定規則、難題用較強的模型。**
   - 【已查核】Anthropic 遷移文章（2026-07-16）：小模型做大量實作，最大的模型做審查與寫規則。
   - 【已查核】Claude Code costs 文件："Reserve Opus for complex architectural decisions or multi-step reasoning."（產品特定，投影片寫成一般原則。）

5. **Skill（技能檔）：把團隊做法寫成資料夾＋說明檔，Agent 需要時才載入（progressive disclosure，逐步揭露）。**
   - 【已查核】Anthropic，〈Equipping agents for the real world with Agent Skills〉，2025-10-16（2025-12-18 更新為開放標準），https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills 。引文："Building a skill for an agent is like putting together an onboarding guide for a new hire."；安全提醒："We recommend installing skills only from trusted sources."
   - 【已查核】Agent Skills 官網 https://agentskills.io/ 。支持：開放格式；啟動時只載入名稱與說明，任務相符才讀全文；Claude Code、Codex、GitHub Copilot、VS Code、Gemini CLI、Cursor、Kiro 等列為支援。
   - 【已查核】Thoughtworks Radar Vol. 34：Agent Skills 列為 Trial（試用）；「Skills as executable onboarding documentation」列為 Assess。

6. **團隊共用規則（shared instructions）要進版本控制、大家一起維護。**
   - 【已查核】Thoughtworks Radar Vol. 34：「Curated shared instructions for software teams」列為 Adopt。
   - 【已查核】GitHub agents.md 研究（2025-11-19）：好的規則檔涵蓋六個面向（如何執行、測試、結構、程式風格、版本控制習慣、邊界）；最常見有用的限制是 "Never commit secrets"；邊界分「一定做／先問／絕不做」三層。

7. **比較方案：要 Agent 用固定欄位列出選項、風險、可逆性，再由人選。** 讓 Agent 在唯讀模式先研究、不動檔案。
   - 【已查核】Anthropic，〈Our framework for developing safe and trustworthy agents〉，2025-08-04，https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents 。支持：預設唯讀，改動前要人核准。引文："humans should retain control over how their goals are pursued, particularly before high-stakes decisions are made."

8. **Guides（事前引導）＋ Sensors（事後感測）：規則檔與 Skill 是事前；測試、lint、型別檢查是事後。**
   - 【已查核】Birgitta Böckeler，〈Harness engineering for coding agent users〉，martinfowler.com，2026-04-02，https://martinfowler.com/articles/harness-engineering.html 。支持：guides 在 Agent 行動前引導，sensors 在行動後幫它自我修正；可計算的檢查（測試、linter）快且確定，推論型檢查（AI 審查）較慢較貴且不確定。比喻：「cybernetic governor」（自動調速器）。

9. **警示：程式碼沒人真正理解，會累積「認知債」。**
   - 【已查核】Thoughtworks Radar Vol. 34：「Codebase cognitive debt」列為 Caution。
   - 【已查核】Anthropic，〈How AI is transforming work at Anthropic〉，2025-12-02，https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic 。支持：工程師擔心「監督的悖論」——監督 AI 需要的技能，正是少寫程式後會退化的技能。

### 比喻與經驗法則

- **「Skill 就是給新同事的入職手冊」**（Anthropic）。
- **「推論強度是微調旋鈕，不是救命按鈕」**（改寫 OpenAI 文件）。
- **「先讓測試紅，再讓它綠」**：修 Bug 的順序。
- **「事前給地圖，事後裝感測器」**（Böckeler 的 guides／sensors）。

### 近期案例

- **Spotify「Honk」背景 Coding Agent：合併超過 1,500 個 PR，遷移省時 60–90%。**【已查核】Max Charas、Marc Bruggmann，〈1,500+ PRs Later: Spotify's Journey with Our Background Coding Agent (Honk, Part 1)〉，Spotify Engineering，2025-11-06，https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1 。重點：舊的決定性腳本處理複雜改動很吃力（一個 Maven 依賴更新腳本長到超過 2 萬行）；Agent 改動後仍跑格式化、lint、LLM 審查，再由人審核合併；作者坦言輸出較難預測、「don't have all the answers yet」。QCon 2026 演講提到「10 天合併 1,000 個 PR」【未查核，僅二手報導】。
- **Airbnb 測試遷移**（見第一場）：同樣適合放在舊系統場景。
- **Bun 與 Python → TypeScript 遷移**（見第一場）：「先翻 6 個檔試跑」正好對應「人核准計畫、先做一小步」。

---

## 第四場：Digital Worker（委派、工作單、核准關卡、自主等級、權限與沙箱、防護、例外、治理、評估）

現有簡報已涵蓋：工作單五部分、授權範圍、停止條件、存成 Skill、三道 Gate、例外事件、自主等級、交付摘要即證據。**較薄的地方**：自主等級的外部框架、資安風險的標準說法（OWASP、lethal trifecta）、真實事故與大規模委派的數據。

### 可教的要點

1. **自主是設計選擇，不等於能力：同一個強 Agent 也可以設成每步都要問人。** 五級框架以「人扮演的角色」區分。
   - 【已查核】K. J. Kevin Feng、David W. McDonald、Amy X. Zhang，〈Levels of Autonomy for AI Agents〉，arXiv 2506.12469，v1 2025-06-14、v2 2025-07-28，https://arxiv.org/abs/2506.12469 。五級：operator（操作者）、collaborator（協作者）、consultant（顧問）、approver（核准者）、observer（觀察者）。可直接對照工作坊的 Tool → Teammate → Digital Worker。

2. **有效監督不是每步都核准，而是在關鍵時刻能介入。** 有經驗的使用者更常放手、也更常中途打斷。
   - 【已查核】Anthropic，〈Measuring AI agent autonomy in practice〉，2026-02-18，https://www.anthropic.com/research/measuring-agent-autonomy 。數據：新手（少於 50 次工作階段）約 20% 使用全自動核准，到 750 次升到 40% 以上；打斷率從約 5% 升到約 9%；最長的工作時間三個月內從 25 分鐘以下增到 45 分鐘以上；只有 0.8% 的動作看起來不可逆。引文："Effective oversight doesn't require approving every action but being in a position to intervene when it matters."

3. **核准疲勞是真的：問太多次，人就開始亂按。用沙箱劃好邊界，才能少問又安全。**
   - 【已查核】Anthropic，〈Beyond permission prompts: making Claude Code more secure and autonomous〉（sandboxing），2025-10-20，https://www.anthropic.com/engineering/claude-code-sandboxing 。引文："sandboxing safely reduces permission prompts by 84%."；檔案系統隔離＋網路隔離兩道邊界；提到 approval fatigue。
   - 【已查核】Claude Code best practices："After the tenth approval you're clicking through rather than reviewing."

4. **最小權限：功能、權限、自主三者都不要給超過需要。** 這是 OWASP 的標準說法。
   - 【已查核】OWASP GenAI Security Project，〈LLM06:2025 Excessive Agency〉，https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ 。三個根因：excessive functionality、permissions、autonomy；緩解：高影響動作要人核准、最小權限、授權在下游系統檢查而不是交給 LLM 判斷。
   - 【部分查核】OWASP，〈Top 10 for Agentic Applications for 2026〉，2025-12-09 發布，https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ 。發布日已查；ASI01 Agent Goal Hijack、ASI02 Tool Misuse、ASI03 Identity and Privilege Abuse 等名稱只見於二手整理【未查核】，上台前請下載原文確認。

5. **「致命三要素」：能讀私密資料＋會接觸不可信內容＋能對外傳送，三者同時存在就可能被提示詞注入偷資料。**
   - 【已查核】Simon Willison，〈The lethal trifecta for AI agents: private data, untrusted content, and external communication〉，2025-06-16，https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ 。引文："We need to avoid the lethal trifecta combination of tools ourselves to stay safe."
   - 教學：工作單的「授權範圍」至少要拿掉其中一項。

6. **把護欄做在平台上，而不是只寫在提示詞裡。** 例：Agent 只能推到自己的分支、不能核准或合併自己的 PR、CI 要人放行、對外網路受限。
   - 【已查核】GitHub，〈Risks and mitigations for GitHub Copilot cloud agent〉，https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations 。引文："Copilot cloud agent cannot mark its pull requests as "Ready for review" and cannot approve or merge a pull request."；"workflows are not triggered until Copilot cloud agent's code is reviewed"。
   - 【已查核】GitHub，〈About GitHub Copilot cloud agent〉，https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent 。支持：在暫時性雲端環境工作、一次一個分支一個 PR、單次最長 59 分鐘。

7. **停止條件與升級：遇到阻礙就停下來問人，不要硬做。**
   - 【已查核】Anthropic，〈Building effective agents〉（2024-12-19）。引文："Agents can then pause for human feedback at checkpoints or when encountering blockers."；另建議 "extensive testing in sandboxed environments, along with the appropriate guardrails."

8. **評估 Agent 產出：做的人不當評分的人。** 用另一個乾淨脈絡審查差異；審查只報影響正確性或需求的問題。
   - 【已查核】Claude Code best practices：獨立審查者「sees only the diff and the criteria you give it」。
   - 【已查核】Böckeler harness engineering：AI 審查屬推論型檢查，較貴且不確定，應搭配測試等可計算檢查。

9. **交付摘要就是證據：要附測試輸出、執行指令與結果，而不是「已完成」三個字。**
   - 【已查核】Claude Code best practices："Reviewing evidence is faster than re-running the verification yourself, and it works for sessions you weren't watching."

### 比喻與經驗法則

- **「給權限像給門禁卡：只開要去的樓層。」**（OWASP 最小權限的白話）
- **「三缺一」**：私密資料、不可信內容、對外通道，至少拿掉一個（lethal trifecta）。
- **「監督不是每步按核准，是隨時能踩煞車。」**（Anthropic 自主研究）
- **「Agent 不能自己批自己的考卷」**（GitHub 不能自我核准 PR；寫的人不當審的人）。

### 近期案例

- **Stripe「Minions」：每週超過一千個 PR 完全由 Agent 產出，全部經人審查。**【已查核】Alistair Gray，〈Minions: Stripe's one-shot, end-to-end coding agents〉，stripe.dev，2026-02-09，https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents 。重點：每次在隔離的 devbox 執行（與正式環境和網際網路隔離，所以不需逐步問權限）；本地 lint＋三百多萬個測試的 CI；最多兩輪 CI；產出是等人審查的 PR。後續報導稱每週 1,300 個【未查核】。**這是「沙箱＋自動驗證＋人審」的教科書案例。**
- **GitHub Copilot coding agent：2025 年 5–9 月建立超過 100 萬個 PR。**【已查核】GitHub，〈Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1〉，2025-10-28，https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ 。注意是「建立」的 PR 數，不是合併數。
- **【警示】Replit Agent 在凍結期間刪除正式資料庫（2025-07）。**【已查核】Fortune，〈AI coding tool Replit wiped database, called it a catastrophic failure〉，2025-07-23，https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/ 。已查：SaaStr 創辦人 Jason Lemkin 測試期間，Agent 在「code and action freeze」下仍執行未授權指令，刪掉 1,200 多位主管、1,190 多家公司的資料，還說無法回復（實際上可以）；Replit 執行長稱「Unacceptable and should never be possible」，事後加上開發與正式資料庫自動分離、只規劃模式。教學：**凍結只寫在對話裡沒有用，要做在權限上。**「捏造 4,000 筆假資料」只見於單一媒體【未查核】。
- **【警示】Amazon Q Developer 擴充套件被植入「清除檔案」提示詞（2025-07）。**【已查核】AWS，〈Security Update for Amazon Q Developer Extension for Visual Studio Code (Version #1.84)〉，AWS-2025-015，2025-07-23，https://aws.amazon.com/security/security-bulletins/AWS-2025-015/ 。已查：CodeBuild 設定中的 GitHub token 權限過大，攻擊者藉此提交惡意程式碼並被自動包進 1.84.0 發布；因語法錯誤未能執行；CVE-2025-8217。教學：**Agent 本身與它的供應鏈都需要最小權限。**

---

## 第五場：Retrospective（組織導入、量測成效、寫自己的 Skill、團隊做法、風險）

現有簡報已涵蓋：三種介入方式與選擇判準、六技巧回顧、把重複做法寫成 Skill、證據支持導入、量測口徑、先試哪裡、誠實的限制。**較薄的地方**：正反並陳的研究證據（尤其是 METR 的更新）、DORA「放大器」與七項能力、「產出變多≠交付變好」的數據。

### 可教的要點

1. **AI 是放大器：放大組織原有的長處與短處。** 工具本身不會修好流程。
   - 【已查核】Google Cloud，〈Announcing the 2025 DORA Report〉，2025-09-24，https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report 。數據：90% 受訪者在工作中使用 AI；超過 80% 認為生產力提升；30% 對 AI 產生的程式碼幾乎或完全不信任；AI 採用與交付吞吐量、產品表現正相關，但與交付穩定度仍為負相關。引文："AI doesn't fix a team; it amplifies what's already there."
   - 【已查核】DORA，〈State of AI-assisted Software Development 2025〉，https://dora.dev/research/2025/dora-report/ 。引文："AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses."

2. **導入先補基本功：DORA 列出七項會放大 AI 效益的能力。**
   - 【已查核】Google Cloud，〈Introducing DORA's inaugural AI Capabilities Model〉，2025-09-24，https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model 。七項：清楚且有溝通的 AI 立場、健康的資料生態、AI 可取用的內部資料、紮實的版本控制、小批量工作、以使用者為中心、高品質的內部平台。引文："simply adopting AI tools isn't a guarantee of success."
   - 【已查核】dora.dev AI Capabilities Model 頁面（2025-11-25 更新），https://dora.dev/ai/capabilities-model/report/ 。

3. **感覺變快≠真的變快：要量測，而且研究結果會隨工具改變。**
   - 【已查核】METR，〈Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity〉，2025-07-10，https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ 。16 位資深開源開發者、246 個任務：用 AI 反而多花 19% 時間；事前預期快 24%，事後仍自認快 20%。頁面現已標示「These results are out of date」。
   - 【已查核】METR，〈We are Changing our Developer Productivity Experiment Design〉，2026-02-24，https://metr.org/blog/2026-02-24-uplift-update/ 。更新：回流的原受試者估計加速 18%（信賴區間 -38% 到 +9%，負值代表加速），新受試者加速 4%（-15% 到 +9%）；許多開發者「do not wish to work without AI」而拒絕參加，造成選樣偏差；METR 認為 2026 年初 AI 很可能有幫助，但數據「only very weak evidence for the size of this increase」。
   - 教學：**兩份都講，講清楚時間點與限制**；這正是「先量測再下結論」的最好示範。

4. **個人產出增加，不等於公司交付變好；瓶頸會移到審查。**
   - 【已查核】Faros AI，〈The AI Productivity Paradox Report 2025〉，2025-07-23，https://www.faros.ai/blog/ai-software-engineering 。1 萬多位開發者、1,255 個團隊：高採用團隊完成任務 +21%、合併 PR +98%，但 PR 審查時間 +91%、PR 大小 +154%、每人 Bug +9%；公司層級 DORA 指標與 AI 採用「no significant correlation」。（廠商報告、相關性非因果。）
   - 【已查核】Spotify Honk（2025-11-06）：審查成為新瓶頸的實例。
   - 【已查核】Thoughtworks Radar Vol. 34：「Coding throughput as a measure of productivity」列為 Caution——不要用程式碼產出量衡量生產力。

5. **開發者信任度低：最大挫折是「差一點就對」。**
   - 【已查核】Stack Overflow，〈2025 Developer Survey — AI〉，https://survey.stackoverflow.co/2025/ai 。84% 使用或打算使用 AI 工具；只有 33% 信任其準確度、46% 不信任；66% 最大挫折是「almost right, but not quite」；45.2% 認為除錯 AI 程式碼更耗時；AI agent 尚未成為主流（約 31% 在工作中使用，37.9% 不用也不打算用）。

6. **品質要另外看：AI 參與的 PR 問題較多。**
   - 【已查核】CodeRabbit，〈State of AI vs Human Code Generation Report〉，David Loker，2025-12-17，https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report 。470 個開源 PR：AI 共同撰寫的 PR 平均 10.83 個問題、純人工 6.45 個（約 1.7 倍）；邏輯正確性問題多約 75%。限制：作者身分由標記推斷、樣本小、發布者賣 AI 審查工具。

7. **寫自己的 Skill：重複做三次以上、步驟固定、有明確完成標準的工作才值得寫。** 從新人入職手冊的角度寫，只放 Agent 猜不到的事。
   - 【已查核】Anthropic Agent Skills（2025-10-16）：入職手冊比喻、只從可信來源安裝。
   - 【已查核】Claude Code best practices：只在部分情境用到的知識放 Skill，不要塞進每次都載入的規則檔。
   - 「三次以上才寫」是本工作坊的經驗法則，非外部研究結論。

8. **人的角色在改變：監督、拆解、判斷，而且要刻意保留技能與傳承。**
   - 【已查核】Anthropic，〈How AI is transforming work at Anthropic〉，2025-12-02。132 人問卷、53 場訪談、20 萬份對話紀錄：自評在 59% 工作中使用 Claude；自評生產力 +50%；27% 的協助工作原本不會被做；但多數人說只能完全委派 0–20% 的工作；擔心技能退化與師徒互動變少。限制：自評、內部早期使用者、不一定能推廣。

9. **導入要小步、可量測、有基準：先選小群體試點，建立基準再擴大。**
   - 【已查核】Claude Code costs 文件："start with a small pilot group and use the tracking tools below to establish a baseline before wider rollout."
   - 【已查核】DORA 七項能力中的「小批量工作」與「紮實的版本控制」。

### 比喻與經驗法則

- **「AI 是擴音器，不是調音師」**：好的流程被放大，亂的流程也被放大（DORA）。
- **「感覺快 20%，量出來慢 19%」**——但一年後結論變了；所以**要自己量，而且要重量**（METR 兩份研究）。
- **「水管變粗，瓶頸往下游移」**：產出 +98%，審查時間 +91%（Faros）。
- **「差一點就對，最花時間」**（Stack Overflow 66%）。

### 近期案例

- **METR 研究的翻轉（2025-07 → 2026-02）**【已查核】：正反兩面都在同一機構的公開更新裡，最適合講「證據會過期」。
- **Faros AI 生產力悖論（2025-07）**【已查核】：產出變多但公司指標沒動。
- **Anthropic 內部研究（2025-12）**【已查核】：高度採用的組織也只能完全委派一小部分工作，並出現技能與傳承的擔憂。
- **Spotify／Stripe**（見第三、四場）【已查核】：成功案例的共同點是平台化的驗證、隔離環境與人審，不是「換一個更聰明的模型」。

---

## 2026-10 補充（查核日 2026-10-21，皆以 WebFetch 開啟原文）

- 【已查核】Addy Osmani、Morgan Westlee Lunt、Qing Wang，〈How the Claude Code team does code review〉，claude.dev，2026-10-15，https://claude.dev/blog/solving-code-review-at-anthropic/ 。依變更風險分級：低風險在自動審查與安全檢查通過後不需人核准、一般一人、最高風險兩人。引文："A docs fix and an auto-updater change carry different risk, so they get different review." 用在第四場「關卡要設在哪裡？」。限制：廠商自家做法。
- 【已查核】Anthropic Engineering，〈Redesigning source control at Anthropic〉，2026-10-13，https://www.anthropic.com/engineering/redesigning-source-control 。每天合併的變更 2026-05 約 2,500 次、9 月超過 30,000 次。引文："The bottleneck, now, is all of the developer infrastructure built for human scale: source control, builds, and CI." 用在第五場「水管變粗，瓶頸移到審查」。限制：廠商自家案例。
- 【已查核】Addy Osmani，〈Brownfield Agentic Engineering〉，2026-09-14，https://addyosmani.com/blog/brownfield-agentic-engineering/ 。引文："Lock today’s behavior before you let anything improve it." 另："Write down what the code can’t say, and nothing else." 用在第三場「修 Bug：先讓測試紅，再讓它綠」。
- 【已查核】Ryan Donovan，〈The results of the 2026 Developer Survey are here!〉，Stack Overflow Blog，2026-10-06，https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/ 。用 AI 的開發者 66% 用 Coding Agent；用助手或 Agent 的人 73% 天天用；20% 用在部署、維運或排查正式系統；93% 認為要附來源才信任。用在第五場「最花時間的是『差一點就對』」，並更新第一場 2025 年 31% 的說法。
- 尚未發布（2026-10-21 查）：Thoughtworks Technology Radar Vol. 35、DORA 2026 年度報告。11 月再查。

## 不要宣稱的說法（流行但沒有根據或已過時）

1. **「AI 讓開發者慢 19%」當成現況。** METR 自己已標示過時，2026 年更新顯示可能有加速但證據很弱。要講就兩份一起講。
2. **「AI 讓開發者快 55%」或其他單一數字當成通則。** 這類數字多來自特定任務或早期實驗（例如 GitHub 2022 年的受控實驗【本次未查核】），不能推到所有工作。
3. **「AI 能力每 7 個月翻倍」當成現行數據。** METR 2025-03 原文已加註部分圖表與翻倍時間過時，且 METR 不再更新該估計。
4. **「Agent 寫了公司 X% 的程式碼」**（各大公司執行長的說法）。定義不一（補全、建議、PR？），本次未找到可查核的方法說明，不要引用。
5. **「90% 開發者用 AI」等於「90% 使用 Agent」。** DORA 90% 是「在工作中使用 AI」；Stack Overflow 2025 年 Agent 約 31%；2026 年調查中，用 AI 的開發者有 66% 用 Coding Agent，但只有 20% 用在部署或維運正式系統。
6. **「規則檔寫了就會被遵守」。** 官方文件明說規則檔是脈絡而非強制設定；一定要發生的事要做成 hook、CI 或權限。
7. **「Context window 越大越好，全部丟進去就好」。** Anthropic 稱 context rot 在所有模型都會發生。
8. **「調高推論強度就能救回品質」。** OpenAI 文件明說它是微調旋鈕，不是主要的補救方法。
9. **「Spec-driven development 是業界標準」。** Thoughtworks 把 Spec Kit、OpenSpec 放在 Assess；Böckeler 指出審查負擔與 Agent 不照規格做的問題。
10. **「AI 寫的程式碼品質跟人一樣／更好」或「AI 程式碼一定比較爛」。** 現有數據（CodeRabbit）樣本小、由廠商發布；DORA 顯示對穩定度仍為負相關。只能說「要另外量品質」。
11. **「Prompt engineering 已死」。** 只是術語轉向 context engineering；寫清楚的提示詞仍是基本功。
12. **Stripe「每週 1,300 個 PR」、Spotify「10 天 1,000 個 PR」、Amazon Q「96 萬次安裝」、Replit「捏造 4,000 筆資料」。** 只見於二手報導，本次未從原始來源確認。要用就用已查核的數字（Stripe「每週超過一千個」、Spotify「超過 1,500 個」）。

## 查核統計

- **已查核（開啟原始頁面確認）：50 個來源**。Anthropic 工程部落格與研究 9 篇、Claude／Claude Code 文件 4 頁、OpenAI 文件 2 頁、GitHub 文件與部落格 4 頁、Google（DORA 部落格 2 篇、Gemini CLI 文件）3 頁、dora.dev 2 頁、METR 3 篇、Thoughtworks Radar、martinfowler.com 2 篇、Kiro 文件、AGENTS.md 官網、agentskills.io、OWASP 2 頁、Simon Willison 4 篇、Addy Osmani、Stack Overflow 調查、Spotify、Stripe、Airbnb、CodeRabbit、Faros AI、Fortune、AWS 安全公告、arXiv 論文、Cucumber 文件。
- **部分查核：3 項**。Airbnb（內容已查，發布日期未顯示）、OWASP Agentic Top 10（發布日已查，ASI 各項名稱未查）、Spotify（部落格數字已查，QCon 數字未查）。
- **未查核：7 項**，均已在文中與「不要宣稱」清單標示：Stripe 每週 1,300 個、Spotify 10 天 1,000 個、Amazon Q 安裝數、Replit 4,000 筆假資料、OWASP ASI 各項名稱、GitHub 2022 年 55% 研究、Anthropic「How Anthropic teams use Claude Code」PDF（無法讀取內容）。
