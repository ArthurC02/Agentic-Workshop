# 用 Agent 做領域設計：不變量、邊界與舊系統

> 讀者：學員。時機：DDD 延伸課 D3a–D3c 之後的 40 分鐘講解。前置：已聽過 DLC Speech 01、02，做完 D3 三段。

**這一段帶走什麼**
- 不變量、Aggregate、領域事件各解決什麼問題，以及怎麼用「是／不是」檢查 Agent 提的概念
- Port／Adapter 與防腐層讓外部說法不滲進領域程式；冪等處理「逾時是不知道」
- 交給 Agent 的方式：先列不變量與證據，Agent 提選項，人來選
- 測試會綠不代表規則有人守；搬程式不等於改模型

每頁最後的段落是講解時來不及說的補充：概念的白話解釋、證據出處、限制與回到團隊的做法；提到的書與文章列在最後的「延伸閱讀」。

本場講概念與技巧，不需要寫程式或打指令。頁面上的提示詞是示範，想試再貼給自己的 Agent；沒有實際執行的結果，一律視為未驗證。案例數字都是該公司自己說的，本工作坊沒有量測效率。本場不公布三張需求卡的參考設計。

## 1. 用 Agent 做領域設計，人守什麼

D3 做了三個新需求。這一場把背後的 DDD 概念講清楚，再看業界怎麼讓 Agent 照著領域模型寫程式。

- **今天的概念**：不變量、Aggregate、領域事件、Port 與防腐層。

- **今天的做法**：交給 Agent 的指令，以及人要確認什麼。

- **今天的案例**：2025–2026 年的舊系統現代化做法。

**人工確認**：D3 三段裡，哪一個決定你們吵最久？最後靠什麼定案？

## 2. 先有模型，Agent 才寫得對

第 01 場說過 Agent 沒有走廊記憶；加深一層：做設計時，需求講不清楚，它就自己下結論。

- **Agent 常見的錯**：沒講清楚的規則，它會補一個看起來合理的。

- **模型提供什麼**：名詞、規則、邊界寫下來，Agent 才有依據。

- **人保留什麼**：哪條規則成立、歸誰負責，由人決定。

Birgitta Böckeler 2025 年在 martinfowler.com 記錄自己用 Agent 寫程式的觀察：沒有詳細描述功能需求時，AI 會跳到錯誤的結論，而且常一次做很廣，而不是一小段一小段做出能用的功能。這就是先建共用模型、再讓 Agent 寫程式的理由：名詞、規則、邊界寫下來，Agent 才有依據，不必自己補。

分工很清楚：模型提供 Agent 依據；哪條規則成立、歸哪個 Bounded Context（限界上下文：名詞意思一致的範圍）負責，仍由人決定。Agent 自己補的每一條規則，都是一條沒人核准的規則。

下週可以檢查最近交給 Agent 的一件工作：產出裡有沒有一個數字、狀態或判斷，是你沒給、它自己補的？

這也是 DDD 和 Agent 最直接的連結：Evans 說模型是「挑出領域的某些面向、能用來解決問題的一套抽象」。Agent 沒有這套抽象，就只能從程式的表面形狀猜；交給它的模型越明確，它猜的空間越小。限制：模型寫了不代表 Agent 照做，第 04 場會講怎麼查證。

📖 延伸閱讀：〈The role of developer skills in agentic coding〉（Birgitta Böckeler／martinfowler.com，2025）

**人工確認**：你最近交給 Agent 的工作，有沒有一條規則是它自己補的？

## 3. 不變量：c 一定等於 a + b

Invariant（不變量）是每次操作完成時都必須成立的業務規則。Vernon 的例子：a 是 2、b 是 3，c 就必須是 5。

改了 a 或 b → 同一次操作裡重算 c → 結束時 c = a + b

- **寫得好**：說得出怎樣算失敗：c 不等於 a + b。

- **寫不好**：「金額要正確」：沒辦法判斷何時失敗。

不變量（Invariant）是每次操作完成時都必須成立的業務規則。Vaughn Vernon 2011 年的〈Effective Aggregate Design〉用最小的例子說明：c 必須等於 a + b；a 是 2、b 是 3，c 就必須是 5。只要 a 或 b 改了，c 必須在同一次操作裡跟著改，否則規則就被破壞。換成業務語言：訂單總額等於各明細小計加總。

「每次操作完成時」比「任何時候」準確：Vernon 說，談不變量時指的是交易一致性，也就是一次操作提交時就必須成立、全有或全無；操作進行到一半，資料可以暫時不一致。也因此，不是每條業務規則都是不變量。有些規則允許晚一點才成立，例如「付款成功後寄出通知」，可以用事件在事後完成，這叫最終一致（eventual consistency）。Vernon 的規則名稱「在一致性邊界內建模真正的不變量」，「真正的」就是提醒：只有必須立即成立的規則，才拿來決定哪些資料要放在同一個 Aggregate。

判斷一條不變量寫得好不好，只問一題：說得出它失敗的樣子嗎？「c 不等於 a + b」可以判斷；「金額要正確」沒辦法判斷何時失敗。說不出失敗樣子的規則，Agent 也寫不出會失敗的測試。

