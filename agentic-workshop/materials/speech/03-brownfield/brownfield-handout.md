# Brownfield：讓 Agent 當隊友，一起接手既有系統

> 讀者：學員。時機：Brownfield（已有程式碼的既有專案）實作後的 45 分鐘講解。前置：做過個人分析、共同脈絡、B1 與 B2。

這份講義整理技巧與人要判斷的事，不含任務解答。指令是示範用；沒有實際執行的結果一律視為未驗證。

**這一段帶走什麼**

- 接手舊系統：先問問題，結論要附出處
- 答不好時先補需求與脈絡，最後才調模型與推論強度
- 團隊規則進版本控制、邊界分三層、重複做法寫成 Skill
- 修 Bug 先讓測試紅再綠；比較方案先看能不能還原
- 程式能跑還不夠，人要說得出改了什麼、為什麼

## 1. Agent 當隊友：人改成核准計畫

Brownfield（已有程式碼的既有專案）／Teammate（隊友）：Agent 先一起分析，人核准計畫後才動手。

Tool：人逐步下指令 → Teammate：人核准計畫 → Digital Worker（數位員工）：下一場

- **剛才做過的**：分析舊系統、寫共同脈絡、B1 修 Bug、B2 改規則。

- **今天補上的**：讀舊系統、模型與強度、規則與 Skill、測試先行、比較方案、認知債。

Teammate 和 Tool 的差別，是人不再逐步下指令：Agent 先和你一起分析、比較，你核准計畫後它才動手，中途不必每一步都等你。人省下的時間，要花在計畫和證據的判斷上。

這份講義不含任何任務的解答，只整理技巧和人要判斷的事。讀的時候想著剛才四段裡你最不放心交給 Agent 的那一段，最後一頁會回來對照。

**人工確認**：剛才四段裡，哪一段你最不放心交給 Agent？

## 2. 把 Agent 當成資深同事來問

接手陌生程式，最快的入門方式是問問題，而不是叫 Agent 直接改。

- **問運作方式**：「下訂單時，資料經過哪幾個地方？」

- **問規則在哪**：「這條優惠規則寫在哪個檔？哪個測試在檢查它？」

- **問為什麼**：「為什麼這裡要這樣做？有文件或紀錄說明嗎？」

### 交給 Agent 的指令

先不要修改程式。我剛接手這個專案，請像資深同事帶新人一樣回答：訂票從收到請求到存檔，經過哪幾個部分？每一步標出檔案位置，說不出依據的標「推測」，最後列出你讀了哪些檔，然後停下。

Claude Code 官方文件建議：問 Agent 你會問資深工程師的問題，並說這是很有效的入職方式。你不讀程式也能這樣做，因為問的是業務流程和規則在哪，不是語法。Michael Feathers 在《Working Effectively with Legacy Code》談的也是同一件事：沒有測試保護的舊程式，要先理解，再小步修改。

問的時候要求兩件事：每一步標出檔案位置，說不出依據的標「推測」。這樣你拿到的不是一篇通順的說明，而是一張能追查的地圖。下週接手陌生專案，第一天就先問「資料從進來到存檔經過哪些地方」。

📖 延伸閱讀：〈Best practices for Claude Code〉（Anthropic，官方文件）

**人工確認**：回答裡每一步都有檔案位置；標「推測」的地方，你知道下一步要問誰。

## 3. 沒有出處的結論，一律當假設

Agent 讀舊程式時，會很自然地把空白處「補」成合理的故事。

- **事實**：附檔案位置、測試名稱或實際執行的結果。

- **假設**：說得出理由，但還缺證據。

- **缺口**：查不到，要問人。

語言模型很擅長寫出通順、可信的說明；舊系統又常有文件和程式不一致的地方。兩者加在一起，最容易產生「聽起來對」的錯誤結論。所以分析結果要分三類：事實（附檔案位置、測試名稱或執行結果）、假設（有理由但缺證據）、缺口（查不到，要問人）。

