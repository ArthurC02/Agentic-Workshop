# D4 Handoff 範本：交給下一個 Agent

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員。使用時機：D4（今天最後一段）檢查點 3。交接單由 Agent 依這份格式寫進 `docs/handoffs/d4-next-agent.md`，Runbook D4 頁的提示詞已附上同一份格式；你們不用自己填，只要讀 Agent 的回報、用短回覆核對。

交接單（Handoff）照 Plugin 的交接格式分七段。**只引用 Registry 查得到的 id**（Agent 用 `get-record` 逐一查證）；查不到的移到 Unknowns，不編 id。每一項標明是已審查（reviewed）還是候選。

- **Domain facts（領域事實）**：reviewed 的 Context、詞彙與規則；D3 新增的候選（尚未審查，不可當成限制）；D3 之後已不成立、要由新候選取代的 reviewed 事實（舊 id → 新候選 id）。
- **Forces（影響決定的考量與限制）**：哪些資料必須同時成立；外部系統失敗與重試，以及冪等鍵（重送多次也只處理一次所依據的鍵）；預留與歸還、部分取消。
- **Decision（決定）**：今天做出的設計決定，各一句，附需求卡驗收條件編號或規則 id。
- **External systems（外部系統）**：領域程式要它做什麼、必須分辨哪些結果、測試用什麼替身。
- **Unknowns（未知項）**：需求卡上仍未決定的問題；`verify-sources` 回報過期（stale）、還沒經過來源確認的新檔案；查不到的 id。
- **Proof obligations（必須用測試證明的事）**：規則或驗收條件編號 → 測試名稱，加上最後一次完整 `pytest -q` 的 passed／failed 數。
- **Counterfactual check（反事實檢查結果）**：故意改壞一處程式，確認測試會失敗；抓到就顯示 killed。每列寫規則 id、改壞的地方（檔案:行，原字串 → 改後）、測試、結果，只列實際看到的結果，沒有就寫「未證明」。

核對時問 Agent 這四件事就夠了：

1. 七段都在嗎？沒有內容的段有寫「無」和原因嗎？
2. 每個 id 都查得到嗎？候選有沒有被寫成 reviewed？
3. 有沒有把未決問題寫成已決定？
4. Counterfactual check 每一列都是實際看到的結果嗎？
