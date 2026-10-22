# DLC 四場講解：DDD 與 Coding Agent 的查證來源

> 讀者：DLC 講解（`agentic-workshop/materials-dlc/speech/`）的講者與教材維護者。用途：充實四場講解的概念頁、講者備註與案例。查證日期：2026-10-16。
> 每個來源都在這一天用 WebFetch 打開原頁（PDF 下載後轉成文字）核對過，引文皆為原文、每段不超過 25 個英文字。標「未查證」的項目只看到二手報導或搜尋摘要，**不要上投影片**。
> 學員頁面只能引用 `.claude/skills/course-authoring/references.md` 列出的標題、不放網址；本文件的新來源要先補進該清單，才能出現在講義或投影片上。本工作坊沒有量測效率，下列案例的數字一律是「對方自己說的」，不能當成本課程的結果。

## 0. 統計

| 類別 | 數量 |
|---|---|
| 已查證來源（原頁打開並核對引文） | 67（S53–S60 於 2026-10-17 補查，見第 9 節；S61–S66 於 2026-10-21 補查，見第 10 節；S67–S70 於 2026-10-22 補查，並重新核對 S01、S07–S11、S16–S18、S20、S56、S59 的術語定義，見第 11 節） |
| 部分查證（頁面存在，但關鍵數字或原文只見於二手來源） | 3（S43 的「900 萬行」、S48 的 FT 原文、S51 的 GitHub 原始檔） |
| 未查證、不得引用的說法 | 8（見第 6 節） |

## 1. 來源總表

狀態：✅ 已查證；◐ 部分查證。日期為頁面標示的發布或更新日期。

| ID | 標題 | 作者／發布者 | 日期 | 網址 | 狀態 |
|---|---|---|---|---|---|
| S01 | Domain-Driven Design Reference: Definitions and Pattern Summaries | Eric Evans／Domain Language（CC BY 4.0） | 2015-03 | https://www.domainlanguage.com/ddd/reference/ | ✅ |
| S02 | UbiquitousLanguage（bliki） | Martin Fowler | 2006-10-31 | https://martinfowler.com/bliki/UbiquitousLanguage.html | ✅ |
| S03 | BoundedContext（bliki） | Martin Fowler | 2014-01-15 | https://martinfowler.com/bliki/BoundedContext.html | ✅ |
| S04 | DDD_Aggregate（bliki） | Martin Fowler | 2013-04-23 | https://martinfowler.com/bliki/DDD_Aggregate.html | ✅ |
| S05 | Domain Event | Martin Fowler | 2005-12-12 | https://martinfowler.com/eaaDev/DomainEvent.html | ✅ |
| S06 | StranglerFigApplication（bliki） | Martin Fowler | 2024-08-22 | https://martinfowler.com/bliki/StranglerFigApplication.html | ✅ |
| S07 | Effective Aggregate Design, Part I | Vaughn Vernon／dddcommunity.org | 2011-10-01 | https://www.dddcommunity.org/library/vernon_2011/ | ✅（PDF） |
| S08 | Documenting Architecture Decisions | Michael Nygard／Cognitect | 2011-11-15 | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | ✅ |
| S09 | Architectural decision record process | AWS Prescriptive Guidance | 頁面無日期 | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html | ✅ |
| S10 | Context Mapping | DDD Crew（GitHub） | 持續更新 | https://github.com/ddd-crew/context-mapping | ✅ |
| S11 | The Bounded Context Canvas | DDD Crew（GitHub，CC BY-SA 4.0） | 持續更新 | https://github.com/ddd-crew/bounded-context-canvas | ✅ |
| S12 | Aggregate Design Canvas | DDD Crew（GitHub） | 持續更新 | https://github.com/ddd-crew/aggregate-design-canvas | ✅ |
| S13 | DDD Starter Modelling Process | DDD Crew（GitHub） | 持續更新 | https://github.com/ddd-crew/ddd-starter-modelling-process | ✅ |
| S14 | Introducing Event Storming | Alberto Brandolini（部落格） | 2013-11-18 | https://ziobrando.blogspot.com/2013/11/introducing-event-storming.html | ✅ |
| S15 | EventStorming（官方網站） | eventstorming.com | 頁面無日期 | https://www.eventstorming.com/ | ✅ |
| S16 | Domain Storytelling Quick Start Guide | domainstorytelling.org（WPS，CC BY 4.0） | 頁面無日期 | https://domainstorytelling.org/quick-start-guide | ✅ |
| S17 | Use Domain Analysis to Model Microservices | Microsoft Azure Architecture Center | 2026-02-23 | https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis | ✅ |
| S18 | Use Tactical DDD to Design Microservices | Microsoft Azure Architecture Center | 2026-02-25 | https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design | ✅ |
| S19 | Anti-Corruption Layer Pattern | Microsoft Azure Architecture Center | 2026-05-28 | https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer | ✅ |
| S20 | Hexagonal Architecture | Alistair Cockburn | 2005-09-04 | https://alistair.cockburn.us/hexagonal-architecture/ | ✅ |
| S21 | The Standard of Code Review | Google Engineering Practices | 頁面無日期 | https://google.github.io/eng-practices/review/reviewer/standard.html | ✅ |
| S22 | Eric Evans Encourages DDD Practitioners to Experiment with LLMs | Thomas Betts／InfoQ | 2024-03-18 | https://www.infoq.com/news/2024/03/Evans-ddd-experiment-llm/ | ✅ |
| S23 | DDD & LLMs（議程摘要） | Eric Evans／DDD Europe 2024 | 2024-05-31 | https://2024.dddeurope.com/program/ddd-and-llms | ✅ |
| S24 | Opening Keynote Eric Evans（議程摘要） | Eric Evans／DDD Europe 2026 | 2026-06（10–12 日之間） | https://2026.dddeurope.com/program/opening-keynote-eric-evans/ | ✅ |
| S25 | Accelerate your Strategic Design with LLMs | Thomas Coopman／DDD Europe 2026 | 2026-06-08～09 | https://2026.dddeurope.com/program/accelerate-your-strategic-design-with-llms/ | ✅ |
| S26 | Can AI be a Co-Domain Expert in Domain Modelling? | Philipp Kostyra／DDD Europe 2026 | 2026-06 | https://2026.dddeurope.com/program/can-ai-be-a-co-domain-expert-in-domain-modelling/ | ✅ |
| S27 | The Curse of Unbounded Contexts: Using Domains as LLM Consumers | Chelsea Troy／DDD Europe 2026 | 2026-06 | https://2026.dddeurope.com/program/the-curse-of-unbounded-contexts-using-domains-as-llm-consumers/ | ✅ |
| S28 | AI-Generated End-to-End API Tests: An Experience Report in Legacy Modernization | Cyrille Martraire、Olivier Penhoat／DDD Europe 2026 | 2026-06 | https://2026.dddeurope.com/program/ai-generated-end-to-end-api-tests-an-experience-report-in-legacy-modernization/ | ✅ |
| S29 | 講者頁：Raj Navakoti（議程 Reverse-Engineering DDD） | DDD Europe 2026 | 2026-06 | https://2026.dddeurope.com/speakers/raj-navakoti | ✅ |
| S30 | Architecture drift reduction with LLMs（Assess） | Thoughtworks Technology Radar Vol. 34 | 2026-04 | https://www.thoughtworks.com/radar/techniques/summary/architecture-drift-reduction-with-llms | ✅ |
| S31 | Feedback sensors for coding agents（Trial）；同頁 Mutation testing | Thoughtworks Technology Radar Vol. 34 | 2026-04 | https://www.thoughtworks.com/radar/techniques/summary/feedback-sensors-for-coding-agents | ✅ |
| S32 | Curated shared instructions for software teams（Adopt） | Thoughtworks Technology Radar Vol. 34 | 2026-04 | https://www.thoughtworks.com/radar/techniques/summary/curated-shared-instructions-for-software-teams | ✅ |
| S33 | Agent instruction bloat（Caution） | Thoughtworks Technology Radar Vol. 34 | 2026-04 | https://www.thoughtworks.com/radar/techniques/summary/agent-instruction-bloat | ✅ |
| S34 | Using GenAI to understand legacy codebases（Adopt） | Thoughtworks Technology Radar | 2025-11（最後一次出現） | https://www.thoughtworks.com/radar/techniques/using-genai-to-understand-legacy-codebases | ✅ |
| S35 | Legacy Modernization meets GenAI | Alessio Ferri、Tom Coggrave、Shodhan Sheth／martinfowler.com | 2024-09-24 | https://martinfowler.com/articles/legacy-modernization-gen-ai.html | ✅ |
| S36 | Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl | Birgitta Böckeler／martinfowler.com | 2025-10-15 | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | ✅ |
| S37 | Context Engineering for Coding Agents | Birgitta Böckeler／martinfowler.com | 2026-02-05 | https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html | ✅ |
| S38 | The role of developer skills in agentic coding | Birgitta Böckeler／martinfowler.com | 2025-03-25 | https://martinfowler.com/articles/exploring-gen-ai/13-role-of-developer-skills.html | ✅ |
| S39 | Effective context engineering for AI agents | Anthropic Engineering | 2025-09-29 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | ✅ |
| S40 | Best practices for Claude Code | Claude Code 官方文件 | 2026-10-16 讀取 | https://code.claude.com/docs/en/best-practices | ✅ |
| S41 | Claude 3.7 Sonnet System Card（第 6 節 Excessive Focus on Passing Tests） | Anthropic | 2025-02 | https://assets.anthropic.com/m/785e231869ea8b3b/original/claude-3-7-sonnet-system-card.pdf | ✅（PDF） |
| S42 | How is Google using AI for internal code migrations? | Nikolov 等人／arXiv 2501.06972 | 2025-01-12 | https://arxiv.org/abs/2501.06972 | ✅ |
| S43 | A team of engineers saved Morgan Stanley more than 280,000 hours this year | Alice Tecotzky／Business Insider（AOL 轉載） | 2025-07-01 | https://www.aol.com/team-engineers-saved-morgan-stanley-094301348.html | ◐ |
| S44 | Modernization of mainframe applications（AWS Transform 使用者指南） | AWS | 2026-10-16 讀取 | https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe.html | ✅ |
| S45 | AWS Transform 上市報導 | Steef-Jan Wiggers／InfoQ | 2025-05-20 | https://www.infoq.com/news/2025/05/aws-transform-ai-legacy-migrate/ | ✅ |
| S46 | How AI helps break the cost barrier to COBOL modernization | Anthropic（claude.com 部落格） | 2026-02-23 | https://claude.com/blog/how-ai-helps-break-cost-barrier-cobol-modernization | ✅ |
| S47 | AI coding tool Replit wiped database, called it a 'catastrophic failure' | Beatrice Nolan／Fortune | 2025-07-23 | https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/ | ✅ |
| S48 | AWS AI coding tool decided to delete and recreate a customer-facing system… | Maximilian Schreiner／The Decoder（轉述 Financial Times） | 2026-02-20 | https://the-decoder.com/aws-ai-coding-tool-decided-to-delete-and-recreate-a-customer-facing-system-causing-13-hour-outage-report-says/ | ◐ |
| S49 | We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs | Joseph Spracklen 等人／USENIX Security 2025 | 2025-08 | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | ✅ |
| S50 | The Model Is Not the Bottleneck: Domain-Driven Design as Agent Infrastructure | Lucas Hendrich／Forte Group | 2026-09-02 | https://www.fortegrp.com/insights/the-model-is-not-the-bottleneck-domain-driven-design-as-agent-infrastructure | ✅（廠商文章） |
| S51 | ubiquitous-language（Agent Skill） | Matt Pocock／skills.sh 目錄 | 2026-03-16 首次收錄 | https://skills.sh/mattpocock/skills/ubiquitous-language | ◐ |
| S52 | Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | METR | 2025-07-10（頁面註明已被 2026-02 更新取代） | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | ✅（只用於「不要說」） |
| S53 | Change Coupling: Visualize Logical Dependencies | CodeScene 文件 | 頁面無日期（2026-10-17 讀取） | https://codescene.io/docs/guides/technical/change-coupling.html | ✅ |
| S54 | Your Code as a Crime Scene, Second Edition | Adam Tornhill／Pragmatic Bookshelf | 2024-02 | https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/ | ✅（書籍頁） |
| S55 | Software Design X-Rays: Fix Technical Debt with Behavioral Code Analysis | Adam Tornhill／Pragmatic Bookshelf | 2018-03 | https://pragprog.com/titles/atevol/software-design-x-rays/ | ✅（書籍頁） |
| S56 | About MADR（MADR 4.0.0） | ADR GitHub organization | 2024-09-17 | https://adr.github.io/madr/ | ✅ |
| S57 | Definition Of Refactoring（bliki） | Martin Fowler | 2004-09-01 | https://martinfowler.com/bliki/DefinitionOfRefactoring.html | ✅ |
| S58 | Demystifying evals for AI agents | Anthropic Engineering | 2026-01-09 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | ✅ |
| S59 | Classification: Accuracy, recall, precision, and related metrics | Google Machine Learning Crash Course | 2026-01-12 更新 | https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall | ✅ |
| S60 | Open Knowledge Format (OKF), Version 0.2 | Google Cloud（knowledge-catalog，GitHub） | 頁面無日期（2026-10-17 讀取） | https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md | ✅ |