人不需要讀懂全部，只要抽一條「事實」追問出處；拿不出證據的，就改標假設。經驗法則：一份分析如果沒有任何一條標假設或缺口，反而要更小心。

**人工確認**：挑一條「事實」追問出處；拿不出證據的，有沒有改標為假設？

## 4. 案例：Spotify 的背景 Coding Agent

Spotify 讓 Agent 在背景做大量程式遷移，公開了成果，也公開了限制（2025 年）。

- **成果**：合併超過 1,500 個變更；遷移類工作省下 60–90% 時間。

- **為什麼用 Agent**：舊的自動化腳本太難維護，一個依賴更新腳本超過兩萬行。

- **沒有省掉的**：Agent 改完照樣跑格式、檢查與 AI 審查，最後由人審核合併。

Spotify 工程部落格（2025-11）公開了背景 Coding Agent「Honk」的經驗：合併超過 1,500 個 PR（Pull Request：請人審查後才合併的一組程式變更），遷移類工作省下 60–90% 時間。改用 Agent 的原因是舊的自動化腳本太難維護，一個依賴更新腳本就超過兩萬行。

沒有被省掉的是檢查：Agent 改完照樣跑格式化、程式檢查和 AI 審查，最後由人審核合併。作者也坦言，Agent 的輸出比舊腳本難預測，他們「還沒有全部答案」。網路上流傳的「10 天合併 1,000 個」只見於二手報導，不要引用。

📖 延伸閱讀：〈1,500+ PRs Later: Spotify's Journey with Our Background Coding Agent (Honk, Part 1)〉（Spotify Engineering，2025）

**人工確認**：這個案例裡，哪一個環節仍然由人負責？

## 5. 模型選擇：按工作分工，不是一律最強

同一個任務裡，不同步驟適合不同大小的模型。

- **量大、明確**：照計畫改格式、批次小修改：較小、較快的模型。

- **難、要判斷**：審查、訂規則、找風險、架構取捨：較強的模型。

- **先用預設**：名稱與價格每幾個月就變；記原則，不記型號。

同一件任務裡，不同步驟適合不同的模型。Anthropic 的大型遷移文章（2026-07）就是這樣分工：用較小的模型做大量實作，用最強的模型做審查與寫規則。Claude Code 官方〈Manage costs effectively〉也建議把最強的模型留給複雜的架構決策或多步推理。這是廠商自家的做法，但原則很通用。

這裡刻意不寫模型名稱或價格，因為每幾個月就變；記原則就好：先用預設，量大明確的工作往小調，要判斷的工作往大調。工具沒有模型選單也沒關係，同樣的原則也適用在分配工作給不同的工具或不同的人。

📖 延伸閱讀：〈Choosing the right model〉（Anthropic，官方文件）；〈Manage costs effectively〉（Anthropic，官方文件）；〈How Anthropic runs large-scale code migrations with Claude Code〉（Anthropic，2026）

**人工確認**：說出你工作中一件「量大、明確」和一件「要判斷」的事。

## 6. 推論強度是微調旋鈕，不是救命按鈕

Reasoning Effort（推論強度）：同一個模型回答前「想多深」。越深越慢，也越耗 Token。

- **先用預設**：有證據顯示不夠，才調高；兩家主要廠商說法一致。

- **簡單量大就調低**：例如整理格式、跑既定步驟。

- **調高救不了模糊**：需求不清、脈絡不足，想再久也是猜。

兩家主要廠商的說法一致。OpenAI〈Reasoning models〉：推論強度是微調旋鈕，不是救回品質的主要方法；很高的檔位（例如 xhigh）只在你的評測顯示有明顯好處時才用。Anthropic〈Effort〉：強度是給模型的行為訊號，不是嚴格的 Token 預算；低強度適合簡單、重視速度的工作，例如子 Agent，並建議用自己的評測決定。

常見的誤解是「調高推論強度就能救回品質」。需求不清、脈絡不足時，想再久也是猜。工具沒有這項設定時，可以在提示詞寫「先仔細想過再回答」，但不要期待它補上缺的資訊。

