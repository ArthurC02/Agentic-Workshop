# D4 Handoff 範本：交給下一個 Agent

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員與 Agent。使用時機：D4（今天最後一段）。檢查點 1、2 照「交接前的檢查」讀指令結果；檢查點 3 照「交接單」寫進 `docs/handoffs/d4-next-agent.md`。你們不用自己填，只要讀 Agent 的回報、用短回覆核對。

## 交接前的檢查（檢查點 1、2）

這一段是給 Agent 的，不需要看懂。只整理指令印出的內容，不自己寫程式或腳本；筆數一律以 `asset:id` 計，同一張清單裡每個 `asset:id` 只列一次，不必列行號。

1. `verify-sources`：`status` 是 current 還是 stale；`changed_sources`（新增、刪除、改名）與 `content_changed`（只改內容）各列了哪些路徑，檔案數從幾變成幾；有 `discovered_but_gone`（D1 盤點時有、現在已不存在的檔案）也列出。
2. `verify-evidence`（輸出很長：存檔後只讀 `summary` 與 stale／shifted 那幾筆的 asset、id）：current、shifted、stale、missing、invalid 各幾筆（數量以引用計），再把 stale 與 shifted 各列成一張 `asset:id` 清單。shifted 表示那幾行原封不動、只是移到別處。
3. `verify-audit`：`status` 與事件數。
4. `coverage`（只讀 `rule_totals` 與 `rules_by_context`）：已審查規則幾條，其中有測試證明（proven）、沒有（unproven）、查不到（unknown）各幾條；每個 Context 的已審查與候選規則各幾條，列出 `reviewed_rules` 是 0 的 Context（沒有就寫「無」）。
5. stale 清單裡的每條規則（`rules:…`）：`get-record --asset rules --id 規則id --changes-root domain-memory/changes`，讀 `proven_by` 裡的 `check`（證明它的測試）。是完整指令就照跑；只有測試路徑就用 venv 的 Python 跑 `-m pytest -q 測試路徑`。每條回報證明它的測試與 passed 或 failed；沒有 `proven_by` 寫「沒有測試證明」。

檢查點 2 分類時：

- 只對 stale 清單的每一筆用 `get-record` 查是候選還是 reviewed；shifted 清單不用查：`notes/` 裡 D3 登記過的候選歸 A，其餘歸 C。同時出現在兩張清單的，以 stale 處理。
- A 的新行號：shifted 的重新執行一次 `verify-evidence`（唯讀），看那筆結果的 `lines`；stale 的先讀檔，找出現在講這件事的那幾行。列出 `asset:id`、舊證據、新證據（`路徑:起-迄`）。
- B 最多 3 項：`rules:REFUND-004` 有變就先列，再挑最重要的 2 項；其餘只列 `asset:id`、標「未完成」，留給交接單的 Unknowns。D3 已經登記了取代它的候選，就寫那個 id，不另登記。每項列出原本的 `asset:id`、新候選 id、一句可以用測試推翻的敘述、證據、所屬 context id。
- C 的理由寫「意思沒變：reviewed 不能覆寫，下一次核准沿用同一個 id 重新證明」，只列筆數。
- 登記後在 `notes/d4.md` 寫下剩下的 shifted 與 stale 筆數與原因，來不及登記的列為「未完成」。

## 交接單（檢查點 3）

交接單（Handoff）照 Plugin 的交接格式分七段，開頭一行是 `# Handoff：Smart Ticket Domain Memory（今天日期）`，每段一個 `##` 標題。沒有內容的段寫「無」並說明原因。

寫之前：

- **只引用 Registry（`domain-memory/` 裡記錄領域知識的檔案）查得到的 id**：文中每一個 `asset:id` 都用唯讀的 `get-record --asset 類別 --id 編號` 查證，只查交接單裡真的引用的 id。查不到的不猜替代品，移到 Unknowns。寫成「類別:id」（例如 `rules:PCR-005`）的一律查；沒有類別前綴的 EINV、PTS、PCR 編號是需求卡驗收條件，不用查。
- reviewed 或候選看 `get-record` 的 `status`（decisions 類別看 `review_status`）。兩者分開寫，候選不能寫成 reviewed；需求卡上還沒決定的問題寫進 Unknowns，不能寫成已決定。
- 寫完在對話只回報 id 核對清單（id、查得到嗎、reviewed 或 candidate）與移到 Unknowns 的項目。

七段：

- **Domain facts（領域事實）**：第一行寫模型版本：已審查模型所在的 commit，也就是 `git log` 最上面（最新）一個訊息含「套用」的 commit，寫前 12 碼。先執行 `export --commit 那個編號 --save ../../tmp/model-reviewed.json` 確認讀得到（exit 0；輸出很長，不讀進對話），再寫「下一個 Agent 可用 export --commit 這個編號讀到當時的模型；之後的候選在工作區」。接著寫 reviewed 的 Context、詞彙與規則；D3 新增的候選（標明尚未審查、不可當成限制）；D3 之後已不成立、要由新候選取代的 reviewed 事實（舊 id → 新候選 id）。
- **Forces（影響決定的考量與限制）**：哪些資料必須同時成立；外部系統失敗與重試，以及冪等鍵（重送多次也只處理一次所依據的鍵）；預留與歸還、部分取消。
- **Decision（決定）**：今天做出的設計決定，各一句，附需求卡驗收條件編號或規則 id。
- **External systems（外部系統）**：每個外部系統：領域程式要它做什麼、必須分辨哪些結果、測試用什麼替身。
- **Unknowns（未知事項）**：需求卡上仍未決定的問題；`verify-sources` 回報過期（stale）的來源與還沒經過來源確認的新檔案，註明留給下一次成對核准；沒有已審查規則的 Context；`notes/d4.md` 列為未完成的事實；查不到的 id。
- **Proof obligations（必須用測試證明的事）**：規則或驗收條件編號 → 測試名稱，加上最後一次完整 `pytest -q` 的 passed／failed 數。
- **Counterfactual check（反事實檢查結果）**：故意改壞一處程式，確認測試會失敗；抓到就顯示 killed。每列寫規則 id｜改壞的地方（檔案:行，原字串 → 改後）｜測試｜結果，只列實際看到 killed 的，沒有就寫「未證明」。Recovery 提供的段落沒有反事實紀錄：那幾段寫「未證明」，並在 Unknowns 註明「Recovery 不含」；自己做的段落照實列。

核對時問 Agent 這四件事就夠了：

1. 七段都在嗎？沒有內容的段有寫「無」和原因嗎？
2. 每個 id 都查得到嗎？候選有沒有被寫成 reviewed？模型版本的 commit 讀得到嗎？
3. 有沒有把未決問題寫成已決定？
4. Counterfactual check 每一列都是實際看到的結果嗎？