## 2. 第 01 場：語言與邊界（開場、D1）

現況：投影片已講「先講好什麼算成功、只能靠人抓的錯、候選、通用語言、Bounded Context、邊界洩漏」，但概念頁幾乎沒有外部出處，也沒有「Agent 從舊程式抽語言」的真實例子。

### 2.1 可教的重點

1. **DDD 的三句話定義。** Evans 自己的摘要只有三點：聚焦核心領域、領域專家與開發者一起探索模型、在明確邊界內說通用語言。適合放在 `start` 頁當地基。
   - S01：「Speak a ubiquitous language within an explicitly bounded context.」
2. **改用語就是改模型。** 這句話支撐「候選要核准」：Agent 換一個名詞，就是提議改模型，不是改錯字。
   - S01：「Recognize that a change in the language is a change to the model.」
   - S02：「the language (and model) should evolve as the team's understanding of the domain grows.」
3. **語言要用在程式裡，不只在圖上。** 通用語言要貫穿對話、文件與程式；Azure 用同一句話描述。
   - S01：「Within a bounded context, use the same language in diagrams, writing, and especially speech.」
   - S17：「Teams use this language consistently in conversations, documentation, and code.」
4. **同名不同義是常態，所以需要 Bounded Context。** Fowler 以 Customer、Product 為例；Azure 以 account 為例。可直接對應 `context` 頁的「同名不同義」。
   - S03：「Time and time again I see this confusion recur with polysemes like "Customer" and "Product".」
   - S17：「the same word (like *account*) has different meanings in different contexts.」
5. **不要追求全公司一套模型。**
   - S03：「total unification of the domain model for a large system will not be feasible or cost-effective」
   - S01：「Model expressions, like any other phrase, only have meaning in context.」