📖 延伸閱讀：〈Reasoning models〉（OpenAI，官方文件）；〈Effort〉（Anthropic，官方文件）

**人工確認**：上次 Agent 答得不好，問題出在「想不夠深」，還是「資訊不夠」？

## 7. 答得不好時，先查這四樣

換更強的模型或調高強度，應該是最後一步，不是第一步。

目標說清楚了嗎 → 給對檔案了嗎 → 有可執行的檢查嗎 → 最後才調模型與強度

### 交給 Agent 的指令

先不要修改。回答前請先告訴我：要把這件事做對，你還缺哪些資訊或檔案？哪些地方你只能用猜的？列完就停下，等我補齊再開始。

答得不好時，最常見的原因不是模型不夠強，而是前三項沒做好：目標沒說清楚（交辦式提示詞）、沒給對檔案（脈絡）、沒有能自己跑的檢查。這三項第一場都教過，這裡把它們排在「換模型、調強度」之前。

讓 Agent 先列出它缺什麼、哪裡只能用猜的，比讓它直接作答更容易發現需求不清。下次 Agent 答得不好，先貼上方的提示詞，補完它列的缺口再重問，比較前後差別。

**人工確認**：Agent 列出的缺口，你補了幾項？補完後答案有沒有變好？

## 8. 團隊規則：進版本控制，大家一起維護

每個人各寫各的提示詞，Agent 就有幾種做事方式；共用一份規則，行為才一致。

- **進版本控制**：改規則也像改程式：有人提、有人審、留紀錄。

- **好規則涵蓋六件事**：怎麼執行、怎麼測試、專案結構、程式風格、版本控制習慣、邊界。

- **最常見的有用限制**：「絕對不要提交密碼與金鑰」。

每個人各寫各的提示詞，同一個 Agent 就會有好幾種做事方式。共用一份規則並放進版本控制，改規則就像改程式：有人提、有人審、留下紀錄。Thoughtworks 技術雷達第 34 期把團隊共同維護的規則列為建議採用；剛才共同脈絡段在 AGENTS.md 加上「開工先讀」與審查準則，就是這個做法。

GitHub 部落格（2025-11）分析兩千五百多個開源專案的規則檔，歸納出好規則涵蓋六件事：怎麼執行、怎麼測試、專案結構、程式風格、版本控制習慣、邊界；最常見的有用限制是「絕對不要提交密碼與金鑰」。第二場說規則檔要短，這裡說要共用、有人維護，兩者要一起做到。

什麼時候該加一行？Claude Code 官方文件的建議是：Agent 同一個錯犯第二次，或審查抓到它本來就該知道的事。B1 檢查點 3 的補充就是這一步：請 Agent 把那條更正寫進 AGENTS.md。

📖 延伸閱讀：〈How to write a great agents.md: Lessons from over 2,500 repositories〉（GitHub，2025）；〈How Claude remembers your project〉（Anthropic，官方文件）

**人工確認**：你團隊的規則裡，六件事缺了哪一件？

## 9. 邊界寫成三層：一定做、先問、絕不做

只寫「要小心」沒有用；把邊界分三層，Agent 和人都知道何時該停。

```text
## 一定做
  修改後執行全部測試，回報通過／失敗／跳過數
## 先問我
  更新既有測試的期待值、增加新套件
## 絕不做
  提交密碼或金鑰、刪除測試、直接改正式環境
```

### 交給 Agent 的指令

先不要修改檔案。請讀我們的規則檔，把每條規則歸到「一定做／先問我／絕不做」三層；分不進去或互相矛盾的單獨列出。用表格回報，然後停下等我決定。

三層邊界（一定做、先問、絕不做）出自同一份 GitHub 規則檔研究。只寫「要小心」沒有用，因為 Agent 和人都判斷不出何時該停；分成三層後，「先問我」那一層就是你真正想親自決定的事。範例內容是通用示意，不是工作坊的答案。