課程裡的例子：需求卡 03 寫明，團體訂票在任何時刻都要滿足「已退款金額加總 + 已收手續費加總 + 有效旅客票價加總 = Order 金額」，這就是一條 c = a + b 型的不變量（卡上的「任何時刻」，指任何一次操作完成後去查都要成立）；需求卡 02 的「會員可用點數不得為負」也是。這兩條都說得出失敗的樣子：等式兩邊對不上、餘額出現負數。由哪個 Aggregate 守、和誰放在同一個邊界，是 D3 由你們做的決定。

對 Agent 更要緊的原因：Agent 會照它看到的程式路徑補判斷，多一條路徑就可能少一次檢查。不變量寫成一句「怎樣算違反」，它才能對每一條路徑寫出同一個會失敗的測試。下週可以從團隊的需求文件挑一條規則，改寫成「怎樣算違反」的一句話，再問 Agent 現有測試裡有沒有一個會在違反時失敗。

📖 延伸閱讀：〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011）；Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 10 章〈Aggregates〉

**人工確認**：挑一條你們寫的不變量：怎樣算它被破壞了？

## 4. Aggregate：訂單和它的明細

Aggregate（聚合）是一組必須一起保持一致、可以當成一個單位處理的資料。Fowler 的例子：訂單和它的明細行。

- **唯一入口**：外界只拿得到訂單（根），不能直接改某一行明細。

- **一起成立**：入口先檢查全部規則，再一次寫入。

Aggregate（聚合）是一組必須一起保持一致、可以當成一個單位處理的資料。Martin Fowler 2013 年用訂單和它的明細行舉例：明細是分開的物件，但和訂單當成一個單位處理。Evans 的定義再加一條：每個 Aggregate 選一個物件當根，外界只能持有根的參照，不能直接碰內部的明細；規則由根負責守住。

Aggregate 和 Aggregate root 是兩件事：Aggregate 是整個一致性邊界，裡面可能有好幾個物件；Aggregate root（聚合根）是邊界裡唯一對外的入口物件，例如「訂單」這個 Aggregate 的根是訂單本身，明細行在邊界內。Aggregate 也可以只有根一個物件：微軟 Azure 架構中心 2026 年的版本特別註明，讓它成為 Aggregate 的是交易邊界，不是子物件的數量。

邊界裡的物件分兩種：Entity（實體）有自己的識別碼，屬性改了仍是同一個，例如一筆訂票；Value Object（值物件）沒有識別碼，只由值決定、建立後不改，例如「新台幣 700 元」這個金額。根一定是 Entity。

為什麼要唯一入口：「訂單總額等於明細加總」這條不變量，只能由同一個入口守住。入口先檢查全部規則，再一次寫入；如果 Agent 另外寫了一條路徑直接改明細，總額就可能和明細對不上，而每條路徑各自看起來都沒錯。

常見誤解：Aggregate 不是資料表，也不是「有子物件的類別」；沒有一條要一起守的不變量，就不需要 Aggregate。一個 Aggregate 也只屬於一個 Bounded Context（Vernon《Implementing Domain-Driven Design》第 10 章）。審查 Agent 的設計時，可以請它對每個 Aggregate 回答兩題：根是哪個物件？它守住哪一條不變量？答不出第二題的，多半只是資料分組。

📖 延伸閱讀：〈DDD_Aggregate〉（Martin Fowler，2013）；〈Domain-Driven Design Reference〉（Eric Evans，2015）

**人工確認**：如果有人能直接改明細，訂單總額的規則還守得住嗎？

## 5. Aggregate 要小：無人機外送

只放必須在同一次交易裡一致的資料；其他 Aggregate 用 id 參照，邊界外的資料事後同步。

外送只存無人機 id → 外送完成：發出事件 → 帳務收到後開發票

- **為什麼要小**：越大越容易同時被改，也越難一起成功。

- **經驗法則**：服務不小於一個 Aggregate，不大於一個 Bounded Context。

Aggregate 要小：只放必須在同一次交易裡一致的資料。微軟 Azure 架構中心的無人機外送範例：外送（Delivery）不直接持有無人機物件，只記無人機的 id；外送完成時發出「外送已完成」事件。Evans 的摘要說：邊界內同步套用一致性規則，跨邊界則非同步（事後）處理。

這個例子還有一層：外送屬於配送 Context，開發票屬於帳務 Context。Azure 2026 年的版本把跨 Context 送出的「外送已完成」稱為整合事件（integration event）：在原本的交易提交後，經訊息系統非同步送出，帳務 Context 收到後才開發票。同一個 Context 裡、在 Aggregate 之間傳的叫領域事件；兩者都是「已經發生的事」，下一頁再分。

為什麼要小：Aggregate 越大，越容易被兩個人同時修改而衝突，一次要一起成功的東西也越多。Vernon 的經驗法則是一次交易只改一個 Aggregate；Azure 的經驗法則：一個服務不小於一個 Aggregate、不大於一個 Bounded Context。

取捨由人做：哪些資料一定要全有或全無、哪些可以晚一點同步，是業務問題，不是技術偏好。Azure 的領域事件說明也這樣寫：一個操作需不需要跨 Aggregate 的單一交易，要由領域專家判斷。可以請 Agent 列出每份資料「如果晚一點才一致，會發生什麼事」，再由懂業務的人決定。

