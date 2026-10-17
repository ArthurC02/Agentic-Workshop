---
id: glossary
title: 詞彙表
minute: 00-180
group: open
section: 參考
---

# 詞彙表

只寫到今天操作夠用的程度。各需求的業務名詞，以需求卡為準。

## DDD 概念

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| 領域模型／共用模型（Domain Memory） | 領域模型：挑出業務的重點，整理成能用來解決問題的一套說法（詞彙、Context、規則與邊界）。今天把它寫成檔案存在 Repo 裡，團隊和 Agent 共用、經人審查，叫共用模型（Domain Memory）。 | Evans〈Domain-Driven Design Reference〉；`vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| DDD（Domain-Driven Design，領域驅動設計） | 先分清楚業務的名詞、規則與責任，再讓程式結構跟著業務邊界走的設計方法。 | Evans《Domain-Driven Design》；Vernon《Implementing Domain-Driven Design》〈Getting Started with DDD〉 |
| 通用語言（Ubiquitous Language） | 同一個 Context 內，團隊、文件、程式與測試對同一件事用同一個名字與定義；今天記在共用模型的詞彙（vocabulary）。 | Evans《Domain-Driven Design》〈Communication and the Use of Language〉 |
| Bounded Context（限界上下文，簡稱 Context） | 在這個範圍內，同一個名詞或規則的意思一致；每個 Context 寫一句「它決定什麼」。要多個訊號一致才劃：用語改變、資料只在一處寫入、一起修改、只透過明確介面呼叫；資料夾名稱本身不算。同一個字有兩種意思，常是兩個 Context 的訊號。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉；`vendor/domain-memory/references/extraction.md`〈The order of work〉 |
| Owner Context（負責的 Context） | 對某個名詞或規則有最終決定權、負責保存與修改它的 Context；其他 Context 只能透過約定取用。例：D3a 決定「發票」歸誰管。 | Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉；`vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| Contract（約定） | Context 之間約定交換的資料或介面；另一方只透過它取得資料，不碰對方內部。例：付款 Context 只用「付款結果」通知發票 Context。 | Vernon《Implementing Domain-Driven Design》〈Context Maps〉；`vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| 邊界洩漏 | 一個 Context 繞過約定，直接讀寫另一個 Context 的資料或內部程式。例：計價程式直接改會員的點數欄位。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| Aggregate（聚合）／Aggregate root（聚合根） | Aggregate 是必須**一起**保持一致的一組資料；外界只能從一個入口物件（Aggregate root）修改它。它守住一條橫跨多份資料的規則；不是一張資料表，也不是「有子物件的類別」。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 不變量（Invariant，INV） | 每次操作結束時都必須成立的業務規則，可以寫成一個會失敗的測試。例：會員點數餘額不得為負。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 一致性邊界 | 每次操作結束時，不變量都必須成立的那一組資料的範圍。邊界內全有或全無；邊界外可以事後再同步。一個測試同時守住好幾條規則（審查包記為 `also_covers`），常是它們同屬一個邊界的訊號。 | Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| Port／Adapter | Port 是領域程式需要的對外能力介面，用自己的業務用語描述；Adapter 是接上真實外部系統的實作。測試時用替身（Fake）實作同一個 Port。 | Vernon《Implementing Domain-Driven Design》〈Architecture〉；`vendor/domain-memory/references/ports-and-adapters.md`〈Ports and adapters〉 |
| 防腐層（ACL，Anticorruption Layer；不是存取控制清單） | 把外部系統的資料格式與錯誤碼翻譯成自己用語的那一層。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| 冪等（Idempotency） | 同一個請求重送多次，結果和送一次相同。通常靠一個穩定的鍵（例如訂單編號）判斷是否已處理過。 | Hohpe & Woolf《Enterprise Integration Patterns》〈Idempotent Receiver〉；`vendor/domain-memory/references/pattern-verification.md`〈Verification questions〉 |
| 預留與歸還 | 先扣下點數（預留），付款成功才確定；團體付款失敗或退票時全數歸還（一般訂票付款失敗仍保留），重複歸還也只算一次。D3b 用到。 | 本課程〈需求卡 02：會員點數折抵〉 |
| ADR（Architecture Decision Record，架構決策紀錄） | 記錄「當時做了什麼架構決定、為什麼」的短文件。 | Michael Nygard〈Documenting Architecture Decisions〉 |
| 模型變更與重構 | 名詞、負責的 Context、不變量或規則、邊界、事件或對外約定，有任何一項改了才是模型變更，要寫成新候選；只搬移或整理程式、這些都沒變的是重構，只要重新引用證據。 | Martin Fowler〈Definition Of Refactoring〉；`vendor/domain-memory/references/extraction.md`〈From a change〉 |

## 和 Agent 協作的技巧

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| 來源（source） | 人確認過、可當證據的資料（路徑清單）。之後新增、刪除或改名檔案，Agent 會回報來源過期（`stale`）。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Before Step 0: Map repository sources〉 |
| 證據（evidence）／`cite` | 指向某個檔案第幾行到第幾行的引用。Agent 寫進模型的每一句都要附證據；原文之後被改，Agent 會回報對不上。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 候選（candidate） | 有證據、但還沒經過核准的主張。Agent 或任何人寫進模型的新內容都是候選，不可當成限制或事實。 | `vendor/domain-memory/references/reliability-architecture.md`〈State model〉 |
| 已審查事實（reviewed） | 經夥伴核准的模型，Agent 之後必須遵守。不能直接覆寫：意思變了，由下一次核准的新候選（新 id）取代；意思沒變、只是證據搬家，下一次核准沿用原 id 重新證明。每筆帶 `verified`：誰、何時核准，像 ADR 寫「已接受」並列出決策者；`get-record --changes-root` 另列 `proven_by`：證明它的測試。規則有多可信，看這個測試還守不守得住；`coverage` 的 `rules_by_context` 列出每個 Context 有幾條已審查規則、幾條有測試證明。 | `vendor/domain-memory/references/proposal-lifecycle.md`〈Proposal lifecycle〉 |
| 開放問題（open_questions） | 提案裡還沒解決的缺口或問題；模型只放元素、關係與證據。D1 找到的缺口，D2 寫進提案的開放問題。 | 本課程〈D2 審查與核准（成對）〉 |
| 模型版本 | 已審查模型所在的 commit；`export --commit` 讀得到當時的模型。D4 寫在交接單 Domain facts 的第一行。 | 本課程〈D4 交接〉 |
| 成對核准（人工核准關卡） | 做的人和核准的人分開：一人提案（Proposer），另一人審查證據後核准（Maintainer）。主課 B3 Gate 的加深，D2 走過一次。 | 本課程〈D2 審查與核准（成對）〉；Anthropic Engineering〈Building effective agents〉 |
| 提案者（Proposer） | 整理變更審查包、送出提案、套用；不得核准自己的提案。提案者的 Agent 不 commit、不 push、不碰金鑰。 | 本課程〈D2 審查與核准（成對）〉 |
| 夥伴（Maintainer，持鑰人） | 在自己的 Agent 對話裡建立簽章金鑰、審查並核准、做簽章 commit 與 push。 | 本課程〈D2 審查與核准（成對）〉 |
| 交接單（Handoff） | 記錄你們決定的文件，交給 Agent 或同事，存在 `docs/handoffs/`；Agent 只照它做，不自己補決定。主課工作單（Work Order）的加深：多了用到的已審查事實與 Unknowns。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| Forces／Unknowns（未知事項）／Proof obligations（必須用測試證明的事） | 交接單的三段。Forces：影響決定的考量與限制；Unknowns：還沒決定的事，不能讓 Agent 自己補；Proof obligations：每條規則用哪個測試證明。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| 反事實檢查（counterfactual） | 故意把守住某條規則的一段程式改壞，跑指定測試，再原樣還原。`killed`：測試抓到了，而且失敗輸出符合事先寫下的斷言（`--expect`）；`survived`：沒有測試守住它；`inconclusive`：逾時、改壞後程式無法載入，或失敗的不是預期的斷言，都不算證明。做法類似變異測試（mutation testing）。 | `vendor/domain-memory/references/script-api.md`〈Checks on the code being written〉 |

## 工具與環境（Agent 會處理；在回報裡看到時再查）

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| Plugin（domain-memory） | 保存共用模型的工具；指令都寫在提示詞裡，由 Agent 執行。 | `vendor/domain-memory/references/packaging.md`〈Packaging modes〉 |
| Registry／record／`asset:id` | Registry 是共用模型的資料檔，也就是 `domain-memory/` 裡的檔案；每筆資料叫 record，引用時寫成 `asset:id`（類別:id），例如 `rules:FARE-005`。每筆 record 是一份人讀得懂的 Markdown 文件：開頭記狀態與證據，內文是敘述，最後列出和其他 record 的關係；只放元素、關係與證據。檔案裡的 `draft`／`stable` 就是指令輸出的 `candidate`／`reviewed`，以指令輸出為準。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉、〈Concept files〉 |
| 評估（eval）／precision／recall | 拿人審查過的版本當基準答案，比對 Agent 的輸出。precision：Agent 寫的有多少在基準答案裡；recall：基準答案有多少被寫到。只比結構，要讀漏掉（missed）與多出（extra）的清單；引用和基準答案一字不差的配對（`copied_evidence`）是照抄的，誠實的分數看排除它們的 `overall_independent`。回顧時用到。 | Anthropic Engineering〈Demystifying evals for AI agents〉；Google Machine Learning Crash Course〈Classification: Accuracy, recall, precision, and related metrics〉 |
| 證據狀態：current／shifted／stale／missing／invalid | current：仍一致。shifted：引用的那幾行沒變，只是移到同一個檔案的別處，不算失敗。stale：引用的內容變了，常常只是程式改了、模型還沒跟上。missing：檔案不存在。invalid：寫法或行號不對。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 檢查指令（`validate`、`verify-*`） | `validate` 檢查模型的格式與狀態；加 `--require-reviewed` 時，還有候選就不通過。`verify-evidence`、`verify-sources` 比對原文；`verify-audit` 檢查稽核紀錄。 | `vendor/domain-memory/references/script-api.md`〈File-backed Domain Memory API〉 |
| 變更審查包（Change Package，CP） | 一次變更的審查資料：要升級哪些候選、每條規則要通過的檢查（obligation，通常是一個測試指令）與實際執行結果。例：D2 的 `CP-D2-001`。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Step 7: Prepare, verify, and review the package〉 |
| 簽章 commit／金鑰指紋／核准紀錄 | 用夥伴私鑰（ed25519 類型）簽過名的 commit，證明是持鑰人提交的。金鑰指紋（fingerprint）辨識是哪一把金鑰，可以公開；私鑰不可外流。寫進變更審查包、指向這個 commit 的證據叫核准紀錄（attestation）。 | Git 官方文件〈git-commit〉；OpenSSH 官方文件〈ssh-keygen〉；`vendor/domain-memory/references/reliability-architecture.md`〈Approval and test attestations〉 |
| Git hook／推送檢查 | pre-push hook 是 Git 在推送（push）前自動執行的腳本，今天用它檢查有沒有核准與簽章。 | Git 官方文件〈githooks〉 |
| 稽核紀錄（audit） | 模型每次變動都附加一筆稽核事件；`verify-audit` 回 `valid` 代表沒被竄改。 | `vendor/domain-memory/references/reliability-architecture.md`〈Update protocol〉 |
| `record-approval`／`amend-policy` | 記錄核准決定、修改審查規則的指令，只由夥伴的 Agent 執行。 | `vendor/domain-memory/references/script-api.md`〈File-backed Domain Memory API〉 |
| SHA256／雜湊 | 由檔案內容算出的固定長度字串，像檔案的指紋；一個位元組被改，值就不同。開場用它確認工具沒被改過。 | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |
| venv（Python 虛擬環境） | 每個專案各自獨立的一套 Python 套件，放在 `.venv` 資料夾。 | Python 官方文件〈venv — Creation of virtual environments〉 |
| Recovery（復原包） | 進度落後時改用的前一段完成版。主持人個別提供解鎖碼，你在新的 `resume-` 資料夾接續；不算自己完成前一段。 | 本課程〈歡迎與使用方式〉 |
| 編號前綴 | CP＝變更審查包、INV＝不變量。EINV、PTS、PCR 分別是 D3a、D3b、D3c 需求卡的驗收條件編號。 | 本課程〈D2 審查與核准（成對）〉 |
