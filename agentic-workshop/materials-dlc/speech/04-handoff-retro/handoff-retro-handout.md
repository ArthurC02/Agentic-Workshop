# 交接與導入：讓下一個 Agent 接得上

> 讀者：學員。時機：DDD 延伸課 D4 與回顧之後的 25 分鐘講解。前置：已聽過前三場 DLC Speech，手邊有自己的 notes/ 與 docs/handoffs/。

**這一段帶走什麼**
- 交接最常掉的是「為什麼」；共用模型與交接單是 Agent 的外部記憶
- 人和 Agent 讀同一份模型；交接單裡的每個 id 都要查證
- 模型會漂移，要定期比對；用人審過的模型評估 Agent，分數之外要讀清單
- 團隊共用的指示要短、有人審查；今天的簽章只是教學示範

每頁最後的段落是講解時來不及說的補充：概念的白話解釋、證據出處、限制與回到團隊的做法；提到的書與文章列在最後的「延伸閱讀」。

本場講概念與技巧，不需要寫程式或打指令。頁面上的提示詞是示範，想試再貼給自己的 Agent；沒有實際執行的結果，一律視為未驗證。案例數字都是對方自己說的，本工作坊沒有量測效率。

## 1. 明天換人接手

接手的人只看得到 Repo、共用模型與交接單；今天的對話，他和下一個 Agent 都看不到。

- **今天的概念**：交接、共用模型、評估 Agent、共用指示。

- **今天的案例**：2025–2026 年的研究與 DDD 社群的做法。

**人工確認**：如果明天換你接手，你最先打開哪一個檔？

## 2. 交接最常掉的是「為什麼」

決定留下來了，理由沒留下來，後來的人只能盲從或盲改。Agent 每次開新對話，都是後來的人。

- **寫在 Repo**：換人、換 Agent，都看得到同一份紀錄。

- **寫理由**：不只寫做了什麼，也寫為什麼、不做什麼。

第 02 場講過 ADR（架構決策紀錄）：決定沒留下理由，後來的人只能盲從或盲改。Nygard 同一篇文章還說，決策紀錄放在 Repo，團隊換人也看得到。交接時這更嚴重：Agent 每次開新對話都從零開始，它就是那個「後來的人」。

所以交接單不只寫做了什麼，也寫為什麼、考慮過什麼、刻意不做什麼。D4 交接單的 Forces（影響決定的條件）與 Decision（決定）兩段，就是在寫理由。

下週可以拿自己最近寫的一份交接或 PR 說明檢查：拿掉「為什麼」那幾句，接手的人還能判斷可不可以改嗎？

📖 延伸閱讀：〈Documenting Architecture Decisions〉（Michael Nygard，2011）

**人工確認**：你的交接單裡，有沒有一個決定只寫了結果、沒寫理由？

## 3. 用編號句子講一遍領域

Domain Storytelling 的寫法：誰（角色）做了什麼（動詞）、對什麼（工作物件），照發生順序編號。

- **人看得懂**：懂業務的人不讀程式，也能指出哪句不對。

- **Agent 讀得準**：名詞和動詞都來自通用語言，不必猜。

```text
1  客人      下單    外送
2  調度員    指派    無人機
3  無人機    完成    外送
4  帳務      開立    發票
```

Domain Storytelling（領域故事敘述）用故事整理業務流程：誰（角色）做了什麼（動詞）、對什麼（工作物件），照發生順序編號。domainstorytelling.org 的快速入門這樣定義三個元素：角色是在故事裡主動做事的一方，可以是人、一群人或一個軟體系統；工作物件是角色建立、處理或交換的東西，例如文件、實物或數位資料；活動畫成箭頭，標上領域語言的動詞，並在箭頭起點加上順序編號。投影片沿用第 03 場的無人機外送例子。

一個故事講一個具體情境，不是畫出所有可能。快速入門建議先畫最常見的情況（約八成時候發生的「順利路徑」）；重要的變化各自另畫一個故事，其他的例外與錯誤用註記寫在旁邊，不要塞進同一個故事。