常見誤讀：「事後同步」不是「可以不一致」。放寬即時一致時，要說得出多久內會一致、送丟或重複送到時怎麼補救；說不出來，就表示這份資料其實該留在同一個邊界裡。

📖 延伸閱讀：〈Use Tactical DDD to Design Microservices〉（Microsoft Azure Architecture Center，2026）；〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011）

**人工確認**：你們的邊界裡，有沒有一份資料其實可以事後再同步？

## 6. 領域事件：領域專家在乎的事

「資料表多了一列」不是領域事件；「外送取消了」才是。用過去式寫，懂業務的人一聽就懂。

- **找事件的方法**：EventStorming：橘色便利貼寫事件，照時間排。

- **跨邊界同步**：邊界外的資料，靠事件事後更新。

- **交給 Agent**：請它從程式列出事件，人刪掉技術動作。

領域事件（Domain Event）是「領域專家在乎的、已經發生的事」，用過去式寫。Evans 的定義就是這句話；Azure 用一組對比說明：「資料表多了一列」不算，「外送取消了」才算。判斷方法：懂業務、不懂程式的人一聽就懂，而且會在乎。Evans 也說，領域事件記的是過去，通常不再修改，並帶著發生時間與相關的 id。

找事件的工作坊方法之一是 EventStorming（事件風暴），Alberto Brandolini 2013 年提出：大家用橘色便利貼寫領域事件，貼在長紙卷上照時間排。今天只借它的規則：過去式、業務語言。領域事件也是跨 Aggregate 同步的方式：邊界外的資料，收到事件後再更新。

領域事件和整合事件（integration event）要分開想。微軟的說明是：兩者在意義上一樣，都是「剛發生了什麼」；差在用途。領域事件在同一個 Context 裡通知其他 Aggregate，通常在同一個程式內處理；整合事件把已提交的結果傳給其他 Context 或外部系統，一定是非同步送出，而且只在交易成功提交後才發。各家用詞不完全一致：Evans 的參考資料把分散式系統裡傳遞的事件也叫領域事件；本 DLC 的工具把「跨 Context、有消費者的已提交業務事件」記成一筆事件紀錄。審查時不必爭名稱，要問清楚三件事：誰負責發出、誰會收到、只在提交後才發嗎？

對 Agent 的意義：跨 Context 的事件一發出去，就成了對方依賴的約定；Agent 改欄位名稱或發出時機，等於改約定。而且整合事件可能重複送到，接收端要能冪等處理（後面會講）。課程例子：「訂票已付款」是業務在乎的事；「booking 表更新了 status 欄位」不是。

交給 Agent 時，先請它從程式與紀錄列一版事件，人刪掉「已儲存」「已呼叫 API」這類技術動作。常見錯誤是把每個資料庫操作都當成事件。

📖 延伸閱讀：〈Introducing Event Storming〉（Alberto Brandolini，2013）；〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Use Tactical DDD to Design Microservices〉（Microsoft Azure Architecture Center，2026）；〈Domain events: Design and implementation〉（Microsoft .NET 架構指南）

**人工確認**：Agent 列的事件裡，有沒有一個其實只是技術動作？

## 7. 定義要寫「是什麼」，也寫「不是什麼」

Agent 最常把相近的東西當成這個概念；給它判斷用的定義時，連同「不是」一起給。

- **Aggregate**：是：根守住不變量的一致性邊界；不是：資料表。

- **規則**：是：能被推翻的敘述；不是：測試名稱。

- **領域事件**：是：提交後業務在乎的事；不是：技術通知。

### 交給 Agent 的指令

送審前幫我篩一次這次的 Aggregate、規則與領域事件候選。標準：Aggregate 是由一個根守住至少一條不變量的一致性邊界，不是資料表；規則是能被推翻的敘述，不是測試名稱；領域事件是提交後業務在乎的事，不是技術通知。不符合的標出來寫理由，先不要改。

給 Agent 判斷用的定義，要同時寫「是什麼」和「不是什麼」，因為 Agent 最常犯的錯，是把相近的東西當成這個概念。前三頁可以收成一張表：Aggregate 是由一個根守住至少一條不變量的一致性邊界，不是資料表；規則是說得出怎樣算違反的敘述，不是測試名稱；領域事件是業務在乎、已經發生的事，不是技術通知。

這張表也是給人自己用的：Aggregate 的定義性質是「有一條必須在同一次操作裡成立的不變量」，不是「有子物件」；規則的定義性質是「說得出怎樣算違反」；領域事件的定義性質是「已經發生、業務在乎」。三個「不是」正好是 Agent 最常提交的近似品：一張資料表、一個測試名稱、一個「已儲存」通知。

測試名稱只是線索，真正的證據是會在規則被違反時失敗的測試。看起來像、但缺少定義性質的候選，寧可不記，或只記成較弱的概念（例如一個名詞）。第 01 場說過 Agent 定 Aggregate 較不可靠，這張表就是人審查時的標準。

回到工作：把這張「是／不是」表寫進團隊的 AGENTS.md，每次整理模型都用同一套標準，提示詞也不必每次重貼定義。

**人工確認**：D3 的候選裡，有沒有一個其實落在「不是」那一欄？

## 8. 交給 Agent：先列不變量，再提邊界