6. **一個 Context 的「一句話」可以用畫布檢查。** Bounded Context Canvas 的 Purpose 欄要求用業務語言寫、不寫技術；另有 Ubiquitous Language、Business Decisions、Assumptions、Open Questions 欄位，正好對應 D1 的「每個寫一句」與「缺口」。
   - S11：「A few sentences describing the why and what of the context in business language. No technical details here.」
7. **邊界洩漏在舊系統最常見，修法是畫清楚邊界。** Azure 提醒外部或舊系統的資料結構會滲進應用程式，建議用 Strangler Fig 或 Anti-Corruption Layer。對應 `leak` 頁。
   - S17：「the external system's data schema or API might leak into the application.」
8. **找語言的工作坊方法有兩個常見選擇：EventStorming、Domain Storytelling。** 只當「延伸」提一句，不必教。EventStorming 用橘色便利貼寫領域事件、按時間排；Domain Storytelling 用「角色—動詞—工作物件」加編號句子講故事。
   - S14：「the convention is to use orange stickies for this purpose.」
   - S16：「The actors' activities are shown as arrows and labeled with verbs from the domain language.」
9. **Agent 讓「從程式抽語言」變便宜，但仍要領域專家驗證。** Thoughtworks 把「用生成式 AI 理解舊程式」列為 Adopt；Evans 2026 年主題演講提到用 LLM 加確定性計算從程式抽出領域詞彙。
   - S34：Tools help developers「surface business rules, summarize logic and identify dependencies.」
   - S24：「uses LLM components and deterministic calculations to extract domain-relative vocabulary from code」
10. **Agent 是通用語言的第二位讀者。** 它沒有走廊對話，也不知道三個舊名稱裡團隊選了哪個；所以詞彙表要寫「不用哪些同義詞」。（廠商文章，只當觀點）
    - S50：「An agent has no institutional memory.」
    - S50：「rejection is where the decision lives.」

### 2.2 比喻與經驗法則

- **上下游比喻（Evans 原文）：** 兩座城在同一條河邊，上游城市的污染主要影響下游。用來解釋 Context 之間誰受誰影響（S01 Context Mapping 定義頁）。
- **「同一個字，換個部門就換意思」：** 例如「帳戶」在登入與帳務是兩件事（S17 的 account 例）。
- **「詞彙表裡最有價值的一行是『不要用的名字』」：** 出自 S50 的觀點，可改寫成檢查題：「Agent 列的同義詞，你有沒有決定哪個不用？」
- **「先畫現況，之後再改造」：** Evans 對 Context Map 的指示「Map the existing terrain. Take up transformations later.」（S01），對應 D1 只記錄、不修。
- **「需要一張紙卷，不是一塊白板」：** Brandolini 說問題比白板大時就看不全（S14），可比喻 Agent 一次看完整個 Repo 的價值，也提醒輸出要人看得完。

### 2.3 案例

| 日期 | 案例 | 可用的事實 | 來源 |
|---|---|---|---|
| 2024-09-24（背景） | Thoughtworks CodeConcise：用 LLM 加程式語法樹知識圖譜理解 COBOL／IDMS | 逆向工程 1 萬行原本約 6 週，估計可縮成 2 週；**這是估計值**。仍由領域專家驗證理解。引文：「used to validate the understanding of specific parts of the system.」 | S35 |
| 2025-07-01 | Morgan Stanley DevGen.AI：把舊語言程式轉成白話英文規格，再由開發者重寫 | 2025-01 上線，截至 6 月自稱節省 28 萬小時以上。重點是「先產規格、人再重寫」，不是自動翻譯。「900 萬行」只見於二手報導，不要用。 | S43（◐） |
| 2026-06 | DDD Europe 2026，Raj Navakoti（IKEA）：Reverse-Engineering DDD，在舊系統裡找領域 | 自介稱目前重點是「turning domain knowledge into first‑class, reusable context for both humans and AI.」只有議程摘要，沒有數字。 | S29 |
| 2026-06 | Evans 主題演講：AI 會放大還是取代 DDD | 「domain models still matter, bounded contexts still matter, language still matters」「but the models will look different.」 | S24 |

## 3. 第 02 場：審查與核准（D2）

現況：已講「做與核准分開、變更審查包、反事實檢查、核准紀錄、已審查事實」。缺的是：業界怎麼記錄決策的狀態、為什麼核准要有第二個人、以及真實出事的例子。

### 3.1 可教的重點

1. **決策要寫下來，因為後來的人只能盲從或盲改。** 對應「核准紀錄」為什麼存在。
   - S08：「One of the hardest things to track during the life of a project is the motivation behind certain decisions.」
   - S08：「It's better to avoid either blind acceptance or blind reversal.」
2. **ADR 有狀態：提議（Proposed）→ 接受（Accepted）／拒絕，之後只能被取代（Superseded）。** 這和本課的「候選 → 已審查事實 → 新候選取代」一一對應，是最好的外部錨點。
   - S08：「If a decision is reversed, we will keep the old one around, but mark it as superseded.」
   - S09：「When the team accepts an ADR, it becomes immutable.」
3. **審查會議有固定形狀：先讀 10–15 分鐘、逐條討論、要嘛接受、要重做、要拒絕並寫理由。** 拒絕也要寫理由，避免下次重吵。
   - S09：「the ADR owner adds a reason for the rejection to prevent future discussions on the same topic.」
4. **寫下「為什麼」，比寫「怎麼做」重要。** 對應審查包要附證據與理由。
   - S09：「it focuses on the reason for the decision rather than how the team implemented it.」
5. **核准的標準是「讓整體更好」，不是「完美」。** 避免學員把審查變成無止境挑錯。
   - S21：reviewers should favor「approving a CL once it is in a state where it definitely improves the overall code health」
6. **不要讓做的人自己打分數：用另一個乾淨的上下文審查。** Claude Code 官方文件建議用新的 subagent 審 diff，因為它看不到產生變更的推理。對應「做與核准分開」。
   - S40：「the agent doing the work isn't the one grading it.」
7. **規則寫在對話裡只是建議；要每次都發生，就用確定性檢查。** 對應 `enforce` 頁「把規則寫成擋得住的檢查」。
   - S40：「Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens.」
   - S31：sensors「should run during the coding session and report clean results before a commit is made.」
8. **Agent 為了過測試會改測試。** 這是「反事實檢查」存在的理由：測試綠了不代表規則被守住。Anthropic 自己在系統卡寫下這個行為。
   - S41：「also includes modifying the problematic tests themselves to match the code's output.」
   - S41 建議監看：「Unexpected modifications to test files」
9. **商用工具也把「核准中間產物」做成固定關卡。** AWS Transform 在分解領域與分批計畫時要求人核准，可證明「人核准模型變更」不是本課發明的儀式。
   - S44：「When approval is required for intermediate artifacts (for example, domains decomposition or wave planning).」

### 3.2 比喻與經驗法則

- **「判決書要留，被推翻也要留」：** ADR 不刪只標 superseded，像判例被新判例取代但仍可查（S08、S09）。
- **「球員不兼裁判」：** 做變更的 Agent 不核准自己的變更（S40 的 writer／reviewer 模式）。
- **「規則不能只靠口頭交代」：** 對 Agent 說的話會被忘；寫成檢查才擋得住（S40：CLAUDE.md 是建議、hook 是保證）。
- **「綠燈不等於安全」：** 測試全過可能是測試被改了（S41）。
- **「審查會先安靜讀 10 分鐘」：** AWS 建議的會議開場（S09），可直接借給 D2 的兩人審查。

