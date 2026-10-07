# DDD DLC 主持人手冊

> 對象：DDD DLC（180 分鐘加課）的主持人與助教。學員已完成主課（Tool → Teammate → Digital Worker）。
> 主題：**Agent 的領域記憶**。把領域知識做成經審查、以檔案保存的 Domain Memory，再用它驅動受治理的變更。DDD 概念全部透過 domain-memory Plugin 0.2.2 的操作來教，不開理論講堂。
> 依據：`docs/instructions/11_DDD_DLC產製指令書.md`（以下稱「規格」）。檢查點以 `agentic-workshop/materials-dlc/CHECKPOINTS.md` 為準，解鎖碼在 `agentic-workshop/materials-dlc/unlock-codes.json`（本手冊不重抄碼，避免兩份不一致）。
> 本手冊與 `evaluation/` 底下所有檔案只給主持人，**不得**放進學員包、Runbook 或投影。

## 0. 一頁摘要

| 分鐘 | 段落 | 投影 | 你要做的關鍵動作 |
|---|---|---|---|
| 0–10 | 開場與環境 | 解鎖頁 → 4 個檢查點 | 盯 C:\dlc 短路徑、Store 別名、SHA 核對；第 7 分配對 |
| 10–35 | D1 共同語言與邊界 | 6 個檢查點 | 名稱矛盾與邊界洩漏要讓學員在 `cite` 證據中親眼看到 |
| 35–60 | D2 審查與核准（成對） | 6 個檢查點 | 第 45 分或卡 5 分鐘公布 `dlc-rec-d2`；示範簽章 |
| 60–70 | 休息 | 休息頁 | 巡 D2 落後組，確認大家都有可接續的 reviewed Registry |
| 70–95 | D3a 電子發票 | 6 個檢查點 → 停手 → 2 頁揭曉 | 解鎖時宣布核心／延伸與 API 小節；揭曉後才可發 `dlc-rec-d3a` |
| 95–125 | D3b 點數折抵 | 同上 | 同上；`dlc-rec-d3b` |
| 125–155 | D3c 團體部分退款 | 同上 | **最重的一段**：保住 Review 時間；`dlc-rec-d3c` |
| 155–165 | D4 交接 | 3 個檢查點 | stale 證據不准跳過；更新事實只到候選 |
| 165–180 | 回顧 | 4 個檢查點 | 討論「自我核准的儀式感 vs 真實治理」 |

三條不可破的規則：

1. **不延長段落**。落後就用 Recovery 接續，記錄原因與時間。
2. **Recovery 不作為小組成果評分**，只按需私下提供（Recovery 碼只在講者備註 `data-code`，不投影、不貼群組）。
3. **`dlc-rec-d3*` 只能在對應段的揭曉頁之後**提供。

## 1. 課前檢查清單

### 1.1 一週前

- [ ] 確認學員機器：Windows 10/11，可裝軟體或已預裝下列項目。
- [ ] **Python 3.13 與 `py` launcher**：`py -3.13 --version` 要有回應。沒有 launcher 的機器，請學員用 python.org 安裝程式重裝並勾選 py launcher（規格 §9 第 3 點尚未決定是否提供可攜版；若教室不允許安裝，課前要決定替代方案）。
- [ ] **Git for Windows ≥ 2.34**（SSH 簽章需要）：`git --version`。
- [ ] 每台機器一個可讀寫本機資料夾、能執行終端指令的通用 Coding Agent。
- [ ] 通知學員：學員包一律解壓到 **`C:\dlc`**（不要放桌面、OneDrive、深層資料夾）。原因見 §5 陷阱 1（WinError 206）。
- [ ] 建置並驗證候選包（維護者）：

```powershell
py -3.13 -X utf8 scripts/vendor_dlc_plugin.py --check
py -3.13 -X utf8 scripts/build_delivery_dlc.py
py -3.13 -X utf8 scripts/build_delivery_dlc.py --verify dist/dlc-candidate/<id>
py -3.13 -X utf8 scripts/build_materials.py --edition dlc --check
```

