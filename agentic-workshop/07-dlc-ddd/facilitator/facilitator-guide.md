# DDD DLC 主持人手冊

> 對象：DDD DLC（180 分鐘加課）的主持人與助教。學員已完成主課（Tool → Teammate → Digital Worker）。
> 主題：**Agent 的領域記憶**。把領域知識做成經審查、以檔案保存的 Domain Memory，再用它約束之後的每一次程式變更（要有證據、經過審查）。DDD 概念全部透過 domain-memory Plugin 0.10.15 的操作來教，不開理論講堂。
> 依據：`docs/instructions/11_DDD_DLC產製指令書.md`（以下稱「規格」）。檢查點以 `agentic-workshop/materials-dlc/CHECKPOINTS.md` 為準，解鎖碼在 `agentic-workshop/materials-dlc/unlock-codes.json`（本手冊不重抄碼，避免兩份不一致）。
> 本手冊與 `evaluation/` 底下所有檔案只給主持人，**不得**放進學員包、Runbook 或投影。

## 0. 一頁摘要

| 分鐘 | 段落 | 投影 | 你要做的關鍵動作 |
|---|---|---|---|
| 0–10 | 開場與環境 | 解鎖頁 → 4 個檢查點 | 盯 C:\dlc 短路徑、Store 別名、SHA 核對；第 7 分配對 |
| 10–35 | D1 共同語言與邊界 | 6 個檢查點 | 名稱矛盾與邊界洩漏要讓學員在 `cite` 證據中親眼看到 |
| 35–60 | D2 審查與核准（成對） | 6 個檢查點 | 第 45 分或卡 5 分鐘把 `dlc-rec-d2` 私下提供給該組；示範簽章 |
| 60–70 | 休息 | 休息頁 | 巡 D2 落後組，確認大家都有可接續的 reviewed Registry |
| 70–95 | D3a 電子發票 | 6 個檢查點 → 停手 → 2 頁揭曉 | 解鎖時宣布核心／延伸與 API 小節；揭曉後才可發 `dlc-rec-d3a` |
| 95–125 | D3b 點數折抵 | 同上 | 同上；`dlc-rec-d3b` |
| 125–155 | D3c 團體部分退款 | 同上 | **最重的一段**：保住 Review 時間；`dlc-rec-d3c` |
| 155–165 | D4 交接 | 3 個檢查點 | stale 證據不准跳過；更新事實只到候選 |
| 165–180 | 回顧 | 4 個檢查點 | 討論「走過場的自我核准」和「真的擋得住錯的核准」差在哪裡 |

三條不可破的規則：

1. **不延長段落**。落後就用 Recovery 接續，記錄原因與時間。
2. **Recovery 不作為小組成果評分**，只視需要私下提供（Recovery 碼只在講者備註 `data-code`，不投影、不貼群組）。
3. **`dlc-rec-d3*` 只能在對應段的揭曉頁之後**提供。

## 1. 課前檢查清單

### 1.1 一週前

- [ ] 確認學員機器：Windows 10/11，可裝軟體或已預裝下列項目。
- [ ] **Python 3.13 與 `py` launcher**：`py -3.13 --version` 要有回應。沒有 launcher 的機器，請學員用 python.org 安裝程式重裝並勾選 py launcher（規格 §9 第 3 點尚未決定是否提供可攜版；若教室不允許安裝，課前要決定替代方案）。
- [ ] **Git for Windows ≥ 2.34**（SSH 簽章需要）：`git --version`。
- [ ] 每台機器一個可讀寫本機資料夾、能執行終端指令的通用 Coding Agent。
- [ ] 通知學員：學員包一律解壓到 **`C:\dlc`**（不要放桌面、OneDrive、深層資料夾）。原因見 §5 陷阱 1（WinError 206）。
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

- Plugin 固定 0.10.15，只封裝執行用的檔案（不含開發用的 `evals/`、`scripts/test_*.py`、`README.md`、`ruff.toml`），檔案內容未經修改，封裝於 `participant/vendor/domain-memory-0.10.15.zip`，逐檔清單 `domain-memory-0.10.15.zip.SHA256SUMS`（70 個 Plugin 檔案＋ZIP 本身＝71 行）。
- 目前 ZIP 的 SHA256 以 `domain-memory-0.10.15.zip.SHA256SUMS` 最後一行為準。
- 學員在開場檢查點 2 應看到 `SHA OK 71 files` 與 `"version": "0.10.15"`。看到 `SHA MISMATCH` 一律停用該份 Plugin，換一份重新下載；不要「先用用看」。

### 1.4 主持人自己的機器（課前 30 分鐘）

