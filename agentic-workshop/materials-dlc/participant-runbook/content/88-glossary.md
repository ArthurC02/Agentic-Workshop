---
id: glossary
title: 詞彙表
minute: 00-180
group: open
section: 參考
---

# 詞彙表

本表整理這堂延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課）常用詞彙的意思。DDD（Domain-Driven Design，領域驅動設計）概念不另開理論課，這裡只寫到「今天操作時夠用」的程度；每個詞第一次真正用到時，該檢查點有「新概念」說明框，這裡標出「首次出現」的位置，方便回頭找；各需求的業務名詞，以該段解鎖後的需求卡為準。

## DDD 概念

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| DDD（Domain-Driven Design，領域驅動設計） | 先把業務的名詞、規則與責任分清楚，再讓程式結構跟著業務邊界走的設計方法。今天只用到本節列出的幾個概念。首次出現：歡迎與使用方式。 | Evans《Domain-Driven Design》；Vernon《Implementing Domain-Driven Design》〈Getting Started with DDD〉 |
| 通用語言（Ubiquitous Language） | 團隊、文件、程式與測試對同一件事使用同一個名字與定義。今天以 Registry 的 vocabulary（詞彙）記錄；同一件事兩個名字、或文件有而程式沒有，都是要記下的發現。例：D3b 要確認需求卡說的「優惠」和 Registry 裡的優惠詞彙是不是同一件事。首次出現：D1 檢查點 3。 | Evans《Domain-Driven Design》〈Communication and the Use of Language〉 |
| Bounded Context（限界上下文，簡稱 Context） | 一個名詞或規則「在這個範圍內意思一致」的邊界，通常對應一群負責同一類決定的程式。今天以 Registry 的 contexts 記錄，每個 Context 寫「它決定什麼」。例：「訂單」在付款和開發票時關心的欄位不同，可能屬於不同 Context。首次出現：D1 檢查點 4。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉 |
| owner Context（負責的 Context） | 對某個名詞或規則有最終決定權、負責保存與修改它的那個 Context。例：D3a 要決定「發票」由哪個 Context 負責；其他 Context 只能透過約定取用。首次出現：D3a 檢查點 2。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉；Vernon《Implementing Domain-Driven Design》〈Domains, Subdomains, and Bounded Contexts〉 |
| Context Map／邊界協作 | Context 之間誰提供、誰使用、交換什麼。`analyze-boundary` 列出已登記的協作；回 `no_registered_collaboration` 表示沒有登記，不代表程式裡沒有互相讀寫。首次出現：D1 檢查點 6。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| Contract（約定） | Context 之間約定交換的資料或介面；另一方只能透過它取得資料，不直接碰對方內部。例：付款 Context 只透過約定好的「付款結果」通知發票 Context。首次出現：D1 檢查點 5。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| 邊界洩漏 | 一個 Context 繞過約定，直接讀寫另一個 Context 的資料或內部程式。例：計價程式直接改會員的點數欄位。首次出現：D1 檢查點 6。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| Aggregate（聚合）／Aggregate root（聚合根） | Aggregate 是必須**一起**保持一致的一組資料；外界只能從一個入口物件（Aggregate root）修改它。用來回答「哪些資料要在同一次操作中同時成立」。例：D3c 團體訂票的旅客、座位與退款紀錄必須一起改，只能透過訂票這個入口。首次出現：D3c 檢查點 2。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 不變量（Invariant，INV） | 任何時刻都必須成立的條件，好的不變量可以寫成一個會失敗的測試。例：會員點數餘額不得為負；一筆訂單最多一張已開立發票。交接單裡的 INV-1、INV-2 由 Agent 依你們同意的不變量編號。首次出現：D3a 檢查點 2。 | Evans《Domain-Driven Design》〈The Life Cycle of a Domain Object〉；Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| 一致性邊界 | 不變量必須立即成立的範圍。邊界內同步處理、全有或全無；邊界外可以事後處理。首次出現：D3c 檢查點 2。 | Vernon《Implementing Domain-Driven Design》〈Aggregates〉 |
| Port／Adapter | Port 是領域程式需要的對外能力介面，用自己的業務用語描述；Adapter 是接上真實外部系統的實作。測試時用替身（Fake）實作同一個 Port。例：「開立發票」是 Port，接某家發票服務商的程式是 Adapter。首次出現：D3a 檢查點 2。 | Vernon《Implementing Domain-Driven Design》〈Architecture〉；`vendor/domain-memory/references/ports-and-adapters.md`〈Ports and adapters〉 |
| 防腐層（ACL，Anti-Corruption Layer；不是存取控制清單） | 把外部系統的資料格式與錯誤碼翻譯成自己用語的那一層，讓外部的命名與規則不滲進領域程式。例：把服務商的各種錯誤碼翻成「暫時失敗」或「永久失敗」。首次出現：D3a 檢查點 2。 | Evans《Domain-Driven Design》〈Maintaining Model Integrity〉；Vernon《Implementing Domain-Driven Design》〈Context Maps〉 |
| 冪等（Idempotency） | 同一個請求重送多次，結果和送一次相同。通常靠一個穩定的鍵（例如訂單編號）判斷是否已處理過。例：同一筆訂單的開立發票請求重送，也不會開出第二張。首次出現：D3a 檢查點 1。 | Hohpe & Woolf《Enterprise Integration Patterns》〈Idempotent Receiver〉；`vendor/domain-memory/references/seven-step-workflow.md`〈Step 4: Decide the event〉 |

