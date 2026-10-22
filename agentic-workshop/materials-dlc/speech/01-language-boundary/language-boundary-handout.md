# 共同語言與邊界：Agent 找證據，人來定義

> 讀者：學員。時機：DDD 延伸課 D1 之後的 30 分鐘講解。前置：已做完開場與 D1。

**這一段帶走什麼**
- DDD 的三句話，以及為什麼 Agent 寫程式時更需要寫在 Repo 裡的共用語言
- 候選與事實：Agent 提的名詞要附證據，等人核准才算數
- 交給 Agent 的順序：先整理語言、再劃邊界；邊界要多個訊號都指向同一處
- 邊界洩漏測試抓不到，要由人看證據判斷

每頁最後的段落是講解時來不及說的補充：概念的白話解釋、證據出處、限制與回到團隊的做法；提到的書與文章列在最後的「延伸閱讀」。

本場講概念與技巧，不需要寫程式或打指令。頁面上的提示詞是示範，想試再貼給自己的 Agent；沒有實際執行的結果，一律視為未驗證。

## 1. DDD 的三句話

DDD（Domain-Driven Design，領域驅動設計）的作者 Evans，把它濃縮成三句話。

- **聚焦核心領域**：力氣花在讓業務與眾不同的那一塊。

- **和領域專家一起建模**：模型是討論出來的，不是工程師自己想的。

- **在明確邊界內說通用語言**：同一個範圍內，同一件事只有一個名字。

Evans 在 2003 年的同名書中提出 DDD；2015 年他把定義與模式整理成免費公開的〈Domain-Driven Design Reference〉，這三句話就出自這份摘要。領域專家是真正懂這門業務的人，例如櫃檯、法遵、產品負責人；「模型」不是一張圖，而是團隊對業務的共同理解：有哪些名詞、哪些規則、誰負責什麼。

三句話裡的詞，Evans 的參考資料都有定義。領域（domain）是使用者把軟體用在哪一塊知識或活動，例如訂票、退票、會員點數；模型（model）是挑出領域的某些面向、能用來解決這個領域問題的一套抽象。所以模型一定有取捨：它只回答它要回答的問題。

「聚焦核心領域」要先分出哪一塊是核心。微軟 Azure 架構中心依 DDD 把子領域（subdomain，業務裡相對獨立的一塊）分成三類：核心（讓公司和對手不同，值得投入最多設計）、支援（業務需要但不構成差異，例如開發票）、通用（業界早有現成做法，例如使用者帳號）。用詞各家略有不同：Evans 的參考資料只寫核心領域（Core Domain）與通用子領域（Generic Subdomains），「支援」這一類出自 Vernon 等後來的作者。對 Agent 協作的意義：核心那一塊最值得人花時間審查 Agent 的提案；通用那一塊，先找現成方案。

有 Agent 寫程式時，這三句話更吃重：Agent 照它讀到的名詞取名、照它看到的規則寫判斷；名詞不一致、規則沒寫下來，它就照最常見的寫法猜。本 DLC 主要練第二、三句：Agent 幫忙找證據，定義由人和領域專家決定。

常見誤解：DDD 不是一種資料夾結構，也不等於拆微服務；它首先是讓團隊說同一套話的做法。下週可以先挑一個團隊最常被說錯的名詞，寫一句定義，問一位懂業務的同事這樣對不對。

📖 延伸閱讀：〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026）

**人工確認**：D1 裡哪一個決定你最沒把握？先記下來，最後一頁回來對照。

## 2. 有了 AI，DDD 還重要嗎

Evans 在 DDD Europe 2026 主題演講：模型、邊界、語言都還重要，只是樣子會變。

- **Evans（2026）**：用 LLM 加上確定性計算，從程式抽出領域詞彙。

- **社群在試**：同場有多場講 LLM 協助策略設計與建模。

Evans 在 2026 年 6 月 DDD Europe 研討會的開場主題演講摘要說：領域模型、Bounded Context（限界上下文，本場後面會講）與語言都還重要，只是模型的樣子會變。摘要也提到用 LLM（Large Language Model，大型語言模型，也就是 Agent 背後的模型）加上確定性的計算（每次結果都一樣的程式），從程式碼抽出領域詞彙。同場還有人用 LLM 協助畫邊界畫布，並討論怎麼分辨有用的協助和幻覺（模型自信地說出不實內容）。

限制：這些都只有議程摘要，沒有公開成效數字；它們說明社群正在試，不證明哪種做法有效。也不要把 Evans 2024 年「訓練好的語言模型就是一個 Bounded Context」那句話，延伸成他背書某種 Agent 流程：那句談的是在系統裡使用 LLM，而且他自己說看法會隨技術變化而過時。