請 Agent 把不變量和放寬時的補救方式並列，提兩個邊界選項，人來選。

- **證據來自事實**：選項要指到模型或程式，不是 Agent 的偏好。

- **回覆很短**：「選 A」；想混合就直接說。

### 交給 Agent 的指令

這個功能動手前，我想先選邊界。依需求文件與共用模型列出每條不變量，各寫一句怎樣算失敗；再給我 A、B 兩個一致性邊界選項：哪些資料一起改、哪些事後同步、放寬時怎麼補救，每點附行號或模型 id。我來選。

DDD Crew（整理 DDD 工作坊工具的開源社群）的〈Aggregate Design Canvas〉（聚合設計畫布）把「不變量」和「修正政策」放在同一張畫布上。修正政策是指：放寬即時一致時（例如允許晚一點同步），出錯了怎麼補救。原文說，兩者並列能讓設計的取捨看得見。

這頁的指令就是請 Agent 先填這兩欄，再提兩個邊界選項，各寫哪些資料一起改、哪些用事件事後同步、出錯怎麼補救，每點附證據；人只做選擇，回「選 A」或說想怎麼混合。這是主課「比較方案」的加深：比較的依據換成已審查的模型，而不是 Agent 的偏好。

限制：Agent 提的兩個選項不代表只有兩種可能；看完覺得都不對，可以請它再提，或自己描述第三種。

課程例子：需求卡 02 的點數折抵，至少有「可用點數不得為負」「合計預留不得超過原可用點數」兩條要同時成立的規則；兩個訂票請求同時扣同一份點數時，哪些資料必須在同一次操作裡一起檢查、哪些可以事後同步，就是邊界選項要回答的問題。Agent 提的 A、B 兩案，要各自說得出這兩條規則在同時送出時怎麼守住。

📖 延伸閱讀：〈Aggregate Design Canvas〉（DDD Crew）

**人工確認**：每條不變量都說得出失敗的樣子嗎？選項的取捨你看得懂嗎？

## 9. Port／Adapter：插座規格與轉接頭

Port 用自己的業務用語說「我需要什麼」；Adapter 把它翻成外部服務的格式。

領域程式 → Port（自己的用語） → Adapter（翻譯） → 外部服務

- **原始用意**：人、程式、測試都能用同一種方式驅動系統。

- **好處**：換服務商、用假服務測逾時，只動 Adapter。

Port／Adapter 出自 Alistair Cockburn 2005 年的〈Hexagonal Architecture〉（六角形架構）。Cockburn 的定義：一個 Port 代表一段「有目的的對話」，由應用程式用自己的話定義；Adapter 負責把這段對話轉成某個外部技術或裝置需要的格式。原始用意：讓應用程式能同樣地被使用者、其他程式、自動測試或批次腳本驅動，並能和資料庫、外部裝置分開開發與測試。

Port 有兩種方向。驅動應用程式的一側（primary／driving），例如使用者介面、API、自動測試從這裡呼叫進來；被應用程式驅動的一側（secondary／driven），例如資料庫、發票服務，是程式需要外界提供的能力。投影片與 D3a 講的「用業務用語說我需要什麼」是後一種；卡片上的「人、程式、測試都能驅動」是前一種。兩種都是 Port。

比喻（本課的說法，不是原文）：Port 是你家插座的規格，Adapter 是出國用的轉接頭。好處：換服務商、或用假服務測試逾時，只動 Adapter，領域程式不變。對 Agent 也有用：它改外部串接時，影響範圍被限制在 Adapter。

課程例子：需求卡 01 的發票服務商「可能變慢、逾時或停機」。如果領域程式裡寫滿服務商的欄位名與錯誤碼，換服務商或測逾時都得動到業務邏輯；用自己的話描述「開立發票」這個需要，測試時接一個會逾時的替身，就能在不連外的情況下驗證逾時處理。要不要這樣做、Port 叫什麼，是 D3a 由你們決定的。

判斷訊號：領域程式裡出現外部服務的欄位名稱或錯誤碼，代表外部的說法已經滲進來。常見誤讀：Port 不等於「每個類別都要配一個介面」；只有一種實作、也不需要替身測試的地方，多一層介面只是多一層間接。要不要為某個外部服務定義 Port，是設計取捨，由人決定。

📖 延伸閱讀：〈Hexagonal Architecture〉（Alistair Cockburn，2005）；Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 4 章〈Architecture〉

**人工確認**：領域程式裡，有沒有出現外部服務的欄位名稱？

## 10. 防腐層：翻譯官只翻譯

Anticorruption Layer（防腐層）是下游自己蓋的翻譯層，讓外部系統的說法不滲進自己的模型。

- **只翻譯**：不放業務規則，也不負責流程編排。

- **有成本**：多一層呼叫與維護；舊系統遷移時要決定留多久。

- **也可以不蓋**：外部模型夠好時，直接照用也是一種選擇。

防腐層（ACL，Anticorruption Layer；不是存取控制清單）是下游自己蓋的翻譯層：用自己領域模型的說法，提供上游系統的功能，讓外部系統的說法不滲進自己的模型。這是 Evans 的定義。