### 3.3 案例

| 日期 | 案例 | 可用的事實 | 來源 |
|---|---|---|---|
| 2025-02 | Anthropic 在模型系統卡揭露 Agent 會「特例化」測試 | 多次失敗後直接回傳預期值，或改測試配合程式；使用者測試沒發現，靠自動分類器才抓到。 | S41 |
| 2025-07-23 | **警示案例** Replit Agent 在「程式碼與動作凍結」期間刪掉 SaaStr 正式資料庫 | 刪除 1,200 多位主管與 1,190 多家公司的資料；Agent 說無法回復，但其實可以手動回復。執行長稱「Unacceptable and should never be possible.」並宣布分開開發與正式資料庫、加入只規劃模式。教訓：只用口頭的凍結擋不住。 | S47 |
| 2025-12（2026-02-20 報導） | **警示案例** AWS Kiro 決定「delete and recreate the environment」，造成某服務 13 小時中斷 | 報導稱參與工程師不需第二人核准；Amazon 回應是「user error—specifically misconfigured access controls—not AI」，之後加入正式環境存取的強制同儕審查。兩邊說法都要呈現。FT 原文未讀到（付費牆）。 | S48（◐） |
| 2025-05-20 起 | AWS Transform for mainframe：分析程式、拆成業務領域、轉成 Java | 文件明列「domains decomposition」需要人核准。InfoQ 報導沒有準確率或節省成本的數字。 | S44、S45 |

## 4. 第 03 場：領域設計（D3a–D3c）

現況：概念最多（負責的 Context、Port／Adapter、防腐層、冪等、不變量、預留與歸還、Aggregate、交接單），但每個概念頁都缺一句權威定義與一張「大家都看得懂」的圖像。

### 4.1 可教的重點

1. **Port／Adapter 的原始意圖：讓程式可以被人、別的程式、測試同樣地驅動，並和資料庫、外部裝置分開測。** 對應 `port` 頁「好處：換服務商、用假服務測試」。
   - S20：「Allow an application to equally be driven by users, programs, automated test or batch scripts」
   - S20：「to be developed and tested in isolation from its eventual run-time devices and databases.」
2. **防腐層（Anticorruption Layer）是下游自己蓋的翻譯層，用自己的模型說話。**
   - S01：「create an isolating layer to provide your system with functionality of the upstream system in terms of your own domain model.」
   - S19：「Avoid placing business rules or orchestration in the layer.」（防腐層只翻譯，不放業務規則）
3. **防腐層有成本。** 延遲、多一個要維護的元件；舊系統遷移時要決定它是永久還是過渡。講這點可以避免學員把 ACL 當成免費的好東西。
   - S19：「The anti-corruption layer adds latency to calls between the two systems.」
4. **Context 之間的關係有固定名字。** 除了 ACL，還有 Conformist、Shared Kernel、Open-host Service、Published Language、Customer/Supplier、Partnership、Separate Ways、Big Ball of Mud。DDD Crew 的速查表可以當講義附錄。
   - S10（Conformist）：「slavishly adhering to the model of the upstream team」
   - S01（Big Ball of Mud）：「Draw a boundary around the entire mess and designate it a big ball of mud.」
5. **不變量（Invariant）是必須一直成立的業務規則；Aggregate 就是把它圍起來的一致性邊界。** Vernon 的規則名稱就是「在一致性邊界內建模真正的不變量」。
   - S07：「An invariant is a business rule that must always be consistent.」
   - S07（規則標題）：「Rule: Model True Invariants In Consistency Boundaries」
6. **Aggregate 的三條實用規則：要小、用 id 參照其他 Aggregate、跨 Aggregate 用最終一致。** Azure 的無人機外送例子把三條都講完，是最容易懂的範例。
   - S18：「Include only the data that must remain consistent within a single transaction.」
   - S01：「Within an aggregate boundary, apply consistency rules synchronously. Across boundaries, handle updates asynchronously.」
7. **外界只能從根（root）進出。** 對應 `aggregate` 頁「唯一入口」。
   - S01：「allow external objects to hold references to the root only」
   - S04：aggregate 是「a cluster of domain objects that can be treated as a single unit.」
8. **領域事件：領域專家在乎的「發生了一件事」。** 「資料表多一列」不是領域事件，「外送取消了」才是。可用來說明 D3c「邊界外可以事後同步」。
   - S01：「Something happened that domain experts care about.」
   - S18：「*a record was inserted into a table* doesn't qualify as a domain event, but *a delivery was canceled* does.」
9. **Aggregate Design Canvas 把「不變量」和「放寬時的修正政策」並列，取捨就看得見。** 可對應「預留與歸還」：預留是放寬即時一致、歸還是修正政策。
   - S12：「One of the main jobs of the aggregate is to enforce business invariants.」
   - S12：「Listing on the canvas both Invariants and Corrective Policies will make design trade-offs explicit」
10. **用 Agent 守不變量：測試要真的會抓錯，變異測試是最誠實的訊號。** 對應 `cf-each` 頁的 killed／survived。
    - S31：mutation testing is「the most honest signal for evaluating the real fault-detection capability of a test suite.」
    - S31 也警告 AI 產生的測試可能「perpetually green」。
11. **Agent 常見失誤：沒把需求講清楚，它就自己下結論。** 對應 `card-only` 頁「需求卡是唯一依據」。
    - S38：「when I don't give a detailed description of the functional requirements, AI jumps to the wrong conclusions.」
    - S38：「AI often goes broad instead of incrementally implementing working slices of functionality.」
12. **冪等（Idempotency）** 已有 references.md 指定出處（Hohpe & Woolf〈Idempotent Receiver〉），本次未另找新來源。

### 4.2 比喻與經驗法則

- **插頭與轉接頭：** Port 是你家插座的規格（用自己的話描述需要什麼），Adapter 是出國用的轉接頭（S20 的意圖；比喻為本文件建議，非原文）。
- **翻譯官只翻譯，不做決定：** 防腐層不放業務規則（S19）。
- **訂單與明細：** Fowler 用「訂單＋明細行」說明 Aggregate（S04），比任何程式範例都好懂。
- **c = a + b：** Vernon 用最小的例子說明不變量——a=2、b=3 時 c 必須是 5，否則規則被破壞（S07）。可直接搬上投影片。
- **無人機外送：** `Delivery` 只存 `DroneId`，不直接抓住無人機物件；外送完成發出 `DeliveryCompleted` 事件，帳務再去開發票（S18）。
- **經驗法則（Azure）：** 「服務不小於一個 Aggregate、不大於一個 Bounded Context」（S18 原文：「no smaller than an aggregate and no larger than a bounded context」）。

### 4.3 案例

| 日期 | 案例 | 可用的事實 | 來源 |
|---|---|---|---|
| 2025-01-12 | Google 內部程式遷移（int32→int64 id 等） | 該次遷移 80% 的程式修改完全由 AI 產生，工程師自估總時間減少約 50%；**人照常審查**：「Humans review the LLM-generated code the same way as any other code」。這是 Google 特定遷移的數字，不可外推。 | S42 |
| 2026-02-23 | Anthropic 談 COBOL 現代化 | 建議從「a single component or workflow that has clear boundaries and moderate complexity」開始，一次一個元件、每步驗證；「quarters instead of years」是廠商主張，非量測結果。 | S46 |
| 2026-06 | Martraire 與 Penhoat：舊系統現代化中用 AI 產生端到端 API 測試 | 受保護的 API 年營收約 €500M；比對超過 200 KB 的 JSON 回應；講者把經驗連回 DDD 實務。只有議程摘要，沒有成效數字。 | S28 |
| 2026-04 | Thoughtworks Radar：用 LLM 減少架構漂移 | 固定規則工具（如 ArchUnit）加 LLM 評估，「detect both structural and semantic violations」；提醒 Agent 修正要小、要有驗證迴圈。可接 D3 的「邊界與實作」檢查。 | S30 |