要記得規則檔是脈絡，不保證照做。「絕不做」那一層最好再用權限或自動檢查擋住，例如推送前自動掃描金鑰；這在下一場加深。

📖 延伸閱讀：〈How to write a great agents.md: Lessons from over 2,500 repositories〉（GitHub，2025）

**人工確認**：「先問我」那一層，是不是剛好列出你真正想親自決定的事？

## 10. Skill：需要時才翻開的入職手冊

Skill（技能檔）：一個資料夾，SKILL.md 開頭寫 name 與 description；任務符合時 Agent 才讀全文。

- **AGENTS.md**：每次對話都整份讀進來，所以要短。

- **Skill**：平常只看 name 與 description，用到才讀全文，可以寫得完整。

- **開放格式**：多數主流 Coding Agent 都支援同一種格式；技術雷達列為試用。

AGENTS.md 每次對話都整份讀進來，所以要短；Skill 是一個資料夾，裡面的 SKILL.md 開頭寫 name（名稱）與 description（做什麼、什麼時候用），工具平常只讀這兩項，任務符合才讀全文，這叫逐步揭露，所以可以寫得完整。Anthropic（2025-10）的比喻是：替 Agent 做 Skill，就像替新同事整理入職手冊。分法很簡單：每次都要遵守的放 AGENTS.md，多步驟的固定做法放 Skill，例如今天的 check 與 fix-bug-with-test。

Skill 已是開放格式：agentskills.io 列出 Claude Code、Codex、GitHub Copilot、Gemini CLI、Cursor 等工具都支援；Thoughtworks 技術雷達第 34 期把它列為「試用」（Trial）。工作坊用的就是這個標準格式：Agent 把 SKILL.md 放在它的工具會自動載入專案 Skill 的位置，例如 Claude Code 是專案的 .claude/skills/，Codex 是 .agents/skills/；也可以直接叫名稱使用。

常見誤解是「Skill 寫了，Agent 就一定會用」。工具是靠 description 判斷何時該讀，所以這句要同時寫出它做什麼、什麼時候用；寫得含糊就不會被選中。Claude Code 成本文件也建議，把只有某類工作才用的指示從規則檔搬到 Skill：用到才載入，平常不佔每次對話的 Token。

📖 延伸閱讀：〈Agent Skills Overview〉（agentskills.io）；〈Extend Claude with skills〉（Anthropic，官方文件）；〈Build skills〉（OpenAI，官方文件）；〈Equipping agents for the real world with Agent Skills〉（Anthropic，2025）

**人工確認**：你的一條做法，該放 AGENTS.md（每次都要）還是 Skill（某類任務才要）？

## 11. 怎麼寫 Skill：從真實工作長出來

先不用 Skill 做完一次，留意你一直重複交代什麼，再請 Agent 寫成 Skill。

- **description 寫兩件事**：第三人稱：做什麼＋什麼時候用，放進使用者會說的字。

- **只寫 Agent 不知道的**：你們的步驟和要交的證據；不寫這一次的答案。

- **只裝信任的來源**：Skill 能叫 Agent 做事；別人的 Skill 要先讀過再用。

### 交給 Agent 的指令

先不要修改程式。請把我們剛才完成的做法整理成一份 Skill 草稿：name 用小寫英文加連字號、和資料夾同名；description 用第三人稱寫它做什麼、什麼時候用，放進我們平常會說的字；內文只寫步驟、每步要交的證據、回報格式，你本來就懂的不用解釋，也不寫這次問題的具體原因。寫好給我看，等我核准再存檔。

Anthropic〈Skill authoring best practices〉的做法：先不用 Skill 完成一次任務，留意自己一直重複提供的背景或步驟；把這個可重用的做法交給 Agent 寫成 Skill；再審一遍，刪掉 Agent 本來就懂的（官方的說法是只補它還不知道的脈絡）；最後在新對話拿類似的任務測，依觀察改。官方也說，不需要特別的系統提示詞或「寫 Skill 的 Skill」，直接請 Agent 幫忙就好。