回到團隊，先盤點領域知識現在放在哪裡。只存在某幾個人腦袋裡的知識，Agent 讀不到，也是交接時最先遺失的部分。

📖 延伸閱讀：〈Opening Keynote Eric Evans〉（DDD Europe，2026）；〈Accelerate your Strategic Design with LLMs〉（Thomas Coopman／DDD Europe，2026）；〈The Curse of Unbounded Contexts: Using Domains as LLM Consumers〉（Chelsea Troy／DDD Europe，2026）；〈Eric Evans Encourages DDD Practitioners to Experiment with LLMs〉（InfoQ，2024）

**人工確認**：你的團隊現在把領域知識放在哪裡：人的腦袋、文件，還是程式？

## 3. Agent 是沒有走廊記憶的新同事

Agent 沒聽過會議和茶水間的討論；對話一結束，就忘了你們選了哪個名字。

- **上下文有限**：塞太多，重要的規則反而被忽略。

- **寫進 Repo**：模型放 domain-memory，團隊決定寫進 AGENTS.md。

Agent 每次開新對話都從零開始：它沒聽過你們的會議，也不知道上週大家同意用哪個名字。它能依靠的只有這次對話裡給它的內容，也就是上下文（context）。Anthropic 工程團隊 2025 年的文章說，上下文對 Agent 是關鍵但有限的資源；Birgitta Böckeler 2026 年在 martinfowler.com 也寫到，給太多上下文，Agent 的效果反而下降。

所以團隊的語言與邊界要寫成檔案、放進 Repo，而且要短、要經人確認。本 DLC 分兩處放：附證據、要核准的模型放在 domain-memory/；團隊自己的決定（選定的名字、不用的名字、邊界）每條一行，附出處，寫進專案根目錄 AGENTS.md 的「通用語言與邊界」。AGENTS.md 是給 Agent 看的專案說明，多數 Coding Agent 開新對話會自動讀它，下一個對話不必你重講，也會用同一個名字。換成 Repo 裡一份經過審查的 Markdown 詞彙表，道理相同。

常見誤解：把所有文件都丟給 Agent 就好。內容越多，重要的規則越容易被淹沒；寫得短、寫得準，比寫得多有用。回到工作：把團隊最常向新人解釋的三個名詞，各寫一行定義和不用的名字，放進 Repo 的 AGENTS.md。

📖 延伸閱讀：〈Effective context engineering for AI agents〉（Anthropic Engineering，2025）；〈Context Engineering for Coding Agents〉（Birgitta Böckeler／martinfowler.com，2026）；〈AGENTS.md〉（OpenAI，官方文件）

**人工確認**：你的專案裡，有沒有一個名詞，不同人說的意思不一樣？

## 4. 技巧：要證據，不要形容詞

請 Agent 做事前先講好：看到哪個實際字樣才算成功；回報對得上才往下。

- **要實際字樣**：例如「76 passed」，不是「看起來沒問題」。

- **只回成功或失敗**：確認時 Agent 只答一句，不順手修改。

Claude Code 官方文件建議讓 Agent 拿出證據，而不是只宣稱成功；其他工具的官方文件通常也有類似章節。「實際字樣」是工具真的印出來的文字，例如測試結果的「76 passed」；Agent 的轉述與形容都不算。

做 DDD 時更是如此：Agent 說「這兩個名詞是同一件事」，要附上它看到的那幾行原文，由你判斷。DLC 每個確認步驟都請 Agent 只回「成功」或「失敗」加一句原因，而且不順手修改；一邊檢查一邊修，你就分不清它到底檢查了什麼。

限制：實際字樣只證明那個指令跑過、結果是那樣，不證明測試寫得夠好。測試本身守不守得住規則，第 02 場會講。

📖 延伸閱讀：〈Best practices for Claude Code〉（Claude Code 官方文件）

**人工確認**：Agent 說「完成了」時，你看的是它的形容，還是實際輸出？

## 5. 通用語言：說的、寫的、程式都一樣

Ubiquitous Language（通用語言）：團隊在對話、文件與程式裡，用同一套名詞。

- **同一套說法**：會議上怎麼說，程式裡的名稱就怎麼取。

- **會跟著成長**：團隊越懂業務，語言和模型就跟著改。

通用語言是 DDD 的核心做法。Evans 要求同一套語言用在圖、文件，尤其是說話裡；Martin Fowler 2006 年的短文〈UbiquitousLanguage〉補充：語言和模型會隨團隊越懂業務而演進，不是定一次就不動。

Evans 的定義更精確：通用語言是以領域模型為骨幹、在一個 Bounded Context 裡全體成員共用的語言，用來把團隊的每一項工作接到軟體上。微軟的說法是開發者和領域專家一起建立。重點有二：它屬於某一個 Context，不是全公司一套；它要用在程式裡，不只是一份名詞表。