課程例子（現有的整筆退票行為）：1 旅客 申請退票 訂票；2 Smart Ticket 釋放 座位；3 Smart Ticket 建立 退款紀錄。三句就說清楚順利路徑；「還沒付款的訂票不能退」這類例外（規則 REFUND-001），用註記另外寫。

用在交接：交接單前面放一段 5 句以內的編號故事，接手的人和 Agent 先知道業務流程，再看細節。懂業務的人不讀程式也能指出哪一句不對；名詞和動詞都來自通用語言，Agent 不必猜。可以請 Agent 從程式與模型草擬，再由人逐句改。常見誤讀：故事不是流程圖，不畫判斷分支；要畫分支，就是兩個故事。

📖 延伸閱讀：〈Domain Storytelling Quick Start Guide〉（domainstorytelling.org）

**人工確認**：你能用 5 句以內的編號句子，講出 D3 其中一個需求嗎？

## 4. 共用模型是 Agent 的外部記憶

第 01 場說過上下文有限；加深一層：長任務靠寫在外面的筆記，交接單只放 id 與路徑，需要時再讀。

- **筆記寫在外面**：共用模型與交接單在 Repo，不在對話裡。

- **只放指標**：交接單放 id、檔案路徑；細節到模型裡查。

第 01 場講過上下文有限、給太多反而變差。長任務的解法是把筆記寫在對話外面：Anthropic 的〈Effective context engineering for AI agents〉建議 Agent 只保留輕量的識別碼（檔案路徑、查詢、連結），需要時再載入，並把結構化筆記寫在上下文之外。共用模型和交接單就是這種外部記憶：交接單只放 id 與路徑，細節到模型裡查。

實務例子：Giles Edwards-Alexander 2026 年 9 月在 martinfowler.com 記錄，10 位工程師四天共用一個 Repo，發現 Agent 會用寫在 Repo 裡的計畫檔彼此協調，計畫檔成了共用黑板。這是一次團隊經驗，沒有數據。

下週可以把交接或計畫寫成 Repo 裡的檔案、跟著 commit 走，而不是貼在聊天室；下一個人和下一個 Agent 都從同一份開始。

對照 DDD：交接單裡寫「依規則 FARE-005」而不是把規則全文貼進來，就是 Anthropic 說的輕量識別碼。好處有兩個：上下文省下來給真正要做的工作；規則改了，交接單不必跟著改，因為它只指向最新的已審查版本。代價是接手的 Agent 必須真的去查，所以下一頁要逐一查證。

📖 延伸閱讀：〈Effective context engineering for AI agents〉（Anthropic Engineering，2025）；〈An Accidental Blackboard〉（Giles Edwards-Alexander／martinfowler.com，2026）

**人工確認**：你的交接單，是貼了整段內容，還是只放查得到的 id？

## 5. 人和 Agent 讀同一份模型

每個概念一份 Markdown 文件，關係寫成有型別的連結：人直接讀得懂，Agent 也照著走。

- **人看得懂**：審查的人直接讀，不靠工具轉譯。

- **關係有型別**：連結寫明「屬於」「不要用」，Agent 不必猜。

```text
# 借閱（名詞）
讀者把館藏帶走，約定期限內歸還。
## 關係
- 屬於：流通 Context（contexts/circulation）
- 不要用：借書、租借
## 證據
- docs/example.md#L41-48
```

外部記憶要人和 Agent 讀同一份，才能互相檢查。一種做法是每個概念一份 Markdown 文件，概念之間的關係寫成連結，並註明是哪一種關係（例如「屬於」「不要用」）。Google Cloud 提出的 Open Knowledge Format（OKF，開放知識格式）就是這種格式：一個資料夾的 Markdown 檔，開頭加上一小段 YAML 格式的欄位；規格的說法是，能用最基本的指令顯示檔案內容，就讀得懂 OKF。

好處：審查的人直接讀，不靠工具轉譯；Agent 照著連結走，不必猜關係。本 DLC 用的工具只是其中一個例子；團隊用 Repo 裡的 Markdown 加上審查，道理相同。