description 最關鍵：工具靠它決定什麼時候用。官方建議同時寫做什麼和什麼時候用、一律用第三人稱、放進具體的關鍵字；「幫忙處理文件」這種含糊說法不會被選中。name 用小寫英文、數字和連字號，64 字以內，和資料夾同名（agentskills.io〈Specification〉）。最常見的錯誤是把這一次的具體原因寫進去，下次遇到不同問題反而把 Agent 帶偏。

安全提醒：Skill 能叫 Agent 做事，Anthropic 建議只從信任的來源安裝，別人的 Skill 要先讀過再用。下週想一件每次都要跟新人講一次的事，那就是你的第一個 Skill 候選。

📖 延伸閱讀：〈Skill authoring best practices〉（Anthropic，官方文件）；〈Specification〉（agentskills.io）；〈Equipping agents for the real world with Agent Skills〉（Anthropic，2025）

**人工確認**：description 看得出做什麼、什麼時候用嗎？草稿裡有沒有混進這一次的答案？

## 12. 修 Bug：先讓測試紅，再讓它綠

先寫一個會失敗的測試把問題重現出來，再修，最後看同一個測試變成通過。

重現：測試失敗（紅） → 修正根本原因 → 同一測試通過（綠） → 其他測試沒變壞

- **為什麼你能信**：修前失敗、修後通過，是不讀程式也看得懂的證據。

- **修根本原因**：不是把錯誤訊息藏起來，也不是改測試配合錯的結果。

### 交給 Agent 的指令

先不要修改測試以外的程式。請先寫一個會失敗的測試，重現這個問題，執行並貼出失敗摘要。然後提出修正根本原因的計畫，最多 3 步，等我核准。

Claude Code 官方文件的範例提示詞就是這個順序：先寫一個會失敗的測試重現問題，再修；而且要修根本原因，不要把錯誤壓下去。修前失敗、修後通過，是你不讀程式也看得懂的證據。

Simon Willison（2025-12）補了一個檢查法：把修正拿掉時，這個測試應該要失敗；不會失敗的測試證明不了什麼。舊系統還要多一步：Addy Osmani〈Brownfield Agentic Engineering〉（2026-09）的第一條建議是，先用測試把今天的行為鎖住，再讓任何東西去改進它。

下週修 Bug 前先問：有沒有一個測試能當裁判？沒有，就從請 Agent 寫第一個會失敗的測試開始。

「紅、綠」來自 Kent Beck 推廣的測試驅動開發（TDD）。Martin Fowler 的說明（2023）是三步：先為下一小段功能寫測試，再寫程式直到測試通過，最後整理新舊程式，常簡稱「紅、綠、重構」。修 Bug 時的紅燈，是把回報的問題重現成一個會失敗的測試；要確認它是因為這個 Bug 而失敗，不是測試本身寫錯。Michael Feathers 在《Working Effectively with Legacy Code》另外提出特性測試（characterization test）：先記錄舊程式「現在實際怎麼做」，不判斷對錯，改的時候才知道有沒有不小心改到別的行為。

📖 延伸閱讀：〈Best practices for Claude Code〉（Anthropic，官方文件）；〈Brownfield Agentic Engineering〉（Addy Osmani，2026）；〈Your job is to deliver code you have proven to work〉（Simon Willison，2025）；〈TestDrivenDevelopment〉（Martin Fowler，2023）

**人工確認**：你看到的是同一個測試的前後對照，而不是 Agent 說「修好了」。

## 13. 事前給地圖，事後裝感測器

讓 Agent 做對有兩種方法：動手前引導它，動手後自動檢查它。

- **事前引導**：規則檔、Skill、計畫：告訴它該怎麼做。

- **事後感測**：測試、格式檢查、型別檢查：做完立刻知道對不對。

- **優先用算得出來的**：測試快又穩定；請 AI 審查較慢、較貴，結果也不固定。