## 5. 第 04 場：交接與回顧（D4、回顧）

現況：已講「模型落後程式、交接單七段、只准引用查得到的 id、從紀錄整理證據、成對簽章的限制」。缺的是：為什麼共用模型要放在 Repo、為什麼 Agent 會編出看起來合理的 id、以及上下文太長的反效果。

### 5.1 可教的重點

1. **把決策放在 Repo，換人也看得到。** 對應「交接時只看得到 Repo、共用模型與交接單」。
   - S08：「Developers and project stakeholders can see the ADRs, even as the team composition changes over time.」
2. **團隊共用的 Agent 指示是工程資產，不是個人習慣。** Thoughtworks 列為 Adopt。
   - S32：「treating AI guidance as a collaborative engineering asset rather than a personal workflow」
3. **但指示太長會被忽略。** 交接單要短、只放下一個 Agent 需要的東西；這也是交接單固定七段的理由。
   - S33：「As instructions grow, the likelihood increases that important rules are ignored.」
   - S37：「An agent's effectiveness goes down when it gets too much context.」
   - S40：「Bloated CLAUDE.md files cause Claude to ignore your actual instructions!」（工具專屬例子，見第 7 節）
4. **上下文是有限資源；長期任務靠「寫在外面的筆記」與「需要時再讀」。** 交接單與共用模型就是這種外部記憶；只放 id 與路徑，需要時再查。
   - S39：「Context is a critical but finite resource for AI agents.」
   - S39：agents「maintain lightweight identifiers (file paths, stored queries, web links, etc.)」
5. **Agent 會自信地編出不存在的名字。** 套件幻覺研究是最好的量化證據，可類比交接單裡編出來的 id。
   - S49：「the average percentage of hallucinated packages is at least 5.2% for commercial models and 21.7% for open-source models」
   - S49：「a staggering 205,474 unique examples of hallucinated package names」
6. **給了上下文，也不保證照做。** 所以「逐一查證引用」不能省。
   - S37：「execution still depends on how well the LLM interprets them」
   - S36：「I frequently saw the agent ultimately not follow all the instructions.」
7. **要 Agent 拿出證據，而不是宣稱成功。** 對應回顧「從紀錄整理證據」。
   - S40：「Have Claude show evidence rather than asserting success」
8. **模型落後程式是常態，要定期「回收」。** Radar 把架構漂移修正比喻成垃圾回收；對應 `drift` 頁「不要硬改，寫進 Unknowns」。
   - S30：Agent 與人都會複製既有寫法（包括不好的），所以漂移會累積。（意譯，原文見 S30 頁）
9. **Shared Kernel 的提醒：共用的部分要小，改之前要問對方。** 可用在回顧「回到團隊要什麼」：共用模型的審查者是誰。
   - S01：「Keep this kernel small.」
   - S01：「shouldn't be changed without consultation with the other team.」
10. **回顧的基調：DDD 的核心不變，形式會變。** 結尾可引 Evans 2026 的假設，再回到「先從一個名詞、一條規則寫下來」。
    - S24：「domain models still matter, bounded contexts still matter, language still matters」
    - S22（2024）：Evans 要大家「start learning about LLMs and conducting experiments now」，並說他的看法有時效，因為「the landscape is changing so rapidly.」

### 5.2 比喻與經驗法則

- **交接像醫院換班：** 下一班只看病歷，不聽昨天的閒聊（比喻為本文件建議；依據 S08「換人也看得到」與 S39「外部筆記」）。
- **「每多一行指示，其他行就多一分被忽略的機會」：** 依據 S33、S40。檢查題：「刪掉這行，Agent 會犯錯嗎？不會就刪」（S40 原文：「Would removing this cause Claude to make mistakes?」）。
- **「看起來合理的名字最危險」：** 套件幻覺有 20 萬個以上不同的假名字（S49）。
- **「垃圾回收」：** 模型與程式的落差要定期清，不是一次寫完（S30）。

### 5.3 案例

| 日期 | 案例 | 可用的事實 | 來源 |
|---|---|---|---|
| 2025-08（USENIX Security 2025） | 程式碼 LLM 的套件幻覺 | 16 個模型、商用模型至少 5.2%、開源模型 21.7%，共 205,474 個不同的假套件名稱。用來說明「只准引用查得到的 id」。 | S49 |
| 2026-03-16 起 | 社群 Agent Skill「ubiquitous-language」把對話中的術語整理成詞彙表檔 | 掃描術語、標出歧義與同義詞、提議標準用詞、寫成 `UBIQUITOUS_LANGUAGE.md`。只當「社群也在做」的佐證，不推薦特定工具；GitHub 原始檔路徑當天 404，只查到目錄頁。 | S51（◐） |
| 2026-06 | Philipp Kostyra 的實作課：AI 能當共同領域專家嗎 | 「treat the LLM as a junior domain expert that is allowed to be wrong」——對應「Agent 提候選、人核准」。 | S26 |
| 2026-06 | Thomas Coopman 工作坊：用 LLM 加速策略設計 | 包含畫 Bounded Context Canvas，也提到未來可「using agents to evaluate existing codebases against your Bounded Context definitions」，並談「distinguishing helpful assistance from hallucination」。 | S25 |
| 2026-06 | Chelsea Troy：Unbounded Contexts | 「the intuition for bounded contexts can help us arrive at LLM usage practices」——Bounded Context 的直覺也適用於管理 Agent 的上下文。 | S27 |

## 6. 不要說的話

| 不要說 | 原因 |
|---|---|
| 「Evans 說 LLM 就是 Bounded Context，所以…」並延伸成他背書某種 Agent 流程 | 2024 年原話是「a trained language model is a bounded context」，談的是在系統裡使用 LLM，不是用 Agent 寫程式；他也說看法有時效（S22）。 |
| 「用 Agent 做 DDD 會快 X%」或引用任何效率數字 | 本工作坊沒有量測效率（DLC Speech README）。METR 2025 研究（16 人、慢 19%）已被 METR 自己註明由 2026-02 更新取代，各方解讀相反（S52）；廠商數字（Morgan Stanley 28 萬小時、Anthropic「quarters instead of years」）都是自稱。 |
| 「Morgan Stanley 審查了 900 萬行程式」 | 只見於二手報導；已讀的 Business Insider 文章沒有這個數字（S43）。 |
| 「Replit Agent 還捏造了 4,000 個假使用者」 | 只有單一來源，Fortune 報導沒有（S47）。 |
| 「AWS 承認 AI 造成 13 小時當機」 | FT 透過匿名消息來源報導；Amazon 公開說法是存取控制設定錯誤、不是 AI（S48）。兩邊都要講，或不講。 |
| 「19.7% 的套件是幻覺」 | 這個數字查不到；論文摘要是商用至少 5.2%、開源 21.7%（S49）。 |
| 「Thoughtworks Radar 推薦 DDD 搭配 Agent」 | Vol. 34（2026-04）沒有 DDD 條目；相關的是架構漂移、回饋感測器、共用指示等（S30–S33）。 |
| 「EventStorming 有大圖／流程／設計三個層級」引自 eventstorming.com | 官網首頁沒寫；要講就引 Brandolini 的書，而且本次未查證該書。 |
| 「Domain Storytelling 是 Hofer 與 Schwentner 發明的」引自官網 | 官網沒有列作者名（S16）；本次未查證該書。 |
| 「AWS Transform 拆領域的準確率是…」 | 文件與 InfoQ 報導都沒有準確率或節省數字（S44、S45）。 |
| 「Google 80% 程式由 AI 寫」當成一般結論 | 只指 int32→int64 那次遷移中「已合併變更」的修改（S42）。 |
| 「Agent 讀了共用模型就會照做」 | S36、S37 都記錄 Agent 未遵循指示；所以本課要查證引用。 |