對 Agent 來說，程式裡的名稱是它最常讀到的語言。Three Dots Labs 的 Miłosz Smółka 在 2026 年 8 月的文章寫到：Agent 會在整個 Repo 裡找你給它的名字，也可能天真地把相似的實體合併。所以兩個看起來很像的名詞為什麼要分開，要寫下來。這是個人實作經驗，沒有數據。

課程裡的例子：Smart Ticket 有「訂票（Booking）」和「訂單（Order）」兩個很像的名詞。依需求卡的說明，Order 是付款成功後才建立的訂單，Booking 在付款前就存在。Agent 看到兩個相似名詞，可能想合併成一個；但它們的建立時機與規則不同，合併了，「付款失敗仍保留座位」這類規則就沒有地方放。這種差別要寫進詞彙表，連同「不要混用」一起寫。

下週可以找一個「客服這樣說、程式那樣寫」的名詞，先記下兩邊的說法和出處，不急著改程式；改名本身就是改模型，下一頁會講。

📖 延伸閱讀：〈UbiquitousLanguage〉（Martin Fowler，2006）；Eric Evans《Domain-Driven Design》（2003）第 2 章〈Communication and the Use of Language〉；〈Domain-Driven Design matters more when AI writes your code〉（Miłosz Smółka／Three Dots Labs，2026）

**人工確認**：說出一個「客服這樣說、程式卻那樣寫」的例子。

## 6. 改一個名詞，就是改模型

Evans：語言的改變就是模型的改變。所以 Agent 提的新名詞，先當候選。

- **候選**：附證據的主張，Agent 只能參考。

- **事實**：經另一個人核准後才成立（下一場）。

```text
詞彙：借閱（圖書館示意）
  不用的名字：借書、租借
  證據：docs/example.md:41-48
  狀態：候選
```

Evans 說：語言的改變就是模型的改變。所以 Agent 把「借書」改成「借閱」，不是改錯字，而是提議改模型。本課把 Agent 提出、附證據、還沒有人核准的主張叫「候選」；候選只能參考，不是必須遵守的規則。

DDD Europe 2026 的 Philipp Kostyra 主張把 LLM 當成「可以犯錯的初級領域專家」：它的意見值得聽，但要有人確認。看證據不需要看懂程式，只要問兩件事：那幾行真的在講這件事嗎？有沒有被斷章取義？

常見誤解：Agent 找得到證據就代表它對。證據只證明某處出現過這個說法，不證明這是團隊選定的說法；由誰、怎麼核准，下一場講。

這也是業界記錄決策的通用做法：架構決策紀錄（ADR）先標「提議」，同意後才標「接受」；本課的候選對應「提議」，第 02 場會把兩者對起來。課程裡的例子：Agent 提議把程式裡的 booking 和文件裡的「訂單」視為同一個詞，附上兩處出現的行號；它只是候選；上一頁說過兩者其實不同，這筆候選就該被退回，退回的理由也值得寫下來。

📖 延伸閱讀：〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Can AI be a Co-Domain Expert in Domain Modelling?〉（Philipp Kostyra／DDD Europe，2026）

**人工確認**：挑一筆候選，打開證據的那幾行：真的在講這件事嗎？

## 7. 案例：用 AI 讀懂舊系統

讓 AI 從舊程式整理業務規則，已是業界常見做法；共同點是最後由人驗證。

- **Thoughtworks 技術雷達**：把「用 AI 理解舊程式」列為建議採用。

- **Morgan Stanley（2025）**：先把舊程式轉成白話規格，再由工程師重寫。

- **COBOL 逆向工程（2024）**：AI 整理理解，仍請領域專家確認。

讓 AI 讀舊程式、整理業務規則，已是常見做法。Thoughtworks 技術雷達（Thoughtworks 定期發布的技術評估報告）把「用生成式 AI 理解舊程式碼」列為 Adopt（建議採用），最後一次出現在 2025 年 11 月。martinfowler.com 2024 年的文章介紹 Thoughtworks 的工具 CodeConcise：用 LLM 加上程式結構的知識圖譜理解 COBOL 舊系統，再由領域專家驗證理解是否正確；文中「逆向工程 1 萬行程式從約 6 週縮成約 2 週」是估計值，不是量測結果。

Business Insider 2025 年報導 Morgan Stanley 的內部工具：先把舊語言程式轉成白話英文規格，再由工程師重寫。報導中「截至 2025 年 6 月節省 28 萬小時以上」是公司自己說的，不是本課程量到的結果。