## domain-memory Plugin

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| Plugin（外掛套件） | 裝進 Agent 的擴充工具組。今天的 domain-memory Plugin 提供查詢、登記與審查領域知識的指令；開場時以 ZIP 發給你，並核對 SHA256。首次出現：開場與環境 檢查點 2。 | `vendor/domain-memory/references/packaging.md`〈Packaging modes〉 |
| Domain Memory／Registry | 存在 Repo 的 `domain-memory/` 資料夾、以 JSON 檔保存的領域知識，包含：審查政策（policy）、可當證據的檔案清單（source map）、一筆筆紀錄（registry）與稽核紀錄（audit）。首次出現：D1 檢查點 2。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| record（紀錄）與 `asset:id` | Registry 裡的一筆資料，例如一個 Context、一個詞彙、一條規則或一個 Aggregate，每筆都有 `id` 與 `evidence`。引用時寫成 `asset:id`：前半是類別（`contexts`、`vocabulary`、`rules`、`aggregates`…），後半是編號，例如 `rules:FARE-005`。首次出現：D1 檢查點 3。 | `vendor/domain-memory/references/registry-schema.md`〈Domain Registry schema〉 |
| `usage`／working-memory | `get-context` 輸出開頭的欄位，說明這些內容能怎麼用。`working-memory` 表示還沒經人核准，Agent 只能參考、不能當成限制；核准成已審查之後就不再是這個值。首次出現：D1 檢查點 6。 | `vendor/domain-memory/references/reliability-architecture.md`〈State model〉 |
| 來源（source）／source map | 人確認過、可以當證據的路徑清單與它們的快照。之後新增、刪除或改名檔案，`verify-sources` 會回報 `stale`。例：D3 在 `src/` 新增檔案後，來源就不再是 D1 確認的那一份。首次出現：D1 檢查點 1。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Before Step 0: Map repository sources〉 |
| agent-asserted／developer-confirmed | 來源清單的確認狀態。agent-asserted：Agent 自己認定、尚未經人確認；developer-confirmed：已由開發者確認（D1 做的事）。首次出現：D1 檢查點 2。 | `vendor/domain-memory/references/script-api.md`〈File-backed Domain Memory API〉 |
| 證據（evidence）／`cite` | 指向某個檔案第幾行到第幾行、並帶內容雜湊的引用。引用的行被改過，`verify-evidence` 會回報 `stale`。首次出現：D1 檢查點 3。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 過期（stale）／不存在（missing）／格式錯誤（invalid） | 驗證指令的結果狀態。stale：內容和當初記錄的不同了；missing：引用的檔案已不存在；invalid：引用寫法不對。仍一致時顯示 current。stale 不一定是錯，常常只是「程式改了，紀錄還沒跟上」。首次出現：D1 檢查點 3。 | `vendor/domain-memory/references/evidence-rules.md`〈Evidence rules〉 |
| 候選（candidate） | 有證據、但還沒經過核准的主張。Agent 或任何人登記的新內容都是候選，不可當成限制或事實。首次出現：D1 檢查點 3。 | `vendor/domain-memory/references/reliability-architecture.md`〈State model〉 |
| upsert | 「有就更新、沒有就新增」。`make_record.py --upsert` 把紀錄寫成候選；候選可以用同一個 id 再寫一次，已審查的不行。首次出現：D1 檢查點 4。 | `vendor/domain-memory/references/script-api.md`〈File-backed Domain Memory API〉 |
| 已審查（reviewed） | 已由另一人核准的正式事實，Agent 可以當成限制。要經過變更審查包、他人核准、簽章 commit 與 `apply-approved-updates` 才會升級；之後不能直接覆寫，只能由下一次核准的提案取代。首次出現：D2 檢查點 6。 | `vendor/domain-memory/references/proposal-lifecycle.md`〈Proposal lifecycle〉 |
| 成對核准 | 一人提案（Proposer）、另一人核准並做簽章 commit（Maintainer）的流程，D2 走過一次。候選要經過它才會變成已審查。首次出現：D2 開始前。 | 本課程〈D2 審查與核准（成對）〉 |
| local-draft-only／scm-verified | Registry 的審查模式。local-draft-only：只能存候選；scm-verified：核准必須有版本控制（SCM）裡的證據，今天是簽章 commit。首次出現：D1 檢查點 2（scm-verified：D2 檢查點 2）。 | `vendor/domain-memory/references/script-api.md`〈Preparing the approval authority〉 |
| SCM（Source Control Management，版本控制） | 管理程式版本的系統，這裡指 Git。首次出現：D2 檢查點 5。 | Pro Git〈About Version Control〉 |
| 變更審查包（Change Package，CP） | 一次變更的審查資料，放在 `domain-memory/changes/<id>/`，共四個 JSON：整理後的需求、修改提案、要通過的檢查、實際執行結果。例：D2 的 `CP-D2-001`。首次出現：D2 檢查點 3。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Step 7: Prepare, verify, and review the package〉 |
| obligation（OB，要通過的檢查） | 一個驗收條件或規則對應的可觀察檢查，通常是一個測試指令。證據包記錄它實際執行的 exit code 與輸出雜湊。首次出現：D2 檢查點 3。 | `vendor/domain-memory/references/seven-step-workflow.md`〈Step 6: Derive test obligations〉 |
| 核准證明（attestation） | 寫進證據包、指向簽章 commit 的核准證據，證明核准發生在 Plugin 之外（Git 裡）。首次出現：D2 檢查點 5。 | `vendor/domain-memory/references/reliability-architecture.md`〈Approval and test attestations〉 |
| 反事實檢查（counterfactual） | 故意把守住某條規則的一段程式改壞，跑指定測試，再原樣還原。`killed`：測試抓到了；`survived`：沒有測試守住它；`inconclusive`：逾時。做法類似變異測試（mutation testing）。首次出現：D2 檢查點 3。 | `vendor/domain-memory/references/script-api.md`〈Checks on the code being written〉 |
| 交接單（Handoff） | 交給下一個 Agent 或同事的決策紀錄，共七段：Domain facts（領域事實）、Forces（考量與限制）、Decision（決定）、External systems（外部系統）、Unknowns（未知項）、Proof obligations（必須用測試證明的事）、Counterfactual check（反事實檢查結果）。首次出現：D3a（決策卡）；七段格式在 D4 檢查點 3。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| Forces／Unknowns／Proof obligations | 交接單裡最容易寫錯的三段。Forces：影響這次決定的考量與限制，例如「發票失敗不能影響付款」；Unknowns：需求卡沒規定、還沒決定的事，例如「處理中太久怎麼辦」，不能讓 Agent 自己補；Proof obligations：每條規則要用哪個測試證明，例如「INV-1 → 某測試檔::某測試名稱」。首次出現：D3a 檢查點 2（決策卡）；D4 檢查點 3。 | `vendor/domain-memory/references/implementation-handoff.md`〈Handoff contents〉 |
| audit（稽核）／`verify-audit` | 每次 Registry 變動都附加一筆、以雜湊串起的稽核事件。能看出被竄改，但不是外部不可變的紀錄。首次出現：D2 檢查點 6。 | `vendor/domain-memory/references/reliability-architecture.md`〈Update protocol〉 |
| SHA256／雜湊 | 雜湊是由檔案內容算出的固定長度字串，像檔案的指紋；一個位元組被改，值就不同。SHA256 是常用的雜湊演算法。今天用它核對 Plugin 檔案、證據內容與稽核鏈。首次出現：開場與環境 檢查點 2。 | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 |
| HITL（Human-in-the-loop，人工把關） | 流程中一定要有人看過並同意才能往下走。今天指 push 時檢查是否有人核准並簽章。首次出現：D2 檢查點 2。 | Anthropic Engineering〈Building effective agents〉 |