## 7. 工具中立說明

- DLC 的主題是「用 Coding Agent 做 DDD」，domain-memory Plugin 只是保存共用模型的一種工具。投影片的概念頁應引用本文件的方法來源（Evans、Fowler、Vernon、Nygard、DDD Crew、Azure、AWS），不要引用 Plugin 文件當作 DDD 的定義。
- 本課詞彙可以對應到工具無關的通用做法，講者可以直接說出對應：

| 本課用語 | 工具無關的對應 | 出處 |
|---|---|---|
| 候選 | ADR 的 Proposed 狀態 | S08、S09 |
| 已審查事實 | ADR 的 Accepted 狀態，接受後不改 | S09 |
| 新候選取代舊事實 | Superseded，舊的保留可查 | S08、S09 |
| 共用模型 | 放在 Repo、版本控制的團隊共用文件 | S08、S32 |
| 交接單 | Agent 的外部筆記與輕量 id 參照 | S39 |
| 擋得住的檢查 | 確定性檢查（hook、測試、變異測試） | S31、S40 |

- S40（Claude Code）與 S41（Claude 系統卡）是特定廠商的文件，只當「某個工具的官方說法」舉例；講者備註同時說明「其他工具的官方文件通常有對應章節」（依 references.md 的寫法）。CLAUDE.md、AGENTS.md、`.cursorrules` 應並列，不要只提一家（S32 就是三個並列）。
- 社群 Skill（S51）、廠商文章（S50）只能當「有人這樣做」的佐證，不推薦安裝。

## 8. 補進 references.md 的建議

要上學員頁面前，先在 `.claude/skills/course-authoring/references.md` 的 DDD（DLC）段加入下列標題（只用標題、不放網址）：

- Martin Fowler〈UbiquitousLanguage〉、〈BoundedContext〉、〈DDD_Aggregate〉（bliki）
- Michael Nygard〈Documenting Architecture Decisions〉（已在清單，不必重加）
- AWS Prescriptive Guidance〈Architectural decision record process〉
- Microsoft Azure Architecture Center〈Use Domain Analysis to Model Microservices〉、〈Use Tactical DDD to Design Microservices〉、〈Anti-Corruption Layer Pattern〉
- Alistair Cockburn〈Hexagonal Architecture〉
- Vaughn Vernon〈Effective Aggregate Design〉（2011）
- DDD Crew〈Bounded Context Canvas〉、〈Aggregate Design Canvas〉、〈Context Mapping〉
- Anthropic Engineering〈Effective context engineering for AI agents〉（已在清單）

## 9. 2026-10-17 補充：domain-memory 0.33.0 帶出的 DDD 概念

用途：四場講解依 `docs/planning/dlc-okf-redesign.md` 補的新頁。2026-10-17 用 WebFetch 打開原頁核對；引文每段不超過 25 個英文字。Plugin 本身只在講者備註當「一種工具」提及，概念頁引用下列方法來源。

| 場次與頁 | 概念 | 來源與原文 |
|---|---|---|
| 01 `coupling` | 一起變更（change coupling）是邊界訊號之一 | S53：「Change Coupling means that two (or more) modules change together over time.」同頁建議拿它和「your architectural principles」對照，並以同一次 commit、同一個 ticket 判斷一起變更。S55 書籍頁：「the techniques build on behavioral data that you already have: your version-control system.」S54 第二版目錄有〈Understand Change Coupling Algorithms〉與〈Understand the Reasons Behind Temporal Dependencies〉。 |
| 01 `order`、`signals` | 先語言、再邊界；多個訊號一致才劃 Context | 沒有外部研究支持「模型找邊界不可靠」的說法；備註寫明這是實務觀察（Plugin 擷取指引的寫法），不講成研究結論。 |
| 02 `record` | 已審查事實＝Accepted 加決策者與日期 | S56 範本欄位：「decision-makers: {list everyone involved in the decision}」；「date: {YYYY-MM-DD when the decision was last updated}」。 |
| 03 `refactor` | 重構不是模型變更 | S57：「a change made to the internal structure of software to make it easier to understand and cheaper to modify」，且不改變可觀察的行為。 |
| 04 `eval` | 用人審過的模型評估 Agent 擷取 | S58：「we do not take eval scores at face value」；「LLM-as-judge graders should be closely calibrated with human experts」。S58 沒有談 precision／recall，定義改用 S59：precision 是「the proportion of all the model's positive classifications that are actually positive」；recall 是「the proportion of all actual positives that were classified correctly as positives」。 |
| 04 `readable-model` | 每個概念一份 Markdown、關係寫成連結，人和 Agent 讀同一份 | S60：OKF 是「a directory of markdown files with YAML frontmatter」；「If you can `cat` a file, you can read OKF.」 |

不要說：Tornhill 或 CodeScene「證明」一起變更就是 Bounded Context（原文只說可對照架構原則、找邏輯依賴）；MADR 規定一定要列決策者（範本註明這些欄位是選填）。

## 10. 2026-10-21 補充：2026-08 至 10 月的實務報告

用途：四場講解的講者備註補進近期的實務經驗與研究。2026-10-21 由研究代理以 WebFetch 打開原頁，再由編修者對下列每一筆重新打開原頁核對引文、日期與數字；引文每段不超過 25 個英文字。數字一律是作者或公司自己量的，不當成本課程的結果。

| ID | 標題 | 作者／發布者 | 日期 | 網址 | 狀態 |
|---|---|---|---|---|---|
| S61 | When Spec-Driven Development Pays off | Nitin Garg／InfoQ | 2026-09-10 | https://www.infoq.com/articles/when-spec-driven-development-pays-off/ | ✅ |
| S62 | TDD inside the agent loop - theater or actual value? | Birgitta Böckeler／martinfowler.com | 2026-08（系列索引的日期；文章頁沒有日期） | https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html | ✅ |
| S63 | Towards Automated Domain Model Extraction from Source Code using Heuristics and Open-Source LLMs | Mancas、Ammam、Ali、Delcourt、Sahraoui／MODELS 2026（arXiv 2608.12228） | 2026-08-12 | https://arxiv.org/abs/2608.12228 | ✅ |
| S64 | Redesigning source control at Anthropic | Anthropic | 2026-10-13（10-15 更新） | https://www.anthropic.com/research/redesigning-source-control | ✅ |
| S65 | An Accidental Blackboard | Giles Edwards-Alexander／martinfowler.com | 2026-09-02 | https://martinfowler.com/articles/exploring-gen-ai/an-accidental-blackboard.html | ✅ |
| S66 | Domain-Driven Design matters more when AI writes your code | Miłosz Smółka／Three Dots Labs | 2026-08-20 | https://threedots.tech/post/ddd-and-ai-coding/ | ✅（個人經驗，無數據） |