- [ ] 在自己的機器以學員身分走完開場四個檢查點（約 3 分鐘＋安裝 50 秒）。
- [ ] 還原一次 reference Registry（見 `evaluation/reference-registry/README.md`「還原」），確認 `validate --require-reviewed`、`verify-audit`、`verify-git-governance` 全 OK。D2 示範與降級都靠它。
- [ ] 準備 D2 示範用的兩個身分：`proposer@example.com`、`maintainer@example.com`；示範金鑰放 `%USERPROFILE%\.dlc-keys\demo-maintainer\`。
- [ ] 投影開啟 `facilitator-deck.html`，副螢幕開講者模式，確認 Recovery 碼只出現在講者畫面。

### 1.5 起始 Repo 殘留字詞審查（規格 §5.1）

以規格 §5.1 的 grep（排除 `.pyc`、`.venv`、`.git`）掃 `participant/repository/smart-ticket-dlc-base/`：**零命中**（2026-10-07 實測）。沒有需要刻意保留的殘留。若之後修改起始 Repo，重跑並把每個命中與保留理由補在這裡。

## 2. 教室配置與分組

- **兩人一組、一台機器、兩個 Agent 對話**。選 D1 做得比較完整的那台；它的主人當 **Proposer**（提案者，用自己的 Agent 對話準備 Change Package，不得核准、不 commit），另一人當 **Maintainer**（夥伴，另開終端機啟動自己的 Agent 對話：持簽章金鑰、讀審查包後核准、簽章 commit、push）。Maintainer 的 Agent 對話開到課程結束：D3a–c 檢查點 5 與 D4 檢查點 3 的簽章 commit、回顧的刪除私鑰都在這個對話執行。
- 開場第 7 分鐘（「找夥伴」頁）就配好對；D1 各人在自己的 Repo 做，D2 起兩人共用一台機器。開場有人環境裝不起來，D1 起先以夥伴的機器為主。
- **人數奇數時組成三人組，第三人當觀察員（Observer）**：看每一步是不是在對的人的 Agent 對話裡執行（核准、簽章 commit、push 只出現在 Maintainer 的對話；proposer 的 Agent 不碰 `record-approval`），並一起看 `verify-audit` 結果。D3 起 Observer 負責對照決策卡，並核對 Agent 回報的 counterfactual 結果。
- D3 三段可以換人操作鍵盤與發言，但提案者與夥伴的 Agent 對話不換；簽章 commit 一律在持鑰夥伴的對話。**Maintainer 的私鑰不換人**：只有持鑰人能簽觸及 Registry 的 commit。
- 座位安排讓兩人能同時看同一個螢幕；助教巡堂路線要能看到螢幕上的終端機輸出。
- 明講（規格 R3）：`record-approval` 只比對身分字串，同機雙身分仍可通過；今天的成對簽章是**教學示範，不是安全保證**。治理強度來自「誰持有簽章私鑰」。

## 3. 逐段腳本

每段固定節奏：解鎖頁（大字解鎖碼）→ 檢查點總覽頁（按 `T` 開段落計時，時間軸自動標示目前檢查點）→ 每到時間點翻到下一個檢查點頁。投影只顯示時間、檢查點編號與一句話任務；提示詞與表單都在 Runbook。各頁講者備註有「說／看／介入訊號／提示」，本節只列每段的骨架與決策點。

**學員的操作方式（每段都一樣）**：複製 Runbook 的提示詞 → 學員的 Agent 執行 Plugin、輔助腳本與 Git 指令並白話回報 → 學員用短回覆做決定（「同意」「選 B」「第 3 項不要」）→ Agent 把結果寫進 `notes/<段落>.md` 或 `docs/handoffs/`。學員不自己打指令；表單每段最多一張，只記人的決定。巡堂時看的是這個循環有沒有轉起來：有沒有讀 Agent 的回報、有沒有在 Agent 停下時真的做決定、Agent 有沒有在學員同意前就寫入。卡住時給學員一段可直接貼的補救提示詞，例如「請解釋剛才的錯誤代表什麼，不要自己修改或重試，給我兩個做法讓我選」，不要替學員打指令。D2 核准的治理意義不變：由夥伴本人坐到鍵盤前、在自己的 Agent 對話裡讀過審查包後回「核准」，夥伴的 Agent 才簽章；提案者的 Agent 不可碰夥伴的金鑰或代替核准。DLC 兩人共用一台機器（D3 延續同一個 Repo 與金鑰），所以「自己的」指自己另開的終端機與 Agent 對話，不是另一台電腦。

### 3.1 開場與環境（0–10，群組 `dlc-opening`）

| 分鐘 | 檢查點 | 你說／做 |
|---|---|---|
| 0 | 解鎖 | 公布開場解鎖碼；說明今天的節奏：複製提示詞 → Agent 執行並白話回報 → 需要時回一句話決定 → Agent 寫紀錄。學員只需自己下載 `participant-dlc-open.zip`、「全部解壓縮」到 `C:\dlc`、在 Repo 根目錄開 Agent，先貼 Runbook 的工作規則 |
| 0–3 | 1 · 安裝相依套件與測試 | Agent 回報 **76 passed**；沒有跑 `pip install -e .` |
| 1–2 | （等待安裝時） | 「為什麼是 Domain Memory」「今天怎麼進行」兩頁 |
| 3–5 | 2 · 解出 Plugin 並核對 SHA256 | Agent 回報 `SHA OK 71 files`、`"version": "0.10.15"` |
| 5–8 | 3 · 專案就緒與品質關卡檢查 | Agent 經 `tools/dm.ps1`／`dm.sh` 執行：`readiness` 說 brownfield，`quality-gates` 只有 pytest；小組口頭討論「哪些錯只能靠測試與人」 |
| 7 | 找夥伴 | 配對；奇數時三人組，第三人當觀察員 |
| 8–10 | 4 · 確認真實 Python | Agent 回報 `python` 路徑在 `.venv\Scripts\`、不含 `WindowsApps`；`doctor.py` 最後一行「全部必要項目通過。」（`[--]` 只是提醒，不算失敗）；`notes/opening.md` 有四段結果後才建立起始 commit，commit 後 `git status --short` 是空的 |

巡場看：學員是不是「貼提示詞 → 看回報 → 對照過關字樣」，而不是自己在終端機打指令。卡住時請學員貼該檢查點的「如果卡住」提示詞，讓 Agent 先解釋錯誤、列出處理方式，等學員同意再做；不要替學員改指令。最常見的是 Agent 沒經 `dm` 腳本（cp950 錯誤）或沒在同一個指令裡啟用 `.venv`（`python` 指到 `WindowsApps`）：請學員重貼工作規則。

降級：第 10 分鐘仍有人未過 → 兩人一機繼續，D1 以夥伴機器為主；請 Agent 在 `notes/opening.md` 記下卡在哪一步，不延長本段。

### 3.2 D1 共同語言與邊界（10–35，群組 `dlc-d1`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 10–13 | 1 · 人工選來源 | Agent 跑 `discover-sources` 並逐列建議；**學員回覆決定**。必含 `docs/requirements/`、`docs/adr/`、`src/`、`tests/`，排除 `**/__pycache__/**` |
| 13–17 | 2 · 初始化與確認來源 | Agent 依學員的決定跑 `init-domain-memory --storage-mode tracked --review-mode local-draft-only` ＋ `confirm-sources`；不 commit |
| 17–22 | 3 · 詞彙候選 | Agent 先列名稱矛盾、再提詞彙草稿與證據原文；學員選 ≥ 5 個、改定義、選矛盾的處理方式；Agent 寫 `d1-records.json` 並試跑 `make_record.py`（內部呼叫 `cite`） |
| 22–27 | 4 · Context 與規則候選 | 同樣由學員決定 ≥ 2 個 contexts、≥ 2 條 rules；Agent 一次登記為候選並跑 `validate`、`verify-evidence` |
| 27–31 | 5 · 找缺口與查詞 | Agent 跑 `coverage` 與兩句 `resolve-terms`；學員選一個要記下的缺口 |
| 31–35 | 6 · 查 Context 與檢查越界 | Agent 跑 `get-context`、兩個不同 Context 的 `analyze-boundary`，對照程式附證據；學員判斷是否洩漏，填「D1 決定」 |

教學重點：名稱矛盾（Fare Policy／Discount Policy；Compensation／補償在 ADR 有、只出現在一個測試名稱、沒有對應類別）與 Context 邊界洩漏，**一定要讓學員在 Agent 摘錄的 `cite` 證據裡親眼看到**，不要口頭告訴他們。Runbook 的提示詞不會主動指向這兩組；Agent 的矛盾清單漏掉 Fare Policy／Discount Policy 時，可以請學員補一句「也比對 Fare Policy 和 Discount Policy」（可選）。Agent 會提草稿，但「哪些來源、哪些名詞、定義怎麼寫、是不是越界」必須是學員的回覆；學員對每個草稿一律回「同意」時，請他挑一個，要 Agent 把證據原文再念一次。

紀錄：Agent 把每個檢查點寫進 `notes/d1.md`，候選寫進 `d1-records.json`；學員只填一張「D1 決定」（三個選擇＋一個短文字）。看紀錄裡有沒有學員的決定與理由，不因少填表扣分。

Recovery：第 35 分鐘 D1 未完成的組，私下提供 `dlc-rec-d1`（Repo＋已確認 source map＋D1 候選集，全部為候選）。切換後 `domain-memory/` 仍未追蹤；D2 夥伴在 `resume-d1` 開自己的 Agent 對話。

收尾（第 35 分前）：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。

### 3.3 D2 審查與核准，成對（35–60，群組 `dlc-d2`）

開始時兩人各在自己的 Agent 對話貼一次 Runbook 的工作規則（提案者的規則明列不可執行核准、簽章、commit、push，也不可讀 `.dlc-keys`）。下表「誰」指在誰的 Agent 對話裡貼提示詞；表內指令都寫在提示詞裡，由該 Agent 執行並白話回報。

| 分鐘 | 檢查點 | 誰 | 重點 |
|---|---|---|---|
| 35–38 | 1 · 夥伴建立簽章金鑰 | Maintainer | `init-signing-key --key-file "$env:USERPROFILE\.dlc-keys\maintainer\signing-key" --sign-every-commit`（Git Bash：`"$HOME/.dlc-keys/maintainer/signing-key"`）；**先於第一個 Registry commit** |
| 38–43 | 2 · 設定審查政策與推送檢查 | Maintainer | `amend-policy` 依序 `authorized_signers`（fingerprint）→ `review_trigger git-push` → `review_mode scm-verified --verifier git-signed-commit`；`install-git-hitl-hook`；`governance-readiness` ready |
| 43–48 | 3 · 建立變更審查包並送出提案 | Proposer | 學員按 Runbook 下載鈕取得 `participant-dlc-d2.zip`，Agent 把格式範本放進 `worksheets/`；Agent 提 2–3 個 counterfactual 方案、學員選一個（只認 `killed`）；`cp-d2.json` 的 `promote` 列 Registry 每個有候選的資產（用過 D1 Recovery 含 aggregates、interactions、decisions，漏列會在 CP6 `validate --require-reviewed` 報 not reviewed）；`fill_package.py`（測試實際執行，不預填 PASS），放 `domain-memory/changes/<id>/`；學員回「送出」才 `submit-proposal` |
| 48–53 | 4 · 夥伴核准與簽章提交 | Maintainer | Agent 先讀審查包、貼一條規則的證據原文並停下；Maintainer 回「核准」後才 `record-approval --reviewer maintainer@example.com`、`verify-proposal`、`git commit -S` |
| 53–56 | 5 · 寫出核准證明並驗證 | Maintainer | `write_scm_attestation.py --commit HEAD`、`verify-git-governance --commit HEAD`；輸出提到的 `finalize-proposal` 是 Proposer 在 CP6 的步驟，Maintainer 的 Agent 不執行 |
| 56–60 | 6 · 完成提案並全部驗證 | Proposer → Maintainer | Proposer 的 Agent：`finalize-proposal` → `apply-approved-updates` → `validate --require-reviewed` → `verify-audit`；Maintainer 的 Agent：簽章 commit、`setup_remote.py`、push（不得 `--no-verify`） |

巡堂看三件事：核准與簽章只出現在 Maintainer 的對話；Maintainer 回「核准」前說得出哪一行證據支持哪條規則；Agent 停下時學員真的做了決定。學員只填一張「D2 決定」（角色、審查決定、三項確認），其餘紀錄由 Agent 寫進 `notes/d2.md`。卡住時請學員貼 Runbook「卡住時」的補救提示詞（請 Agent 白話解釋錯誤、不改設定、不重做 commit、不繞過 hook），不要替學員打指令。

收尾（第 60 分前）：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。

**Recovery 釋放規則（`dlc-rec-d2`）**：

- 最早第 **45** 分鐘可用（規格 §3.2）。
- 任一組在任一步**卡住 5 分鐘**即可私下提供；第 45 分多數組還沒 `submit-proposal` 時，對卡住的組提供。
- 改用 Recovery 的組照 Recovery 頁三步切換（與 `recovery/d2/RECOVERY.md` 第 1–3 節同一份指令，見 §4「Recovery 切換做法」）：提案者原對話解出 Recovery 並複製成 `resume-d2`，原 Repo 的 `notes/`、`docs/handoffs/` 一併複製，原狀態寫進 `resume-d2` 的 `notes/d2.md`（不寫原 Repo）；**夥伴**在 `resume-d2` 新開自己的 Agent 對話，從 `repo.bundle` 還原簽章歷史、以自己的金鑰接手（`amend-policy authorized_signers`、hook、readiness ready），回「同意」後做簽章 commit；提案者在 `resume-d2` 新開對話建環境並跑 `validate --require-reviewed`、`verify-audit`。夥伴的接手簽章就是這組的簽章練習；有空再看你的簽章示範（下方）。

**成對簽章示範腳本（約 4 分鐘，用 reference Registry 或自己的乾淨複本）**：

1. 「Proposer 做完 Change Package，現在換 Maintainer 坐到鍵盤前，用自己的 Agent 對話。」示範 `record-approval --reviewer maintainer@example.com`。順便示範反例：以 `proposer@example.com` 當 reviewer 會被拒；再說明以另一個字串也能通過，**所以真正的保護是簽章**。
2. `git -c user.name="DLC Maintainer" -c user.email=maintainer@example.com commit -S -m "..."`，接著 `git log --show-signature -1`，指出 `Good "git" signature for maintainer@example.com`。
3. `write_scm_attestation.py --commit HEAD` → `verify-git-governance --commit HEAD`：「核准證據不是一行文字，是一個可驗證的已簽章 commit。」
4. （有時間）做一個不簽章、觸及 `domain-memory/` 的 commit 再 push，給大家看 hook 拒絕的輸出。
5. 收尾：「私鑰在 `%USERPROFILE%\.dlc-keys\`，不在 Repo、不在 `.ssh`、不截圖。回顧檢查點 4 只刪私鑰 `signing-key`，`signing-key.allowed_signers` 保留；公用電腦課後再刪整個 `.dlc-keys` 資料夾。」

### 3.4 休息（60–70）

巡一圈：每組都要有一份 `validate --require-reviewed` OK 的 Registry（自己的或 Recovery），D3 才接得下去。還沒有的組，休息時協助還原 `dlc-rec-d2`。

### 3.5 D3 共同節奏（70–155）

三個情境**全體依序、三個都做**，每段在前一段成果上累積。每段六個檢查點同一個節奏：

1. 學員貼提示詞：Agent 存下需求卡、執行 `resolve-terms`／`get-context`，已知事實與知識缺口分開寫進 `notes/d3*.md`。
2. Agent 每題提兩個選項＋證據（「類別:id」或「檔案路徑:行號」），**人**討論後以短回覆選擇（例如「1A、2B」）；`analyze-boundary` 的 source 填提供資料或能力的一方、target 填使用的一方，回 `no_registered_collaboration` 就對調再查一次；Agent 依選擇寫成 D3 決策卡（`docs/handoffs/d3*.md`），人確認不變量後回「同意」。
3. Agent 依交接單先提計畫、等「同意」，分兩段實作，每段停下回報**實際**測試結果，人回「繼續」才往下。
4. Agent 先列出每條新規則要改壞哪裡，人同意後才執行 `counterfactual`；只認 `killed`，survived 補測試用同一組字串重跑。Agent 指出沒有任何輸入分辨得出改壞前後（等價，例如另一段程式也擋住，或輸入不可能落在那個邊界，如 D3a 5% 稅額下整數總額永遠不會落在 .5）時，學員確認後標「等價、未證明」，那個 survived 的 cf 檔保留並一起 commit。`--test-command` 帶 `-W ignore::DeprecationWarning`：萬一有套件過時警告（例如用 D2 Recovery 時），它會把真正的失敗訊息擠出 `failing_evidence`；只有被拒絕執行、沒有 verdict 的那次留下的 cf 檔，重跑前先刪掉。
5. Agent 用 `git status --short`（新檔只出現在這裡）、`git diff` 與測試回答四個審查問題；人同意後提案者的 Agent 才用 `make_record.py` 登記，**仍是候選**；提案者的 Agent 不得執行 `record-approval`、`amend-policy`、`git commit`／`push`。夥伴讀過紀錄後，在**自己的 Agent 對話**做簽章 commit（與 D2 相同）。
6. 停手 → Agent 整理決策摘要 →「請先停手」頁 → 兩頁揭曉 → 學員填一張揭曉對照表單（兩個下拉、一個勾選、一句話）→ 收尾：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。

**巡場看流程**：每組是否「貼提示詞 → 看 Agent 回報 → 自己做決定 → 讓 Agent 記錄」。決策點（檢查點 2、4）學員要自己選，回「你決定」就介入。卡住時給可直接貼的補救提示詞，不替學員決定：

- Agent 替學員選了或開始改程式：「停下，不要再修改。如果你已經改了檔案，列出改了哪些。請回到只列選項與證據，等我們選擇。」
- Agent 說「完成」但沒附實際輸出：「請貼出你實際執行的指令與輸出；沒有執行的標『未驗證』。」
- counterfactual 只有亂碼或 ERROR：「這不算 killed，請說明原因，不要換字串。」
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

### 3.6 D3a 電子發票（70–95，群組 `dlc-d3a`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 70–73 | 1 · 讀情境卡與已審查事實 | 宣布核心／延伸與 API 小節。H1：「逾時代表什麼？對方可能已經開出發票了嗎？」 |
| 73–78 | 2 · 對外介面（Port）與邊界決策 | 發票歸哪個 Context？Port 放哪層？誰把 Order 翻成發票語言？H2：「付款 Gateway 沒有 Port，這次要照做還是改？」 |
| 78–85 | 3 · 交接單與 Agent 實作 | 盯鎖：`pay_group` 持有 RLock 時呼叫 `pay`；盯「付款請求內同步重試 5 次」 |
| 85–89 | 4 · 反事實檢查 | 先做建議的 3 個 |
| 89–92 | 5 · 檢視差異與登記候選 | 有沒有供應商代碼（`9001`、`2001`）出現在 Domain／Service |
| 92–95 | 6 · 停手與揭曉對照 | 揭曉：新的 Invoicing Context；Port `InvoiceIssuer` 只回 ISSUED／REJECTED／UNAVAILABLE；Adapter 翻譯代碼、逾時、連線失敗；鎖內只建 PENDING，鎖外呼叫一次；冪等鍵＝order_id |

時間判斷：參考解答完整 15 條 AC 約 340 行程式＋320 行測試，25 分鐘只夠核心切片。第 85 分 Agent 還沒做完核心也要進 counterfactual。

### 3.7 D3b 點數折抵（95–125，群組 `dlc-d3b`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 95–98 | 1 · 讀情境卡與已審查事實 | 宣布核心／延伸與 API 小節。H1：「折抵要加在哪裡，才不會漏掉其中一條計價路徑？」 |
| 98–103 | 2 · 決定負責的 Context 與不變量 | 點數歸誰、理由；30% 上限歸誰；reserve／restore 的時機。H2：「預留要不要成為獨立概念？」 |
| 103–111 | 3 · 交接單與 Agent 實作 | 盯「點數塞進 `DiscountPolicy`」與「從 `total_fare` 扣點」；扣點位置要在座位規劃之後、寫入之前 |
| 111–116 | 4 · 反事實檢查 | 建議的 4 個，其中「上限以優惠後總額」「退款＝Order.amount」是先 survived 再補測試的好示範 |
| 116–121 | 5 · 檢視差異與登記候選 | 商業數字（30、100）是否只有一個家 |
| 121–125 | 6 · 停手與揭曉對照 | 揭曉：Membership 擁有點數與折抵規則（含 30% 上限）；Pricing 與三條計價迴圈一行不改；Booking 記折抵點數、推導 `payable_amount`；閘道扣 `payable_amount`＝Order.amount；發票自動是 500 → 476＋24 |

時間判斷：程式只約 +80 行，核心切片可行；省下的時間給 Review。D3a 未完成的組，揭曉 D3a 後已可用 `dlc-rec-d3a` 接續，本段不用從頭補 D3a。

### 3.8 D3c 團體部分退款（125–155，群組 `dlc-d3c`）

| 分鐘 | 檢查點 | 決策點 |
|---|---|---|
| 125–128 | 1 · 讀情境卡與已審查事實 | 宣布核心／延伸與 API 小節，並明講「本段最緊，延伸一律最後」。H1：「現在的退款紀錄能表達『同一筆訂票退過兩次』嗎？」 |
| 128–133 | 2 · Aggregate（聚合）邊界與不變量 | Aggregate root、唯一入口、恆等式誰保證、手續費歸誰、退款紀錄結構 |
| 133–142 | 3 · 交接單與 Agent 實作 | Handoff 要有「四份座位資料」「先拒絕再修改」「不要動 `total_fare`」與混合團範例 |
| 142–148 | 4 · 反事實檢查 | 建議的 4 個；第 142 分沒做完也進來 |
| 148–152 | 5 · 檢視差異與登記候選 | **不可壓縮**。看整筆退票路徑、恆等式在哪裡成立、座位四份是否一致 |
| 152–155 | 6 · 停手與揭曉對照 | 揭曉：團體 Booking 擁有旅客取消（`cancel_passengers` 唯一入口，全部檢查完才寫入）；費率帶與 D ≤ 0 不受理在同一模組、逐位向下取整；只釋放被取消旅客的座位；退款紀錄改 append-only 清單；部分取消過不可整筆退 |

**時間風險：這是三張卡最重的一張**。參考解答 +141 行、是唯一需要改既有資料結構的一張；核心切片勉強放得下，前提是學員從第 125 分就照卡上的 API 做。規格 R2 允許只完成 Aggregate 與兩條規則。寧可少做 AC，也不要吃掉第 148–152 分的 Review：本段教學重點全在 Review。

### 3.9 D4 交接（155–165，群組 `dlc-d4`）

| 分鐘 | 檢查點 | 重點 |
|---|---|---|
| 155–158 | 1 · 驗證來源、證據與稽核 | Agent 跑 `verify-sources`、`verify-evidence`、`verify-audit`，寫進 `notes/d4.md`。`verify-sources` 會是 `stale`、exit 1：D3 新增了檔案，來源資料夾列在 `changed_sources`，只改內容的列在 `content_changed`；`verify-evidence` 只有引用行被改過的證據是 `stale`、exit 1。兩者都是預期；要記下，不准跳過，也不讓 Agent 當場修。`verify-evidence` 只印 stale 的路徑，只要求數量與依檔案分組（每個檔案大約幾筆即可），不讓 Agent 自寫腳本對 id |
| 158–161 | 2 · 更新已變動事實 | Agent 先列更新清單（stale 候選的 id 從 D3 notes「審查與候選」取出，用 `get-record` 查；decisions 看 `review_status`，其他看 `status`），學員回「同意」後才用 `make_record.py --upsert` 登記，只到候選；reviewed 事實以新 id 候選取代；只是行號移動的 reviewed 事實維持 stale、不登記。參考：D3c 讓 `REFUND-004`、Booking 的「只能退一次」與 `ASIS-004` 不再成立 |
| 161–165 | 3 · 寫交接單並核對 id | Agent 依七段（Domain facts、Forces、Decision、External systems、Unknowns、Proof obligations、Counterfactual check）寫 `docs/handoffs/d4-next-agent.md`，每個 id 用 `get-record` 查證並回報核對清單；學員同意後，Maintainer 在自己的 Agent 對話簽章 commit（提案者的 Agent 不 commit） |

看什麼：Agent 是否等學員回覆才寫入；commit 是否在 Maintainer 的對話執行；id 核對清單是否全部查得到（查不到的移到 Unknowns，而不是換成猜的 id）；候選沒有寫成 reviewed。D3c 未完成者仍可用 `dlc-rec-d3c`（D3c 揭曉後）接續 D4。

收尾（第 165 分前）：請學員看 Runbook「完成後想一想」，挑第 2 題請 1–2 組分享（約 1 分鐘）。回顧檢查點 2 會再引用各段的答案。

### 3.10 回顧（165–180，群組 `dlc-retro`）

四個檢查點：請 Agent 從紀錄整理證據（165–169，Agent 寫 `notes/retro.md`）、比較哪些核准步驟擋得住錯（169–174，Agent 列出核准步驟，小組口頭討論）、挑選提示詞與一項行動（174–178，Agent 起草、每人挑選，寫成 `notes/my-prompts-<名字>.md`）、匯出與結束（178–180，Maintainer 請自己的 Agent 刪除私鑰，全員匯出）。討論只用口頭，不要求寫下來；檢查點 2 請學員回想各段「完成後想一想」第 2 題的答案，對照哪個技巧真的擋住了錯。必談：

1. 哪一個 reviewed 事實改變了 Agent 的輸出？
2. 哪一個候選差點被當成事實？
3. 走過場的自我核准，和真的擋得住錯的核准差在哪裡？（直接回到 R3：`record-approval` 只比字串）

看什麼：學員是否抽問 Agent「這句的證據在哪？」，把沒有證據的句子改成「未觀察」。最後提醒匯出 Runbook（`smart-ticket-dlc-runbook-<stamp>.zip`）並保存 `notes/`，以及刪除金鑰（§7）。

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

- Recovery 碼與一般碼分開、只視需要提供，不投影、不貼群組；Recovery 不作為小組成果評分。
- 使用 Recovery 的組如實記錄觸發原因與時間（依 Runbook 對應 Recovery 頁的做法）。
- Recovery 包只含可接續的 Repo（含 `domain-memory/`），不含觀察指引、counterfactual 證據原稿或任何 `evaluation/` 檔案。
- **Recovery 切換做法（五個 Recovery 頁共用，與各段 `recovery/<段>/RECOVERY.md` 同一份指令）**：原 Repo 不改名、不覆寫；Recovery 複製成同一層的 `resume-<段>`，從 `repo.bundle` 還原 Git 歷史（不重新 `git init` 出未簽章的起點 commit）。D1 只有一個不含 `domain-memory/` 的「起始 Repo」commit，兩步都由提案者的 Agent 做、沒有 commit。D2 起分三步：① 提案者原對話解出 Recovery、把原 Repo 的 `notes/`、`docs/handoffs/` 複製進 `resume-<段>`，原狀態寫進 `resume-<段>` 的 `notes/<段>.md`（原 Repo 什麼都不寫）；② **夥伴**在 `resume-<段>` 新開自己的 Agent 對話（先貼 D2【夥伴】規則）：還原歷史、`init-signing-key`（沿用 `.dlc-keys\maintainer\` 的 D2 金鑰，沒有就新建）、把 `keys/maintainer.allowed_signers` 附加到新的 allowed signers 檔、`amend-policy authorized_signers` 加入自己的 fingerprint、`install-git-hitl-hook`、`governance-readiness` ready，回「同意」後以 `git add domain-memory notes docs` 把複製來的 `notes/`、`docs/handoffs/` 一起簽章 commit（commit 後 `git status --short` 是空的）並 `verify-git-governance --commit HEAD`；③ 提案者在 `resume-<段>` 新開對話建 venv、測試、`validate --require-reviewed`、`verify-audit`、`verify-evidence`。之後 D3、D4 的 commit 照常由夥伴簽章。Git Bash 區塊整段包在 `( set -e … )` 子 shell 裡，任何一行失敗只結束這一段，不會關掉 Agent 的終端機。複製來的 `notes/` 提到的候選 id 是原 Repo 的，Recovery 的 Registry 不一定有，查不到是預期。
- D3a／D3b／D3c 的 Recovery 還原後，`verify-evidence` 會對引用行被改過的證據回報 `stale`，`verify-sources` 會因來源資料夾新增了檔案回報 `stale`，都是 exit 1，屬預期，留到 D4 處理。`git log` 最上面的「Recovery 參考實作」commit 是 `N`（未簽章），因為它不碰 Registry，hook 允許；Registry 的三個 commit 是 `G maintainer@example.com`。D2 起每個 Recovery 最下面的「Smart Ticket DLC base」（起始程式）也是 `N`，同樣不碰 Registry。

## 5. Windows 已知陷阱與修正

| # | 症狀 | 原因 | 修正 |
|---|---|---|---|
| 1 | D1 寫 Registry 時「檔名或副檔名太長」`WinError 206` | Plugin 在 `domain-memory/` 底下建很長的暫存資料夾名；放在桌面、OneDrive 或深層資料夾就超過路徑上限 | 解壓到 `C:\dlc`（Recovery 用 `C:\dlc-rec\<段>`）。已出錯的組：整個資料夾搬到 `C:\dlc` 再重跑該步 |
| 2 | `UnicodeDecodeError: 'cp950' codec ...` | 直接呼叫 `registry_tools.py`，缺 `-X utf8` | 一律經 `tools\dm.ps1`／`dm.sh`（固定 `py -3.13 -X utf8`） |
| 3 | counterfactual 印出亂碼（Big5）並以 ERROR 結束（exit 1） | `--test-command` 由 cmd.exe 執行，直譯器路徑寫錯 | 寫 `.venv\Scripts\python.exe -m pytest -q <測試>`（反斜線）。**只認輸出中的 `killed`**；`failing_evidence` 要是 assertion 失敗 |
| 4 | push 時 hook 失敗、或跳出 Microsoft Store | pre-push hook 呼叫裸 `python`，`python` 是 Store 別名（路徑含 `WindowsApps`） | push 前啟用 Repo 的 `.venv`；或關閉「應用程式執行別名」。開場檢查點 4 就要攔下 |
| 5 | push 被拒「Git commit signature is invalid」或未簽章 | 簽章在第一個 Registry commit 之後才設定；或 Recovery 接手時沒附 maintainer 的 allowed_signers | 簽章先於第一個 Registry commit（`--sign-every-commit`）；Recovery 照切換頁步驟 2（RECOVERY.md 第 2 節）附上 allowed_signers 那一行，不要讓 Agent 自己 `git init` 出未簽章的起點 commit；用 `git log --format='%h %G? %s'` 找出 `N` 的那個 commit |
| 6 | 新開的終端機裡 `python` 又不對 | venv 只對目前視窗有效 | 每個新視窗：PowerShell `Set-ExecutionPolicy -Scope Process Bypass -Force` ＋ `.\.venv\Scripts\Activate.ps1`；Git Bash `source .venv/Scripts/activate` |
| 7 | `ssh-keygen` 行為不同、金鑰路徑找不到 | Git Bash 與 PowerShell 的 `ssh-keygen` 不同 | 兩者皆可，但同一組全程用同一種 shell |
| 8 | clone／還原後 `verify-evidence` 把引用全部報成 `stale`（`verify-sources` 則把來源列在 `content_changed`） | `core.autocrlf=true` 轉換換行，Plugin 以原始位元組算雜湊 | 起始 Repo 已有 `.gitattributes`（`* -text`）；在已 `git init` 的 Repo 執行 `doctor.py` 時也會檢查。不要刪它 |
| 9 | push 時 hook 輸出亂碼或編碼錯誤 | hook 內 Python 用系統編碼 | Runbook 已在 push 前設 `$env:PYTHONUTF8 = '1'`（Git Bash `export PYTHONUTF8=1`） |
| 10 | 安裝很久或有人跑 `pip install -e .` | 不需要可編輯安裝 | 只用 `pip install -r requirements.txt`（約 50 秒） |
| 11 | `scan-secrets` 有 finding | 金鑰放進 Repo 內（含被 `.gitignore` 忽略的資料夾，只有 `.git`、`.venv`、`node_modules` 不掃；Repo 外的 `.ssh` 不會被掃到） | 金鑰只放 `%USERPROFILE%\.dlc-keys\<代號>\`（Git Bash `~/.dlc-keys/<代號>/`），預期 exit 0；另外，不要和 `~/.ssh` 的個人金鑰共用，那是不共用金鑰的規則，不是 scan-secrets 會抓的問題 |
| 12 | PowerShell 說「已停用指令碼」 | 執行原則 | `Set-ExecutionPolicy -Scope Process Bypass -Force`（只影響目前視窗） |
| 13 | push 出現 `unpacker error` | Repo 路徑太長 | 把 Repo 複製到短路徑（例如 `C:\dlc`）再 push |

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

- [ ] 確認每組已在回顧檢查點 4 只刪除私鑰 `signing-key`。同一個資料夾裡的 `signing-key.allowed_signers` 刻意保留：它只有公鑰，Git 驗證今天的簽章要用它。公用電腦由主持人課後連同 `C:\dlc` 一起刪除整個金鑰資料夾：PowerShell `Remove-Item -Recurse -Force "$env:USERPROFILE\.dlc-keys"`；Git Bash `rm -rf ~/.dlc-keys`。主持人示範金鑰同樣刪除。
- [ ] 確認沒有人把 `signing-key`（無副檔名的私鑰檔）複製進 Repo、貼到 Agent、表單或聊天、或出現在截圖。
- [ ] 公用電腦：刪除 `C:\dlc`、`C:\dlc-rec`；清除瀏覽器中 `stwdlc:` 開頭的 Runbook 暫存（或請學員在 Runbook 內清除）。
- [ ] 收回學員匯出的 Runbook ZIP（若有收集），存放時視為個人資料。
- [ ] 記錄本場：各組使用了哪些 Recovery、在第幾分鐘；哪些段落超時；這些資料回填規格 §7 的真人演練紀錄（未有實際場次前，該項一律 `NOT_RUN`）。

## 8. 參考

- 觀察與介入：`evaluation/observation-guide.md`
- 參考 Registry 與還原：`evaluation/reference-registry/README.md`
- 參考解答與 Agent 常見錯誤：`evaluation/reference-solutions/{d3a-e-invoice,d3b-points-redemption,d3c-group-partial-refund}/SOLUTION-NOTES.md`
- Recovery 原始來源：`facilitator/recovery/<段>/RECOVERY.md`
