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
| DDD（Domain-Driven Design，領域驅動設計） | 先把業務的名詞、規則與責任分清楚，再讓程式結構跟著業務邊界走的設計方法。 | Evans《Domain-Driven Design》；Vernon《Implementing Domain-Driven Design》〈Getting Started with DDD〉 |
| 通用語言（Ubiquitous Language） | 在同一個 Context 內，團隊、文件、程式與測試對同一件事使用同一個名字與定義；今天以 Registry 的詞彙（vocabulary）記錄。 | Evans《Domain-Driven Design》〈Communication and the Use of Language〉 |
| Bounded Context（限界上下文，簡稱 Context） | 一個名詞或規則「在這個範圍內意思一致」的邊界，通常對應一群負責同一類決定的程式。每個 Context 寫「它決定什麼」。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉 |
| Owner Context（負責的 Context） | 對某個名詞或規則有最終決定權、負責保存與修改它的那個 Context。例：D3a 要決定「發票」由哪個 Context 負責；其他 Context 只能透過約定取用。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉；Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉 |
| Contract（約定） | Context 之間約定交換的資料或介面；另一方只能透過它取得資料，不直接碰對方內部。例：付款 Context 只透過約定好的「付款結果」通知發票 Context。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| 邊界洩漏 | 一個 Context 繞過約定，直接讀寫另一個 Context 的資料或內部程式。例：計價程式直接改會員的點數欄位。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| Aggregate（聚合）／Aggregate root（聚合根） | Aggregate 是必須**一起**保持一致的一組資料；外界只能從一個入口物件（Aggregate root）修改它。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 不變量（Invariant，INV） | 每次操作結束時都必須成立的業務規則，可以寫成一個會失敗的測試。例：會員點數餘額不得為負。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 一致性邊界 | 每次操作結束時，不變量都必須成立的那一組資料的範圍。邊界內全有或全無；邊界外可以事後再同步。 | Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| Port／Adapter | Port 是領域程式需要的對外能力介面，用自己的業務用語描述；Adapter 是接上真實外部系統的實作。測試時用替身（Fake）實作同一個 Port。 | Vernon《Implementing Domain-Driven Design》〈Architecture〉；`vendor/domain-memory/references/ports-and-adapters.md`〈Ports and adapters〉 |
| 防腐層（ACL，Anti-Corruption Layer；不是存取控制清單） | 把外部系統的資料格式與錯誤碼翻譯成自己用語的那一層。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| 冪等（Idempotency） | 同一個請求重送多次，結果和送一次相同。通常靠一個穩定的鍵（例如訂單編號）判斷是否已處理過。 | Hohpe & Woolf《Enterprise Integration Patterns》〈Idempotent Receiver〉；`vendor/domain-memory/references/pattern-verification.md`〈Verification questions〉 |

