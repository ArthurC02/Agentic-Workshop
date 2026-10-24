# DDD DLC 主持人手冊

> 對象：DDD DLC（255 分鐘加課）的主持人與助教。學員已完成主課（Tool → Teammate → Digital Worker）。
> 主題：**和 Coding Agent 一起做 DDD**：Agent 找證據、提選項、實作；學員定義模型、做決定、用證據驗收。domain-memory Plugin 4.2.0 只是保存共用模型的工具，指令全在提示詞裡。不開理論講堂。
> 依據：`docs/instructions/11_DDD_DLC產製指令書.md`（以下稱「規格」）。檢查點以 `agentic-workshop/materials-dlc/CHECKPOINTS.md` 為準，解鎖碼在 `agentic-workshop/materials-dlc/unlock-codes.json`（本手冊不重抄碼，避免兩份不一致）。
> 本手冊與 `evaluation/` 底下所有檔案只給主持人，**不得**放進學員包、Runbook 或投影。

## 學習目標

- **DDD**：通用語言與名稱矛盾（D1）；Bounded Context 與邊界洩漏（D1）；負責的 Context、Port／Adapter、防腐層、冪等（D3a）；不變量放在唯一負責處並接上每條路徑（D3b）；Aggregate 一致性邊界與唯一入口（D3c）；模型跟上程式、以新候選取代而非覆寫（D4）。
- **Agent 技巧**：Agent 找證據、人定義；做的人與核准的人分開（加深主課 B3 的 Gate）；選項 → 決定 → 交接單（加深 Work Order）→ 計畫 → 分段實作；反事實檢查證明測試守著規則；查證 Agent 的每個引用。
- **工具**：金鑰、政策、雜湊、核准紀錄都在提示詞與 ③ 裡；巡場不講指令細節，學員卡住才解釋。

## 0. 一頁摘要

| 分鐘 | 段落 | 投影 | 你要做的關鍵動作 |
|---|---|---|---|
| 0–14 | 開場與環境 | 解鎖頁 → 4 個檢查點 | 學員邊聽說明邊下載學員包；盯 Store 別名、SHA 核對；第 11 分配對 |
| 14–43 | D1 共同語言與邊界 | 6 個檢查點 | 名稱矛盾與邊界洩漏要讓學員在 `cite` 證據中親眼看到 |
| 43–70 | D2 審查與核准（成對） | 6 個檢查點 | 第 51 分或卡 5 分鐘把 `dlc-rec-d2` 私下提供給該組；示範簽章 |
| 70–80 | 休息 | 休息頁 | 巡 D2 落後組，確認大家都有可接續的 reviewed Registry |
| 80–120 | D3a 電子發票 | 6 個檢查點 → 停手 → 2 頁揭曉 | 解鎖時宣布核心／延伸與 API 小節；揭曉後才可發 `dlc-rec-d3a` |
| 120–170 | D3b 點數折抵 | 同上 | 同上；`dlc-rec-d3b` |
| 170–217 | D3c 團體部分退款 | 同上 | **最重的一段**：保住 Review 時間；`dlc-rec-d3c` |
| 217–240 | D4 交接 | 3 個檢查點 | stale 與 shifted 證據不准跳過；更新事實只到候選 |
| 240–255 | 回顧 | 4 個檢查點 | 討論「走過場的自我核准」和「真的擋得住錯的核准」差在哪裡 |

三條不可破的規則：

1. **不延長段落**。落後就用 Recovery 接續，記錄原因與時間。
2. **Recovery 不作為小組成果評分**，只視需要私下提供（Recovery 碼只在講者備註 `data-code`，不投影、不貼群組）。
3. **`dlc-rec-d3*` 只能在對應段的揭曉頁之後**提供。

## 1. 課前檢查清單

### 1.1 一週前

- [ ] 確認學員機器：Windows 10/11 或 macOS 12 以上，可裝軟體或已預裝下列項目。
- [ ] **Python 3.13 與 `py` launcher**：`py -3.13 --version` 要有回應。沒有 launcher 的機器，請學員用 python.org 安裝程式重裝並勾選 py launcher（規格 §9 第 3 點尚未決定是否提供可攜版；若教室不允許安裝，課前要決定替代方案）。
- [ ] **Git for Windows ≥ 2.34**（SSH 簽章需要）：`git --version`。
- [ ] **macOS 機器**：
  - `python3.13 --version` 要有回應（python.org 安裝程式或 `brew install python@3.13`；內建的 `python3` 是 3.9，不能用）；
  - `git --version` ≥ 2.34（Xcode Command Line Tools 14 以上：`xcode-select --install`，或 `brew install git`）；
  - macOS 12 以上（`ssh-keygen -Y` 簽章需要）；
  - Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」，或改用 Chrome（否則 zip 會被自動解開並丟到垃圾桶）；
  - venv 在 `.venv/bin`（不是 `.venv\Scripts`）。
- [ ] 每台機器一個可讀寫本機資料夾、能執行終端指令的通用 Coding Agent。
- [ ] 建置並驗證候選包（課程維護人員）：

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

- Plugin 固定 4.2.0，只封裝執行用的檔案（不含開發用的 `evals/`、`scripts/test_*.py`、`README.md`、`ruff.toml`），檔案內容未經修改，封裝於 `participant/vendor/domain-memory-4.2.0.zip`，逐檔清單 `domain-memory-4.2.0.zip.SHA256SUMS`（97 個 Plugin 檔案＋ZIP 本身＝98 行）。
- 目前 ZIP 的 SHA256 以 `domain-memory-4.2.0.zip.SHA256SUMS` 最後一行為準。
- 學員在開場檢查點 2 應看到 `SHA OK 86 files` 與 `"version": "4.2.0"`。看到 `SHA MISMATCH` 一律停用該份 Plugin，換一份重新下載；不要「先用用看」。

### 1.4 主持人自己的機器（課前 30 分鐘）