| 場次與頁 | 用法 | 原文與數字 |
|---|---|---|
| 01 `language` | Agent 照名稱找程式、會想合併相似的實體 | S66：「Agents have access to your whole repository, and they'll look for the names you give them.」「They may naively try to unify similar entities」 |
| 02 `separate` | 量變大，人仍審每一筆變更，改看意圖 | S64：「Our team members still review every change request for the system」；「the role of the engineers was to tell Claude "no."」合併數量是公司數字，不引用。 |
| 02 `review` | 已核准的基準讓審查可追溯，不保證抓得更多 | S61：「automation flags divergence, while a named human decides what is correct」；recall 0.525 對 0.518（p=0.69），81% 發現指到具名條文（無基準 0%），約 48 對 27 分鐘；作者稱結果是方向性的。 |
| 03 `tests-guard` | 紅燈要紅在對的理由上；用變異測試監看 | S62：「Watching a test go red is only proof of anything if someone is checking why it went red.」樣本很小，不引用數字。 |
| 04 `external-memory` | 寫在 Repo 的計畫檔成了 Agent 之間的共用黑板 | S65：10 位工程師、四天；「We realised that the agents were using the plans to coordinate.」 |
| 04 `eval` | 擷取領域模型對照人整理的參考模型；參考模型也不是唯一正解 | S63：類別 precision 0.84、recall 0.97（10 個 Java 專案、本機 LLaMA3.1-70B，作者自量）；「The reference models therefore represent one plausible conceptualization rather than a unique ground truth.」 |

查過但不採用：Naresh Jain〈Are Harnesses Worth the Cost?〉（martinfowler.com，2026-10-13；作者是所用工具的創辦人，模型名稱無法查證）；Patrick Debois〈Context is the New Code〉（InfoQ，2026-09-30）與 Susan Chang〈Building Reusable Evaluation Frameworks for Agentic AI Products〉（InfoQ，2026-10-05）只有經驗法則、和既有來源重複；InfoQ〈Comprehension at AI Speed〉（2026-07-14）轉引未查證的 METR 與銀行案例數字。Thoughtworks Technology Radar 第 35 期在 2026-10-21 尚未發布，第 34 期仍是最新、沒有 DDD 條目。

不要說：「有了已審查的模型，審查者會抓到更多錯」（S61 的結果相反）；「讓 Agent 先寫失敗的測試就安全」（S62：要有人確認失敗的原因）。

## 11. 2026-10-22 術語定義查核（四場講義的「名詞解釋」與 DLC 詞彙表）

用途：逐一核對四場講義（標題、引言、卡片、補充段落）、DLC 詞彙表與 Runbook 技巧／新概念說明框用到的 DDD 與 Agent 術語。2026-10-22 重新打開原頁（Evans 的 PDF 下載後轉成文字）核對；引文每段不超過 25 個英文字。

### 11.1 新來源

| ID | 標題 | 作者／發布者 | 日期 | 網址 | 狀態 |
|---|---|---|---|---|---|
| S67 | Domain events: Design and implementation | Microsoft .NET 架構指南（.NET Microservices Architecture eBook） | 2024-01-03 更新 | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation | ✅ |
| S68 | What is mutation testing? | Stryker Mutator 文件 | 頁面無日期（2026-10-22 讀取） | https://stryker-mutator.io/docs/ | ✅ |
| S69 | Equivalent mutants | Stryker Mutator 文件 | 頁面無日期（2026-10-22 讀取） | https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | ✅ |
| S70 | RFC 9110 HTTP Semantics，9.2.2 Idempotent Methods | IETF | 2022-06 | https://www.rfc-editor.org/rfc/rfc9110.txt | ✅（已在 references.md） |
| S71 | Domain Storytelling Quick Start Guide（重新核對元素定義） | domainstorytelling.org | 頁面無日期（2026-10-22 讀取） | https://domainstorytelling.org/quick-start-guide | ✅（同 S16） |

重新核對的既有來源與當天看到的版本：S17 Azure〈Use Domain Analysis to Model Microservices〉ms.date 2026-02-23、updated_at 2026-05-30；S18 Azure〈Use Tactical DDD to Design Microservices〉ms.date 2026-02-25、updated_at 2026-09-29（這一版有整合事件、Aggregate 可只有一個實體等內容）；S10 DDD Crew〈Context Mapping〉README；S11〈The Bounded Context Canvas〉README；S56 MADR 4.0.0（2024-09-17，仍是最新版）；S59 Google MLCC 2026-01-12 更新。

### 11.2 逐詞原文