三個案例的共同點：AI 讓「讀」變便宜，但「這是不是真的業務規則」仍由人和懂業務的人判斷。回到團隊，可以先請 Agent 整理一個你熟悉的舊模組，看它說對多少，再決定要不要用在不熟的模組。

📖 延伸閱讀：〈Using GenAI to understand legacy codebases〉（Thoughtworks Technology Radar，2025）；〈Legacy Modernization meets GenAI〉（Ferri、Coggrave、Sheth／martinfowler.com，2024）；〈A team of engineers saved Morgan Stanley more than 280,000 hours this year〉（Business Insider，2025）

**人工確認**：這些案例裡，哪一步一定要人來做？

## 8. 示範：請 Agent 整理詞彙表

Agent 找名詞與證據；人決定標準名稱，並寫下「不要用的名字」。

- **人決定**：標準名稱、定義，以及哪些名字以後不用。

- **不要用的名字**：寫進詞彙表，Agent 下次才不會換回來。

### 交給 Agent 的指令

我們要統一這個模組的用詞。先找出同一件事有兩個以上名字、或文件有而程式沒有的名詞，素材是 docs/、src/ 和 tests/。給我一張表：名詞、各處說法、證據行號；標準名稱我來選。

這頁的指令示範分工：Agent 找出同一件事有幾個名字、各在哪裡出現；人決定標準名稱、寫定義，並寫下「以後不用的名字」。指令最後的「標準名稱我來選」是關鍵：選名字就是定義模型，定義是人的事。

為什麼要寫「不用的名字」：Agent 下次讀到舊程式裡的舊名稱，如果詞彙表沒說它已停用，就可能把舊名稱帶回新程式。Forte Group 2026 年一篇廠商文章的說法是「拒絕才是決定所在」；這是觀點，不是研究。

發現矛盾時（文件說 A、程式做 B），先記成發現，不要讓 Agent 偷偷修掉：哪一邊才對，是業務問題。這頁的提示詞是示範，沒有實際執行過。

一筆好的詞彙紀錄長這樣：名詞「可用點數」，定義「會員目前可以拿來折抵的點數」，不要用的名字列出程式裡曾出現的其他寫法，證據指到需求卡與程式的行號。定義用業務的話寫，不寫「points_balance 欄位」這類實作細節；欄位名稱放在證據裡就好。

**人工確認**：Agent 列的同義詞，你有沒有決定哪一個不用？

## 9. 小心：Agent 會編出合理的名字

Agent 會自信地說出不存在的名字；每個名詞都要附查得到的證據。

- **研究（2025）**：程式碼模型推薦的套件，商用模型至少 5.2% 不存在。

- **防法**：證據寫成路徑與行號，再請工具確認原文還在。

LLM 會自信地說出不存在的東西，稱為幻覺（hallucination）。2025 年 USENIX Security 研討會的論文測了 16 個程式碼生成模型：它們推薦的套件裡，商用模型平均至少 5.2%、開源模型 21.7% 根本不存在，總共出現 205,474 個不同的假套件名稱。

這是套件名稱，不是領域名詞，但道理相通：越像真的名字越難發現。防法是每個名詞都附「路徑:起-迄行」的證據，並請工具或另一個步驟確認那幾行原文還在、還在講同一件事。Böckeler 也記錄過，就算給了正確的上下文，Agent 也不一定照做，所以查證不能省。

引用數字時請回到論文摘要核對：摘要裡的比例就是上面兩個，看到其他比例（例如 19.7%）不要沿用。

一個實用的檢查：請 Agent 對每個名詞附「路徑:起-迄行」，再請另一個步驟只做一件事：打開那幾行，回報原文裡有沒有這個字。兩步分開，比讓同一個步驟「找完順便確認」可靠，因為查證的一方沒有替自己的答案辯護的動機。

📖 延伸閱讀：〈We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs〉（Spracklen 等人，USENIX Security 2025）

**人工確認**：Agent 提的名詞裡，有沒有一個在證據裡找不到？

## 10. Bounded Context：意思一致的範圍

Bounded Context（限界上下文）：一個模型適用的範圍；在範圍內，同一個名詞只有一種意思。

- **同字異義是邊界訊號**：「帳戶」在登入和帳務是兩件事。

- **不要硬統一**：大系統要一套全公司模型，既不可行也不划算。

Bounded Context（限界上下文）是一個明確的邊界，在邊界內有一個特定的模型被定義、也適用。Evans 的定義補了一句：這個邊界通常是一個子系統，或一個團隊負責的範圍。在範圍內，每個名詞只有一種意思。Martin Fowler 2014 年的短文以「客戶」「產品」為例：同一個詞，在不同部門可能指不同的東西。微軟 Azure 架構中心也用 account（帳戶）舉例，例如登入用的帳戶和帳務上的帳戶就是兩件事。