- [ ] 在自己的機器以學員身分走完開場四個檢查點（演練實測約 15 分鐘，其中建 venv、安裝套件與第一次測試約 2–3 分鐘）。
- [ ] 在每台學員機器確認 `py -3.13 --version`（macOS `python3.13 --version`）印出 3.13。只有 uv、conda 或 Microsoft Store 版 Python 的機器，`py` 啟動器找不到 3.13，開場檢查點 4 的健檢會出現 `[!!] Python 3.13（py launcher）` 而停下；課前請學員改裝 python.org 的 3.13（勾選 py launcher）。
- [ ] 還原一次 reference Registry（見 `evaluation/reference-registry/README.md`「還原」），確認 `validate --require-reviewed`、`verify-audit`、`verify-git-governance` 全 OK。D2 示範與降級都靠它。
- [ ] 準備 D2 示範用的兩個身分：`proposer@example.com`、`maintainer@example.com`；示範金鑰放 `%USERPROFILE%\.dlc-keys\demo-maintainer\`。
- [ ] 投影開啟 `facilitator-deck.html`，副螢幕開講者模式，確認 Recovery 碼只出現在講者畫面。
- [ ] 每位學員桌上放綠色、紅色便利貼各一疊：③ 回「成功」貼綠色；卡住、或「失敗時」也沒解決就貼紅色。每個檢查點截止時掃一眼全場顏色，紅色先過去。

### 1.5 起始 Repo 殘留字詞審查（規格 §5.1）

以規格 §5.1 的 grep（排除 `.pyc`、`.venv`、`.git`）掃 `participant/repository/smart-ticket-dlc-base/`：**零命中**（2026-10-07 實測）。沒有需要刻意保留的殘留。若之後修改起始 Repo，重跑並把每個命中與保留理由補在這裡。

## 2. 教室配置與分組

- **兩人一組、一台機器、兩個 Agent 對話**。選 D1 做得比較完整的那台；它的主人當 **Proposer**（提案者，用自己的 Agent 對話準備 Change Package，不得核准、不 commit），另一人當 **Maintainer**（夥伴，另開終端機啟動自己的 Agent 對話：持簽章金鑰、讀審查包後核准、簽章 commit、push）。Maintainer 的 Agent 對話開到課程結束：D3a–c 檢查點 5 與 D4 檢查點 3 的簽章 commit、回顧的刪除私鑰都在這個對話執行。
- 開場檢查點 4（第 11–14 分鐘）就配好對；D1 各人在自己的 Repo 做，D2 起兩人共用一台機器。開場有人環境裝不起來，D1 起先以夥伴的機器為主。
- **人數奇數時組成三人組，第三人當觀察員（Observer）**：看每一步是不是在對的人的 Agent 對話裡執行（核准、簽章 commit、push 只出現在 Maintainer 的對話；proposer 的 Agent 不碰 `record-approval`），並一起看 `verify-audit` 結果。D3 起 Observer 負責對照交接單（`docs/handoffs/d3*.md`），並核對 Agent 回報的 counterfactual 結果。
- D3 三段可以換人操作鍵盤與發言，但提案者與夥伴的 Agent 對話不換；簽章 commit 一律在持鑰夥伴的對話。**Maintainer 的私鑰不換人**：只有持鑰人能簽觸及 Registry 的 commit。
- 座位安排讓兩人能同時看同一個螢幕；助教巡堂路線要能看到螢幕上的終端機輸出。
- 明講（規格 R3）：`record-approval` 只比對身分字串，同機雙身分仍可通過；今天的成對簽章是**教學示範，不是安全保證**。治理強度來自「誰持有簽章私鑰」。

## 3. 逐段腳本

每段固定節奏：解鎖頁（大字解鎖碼）→ 檢查點總覽頁（按 `T` 開段落計時，時間軸自動標示目前檢查點）→ 每到時間點翻到下一個檢查點頁。投影顯示時間、檢查點與學員下一步要做的事（打開哪頁、貼哪段提示詞、怎麼確認）；完整提示詞與表單都在 Runbook。各頁講者備註有「說／看／介入訊號／提示」，本節只列每段的骨架與決策點。

**學員的操作方式（每段都一樣）**：複製 Runbook 的提示詞 → 學員的 Agent 執行 Plugin、輔助腳本與 Git 指令並白話回報 → 學員用短回覆做決定（「同意」「選 B」「第 3 項不要」）→ Agent 把結果寫進 `notes/<段落>.md` 或 `docs/handoffs/`。學員不自己打指令；表單每段最多一張，只記人的決定。提示詞只交代這次的事；每次都要的做法（怎麼跑、工作規則、兩個角色、審查準則）寫在 Repo 的 `AGENTS.md`，一步步的固定做法在開場檢查點 1 由 Agent 裝好的 5 個 Skill（`check`、`record-candidates`、`counterfactual`、`signed-commit`、`dlc-recovery`）。Runbook 每個檢查點分四塊：① 為什麼做這一步（學員要判斷什麼寫在這裡）、② 貼給 Agent（多半以「做完用 check 檢查，最後一行寫成功或失敗。」結尾）、③ 確認結果（一行「用 check 檢查剛才這一段」：`check` Skill 只讀不改，對照 notes、實際指令結果與學員的決定，最後一行回「成功」或「失敗：原因」；回報最後一行已是成功就不另貼）、④ 補充。巡場口令：「Agent 最後一行有成功嗎？沒有就貼 ③『用 check 檢查剛才這一段』；失敗就貼『失敗時』。」下文「你說／做」與講者備註「看」裡，學員自己判斷的項目對應 ①，Agent 回報的數字與檔案對應 ③。巡堂時看的是這個循環有沒有轉起來：有沒有讀 Agent 的回報、有沒有在 Agent 停下時真的做決定、Agent 有沒有在學員同意前就寫入。Runbook 沒寫到的狀況，再給學員一段可直接貼的補救提示詞，例如「請解釋剛才的錯誤代表什麼，不要自己修改或重試，給我兩個做法讓我選」，不要替學員打指令。

### 3.1 開場與環境（0–14，群組 `dlc-opening`）

| 分鐘 | 檢查點 | 你說／做 |
|---|---|---|
| 0 | 解鎖（標題頁之後就翻到） | 公布開場解鎖碼，請學員先按檢查點 1 的下載鈕，下載、解壓縮學員包，邊做邊聽下兩頁（不佔檢查點 1 的時間）；說明今天的節奏：複製提示詞 → Agent 執行並白話回報 → 需要時回一句話決定 → Agent 寫紀錄。學員只需自己下載 `participant-dlc-open.zip`、解壓縮到習慣的位置（例如下載資料夾）、用 Agent 開啟 `participant-dlc-open/repository/smart-ticket-dlc-base`、開新對話，貼檢查點 1 的提示詞。沒有要貼的規則：專案已有團隊寫好的 `AGENTS.md` |
| 0 | （學員邊下載邊聽） | 「為什麼要和 Agent 一起建模」「今天怎麼進行」兩頁，共約 2 分鐘；講完在總覽頁按 `T` 開 14:00 計時 |
| 0–6 | 1 · 確認起點：測試全部通過 | Agent 先把學員包 `skills/` 的 5 個 Skill 放到它的工具自動載入專案 Skill 的位置、在 `AGENTS.md`「Skill」一節加一行位置，回報完整路徑；再回報 **76 passed**；沒有跑 `pip install -e .`。`check` 回「失敗」說少了 Skill 時，請 Agent 照提示詞第 1 步補放 |
| 6–8 | 2 · 備好可信的共用模型工具 | Agent 回報 `SHA OK 86 files`、`"version": "4.2.0"` |
| 8–11 | 3 · 找出只能靠人審查的錯 | Agent 經 `tools/dm.ps1`／`dm.sh` 執行：`readiness` 說 brownfield，`quality-gates` 只有 pytest；Agent 回答「哪些問題只能靠測試和人的審查才抓得到」 |
| 11–14 | 4 · 確認環境並建立起始版本 | Agent 回報 `python` 路徑在 `.venv\Scripts\`、不含 `WindowsApps`（macOS：在 `.venv/bin/`）；`doctor.py` 最後一行「全部必要項目通過。」（`[--]` 只是提醒，不算失敗）；`notes/opening.md` 有四段結果後才建立起始 commit（含 `AGENTS.md` 與放 Skill 的資料夾，不含 `domain-memory/`），commit 後 `git status --short` 是空的；同時配好 D2 夥伴（奇數時三人組，第三人當觀察員） |

巡場看：學員是不是「貼 ② → 看回報 → 看最後一行成功／失敗」，而不是自己在終端機打指令。四個檢查點的 ② 都以「做完用 check 檢查」結尾，學員不另貼 ③（最後一行不是成功才貼）；檢查點 4 等 Agent 時找好 D2 夥伴。回「失敗」時請學員貼該檢查點的「失敗時」提示詞，讓 Agent 先解釋錯誤、列出處理方式，等學員同意再做；不要替學員改指令。最常見的是 Agent 沒經 `dm` 腳本（cp950 錯誤）或沒在同一次執行裡啟用 `.venv`（`python` 指到 `WindowsApps`）：請學員對 Agent 說「照 AGENTS.md 用 dm 腳本執行」或「先讀 AGENTS.md『怎麼跑』，在同一次執行裡啟用 .venv 再重跑」，不要重貼任何規則。

降級：第 14 分鐘仍有人未過 → 兩人一機繼續，D1 以夥伴機器為主；請 Agent 在 `notes/opening.md` 記下卡在哪一步，不延長本段。

### 3.2 D1 共同語言與邊界（14–43，群組 `dlc-d1`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 14–18 | 1 · 決定哪些資料算證據 | Agent 跑 `discover-sources`，每個路徑一行建議；**學員回覆決定**，Agent 記好後自己回成功／失敗（不另貼 ③）。必含 `docs/requirements/`、`docs/adr/`、`src/`、`tests/`，排除 `**/__pycache__/**` |
| 18–21 | 2 · 建立共用模型並記下來源 | Agent 依學員的決定跑 `init-domain-memory --storage-mode tracked --review-mode local-draft-only` ＋ `confirm-sources`；不 commit |
| 21–28 | 3 · 統一名詞：通用語言 | 擷取順序先名詞、再 Context、再規則（錯的邊界會擴散到之後每一筆紀錄）。Agent 先列名稱矛盾（含「同一個字兩種意思」，標為邊界訊號）、再提詞彙草稿與證據原文；學員選 ≥ 5 個、改定義、選矛盾的處理方式；Agent 寫 `d1-records.json` 並試跑 `make_record.py`（內部呼叫 `cite`），最後一行自己回成功／失敗（不另貼 ③） |
| 28–35 | 4 · 劃分 Context，寫下規則 | Agent 為每個 Context 標出有哪幾種訊號（用語改變、資料只在一處寫入、一起修改、只透過明確介面呼叫），只有一種的標「證據薄弱」；規則是能被推翻的敘述，不是測試名稱。「一起修改」查不到歷史時 Agent 寫「無歷史」、不猜。同樣由學員決定 2–4 個 contexts（至少涵蓋檢查點 3 詞彙用到的 context id）、2–3 條 rules；登記後學員打開 Agent 指出的一份規則紀錄檔親眼看；Agent 一次登記為候選並跑 `validate`、`verify-evidence`，最後一行自己回成功／失敗（不另貼 ③） |
| 35–39 | 5 · 用客人的話找出模型缺口 | Agent 跑 `coverage` 與兩句 `resolve-terms`；Agent 說明每個命中的詞屬於哪個 Context、是不是句子說的意思：範例句「團體訂票付款失敗時…」通常以名稱命中一般訂票的付款失敗（保留座位），不是團體付款失敗（取消），名稱命中但意思不對不算通過，記成缺口。學員選一個要記下的缺口，只寫進 `notes/d1.md`，不寫進模型（D2 放進提案的 `open_questions`）。失敗時 Agent 用 `export --save ../../tmp/registry.json` 再只列詞彙名稱，不直接讀 `domain-memory/` 的檔案 |
| 39–43 | 6 · 對照程式判斷邊界洩漏 | Agent 跑 `get-context`、兩個不同 Context 的 `analyze-boundary`，對照程式附證據；學員判斷是否洩漏，Agent 把名詞處理和邊界判斷各寫一行到 `AGENTS.md`「通用語言與邊界」（附 notes 出處，之後每段的新對話都會讀到），寫完紀錄自己檢查（含 `git status`）；學員趁等 Agent 時聊「完成後想一想」，填「D1 決定」 |

**一筆紀錄長什麼樣（投影或口頭說明用）**：每筆是 `domain-memory/` 裡的一份 Markdown 文件。開頭的區塊有 `type`、`status`（磁碟上 `draft`＝候選、`stable`＝已審查；指令與 `export` 輸出仍寫 candidate／reviewed，學員的檢查一律看指令輸出）、`sources`（每段證據一行「路徑#L起-迄」加 `excerpt_sha256`），已審查的還有 `verified`；內文第一段是規則敘述或定義；最後 `# Relations` 一行一個連結，例如「Contexts:」後面接指向 `/contexts/pricing` 的連結。紀錄只放元素、關係與證據，看到「怎麼找到的」「信心」「待辦」就請 Agent 拿掉。

**「一起修改」這個訊號（`change-coupling`）不在學員路徑上**：起始 Repo 與 D3 每段都只有一個大 commit（超過 30 個檔案會被略過），輸出全空；即使在 D3c Recovery 上把門檻放到最低，也只看到 `api`／`application`／`domain`／`infrastructure` 四個技術分層彼此一起改，對不上任何 Context。提示詞要 Agent 遇到時寫「無歷史」、不要猜；學員或 Agent 問到時就用它教一句：說不出東西的訊號不是證據，依技術分層放的程式把 Context 藏在各層裡。

教學重點：名稱矛盾（Fare Policy／Discount Policy；Compensation／補償在 ADR 有、只出現在一個測試名稱、沒有對應類別）與 Context 邊界洩漏，**一定要讓學員在 Agent 摘錄的 `cite` 證據裡親眼看到**，不要口頭告訴他們。Runbook 的提示詞不會主動指向這兩組；Agent 的矛盾清單漏掉 Fare Policy／Discount Policy 時，可以請學員補一句「也比對 Fare Policy 和 Discount Policy」（可選）。Agent 會提草稿，但「哪些來源、哪些名詞、定義怎麼寫、是不是越界」必須是學員的回覆；學員對每個草稿一律回「同意」時，請他挑一個，要 Agent 把證據原文再念一次。

紀錄：Agent 把每個檢查點寫進 `notes/d1.md`，候選寫進 `d1-records.json`；學員只填一張「D1 決定」（兩個選擇、一組勾選、一個短文字）。看紀錄裡有沒有學員的決定與理由，不因少填表扣分。

Recovery：第 43 分鐘 D1 未完成的組，私下提供 `dlc-rec-d1`（Repo＋已確認 source map＋D1 候選集，全部為候選）。切換後 `domain-memory/` 仍未追蹤；D2 夥伴在 `resume-d1` 開自己的 Agent 對話。

收尾（第 43 分前）：學員趁等 Agent 時聊 Runbook「完成後想一想」，再填「D1 決定」；這段時間已滿，不另開全場分享（會吃掉 D2 約 1 分鐘）。

### 3.3 D2 審查與核准，成對（43–70，群組 `dlc-d2`）

開始時兩人各在自己的 Agent 對話貼 Runbook「開始前」的一行角色宣告（提案者沿用 D1 的對話；夥伴另開終端機和新對話）。兩個角色能做什麼寫在 `AGENTS.md`「兩個角色」（提案者不執行核准、簽章、commit、push，也不讀 `.dlc-keys`）；夥伴那一行要 Agent 先引用這一節說出自己不能做什麼、哪些事要等「核准」，答不出來就請學員說「請先讀 AGENTS.md」。下表「誰」指在誰的 Agent 對話裡貼提示詞；表內指令都寫在提示詞裡，由該 Agent 執行並白話回報。

| 分鐘 | 檢查點 | 誰 | 重點 |
|---|---|---|---|
| 43–47 | 1 · 夥伴取得核准權 | Maintainer（提案者同時貼檢查點 3 第一段） | `init-signing-key --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit`（Git Bash：`"$HOME/.dlc-keys/maintainer/signing-key"`）；**先於第一個 Registry commit** |
| 47–49 | 2 · 規定只有夥伴核准才算數 | Maintainer | `amend-policy` 依序 `authorized_signers`（fingerprint）→ `review_trigger git-push` → `review_mode scm-verified --verifier git-signed-commit`；`install-git-hitl-hook`；`governance-readiness` ready |
| 49–55 | 3 · 整理提案並證明測試守得住 | Proposer | 提案者在夥伴做檢查點 1、2 時就先按 Runbook 下載鈕取得 `participant-dlc-d2.zip`，並貼第一段（Agent 把格式範本放進 `worksheets/`、列候選、提方案，不改檔）；第二段等夥伴的檢查點 2 回成功（政策改完）才貼，否則送出後要重新核准；Agent 把 `export` 存到 Repo 外的 `tmp/export-d2.json`（可能有數十 KB，用過 Recovery 約 80 KB；不讀進對話），再用一行指令只印各類別候選 id，回報各類別候選數；照 `counterfactual` Skill 提 2 個方案（含 `--expect` 要符合的斷言片段，範例是 `700 == 595`）、學員選一個（只認 `killed`；失敗的不是那個斷言會是 `inconclusive`）；`cp-d2.json` 的 `promote` 列 Registry 每個有候選的資產（用過 D1 Recovery 含 aggregates、interactions、decisions，漏列會在 CP6 `validate --require-reviewed` 報 not reviewed）；`open_questions` 放 D1 選的缺口；`fill_package.py`（測試實際執行，不預填 PASS），放 `domain-memory/changes/<id>/`；送出併在第二段提示詞裡，學員回一句「送出」才 `submit-proposal`，Agent 最後一行自己回成功／失敗（不另貼 ③） |
| 55–62 | 4 · 夥伴審查證據並決定核准 | Maintainer | Agent 先讀審查包（只重跑每個 obligation 指定的測試，D2 沒改程式）、貼一條規則的證據原文、給出那條規則的紀錄檔路徑並停下（夥伴自己打開讀）；Maintainer 回「核准」後才 `record-approval --reviewer maintainer@example.com`、`verify-proposal`，再照 `signed-commit` Skill 列出要 commit 的檔案、夥伴回「同意」後簽章 commit，Agent 最後一行自己回成功／失敗（不另貼 ③） |
| 62–64 | 5 · 留下可驗證的核准紀錄 | Maintainer | `git log -1` 確認 HEAD 是「D2：核准 CP-D2-001」，`verify-git-governance --commit HEAD` 回 `Git governance is valid for 1 commit.`：這個簽章 commit 就是核准紀錄，CP6 的 `ship-package` 才把它寫進審查包 |
| 64–70 | 6 · 套用核准，模型成為事實 | Proposer → Maintainer | Proposer 的 Agent：`ship-package --commit HEAD`（一步確認簽章 commit 有授權且帶著審查包、寫成核准證明、定案並套用；`completed` 三步、`status` `applied`；任何一步拒絕就停在那一步、什麼都不寫）→ `validate --require-reviewed` → `verify-audit` → `get-record --changes-root domain-memory/changes` 回報一條規則的 `verified`（`by: human:maintainer@example.com`、`at`：核准時間；≈ ADR 的 Accepted 加決策者，審查它的提案記在稽核紀錄）與 `proven_by`（審查包裡證明它的 obligation 與 `check`；和 `verified` 同一張加深「已審查事實」的小卡，D4 檢查點 1 會再用）；Maintainer 的 Agent：列出要 commit 的檔案、停下等「同意」（Runbook 有提醒），再簽章 commit、`setup_remote.py`、push（不得 `--no-verify`；hook 一次檢查整個 push、只印一行，自己做的 D2 是 `Git governance is valid for 2 commits.`） |

巡堂看三件事：核准與簽章只出現在 Maintainer 的對話；Maintainer 回「核准」前說得出哪一行證據支持哪條規則；Agent 停下時學員真的做了決定。學員只填一張「D2 決定」（角色、審查決定、三項確認），其餘紀錄由 Agent 寫進 `notes/d2.md`。③ 回「失敗」時請學員貼該檢查點的「失敗時」提示詞（請 Agent 白話解釋錯誤、不改設定、不重做 commit、不繞過 hook），不要替學員打指令。

收尾（第 70 分前）：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。

**Recovery 釋放規則（`dlc-rec-d2`）**：

- 最早第 **51** 分鐘可用（規格 §3.2 的時點依 255 分鐘排程平移）。
- 任一組在任一步**卡住 5 分鐘**即可私下提供；第 51 分多數組還沒 `submit-proposal` 時，對卡住的組提供。
- 改用 Recovery 的組照 Recovery 頁三步切換（步驟 1 是 `dlc-recovery` Skill，步驟 2–3 是 `recovery/d2/RECOVERY.md` 第 2–3 節，見 §4「Recovery 切換做法」）：提案者原對話解出 Recovery 並複製成 `resume-d2`，原 Repo 的 `notes/`、`docs/handoffs/`、`AGENTS.md` 和放 Skill 的資料夾一併複製，原狀態寫進 `resume-d2` 的 `notes/d2.md`（不寫原 Repo）；**夥伴**在 `resume-d2` 新開自己的 Agent 對話，從 `repo.bundle` 還原簽章歷史、以自己的金鑰接手（`amend-policy authorized_signers`、hook、readiness ready），回「同意」後做簽章 commit；提案者同時在 `resume-d2` 新開對話建環境、跑測試，夥伴的簽章 commit 出現後再跑 `validate --require-reviewed`、`verify-audit`。夥伴的接手簽章就是這組的簽章練習；有空再看你的簽章示範（下方）。

**成對簽章示範腳本（約 4 分鐘，用 reference Registry 或自己的乾淨複本）**：

1. 「Proposer 做完 Change Package，現在換 Maintainer 坐到鍵盤前，用自己的 Agent 對話。」示範 `record-approval --reviewer maintainer@example.com`。順便示範反例：以 `proposer@example.com` 當 reviewer 會被拒；再說明以另一個字串也能通過，**所以真正的保護是簽章**。
2. `git -c user.name="DLC Maintainer" -c user.email=maintainer@example.com commit -S -m "..."`，接著 `git log --show-signature -1`，指出 `Good "git" signature for maintainer@example.com`。
3. `verify-git-governance --commit HEAD` → `ship-package --commit HEAD`：「核准證據不是一行文字，是一個可驗證的已簽章 commit；ship-package 先驗它，才肯定案與套用。」反例：對一個未簽章的 commit 跑 `ship-package --commit`，它在 `attest-signed-commit` 這一步就拒絕，什麼都不寫。
4. （有時間）做一個不簽章、觸及 `domain-memory/` 的 commit 再 push，給大家看 hook 拒絕的輸出。
5. 收尾：「私鑰在 `%USERPROFILE%\.dlc-keys\`，不在 Repo、不在 `.ssh`、不截圖。回顧檢查點 4 只刪私鑰 `signing-key`，`signing-key.allowed_signers` 保留；公用電腦課後再刪整個 `.dlc-keys` 資料夾。」

### 3.4 休息（70–80）

巡一圈：每組都要有一份 `validate --require-reviewed` OK 的 Registry（自己的或 Recovery），D3 才接得下去。還沒有的組，休息時協助還原 `dlc-rec-d2`。

### 3.5 D3 共同節奏（80–217）

三個情境**全體依序、三個都做**，每段在前一段成果上累積。每段六個檢查點同一個節奏：

1. 學員貼提示詞：Agent 存下需求卡（D3a 由提案者下載 `participant-dlc-d3a.zip`，Agent 照 `AGENTS.md` 解到 `../../pkg-d3a`，需求卡與決策卡都在裡面；D3b、D3c 學員按需求卡的「複製 Markdown」接在提示詞後面）、執行 `resolve-terms`／`get-context`，已知事實與知識缺口分開寫進 `notes/d3*.md`。
2. Agent 每題提兩個選項＋證據（「類別:id」或「檔案路徑:行號」），**人**討論後以一行回覆選擇（例如「1A、2B」）；Unknowns 每項由 Agent 給兩個具體做法並標建議，學員回「照建議」或「U1 改 B」就在這裡定案，實作時不再問；`analyze-boundary` 一次回報兩個方向（`source_depends_on_target`、`target_depends_on_source`），兩邊都空才是 `no_registered_collaboration`；Agent 依選擇寫成交接單（`docs/handoffs/d3*.md`），人確認不變量後回「同意」。
3. Agent 依交接單先提計畫、等「同意」，分兩段實作，每段停下回報**實際**測試結果，人回「繼續」才往下。
4. Agent 先列出要改壞哪裡（D3a、D3b 只跑檢查點 5 要登記的 2 條，其餘標「未證明」；D3c 每一條，同意後一批跑完），人同意後才執行 `counterfactual`；`--expect` 從實際斷言那一行複製一段獨特的子字串（pytest 會把長 tuple 縮寫成 `...`）；只認 `killed`，survived 補測試用同一組字串重跑。Agent 指出沒有任何輸入分辨得出改壞前後（等價，例如另一段程式也擋住，或輸入不可能落在那個邊界，如 D3a 5% 稅額下整數總額永遠不會落在 .5）時，學員確認後標「等價、未證明」，那個 survived 的 cf 檔保留並一起 commit。`--test-command` 寫 `./.venv/Scripts/python.exe`（不經 shell，見常見問題第 2 條）並帶 `-W ignore::DeprecationWarning`，讓套件過時警告（例如用 D2 Recovery 時）不混進 `failure_evidence`。`inconclusive` 不算 killed 也不算 survived：逾時就縮小測試範圍，改壞後程式無法載入就換改法；被測行為改變、測試讀結果時出錯（例如回應少了欄位的 KeyError）算 killed；改壞的程式自己意外崩潰（和規則無關的 NameError、KeyError、TypeError、AttributeError；演練：不加 `--expect` 時 Plugin 照樣寫 killed，`failure_evidence` 只有一串 FAILED）算 inconclusive，除非規則本身就是丟出或傳出那個例外（例如服務商替身的 ConnectionError）；`failure_evidence` 的斷言不是守住規則的那一行、或看不到斷言時，加 `--expect`（具體斷言值，不能只寫 `assert`）重跑；只有被拒絕執行、沒有 verdict 的那次留下的 cf 檔，重跑前先刪掉。
5. Agent 用 `git status --short`（新檔只出現在這裡）、`git diff` 與測試回答四個審查問題；D3b、D3c 再讀變更簡報 `brief --base HEAD --markdown`，只看 Attention 裡改動碰到引用行的已審查紀錄，逐筆判斷模型有沒有變（名詞、負責的 Context、不變量或規則、邊界、事件或對外約定），只搬移程式的重構不登記（「模型變更與重構」在 D3b 檢查點 5 才第一次講；「lies outside every Context」是因為 Context 沒登記程式路徑，這些行不算進摘要，但它們點名、又在檢查點 1 清單上的事實仍逐筆看；不執行它建議的 `recite`）；D3c 的規則在 `d3c-records.json` 寫上 `aggregate`，規則和 Aggregate 不在同一個 Context 時 Plugin 拒絕登記，讓學員決定哪一邊放錯；人同意後提案者的 Agent 才照 `record-candidates` Skill（`make_record.py`）登記，**仍是候選**；提案者的 Agent 不得執行 `record-approval`、`amend-policy`、`git commit`／`push`。夥伴讀過紀錄後，在**自己的 Agent 對話**照 `signed-commit` Skill 做簽章 commit（與 D2 相同）。
6. 停手 → Agent 整理決策摘要 →「請先停手」頁 → 兩頁揭曉 → 學員填一張揭曉對照表單（兩個下拉、一個勾選、一句話）→ 收尾：Runbook 檢查點 6 ④ 的三題請兩人對照參考設計時一起聊，挑第 3 題請 1–2 組分享（約 1 分鐘）。

**巡場看流程**：每組是否「貼提示詞 → 看 Agent 回報 → 自己做決定 → 讓 Agent 記錄」。決策點（檢查點 2–5）學員要自己選，回「你決定」就介入。卡住時給可直接貼的補救提示詞，不替學員決定：

- Agent 替學員選了或開始改程式：「停下，不要再修改。如果你已經改了檔案，列出改了哪些。請回到只列選項與證據，等我們選擇。」
- Agent 說「完成」但沒附實際輸出：「請貼出你實際執行的指令與輸出；沒有執行的標『未驗證』。」
- counterfactual 只有亂碼，或 `verdict` 是 `error`（指令拒絕執行，原因在 `reason`）：「這不算 killed，請說明原因，不要換字串。」
- commit 遇到簽章錯誤：「不要修改 Git 設定、不要碰金鑰，貼出錯誤訊息後停下。」然後由主持人處理。

評估以紀錄檔（`notes/d3*.md`、`docs/handoffs/d3*.md`、`cf-d3*.json`）裡的證據與「學員有沒有自己做決定」為準，不因表單欄位少而扣分。

**解鎖時就宣布兩件事**（三段都一樣，講者備註有提示）：

- **核心／延伸**：需求卡「本次範圍」已把每條 AC 標成［核心］或［延伸］。先做完核心；延伸只在時間允許時做。沒做延伸時，核心行為仍須完整可用。
- **API 小節**：卡上已定義路徑、欄位與錯誤碼。叫學員先看，並在 Handoff 中要求 Agent 照卡做，不准自己發明介面。這省下的時間要留給 Review 與 counterfactual。

各情境核心／延伸：

| 情境 | 核心（必做） | 延伸（時間允許） | 建議現場 counterfactual |
|---|---|---|---|
| D3a 電子發票 | EINV-001、002、003、005、006、007、008、009、010、011、015 | EINV-004、012、013、014 | 重試上限 `MAX_ISSUE_ATTEMPTS`；鎖外呼叫；冪等鍵 `merchant_order_no` |
| D3b 點數折抵 | PTS-001、003、004、005、006、007、008、009、010、012、014 | PTS-002、011、013、015 | 上限以優惠後總額計（只有 665 抓得到）；預留在寫入前；團體付款失敗歸還；退款現金＝Order.amount（要有改票後退票測試） |
| D3c 團體部分退款 | PCR-001、003、004、005、006、007、008、009、011、012 | PCR-002 完整驗證、010、013、014、passenger_id 唯一性 | 手續費逐位／以自己的票價（要有混合團測試）；先決定再釋放；部分取消後不可整筆退；只釋放被取消者的座位 |

**揭曉與 Recovery 規則**：第 6 個檢查點開始時翻到「請先停手」頁，確認全員停手後才翻揭曉頁。揭曉頁講「設計判斷與理由」，不現場補寫答案程式，不說「標準答案」。揭曉之後，落後的組才可私下拿到該段的 `dlc-rec-d3*`，用它接續下一段。

### 3.6 D3a 電子發票（80–120，群組 `dlc-d3a`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 80–84 | 1 · 讀需求卡與已審查事實 | 宣布核心／延伸與 API 小節。H1：「逾時代表什麼？對方可能已經開出發票了嗎？」 |
| 84–91 | 2 · 對外介面（Port）與邊界決策 | 發票歸哪個 Context？Port 放哪層？誰把 Order 翻成發票語言？H2：「付款 Gateway 沒有 Port，這次要照做還是改？」 |
| 91–100 | 3 · 交接單與 Agent 實作 | 盯鎖：`pay_group` 持有 RLock 時呼叫 `pay`；盯「付款請求內同步重試 5 次」 |
| 100–106 | 4 · 反事實檢查 | 從建議的 3 個挑 2 個（就是檢查點 5 要登記的）；第 106 分沒跑完的標「未證明」 |
| 106–117 | 5 · 審查變更，新知識寫回模型 | 只登記檢查點 4 證明 killed 的 2 條規則，未證明的留給 D4；有沒有供應商代碼（`9001`、`2001`）出現在 Domain／Service；候選清單把同一個測試守住的規則排在一起（加深「不變量」：同一個不變量的不同面向，該同屬一個 Context），H：「這幾條規則分在兩個 Context，那個測試要歸誰？」 |
| 117–120 | 6 · 停手與揭曉對照 | 揭曉：新的 Invoicing Context；Port `InvoiceIssuer` 只回 ISSUED／REJECTED／UNAVAILABLE；Adapter 翻譯代碼、逾時、連線失敗；鎖內只建 PENDING，鎖外呼叫一次；冪等鍵＝order_id |

時間判斷：參考解答完整 15 條 AC 約 340 行程式＋320 行測試，40 分鐘只夠核心切片（演練實測：整段約 46 分鐘，光 Agent 工作就約 29 分鐘；檢查點 3 約 9–10 分鐘，檢查點 5 審查、登記加夥伴 commit 約 15 分鐘）。Runbook 頁首的「最低完成線」有時間點：第 100 分還沒做完核心，就請 Agent 做完手上這一步、跑完整測試收尾，進 counterfactual（要登記的 2 條核心規則各一條 killed）；第 106 分不論做到哪都進 Review。改用 D2 Recovery 的組直接照這條線做。

### 3.7 D3b 點數折抵（120–170，群組 `dlc-d3b`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 120–125 | 1 · 讀需求卡與已審查事實 | 宣布核心／延伸與 API 小節。H1：「折抵要加在哪裡，才不會漏掉其中一條計價路徑？」 |
| 125–133 | 2 · 決定負責的 Context 與不變量 | 點數歸誰、理由；30% 上限歸誰；reserve／restore 的時機。H2：「預留要不要成為獨立概念？」 |
| 133–145 | 3 · 交接單與 Agent 實作 | 盯「點數塞進 `DiscountPolicy`」與「從 `total_fare` 扣點」；扣點位置要在座位規劃之後、寫入之前 |
| 145–151 | 4 · 反事實檢查 | 從建議的 4 個挑要登記的 2 個（預留與歸還各一），其中「上限以優惠後總額」「退款＝Order.amount」是先 survived 再補測試的好示範 |
| 151–165 | 5 · 審查變更，新知識寫回模型 | 商業數字（30、100）是否只有一個家；killed 規則最多登記 2 條、取代舊事實的候選最多 3 項，已有新規則取代的舊事實只在 notes 寫「舊 id → 新規則 id」；brief 裡含「lies outside every Context」的行不算進摘要，但它點名、又在檢查點 1 清單上的事實仍逐筆看（演練：`MEMBER-004` 只出現在這種行） |
| 165–170 | 6 · 停手與揭曉對照 | 揭曉：Membership 擁有點數與折抵規則（含 30% 上限）；Pricing 與三條計價迴圈一行不改；Booking 記折抵點數、推導 `payable_amount`；閘道扣 `payable_amount`＝Order.amount；發票自動是 500 → 476＋24 |

時間判斷：程式只約 +80 行，核心切片可行；省下的時間給 Review（本段 14 分鐘：brief、候選、夥伴 commit；演練實測整段約 60 分鐘，Review 約 16 分鐘）。最低完成線：第 145 分檢查點 3 沒做完就收尾進 counterfactual，第 151 分一定進 Review。D3a 未完成的組，揭曉 D3a 後已可用 `dlc-rec-d3a` 接續，本段不用從頭補 D3a；切換約 12 分鐘，直接照最低完成線做。

### 3.8 D3c 團體部分退款（170–217，群組 `dlc-d3c`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 170–175 | 1 · 讀需求卡與已審查事實 | 宣布核心／延伸與 API 小節，並明講「本段最緊，延伸一律最後」。H1：「現在的退款紀錄能表達『同一筆訂票退過兩次』嗎？」 |
| 175–184 | 2 · Aggregate（聚合）邊界與不變量 | Aggregate root、唯一入口、恆等式誰保證、手續費歸誰、退款紀錄結構。Aggregate 選項要寫出守住哪一條必須同時成立的規則；「把這些類別包在一起」或「一張表」不算 |
| 184–195 | 3 · 交接單與 Agent 實作 | Handoff 要有「四份座位資料」「先拒絕再修改」「不要動 `total_fare`」與混合團範例；需求卡範例的三步示範只在最後做一次 |
| 195–203 | 4 · 反事實檢查 | 建議的 4 個；同意後全部方案一批跑完；第 195 分沒做完也進來 |
| 203–214 | 5 · 審查變更，新知識寫回模型 | **不可壓縮**。看整筆退票路徑、恆等式在哪裡成立、座位四份是否一致 |
| 214–217 | 6 · 停手與揭曉對照 | 揭曉：團體 Booking 擁有旅客取消（`cancel_passengers` 唯一入口，全部檢查完才寫入）；費率帶與 D ≤ 0 不受理在同一模組、逐位向下取整；只釋放被取消旅客的座位；退款紀錄改 append-only 清單；部分取消過不可整筆退 |

**時間風險：這是三張卡最重的一張**。參考解答 +141 行、是唯一需要改既有資料結構的一張；核心切片勉強放得下（演練實測完整做約 64 分鐘，光 Agent 工作就約 42 分鐘），前提是學員從第 170 分就照卡上的 API 做。規格 R2 允許只完成 Aggregate 與兩條規則（Runbook 頁首的「最低完成線」：第 195 分沒做完就收尾進 counterfactual，第 203 分一定進 Review；改用 D3b Recovery 的組直接照這條線做）。寧可少做 AC，也不要吃掉第 203–214 分的 Review：本段教學重點全在 Review。

### 3.9 D4 交接（217–240，群組 `dlc-d4`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 217–221 | 1 · 檢查模型是否落後程式 | 學員先下載 `participant-dlc-d4.zip`（交接單範本），Agent 照 `AGENTS.md` 解到 `../../pkg-d4`、把 `d4-handoff-template.md` 複製到 `../../worksheets`，再照它「交接前的檢查」跑 `verify-sources`、`verify-evidence`、`verify-audit`、`coverage`，寫進 `notes/d4.md`；`verify-evidence` 輸出很長，只讀 summary 與 stale／shifted 的 asset、id 欄位。`verify-sources` 會是 `stale`、exit 1：D3 新增了檔案，來源資料夾列在 `changed_sources`，只改內容的列在 `content_changed`；`verify-evidence` 對只是移動的引用回報 `shifted`（不算失敗），引用行被改過的才是 `stale`、exit 1。stale 的規則再用 `get-record --changes-root domain-memory/changes` 找出 `proven_by` 的測試並跑一次（D3c Recovery 實測 5 條 stale 規則都有、都通過；check 是 CP-CORE 的測試路徑，Agent 前面加 python -m pytest -q）：通過代表行為多半沒變，失敗或沒有測試才是模型真的落後。兩者都是預期；要記下，不准跳過，也不讓 Agent 當場修。`coverage` 的 `rule_totals` 與 `rules_by_context` 說出模型在哪些 Context 說了算：每個 Context 有幾條已審查規則、其中幾條有測試證明（`proven`／`unproven`／`unknown`）；D3c Recovery 實測 16 條已審查規則全部 proven、`contexts_without_reviewed_rules` 0。自己做 D3 的組，D3 新增、只有候選規則的 Context 會出現 `reviewed_rules` 0，寫進交接單 Unknowns。`verify-sources` 的 `discovered_but_gone` 列出 D1 盤點時有、現在已刪的檔案；D3 只新增檔案，通常是 `[]`。stale 與 shifted 清單只列 asset:id（檔案），行號不必列（檢查點 2 要新行號時再跑一次 `verify-evidence`），不必自寫腳本 |
| 221–228 | 2 · 把改變的規則寫回模型 | Agent 依檢查點 1 的 asset:id 清單，只對 stale 的 id 用 `get-record` 分出候選與 reviewed（decisions 看 `review_status`，其他看 `status`；shifted 的 reviewed 一律歸 C，兩張清單都有的以 stale 處理），列出更新清單；學員回「同意」後才照 `record-candidates` Skill（`make_record.py --upsert`）登記，只到候選。stale 或 shifted 的候選用同一個 id 重新引用；意思被改變（名詞、負責者、不變量或規則、邊界、事件或約定至少一項）的 reviewed 事實以新 id 候選取代，只是重構的歸 C；只是移動（shifted）或行為沒變的 reviewed 事實不登記，下一次核准沿用原 id 重新證明（Plugin 的 `promote-candidate --amend`；學員只需分得出「同一條規則重新證明」與「意思變了的新規則」，這是 D3b「模型變更與重構」的加深）。B 類最多 3 項（`REFUND-004` 先列），其餘列為未完成、寫進交接單 Unknowns。參考：D3c 讓 `REFUND-004`、`vocabulary:refund-record`、Booking 的「只能退一次」（`aggregates:booking`）與 `ASIS-004` 不再成立；D3c Recovery 也含 D3a／D3b 的變更，所以 `MEMBER-004`、`vocabulary:points-balance`（已可折抵點數）、`ORDER-002`、`vocabulary:order`、`aggregates:order`（Order 金額改為折抵後的應付金額）同樣不再成立，`contexts:membership`（多了預留與歸還點數）與 `contexts:payment`（多了開立電子發票）的職責描述已不完整。D3c Recovery 的清單約 39 個 asset:id（stale 21、shifted 26，8 個兩張都有），7 分鐘內登記不完，其餘列為未完成是預期。新候選的 id 不用需求卡驗收條件的編號（EINV-、PTS-、PCR- 開頭）：`AGENTS.md`、`record-candidates` Skill 與 D4 範本都已寫明。Agent 登記後最後一行自己回成功／失敗（不另貼 ③） |
| 228–240 | 3 · 寫交接單並查證每個引用 | Agent 照 `../../worksheets/d4-handoff-template.md` 的七段（Domain facts、Forces、Decision、External systems、Unknowns、Proof obligations、Counterfactual check）寫 `docs/handoffs/d4-next-agent.md`，Domain facts 第一行寫模型版本（git log 最上面（最新）一個訊息含「套用」的 commit；Agent 以 `export --commit <編號> --save ../../tmp/model-reviewed.json` 確認讀得到），每個 id 用 `get-record` 查證並回報核對清單；提案者的 Agent 只回報 id 核對清單與移到 Unknowns 的項目（各段學員自己打開看）；學員同意後，Maintainer 在自己的 Agent 對話照 `signed-commit` Skill 列出檔案、停下等「同意」，再簽章 commit（提案者的 Agent 不 commit），接著 `install-pre-commit-hook` 並示範一次：把 `discounts.py` `git mv` 改名後 commit，被提交前檢查擋下（點名引用它的紀錄、印出 `relocate-evidence --from … --to …`），再搬回原位；夥伴的 Agent 最後一行自己回成功／失敗（不另貼 ③）。新概念「讓模型擋住讓引用失效的 commit」：hook 只看這次 commit 的檔案，要在 PATH 上找到 Python 3.10 以上，所以同一次執行先啟用 venv；它留在學員的 Repo 裡，課後刪掉工作坊資料夾（Plugin 在 `vendor/`）會讓碰到引用檔的 commit 失敗，屆時刪除 `.git/hooks/pre-commit` 即可 |

**時間**：演練實測 D4 約 25 分鐘（Agent 工作約 13 分鐘；檢查點 3 最長，提案者寫交接單、夥伴列檔案再 commit 是兩段來回）。第 240 分還沒完成就收在最低完成線：「檢查點 1 + 只含 Unknowns 的交接單，其他段寫『未完成』」，夥伴 commit 後進回顧。第 205 分決定改用 D3c Recovery 的組（切換約 12 分鐘，會吃掉一半的 D4），D4 一開始就只做這條線。

看什麼：Agent 是否等學員回覆才寫入；commit 是否在 Maintainer 的對話執行；id 核對清單是否全部查得到（查不到的移到 Unknowns，而不是換成猜的 id）；候選沒有寫成 reviewed。第 205 分決定切換的組用 `dlc-rec-d3c` 接續 D4（見 §4）；Recovery 提供的段落沒有交接單、情境卡與 `cf-*.json`：Counterfactual check 那幾段寫「未證明」，Unknowns 註明「Recovery 不含」；自己做的段落照實列。

收尾（第 240 分前）：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。回顧檢查點 2 會再引用各段的答案。

### 3.10 回顧（240–255，群組 `dlc-retro`）

四個檢查點：請 Agent 從紀錄整理證據（240–244，Agent 寫 `notes/retro.md`）、比較哪些人工把關擋得住錯（244–249，Agent 依紀錄把今天每個人工把關點列成清單：留下了什麼證據、同一個人在同一台機器上能不能自己完成；再以 git log 最上面（最新）一個訊息含「套用」的 commit 當基準答案跑 `compare-registry --gold-commit`，回報 precision、recall、`overall_independent`（排除 `copied_evidence` 照抄配對後的分數；D3c Recovery 實測 57 個配對有 52 個是核准後沒動過的紀錄，`overall` 1.0 幾乎全靠它們；D3a Recovery 加 3 筆候選後 `overall` precision 0.95、`overall_independent` 0.625）與每類的 missed／extra；小組口頭討論）、挑選提示詞與一項行動（249–253，Agent 起草、每人挑選，寫成 `notes/my-prompts-<名字>.md`；最後一人貼第二段，小組選一項行動寫進 `notes/retro.md`）、匯出與結束（253–255，Maintainer 請自己的 Agent 刪除私鑰，全員匯出）。討論只用口頭，不要求寫下來；檢查點 2 請學員回想各段結尾的討論（D1、D2、D4 的「完成後想一想」，D3 檢查點 6 的三題），對照哪個技巧真的擋住了錯。必談：

1. 哪一個 reviewed 事實改變了 Agent 的輸出？
2. 哪一個候選差點被當成事實？
3. 走過場的自我核准，和真的擋得住錯的核准差在哪裡？（直接回到 R3：`record-approval` 只比字串）
4. Agent 的分數：extra 是核准後 Agent 新寫、還沒有人審的（自己做 D3 的組通常是 D3 與 D4 的候選）；missed 不是 0，代表核准過的事實不見了，請 Agent 指出是哪一段改掉的。分數只比結構（名稱、id、引用的檔案），不比意思；用過 Recovery 又沒做 D3 登記的組會是 1.0，照實說「沒有新候選」即可。

看什麼：學員是否抽問 Agent「這句的證據在哪？」，把沒有證據的句子改成「未觀察」。最後提醒匯出 Runbook（`smart-ticket-dlc-runbook-<stamp>.zip`）並保存 `notes/`，以及刪除金鑰（§7）。

## 4. 解鎖碼與 Recovery 釋放規則

| 群組 | 最早分鐘 | 類型 | 釋放條件 |
|---|---:|---|---|
| `open` | 0 | 不鎖 | — |
| `dlc-opening`、`dlc-d1`、`dlc-d2`、`dlc-d3a`、`dlc-d3b`、`dlc-d3c`、`dlc-d4`、`dlc-retro` | 0、14、43、80、120、170、217、240 | 一般 | 該段解鎖頁大字公布 |
| `dlc-rec-d1` | 43 | Recovery | D1 未完成者，第 43 分起私下提供 |
| `dlc-rec-d2` | 51 | Recovery | 第 51 分起；或任一組任一步卡 5 分鐘 |
| `dlc-rec-d3a` | 120 | Recovery | **D3a 揭曉頁之後**才可提供 |
| `dlc-rec-d3b` | 170 | Recovery | **D3b 揭曉頁之後**才可提供 |
| `dlc-rec-d3c` | 214 | Recovery | **第 205 分決定**哪些組切換；切換的組在 **D3c 揭曉頁之後**立即私下提供（約第 214 分，不等第 217 分）。切換約 12 分鐘、與 D4 前半重疊，這些組 D4 只做最低完成線（§3.9） |

- Recovery 碼與一般碼分開、只視需要提供，不投影、不貼群組；Recovery 不作為小組成果評分。
- 使用 Recovery 的組如實記錄觸發原因與時間（依 Runbook 對應 Recovery 頁的做法）。
- Recovery 包只含可接續的 Repo（含 `domain-memory/`），不含觀察指引、counterfactual 證據原稿或任何 `evaluation/` 檔案。
- **Recovery 切換做法（五個 Recovery 頁共用）**：步驟 1 是學員 Agent 已裝好的 `dlc-recovery` Skill 的步驟 1（與 `make_recovery.py` 產生的 `recovery/<段>/RECOVERY.md` 第 1 節同一份指令），步驟 2–3 是 RECOVERY.md 第 2–3 節。原 Repo 不改名、不覆寫；Recovery 複製成同一層的 `resume-<段>`，從 `repo.bundle` 還原 Git 歷史（不重新 `git init` 出未簽章的起點 commit）。D1 只有一個不含 `domain-memory/` 的「起始 Repo」commit，兩步都由提案者的 Agent 做、沒有 commit。D2 起分三步：① 提案者原對話照 `dlc-recovery` 解出 Recovery，把原 Repo 的 `notes/`、`docs/handoffs/`、`AGENTS.md`（含學員寫的「通用語言與邊界」）複製進 `resume-<段>`，再把原 Repo 放 Skill 的資料夾原樣複製到同一路徑（Skill 第 1.3 步），原狀態寫進 `resume-<段>` 的 `notes/<段>.md`（原 Repo 什麼都不寫）；② **夥伴**在 `resume-<段>` 新開自己的 Agent 對話（Recovery 頁的提示詞以「我是夥伴」開頭，`AGENTS.md`「兩個角色」由 Agent 自己讀）：還原歷史、`init-signing-key`（沿用 `.dlc-keys\maintainer\` 的 D2 金鑰，沒有就新建）、把 `keys/maintainer.allowed_signers` 附加到新的 allowed signers 檔、`amend-policy authorized_signers` 加入自己的 fingerprint、`install-git-hitl-hook`、`governance-readiness` ready，列出要 commit 的檔案、夥伴回「同意」後以 `git add -A -- . ':!records'` 把複製來的 `notes/`、`docs/handoffs/`、`AGENTS.md` 和 Skill 資料夾一起簽章 commit（commit 後 `git status --short` 是空的）並 `verify-git-governance --commit HEAD`；③ 提案者不等 ②，同時在 `resume-<段>` 新開對話建 venv、跑測試；夥伴的簽章 commit（「<段> Recovery：授權本組金鑰」）出現在 `git log` 後再跑 `validate --require-reviewed`、`verify-audit`、`verify-evidence`（還沒出現 Agent 會停下，最後一行寫「等待夥伴」，等學員說「夥伴好了」；步驟 1 先問進度時最後一行是「等你們回答」，兩者都不是失敗）。之後 D3、D4 的 commit 照常由夥伴簽章。Git Bash 區塊整段包在 `( set -e … )` 子 shell 裡，任何一行失敗只結束這一段，不會關掉 Agent 的終端機。複製來的 `notes/` 提到的候選 id 是原 Repo 的，Recovery 的 Registry 不一定有，查不到是預期。
- D3a／D3b／D3c 的 Recovery 還原後，`verify-evidence` 會對引用行只是移動的證據回報 `shifted`、被改過的回報 `stale`，`verify-sources` 會因來源資料夾新增了檔案回報 `stale`，都是 exit 1，屬預期，留到 D4 處理。`git log` 最上面的「Recovery 參考實作」commit 是 `N`（未簽章），因為它不碰 Registry，hook 允許；Registry 的七個 commit（最上面一個是改存 OKF 版面）是 `G maintainer@example.com`。D2 起每個 Recovery 最下面的「Smart Ticket DLC base」（起始程式）也是 `N`，同樣不碰 Registry。

## 5. Windows／macOS 已知陷阱與修正

| # | 症狀 | 原因 | 修正 |
|---|---|---|---|
| 1 | `UnicodeDecodeError: 'cp950' codec ...` | 直接呼叫 `registry_tools.py`，缺 `-X utf8` | 一律經 `tools\dm.ps1`／`dm.sh`（固定 `py -3.13 -X utf8`） |
| 2 | counterfactual 以 `ERROR: … could not start: [WinError 2]` 結束（exit 1） | `--test-command` 不經 shell，由 Plugin 以 shlex 拆字後直接執行：反斜線被吃掉，`.venv/Scripts/python.exe` 沒有 `./` 開頭 Windows 也找不到 | 寫 `./.venv/Scripts/python.exe -m pytest -q <測試>`（PowerShell 與 Git Bash 相同；macOS 寫 `.venv/bin/python`）。**只認輸出中的 `killed`**；`failure_evidence` 要是 assertion 失敗，`inconclusive` 看 `reason` |
| 3 | push 時 hook 印出 `no Python 3.10 or later on PATH as python3 or python` | pre-push hook 只在 PATH 上找 `python3`、`python`（要 3.10 以上）；Windows 常只有 `py` 啟動器，或 `python` 是 Store 別名（路徑含 `WindowsApps`）；macOS 的 `python3` 可能是內建的 3.9 | push 前在同一次執行啟用 Repo 的 `.venv`（`AGENTS.md`「Git 與金鑰」與 `signed-commit` Skill 已寫好；Agent 漏了就請學員說「照 AGENTS.md，push 前在同一次執行啟用 .venv」）。開場檢查點 4 就要攔下 |
| 4 | push 被拒「Git commit signature is invalid」：後面接 `carries no signature`（沒有簽章）或 `is signed, but the signature does not verify`（有簽章但驗不過），並寫出是哪個 commit | 沒有簽章：簽章在第一個 Registry commit 之後才設定，或 Agent 用 rebase／amend 改寫過已簽章的 commit；驗不過：Recovery 接手時沒附 maintainer 的 allowed_signers | 簽章先於第一個 Registry commit（`--sign-every-commit`）；已簽章的 commit 不要 amend 或 rebase，要合併別人的變更用 merge；Recovery 照切換頁步驟 2（RECOVERY.md 第 2 節）附上 allowed_signers 那一行，不要讓 Agent 自己 `git init` 出未簽章的起點 commit；用 `git log --format='%h %G? %s'` 找出 `N` 的那個 commit |
| 5 | 新開的終端機裡 `python` 又不對 | venv 只對目前視窗有效 | 每個新視窗：PowerShell `Set-ExecutionPolicy -Scope Process Bypass -Force` ＋ `.\.venv\Scripts\Activate.ps1`；Git Bash `source .venv/Scripts/activate`；macOS `source .venv/bin/activate` |
| 6 | `ssh-keygen` 行為不同、金鑰路徑找不到；或驗證簽章時出現 `Git commit signature was not checked`，後面接 `cannot spawn ssh-keygen`（Windows）或 `cannot run ssh-keygen`（macOS） | Git Bash 與 PowerShell 的 `ssh-keygen` 不同；後者是 Git 在目前的 PATH 找不到或啟動不了 `ssh-keygen`，簽章沒有被檢查，不是簽章錯 | 兩者皆可，但同一組全程用同一種 shell。找不到時先跑開場的 `doctor.py`（會檢查 `ssh-keygen`）；Windows 在「選用功能」啟用 OpenSSH Client，或改在 Git Bash 執行；macOS 確認 `which ssh-keygen` 指到內建的 `/usr/bin/ssh-keygen`。再驗證一次 |
| 7 | clone／還原後 `verify-evidence` 把引用全部報成 `stale`（`verify-sources` 則把來源列在 `content_changed`） | `core.autocrlf=true` 轉換換行，Plugin 以原始位元組算雜湊 | 起始 Repo 已有 `.gitattributes`（`* -text`）；在已 `git init` 的 Repo 執行 `doctor.py` 時也會檢查。不要刪它。Recovery 第一次寫入後 registry 檔整檔換行改變（CRLF→LF）是預期，diff 很大但雜湊與稽核不受影響 |
| 8 | push 時 hook 輸出亂碼或編碼錯誤 | hook 內 Python 用系統編碼 | `AGENTS.md`「Git 與金鑰」已要求 push 前設 `PYTHONUTF8=1`（PowerShell `$env:PYTHONUTF8 = '1'`，Git Bash `export PYTHONUTF8=1`）；Agent 漏了就請學員說「先讀 AGENTS.md『Git 與金鑰』再 push」 |
| 9 | 安裝很久或有人跑 `pip install -e .` | 不需要可編輯安裝 | 只用 `pip install -r requirements.txt`（約 50 秒；連同建 venv 與第一次測試，演練實測約 2–3 分鐘）。之後 `check` 在程式和測試沒改時沿用上次測試結果，不重跑 |
| 10 | `scan-secrets` 有 finding | 金鑰放進 Repo 內（含被 `.gitignore` 忽略的資料夾，只有 `.git`、`.venv`、`node_modules` 不掃；Repo 外的 `.ssh` 不會被掃到） | 金鑰只放 `%USERPROFILE%\.dlc-keys\<代號>\`（Git Bash `~/.dlc-keys/<代號>/`），預期 exit 0；另外，不要和 `~/.ssh` 的個人金鑰共用，那是不共用金鑰的規則，不是 scan-secrets 會抓的問題 |
| 11 | PowerShell 說「已停用指令碼」 | 執行原則 | `Set-ExecutionPolicy -Scope Process Bypass -Force`（只影響目前視窗） |
| 12 | macOS：下載資料夾沒有 zip，只有同名資料夾 | Safari 預設「下載後打開『安全』的檔案」，自動解開後把 zip 丟到垃圾桶 | Safari › 設定 › 一般 取消該項，或改用 Chrome，再重新下載。Recovery 的 macOS 指令找不到 zip 時會印出這個提示 |
| 13 | macOS：`dm.sh` 出現語法錯誤或版本錯誤 | PATH 上沒有 `python3.13`，`dm.sh` 退回 `python3`（內建 3.9 跑不動 Plugin） | 安裝 Python 3.13（python.org 或 `brew install python@3.13`），確認 `python3.13 --version` |
| 14 | macOS：`ssh-keygen` 不認得 `-Y`，或 git 版本低於 2.34 | macOS 11 以前內建的 OpenSSH 太舊；Xcode Command Line Tools 太舊 | macOS 12 以上；`xcode-select --install` 或 `brew install git`。來不及就和夥伴共用已通過的機器 |
| 15 | macOS：`dm.sh: permission denied` | 解壓工具沒保留執行權限 | `chmod +x ../../tools/dm.sh`（`AGENTS.md`「怎麼跑」已寫；Agent 沒做就請學員說「照 AGENTS.md 處理 permission denied」） |
| 16 | push 被拒，hook 印出 `domain-memory pre-push: the chained hook .git/hooks/pre-push.domain-memory-existing is not executable` | 裝 hook 前，這個 Repo 已經有別的 pre-push hook（例如 Git LFS 裝的），`install-git-hitl-hook` 把它改名成 `pre-push.domain-memory-existing` 並在 push 時先執行它；之後 Repo 經過解壓、雲端同步或複製，那個檔案失去執行權限（macOS 常見；Windows 的 Git Bash 看檔案第一行是不是 `#!`）。hook 這時會停下 push，不會默默跳過原本的檢查 | 先確認原本那個 hook 還要不要：要的話，macOS `chmod +x .git/hooks/pre-push.domain-memory-existing`，Windows 確認它第一行是 `#!/bin/sh` 之類的直譯器行；不要的話刪掉它。再 push 一次。`pre-push` 本身遺失或被覆蓋時，重跑 `install-git-hitl-hook` 裝回 |
| 17 | Agent 或學員手動改了 `domain-memory/` 裡的紀錄檔，`validate` 回 `ERROR: <類別>/<id>.md: frontmatter line N: …` | 紀錄檔開頭區塊只接受 YAML 的一小部分：`key: value`、兩格縮排、`- ` 項目、值不加引號或用雙引號；單引號、`[a, b]` 會被拒並附行號。手改也不會留下稽核事件（`verify-audit` 照樣 valid），等於繞過候選與核准 | `git checkout -- <那個檔>` 還原（還沒 commit 時）；要改內容就照 Runbook 走候選與核准，不手改。學員只「打開來讀」 |
| 18 | 編輯器存檔後，紀錄檔的換行從 LF 變成 CRLF | Plugin 寫的紀錄檔一律 LF；Windows 編輯器另存可能改成 CRLF | 讀取與 `validate` 不受影響（實測：改成 CRLF 後 `validate`、`get-record` 正常），但 `git diff` 會顯示整檔改變；還沒 commit 就 `git checkout -- <那個檔>` 還原，請學員只讀不存 |
| 19 | D2 檢查點 6 提案者的 Agent 跑 `ship-package` 被拒，errors 寫 `finalize-proposal: proposal base revision is stale; rebase-proposal, then obtain fresh approval: …`（冒號後是 `commit <12 碼> does not hold the Registry at …` 或 `the Registry committed at <12 碼> does not reproduce the recorded base digest, …`），`completed` 是 `[]`（簽章還沒記進審查包，什麼都沒寫入） | 檢查點 3 提交提案之後，模型又被改過（例如提案者的 Agent 又登記或修改了候選，或有人跑了 `amend-policy`）。夥伴核准的是提交當時那一版模型，核准不涵蓋改過的模型 | 先問兩人：「夥伴核准的是哪一版模型？」改動是提交後誤加的候選：請提案者的 Agent 用 `retract-candidate` 撤回，模型回到核准的那一版，重跑 `ship-package` 就會通過（實測）。改動要留下：照 `next`（`the proposal base is stale; rebase-proposal, then …`）請提案者的 Agent 跑 `rebase-proposal --package-root domain-memory/changes/CP-D2-001`（只在看到這個錯誤時才跑；基準沒過期時它只回 `the proposal base is current; nothing was written`，不動核准）：它只改審查包，回報 `status` 回到 `submitted`、`proposal_revision` 加 1、`approvals_retired`（作廢的舊核准數）。接著夥伴重貼檢查點 4 第二段（先讓 Agent 說明模型改了什麼，再回「核准」；會再做一個簽章 commit）與檢查點 5，提案者重跑檢查點 6。push 時 hook 會說 `for 3 commits.`。`rebase-proposal` 不改提案內容：提交後才登記的候選不會跟著升級，`validate --require-reviewed` 會說它 `not reviewed`；內容要改就退回重做。不要手改 JSON，也不要用 `--no-verify` |
| 20 | `ERROR: Command '[...]' timed out after 60 seconds; …; set DOMAIN_MEMORY_GIT_TIMEOUT to a larger number of seconds to wait longer` | 防毒掃描或 OneDrive 同步讓 `git verify-commit`、`ssh-keygen` 變慢。經 `dm.ps1`／`dm.sh` 呼叫時每次 git 呼叫等 60 秒；push 時的 hook 不經 dmlib，用 Plugin 預設的 15 秒 | 訊息有 `nothing was written, so it is safe to run again` 就直接重跑；沒有這句（`ssh-keygen`、`git config`）先請 Agent 查看狀態再重跑。仍逾時：請 Agent 在同一個終端機設 `$env:DOMAIN_MEMORY_GIT_TIMEOUT = '120'`（Git Bash／macOS：`export DOMAIN_MEMORY_GIT_TIMEOUT=120`）再重跑；值不是正數時 Plugin 回 `must be a positive number of seconds` |
| 21 | 新對話的 Agent 答不出 `AGENTS.md` 的規則（例如夥伴的 Agent 說不出自己不能做什麼），或沒照 Skill 做（自己編檢查方式、commit 前沒列檔案） | 有些工具不會每次都主動讀 `AGENTS.md`；Claude Code 2.1.277 起才在沒有 `CLAUDE.md` 時直接讀 `AGENTS.md`（演練：2.1.288、2.1.304 會讀，2.1.266 不讀），Repo 有 `CLAUDE.md` 時不理會 `AGENTS.md`；課前把學員機的工具更新到新版。Skill 只有放在工具會自動載入的位置、且提示詞說出它的名字才會被用上 | 請學員說「請先讀 AGENTS.md」，再重貼剛才的提示詞；沒用上 Skill 就在提示詞點名，例如「用 check 檢查剛才這一段」「照 signed-commit 做」。Skill 找不到時，請 Agent 照開場檢查點 1 第 1 步重放。**不要讓 Agent 建立 `CLAUDE.md` 或把 `AGENTS.md` 改名**：學員包刻意不附 `CLAUDE.md` |
| 22 | 改用 Recovery 後，`resume-<段>` 的新對話用不了 Skill（`check`、`signed-commit` 等不存在），或 `AGENTS.md` 少了學員寫的「通用語言與邊界」 | `dlc-recovery` 步驟 1 沒做完：第 2 步的指令只複製 `notes/`、`docs/handoffs/`、`AGENTS.md`，放 Skill 的資料夾要第 1.3 步另外複製 | 回提案者原本的對話（在原 Repo），請 Agent「照 dlc-recovery 步驟 1.3，把原 Repo 放 Skill 的資料夾原樣複製到 resume-<段> 的同一路徑」；`AGENTS.md` 沒帶到也同樣從原 Repo 複製。然後在 `resume-<段>` 開新對話（新對話才會自動載入 Skill）。夥伴已 commit 過時，新複製的檔案下一次由夥伴的對話一起 commit |
| 23 | `check` 回「失敗：…」，但學員看 Agent 的回報覺得這一步做對了 | `check` 對照的是 notes、實際指令結果和學員的決定，三樣有一樣對不上就失敗；常見是 notes 沒寫、或寫的和實際輸出不一致，也可能真的漏了一步 | 請學員問：「是哪一個條件沒過？貼出你檢查時執行的指令和輸出。」只是 notes 沒寫或寫錯，就請 Agent 補正後再「用 check 檢查剛才這一段」；真的漏做就照「失敗時」處理。不要讓 Agent 改測試、改 Registry 或放寬條件來換成功 |
| 24 | D2 檢查點 4 第二段：夥伴的 Agent 跑 `verify-proposal` 回 `ERROR: proposal base revision is stale; rebase-proposal, then obtain fresh approval: …`（exit 1）；或沒停下照樣 commit，檢查點 6 的 `ship-package` 回 `finalize-proposal: only a verified proposal may be finalized`、`status` 仍是 `submitted` | 提交提案後、夥伴核准前，模型又被改過（例如提案者的 Agent 又登記了候選）。演練實測：此時 `ship-package` 會先寫入簽章證明（`completed` 有 `attest-signed-commit`），和第 19 列「什麼都沒寫入」不同 | Runbook 檢查點 4 第二段已要求 `verify-proposal` 沒回 `Proposal test evidence verified.` 就停下、不 commit。處理同第 19 列：誤加的候選用 `retract-candidate` 撤回後重跑檢查點 4 第二段；要留下就 `rebase-proposal`，再重貼檢查點 4 第二段、檢查點 5、檢查點 6 |
| 25 | 走第 19／24 列的 `rebase-proposal` 之後，檢查點 6 的 ③ 回失敗：`validate --require-reviewed` 說某筆 `is not reviewed` | `rebase-proposal` 不改提案內容，提交後才登記的候選不會跟著升級（演練實測） | 屬預期，不算這組失敗：請提案者的 Agent 把這筆候選和原因記進 `notes/d2.md`，留到下一次核准；其他項目（applied、`verify-audit` valid、push）照常確認。不要為了讓 ③ 通過而手改紀錄或撤回已核准的內容 |
| 26 | D2 檢查點 2 或 Recovery 步驟 2：`amend-policy` 印出 `The Registry revision moved once, so every captured base revision is now stale and needs fresh approval.` | 改政策會讓 Registry 版本前進一次；已送出、還沒套用的提案就得重新核准 | 這時還沒有提案，屬正常提醒，不用處理（`AGENTS.md`「領域模型」已寫）。Agent 想因此重做或停下時，請學員說「照 AGENTS.md，這時沒有提案，繼續」。檢查點 3 送出提案之後才跑 `amend-policy`，就照第 19／24 列處理 |
| 27 | `make_record.py --batch` 只回報一筆錯誤就停了 | 批次在第一筆沒通過的紀錄就停下，後面的還沒檢查 | 屬預期（`record-candidates` Skill 已寫）：修好那一筆再重跑，直到全部通過；不要讓 Agent 改成一筆一筆手寫進 `domain-memory/` |
| 28 | Agent 整段用英文回報 | 工具或模型的預設語言（演練：Recovery 新開的對話、夥伴的對話都出現過） | `AGENTS.md` 工作規則第 1 條已寫「一律用繁體中文回覆」；仍是英文就請學員說「照 AGENTS.md 用繁體中文回覆」 |
| 29 | D2 夥伴寫的 notes 段落不見了 | 兩個對話寫同一個 `notes/d2.md`，其中一個整檔覆寫（演練：提案者的 Agent 在檢查點 3 蓋掉夥伴檢查點 1、2 的紀錄） | `AGENTS.md` 工作規則第 5 條已寫「notes 只附加、兩個角色各寫自己的一節」；發生時請被蓋掉的那一方從自己的對話補回，並說「照 AGENTS.md，notes 只附加」 |

## 6. 時間風險

| 風險 | 早期訊號 | 處置 |
|---|---|---|
| D1 29 分鐘、D2 27 分鐘仍偏緊（規格 R1） | 第 28 分還不到 3 個詞；第 51 分還沒 submit | 不延長；第 43 分 `dlc-rec-d1`、第 51 分或卡 5 分鐘 `dlc-rec-d2` |
| D3 依序進行，一段落後連鎖拖延（R2） | 第 100／145／195 分 Agent 還在寫核心 | 照各頁「最低完成線」收尾，照樣進 counterfactual 與 Review（第 106／151／203 分）；揭曉後用 `dlc-rec-d3*` 接續下一段，下一段直接照最低完成線做 |
| **D3c 最重** | 第 184 分還在討論邊界；第 195 分核心未完成 | 只做 Aggregate 與兩條規則也合格；**保住第 203–214 分 Review**；延伸全部放棄 |
| Agent 自己發明 API | 交接單沒提 API、Agent 計畫裡出現卡上沒有的路徑 | 叫他們回到卡上「API」小節，Handoff 明寫「介面照卡」 |
| 延伸 AC 吃掉時間 | 在核心沒做完前做發票資訊驗證、Audit、查詢欄位 | 指著卡上的［延伸］標記：「這些最後做」 |
| counterfactual 誤判（R6） | 只看 exit code | 只認 `killed`；D2 用 `--expect` 寫下預期的斷言，D3 看 `failure_evidence` 是 assertion 而不是 import／語法錯誤（後者是 `inconclusive`） |

## 7. 課後清理

- [ ] 確認每組已在回顧檢查點 4 只刪除私鑰 `signing-key`。同一個資料夾裡的 `signing-key.allowed_signers` 刻意保留：它只有公鑰，Git 驗證今天的簽章要用它。公用電腦由主持人課後連同 `C:\dlc` 一起刪除整個金鑰資料夾：PowerShell `Remove-Item -Recurse -Force "$env:USERPROFILE\.dlc-keys"`；Git Bash `rm -rf ~/.dlc-keys`。主持人示範金鑰同樣刪除。
- [ ] 確認沒有人把 `signing-key`（無副檔名的私鑰檔）複製進 Repo、貼到 Agent、表單或聊天、或出現在截圖。
- [ ] 公用電腦：刪除學員解出來的 `participant-dlc-open` 資料夾（Recovery 也解在裡面）；清除瀏覽器中 `stwdlc:` 開頭的 Runbook 暫存（或請學員在 Runbook 內清除）。
- [ ] 收回學員匯出的 Runbook ZIP（若有收集），存放時視為個人資料。
- [ ] 記錄本場：各組使用了哪些 Recovery、在第幾分鐘；哪些段落超時；這些資料回填規格 §7 的真人演練紀錄（未有實際場次前，該項一律 `NOT_RUN`）。

## 8. 參考

- 觀察與介入：`evaluation/observation-guide.md`
- 參考 Registry 與還原：`evaluation/reference-registry/README.md`
- 參考解答與 Agent 常見錯誤：`evaluation/reference-solutions/{d3a-e-invoice,d3b-points-redemption,d3c-group-partial-refund}/SOLUTION-NOTES.md`
- Recovery 原始來源：`facilitator/recovery/<段>/RECOVERY.md`
