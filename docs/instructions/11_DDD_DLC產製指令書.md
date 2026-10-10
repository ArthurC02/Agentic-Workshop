# DDD DLC 產製指令書（P13）

> 讀者：產製 DDD DLC 教材、參考解答、建置與打包工具的 Coding Agent，以及驗收者。
> 時機：主課 P12 素材完成之後；與 edition-aware 建置（`scripts/build_materials.py --edition dlc`）平行進行。
> 前置：00 總控、05、06、10 指令書；起始 Repo `agentic-workshop/07-dlc-ddd/participant/repository/smart-ticket-dlc-base/`；domain-memory Plugin 0.10.15（`SKILL.md`、`AGENTS.md`、`references/script-api.md`、`references/seven-step-workflow.md`、`references/implementation-handoff.md`、`references/ports-and-adapters.md`、`references/pattern-verification.md`）。
> 主課候選以程式為準：`scripts/build_materials.py` 的 `CANDIDATE_ID`。

## 1. 已核准變更（2026-10-07，使用者於對話中核准）

1. 新增獨立產品「DDD DLC」：180 分鐘加課，對象為已完成主課（Tool → Teammate → Digital Worker）的學員。不改主課 90 分鐘時程、商業規則、版本、測試期待值或任何凍結候選。
2. 主題：**Agent 的領域記憶**。把領域知識轉成經審查、以檔案保存的 Domain Memory，並用它驅動受治理的變更。DDD 概念（Ubiquitous Language、Bounded Context、Context Map、Aggregate／invariant／一致性邊界、Port／Adapter／ACL）一律透過 domain-memory Plugin 操作來教，不另開理論講堂。
3. Plugin 版本固定為 0.10.15，只內嵌執行用的檔案（依 Plugin README，排除 `evals/`、`scripts/test_*.py` 與開發用的 `README.md`、`ruff.toml`；由 `scripts/vendor_dlc_plugin.py` 產生），附 SHA256 清單；內嵌的檔案不得修改任何位元組。
4. 起始 Repo 為 B3 團體訂票解答的清理複本 `smart-ticket-dlc-base`。設計洩漏（貧血模型、三處複製計價、具體 Gateway 無 Port、三份座位真相、退款以 booking_id 為鍵）刻意保留作為教材；產品規則放在 `docs/requirements/`，因為 Plugin 只自動分類該類資料夾。
5. 情境卡為 `agentic-workshop/07-dlc-ddd/participant/scenarios/01-e-invoice.md`、`02-points-redemption.md`、`03-group-partial-refund.md`，由平行工作撰寫；本指令書只引用路徑，不得改寫其內容。
6. D3 三個情境**全體依序進行、三個都做**（D3a → D3b → D3c），每段在前一段成果上累積。
7. D2 為成對練習：每組一人當 proposer，夥伴持 maintainer 簽章金鑰並核准。主持人提供的 reviewed Registry 為預設降級與 Recovery。
8. 每個 D 段沿用主課檢查點節奏：投影顯示時間與目前檢查點；每段有獨立解鎖碼與 Recovery 包。2026-10-09 已核准變更：Runbook 每個檢查點是「說明 → 可直接複製的提示詞 → 看到什麼算過關」，Plugin 與 Git 指令原樣寫進提示詞由 Agent 執行並白話回報，學員只用短回覆做決定；紀錄由 Agent 寫入檔案；表單每段最多一張、以下拉／勾選為主；小組討論用「討論一下」提示，不用表格。D2 核准仍須由夥伴本人在自己開的 Agent 對話中（同一台電腦、另一個終端機）、讀過審查包後下指令簽章；提案者的 Agent 不得執行簽章、核准、commit 或 push，也不得讀取金鑰。
9. 學員輔助腳本由 Spike 衍生（以 `cite` 組 record、Change Package 填寫器、SCM attestation 寫入器），讓時間花在領域決策而不是手打 JSON。
10. 建置走 edition 參數：`scripts/build_materials.py --edition dlc`，輸出 `agentic-workshop/materials-dlc/`；Runbook 儲存前綴 `stwdlc:`；打包獨立（`scripts/package-manifest-dlc.json`、`dist/dlc-candidate/<id>/`、獨立證據）。DLC 工作不得變更主課 `scripts/package-manifest.json` 與主課候選。
11. Evaluation 素材（reference Registry、各情境參考解答、觀察指引／評分表）僅供主持人；揭曉前不得可由任何學員包或 Runbook 取得。
12. 2026-10-07 追加核准：(a) 起始 Repo 允許新增 `.gitattributes`（`* -text`），測試數為 76；(b) DLC 學員簽章金鑰放在 Repo 外 `%USERPROFILE%\.dlc-keys\<代號>\`（Git Bash `~/.dlc-keys/<代號>/`），不放 Repo 內 `.dlc-keys/`（scan-secrets 會掃忽略目錄）也不放 `~/.ssh`，故 `scan-secrets` 預期 exit 0。
13. 2026-10-07 依最終驗證報告（`evaluation/dlc-final-report.md`）對齊已建成設計，不放寬任何安全要求：(a) **D3 參考解答**的 Registry 狀態 = D2 reviewed Registry ＋ 新增／變更事實以**候選**（`upsert-candidate`）登記；D3 不產出已 finalize 的 Change Package（受治理的晉升是 D2 的課題，D4 負責交接）。驗證改為對各參考解答的 `domain-memory/` 執行 `validate`、`verify-audit`、`coverage`；已變動檔案上的 stale evidence 為預期並須列出。(b) **開場**：環境／下載頁屬解鎖群組 `dlc-opening`（第 0 分鐘，碼寫在第一張解鎖投影片），因為開放頁不得提供下載；只有開始之前、Runbook 用法、詞彙表為 `open`。開場有四個檢查點（見 `materials-dlc/CHECKPOINTS.md`）：依賴安裝與測試／Plugin 解出與 SHA 核對／readiness 與 quality-gates／確認真實 Python。(c) **實際檔名**：DLC 建置測試為 `scripts/test_build_materials.py`（`EditionTests`）與 `scripts/test_build_delivery_dlc.py`；DLC 包驗證器為 `scripts/build_delivery_dlc.py --verify <dir>`；Plugin 封裝為 `scripts/vendor_dlc_plugin.py`；Recovery 產生器為 `agentic-workshop/07-dlc-ddd/facilitator/recovery/make_recovery.py`（資料夾 d1、d2、d3a、d3b、d3c）；不存在 `scripts/test_build_materials_dlc.py`、`scripts/validate_dlc.py`。(d) **檢查點時窗例外**：D3 步驟 3「Handoff 與 Agent 實作」為 7／8／9 分（d3a／d3b／d3c）、D3c 步驟 4 為 6 分，超過每步 5 分鐘，列為已接受例外；緩解：情境卡把 AC 分成核心與延伸，時間不足只做核心。(e) **RECOVERY 接手**會把維護者**公鑰**（allowed-signers 一行）複製到學員的 `~/.dlc-keys`；僅公鑰，可接受，私鑰仍不得出現在任何包內。

## 2. 產出

| 位置（相對 Repo 根） | 內容 | 受眾 |
|---|---|---|
| `agentic-workshop/07-dlc-ddd/README.md` | DLC 總覽、三分目錄說明、建置與驗證指令 | 維護者 |
| `07-dlc-ddd/participant/repository/smart-ticket-dlc-base/` | 起始 Repo（已存在；僅允許第 5.3 節列出的補強） | 學員 |
| `07-dlc-ddd/participant/scenarios/01–03-*.md` | 情境卡（平行工作產出，本指令書只驗收引用） | 學員 |
| `07-dlc-ddd/participant/vendor/domain-memory-0.10.15.zip`、`domain-memory-0.10.15.SHA256SUMS` | Plugin 原樣封裝與逐檔／整包雜湊 | 學員 |
| `07-dlc-ddd/participant/tools/` | `dm.ps1`、`dm.sh`（固定 `-X utf8` 與 `--registry-root domain-memory` 的命令前綴）、`make_record.py`、`fill_package.py`、`write_scm_attestation.py`、`setup_remote.py`（建本機 bare remote）、`dmlib.py`（共用函式）、`doctor.py`（環境自檢） | 學員 |
| `07-dlc-ddd/participant/worksheets/` | D1 來源選擇表、D2 角色卡、D3 決策卡、D4 Handoff 範本（純 Markdown，供 Runbook include） | 學員 |
| `07-dlc-ddd/facilitator/facilitator-guide.md` | 逐段 cue、檢查點、提示條件、降級規則、成對簽章示範腳本 | 主持人 |
| `07-dlc-ddd/facilitator/recovery/` | 各段 Recovery 來源（見第 3.2 節）與產生器 `make_recovery.py`（d1、d2、d3a、d3b、d3c），由參考解答清理而來 | 主持人（揭曉後才發） |
| `07-dlc-ddd/evaluation/reference-registry/` | 完整 reviewed Registry（含 policy、source map、audit chain、已 finalize 的 Change Package，即 D2 成果） | 主持人 |
| `07-dlc-ddd/evaluation/reference-solutions/d3a-e-invoice/`、`d3b-points-redemption/`、`d3c-group-partial-refund/` | 累積式參考解答 Repo，含測試、`domain-memory/`（D2 reviewed Registry ＋ 候選事實，無 Change Package）、counterfactual 證據 | 主持人 |
| `07-dlc-ddd/evaluation/observation-guide.md` | 觀察指引與評分表（每段 3–5 個可觀察行為） | 主持人 |
| `07-dlc-ddd/evaluation/dlc-validation-evidence.json` | 第 7 節驗證的實際輸出摘要與雜湊 | 驗收者 |
| `agentic-workshop/materials-dlc/README.md` | 使用方式、建置指令、解鎖碼位置、Preflight | 主持人／維護者 |
| `materials-dlc/unlock-codes.json` | 群組 id 一律 `dlc-` 前綴 | 主持人 |
| `materials-dlc/facilitator-deck/src/`、`facilitator-deck.html` | 簡報原稿（自有 `js/10-deck-core.js` PLAN）與建置成品 | 主持人 |
| `materials-dlc/participant-runbook/content/`、`template/`、`runbook.html` | Runbook 原稿、模板（前綴 `stwdlc:`）與建置成品 | 學員（只發 `runbook.html`） |
| `scripts/package-manifest-dlc.json`、`scripts/build_delivery_dlc.py`（含 `--pin`／`--verify`）、`scripts/vendor_dlc_plugin.py`、`scripts/test_build_materials.py`（EditionTests）、`scripts/test_build_delivery_dlc.py` | DLC 打包清單、DLC 包建置與驗證、Plugin 封裝、建置測試 | 維護者 |
| `dist/dlc-candidate/<id>/`、`dist/materials-dlc/participant-materials-dlc.zip` | DLC 受控候選包與學員發放 ZIP（忽略追蹤） | 維護者 |

不得新增上表以外的頂層資料夾。`scripts/build_materials.py` 的 edition 實作屬平行工作，本指令書只規定其 DLC 輸入與驗收。

## 3. 時程、檢查點與解鎖

### 3.1 時程（合計 180 分鐘，連續無重疊）

| 分鐘 | 段落 id | 名稱 | 主要操作（全部經 `tools/dm.*` 執行） |
|---|---|---|---|
| 0–10 | `dlc-opening` | 開場與環境 | 安裝依賴、解出 Plugin 並核對 SHA、`readiness`、`quality-gates`、`python --version` |
| 10–35 | `dlc-d1` | 共同語言與邊界 | `discover-sources` → 人工選來源 → `init-domain-memory` → `confirm-sources` → 以 `cite` 建 vocabulary／contexts／rules 候選 → `coverage` → `resolve-terms` → `get-context` → `analyze-boundary`（至少 2 個 Context） |
| 35–60 | `dlc-d2` | 審查與核准（成對） | `init-signing-key --key-file <忽略目錄或 %TEMP%> --sign-every-commit` → `amend-policy`（依 3.3 順序）→ `install-git-hitl-hook` → `governance-readiness` → Change Package → 夥伴 `record-approval` → 簽章 commit → attestation → `finalize-proposal` → `apply-approved-updates` → `validate --require-reviewed` → `verify-audit` |
| 60–70 | `dlc-break` | 休息 | — |
| 70–95 | `dlc-d3a` | 電子發票 | Port／Adapter、ACL、失敗隔離、冪等 |
| 95–125 | `dlc-d3b` | 點數折抵 | 決定 owner Context；跨 Membership／Pricing／Payment 的不變量；reserve／restore |
| 125–155 | `dlc-d3c` | 團體部分退款 | Aggregate 一致性邊界；每條新規則都有 counterfactual |
| 155–165 | `dlc-d4` | 交接 | `verify-sources`、`verify-evidence`、`verify-audit`；以 `upsert-candidate` 更新已變動事實；依 `implementation-handoff.md` 寫給下一個 Agent 的 Handoff |
| 165–180 | `dlc-retro` | 回顧 | 反思表；Domain Memory 對 Agent 行為的影響 |

Python `PLAN` 與 `materials-dlc/facilitator-deck/src/js/10-deck-core.js` 的 PLAN 必須一致，DLC 測試必須解析兩者比對。

### 3.2 解鎖群組與 Recovery

| 最早分鐘 | 群組 id | 解開內容 | 類型 |
|---|---|---|---|
| 00 | `open` | 開始之前、Runbook 用法、詞彙表（不得提供下載） | 不鎖 |
| 00 | `dlc-opening` | 環境準備、Plugin 與起始 Repo 下載（碼寫在第一張解鎖投影片） | 一般 |
| 10 | `dlc-d1` | D1 步驟、來源選擇表 | 一般 |
| 35 | `dlc-d2` | D2 步驟、角色卡、成對簽章流程 | 一般 |
| 70 | `dlc-d3a` | 情境卡 01、D3 決策卡 | 一般 |
| 95 | `dlc-d3b` | 情境卡 02 | 一般 |
| 125 | `dlc-d3c` | 情境卡 03 | 一般 |
| 155 | `dlc-d4` | D4 步驟、Handoff 範本 | 一般 |
| 165 | `dlc-retro` | 反思表 | 一般 |
| 35 | `dlc-rec-d1` | Repo＋已確認 source map＋D1 候選集 | Recovery |
| 45 | `dlc-rec-d2` | 主持人 reviewed Registry（D2 預設降級，成對簽章任一步卡住 5 分鐘即可公布） | Recovery |
| 95 | `dlc-rec-d3a` | D3a 參考解答清理版（揭曉後） | Recovery |
| 125 | `dlc-rec-d3b` | D3b 參考解答清理版（揭曉後） | Recovery |
| 155 | `dlc-rec-d3c` | D3c 參考解答清理版（揭曉後） | Recovery |

- Recovery 碼與一般碼分開、只按需公布；Recovery 不得作為小組成果評分。`dlc-rec-d3*` 只能在對應段揭曉頁之後公布。
- RECOVERY 接手會把維護者公鑰（allowed-signers 一行）複製到學員 `~/.dlc-keys`：僅公鑰，可接受。
- Recovery 包只含可接續的 Repo（含 `domain-memory/`），不含觀察指引、評分表、counterfactual 證據原稿或任何 `evaluation/` 檔案。
- 同一瀏覽器可同時開主課與 DLC Runbook：所有 localStorage 鍵必須以 `stwdlc:` 開頭，匯出檔名改為 `smart-ticket-dlc-runbook-<stamp>.zip`。

### 3.3 固定操作順序（來自 Spike，Runbook 與參考解答必須一致）

1. 簽章必須在**第一個** Registry commit 之前設定（`init-signing-key --sign-every-commit`），否則 push 會因先前未簽章 commit 被拒。
2. `amend-policy` 依序：`authorized_signers`（填 fingerprint）→ `review_trigger git-push` → `review_mode scm-verified --verifier git-signed-commit`；之後 `install-git-hitl-hook`，`governance-readiness` 必須回報 ready。
3. Change Package 放在 `domain-memory/changes/<id>/`，使簽章 commit 觸及 Registry 路徑但不改變 Registry digest。
4. proposer 不得 `record-approval`；`--reviewer` 必須是夥伴身分，簽章 commit 由持鑰夥伴執行。

## 4. 各段內容與驗收條件

> 2026-10-09 已核准變更（見第 1 節第 8 點與 [00 總控指令書 §1](00_Agentic工作坊素材產製總控指令書.md#1-專案目標)）：本節「可複製指令」改為寫進提示詞由 Agent 執行，學員不自行輸入；確認表單每段最多一張、以下拉／勾選為主。

每段 Runbook 必須有：目標一句、檢查點步驟（每步 ≤ 5 分鐘；例外見第 1 節第 13 項(d)）、提示詞（結尾固定「停下等我」）、確認表單（附建議膠囊選項）、卡關時的 Recovery 指引。投影只顯示時間、檢查點編號與一句話任務，不顯示主持專用內容。

### 4.1 開場與環境（0–10）

- 檢查點（四個，對應 `materials-dlc/CHECKPOINTS.md`）：依賴安裝與測試（76 passed）；Plugin 解出與 SHA 核對；`readiness`（brownfield）與 `quality-gates`（列出 pytest）；確認真實 Python（非 Store 別名）。環境／下載頁屬 `dlc-opening` 群組。
- 驗收：四點都有可複製指令（PowerShell 與 bash 兩版），且每點有「看到什麼算成功」的輸出片段。

### 4.2 D1 共同語言與邊界（10–35）

- 檢查點：D1-1 人工從 `discover-sources` 結果勾選來源（必含 `docs/requirements/`、`docs/adr/`、`src/`、`tests/`，排除 `**/__pycache__/**`）；D1-2 `init-domain-memory`（`--storage-mode tracked --review-mode local-draft-only`）＋`confirm-sources`；D1-3 以 `make_record.py`（內部呼叫 `cite`）建立 ≥5 個 vocabulary、≥2 個 contexts、≥2 個 rules 候選；D1-4 `coverage`、`resolve-terms`（用一句話查詢）、`get-context`、`analyze-boundary`（兩個不同 Context）。
- 教學重點：名稱矛盾（Fare Policy／Discount Policy、Compensation 無對應程式）、Context 邊界洩漏，均須讓學員在 `cite` 的證據中親眼看到。
- 驗收：`validate` 通過；`verify-evidence` 全部 current；每個候選至少一個 `cite` 證據；所有規則證據都在已確認來源內。

### 4.3 D2 審查與核准（35–60，成對）

- 角色：proposer（操作者機器）與 maintainer 夥伴（持鑰、核准、簽章）。兩人共用同一台機器時，夥伴金鑰一律放在 Repo 外的 `%USERPROFILE%\.dlc-keys\<夥伴代號>\`（Git Bash：`~/.dlc-keys/<夥伴代號>/`），不放 Repo 內的 `.dlc-keys/`、不放 `~/.ssh`。
- 檢查點：D2-1 夥伴 `init-signing-key`；D2-2 三次 `amend-policy`＋hook＋`governance-readiness` ready；D2-3 proposer 以 `fill_package.py` 建 Change Package 並 `validate-change-package`、`submit-proposal`；D2-4 夥伴 `record-approval`、`verify-proposal`、簽章 commit、`write_scm_attestation.py`、`verify-git-governance --commit`；D2-5 `finalize-proposal` → `apply-approved-updates` → `validate --require-reviewed` → `verify-audit`。
- 降級：任一步卡 5 分鐘，公布 `dlc-rec-d2`，小組改為對 reviewed Registry 執行 `validate --require-reviewed` 與 `verify-audit`，並觀看主持人示範簽章段落。
- 驗收：參考 Registry 與成對流程皆 `validate --require-reviewed` OK、`verify-audit` OK；`git log --show-signature` 可見核准 commit 已簽章；私鑰不在任何 commit、ZIP 或 Runbook 中。

### 4.4 D3 共同規則（70–155）

每個情境依同一節奏：讀情境卡 → `get-context`／`resolve-terms` 取得 reviewed 事實 → 寫 D3 決策卡（owner Context、不變量、外部系統、未知項）→ 交 Agent 實作 → 測試 → 每條新規則跑 `counterfactual` → 以 `upsert-candidate` 登記新事實（候選，不得自稱 reviewed）。參考解答的 Registry 狀態 = D2 reviewed Registry ＋ 新增／變更事實候選；D3 不 finalize Change Package（見第 1 節第 13 項）。
- 檢查點時窗：D3 步驟 3「Handoff 與 Agent 實作」為 7／8／9 分、D3c 步驟 4 為 6 分，屬已接受例外；緩解為情境卡 AC 的核心／延伸切分。

- **D3a 電子發票（70–95）**：`InvoiceIssuer` 類 Port 在 domain／application 邊界，Adapter 在 infrastructure；ACL 把 Order 翻譯為發票語言；付款成功不得因發票失敗回滾；以 order_id 冪等；不得持鎖做外部呼叫。驗收：Fake Adapter 可注入暫時性與永久性失敗，兩者各有測試。
- **D3b 點數折抵（95–125）**：先決定 owner Context 並記錄理由；餘額不為負、折抵後應付 ≥ 0 且為整數、先折扣後折抵；建立時 reserve、付款失敗或取消時 restore，不重複扣點。驗收：一般、團體、改票三條計價路徑都有測試，付款失敗返點有測試。
- **D3c 團體部分退款（125–155）**：Booking 為 Aggregate root，`cancel_passengers` 為唯一入口；累計退款 ≤ 已付金額；座位數 = 剩餘旅客數；同一旅客不得重複取消；全部取消等同整張退票。驗收：**每一條**新規則都有一次 killed 的 counterfactual 紀錄。

### 4.5 D4 交接（155–165）

- 檢查點：D4-1 `verify-sources`、`verify-evidence`、`verify-audit`；D4-2 對 D3 改變的事實 `upsert-candidate`；D4-3 依 `implementation-handoff.md` 七段（Domain facts、Forces、Decision、External systems、Unknowns、Proof obligations、Counterfactual check）填 Handoff 範本。
- 驗收：Handoff 範本七段齊全且只引用 Registry 中存在的 id。

### 4.6 回顧（165–180）

反思表至少問：哪個 reviewed 事實改變了 Agent 的輸出；哪個候選差點被當成事實；自我核准的儀式感與真實治理差在哪裡。

## 5. 學員素材規則

### 5.1 三分隔離與 Leakage

- `participant/` 下的任何檔案不得連到含 `facilitator`、`evaluation`、`instructions` 路徑段的位置，不得出現字面 `reference-solution` 或 `reference-solutions/`。
- Runbook forbidden markers（DLC edition 設定）：沿用主課 `facilitator`、`evaluation`、`reference-solution`、`reference answer`、`標準答案`，另加 `observation-guide`、`rubric`、`評分表`、`reference-registry`。`STUDENT_FARE_RATE` 對 DLC 不列入（起始 Repo 程式碼本來就含此常數，且只透過 ZIP 下載，不進 Runbook 文字）。
- 豁免只允許「頁 id＋精確片語」形式，寫在 DLC edition 設定並在 `materials-dlc/README.md` 逐條說明理由；不得對整頁或整個 marker 豁免。
- 學員可見文字不得出現主課內部代號（G0、G1、B0–B3、DEBT-、Level 1–3、Agent Production、Validation Report）。起始 Repo 以 `grep -rniE "B0|B1|B2|B3|G0|G1|DEBT|Evaluation|Participant|Reference|Validation Report|Level ?[123]|Agent Production|主持人|驗收|產製|Greenfield"`（排除 `.pyc`、`.venv`）檢查，每個殘留命中必須是刻意保留並在 facilitator guide 列明。

### 5.2 Windows 陷阱（素材必須事先處理，不得留給學員現場排除）

1. 所有 Plugin 指令經 `tools/dm.ps1`／`dm.sh`，固定 `py -3.13 -X utf8`（缺 `-X utf8` 會 cp950 UnicodeDecodeError）。
2. `counterfactual --test-command` 由 cmd.exe 執行：Runbook 範例一律用 `.venv\Scripts\python.exe -m pytest -q <test>` 這種反斜線或絕對路徑；並提醒錯誤路徑會印出 Big5 亂碼且 CLI 仍 exit 0，所以必須看到 `killed` 字樣才算數。
3. pre-push hook 呼叫裸 `python`：push 前必須啟用 Repo 的 `.venv`；E5 檢查點預先攔下 Store 別名。
4. 簽章先於第一個 Registry commit（見 3.3）。
5. Git Bash 與 PowerShell 的 `ssh-keygen` 不同，兩者皆可，但同一組全程用同一個 shell。
6. 依賴以 `pip install -r requirements.txt` 安裝（約 50 秒），不得要求 `pip install -e .`。

### 5.3 起始 Repo 允許的補強

僅允許：新增 `.gitattributes`，內容 `* -text`（已核准，停用換行轉換以保持 Plugin 引用雜湊穩定；金鑰放 Repo 外，故不再於 `.gitignore` 加入 `.dlc-keys/`）；README 補 DLC 前提（取代與情境衝突的「無外部服務」敘述）。不得修正刻意保留的設計洩漏，不得變更既有 76 個測試的行為。其他變更須回報使用者。

### 5.4 輔助腳本

- 只用標準函式庫；以 subprocess 呼叫 Plugin 的 `registry_tools.py`，不得 import 或修改 Plugin 內部。
- `make_record.py`：輸入 asset、id、名稱、定義與 `path:start-end`，輸出含 `cite` 證據的 record JSON。
- `fill_package.py`：填 requirement／proposal／obligations／evidence；測試結果必須來自實際 pytest exit code 與輸出 sha256，不得預填 PASS。
- `write_scm_attestation.py`：以指定 commit 寫出 `git-signed-commit` attestation。
- 每支腳本附一個 `__main__` 自檢或 `test_*.py`，於第 7 節執行。

## 6. 建置與打包

- DLC 建置：`python -X utf8 scripts/build_materials.py --edition dlc`；DLC edition 的 PLAN、段落 id、Recovery 群組、forbidden markers 與豁免集中於 edition 設定，不得散寫在 builder 主體。
- 打包：`scripts/package-manifest-dlc.json`（與主課同 schema），包別至少 `participant-dlc-00-open`、`participant-dlc-<段>`、`recovery-dlc-<段>`、`facilitator-dlc-before-session`、`evaluation-dlc-private`。學員來源路徑必須含 `participant` 段；輸出至 `dist/dlc-candidate/<manifest sha256 前 16 碼>/`，永不覆寫既有目錄；ZIP 固定時間戳與排序；`build-evidence.json` 另記錄 Python 與 zlib 版本。
- Runbook 只讀 DLC 候選包 ZIP 位元組並比對 `zip_sha256`，不得讀作者 Repo 的 facilitator／evaluation 目錄。
- 學員發放：只發 `dist/materials-dlc/participant-materials-dlc.zip`（內含 `runbook.html`）；不得覆寫 `dist/materials/participant-materials.zip`。
- 主課保護：DLC 工作不得變更 `scripts/package-manifest.json` 與主課候選；主課來源本身的修改依 [08 規範調整](08_全域驗證與受控打包產製指令書.md) 重驗並重新釘選；主課 `--check` 必須維持 UP-TO-DATE。若 builder 位元組變更迫使主課兩份 HTML 重建一次，差異僅限 build id／digest，且由 edition 平行工作負責記錄。

## 7. 驗證

所有指令於 Repo 根以 Python 3.13 執行，實際輸出摘要寫入 `dlc-validation-evidence.json`。

1. **Plugin 完整性**：解出的 Plugin 每檔 SHA256 與 `SHA256SUMS` 一致；`plugin.json` 版本為 0.10.15。
2. **起始 Repo**：全新 venv 安裝後 `pytest -q` 為 76 passed，無 Skip／XFail；第 5.1 節 grep 結果已審查。
3. **Reference Registry**：`validate --require-reviewed`、`verify-evidence`、`verify-sources`、`verify-audit`、`governance-readiness` 全部 OK；`coverage` 輸出已審查並記錄刻意未建模的缺口。
4. **參考解答（d3a、d3b、d3c 各自）**：pytest 全綠且無 Skip／XFail，記錄實際 passed 數；對各自 `domain-memory/` 執行 `validate`、`verify-audit`、`coverage` 皆 OK；已變動檔案上的 stale evidence 為預期，須列出（`verify-evidence`／`verify-sources` 可 exit 1，留到 D4）。
5. **Counterfactual**：每條新規則（三情境合計）各有一次 `counterfactual` 結果為 killed，原檔還原後全套測試仍全綠；列成「規則 id → 修改點 → 測試 → killed」對照表。
6. **成對簽章演練**：以兩個不同身分在乾淨複本上完整跑一次 D2，push 至本機 bare remote 被 hook 接受；另以未簽章 commit 驗證 push 被拒。
7. **輔助腳本**：每支自檢通過；以腳本重做 D1、D2 的計時（記錄分鐘數）。
8. **建置**：`build_materials.py --edition dlc` 兩次輸出位元組相同；`--edition dlc --check` 為 UP-TO-DATE；主課 `build_materials.py --check` 仍 UP-TO-DATE。
9. **DLC 測試**：`scripts/test_build_materials.py`（EditionTests）與 `scripts/test_build_delivery_dlc.py` 覆蓋 PLAN 連續且合計 180、Python／JS PLAN 一致、每個一般群組有對應 `data-unlock` 投影片且分鐘等於段落起點、碼與鎖定頁明文不出現在輸出、無外部 URL、forbidden marker 為零、下載 ZIP 雜湊屬於 DLC evidence、localStorage 鍵皆為 `stwdlc:`。
10. **全域**：`python -X utf8 scripts/validate_workshop.py --static-only`、`scripts/validate_consistency_corrections.py`、`python -m unittest discover -s scripts -p "test_*.py"` 與 `python -X utf8 scripts/build_delivery_dlc.py --verify <dir>` 通過；`git status` 確認主課 manifest 與凍結候選未變、`dist/` 未被追蹤、無私鑰檔被追蹤（`scan-secrets` exit 0；金鑰在 Repo 外，預期無 finding）。
11. **Leakage**：解開全部一般群組後，Runbook 不含 evaluation 原文、參考解答程式、觀察指引或評分表字句；Recovery 包內容符合第 3.2 節。
12. **瀏覽器冒煙**：實際瀏覽器以 `file://` 開啟兩份 HTML，完成翻頁、解鎖、下載、表單暫存、匯出、與主課 Runbook 同時開啟不互相污染，並截圖審視版面。

無法執行的項目必須標記 `NOT_RUN` 並寫明原因與補驗方式，不得宣稱 PASS。真人演練一律為 `NOT_RUN`，直到有真實場次證據。

## 8. 風險

| # | 風險 | 處置 |
|---|---|---|
| R1 | D1、D2 各 25 分鐘偏緊（Spike：候選 20–30 分、Change Package 30–45 分，主要耗在手打 JSON） | 輔助腳本；第 7.7 節實測計時；超時即公布 Recovery，不延長段落 |
| R2 | D3 三情境依序進行，任一段落後會連鎖拖延 | 每段揭曉後即可公布 `dlc-rec-d3*`；D3c 允許只完成 Aggregate 與兩條規則 |
| R3 | 自我核准淪為儀式：`record-approval` 只比對字串，同機雙身分仍可通過 | 成對分工；主持人明講此為教學示範而非安全保證；回顧題目直接討論 |
| R4 | 私鑰外洩至 commit、ZIP 或螢幕截圖 | 金鑰放 Repo 外的 `%USERPROFILE%\.dlc-keys\`；`scan-secrets` 與打包檢查；課後提示刪除 |
| R5 | Windows：cp950、cmd.exe 路徑、裸 `python`、未簽章歷史 commit | 第 5.2 節全部預先處理並在 E 檢查點攔截 |
| R6 | counterfactual 指令錯誤時仍 exit 0，學員誤認 killed | 只認輸出中的 killed 字樣；參考證據逐條人工核對 |
| R7 | forbidden marker 誤殺 DDD 用語（如 evaluation） | 先掃草稿；精確片語豁免並說明 |
| R8 | 起始 Repo 測試直接戳 store 內部，重構變成修測試 | 情境卡與決策卡明示可改寫哪些測試；參考解答記錄改寫理由 |
| R9 | Plugin 內 `.md` 若以展開樹放入 `agentic-workshop/` 會被 `validate_workshop.documents()` 掃描，且不得修改 | 以 ZIP 原樣封裝，不展開進 Repo |
| R10 | 主課與 DLC 共用 builder，DLC 變更波及主課 | 第 6 節主課保護與第 7.8、7.10 節回歸 |

## 9. 未決事項

1. D3 是否全體依序做三個情境：**已核准為依序、全做**（2026-10-07）。
2. D2 每組人數為奇數時的第三人角色（建議：observer 負責核對 `verify-audit` 輸出），待使用者確認。
3. 學員機器是否保證有 Python 3.13 與 `py` launcher；若無，需決定 Preflight 安裝方式或改用可攜版本。
4. D3c 退款手續費與時間門檻規則以情境卡為準；若情境卡未定，參考解答不得自創，須回報。
5. 是否需要主持人用的 D2 完整示範錄影作為現場備援。

## 10. Coding Agent 最終回報格式

```markdown
# DDD DLC 產製結果

## 產製檔案

## Plugin 封裝與 SHA 核對

## 起始 Repo 檢查（測試數、殘留字詞審查）

## Reference Registry 驗證

## 參考解答驗證（d3a／d3b／d3c：passed 數、Change Package 狀態）

## Counterfactual 對照表

## 成對簽章演練

## 輔助腳本與計時實測

## 建置、打包與主課回歸

## Participant Leakage Check

## NOT_RUN 項目與補驗方式

## 與上位規格的一致性檢查

## 已知限制

## Final Decision
```

Final Decision 僅可為 `PASS FOR WORKSHOP USE` 或 `FAIL`；任何第 7 節項目為 FAIL 時必須為 `FAIL`。

## 完成條件

- 第 2 節產出齊備，且未新增表外頂層資料夾。
- Plugin 0.10.15 原樣封裝，SHA 清單核對通過。
- 時程連續、合計 180 分鐘，九段與第 3.1 節一致；每個 D 段有檢查點、「停下等我」提示詞、確認表單、獨立解鎖碼與 Recovery。
- 第 3.3 節操作順序與第 5.2 節 Windows 陷阱在 Runbook 與參考解答中一致處理。
- 三個參考解答測試全綠；其 `domain-memory/` 的 `validate`、`verify-audit`、`coverage` OK（stale evidence 已列出）；reference Registry（D2）`validate --require-reviewed` 與 `verify-audit` OK；每條新規則有 killed counterfactual。
- Participant、Facilitator、Evaluation 隔離，Leakage Check 通過，私鑰未被追蹤或打包。
- 主課 `package-manifest.json`、主課候選未因 DLC 工作而變，主課 `--check` UP-TO-DATE。
- 第 7 節結果如實記錄，NOT_RUN 有原因；未經使用者要求不得 Commit。