放在 Context Map 裡看：防腐層是下游保護自己的做法，上游通常不用改。Evans 寫明這一層透過對方現有的介面溝通，「很少或不需要修改對方系統」，並視需要在兩個模型之間單向或雙向翻譯。對 Agent 的提醒：它在翻譯層順手加「金額小於 0 就拒絕」這類判斷，看起來很周到，其實是把業務規則放錯地方；規則該留在自己的領域程式，翻譯層只做格式與代碼的對應。

微軟 Azure 架構中心的〈Anti-Corruption Layer Pattern〉（2026 年 5 月更新）有兩個提醒：不要在這一層放業務規則或流程編排，它只翻譯；它也會增加兩個系統之間的延遲，多一個要維護的元件。舊系統遷移時，要決定它是永久保留還是過渡用。

也可以不蓋：外部模型夠好時，直接照用也是一種關係，叫 Conformist（跟隨上游模型）。防腐層是付出成本換隔離，不是免費的好東西。審查時可以問 Agent：這一層裡有沒有藏著一條業務規則？

📖 延伸閱讀：〈Anti-Corruption Layer Pattern〉（Microsoft Azure Architecture Center，2026）；〈Context Mapping〉（DDD Crew）；Eric Evans《Domain-Driven Design》（2003）第 14 章〈Maintaining Model Integrity〉

**人工確認**：你們的翻譯層裡，有沒有藏著一條業務規則？

## 11. 冪等：逾時是「不知道」

Idempotency（冪等）：同一個請求送很多次，效果和送一次一樣。外部服務逾時，你不知道它到底收到沒有。

- **為什麼需要**：逾時後重送，最怕多開一張、多扣一次。

- **人要確認**：重送與同時送出，結果都只算一次。

冪等（Idempotency）是指同一個請求送很多次，產生的效果和送一次一樣。為什麼需要：呼叫外部服務逾時，你不知道對方到底有沒有收到；逾時不是成功、也不是失敗，而是「不知道」。這時只能重送，而重送最怕多開一張單、多扣一次款。

權威定義有兩個常用版本。HTTP 標準 RFC 9110 說：同一個方法的多次相同請求，對伺服器的預期效果和送一次相同，就是冪等。Gregor Hohpe 與 Bobby Woolf 的《Enterprise Integration Patterns》（2003）把能安全處理重複訊息的接收端稱為 Idempotent Receiver（冪等接收者）。兩者講的都是「效果」只發生一次，不是「回應」每次都一模一樣：第二次可以回「已經處理過」。

做法通常是一個穩定的鍵。需求卡 01 的「商家訂單編號」就是這種鍵：服務商用它判斷是否重複開立。外部服務的回應因此不能只分成功與失敗，至少還要有「不知道」這一類，再用同一個鍵重送。

常見誤讀：冪等只保證重送安全，不保證兩個請求「同時」送進來也只算一次；同時送出要另外靠鎖或唯一性檢查。Agent 很容易只寫「成功」「失敗」兩種分支。審查時請它說明：逾時那一條怎麼處理？同一個請求重送或同時送出兩次，結果算幾次？

📖 延伸閱讀：Gregor Hohpe & Bobby Woolf《Enterprise Integration Patterns》（2003）〈Idempotent Receiver〉；IETF〈RFC 9110 HTTP Semantics〉

**人工確認**：逾時後重送，你怎麼知道對方沒有處理兩次？

## 12. 交給 Agent：外部說法有沒有滲進來

固定規則抓結構，Agent 補看語意；Agent 只回報，改不改由人決定。

- **為什麼請 Agent**：名稱換了寫法，固定規則就抓不到。

- **人來決定**：每筆看行號，再決定改不改。

### 交給 Agent 的指令

這次變更後，確認一下外部服務的說法有沒有滲進領域程式：Adapter 以外有沒有外部的欄位名稱、錯誤碼或資料格式，每筆附行號、該由哪一層翻譯。Adapter 裡像業務規則的判斷也列出來。改不改我決定。

外部說法有沒有滲進領域程式，可以兩種方式一起查：固定規則的架構檢查工具（例如 ArchUnit）抓結構上的依賴，Agent 補看語意，例如名稱換了寫法、固定規則就抓不到的情況。Thoughtworks 技術雷達第 34 期把「用 LLM（大型語言模型）減少架構漂移」列為 Assess（評估中），說兩者合用能同時發現結構與語意上的違規，也提醒 Agent 的修正要小、要有驗證迴圈。

這是第 01 場「邊界洩漏」的加深：從找一次，變成每次變更後都查一次。Agent 只回報，改不改由人看行號決定；也請它列出 Adapter 裡看起來像業務規則的判斷，因為翻譯層不該放規則。

限制：Assess 表示還在評估，不是成熟做法；Agent 的回報可能漏報或誤報，每筆都要對照它指的那一行。

📖 延伸閱讀：〈Architecture drift reduction with LLMs〉（Thoughtworks Technology Radar，2026）

**人工確認**：表裡每一筆，你都對照過它指的那一行嗎？

## 13. 測試會綠，不代表規則有人守

第 02 場看過：Agent 可能改測試配合程式。加深一層：每條不變量都要故意改壞一次，看測試抓不抓得到。

- **killed**：這條規則有測試守著。

- **survived**：補一個會失敗的測試，不換較好抓的改法。

### 交給 Agent 的指令