下週可以試：不開任何工具，直接打開你們的設計文件或模型，看懂業務的同事讀不讀得懂。人讀不懂的，Agent 多半也讀不準。

📖 延伸閱讀：〈Open Knowledge Format (OKF)〉規格（Google Cloud）

**人工確認**：你們團隊的模型，不靠工具打得開、讀得懂嗎？

## 6. 看起來合理的名字最危險

第 01 場看過：模型會編出看起來合理的名字。加深一層：交接單裡的每個 id，都要逐一查證。

- **為什麼會錯**：Agent 照格式「合理地」編出名字。

- **人看什麼**：表裡有沒有「查不到」或「狀態不同」。

### 交給 Agent 的指令

不要修改任何檔案。請把這份交接單引用的每個 id 與檔案路徑列出來，逐一到共用模型與 Repo 查證：查得到、查不到、或狀態不同（例如寫成已審查事實，其實是候選）。列成表，查不到的不要自己補，列完停下。

第 01 場看過：模型會編出看起來合理的套件名稱。交接單裡的 id 是同一種風險：格式對、看起來合理，卻查不到，或狀態不對（例如寫成已審查事實，其實還是候選）。

給了正確的上下文，也不保證照做：Böckeler 2025 年比較幾種規格驅動開發（先寫規格、再讓 Agent 實作）工具時寫到，她常看到 Agent 最後沒有遵守全部指示。所以交接單的每個 id 與路徑都要逐一查證，查不到的不要讓 Agent 自己補。

下週可以在團隊的交接或 PR 範本加一條「引用的 id 與路徑都已查證」，並請 Agent 交出查證表，而不是只說「都查過了」。

📖 延伸閱讀：〈Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl〉（Birgitta Böckeler／martinfowler.com，2025）

**人工確認**：你的交接單裡，有沒有一個 id 第一次查不到？

## 7. 模型會落後程式：定期回收

程式一直在變，人與 Agent 都會照著既有寫法複製；模型和程式的落差要定期清，不是寫一次就好。

- **不要硬改**：落差寫成新候選或 Unknowns，等人核准。

- **定期做**：每次大變更後跑一次，像垃圾回收。

- **擋在門口**：引用沒跟上，commit 就進不來。

### 交給 Agent 的指令

不要修改任何檔案，也不要試著修好。請比對共用模型與目前的程式：列出模型有、但程式已經不同的規則，和程式有、但模型還沒記的規則，每筆附模型 id 與檔案路徑:行號。列成表，列完停下。

模型漂移是指共用模型和程式慢慢對不上：程式一直在變，模型沒跟上。Thoughtworks 技術雷達第 34 期指出，Agent 和人都會照著既有寫法複製，包括不好的寫法，所以漂移會累積；他們用垃圾回收比喻：要定期清，不是寫一次就好。

清的方式：請 Agent 比對模型與程式，列出兩個方向的落差，但不要讓它自己修好。落差可能是程式改錯了，也可能是模型該更新了；哪一個是業務判斷，要寫成新候選或 Unknowns（未知事項）等人核准。

也可以擋在門口：pre-commit hook（commit 前 Git 自動執行的檢查腳本）回報失敗時，Git 會在建立 commit 之前中止；D4 用它擋下改到被引用的程式、引用卻沒跟上的 commit。下週可以在每次大變更後排一次比對。

課程例子：D3 加了新檔案，D4 一開始工具就回報「來源過期」；引用的程式只是換了位置叫 shifted，內容變了叫 stale。前者是重構留下的痕跡，重新指向即可；後者要逐項問：是程式改錯了，還是模型該更新？這兩種回報正是漂移的早期訊號，越早處理越便宜。

📖 延伸閱讀：〈Architecture drift reduction with LLMs〉（Thoughtworks Technology Radar，2026）；〈githooks〉（Git 官方文件）

**人工確認**：Agent 回報落差時，有沒有想自己「修好」它？

## 8. 評估 Agent：和人審過的模型比

讓 Agent 從程式重新整理一份模型，和人審查過的逐筆配對：它漏了什麼、多編了什麼。

- **漏掉的**：人審過、Agent 沒找到：召回率低。