Bounded Context 和子領域不一樣：子領域是業務這一側的劃分（業務自然分成哪幾塊），Bounded Context 是解法這一側的劃分（哪個模型在哪裡適用）。理想上一個 Context 對應一個子領域，但舊系統常常不是；Azure 的寫法是「每個 Bounded Context 包含一個代表特定子領域的領域模型」。

Fowler 也說，大系統想要全公司只用一套模型，既不可行也不划算；與其硬統一，不如畫出邊界，在每個邊界內說清楚。對 Agent 而言，沒有標出邊界，它很容易把兩個「訂單」當成同一個，寫出把兩邊混在一起的程式。

實際做法：Agent 發現同一個字有兩種意思時，不要讓它合併成一個名詞，由人決定這是兩個不同的名詞，還是兩個 Context 的界線。常見誤解：一個 Context 不等於一個微服務、一個資料夾或一張資料表；它是語言與模型的邊界，程式怎麼部署是另一個決定。下週可以問問團隊：哪個詞一換部門，意思就變了？

📖 延伸閱讀：〈BoundedContext〉（Martin Fowler，2014）；Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 2 章〈Domains, Subdomains, and Bounded Contexts〉；〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026）

**人工確認**：你們公司哪個詞，換個部門意思就不一樣？

## 11. 交給 Agent 的順序：先語言，再邊界

請 Agent 分四步整理，每一步人確認過才往下；越後面的步驟，越依賴前面對不對。

語言 → 邊界 → 關係 → 規則與 Aggregate

- **Agent 較可靠**：找名詞、找誰呼叫誰：結果穩定、容易驗。

- **Agent 較不可靠**：劃邊界、定 Aggregate：一錯就往後擴散。

為什麼是這個順序：找名詞、找「誰呼叫誰」，程式裡有字面證據，結果穩定、容易驗；劃邊界、定 Aggregate 要綜合判斷，比較容易出錯。邊界一旦劃錯，之後每一條規則、每一個事件都會掛在錯的地方，越晚發現越難改。Aggregate 與規則第 03 場會講。

限制：「哪些步驟 Agent 比較可靠」是實務觀察，不是研究結論，沒有數字支持。回到團隊，把它當成安全的預設順序，而不是定律。

為什麼「關係」排在邊界之後、規則之前：Context Map 要先有 Context 才畫得出來；而一條規則掛在哪個 Context、要不要跨 Context 協作，又要先知道 Context 之間是什麼關係。每一步的產出都是下一步的輸入，所以每一步都要人確認後再往下。

**人工確認**：D1 裡，你是先定好名詞才劃邊界，還是一起做？

## 12. 邊界：多個訊號都指向同一處

語言在這裡改變、資料只在這裡寫入、變更一起發生、只透過明確介面往來：重疊越多，邊界越可信。

- **一個訊號不夠**：資料夾或服務名稱，本身不是邊界。

- **寧少勿多**：證據不夠就先不切，記成待確認。

四個訊號的證據來源不同：語言改變，看詞彙表與程式裡的名稱；資料寫入集中，看哪些程式會寫入這份資料；一起變更，看版本紀錄（下一頁）；明確介面，看跨模組的呼叫與事件。

一個訊號不夠：資料夾可能只是當初的習慣，服務名稱可能早已名不符實。請 Agent 為每個候選 Context 列出它找到哪些訊號、各附證據；只有一個訊號的，人要特別看。

寧可少切：證據不夠就先不切，記成待確認。切錯的邊界比沒切的更難修，因為之後的規則都會照著錯的邊界寫。

課程例子（只說訊號，不說答案）：如果「點數」這個字在會員相關的程式裡指餘額、在計價相關的程式裡指這次折抵的數量，這是「語言改變」的訊號；再看寫入點數餘額的程式是否只有一處、它們是否常一起修改、彼此是否只透過明確的函式往來。四個問題的答案指向同一處，才把邊界畫在那裡。

**人工確認**：你劃的 Context，有幾個訊號支持？只有一個的是哪個？

## 13. 一起變更：從版本紀錄找訊號

Tornhill 稱為 change coupling：常在同一次 commit 一起改的模組，彼此有看不見的依賴。

- **支持**：同一個候選 Context 裡常一起改。

- **質疑**：兩個 Context 總一起改：該合併或藏了約定？

- **例外**：組裝程式跟什麼都一起改，不算訊號。

### 交給 Agent 的指令

我想知道哪些模組其實綁在一起。從版本紀錄找出最近一年最常在同一次 commit 一起改的模組配對，給我前 10 名：配對、一起改的次數、各自被改的次數。組裝程式、設定檔這類跟什麼都一起改的標出來；邊界結論我來下。