## domain-memory Plugin

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| Plugin（外掛套件） | 裝進 Agent 的擴充工具組。今天的 domain-memory Plugin 提供查詢、登記與審查領域知識的指令。 | `vendor/domain-memory/references/packaging.md`〈Packaging modes〉 |
| Domain Memory／Registry | Domain Memory 是經人審查、存在 Repo 裡的領域知識；Registry 是它的資料檔，放在 `domain-memory/` 資料夾、以 JSON 檔保存。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| record（紀錄）與 `asset:id` | Registry 裡的一筆資料。引用時寫成 `asset:id`（類別:id），例如 `rules:FARE-005`。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| `usage`／working-memory | `get-context` 輸出開頭的欄位：D1 是 `working-memory`（整份只能參考），D2 起是 `constraint`（已審查的紀錄可當限制）。某一筆是候選還是已審查，看它自己的 `status`。 | `vendor/domain-memory/references/script-api.md`〈Preparing the approval authority〉 |
| 來源（source）／source map | 人確認過、可以當證據的路徑清單。之後新增、刪除或改名檔案，`verify-sources` 會回報 `stale`。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Before Step 0: Map repository sources〉 |
| 證據（evidence）／`cite` | 指向某個檔案第幾行到第幾行、並帶內容雜湊的引用。引用的行被改過，`verify-evidence` 會回報 `stale`。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 過期（stale）／不存在（missing）／格式錯誤（invalid） | stale：引用的那幾行內容變了；missing：檔案不存在；invalid：寫法或行號不對；仍一致是 current。stale 常常只是「程式改了，紀錄還沒跟上」。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 候選（candidate） | 有證據、但還沒經過核准的主張。Agent 或任何人登記的新內容都是候選，不可當成限制或事實。 | `vendor/domain-memory/references/reliability-architecture.md`〈State model〉 |
| 已審查（reviewed） | 已由另一人核准的正式事實，Agent 可以當成限制。之後不能直接覆寫，只能由下一次核准的提案取代。 | `vendor/domain-memory/references/proposal-lifecycle.md`〈Proposal lifecycle〉 |
| 成對核准 | 一人提案（Proposer）、另一人核准並做簽章 commit（Maintainer）的流程，D2 走過一次。候選要經過它才會變成已審查。 | 本課程〈D2 審查與核准（成對）〉 |
| local-draft-only／scm-verified | Registry 的審查模式。local-draft-only：只能存候選；scm-verified：核准必須有版本控制（SCM）裡的證據，今天是簽章 commit。 | `vendor/domain-memory/references/script-api.md`〈Preparing the approval authority〉 |
| 變更審查包（Change Package，CP） | 一次變更的審查資料：要升級哪些候選、要通過的檢查、實際執行結果。例：D2 的 `CP-D2-001`。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Step 7: Prepare, verify, and review the package〉 |
| obligation（OB，要通過的檢查） | 一個驗收條件或規則對應的可觀察檢查，通常是一個測試指令。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Step 6: Derive test obligations〉 |
| 核准證明（attestation） | 寫進變更審查包、指向簽章 commit 的核准證據。 | `vendor/domain-memory/references/reliability-architecture.md`〈Approval and test attestations〉 |
| 反事實檢查（counterfactual） | 故意把守住某條規則的一段程式改壞，跑指定測試，再原樣還原。`killed`：測試抓到了；`survived`：沒有測試守住它；`inconclusive`：逾時。做法類似變異測試（mutation testing）。 | `vendor/domain-memory/references/script-api.md`〈Checks on the code being written〉 |
| 交接單（Handoff） | 交給 Agent 或同事的決策紀錄，存在 `docs/handoffs/`；Agent 只照它做、不自己補決定。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| Forces／Unknowns（未知事項）／Proof obligations（必須用測試證明的事） | 交接單的三段。Forces：影響決定的考量與限制；Unknowns：還沒決定的事，不能讓 Agent 自己補；Proof obligations：每條規則用哪個測試證明。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| 稽核紀錄（audit）／`verify-audit` | Registry 每次變動都附加一筆稽核事件；`verify-audit` 回 `valid` 代表沒被竄改。 | `vendor/domain-memory/references/reliability-architecture.md`〈Update protocol〉 |
| SHA256／雜湊 | 由檔案內容算出的固定長度字串，像檔案的指紋；一個位元組被改，值就不同。 | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |

## 角色與工具

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| 編號前綴 | CP＝變更審查包、INV＝不變量。EINV、PTS、PCR 分別是 D3a、D3b、D3c 需求卡的驗收條件編號。 | 本課程〈D2 審查與核准（成對）〉 |
| ADR（Architecture Decision Record，架構決策紀錄） | 記錄「當時做了什麼架構決定、為什麼」的短文件。 | Michael Nygard〈Documenting Architecture Decisions〉 |
| brownfield | 已有程式碼的既有專案（相對於從零開始的 greenfield）。 | Feathers《Working Effectively with Legacy Code》；`vendor/domain-memory/references/readiness.md`〈Project readiness〉 |
| 提案者（Proposer） | 整理變更審查包、送出提案、套用；不得核准自己的提案。提案者的 Agent 不 commit、不 push、不碰金鑰。 | 本課程〈D2 審查與核准（成對）〉 |
| 夥伴（Maintainer，持鑰人） | 在自己的 Agent 對話裡建立簽章金鑰、審查並核准、做簽章 commit 與 push。 | 本課程〈D2 審查與核准（成對）〉 |
| ed25519／金鑰指紋（fingerprint） | ed25519 是今天簽 commit 用的金鑰類型。金鑰指紋用來辨識是哪一把金鑰，可以公開；私鑰不可外流。 | IETF〈RFC 8032 Edwards-Curve Digital Signature Algorithm (EdDSA)〉；OpenSSH 官方文件〈ssh-keygen〉 |
| 簽章 commit | 用 Maintainer 私鑰簽過名的 commit，證明是持鑰人提交的。今天以它作為核准證據。 | Git 官方文件〈git-commit〉 |
| Git hook／pre-push hook | pre-push hook 是 Git 在 push 前自動執行的腳本，今天用它檢查有沒有核准與簽章。 | Git 官方文件〈githooks〉 |
| venv（Python 虛擬環境） | 每個專案各自獨立的一套 Python 套件，放在 `.venv` 資料夾。 | Python 官方文件〈venv — Creation of virtual environments〉 |
| Recovery（復原包） | 進度落後時改用的接續基線，由主持人個別提供解鎖碼，在新的 `resume-` 資料夾接續。不算自己完成前一段。 | 本課程〈歡迎與使用方式〉 |
| `record-approval` | 記錄夥伴核准決定的 Plugin 指令，只由夥伴的 Agent 執行。 | `vendor/domain-memory/references/script-api.md`〈File-backed Domain Memory API〉 |
