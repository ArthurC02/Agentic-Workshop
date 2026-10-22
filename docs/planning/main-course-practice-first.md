# 主課程實戰化：AGENTS.md、標準 Skill、像真實工作的提示詞（設計，2026-10-22）

> 狀態（2026-10-22）：已實作，未提交。AGENTS.md 取代 skills/team-rules.md（B0 與兩個 Recovery 包附前任的 AGENTS.md，不附 CLAUDE.md）；check、fix-bug-with-test、b3-work-order、回顧 Skill 改標準格式；每個 ③ 改成「用 check 檢查剛才這一段」；提示詞改成交辦工作（Runbook 提示詞總字數 29,998 → 12,445，最長 1,338 → 822）；Greenfield 的固定決定移到 02 需求文件。三條路徑演練通過（Claude Code 2.1.288 實測：新對話自動讀 AGENTS.md、check Skill 依說明自動用上），發現已修正並重跑發布流程。

> 起因：使用者回饋「參考他的內容，而不是設計。教學要能夠學以致用」「提供給參與者的 Prompt…更符合實際工作狀況，而不是只存在教科書上的格式」「AGENTS.md 這類型和實戰相關的知識，都應該加進去課程中」。
> 原則：學員今天做的，就是明天上班會做的。規則與做法放在工具會自動讀的檔案裡，提示詞只寫這次的事。

## 1. 已查核的事實（2026-10-22，官方文件原文）

| 主題 | 事實 | 出處 |
|---|---|---|
| AGENTS.md（Codex） | 從專案根目錄（通常是 Git 根目錄）往下走到目前資料夾，每層最多一個檔；越靠近目前資料夾的越後面、優先；合計上限預設 32 KiB；建議在規則附近加 `## Code Review Rules` 一節，「describe the behavior to flag and any safe path, and leave formatting and lint checks to CI」 | OpenAI〈AGENTS.md〉learn.chatgpt.com/docs/agent-configuration/agents-md |
| AGENTS.md（Claude Code） | 沒有 CLAUDE.md 時直接讀 AGENTS.md（v2.1.277 起）；兩者都有時只讀 CLAUDE.md，除非 CLAUDE.md 匯入 `@AGENTS.md` 或改設定；子資料夾的 AGENTS.md 在讀到該資料夾的檔案時載入 | Claude Code 官方文件〈How Claude remembers your project〉code.claude.com/docs/en/memory |
| 什麼時候加進規則檔 | 「Claude makes the same mistake a second time」「A code review catches something Claude should have known」「You type the same correction … that you typed last session」；只放每次都要的事實（建置指令、慣例、專案結構）；多步驟流程放 Skill；目標每檔 200 行內 | 同上 |
| 規則檔不是強制 | 「Claude treats them as context, not enforced configuration」；要擋的動作用 hook | 同上 |
| Agent Skills 標準 | 一個資料夾含 `SKILL.md`，至少有 `name` 與 `description`；漸進載入：啟動只讀名稱與描述，任務符合描述才讀全文 | agentskills.io〈Agent Skills Overview〉 |
| Skill 位置與呼叫 | Claude Code：`.claude/skills/<name>/SKILL.md`，自動依 description 載入或 `/name`；自訂指令已併入 Skill。Codex：`.agents/skills`（目前資料夾到 repo 根目錄），自動依 description 或 `$name`／`/skills` | Claude Code〈Extend Claude with skills〉；OpenAI〈Build skills〉learn.chatgpt.com/docs/build-skills |
| 支援 AGENTS.md 的其他工具 | Cursor、GitHub Copilot 據二手來源原生支援；Gemini CLI 說法不一 → 學員頁不列工具清單，只說「多數 Coding Agent 會自動讀；讀不到就說『請先讀 AGENTS.md』」 | 二手（morphllm、deployhq），未查官方 |

## 2. 現況的問題

- 規則檔叫 `skills/team-rules.md`，Agent 不會自動讀，每段提示詞都要寫「請先讀 skills/team-rules.md 並照做」。
- Skill 是 `skills/<名>.md` 一般檔案，不是標準格式，回到工作放進工具裡不會自動觸發。
- 108 段提示詞反覆寫同樣的限制（不要改檔、用白話、停下等我、伺服器連同子程序停止…），單段最長 1,600 字。
- 每個 ③ 是一份不同的「請檢查下列三件事…只回成功／失敗」考卷。
- 提示詞內含答案（1225、常漏的 AC、預先決定的錯誤碼），真實的需求方不會知道。