一起變更（change coupling）是指兩個以上的模組，在一段時間內常常一起被修改。CodeScene 的文件這樣定義，並建議拿結果和你的架構原則對照。Adam Tornhill 在《Your Code as a Crime Scene》（第二版，2024）與《Software Design X-Rays》（2018）介紹這類分析，資料就來自團隊本來就有的版本控制紀錄（Git 的 commit 歷史）。

怎麼解讀：同一個候選 Context 裡常一起改，支持這條邊界；兩個不同 Context 總是一起改，要問是不是該合併，或兩邊共用一個沒寫下來的約定。組裝程式（把各模組接在一起的進入點）、設定檔、按技術分層的資料夾，跟什麼都一起改，不提供邊界資訊。

限制：一起變更只是訊號之一，不能「證明」哪裡是 Bounded Context；只看還存在的模組，歷史大改過的只看近期。練習 Repo 的歷史很短，不一定看得出來；你們團隊有一兩年歷史的 Repo 反而更適合試。

📖 延伸閱讀：〈Change Coupling: Visualize Logical Dependencies〉（CodeScene 文件）

**人工確認**：前 10 名裡，哪一對讓你懷疑自己劃的邊界？

## 14. 示範：用畫布寫清楚一個 Context

DDD Crew 的 Bounded Context Canvas：先用業務語言寫目的，不寫技術。

- **Agent 填**：名詞、業務決定，以及每一欄的證據。

- **人寫**：目的那一句，和要問專家的問題。

### 交給 Agent 的指令

我想把這個 Context 寫成一張 Bounded Context Canvas，給新同事看。先填草稿：目的、它做的業務決定、使用的名詞、假設、待確認問題，每欄附證據行號，找不到的寫「待確認」。目的給我 2 個選項，我來定。

Bounded Context Canvas（限界上下文畫布）是 DDD Crew（整理 DDD 工作坊工具的開源社群）提供的一張表，幫你把一個 Context 寫清楚。它的「目的」欄要求用業務語言寫幾句：這個 Context 為什麼存在、做什麼，不寫技術細節；其他欄位包括使用的名詞、它做的業務決定、假設與待確認問題。

分工：Agent 適合填名詞和業務決定，並為每欄附證據；目的那一句和要問專家的問題，由人寫。如果目的一定要用技術名詞才說得清楚（例如「處理 API 請求」），通常表示還沒想清楚這個 Context 負責什麼業務。

D1 只要求一句話職責，整張畫布是回到團隊後的延伸。下週可以挑一個熟悉的模組，用目的欄寫三句話，給一位非工程師的同事看懂不懂。

📖 延伸閱讀：〈The Bounded Context Canvas〉（DDD Crew）

**人工確認**：這個 Context 的目的，不用技術名詞也說得清楚嗎？

## 15. Context Map：上游與下游

Evans 的比喻：兩座城在同一條河邊，上游倒進河裡的東西，會流到下游。

上游 Context → 提供資料或服務 → 下游 Context → 跟著上游的變動改

- **先畫現況**：照實記下誰依賴誰，改造之後再說。

- **Agent 幫忙找**：誰呼叫誰、誰讀誰的資料，都附證據。

Context Map（上下文地圖）記錄各個 Context 之間怎麼接觸。Evans 的定義比「誰依賴誰」多：要為每個模型畫出 Context、取好名字，並寫出模型之間的接觸點，包括哪裡需要明確翻譯、哪裡共用、哪裡刻意隔離，以及誰影響誰。他的建議是先照實畫出現有地形，改造之後再說。

上游與下游是影響的方向，不是呼叫的方向。Evans 用河流比喻：上游城市倒進河裡的東西，會流到下游；上游的作為會影響下游成敗，下游的作為對上游影響不大。最常見的情況是下游呼叫上游提供的資料或服務，但用事件時，發出事件的上游並不呼叫誰。判斷時問：哪一邊改了，另一邊得跟著改？

DDD Crew 的〈Context Mapping〉把團隊之間的關係分成三種，再列出常見的關係名稱。上下游關係：Customer-Supplier（下游的需求排進上游的計畫）、Conformist（下游直接照用上游的模型）、Anticorruption Layer（防腐層，下游自己翻譯，第 03 場會講）、Open Host Service（上游開放一套給所有人用的介面）與 Published Language（雙方用一份有文件的共用格式交換）。互相依賴：Partnership（兩邊一起規劃、一起成功或失敗）與 Shared Kernel（兩邊明確共用一小塊模型，改之前要先商量）。各走各的：Separate Ways（刻意不整合）。名稱不必背，重點是看出誰會被誰的變動影響。