Birgitta Böckeler〈Harness engineering for coding agent users〉（martinfowler.com，2026-04）把讓 Agent 做對的方法分成兩類：事前引導（規則檔、Skill、計畫）在它動手前影響它；事後感測（測試、格式檢查、型別檢查）在它動手後讓它自己修正。她用自動調速器比喻：兩者搭配才穩。

她也區分兩種檢查：測試、格式檢查這類算得出來的檢查，快而且結果固定；請 AI 審查這類推論型的檢查，較慢、較貴，結果也不固定。所以優先用算得出來的，AI 審查當補充。下週找一條你團隊只靠「提醒」的規則，問它能不能變成一個自動檢查。

📖 延伸閱讀：〈Harness engineering for coding agent users〉（martinfowler.com，2026）

**人工確認**：你的團隊做法裡，哪一條只有「事前提醒」，還沒有「事後檢查」？

## 14. 比較方案：先唯讀研究，再由人選

有不只一種做法時，請 Agent 不動檔案、先研究，用同一組欄位列出 2–3 個方案。

```text
| 方案 | 改動範圍 | 風險 | 可逆性 | 未確認的假設 |
|------|----------|------|--------|--------------|
| A    | 附檔案或測試名稱 | … | 容易還原？ | … |
| B    | …        | …    | …      | …            |
```

### 交給 Agent 的指令

先不要修改任何檔案。請提出 2–3 個真的可行的方案，用表格比較：改動範圍（附檔案或測試名稱）、風險、可逆性、未確認的假設。最後寫你的建議與理由，然後停下等我選。

有不只一種做法時，讓 Agent 先唯讀研究、用同一組欄位列出方案，你才能公平比較，也看得出哪個方案只是陪襯。Anthropic〈Our framework for developing safe and trustworthy agents〉（2025-08）的原則是：尤其在高風險決定前，人要保有控制權；文中以當時的 Claude Code 為例，預設唯讀，改動前要人核准。工具的預設會隨版本改變（2026 年的 Claude Code 在多數互動情境，預設改由另一個模型先審查動作），所以不要依賴預設：比較方案這一步，在提示詞寫明「先不要修改任何檔案」。

這裡比 B2 多一欄「可逆性」，因為它直接決定你可以多快做決定（下一頁）。表格只是格式示意，不代表任何一組的方案。

📖 延伸閱讀：〈Our framework for developing safe and trustworthy agents〉（Anthropic，2025）；〈Structured outputs〉（Anthropic，官方文件）

**人工確認**：每個方案都填滿同一組欄位；有沒有方案只是陪襯？

## 15. 人怎麼選：先看能不能還原

選方案不用讀程式，問兩個問題就夠。

- **能輕易還原嗎**：能：選一個先做小步試。不能：要更多證據再決定。

- **哪個假設最危險**：「哪個未確認的假設錯了，會改變選擇？」先驗證它。

- **Agent 的建議只是一票**：它不知道的業務限制，只有你知道。

經驗法則：可還原的決定可以快，選一個先小步試；難還原的決定要慢，先要更多證據，例如刪資料、改正式環境、改對外介面。另一個問題是：哪個未確認的假設一旦錯了，會改變你的選擇？先驗證那一個。

Agent 的建議常偏向它看得到的程式面理由；業務、客戶、時程的考量它不知道，只有你能補上。所以它的建議只是一票，最後你要說得出是根據哪一欄做決定。

**人工確認**：你這次的選擇，說得出是根據哪個欄位決定的嗎？

## 16. 警示：程式能跑，但沒有人懂

Cognitive Debt（認知債）：Agent 改得越快，團隊真正理解的部分可能越少。

- **業界警示**：技術雷達把「程式碼的認知債」列為警示。

- **監督的悖論**：監督 AI 需要的能力，正是少寫程式後最容易退化的能力。

- **人能說出為什麼**：每個核准的變更，你能用一句話說出改了什麼、為什麼。

### 交給 Agent 的指令

請用三句白話向一位新同事說明這次的變更：改了什麼行為、為什麼要改、用什麼證據確認沒改壞。不要貼程式，然後停下。