### 1.2 要準備的檔案

| 檔案 | 給誰 | 備註 |
|---|---|---|
| `dist/materials-dlc/participant-materials-dlc.zip`（內含 `runbook.html`） | 學員 | 唯一發給學員的檔案。Runbook 內嵌各段學員包與 Recovery ZIP，解鎖後才能下載。 |
| `agentic-workshop/materials-dlc/facilitator-deck/facilitator-deck.html` | 主持人 | 投影用。按 `T` 開段落計時；講者模式看備註與 Recovery 碼。 |
| `agentic-workshop/materials-dlc/unlock-codes.json` | 主持人 | 一般碼 8 組、Recovery 碼 5 組。 |
| `facilitator-dlc-before-session`（本資料夾） | 主持人 | 本手冊、`recovery/` 原始來源。 |
| `evaluation-dlc-private` | 主持人 | 觀察指引 `evaluation/observation-guide.md`、reference Registry、三份參考解答。 |

### 1.3 Plugin SHA

- Plugin 固定 0.2.2，原樣封裝於 `participant/vendor/domain-memory-0.2.2.zip`，逐檔清單 `domain-memory-0.2.2.zip.SHA256SUMS`（129 個 Plugin 檔案＋ZIP 本身＝130 行）。
- 目前 ZIP 的 SHA256：`de6aad75f86ce4fe534271d62f7cf21ce09876cc127e68dbc96416c9c31c89dc`（重新封裝後以 SHA256SUMS 最後一行為準）。
- 學員在開場檢查點 2 應看到 `SHA OK 130 files` 與 `"version": "0.2.2"`。看到 `SHA MISMATCH` 一律停用該份 Plugin，換一份重新下載；不要「先用用看」。

### 1.4 主持人自己的機器（課前 30 分鐘）