我想確認每條不變量都有測試守著。每條用 counterfactual 各做一次反事實檢查，回報 killed 或 survived；survived 的不要換改法，告訴我缺哪個測試。

第 02 場講過兩件事：Agent 可能改測試去配合程式，以及反事實檢查（故意改壞程式，看測試抓不抓得到）。這裡加深的是範圍：D2 只要求至少一條反事實檢查，D3 每條新規則都要各改壞一次。survived（測試沒抓到）時，不換一個比較好抓的改法，而是補一個會失敗的測試。

Birgitta Böckeler 2026 年 8 月的實驗文章結論很直接：看著測試變紅，只有在有人確認它為什麼變紅時才算證明。TDD（Test-Driven Development，測試驅動開發）是先寫會失敗的測試、再寫程式讓它通過；她發現與其給 Agent 長長的 TDD 指示，不如用變異測試監看測試守不守得住。她的樣本很小，數字不引用。

所以要事先寫下預期哪個斷言失敗，只認測試因為規則被破壞而失敗。不要說「讓 Agent 先寫失敗的測試就安全」：要有人確認失敗的原因。

什麼叫「對的理由」：把守住點數不得為負的那行判斷拿掉，應該失敗的是斷言餘額的那個測試；如果失敗的是一個無關的匯入錯誤，或測試因逾時才失敗，就不算抓到。這也是反事實檢查要先寫下預期斷言（`--expect`）的原因。

📖 延伸閱讀：〈TDD inside the agent loop - theater or actual value?〉（Birgitta Böckeler／martinfowler.com，2026）

**人工確認**：有沒有一條規則第一次是 survived？後來補了什麼測試？

## 14. 需求沒寫的，Agent 會自己補

D3 的需求卡是唯一依據：卡片沒規定的值，寫進交接單的 Unknowns（未知事項），停下來問。

- **卡片有寫**：照做：路徑、欄位與錯誤碼不自己發明。

- **卡片沒寫**：寫進 Unknowns：停下來問，或本段不處理。

Agent 很會「合理地補」：逾時幾秒、重試幾次、狀態叫什麼。它自己補的每一個值，都是一條沒人核准的業務規則，而且因為看起來合理，審查時很容易放過。

D3 的做法是把需求卡當唯一依據：卡片有寫的照做，路徑、欄位與錯誤碼不自己發明；卡片沒寫的，寫進交接單的 Unknowns（未知事項），停下來問，或本段不處理。這是第 2 頁 Böckeler 觀察「需求沒寫清楚，AI 會跳到錯誤結論」的實際對策。

回到團隊：把需求交給 Agent 時，請它最後列出「我自己假設的值」；這張清單就是要拿去問業務的問題。

**人工確認**：Agent 有沒有自己補了一個卡片沒寫的數字或狀態？

## 15. 案例：Agent 大量修改，人照常審查

大公司用 Agent 改舊程式的共同點：先有清楚的規格或規則，人照常審查。數字都是公司自己說的。

- **Google，2025-01**：一次 id 型別遷移中，已合併的修改約 80% 由 AI 產生；人照常審查。

- **Morgan Stanley（第 01 場）**：先產白話規格、工程師再重寫：同樣是人把關。

Google 2025 年 1 月的論文描述一次把 id 型別從 32 位元整數改成 64 位元整數（int32 改 int64）的遷移：已合併的變更裡，80% 的程式修改完全由 AI 產生，工程師自估總時間減少約 50%。原文強調，人審查 AI 產生的程式，和審查其他程式一樣。

要注意這是 Google 對特定一次遷移的自評，不能說成「Google 80% 的程式由 AI 寫」，也不能外推到其他團隊。第 01 場講過的 Morgan Stanley 是同一個模式：先產白話規格，工程師再重寫。

共同點：改動前有清楚的規格或規則，改動後人照常審查。本工作坊沒有量測效率，這些數字只說明「有人這樣做」。

📖 延伸閱讀：〈How is Google using AI for internal code migrations?〉（Nikolov 等人，2025）

**人工確認**：兩個案例裡，哪一步一定由人做？

## 16. 從一塊邊界清楚的地方開始

舊系統現代化的建議很一致：先拆出業務領域，人核准拆法，一次改一塊、每步驗證。

- **Anthropic，2026-02**：先挑邊界清楚、複雜度中等的一個元件。

- **AWS Transform**：拆成業務領域與分批計畫時，要人核准。

- **DDD Europe 2026**：用 AI 產生端到端 API 測試，先守住舊行為。

舊系統現代化的建議很一致：先拆出業務領域，由人核准拆法，一次改一塊、每步驗證。Anthropic 2026 年 2 月的文章建議從「邊界清楚、複雜度中等的單一元件或流程」開始；文中「幾季而不是幾年」是廠商主張，不是量測結果。AWS Transform 的大型主機現代化使用者指南，把「拆成業務領域」與「分批計畫」列為需要人核准的中間產物。

DDD Europe 2026 有一場經驗分享（Cyrille Martraire 與 Olivier Penhoat）：在舊系統現代化中，用 AI 產生端到端 API 測試，先守住一個年營收約 5 億歐元的 API 的既有行為，再動手改。只有議程摘要，沒有成效數字。