- **多出的**：Agent 有、人沒認可：精確率低。

- **先讀清單**：分數只看結構；漏掉與多出逐筆讀。

### 交給 Agent 的指令

先不要修改任何檔案。請只讀程式，重新整理一份名詞、Context 與規則清單，這一步不要讀共用模型。整理完再和共用模型裡已審查的紀錄逐筆配對，列三張表：配對成功、已審查但你沒找到、你找到但沒有已審查紀錄的。最後算精確率與召回率，列完停下。

評估（eval）Agent 的做法：讓 Agent 只讀程式、重新整理一份模型，和人審查過的模型逐筆配對；人審過的模型就是基準答案。兩個指標依 Google 機器學習速成課程的定義：精確率（precision）是 Agent 提出的裡面有多少是對的；召回率（recall）是該找到的裡面 Agent 找到多少。

算一次就懂：人審過的模型有 20 條規則，Agent 只讀程式整理出 18 條，其中 15 條配得上。精確率＝15÷18，約 0.83，表示 Agent 寫的有八成多是對的；召回率＝15÷20＝0.75，表示該找的找到四分之三。漏掉的 5 條和多出的 3 條才是要讀的地方。Google 機器學習速成課程也提醒，兩個指標常常此消彼長：要 Agent 寫得保守，精確率升、召回率降；要它寫得完整，反過來。

分數不能只看數字。Anthropic 2026 年的〈Demystifying evals for AI agents〉說，他們不照單全收評估分數，要讀實際紀錄；用模型當評分者時，也要和人類專家校準。所以一定要讀兩張清單：多出的可能是 Agent 編的，也可能是人漏審的真規則；措辭不同、意思一樣的規則，可能被算成漏掉。和基準一字不差的配對多半是照抄來的，算分前要排除。

研究也這樣做：Mancas 等人在 MODELS 2026 的論文，用本機執行的開源模型從 10 個 Java 專案擷取領域模型，對照人整理的參考模型，作者自量類別的精確率 0.84、召回率 0.97；作者也提醒，參考模型只是一種合理的理解，不是唯一正解。回到團隊：換模型、改提示詞前後各跑一次，才知道有沒有變好。

📖 延伸閱讀：〈Demystifying evals for AI agents〉（Anthropic Engineering，2026）；〈Classification: Accuracy, recall, precision, and related metrics〉（Google Machine Learning Crash Course）；〈Towards Automated Domain Model Extraction from Source Code using Heuristics and Open-Source LLMs〉（Mancas 等人，MODELS 2026）

**人工確認**：多出來的那幾筆，是 Agent 編的，還是人漏審的？

## 9. 團隊共用的 Agent 指示是工程資產

規則檔不是個人習慣：放進版本控制，像程式一樣審查與維護。

- **放哪裡**：每次對話都會讀的規則檔，例如 AGENTS.md、CLAUDE.md。

- **放什麼**：通用語言、不用的同義詞、哪些事要先問人。

- **誰維護**：改規則也要審查，和改程式一樣。

Thoughtworks 技術雷達第 34 期把「團隊共用、經過整理的 Agent 指示」列為 Adopt（建議採用）：把給 AI 的指引當成協作的工程資產，而不是個人習慣。條目並列多種工具的規則檔（例如 AGENTS.md、CLAUDE.md、.cursorrules），本課不指定工具。

和 DDD 的關係：通用語言、不用哪些同義詞、哪個 Context 負責什麼、哪些事要先問人，是最值得放進共用指示的內容。這是主課 Skill 與共同規則的加深一層：規則檔放進版本控制，改規則也要審查，和改程式一樣。

下週可以收集團隊成員各自的 Agent 規則檔，挑出大家都寫了的幾條，合成一份放進 Repo，並指定一位審查者。

和 DDD 的對應：共用指示裡的名詞表，就是通用語言在 Agent 身上的那一份；它也該只屬於一個 Context。把兩個 Context 的名詞寫進同一份規則檔、又沒標明範圍，Agent 會把它們當成同一套語言，這正是第 01 場說的同字異義問題。