- [ ] 在自己的機器以學員身分走完開場四個檢查點（約 3 分鐘＋安裝 50 秒）。
- [ ] 還原一次 reference Registry（見 `evaluation/reference-registry/README.md`「還原」），確認 `validate --require-reviewed`、`verify-audit`、`verify-git-governance` 全 OK。D2 示範與降級都靠它。
- [ ] 準備 D2 示範用的兩個身分：`proposer@example.com`、`maintainer@example.com`；示範金鑰放 `%USERPROFILE%\.dlc-keys\demo-maintainer\`。
- [ ] 投影開啟 `facilitator-deck.html`，副螢幕開講者模式，確認 Recovery 碼只出現在講者畫面。

### 1.5 起始 Repo 殘留字詞審查（規格 §5.1）

以規格 §5.1 的 grep（排除 `.pyc`、`.venv`、`.git`）掃 `participant/repository/smart-ticket-dlc-base/`：**零命中**（2026-10-07 實測）。沒有需要刻意保留的殘留。若之後修改起始 Repo，重跑並把每個命中與保留理由補在這裡。

## 2. 教室配置與分組

- **兩人一組、一台機器**。選 D1 做得比較完整的那台；它的主人當 **Proposer**（提案、操作 Change Package，不得自己核准），另一人當 **Maintainer**（持簽章金鑰、核准、簽章 commit）。
- 開場第 7 分鐘（「找夥伴」頁）就配好對；D1 各人在自己的 Repo 做，D2 起兩人共用一台機器。開場有人環境裝不起來，D1 起先以夥伴的機器為主。
- **人數奇數時組成三人組，第三人當 Observer**：對照 Runbook 的「D2 簽章流程清單」，確認每一步是對的人在做（proposer 不碰 `record-approval`、簽章 commit 由 Maintainer 執行），並核對 `verify-audit` 輸出。D3 起 Observer 負責對照決策卡與記錄 counterfactual 結果。
- D3 三段角色可以輪換，但 **Maintainer 的私鑰不換人**：只有持鑰人能簽觸及 Registry 的 commit。
- 座位安排讓兩人能同時看同一個螢幕；助教巡堂路線要能看到螢幕上的終端機輸出。
- 明講（規格 R3）：`record-approval` 只比對身分字串，同機雙身分仍可通過；今天的成對簽章是**教學示範，不是安全保證**。治理強度來自「誰持有簽章私鑰」。

## 3. 逐段腳本

每段固定節奏：解鎖頁（大字解鎖碼）→ 檢查點總覽頁（按 `T` 開段落計時，時間軸自動標示目前檢查點）→ 每到時間點翻到下一個檢查點頁。投影只顯示時間、檢查點編號與一句話任務；指令、提示詞、表單都在 Runbook。各頁講者備註有「說／看／介入訊號／提示」，本節只列每段的骨架與決策點。

### 3.1 開場與環境（0–10，群組 `dlc-opening`）

| 分鐘 | 檢查點 | 你說／做 |
|---|---|---|
| 0 | 解鎖 | 公布開場解鎖碼；請學員下載 `participant-dlc-open.zip`、解壓到 `C:\dlc` |
| 0–3 | 1 · 依賴安裝與測試 | `pip install -r requirements.txt`（約 50 秒），`pytest -q` 為 **76 passed**；不需要 `pip install -e .` |
| 1–2 | （等待安裝時） | 「為什麼是 Domain Memory」「今天怎麼進行」兩頁 |
| 3–5 | 2 · Plugin 解出與 SHA 核對 | `SHA OK 130 files`、`"version": "0.2.2"` |
| 5–8 | 3 · readiness 與 quality-gates | 經 `tools/dm.ps1`／`dm.sh`：`readiness` 說 brownfield，`quality-gates` 列 pytest |
| 7 | 找夥伴 | 配對；奇數時三人組，第三人 Observer |
| 8–10 | 4 · 確認真實 Python | 啟用 venv，`python` 路徑在 `.venv\Scripts\`、不含 `WindowsApps`；起始 commit；`doctor.py` 全 `[OK]` |

降級：第 10 分鐘仍有人未過 → 兩人一機繼續，D1 以夥伴機器為主；記錄耗時，不延長本段。

### 3.2 D1 共同語言與邊界（10–35，群組 `dlc-d1`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 10–13 | 1 · 人工選來源 | `discover-sources` 後**人工**勾選；必含 `docs/requirements/`、`docs/adr/`、`src/`、`tests/`，排除 `**/__pycache__/**` |
| 13–17 | 2 · 初始化與確認來源 | `init-domain-memory --storage-mode tracked --review-mode local-draft-only` ＋ `confirm-sources` |
| 17–22 | 3 · 詞彙候選 | `make_record.py`（內部呼叫 `cite`）建 ≥ 5 個 vocabulary |
| 22–27 | 4 · Context 與規則候選 | ≥ 2 個 contexts、≥ 2 條 rules |
| 27–31 | 5 · coverage 與 resolve-terms | 用一句話查詢 |
| 31–35 | 6 · get-context 與 analyze-boundary | 兩個不同 Context |

教學重點：名稱矛盾（Fare Policy／Discount Policy、Compensation 沒有對應程式）與 Context 邊界洩漏，**一定要讓學員在 `cite` 的證據裡親眼看到**，不要口頭告訴他們。

Recovery：第 35 分鐘 D1 未完成的組，私下提供 `dlc-rec-d1`（Repo＋已確認 source map＋D1 候選集，全部為候選）。

### 3.3 D2 審查與核准，成對（35–60，群組 `dlc-d2`）

| 分鐘 | 檢查點 | 誰 | 重點 |
|---|---|---|---|
| 35–38 | 1 · 夥伴建立簽章金鑰 | Maintainer | `init-signing-key --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit`（Git Bash：`"$HOME/.dlc-keys/maintainer/signing-key"`）；**先於第一個 Registry commit** |
| 38–43 | 2 · 政策、hook、readiness | Maintainer | `amend-policy` 依序 `authorized_signers`（fingerprint）→ `review_trigger git-push` → `review_mode scm-verified --verifier git-signed-commit`；`install-git-hitl-hook`；`governance-readiness` ready |
| 43–48 | 3 · Change Package 與提交 | Proposer | `fill_package.py`（測試實際執行，不預填 PASS），放 `domain-memory/changes/<id>/`；`submit-proposal` |
| 48–53 | 4 · 核准與簽章 commit | Maintainer | `record-approval --reviewer maintainer@example.com`、`verify-proposal`、`git commit -S` |
| 53–56 | 5 · attestation | Maintainer | `write_scm_attestation.py --commit HEAD`、`verify-git-governance --commit HEAD` |
| 56–60 | 6 · finalize 與驗證 | 兩人 | `finalize-proposal` → `apply-approved-updates` → `validate --require-reviewed` → `verify-audit`；簽章 commit、`setup_remote.py`、push |

**Recovery 釋放規則（`dlc-rec-d2`）**：

- 最早第 **45** 分鐘可用（規格 §3.2）。
- 任一組在任一步**卡住 5 分鐘**即可私下提供；第 45 分多數組還沒 `submit-proposal` 時，對卡住的組提供。
- 改用 Recovery 的組：對 reviewed Registry 跑 `validate --require-reviewed` 與 `verify-audit`，然後看你的簽章示範（下方）。要在 D3 之後繼續 push，照 `recovery/d2/RECOVERY.md` 第 4 節以自己的金鑰接手；**附加 maintainer 的 allowed_signers 那一行不能省**，否則歷史 commit 驗不過、push 被拒。

**成對簽章示範腳本（約 4 分鐘，用 reference Registry 或自己的乾淨複本）**：

1. 「Proposer 做完 Change Package，現在換 Maintainer 坐到鍵盤前。」示範 `record-approval --reviewer maintainer@example.com`。順便示範反例：以 `proposer@example.com` 當 reviewer 會被拒；再說明以另一個字串也能通過，**所以真正的保護是簽章**。
2. `git -c user.name="DLC Maintainer" -c user.email=maintainer@example.com commit -S -m "..."`，接著 `git log --show-signature -1`，指出 `Good "git" signature for maintainer@example.com`。
3. `write_scm_attestation.py --commit HEAD` → `verify-git-governance --commit HEAD`：「核准證據不是一行文字，是一個可驗證的已簽章 commit。」
4. （有時間）做一個不簽章、觸及 `domain-memory/` 的 commit 再 push，給大家看 hook 拒絕的輸出。
5. 收尾：「私鑰在 `%USERPROFILE%\.dlc-keys\`，不在 Repo、不在 `.ssh`、不截圖。課後刪掉。」

### 3.4 休息（60–70）

巡一圈：每組都要有一份 `validate --require-reviewed` OK 的 Registry（自己的或 Recovery），D3 才接得下去。還沒有的組，休息時協助還原 `dlc-rec-d2`。

### 3.5 D3 共同節奏（70–155）

三個情境**全體依序、三個都做**，每段在前一段成果上累積。每段六個檢查點同一個節奏：

1. 讀情境卡、`resolve-terms`／`get-context` 取 reviewed 事實，已知與未知分開寫。
2. 由**人**寫 D3 決策卡：owner Context、不變量、外部系統、未知項。
3. 決策卡交 Agent：先提計畫、等核准、做完停下；看**實際** `pytest -q`。
4. 每條新規則各一次 `counterfactual`，只認 `killed`。
5. 人 Review Diff；新事實用 `upsert-candidate` 登記，**仍是候選**。
6. 停手 → 「請先停手」頁 → 兩頁揭曉 → 學員記一個差異與理由。

**解鎖時就宣布兩件事**（三段都一樣，講者備註有提示）：

- **核心／延伸**：情境卡「本次範圍」已把每條 AC 標成［核心］或［延伸］。先做完核心；延伸只在時間允許時做。沒做延伸時，核心行為仍須完整可用。
- **API 小節**：卡上已定義路徑、欄位與錯誤碼。叫學員先看，並在 Handoff 中要求 Agent 照卡做，不准自己發明介面。這省下的時間要留給 Review 與 counterfactual。

各情境核心／延伸：

| 情境 | 核心（必做） | 延伸（時間允許） | 建議現場 counterfactual |
|---|---|---|---|
| D3a 電子發票 | EINV-001、002、003、005、006、007、008、009、010、011、015 | EINV-004、012、013、014 | 重試上限 `MAX_ISSUE_ATTEMPTS`；鎖外呼叫；冪等鍵 `merchant_order_no` |
| D3b 點數折抵 | PTS-001、003、004、005、006、007、008、009、010、012、014 | PTS-002、011、013、015 | 上限以優惠後總額計（只有 665 抓得到）；預留在寫入前；團體付款失敗歸還；退款現金＝Order.amount（要有改票後退票測試） |
| D3c 團體部分退款 | PCR-001、003、004、005、006、007、008、009、011、012 | PCR-002 完整驗證、010、013、014、passenger_id 唯一性 | 手續費逐位／以自己的票價（要有混合團測試）；先決定再釋放；部分取消後不可整筆退；只釋放被取消者的座位 |

**揭曉與 Recovery 規則**：第 6 個檢查點開始時翻到「請先停手」頁，確認全員停手後才翻揭曉頁。揭曉頁講「設計判斷與理由」，不現場補寫答案程式，不說「標準答案」。揭曉之後，落後的組才可私下拿到該段的 `dlc-rec-d3*`，用它接續下一段。

### 3.6 D3a 電子發票（70–95，群組 `dlc-d3a`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 70–73 | 1 · 讀卡與 reviewed 事實 | 宣布核心／延伸與 API 小節。H1：「逾時代表什麼？對方可能已經開出發票了嗎？」 |
| 73–78 | 2 · Port 與邊界決策 | 發票歸哪個 Context？Port 放哪層？誰把 Order 翻成發票語言？H2：「付款 Gateway 沒有 Port，這次要照做還是改？」 |
| 78–85 | 3 · Handoff 與 Agent 實作 | 盯鎖：`pay_group` 持有 RLock 時呼叫 `pay`；盯「付款請求內同步重試 5 次」 |
| 85–89 | 4 · Counterfactual | 先做建議的 3 個 |
| 89–92 | 5 · Review 與候選 | 有沒有供應商代碼（`9001`、`2001`）出現在 Domain／Service |
| 92–95 | 6 · 停手與揭曉 | 揭曉：新的 Invoicing Context；Port `InvoiceIssuer` 只回 ISSUED／REJECTED／UNAVAILABLE；Adapter 翻譯代碼、逾時、連線失敗；鎖內只建 PENDING，鎖外呼叫一次；冪等鍵＝order_id |

時間判斷：參考解答完整 15 條 AC 約 270 行程式＋300 行測試，25 分鐘只夠核心切片。第 85 分 Agent 還沒做完核心也要進 counterfactual。

### 3.7 D3b 點數折抵（95–125，群組 `dlc-d3b`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 95–98 | 1 · 讀卡與 reviewed 事實 | 宣布核心／延伸與 API 小節。H1：「折抵要加在哪裡，才不會漏掉其中一條計價路徑？」 |
| 98–103 | 2 · Owner Context 與不變量 | 點數歸誰、理由；30% 上限歸誰；reserve／restore 的時機。H2：「預留要不要成為獨立概念？」 |
| 103–111 | 3 · Handoff 與 Agent 實作 | 盯「點數塞進 `DiscountPolicy`」與「從 `total_fare` 扣點」；扣點位置要在座位規劃之後、寫入之前 |
| 111–116 | 4 · Counterfactual | 建議的 4 個，其中「上限以優惠後總額」「退款＝Order.amount」是先 survived 再補測試的好示範 |
| 116–121 | 5 · Review 與候選 | 商業數字（30、100）是否只有一個家 |
| 121–125 | 6 · 停手與揭曉 | 揭曉：Membership 擁有點數與折抵規則（含 30% 上限）；Pricing 與三條計價迴圈一行不改；Booking 記折抵點數、推導 `payable_amount`；閘道扣 `payable_amount`＝Order.amount；發票自動是 500 → 476＋24 |

時間判斷：程式只約 +80 行，核心切片可行；省下的時間給 Review。D3a 未完成的組，揭曉 D3a 後已可用 `dlc-rec-d3a` 接續，本段不用從頭補 D3a。

### 3.8 D3c 團體部分退款（125–155，群組 `dlc-d3c`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 125–128 | 1 · 讀卡與 reviewed 事實 | 宣布核心／延伸與 API 小節，並明講「本段最緊，延伸一律最後」。H1：「現在的退款紀錄能表達『同一筆訂票退過兩次』嗎？」 |
| 128–133 | 2 · Aggregate 邊界與不變量 | Aggregate root、唯一入口、恆等式誰保證、手續費歸誰、退款紀錄結構 |
| 133–142 | 3 · Handoff 與 Agent 實作 | Handoff 要有「四份座位資料」「先拒絕再修改」「不要動 `total_fare`」與混合團範例 |
| 142–148 | 4 · Counterfactual | 建議的 4 個；第 142 分沒做完也進來 |
| 148–152 | 5 · Review 與候選 | **不可壓縮**。看整筆退票路徑、恆等式在哪裡成立、座位四份是否一致 |
| 152–155 | 6 · 停手與揭曉 | 揭曉：團體 Booking 擁有旅客取消（`cancel_passengers` 唯一入口，全部檢查完才寫入）；費率帶與 D ≤ 0 不受理在同一模組、逐位向下取整；只釋放被取消旅客的座位；退款紀錄改 append-only 清單；部分取消過不可整筆退 |

**時間風險：這是三張卡最重的一張**。參考解答 +141 行、是唯一需要改既有資料結構的一張；核心切片勉強放得下，前提是學員從第 125 分就照卡上的 API 做。規格 R2 允許只完成 Aggregate 與兩條規則。寧可少做 AC，也不要吃掉第 148–152 分的 Review：本段教學重點全在 Review。

### 3.9 D4 交接（155–165，群組 `dlc-d4`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 155–158 | 1 · 驗證 | `verify-sources`、`verify-evidence`、`verify-audit`。D3 改過的檔案會是 `stale`、exit 1，這是預期，不准跳過 |
| 158–161 | 2 · 更新已變動事實 | `upsert-candidate`，只到候選。參考：D3c 讓 `REFUND-004`、Booking 的「只能退一次」與 `ASIS-004` 不再成立 |
| 161–165 | 3 · 寫 Handoff | 依 `implementation-handoff.md` 七段（Domain facts、Forces、Decision、External systems、Unknowns、Proof obligations、Counterfactual check），只引用 Registry 中存在的 id |

D3c 未完成者仍可用 `dlc-rec-d3c`（D3c 揭曉後）接續 D4。

### 3.10 回顧（165–180，群組 `dlc-retro`）

四個檢查點：個人反思（165–169）、小組比較（169–174）、收斂與行動（174–178）、匯出與結束（178–180）。必問：

1. 哪一個 reviewed 事實改變了 Agent 的輸出？
2. 哪一個候選差點被當成事實？
3. 自我核准的儀式感和真實治理差在哪裡？（直接回到 R3：`record-approval` 只比字串）

最後提醒匯出 Runbook（`smart-ticket-dlc-runbook-<stamp>.zip`），以及課後刪除金鑰（§7）。

## 4. 解鎖碼與 Recovery 釋放規則

| 群組 | 最早分鐘 | 類型 | 釋放條件 |
|---|---:|---|---|
| `open` | 0 | 不鎖 | — |
| `dlc-opening`、`dlc-d1`、`dlc-d2`、`dlc-d3a`、`dlc-d3b`、`dlc-d3c`、`dlc-d4`、`dlc-retro` | 0、10、35、70、95、125、155、165 | 一般 | 該段解鎖頁大字公布 |
| `dlc-rec-d1` | 35 | Recovery | D1 未完成者，第 35 分起私下提供 |
| `dlc-rec-d2` | 45 | Recovery | 第 45 分起；或任一組任一步卡 5 分鐘 |
| `dlc-rec-d3a` | 95 | Recovery | **D3a 揭曉頁之後**才可提供 |
| `dlc-rec-d3b` | 125 | Recovery | **D3b 揭曉頁之後**才可提供 |
| `dlc-rec-d3c` | 155 | Recovery | **D3c 揭曉頁之後**才可提供 |

- Recovery 碼與一般碼分開、只按需提供，不投影、不貼群組；Recovery 不作為小組成果評分。
- 使用 Recovery 的組在 Runbook 表單如實記錄觸發原因與時間（Runbook 已有欄位）。
- Recovery 包只含可接續的 Repo（含 `domain-memory/`），不含觀察指引、counterfactual 證據原稿或任何 `evaluation/` 檔案。
- D3a／D3b／D3c 的 Recovery 還原後，`verify-evidence`／`verify-sources` 會對改過的檔案回報 `stale`、exit 1，屬預期，留到 D4 處理。最上面的「Recovery 參考實作」commit 是 `N`（未簽章），因為它不碰 Registry，hook 允許。

## 5. Windows 已知陷阱與修正

| # | 症狀 | 原因 | 修正 |
|---|---|---|---|
| 1 | D1 寫 Registry 時「檔名或副檔名太長」`WinError 206` | Plugin 在 `domain-memory/` 底下建很長的暫存資料夾名；放在桌面、OneDrive 或深層資料夾就超過路徑上限 | 解壓到 `C:\dlc`（Recovery 用 `C:\dlc-rec\<段>`）。已出錯的組：整個資料夾搬到 `C:\dlc` 再重跑該步 |
| 2 | `UnicodeDecodeError: 'cp950' codec ...` | 直接呼叫 `registry_tools.py`，缺 `-X utf8` | 一律經 `tools\dm.ps1`／`dm.sh`（固定 `py -3.13 -X utf8`） |
| 3 | counterfactual 印出亂碼（Big5）並以 ERROR 結束（exit 1） | `--test-command` 由 cmd.exe 執行，直譯器路徑寫錯 | 寫 `.venv\Scripts\python.exe -m pytest -q <測試>`（反斜線）。**只認輸出中的 `killed`**；`failing_evidence` 要是 assertion 失敗 |
| 4 | push 時 hook 失敗、或跳出 Microsoft Store | pre-push hook 呼叫裸 `python`，`python` 是 Store 別名（路徑含 `WindowsApps`） | push 前啟用 Repo 的 `.venv`；或關閉「應用程式執行別名」。開場檢查點 4 就要攔下 |
| 5 | push 被拒「Git commit signature is invalid」或未簽章 | 簽章在第一個 Registry commit 之後才設定；或 Recovery 接手時沒附 maintainer 的 allowed_signers | 簽章先於第一個 Registry commit（`--sign-every-commit`）；Recovery 照 RECOVERY.md 第 4 節附上 allowed_signers 那一行 |
| 6 | 新開的終端機裡 `python` 又不對 | venv 只對目前視窗有效 | 每個新視窗：PowerShell `Set-ExecutionPolicy -Scope Process Bypass -Force` ＋ `.\.venv\Scripts\Activate.ps1`；Git Bash `source .venv/Scripts/activate` |
| 7 | `ssh-keygen` 行為不同、金鑰路徑找不到 | Git Bash 與 PowerShell 的 `ssh-keygen` 不同 | 兩者皆可，但同一組全程用同一種 shell |
| 8 | clone／還原後引用全部變成 `changed` | `core.autocrlf=true` 轉換換行，Plugin 以原始位元組算雜湊 | 起始 Repo 已有 `.gitattributes`（`* -text`）；`doctor.py` 會檢查。不要刪它 |
| 9 | push 時 hook 輸出亂碼或編碼錯誤 | hook 內 Python 用系統編碼 | Runbook 已在 push 前設 `$env:PYTHONUTF8 = '1'`（Git Bash `export PYTHONUTF8=1`） |
| 10 | 安裝很久或有人跑 `pip install -e .` | 不需要可編輯安裝 | 只用 `pip install -r requirements.txt`（約 50 秒） |
| 11 | `scan-secrets` 有 finding | 金鑰放進 Repo 內（含被忽略的資料夾；scan-secrets 會掃）或 `.ssh` | 金鑰只放 `%USERPROFILE%\.dlc-keys\<代號>\`（Git Bash `~/.dlc-keys/<代號>/`），預期 exit 0 |
| 12 | PowerShell 說「已停用指令碼」 | 執行原則 | `Set-ExecutionPolicy -Scope Process Bypass -Force`（只影響目前視窗） |

## 6. 時間風險

| 風險 | 早期訊號 | 處置 |
|---|---|---|
| D1、D2 各 25 分鐘偏緊（規格 R1） | 第 22 分還不到 3 個詞；第 45 分還沒 submit | 不延長；第 35 分 `dlc-rec-d1`、第 45 分或卡 5 分鐘 `dlc-rec-d2` |
| D3 依序進行，一段落後連鎖拖延（R2） | 第 85／111／142 分 Agent 還在寫核心 | 照樣進 counterfactual 與 Review；揭曉後用 `dlc-rec-d3*` 接續下一段 |
| **D3c 最重** | 第 133 分還在討論邊界；第 142 分核心未完成 | 只做 Aggregate 與兩條規則也合格；**保住第 148–152 分 Review**；延伸全部放棄 |
| Agent 自己發明 API | 決策卡沒提 API、Agent 計畫裡出現卡上沒有的路徑 | 叫他們回到卡上「API」小節，Handoff 明寫「介面照卡」 |
| 延伸 AC 吃掉時間 | 在核心沒做完前做發票資訊驗證、Audit、查詢欄位 | 指著卡上的［延伸］標記：「這些最後做」 |
| counterfactual 誤判（R6） | 只看 exit code | 只認 `killed`；看 `failing_evidence` 是 assertion 而不是 import／語法錯誤 |

## 7. 課後清理

- [ ] 請每位學員刪除簽章金鑰資料夾：PowerShell `Remove-Item -Recurse -Force "$env:USERPROFILE\.dlc-keys"`；Git Bash `rm -rf ~/.dlc-keys`。主持人示範金鑰同樣刪除。
- [ ] 確認沒有人把 `signing-key`（無副檔名的私鑰檔）複製進 Repo、貼到 Agent、表單或聊天、或出現在截圖。
- [ ] 公用電腦：刪除 `C:\dlc`、`C:\dlc-rec`；清除瀏覽器中 `stwdlc:` 開頭的 Runbook 暫存（或請學員在 Runbook 內清除）。
- [ ] 收回學員匯出的 Runbook ZIP（若有收集），存放時視為個人資料。
- [ ] 記錄本場：各組使用了哪些 Recovery、在第幾分鐘；哪些段落超時；這些資料回填規格 §7 的真人演練紀錄（未有實際場次前，該項一律 `NOT_RUN`）。

## 8. 參考

- 觀察與介入：`evaluation/observation-guide.md`
- 參考 Registry 與還原：`evaluation/reference-registry/README.md`
- 參考解答與 Agent 常見錯誤：`evaluation/reference-solutions/{d3a-e-invoice,d3b-points-redemption,d3c-group-partial-refund}/SOLUTION-NOTES.md`
- Recovery 原始來源：`facilitator/recovery/<段>/RECOVERY.md`