## 角色與工具

| 詞彙 | 今天的用法 | 出處 |
|---|---|---|
| DLC | 延伸課程。原指遊戲的追加內容，這裡指主課之後的 DDD 加課；Git 使用者名稱「DLC Proposer／DLC Maintainer」裡的 DLC 也是這個意思。首次出現：歡迎與使用方式。 | 本課程〈歡迎與使用方式〉 |
| D1–D4 | 今天四段的代號：D1 共同語言與邊界、D2 審查與核准、D3 受治理的變更、D4 交接。D3 再分 a、b、c 三張需求（電子發票、點數折抵、團體部分退款）。首次出現：歡迎與使用方式。 | 本課程〈歡迎與使用方式〉 |
| 編號前綴 | CP＝Change Package、REQ＝需求、AC＝驗收條件、OB＝obligation（要通過的檢查）、INV＝不變量。EINV、PTS、PCR 分別是 D3a、D3b、D3c 需求卡的驗收條件編號。首次出現：D2 簽章流程清單。 | 本課程〈D2 簽章流程清單〉 |
| ADR（Architecture Decision Record，架構決策紀錄） | 記錄「當時做了什麼架構決定、為什麼」的短文件。D1 可以把它當成候選來源之一。首次出現：歡迎與使用方式。 | Michael Nygard〈Documenting Architecture Decisions〉 |
| brownfield | 已有程式碼的既有專案（相對於從零開始的 greenfield）。今天的 Repo 是 brownfield，開場時 Plugin 會判定出這一點。首次出現：開場與環境 檢查點 3。 | Feathers《Working Effectively with Legacy Code》；`vendor/domain-memory/references/readiness.md`〈Project readiness〉 |
| Proposer（提案人） | D2 的提案人：用自己的 Agent 對話整理變更審查包、送出提案、套用。不得核准自己的提案；提案人的 Agent 不 commit、不 push、不碰金鑰。首次出現：D2 角色卡。 | 本課程〈D2 角色卡〉 |
| Maintainer（持鑰人） | D2 的持鑰人：在同一台機器另開終端機與自己的 Agent 對話，建立簽章金鑰、決定授權誰簽章、核准並做簽章 commit 與 push。首次出現：D2 角色卡。 | 本課程〈D2 角色卡〉 |
| Observer（觀察員） | 三人一組時的第三人：看 D2 每一步是在誰的 Agent 對話裡執行，確認核准與簽章只發生在夥伴自己的對話。首次出現：D2 角色卡。 | 本課程〈D2 角色卡〉 |
| ed25519／金鑰指紋（fingerprint） | ed25519 是一種 SSH 金鑰類型，今天用來簽 commit。金鑰指紋用來辨識是哪一把金鑰，可以公開；私鑰不可外流。首次出現：D2 檢查點 1。 | IETF〈RFC 8032 Edwards-Curve Digital Signature Algorithm (EdDSA)〉；OpenSSH 官方文件〈ssh-keygen〉 |
| 簽章 commit | 用 Maintainer 私鑰簽過名的 commit，證明是持鑰人提交的。今天以它作為核准證據。首次出現：D2 檢查點 1。 | Git 官方文件〈git-commit〉 |
| Git hook／pre-push hook | Git hook 是 Git 在特定時機自動執行的腳本；pre-push hook 在 push 前執行，今天用它檢查有沒有核准與簽章。首次出現：開場與環境 檢查點 4。 | Git 官方文件〈githooks〉 |
| bare repo（本機模擬的遠端倉庫） | 只存 Git 歷史、沒有工作檔案的倉庫。今天在本機建一個代替伺服器，用來練習 push 與 pre-push 檢查。首次出現：D2 檢查點 6。 | Git 官方文件〈git-init〉 |
| venv（Python 虛擬環境） | 每個專案自己的一套 Python 與套件，放在 `.venv` 資料夾，不影響電腦上的其他專案。首次出現：開場與環境 檢查點 1。 | Python 官方文件〈venv — Creation of virtual environments〉 |
| 提示詞／紀錄檔（`notes/`） | 今天每個檢查點都給一段可直接複製的提示詞：貼給 Agent，它執行指令、白話回報，需要決定時停下等你短短回一句。結果由 Agent 寫進 Repo 的紀錄檔：各段 `notes/<段落>.md`，決策卡與交接單在 `docs/handoffs/`。首次出現：歡迎與使用方式。 | 本課程〈歡迎與使用方式〉 |
| `dm.ps1`／`dm.sh` | 學員包 `tools/` 中呼叫 domain-memory Plugin 的捷徑腳本（PowerShell 用 `dm.ps1`，Git Bash 用 `dm.sh`），由 Agent 依提示詞執行。它會自動補上 Python 版本、UTF-8 與 Registry 位置等參數；`--save 檔案` 以 UTF-8 存輸出。首次出現：開場與環境 檢查點 3。 | 本課程〈延伸課程輔助工具〉（`tools/README.md`） |
| `make_record.py` | 由 id、名稱、定義與「路徑:起-迄」產生帶 `cite` 證據的 record；`--upsert` 直接登記為候選，`--batch` 一次多筆。首次出現：D1 檢查點 3。 | 本課程〈延伸課程輔助工具〉（`tools/README.md`） |
| `fill_package.py` | 由一份精簡描述 JSON 填寫變更審查包，並實際執行每個測試。首次出現：D2 檢查點 3。 | 本課程〈延伸課程輔助工具〉（`tools/README.md`） |
| `write_scm_attestation.py` | 把已簽章的 commit 寫成核准證明（attestation）。首次出現：D2 檢查點 5。 | 本課程〈延伸課程輔助工具〉（`tools/README.md`） |
| `doctor.py` | 檢查 Python、UTF-8、PATH 上的 python、Git、ssh-keygen 與 Plugin 版本等環境問題。首次出現：開場與環境 檢查點 4。 | 本課程〈延伸課程輔助工具〉（`tools/README.md`） |
| Recovery | 落後時由主持人個別提供的接續起點。使用 Recovery 不算自己完成前一段。首次出現：歡迎與使用方式。 | 本課程〈歡迎與使用方式〉 |