對照本 DLC 的工具：它把這些名稱記在兩個 Context 之間的一筆協作紀錄上，而且一律把提供的一方記成上游。這對上下游關係沒問題，但 Partnership 與 Shared Kernel 在 DDD Crew 的分類裡是互相依賴、沒有上下游；讀紀錄時要知道這是工具的簡化。Separate Ways 則不是一種協作，工具把它記成「禁止依賴」的規則。Shared Kernel 也不是一種 Context，是兩個 Context 之間的關係。

Agent 很適合找「誰呼叫誰、誰讀誰的資料」，因為程式裡有字面證據；請它每一筆附出處，再由人判斷哪些依賴是設計好的、哪些是不知不覺長出來的，以及它屬於哪一種關係。

📖 延伸閱讀：〈Context Mapping〉（DDD Crew）；Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 3 章〈Context Maps〉

**人工確認**：你的系統裡，哪個模組一改，別人就得跟著改？

## 16. 邊界洩漏：測試抓不到的錯

一個 Context 繞過約定，直接讀寫另一個的資料；測試常常全過，只能靠人看。

- **真的越界**：程式該改，經核准後再做。

- **模型漏寫**：補一條 Context 之間的協作。

### 交給 Agent 的指令

我懷疑有 Context 繞過約定，直接讀寫別人的資料。對照模型裡的 Context 和它們的協作，列出可疑的地方：證據行號、模型怎麼說、程式怎麼做。是越界還是模型漏寫，我來判斷。

邊界洩漏是指一個 Context 繞過約定好的介面，直接讀寫另一個 Context 的資料或內部程式。例如計價程式直接去改會員資料：金額算對、測試全過，但兩個 Context 從此綁在一起，之後改會員規則就可能悄悄弄壞計價。

這種錯測試通常抓不到，因為功能結果是對的，需要人對照模型看。微軟 Azure 架構中心提醒，外部或舊系統的資料結構與 API 很容易滲進新程式。Agent 可以列出可疑處並附證據，但結論有兩種：真的越界（程式該改，核准後再改），或模型漏寫了一條合理的協作（補進模型）。兩種後續不同，所以由人判斷。

在沒有自動架構檢查的 Repo，這類問題只能靠審查發現；第 03 場會講怎麼讓 Agent 在每次變更後都查一次。

課程例子（虛構，不在練習 Repo 裡）：計價程式為了算折扣，直接把會員的點數餘額減掉。功能看起來對、測試也過，但「點數不得為負」這條規則從此有兩個地方在改，任何一邊漏了檢查，另一邊都不知道。看到這種寫法，要問的不是「能不能動」，而是「這份資料歸誰管、別人該透過什麼約定取用」。

📖 延伸閱讀：〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026）

**人工確認**：你判斷的那一處，理由是看了證據，還是聽了 Agent 的結論？

## 17. 帶走什麼

Agent 找證據、人來定義；寫下來的都是候選，等另一個人核准。

人選來源 → Agent 先整理語言 → 人定義語言與邊界 → 人判斷洩漏 → 另一個人核准

- **回到團隊**：從一個常被說錯的名詞開始，寫進 Repo。

- **下一場**：審查與核准：候選怎麼成為必須遵守的事實。

**人工確認**：回到第一頁你最沒把握的決定：它的證據是哪幾行？

## 完成條件
說得出 DDD 的三句話、為什麼 Agent 需要寫在 Repo 裡的共用語言、候選和事實差在哪；知道為什麼要讓 Agent 先整理語言、再劃邊界，邊界要多個訊號（包括版本紀錄裡的一起變更）都指向同一處；知道怎麼請 Agent 從文件與程式整理詞彙表與 Context 畫布、怎麼防 Agent 編出不存在的名字，以及邊界洩漏要由人看證據判斷；知道下一場要讓另一個人審查核准。

## 下週可以做的事
- 挑一個團隊最常被說錯的名詞，寫一句定義和「不要用的名字」，請懂業務的同事確認。
- 請 Agent 列出一個你熟悉模組裡的同義詞與證據，親自打開幾行證據核對。
- 拿一個有一兩年歷史的 Repo，請 Agent 列出最常一起修改的模組，對照你心中的邊界。