📖 延伸閱讀：〈Curated shared instructions for software teams〉（Thoughtworks Technology Radar，2026）；〈Custom instructions with AGENTS.md〉（OpenAI Codex 官方文件）

**人工確認**：你的團隊裡，有沒有一份大家共用、而且有人審查的規則檔？

## 10. 指示越長，越容易被忽略

每多一行指示，其他規則就多一分被忽略的機會。檢查每一行：刪掉它，Agent 會犯錯嗎？

- **每次都用到**：留在規則檔。

- **偶爾才用**：移到需要時才讀的文件或 Skill。

### 交給 Agent 的指令

不要修改任何檔案。請逐行檢查團隊的規則檔：哪些行刪掉後你會犯錯、哪些和其他行重複、哪些只在特定工作才用得到。列成表，每行附原因，建議刪除或移出的也列出來。列完停下，由我決定。

技術雷達第 34 期把「Agent 指示膨脹」列為 Caution（要小心）：指示越多，重要規則被忽略的可能性越高。Claude Code 官方文件也有同樣的提醒，並給了檢查題：刪掉這一行，Agent 會犯錯嗎？不會就刪。其他工具的官方文件通常有對應章節。

處理方式：每次都用得到的留在規則檔；只有特定工作才用到的，移到需要時才讀的文件或 Skill。D4 交接單固定七段、沒內容就寫「無」，也是同一個理由：短、可預期。

限制：刪過頭也會出錯；刪哪一行由人決定，Agent 只列建議與理由。

📖 延伸閱讀：〈Agent instruction bloat〉（Thoughtworks Technology Radar，2026）；〈Best practices for Claude Code〉（Claude Code 官方文件）

**人工確認**：你的規則檔裡，有沒有一行刪掉也不會出錯？

## 11. 說清楚：今天的簽章是教學示範

兩人在同一台機器上，任一人都拿得到私鑰，推送前的檢查也能被跳過；它不能證明真的有兩個人審查。

- **它的用處**：讓你看見每一步留下什麼證據。

- **真實團隊要什麼**：每人自己的金鑰，伺服器端擋住沒核准的合併。

今天的成對簽章是教學示範：兩人在同一台機器上，任一人都拿得到私鑰；推送前檢查（pre-push hook）可以用 Git 內建的選項跳過，提交前檢查也一樣。它讓你看見每一步留下什麼證據，但不能證明真的有兩個人審查過。

真實團隊要的是：每人自己的金鑰，加上伺服器端的檢查，例如受保護分支（沒有核准就不能合併進主要分支），不靠個人電腦上的設定。第 02 場的 AWS 事件，Amazon 事後加入的也是正式環境存取的強制同儕審查。

下週可以問：你們的主要分支，現在有沒有「沒經另一個人核准就合併不了」的設定？

📖 延伸閱讀：〈githooks〉（Git 官方文件）；〈git-push〉（Git 官方文件）

**人工確認**：要證明「真的有另一個人審查過」，今天還缺什麼？

## 12. 回顧：用證據決定留下哪些把關

請 Agent 從 notes/、交接單與版本紀錄整理證據，人判斷哪一步真的擋住過錯；沒有紀錄就寫「未觀察」。

- **擋住過**：紀錄裡找得到它抓到的錯。

- **只是做完**：做了，但沒有改變任何結果。

- **帶走一項行動**：寫出誰做、何時、怎麼知道做到了。

回顧也套用第 01 場「要證據，不要形容詞」：請 Agent 從 notes/、交接單與版本紀錄整理證據，人判斷每一道把關是「擋住過錯」（紀錄裡找得到它抓到的錯），還是「只是做完」（做了，但沒有改變任何結果）；沒有紀錄的寫「未觀察」。

「只是做完」不代表沒價值，可能只是今天剛好沒遇到錯，但要誠實分開說。本工作坊沒有量測效率，回顧裡不寫沒有證據的效率結論。

帶走一項行動，要寫出誰做、何時、怎麼知道做到了，例如「下週五前，我替一個常吵的名詞寫定義，請一位同事核准」。

**人工確認**：你的回顧裡，有沒有一句沒有證據、卻寫成了結論？