Thoughtworks 技術雷達第 34 期（2026-04）把「程式碼的認知債」列為警示：程式能跑，但團隊裡沒有人真正懂。Anthropic〈How AI is transforming work at Anthropic〉（2025-12）訪問自家工程師，提到「監督的悖論」：監督 AI 需要的能力，正是少寫程式後最容易退化的能力。

這不是叫大家少用 Agent，而是把「理解」也當成交付的一部分：每個核准的變更，你要能用一句話說出改了什麼、為什麼，決定和原因寫進 notes/。下週可以請 Agent 用三句白話向新同事解釋一次變更，看不懂的那句，就是要追問的地方。

📖 延伸閱讀：〈Technology Radar Vol. 34〉（Thoughtworks，2026）；〈How AI is transforming work at Anthropic〉（Anthropic，2025）

**人工確認**：這三句你自己看得懂嗎？看不懂的那句，就是要追問的地方。

## 17. 人判斷的四件事

Agent 負責讀、跑、寫；人負責判斷。這就是 Teammate 的分工。

- **證據**：這個「事實」有出處嗎？是實際執行看到的嗎？

- **範圍**：計畫夠小嗎？寫了不改什麼嗎？

- **選擇**：能還原嗎？哪個假設最危險？

- **理解**：我說得出改了什麼、為什麼嗎？

四件事對應今天的四段：證據（讀舊系統）、範圍（測試先行與計畫）、選擇（比較方案）、理解（認知債）。Agent 負責讀、跑、寫，人負責這四個判斷，這就是 Teammate 的分工。

某一段不放心交出去，通常是那一步沒有證據可看。解法是要求 Agent 拿出證據，而不是自己去讀程式。

**人工確認**：回到開場：你最不放心的那段，缺的是四件事裡的哪一件？

## 18. 下一場：你沒辦法盯每一段

任務再大一點，人就得先寫清楚範圍，只在幾個關鍵點做決定。

Tool：逐步下指令 → Teammate：核准計畫 → Digital Worker：只在關鍵點決定

- **帶到下一場**：團隊規則、修 Bug 的 Skill、共同脈絡紀錄。

- **想一想**：如果不能盯每一小段，你會先寫清楚哪些事，才敢讓 Agent 自己往前走？

**人工確認**：離場前寫下一條你團隊值得寫成 Skill 的做法。

## 完成條件
說得出 Teammate 的介入方式（核准計畫，不盯每一步）；知道答不好時先補需求與脈絡、最後才調模型與推論強度；能分辨規則檔與 Skill，並為自己的工作寫下一條三層邊界規則，以及一個「先讓測試紅再綠」或「先比較再選」的做法。

**下週可以做的事**

- 接手陌生程式時，先請 Agent 說明資料流程，並標出哪些是「推測」
- 把團隊規則歸成「一定做／先問我／絕不做」三層
- 修下一個 Bug 前，先請 Agent 寫一個會失敗的測試