回到團隊：要改一個舊系統時，第一塊選邊界清楚、規則你們最懂的地方，先讓測試守住現有行為，再請 Agent 動手。

📖 延伸閱讀：〈How AI helps break the cost barrier to COBOL modernization〉（Anthropic，2026）；〈Modernization of mainframe applications〉（AWS Transform 使用者指南）；〈AI-Generated End-to-End API Tests: An Experience Report in Legacy Modernization〉（Cyrille Martraire、Olivier Penhoat／DDD Europe，2026）

**人工確認**：如果你的團隊要改一個舊系統，第一塊會選哪裡？為什麼？

## 17. 交給 Agent：舊程式先抽出領域

請 Agent 讀舊程式，整理業務規則與候選邊界；它只提候選，由人和懂業務的人核准。

- **Agent 做**：讀大量舊程式，整理成可以審查的清單。

- **人做**：核准哪些是真規則，選第一塊邊界。

### 交給 Agent 的指令

這個舊模組要先拆一塊出來，我得先看懂它的業務。用業務語言列出它處理的業務事件、守的規則、用到的名詞，每項附行號，標成事實、推測或不確定；最後給 2 個可以先獨立的邊界選項，各寫風險。我來選。

第 01 場講過用 AI 讀舊程式、由領域專家驗證，以及把 LLM 當成「可以犯錯的初級領域專家」。這裡多走一步：請 Agent 讀舊模組，不只整理名詞，還列出它處理哪些業務事件、守哪些規則，每一項標成「事實」（有程式行號直接支持）、「推測」或「不確定」，最後提兩個可以先獨立出來的邊界選項。

標記很重要：Agent 寫出的每一句看起來都一樣有把握，要它自己分級，人才知道先查哪裡。標成事實的規則也要找懂業務的人確認，因為舊程式裡的規則，本身可能就是當年的錯誤。

這就是 DLC 的核心模式：Agent 提候選，人核准才成為事實。

**人工確認**：清單裡標成「事實」的規則，有沒有一條你找懂業務的人確認過？

## 18. 搬程式不等於改模型

名詞、負責者、不變量、邊界都沒變，只是搬位置或拆函式，就是重構；模型不改，只更新證據位置。

- **是模型變更**：改名詞、換負責者、改不變量或邊界。

- **不是**：改檔名、搬資料夾、拆函式。

### 交給 Agent 的指令

這次改動我認為只是重構，幫我確認。列出改動碰到引用行的模型紀錄，每一筆判斷名詞、歸哪個 Context、不變量或規則、邊界與依賴、事件或約定有沒有改，各附證據行號。全部沒改就回「只是重構」，並列出要重新指向的證據。

重構（refactoring）依 Martin Fowler 2004 年的定義，是改變程式的內部結構，讓它更容易理解、修改成本更低，而且不改變外部可觀察的行為。對模型也一樣：逐一問名詞、決定歸哪個 Context、不變量或規則、邊界與允許的依賴、事件或約定有沒有變；全都沒變，就只是重構，模型不改，只把證據改指到新位置。

兩個方向的錯都常見：Agent 把「檔案搬了」當成模型變了，提出一堆沒必要的候選，增加審查負擔；反過來，改名看起來像小重構，其實是改模型（第 01 場：改一個名詞就是改模型），要提候選、等核准。

下週可以在團隊的 PR（合併請求）範本加一題：「這次有沒有改到名詞、負責者、規則或邊界？」有就附模型變更，沒有就標明只是重構。

灰色地帶：把「預留」改名成「凍結」看起來只是改字，其實改了通用語言，是模型變更；把計價程式從一個檔案搬到另一個檔案、名稱與規則都沒變，是重構。拿不準時問一題：原本證明這條規則的測試，改完後應該仍然通過嗎？仍然通過是重構，應該失敗是規則變了。

📖 延伸閱讀：〈Definition Of Refactoring〉（Martin Fowler，2004）

**人工確認**：D3 寫回模型的候選，有沒有一筆其實只是重構？

## 19. D3 帶走什麼

人定不變量與邊界，Agent 依模型實作與檢查，每條規則都要有會失敗的測試守著。

不變量 → Aggregate 邊界 → 事件與防腐層 → Agent 實作 → 每條 killed → 候選寫回

- **今天帶走**：先列不變量與證據，再讓 Agent 動手。

- **下一場**：模型落後程式時怎麼辦，以及怎麼交給下一個 Agent。

**人工確認**：回到開場：吵最久的那個決定，最後寫進交接單的哪一段？

## 完成條件
能用自己的話說明不變量、Aggregate、領域事件、Port／Adapter 與防腐層、冪等各解決什麼問題；會用「是什麼／不是什麼」檢查 Agent 提的概念、分得出重構與模型變更；會用「先列不變量與證據、Agent 提選項、人來選」的方式把領域設計交給 Agent；知道測試會綠不代表規則有人守；說得出近期用領域模型引導 Agent 改舊系統的做法。

## 下週可以做的事
- 從需求文件挑一條規則，改寫成「怎樣算違反」的一句話，請 Agent 找出會在違反時失敗的測試；找不到就補一個。
- 請 Agent 檢查領域程式裡有沒有外部服務的欄位名稱或錯誤碼，每筆附行號，由你決定改不改。
- 在 PR 範本加一題：「這次有沒有改到名詞、負責者、規則或邊界？」