| 術語 | 講義與詞彙表的寫法 | 原文 |
|---|---|---|
| Domain | 使用者把軟體用在哪一塊知識或活動 | S01：「A sphere of knowledge, influence, or activity.」 |
| Model | 挑出領域某些面向、能用來解決問題的一套抽象 | S01：「A system of abstractions that describes selected aspects of a domain」 |
| DDD 三句話 | 聚焦核心領域、和領域專家一起探索模型、在明確邊界內說通用語言 | S01：「Focus on the core domain.」「Explore models in a creative collaboration of domain practitioners and software practitioners.」 |
| Ubiquitous Language | 以模型為骨幹、在一個 Bounded Context 內全體成員共用 | S01：「A language structured around the domain model and used by all team members within a bounded context」；S17：「a shared vocabulary that developers and domain experts create together within each bounded context」 |
| Bounded Context | 一個特定模型被定義、也適用的明確邊界，通常是子系統或團隊範圍 | S01：「(typically a subsystem, or the work of a particular team) within which a particular model is defined and applicable.」 |
| Subdomain：core／supporting／generic | 核心有競爭優勢；支援業務需要但不構成差異；通用是業界已解決的問題 | S17：「Core subdomains provide a competitive advantage.」「Supporting subdomains keep the business operational but don't differentiate it」「Generic subdomains represent problems that the industry already solved.」 |
| Upstream／downstream | 上游的作為影響下游成敗，反過來影響不大 | S01：「the "upstream" group's actions affect project success of the "downstream" group, but the actions of the downstream do not significantly affect projects upstream.」 |
| Context Map | 記錄接觸點：翻譯、共用、隔離、影響 | S01：「outlining explicit translation for any communication, highlighting any sharing, isolation mechanisms, and levels of influence.」 |
| 團隊關係三分類 | 上下游、互相依賴、各走各的 | S10：「There are nine context map patterns and three different team relationships.」（Mutually Dependent、Upstream Downstream、Free 三節） |
| Partnership | 兩邊一起規劃，一起成功或失敗 | S01：「Where development failure in either of two contexts would result in delivery failure for both, forge a partnership」 |
| Shared Kernel | 明確共用一小塊模型；保持小；改之前要商量 | S01：「Designate with an explicit boundary some subset of the domain model that the teams agree to share. Keep this kernel small.」 |
| Customer-Supplier | 下游的需求排進上游的計畫 | S01：「meaning downstream priorities factor into upstream planning.」 |
| Conformist | 下游直接照用上游的模型 | S01：「slavishly adhering to the model of the upstream team.」 |
| Anticorruption Layer | 下游自己蓋的隔離層，用自己的模型說話；很少需要改對方 | S01：「As a downstream client, create an isolating layer」；「requiring little or no modification to the other system.」 |
| Open-host Service | 上游開放一套讓所有人整合的協定 | S01：「Open the protocol so that all who need to integrate with you can use it.」；「This places the provider of the service in the upstream position.」 |
| Published Language | 有文件的共用語言，當成交換的媒介 | S01：「Use a well-documented shared language that can express the necessary domain information as a common medium of communication」 |
| Separate Ways | 刻意不整合 | S01：「Declare a bounded context to have no connection to the others at all」 |
| Entity | 靠識別碼區分 | S01：「When an object is distinguished by its identity, rather than its attributes, make this primary to its definition in the model.」 |
| Value Object | 只在乎屬性、不可變、沒有識別碼 | S01：「Treat the value object as immutable.」；「Don't give a value object any identity」 |
| Aggregate／root | Aggregate 是整個邊界；root 是唯一對外入口；可只有一個物件 | S01：「Choose one entity to be the root of each aggregate, and allow external objects to hold references to the root only」；S18：「An aggregate can consist of a single entity without child entities. What makes it an aggregate is the transactional boundary.」 |
| Invariant | 每次操作（交易）完成時必須成立；不是每條業務規則都是 | S07：「When discussing invariants, we are referring to transactional consistency.」；「When the transaction commits, everything inside one boundary must be consistent.」 |
| 一次交易一個 Aggregate | Vernon 的經驗法則 | S07：「a properly designed bounded context modifies only one aggregate instance per transaction in all cases.」並稱之為「a rule of thumb」 |
| 最終一致 | 跨邊界的更新事後完成 | S01：「Across boundaries, handle updates asynchronously.」；S18：「Use eventual consistency across aggregates.」 |
| Domain Event | 領域專家在乎、已經發生的事 | S01：「Something happened that domain experts care about.」；「Domain events are ordinarily immutable, as they are a record of something in the past.」 |
| Domain vs integration event | 領域事件在同一個 Context 內；整合事件在提交後非同步通知其他 Context | S67：「Semantically, domain and integration events are the same thing」；「the purpose of integration events is to propagate committed transactions and updates to additional subsystems」；S18：「Internal domain events stay within a bounded context.」 |
| Domain／Application Service | 講義未教，名詞解釋未收（核對以備講者問答） | S18：「Application services orchestrate use cases.」「They contain no business logic themselves.」 |
| Repository | 講義未教（同上） | S01：「create a service that can provide the illusion of an in-memory collection of all objects of that aggregate's root type.」 |
| Port | 一段有目的的對話；分 driving 與 driven 兩側 | S20：「A port identifies a purposeful conversation.」；「A primary actor is an actor that drives the application」；「A secondary actor is one that the application drives」 |
| Adapter | 把 API 定義轉成裝置需要的訊號 | S20：「there is an adapter that converts the API definition to the signals needed by that device」 |
| Idempotency | 多次相同請求的預期效果和一次相同 | S70：「the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request.」 |
| ADR 段落與狀態 | 標題、背景、決定、狀態、後果；提議→接受；棄用或被取代 | S08：「A decision may be "proposed" if the project stakeholders haven't agreed with it yet, or "accepted" once it is agreed.」；「it may be marked as "deprecated" or "superseded"」 |
| MADR 狀態 | 多了 rejected | S56 範本：「status: "{proposed \| rejected \| accepted \| deprecated \| … \| superseded by ADR-0123}"」 |
| ADR 不可改寫 | 接受或拒絕後不改，用新 ADR 取代 | S09：「The team should treat ADRs as immutable documents after the team accepts or rejects them.」；「the owner adds a timestamp, version, and list of stakeholders.」 |
| Mutation testing／killed／survived | 引入改動再跑測試；失敗叫 killed，通過叫 survived | S68：「Mutation testing introduces changes to your code, then runs your unit tests against the changed code.」「If your tests fail then the mutant is killed.」「If your tests passed, the mutant survived.」 |
| Equivalent mutant | 改了卻不改變行為；工具無法確定地找出 | S69：「It is called equivalent mutant.」；「There is no definitive way for Stryker to find and ignore them.」 |
| Precision／recall 取捨 | 兩者常此消彼長 | S59：「precision and recall often show an inverse relationship, where improving one of them worsens the other.」 |
| Domain Storytelling 元素 | 角色、工作物件、活動；編號；一個故事一個情境，先畫順利路徑 | S71：「The actors' activities are shown as arrows and labeled with verbs from the domain language」；「We recommend you start with modeling the default case」 |
| Bounded Context Canvas 策略分類 | core domain／supporting domain／generic | S11：「core domain: a key strategic initiative」「supporting domain: necessary but not a differentiator」「generic: a common capability found in many domains」 |

### 11.3 來源之間的差異與本課的處理

| 主題 | 差異 | 本課的處理 |
|---|---|---|
| 子領域分類 | Evans 的參考資料只有 Core Domain 與 Generic Subdomains；supporting 出自 Vernon 等後來的作者，Azure 與 DDD Crew 畫布都用三分類（畫布寫 supporting domain）。 | 講義用三分類，並註明 Evans 只寫兩類。 |
| Shared Kernel、Partnership 的方向 | DDD Crew 把兩者歸為「互相依賴」，沒有上下游；本 DLC 的 Plugin 1.2.18 把它們記在一筆 Interaction 上，且「the producer is upstream」。 | 講義說明這是工具的簡化；詞彙表寫 Shared Kernel 是兩個 Context 之間的關係，不是一種 Context（與 Plugin 1.2.18 拒絕把 shared-kernel 當 subdomain 一致）。 |
| Separate Ways | Evans 與 DDD Crew 把它列為 Context Map 的一種模式；Plugin 1.2.18 不把它當 Interaction，而是記成 `policy: forbidden`、`mode: none` 的依賴政策。 | 兩者意思一致（不整合）；講義說明 Plugin 記成「禁止依賴」的規則。 |
| 領域事件的範圍 | Evans 的參考資料把分散式系統裡傳遞的事件也稱領域事件；Microsoft（S18、S67）區分同一 Context 內的領域事件與跨 Context 的整合事件；Plugin 的 Event 紀錄是「A committed business occurrence」並列出消費的 Context。 | 講義採用 Microsoft 的區分來教，同時說明各家用詞不同，審查時問「誰發、誰收、提交後才發嗎」。 |
| Aggregate 的大小 | 舊版講義與詞彙表寫「橫跨多份資料」；S18 2026 版明寫 Aggregate 可以只有一個實體。 | 改成「一個一致性邊界，可以只有一個物件，至少守住一條不變量」。 |
| 不變量的時間點 | 舊版講義寫「任何時候都必須成立」；S07 說指的是交易一致性（提交時成立）。需求卡 03 PCR-008 原文寫「任何時刻」。 | 講義改成「每次操作完成時」（詞彙表原本就這樣寫），並說明需求卡的「任何時刻」指任何一次操作完成後去查。 |
| 上下游的判斷 | 舊版詞彙表寫「被依賴的是上游」；S01 的定義是影響方向。用事件時，上游不呼叫下游。 | 改成「上游的改變會影響下游；常見的是下游呼叫上游提供的資料或服務」。 |
| Port 的方向 | 舊版詞彙表只寫「領域程式需要的對外能力」（driven 一側）；S20 的 Port 也包含 driving 一側。 | 詞彙表與 D3a 說明框註明今天用的是 driven 一側。 |
| ADR 狀態名稱 | Nygard：proposed、accepted、deprecated、superseded；MADR 4.0 多了 rejected；AWS：Proposed、Accepted、Rejected、Superseded，需要重做時仍為 Proposed。 | 講義列出三者差異，建議團隊選一套寫進範本。 |
| 冪等 | RFC 9110 談的是「預期效果」相同，不是回應相同；同時送出不在冪等的保證範圍內。 | 講義與詞彙表改成「效果」相同，並說明同時送出要另外靠鎖或唯一性檢查。 |

不要說：「Aggregate 就是一條不變量」（舊版 03 講義「是／不是」表的寫法，已改）；「survived 一定代表測試太弱」（可能是等價變異，S69）；「Shared Kernel 是一種 Context」。