## 名詞解釋
| 名詞 | 意思 | 出處 |
|---|---|---|
| Brownfield／Greenfield | Brownfield 是已有程式碼的既有專案，要先讀懂、先鎖住現有行為再改；Greenfield 是從頭開始的新專案。 | Addy Osmani〈Brownfield Agentic Engineering〉 |
| Teammate（隊友） | Agent 先和你一起分析、比較，你核准計畫後它才動手，中途不必每一步都等你。 | 本課程〈歡迎與使用方式〉 |
| 模型選擇 | 量大、明確的工作用較小較快的模型，要判斷的工作用較強的模型；先用預設，有證據再換。 | Anthropic〈Choosing the right model〉 |
| 推論強度（Reasoning Effort） | 同一個模型回答時投入多少思考、花多少 Token；越高越慢越貴，是微調旋鈕，補不了需求不清。 | Anthropic〈Effort〉；OpenAI〈Reasoning models〉 |
| Skill（技能檔） | 一個資料夾，裡面的 SKILL.md 開頭寫 name（名稱，和資料夾同名）與 description（做什麼、什麼時候用），內文寫一套做法；工具平常只讀這兩項，任務符合才讀全文。 | agentskills.io〈Agent Skills Overview〉；agentskills.io〈Specification〉 |
| description 與觸發（trigger） | description 用第三人稱寫 Skill 做什麼、什麼時候用，放進使用者會說的字；工具拿你的話和它比對，符合就自己用上，叫觸發。沒觸發先改 description。 | Anthropic 官方文件〈Skill authoring best practices〉；Anthropic Academy〈Introduction to agent skills〉 |
| 三層邊界 | 規則分成一定做、先問我、絕不做；「先問我」那層就是人要親自決定的事。 | GitHub〈How to write a great agents.md: Lessons from over 2,500 repositories〉 |
| 測試驅動開發（TDD） | 先為下一小段功能寫測試，再寫程式到測試通過，最後整理程式；常簡稱「紅、綠、重構」。 | Martin Fowler〈TestDrivenDevelopment〉 |
| 重現 Bug 的失敗測試 | 修 Bug 前先寫一個現在會失敗的測試把問題重現出來；修好後同一個測試通過，就是不讀程式也看得懂的證據。 | Claude Code 官方文件〈Best practices for Claude Code〉 |
| 特性測試（characterization test） | 記錄舊程式目前實際行為的測試，不判斷對錯；改程式時用來發現有沒有不小心改到別的行為。 | Michael Feathers《Working Effectively with Legacy Code》；Addy Osmani〈Brownfield Agentic Engineering〉 |
| 事前引導／事後感測 | 規則檔、Skill、計畫在動手前引導 Agent；測試、格式檢查在動手後讓它自己修正。 | martinfowler.com〈Harness engineering for coding agent users〉 |
| PR（Pull Request） | 把一組程式變更提議合併進專案；合併前讓別人討論與審查。 | GitHub 官方文件〈Pull requests〉 |
| 認知債（Cognitive debt） | 程式能跑，但團隊裡沒有人真正懂它怎麼運作；Agent 改得越快越容易累積。 | Thoughtworks〈Technology Radar Vol. 34〉 |

## 延伸閱讀
- 〈Best practices for Claude Code〉（Anthropic，官方文件）
- 〈1,500+ PRs Later: Spotify's Journey with Our Background Coding Agent (Honk, Part 1)〉（Spotify Engineering，2025）
- 〈Choosing the right model〉（Anthropic，官方文件）
- 〈Manage costs effectively〉（Anthropic，官方文件）
- 〈How Anthropic runs large-scale code migrations with Claude Code〉（Anthropic，2026）
- 〈Reasoning models〉（OpenAI，官方文件）
- 〈Effort〉（Anthropic，官方文件）
- 〈How to write a great agents.md: Lessons from over 2,500 repositories〉（GitHub，2025）
- 〈How Claude remembers your project〉（Anthropic，官方文件）
- 〈Agent Skills Overview〉（agentskills.io）
- 〈Extend Claude with skills〉（Anthropic，官方文件）
- 〈Build skills〉（OpenAI，官方文件）
- 〈Equipping agents for the real world with Agent Skills〉（Anthropic，2025）
- 〈Skill authoring best practices〉（Anthropic，官方文件）
- 〈Specification〉（agentskills.io）
- 〈Brownfield Agentic Engineering〉（Addy Osmani，2026）
- 〈Your job is to deliver code you have proven to work〉（Simon Willison，2025）
- 〈TestDrivenDevelopment〉（Martin Fowler，2023）
- 〈Harness engineering for coding agent users〉（martinfowler.com，2026）
- 〈Our framework for developing safe and trustworthy agents〉（Anthropic，2025）
- 〈Structured outputs〉（Anthropic，官方文件）
- 〈Technology Radar Vol. 34〉（Thoughtworks，2026）
- 〈How AI is transforming work at Anthropic〉（Anthropic，2025）