## 名詞解釋
| 名詞 | 意思 | 出處 |
|---|---|---|
| DDD（Domain-Driven Design，領域驅動設計） | 聚焦核心領域、和領域專家一起探索模型、在明確邊界內說通用語言的軟體開發方法。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 領域（domain） | 使用者把軟體用在哪一塊知識或活動，例如訂票、退票。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 模型（model） | 挑出領域的某些面向、能用來解決這個領域問題的一套抽象；不是一張圖，而是團隊的共同理解。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 子領域（subdomain）：核心／支援／通用 | 業務裡相對獨立的一塊。核心讓公司與眾不同、最值得投入；支援是業務需要但不構成差異；通用是業界已有現成做法。 | 〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026） |
| 領域專家 | 真正懂這門業務的人，例如櫃檯、法遵、產品負責人；模型要和他們一起建立。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 通用語言（Ubiquitous Language） | 以模型為骨幹、在一個 Bounded Context 內全體成員共用的語言；說的、寫的、程式裡都用同一套。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈UbiquitousLanguage〉（Martin Fowler，2006） |
| Bounded Context（限界上下文） | 一個特定模型被定義、也適用的明確邊界，通常是一個子系統或一個團隊負責的範圍；範圍內每個名詞只有一種意思。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈BoundedContext〉（Martin Fowler，2014） |
| 候選 | 本課用語：Agent 提出、附證據、還沒有人核准的主張；只能參考，對應 ADR 的「提議」。 | 〈Documenting Architecture Decisions〉（Michael Nygard，2011） |
| 一起變更（change coupling） | 兩個以上的模組在一段時間內常常一起被修改；是邊界訊號之一，不是證明。 | 〈Change Coupling: Visualize Logical Dependencies〉（CodeScene 文件） |
| Bounded Context Canvas（限界上下文畫布） | 把一個 Context 寫清楚的表格：目的、策略分類、使用的名詞、業務決定、假設、待確認問題等欄位。 | 〈The Bounded Context Canvas〉（DDD Crew） |
| Context Map（上下文地圖） | 記錄各個 Context 之間的接觸點：誰影響誰、哪裡要翻譯、哪裡共用、哪裡隔離。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Context Mapping〉（DDD Crew） |
| 上游／下游 | 上游的作為會影響下游的成敗，反過來影響不大；判斷看「誰改了，另一邊得跟著改」，不是看誰呼叫誰。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| Shared Kernel（共用核心） | 兩個 Context 明確約定共用的一小塊模型與程式；要保持小，改之前要和對方商量。是兩個 Context 之間的關係，不是一種 Context。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Context Mapping〉（DDD Crew） |
| Separate Ways（各走各的） | 刻意讓兩個 Context 完全不整合，各自找簡單的解法；它是「不協作」的決定。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 邊界洩漏 | 本課用語：一個 Context 繞過約定，直接讀寫另一個 Context 的資料或內部程式；外部系統的資料結構滲進來也是。 | 〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026） |

## 延伸閱讀
- 〈Domain-Driven Design Reference〉（Eric Evans，2015）
- 〈Use Domain Analysis to Model Microservices〉（Microsoft Azure Architecture Center，2026）
- 〈Opening Keynote Eric Evans〉（DDD Europe，2026）
- 〈Accelerate your Strategic Design with LLMs〉（Thomas Coopman／DDD Europe，2026）
- 〈The Curse of Unbounded Contexts: Using Domains as LLM Consumers〉（Chelsea Troy／DDD Europe，2026）
- 〈Eric Evans Encourages DDD Practitioners to Experiment with LLMs〉（InfoQ，2024）
- 〈Effective context engineering for AI agents〉（Anthropic Engineering，2025）
- 〈Context Engineering for Coding Agents〉（Birgitta Böckeler／martinfowler.com，2026）
- 〈AGENTS.md〉（OpenAI，官方文件）
- 〈Best practices for Claude Code〉（Claude Code 官方文件）
- 〈UbiquitousLanguage〉（Martin Fowler，2006）
- Eric Evans《Domain-Driven Design》（2003）第 2 章〈Communication and the Use of Language〉
- 〈Domain-Driven Design matters more when AI writes your code〉（Miłosz Smółka／Three Dots Labs，2026）
- 〈Can AI be a Co-Domain Expert in Domain Modelling?〉（Philipp Kostyra／DDD Europe，2026）
- 〈Using GenAI to understand legacy codebases〉（Thoughtworks Technology Radar，2025）
- 〈Legacy Modernization meets GenAI〉（Ferri、Coggrave、Sheth／martinfowler.com，2024）
- 〈A team of engineers saved Morgan Stanley more than 280,000 hours this year〉（Business Insider，2025）
- 〈We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs〉（Spracklen 等人，USENIX Security 2025）
- 〈BoundedContext〉（Martin Fowler，2014）
- Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 2 章〈Domains, Subdomains, and Bounded Contexts〉
- 〈Change Coupling: Visualize Logical Dependencies〉（CodeScene 文件）
- 〈The Bounded Context Canvas〉（DDD Crew）
- 〈Context Mapping〉（DDD Crew）
- Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 3 章〈Context Maps〉