## 13. 帶回團隊：從一個 Context 開始

AI 不會修好團隊，只會放大原有的長處與短處。先挑一個常吵的名詞或規則，寫下來、請人核准。

一個名詞或規則 → 寫進共用模型 → 有人審查 → Agent 依它工作 → 測試守著

- **共用的部分要小**：改共用模型之前，先問會受影響的團隊。

- **一個審查角色**：誰負責核准共用模型，要有人擔任。

Google Cloud 2025 年 DORA 報告（研究軟體交付表現的年度報告）的結論之一：AI 不會修好一個團隊，只會放大原本就有的長處與短處。

Evans 對 Shared Kernel 的提醒也適用於共用模型。Shared Kernel 是兩個 Context 之間的一種關係：兩個團隊明確約定共用一小塊模型與相關程式，雙方因此互相依賴。Evans 說這一塊要保持小，改之前要和另一個團隊商量。團隊共用的模型與規則檔也一樣：共用的部分越大，越多人要一起同意才能改。

兩句合起來就是導入建議：先挑一個常吵的名詞或規則，寫進共用模型、有人審查，再讓 Agent 依它工作、用測試守著；一次一個 Context，和第 03 場舊系統現代化的「一次一塊、每步驗證」一致。也要有人擔任共用模型的審查角色。

第一個 Context 怎麼挑：選規則你們最懂、最常被問、而且有測試的那一塊，最好是讓公司與眾不同的核心子領域；通用的那一塊（例如登入）先用現成方案，不必先建模。三個月後回頭看：Agent 在這一塊的提案被退回的次數有沒有變少，就是有沒有用的證據。

Evans 2024 年鼓勵 DDD 實踐者現在就開始學 LLM、做實驗，也說他的看法會因為變化太快而過時。今天的做法也一樣：回去要用自己的紀錄驗證，而不是照單全收。

📖 延伸閱讀：〈Announcing the 2025 DORA Report〉（Google Cloud，2025）；〈Eric Evans Encourages DDD Practitioners to Experiment with LLMs〉（InfoQ，2024）；〈Domain-Driven Design Reference〉（Eric Evans，2015）

**人工確認**：回到開場：明天接手時你打開的那個檔，今天有寫好嗎？

## 完成條件
說得出交接為什麼要寫理由、共用模型為什麼是 Agent 的外部記憶、為什麼要讓人和 Agent 讀同一份模型、怎麼用人審過的模型評估 Agent 漏了什麼與多編了什麼、看起來合理的 id 為什麼要逐一查證；知道模型漂移要定期回收、團隊共用指示要短且有人審查；說得出成對簽章的限制，帶走一項回到團隊的行動。

## 下週可以做的事
- 從一個 Context 開始：挑一個常吵的名詞或規則，寫進 Repo、請一位同事核准。
- 收集團隊各自的 Agent 規則檔，合成一份共用、有人審查的版本，逐行問「刪掉會出錯嗎」。
- 確認主要分支是否設定為「沒經另一個人核准就合併不了」；沒有的話，提給團隊討論。