## 3. 改造

### 3.1 AGENTS.md 取代 skills/team-rules.md

- **Greenfield CP1**：工作規則不再整段貼進對話，而是請 Agent 寫成專案根目錄的 `AGENTS.md`，分「怎麼跑」（測試、伺服器啟停、埠號、Git 身分；Windows／macOS 各一行，Agent 依自己的作業系統用）與「工作規則」。之後開新對話會自動載入。
- **Time Skip**：「開新對話先給規則」改成「開新對話，確認 Agent 讀到了 AGENTS.md」（問它：「這個專案的工作規則是什麼？只引用 AGENTS.md 原文」；讀不到就說「請先讀 AGENTS.md」）。
- **共同脈絡 CP2**：小組共識寫進 `AGENTS.md`：工作規則、審查準則（對應 Codex 文件的 Code Review Rules）、開工先讀 `notes/shared-context.md`。
- **新規則的時機**：「同一個錯第二次」就請 Agent 加一行（官方原文），B1／B2 各練一次。
- Recovery 包與 fallback 區塊一併改成 `AGENTS.md`。`check_*.py`、工作單、範本同步。

### 3.2 Skill 用標準格式

- B1 CP3、B3 工作單、回顧 CP2 的 Skill 改成 `<Skill 資料夾>/<name>/SKILL.md`，開頭 `name`、`description`（寫清楚什麼情況該用）。位置由 Agent 依自己的工具決定（提示詞：「放在你這個工具會自動載入專案 Skill 的位置，告訴我完整路徑」），學員頁不寫工具名稱。
- 回顧 CP2 的試跑改成 playbook 的做法：**換兩種說法下任務，看 Skill 會不會自動被用上**。

### 3.3 提示詞像交辦工作

- 一段提示詞只寫：這次要什麼、為什麼、完成的樣子、素材在哪。限制與回報格式靠 AGENTS.md 與 Skill。
- 答案放回需求文件與任務卡；Agent 發現缺口就列問題附建議答案，學員決定。課程需要固定結果的，寫進文件（例如錯誤碼寫進 02 需求文件），不寫在提示詞。
- 例：B1 CP1（現在 690 字、五步）→「客服回報學生票價算錯，任務卡附在後面。先別改程式：重現給我看、找出原因，再給我最多三步的修正計畫。有證據的事實和推論分開寫。」

### 3.4 一個驗收 Skill 取代 108 份考卷

- 共同脈絡（Greenfield 用 AGENTS.md 一節）建立 `check` Skill：只讀不改；對照計畫與驗收條件、notes 寫的與實際指令結果；列出對不上的；最後一行「成功」或「失敗：原因」。
- 每個 ③ 變成一行：「用 check 檢查剛才這一段」，必要時補一句這段特有的條件。綠／紅便利貼的節奏不變。
- 這就是 playbook 的「只報告、不修改」驗證者，學員帶得回去。

## 4. 不變

分鐘、解鎖碼、表單 id、檢查點標題、四段式 ①②③④、Windows／macOS 都要能跑、學員不讀寫程式也不打指令。

## 5. 風險與驗證

- 自動載入依工具版本：每次開新對話的第一個動作是確認讀到 AGENTS.md，讀不到就用一句話補救。
- 提示詞變短，更依賴 Agent 判斷 → 三條路徑完整演練（Greenfield、Time Skip→回顧、Recovery），計時並比較成功率；任一段比現在慢或不穩，就在那段補回必要的句子。
- course-authoring 的 ③ 規格、`check_blocks.py`、`check_deck_runbook.py` 要跟著改。

## 6. DLC 照做（2026-10-23）

同樣三件事套到 DLC，決定與數字見 decisions-and-open-issues.md「DLC 實戰化」。差別：DLC 的 `AGENTS.md` 是團隊已寫好的（學員接手既有專案），學員在 D1 把自己的名詞與邊界決定加進去；Skill 由學員包提供原稿，開場由 Agent 放到工具會自動載入的位置；兩人共用一台機器，角色寫在 `AGENTS.md`「兩個角色」，新對話第一句只說自己是誰。