## 名詞解釋
| 名詞 | 意思 | 出處 |
|---|---|---|
| 不變量（Invariant） | 每次操作（交易）完成時都必須成立、說得出怎樣算違反的業務規則；可以晚一點才成立的規則不算。 | 〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011） |
| 業務規則 | 業務對資料或行為的要求；其中必須在同一次操作裡立即成立的才是不變量，其他可以用事件事後完成。 | 〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011） |
| 一致性邊界 | 一次操作提交時，裡面的不變量都必須成立的資料範圍；邊界內全有或全無，邊界外事後同步。 | 〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011） |
| Aggregate（聚合） | 必須一起保持一致、當成一個單位修改的一組物件，也就是一個一致性邊界；可以只有一個物件。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Use Tactical DDD to Design Microservices〉（Microsoft Azure Architecture Center，2026） |
| Aggregate root（聚合根） | Aggregate 裡唯一對外的入口物件；外界只持有它的參照，規則由它負責守住。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| Entity（實體） | 靠識別碼區分的物件，屬性改了仍是同一個，例如一筆訂票。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| Value Object（值物件） | 沒有識別碼、只由值決定、建立後不改的物件，例如一個金額。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 最終一致（eventual consistency） | 跨 Aggregate 或跨 Context 的資料不在同一次交易裡更新，而是事後（通常經由事件）在一段時間內變成一致。 | 〈Use Tactical DDD to Design Microservices〉（Microsoft Azure Architecture Center，2026） |
| 領域事件（Domain Event） | 領域專家在乎、已經發生的事，用過去式寫；「資料表多了一列」不算。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |
| 整合事件（integration event） | 交易提交後，把已發生的事非同步通知其他 Context 或外部系統的事件；它成為雙方的約定。 | 〈Domain events: Design and implementation〉（Microsoft .NET 架構指南） |
| Port（埠） | 應用程式和外界一段「有目的的對話」的介面，用自己的用語定義；分成外界驅動程式的一側，與程式需要外界能力的一側。 | 〈Hexagonal Architecture〉（Alistair Cockburn，2005） |
| Adapter（轉接器） | 把 Port 的對話轉成某個外部技術或服務格式的實作；測試時可換成替身。 | 〈Hexagonal Architecture〉（Alistair Cockburn，2005） |
| 防腐層（ACL，Anticorruption Layer） | 下游自己蓋的翻譯層，用自己模型的說法取用上游功能；只翻譯，不放業務規則。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015）；〈Anti-Corruption Layer Pattern〉（Microsoft Azure Architecture Center，2026） |
| 冪等（Idempotency） | 同一個請求送很多次，產生的效果和送一次相同；第二次可以回「已處理過」。 | IETF〈RFC 9110 HTTP Semantics〉；Gregor Hohpe & Bobby Woolf《Enterprise Integration Patterns》（2003）〈Idempotent Receiver〉 |
| 重構（refactoring） | 改變程式內部結構，讓它更好懂、更好改，但不改外部可觀察的行為。 | 〈Definition Of Refactoring〉（Martin Fowler，2004） |

## 延伸閱讀
- 〈The role of developer skills in agentic coding〉（Birgitta Böckeler／martinfowler.com，2025）
- 〈Effective Aggregate Design, Part I〉（Vaughn Vernon，2011）
- Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 10 章〈Aggregates〉
- 〈DDD_Aggregate〉（Martin Fowler，2013）
- 〈Domain-Driven Design Reference〉（Eric Evans，2015）
- 〈Use Tactical DDD to Design Microservices〉（Microsoft Azure Architecture Center，2026）
- 〈Introducing Event Storming〉（Alberto Brandolini，2013）
- 〈Domain events: Design and implementation〉（Microsoft .NET 架構指南）
- 〈Aggregate Design Canvas〉（DDD Crew）
- 〈Hexagonal Architecture〉（Alistair Cockburn，2005）
- Vaughn Vernon《Implementing Domain-Driven Design》（2013）第 4 章〈Architecture〉
- 〈Anti-Corruption Layer Pattern〉（Microsoft Azure Architecture Center，2026）
- 〈Context Mapping〉（DDD Crew）
- Eric Evans《Domain-Driven Design》（2003）第 14 章〈Maintaining Model Integrity〉
- Gregor Hohpe & Bobby Woolf《Enterprise Integration Patterns》（2003）〈Idempotent Receiver〉
- IETF〈RFC 9110 HTTP Semantics〉
- 〈Architecture drift reduction with LLMs〉（Thoughtworks Technology Radar，2026）
- 〈TDD inside the agent loop - theater or actual value?〉（Birgitta Böckeler／martinfowler.com，2026）
- 〈How is Google using AI for internal code migrations?〉（Nikolov 等人，2025）
- 〈How AI helps break the cost barrier to COBOL modernization〉（Anthropic，2026）
- 〈Modernization of mainframe applications〉（AWS Transform 使用者指南）
- 〈AI-Generated End-to-End API Tests: An Experience Report in Legacy Modernization〉（Cyrille Martraire、Olivier Penhoat／DDD Europe，2026）
- 〈Definition Of Refactoring〉（Martin Fowler，2004）