## 名詞解釋
| 名詞 | 意思 | 出處 |
|---|---|---|
| 上下文（context） | 這次對話裡交給模型的全部內容；對 Agent 是關鍵但有限的資源，給太多反而會變差。 | 〈Effective context engineering for AI agents〉（Anthropic Engineering，2025） |
| 外部記憶（結構化筆記） | 寫在對話之外、需要時再讀的筆記與識別碼（檔案路徑、id）；共用模型與交接單就是這一種。 | 〈Effective context engineering for AI agents〉（Anthropic Engineering，2025） |
| Domain Storytelling（領域故事敘述） | 用編號的句子講一個具體的業務情境：角色對工作物件做了什麼活動。 | 〈Domain Storytelling Quick Start Guide〉（domainstorytelling.org） |
| 角色／工作物件／活動 | 角色是主動做事的人或系統；工作物件是被建立、處理或交換的東西；活動是標上領域動詞的箭頭。 | 〈Domain Storytelling Quick Start Guide〉（domainstorytelling.org） |
| ADR（架構決策紀錄）放在 Repo | 決策紀錄跟著程式放在版本控制裡，團隊換人也看得到當初的理由。 | 〈Documenting Architecture Decisions〉（Michael Nygard，2011） |
| 模型漂移（architecture drift） | 程式一直在變、模型與架構規則沒跟上，兩者慢慢對不上；要定期比對清理。 | 〈Architecture drift reduction with LLMs〉（Thoughtworks Technology Radar，2026） |
| pre-commit hook | Git 在建立 commit 前自動執行的腳本；回報失敗時，commit 不會建立。 | 〈githooks〉（Git 官方文件） |
| 評估（eval） | 用固定的基準與方法量 Agent 的輸出；分數不照單全收，要讀實際紀錄。 | 〈Demystifying evals for AI agents〉（Anthropic Engineering，2026） |
| 精確率（precision） | Agent 提出的項目裡，真的對的比例。 | 〈Classification: Accuracy, recall, precision, and related metrics〉（Google Machine Learning Crash Course） |
| 召回率（recall） | 該找到的項目裡，Agent 找到的比例。 | 〈Classification: Accuracy, recall, precision, and related metrics〉（Google Machine Learning Crash Course） |
| 參考模型（基準答案） | 人整理、審查過的模型，拿來和 Agent 的輸出比對；它是一種合理的理解，不是唯一正解。 | 〈Towards Automated Domain Model Extraction from Source Code using Heuristics and Open-Source LLMs〉（Mancas 等人，MODELS 2026） |
| 團隊共用的 Agent 指示 | 放進版本控制、像程式一樣審查與維護的規則檔，例如 AGENTS.md、CLAUDE.md。 | 〈Curated shared instructions for software teams〉（Thoughtworks Technology Radar，2026） |
| Agent 指示膨脹 | 規則檔越寫越長，重要規則被忽略的可能性跟著升高。 | 〈Agent instruction bloat〉（Thoughtworks Technology Radar，2026） |
| Open Knowledge Format（OKF） | 每個概念一份 Markdown 檔、開頭加一小段 YAML 欄位的知識格式；人和 Agent 讀同一份。 | 〈Open Knowledge Format (OKF)〉規格（Google Cloud） |
| Shared Kernel（共用核心） | 兩個 Context 明確約定共用的一小塊模型；要保持小，改之前要和對方商量。 | 〈Domain-Driven Design Reference〉（Eric Evans，2015） |

## 延伸閱讀
- 〈Documenting Architecture Decisions〉（Michael Nygard，2011）
- 〈Domain Storytelling Quick Start Guide〉（domainstorytelling.org）
- 〈Effective context engineering for AI agents〉（Anthropic Engineering，2025）
- 〈An Accidental Blackboard〉（Giles Edwards-Alexander／martinfowler.com，2026）
- 〈Open Knowledge Format (OKF)〉規格（Google Cloud）
- 〈Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl〉（Birgitta Böckeler／martinfowler.com，2025）
- 〈Architecture drift reduction with LLMs〉（Thoughtworks Technology Radar，2026）
- 〈githooks〉（Git 官方文件）
- 〈Demystifying evals for AI agents〉（Anthropic Engineering，2026）
- 〈Classification: Accuracy, recall, precision, and related metrics〉（Google Machine Learning Crash Course）
- 〈Towards Automated Domain Model Extraction from Source Code using Heuristics and Open-Source LLMs〉（Mancas 等人，MODELS 2026）
- 〈Curated shared instructions for software teams〉（Thoughtworks Technology Radar，2026）
- 〈Custom instructions with AGENTS.md〉（OpenAI Codex 官方文件）
- 〈Agent instruction bloat〉（Thoughtworks Technology Radar，2026）
- 〈Best practices for Claude Code〉（Claude Code 官方文件）
- 〈git-push〉（Git 官方文件）
- 〈Announcing the 2025 DORA Report〉（Google Cloud，2025）
- 〈Eric Evans Encourages DDD Practitioners to Experiment with LLMs〉（InfoQ，2024）
- 〈Domain-Driven Design Reference〉（Eric Evans，2015）
