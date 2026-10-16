# domain-memory 觸及點與換版步驟

> 讀者：DLC 維護者。時機：domain-memory 換版前。可見性：內部，不發學員。
> 更新日期：2026-10-17。目前固定 0.33.0（SkillHub `b00228f49`），Registry 已是 OKF（Open Knowledge Format）版面；升級紀錄見 `decisions-and-open-issues.md`〈domain-memory 升級 0.33.0（OKF）〉。

## 0. 現況

| 項目 | 0.27.2（舊） | 0.33.0（現行） |
|---|---|---|
| Registry 版面 | `domain-memory/registry/<資產>.json`＋`manifest.json` | `registry/index.md`＋`registry/<資產>/index.md`＋每筆一個 `registry/<資產>/<id>.md`（YAML 開頭區塊＋內文＋`# Relations` 連結） |
| 狀態 | `status`（decisions 用 `review_status`）：candidate／reviewed | 檔案裡 `status`：draft／stable／deprecated；**指令與 `export` 輸出仍是 candidate／reviewed** |
| 審查紀錄 | 每筆 `review` 區塊（提案、核准） | 每筆 `verified`（`by: "human:<reviewer>"`、`at`）；審查它的提案記在 audit log（`apply-approved-updates` 或 `migrate-registry` 的 event） |
| 證據 | `evidence[]`：`path`、`lines`、`excerpt_sha256`、`content_sha256`、`source_kind` | 檔案裡 `sources[]`：`resource: "path#L起-迄"`＋`excerpt_sha256`；`source_kind` 驗證時才由 source map 推出 |
| 讀取 | 開檔 | `export`（`--commit` 可讀某個 commit 當時的 Registry，兩種版面都行） |
| 新增 Registry | `init-domain-memory` 寫 JSON | 寫 OKF |
| 舊 Registry | — | 沒有 `index.md` 時照舊讀 JSON；`validate` 拒絕仍有 `review` 區塊的紀錄；`migrate-registry` 一次轉換，audit 加 1 筆 event（`migrate-registry`、`layout: okf`、`reviewed_by`） |
| 不動的檔案 | policy、source map、`audit/`、`changes/` 在 `domain-memory/` 根 | 同左（換行也保留原樣） |
| 換行 | JSON 由寫入時的平台決定（參考 Registry 多數 CRLF） | 概念檔一律 LF；`events.jsonl` 舊行 CRLF、新行 LF，`verify-audit` 照常通過 |

DLC 工具讀 Registry 一律經 `dmlib.registry_documents()`（＝`export`），寫入只經 Plugin 指令或 Plugin 的 Change Package 範本（`changes/<CP>/*.json`）。學員路徑上原本寫死 JSON 版面的 D2 檢查點 3 與簽章流程清單已改用 `dm export`。

標記：**不受影響**＝換版後照常；**已處理**＝0.33.0 升級時改過；**第二階段**＝留給內容重新設計（清單在升級紀錄）。

## 1. Plugin 指令與旗標

學員都經 `dm.ps1`／`dm.sh`（→ `dmlib.py`）呼叫；`dmlib.expand()` 自動補 `--registry-root domain-memory`、`--repo-root .`，`verify-sources` 另補 `--source-map`、`--policy`，`init-signing-key` 補 `--key-file`。三組指令集合（`REGISTRY_REQUIRED`／`REGISTRY_OPTIONAL`／`REPO_ROOT`）與 0.33.0 的 `cli_parser.py` 完全一致，相容性檢查會逐一比對。

| 指令 | 用到的旗標 | 出處 | 標記 |
|---|---|---|---|
| `readiness`、`quality-gates` | — | Runbook 01；`CHECKPOINTS.md`；主持人指南 | 不受影響 |
| `init-domain-memory` | `--output --source --exclude --storage-mode tracked --data-classification internal --review-mode local-draft-only --source-authority` | Runbook 10；`make_recovery.py` d1；`test_tools.py`；參考 README | 不受影響（產出 OKF） |
| `discover-sources`、`confirm-sources` | `--confirmed-by` | Runbook 10；`make_recovery.py`；`test_tools.py` | 不受影響 |
| `verify-sources`、`verify-evidence`、`coverage` | （dmlib 補 `--source-map`、`--policy`） | Runbook 10／19／29–59／60；RECOVERY.md；參考 README | 不受影響 |
| `cite` | `--path --start --end` | `make_record.py`、`fill_package.py` | 不受影響（仍回 `source_kind`，寫入時 Plugin 去掉衍生欄位） |
| `upsert-candidate` | `--asset --record-file`（多個） | `make_record.py --upsert` | 不受影響 |
| `resolve-terms`、`get-context`、`get-record`、`analyze-boundary` | `--query`；`--id`；`--asset --id`；`--source-context --target-context` | Runbook 10／30／40／50／60；`fill_package.py`（`get-record`）；tools README | 不受影響（輸出帶 `verified`，沒有 `review`） |
| `counterfactual` | `--file --find --replace --test-command`（＋dmlib `--save`） | Runbook 20／30／40／50；`test_tools.py`；tools README | 不受影響 |
| `init-change-package`、`validate-change-package` | `--output`；`--package-root` | `fill_package.py` | 不受影響 |
| `submit-proposal`、`record-approval`、`verify-proposal`、`finalize-proposal`、`apply-approved-updates` | `--package-root`；`--role --reviewer --scope` | Runbook 20；`d2-signing-checklist.md`；`test_tools.py` | 不受影響（套用後寫 `verified`） |
| `init-signing-key`、`amend-policy`、`install-git-hitl-hook`、`governance-readiness`、`verify-git-governance`、`verify-audit`、`scan-secrets` | `--principal --key-file --sign-every-commit`；`--field --value --reason --verifier`；`--commit` | Runbook 20／29–59／60／70；RECOVERY.md；`make_recovery.py`；參考 README；簡報 30-d2 | 不受影響 |
| `validate` | `--require-reviewed` | 幾乎每一頁；簡報 20／30／40 | 不受影響 |
| `export` | `--registry-root`（`--commit --repo-root` 可選） | Runbook 20-d2 檢查點 3；`d2-signing-checklist.md`；`dmlib.registry_documents()`；相容性檢查 | 已處理 |
| `migrate-registry` | `--registry-root` | 只在維護時（參考 Registry、參考解答） | 已處理 |
| `compare-registry` | `--gold-root --gold-commit --candidate-root`（＋dmlib `--save`） | Runbook 70 回顧檢查點 2（基準＝最後一個「套用」commit） | 已處理（第二階段） |
| `change-coupling` | `[--root --depth --since --min-*]` | 不在學員路徑；只在簡報備註與主持人指南當反例 | 已處理（第二階段） |

## 2. 直接讀寫的檔案路徑

| 路徑 | 誰、怎麼用 | 標記 |
|---|---|---|
| `domain-memory/registry/**` | 沒有任何 DLC 工具或學員提示詞直接開；讀取一律 `export` | 已處理 |
| `domain-memory/domain-memory-policy.json` | Recovery 步驟 2 讀 `review_governance.authorized_signers`（`make_recovery.py`、RECOVERY.md、Runbook 29／39／49／59 兩個分頁）；D2 檢查點 2 的 ③ 讀 `review_mode` 等；dmlib 補 `--policy` | 不受影響 |
| `domain-memory/source-map.json` | dmlib 補 `--source-map` | 不受影響 |
| `domain-memory/audit/events.jsonl`、`audit/manifest.json` | 只經 `verify-audit`；參考 README 與 SOLUTION-NOTES 記 events 數與 head | 已處理（數字已更新） |
| `domain-memory/changes/<CP>/*.json` | `fill_package.py`、`write_scm_attestation.py` 直接讀寫（Plugin 的設計：`init-change-package` 產生範本，由人或 Agent 填寫） | 不受影響 |
| `records/<資產>-<id>.json`、`cf-*.json`、`cp-d2.json` | DLC 工具自己的輸入輸出 | 不受影響 |
| `.git/hooks/pre-push` | D2 檢查點 2 的 ③；Recovery | 不受影響 |
| 「讀 domain-memory/ 裡的詞彙紀錄」 | 已改為 `export --save ../../tmp/registry.json` 後只列 Context 與詞彙名稱（Runbook 10 檢查點 5 失敗時、30／40／50 第 2 步與失敗提示）；學員只「打開來讀」紀錄檔（D1 檢查點 4、D2 檢查點 4） | 已處理（第二階段） |

## 3. 學員看到或 ③ 檢查的 Plugin 輸出

全部列在 `check_dlc_plugin_compat.py` 的 `QUOTED`；檢查時在本次執行的輸出或 Plugin 原始碼裡找得到才算 PASS。0.33.0 全部找得到。

| 字串 | 出處 | 標記 |
|---|---|---|
| `Registry is valid.` | Runbook 01／10／19／20／29–59／60；RECOVERY.md；簡報 30-d2；tools README | 不受影響 |
| `Change package is valid.`、`Proposal submitted for human review.`、`Proposal test evidence verified.` | Runbook 20 | 不受影響 |
| `Git governance is valid.`（D2 Recovery 推送時「八行」） | Runbook 20／29–59；RECOVERY.md；簡報 30-d2；參考 README | 已處理（行數） |
| `That is reach, not an error.` | Runbook 30／40／50／60；簡報 70-d4 | 不受影響 |
| `the tests do not pass before anything is broken`、`Git commit signature is invalid`、`not reviewed` | tools README；RECOVERY.md；簡報 30-d2 | 不受影響 |
| `{"status": "ready", "blocks": []}`、`"status": "valid"` | Runbook 20／29–59／60；RECOVERY.md | 不受影響 |
| `verdict`／`killed`／`survived`、`failing_evidence`、`restoration_result.restored` | Runbook 20／30／40／50；詞彙表；worksheets | 不受影響 |
| `match_kind`、`mentioned`、`authoritative`、`no_registered_collaboration` | Runbook 30／40／50；tools README；主持人指南 | 不受影響 |
| `current`／`shifted`／`stale`、`discovered_but_gone`、`developer-confirmed`、`content_changed`、`changed_sources`、`confirmed_absences`、`source_kind`／`unclassified` | Runbook 10／19／60；詞彙表；RECOVERY.md；主持人指南；`make_record.py` | 不受影響 |
| `authorized_signers`、`review_governance`、`review_mode`、`scm-verified`、`git-signed-commit`、`git-push`、`fingerprint` | Runbook 20／29–59；RECOVERY.md | 不受影響（policy 檔） |
| `"state": "brownfield"`、`"tool": "pytest"`、`"confidence": "high"` | Runbook 01（`readiness`／`quality-gates` 的 ③） | 不受影響 |
| `not_applicable`、`applied` | 參考 README | 不受影響 |

## 4. 隨包附帶的檔案

| 內容 | 位置 | 現況 |
|---|---|---|
| 參考 Registry 的 Git 歷史 | `evaluation/reference-registry/smart-ticket-dlc-reference.bundle`，tag `dlc-d2-reviewed` → `de53623` | 6 個 JSON 版面的 Maintainer 簽章 Registry commit＋1 個 Maintainer-2 簽章的 OKF 遷移 commit；證據雜湊依起始 Repo 原始位元組（22 個 CRLF 檔＋`.gitignore` 混合） |
| 參考 Registry 快照 | `evaluation/reference-registry/domain-memory/` | 以 `git archive dlc-d2-reviewed domain-memory` 匯出 |
| D1 輸入、套件描述、反事實結果 | `reference-registry/inputs/`、`counterfactual/` | DLC 自己的格式，不受影響 |
| Recovery d1 | `facilitator/recovery/d1/`（`make_recovery.py d1` 以 Plugin 現場產生，未簽章、未 commit Registry） | OKF |
| Recovery d2～d3c | `facilitator/recovery/d2…d3c/`（從 bundle tag 重產，`repo.bundle` 帶簽章歷史） | OKF；Registry commit 7 個 |
| 參考解答 d3a～d3c 的 `domain-memory/` | `evaluation/reference-solutions/*/domain-memory/`（含 D3 候選；不是 Git repo） | OKF（各跑過一次 `migrate-registry`） |
| Plugin ZIP 與逐檔 SHA256 | `participant/vendor/domain-memory-0.33.0.zip(.SHA256SUMS)` | 79 個 Plugin 檔案，`SHA OK 80 files` |
| 打包清單 | `scripts/package-manifest-dlc.json` | 由 `release_materials.py` 自動 `--pin` |
| 驗證證據 | `evaluation/dlc-validation-evidence.json` 的 `plugin_0_33_0_remeasure` | 已記 |

版本字串（換版時以舊版本號全文搜尋）：`07-dlc-ddd/README.md`、`participant/tools/{dmlib.py,doctor.py,README.md}`、`facilitator/facilitator-guide.md`、`evaluation/{observation-guide.md,dlc-validation-evidence.json,reference-registry/README.md}`、`materials-dlc/README.md`、Runbook `01-environment.md`、開場投影片 `10-opening.html`、`docs/instructions/11_DDD_DLC產製指令書.md`、`scripts/{build_delivery_dlc.py,test_build_delivery_dlc.py,check_dlc_plugin_compat.py,package-manifest-dlc.json}`。`doctor.py` 的 `PLUGIN_VERSION` 會把其他版本判為 `[!!]`。主持指南常見問題第 19 條的「Plugin 0.27.2 起」是行為的起始版本，不要改。

## 5. 相容性檢查

`scripts/check_dlc_plugin_compat.py [--source <匯出的 Plugin 資料夾或 ZIP>]`：在暫存沙箱跑（一）`cli_parser` 與 dmlib 指令集合、學員用到的指令與旗標；（二）tools 自檢；（三）D1 重播（`make_recovery.build_d1`）與 D1／D3 的查詢指令；（四）參考 Registry（從 bundle 還原）唯讀驗證、兩個 attestation commit、兩個 Change Package、export 的 OKF 紀錄形狀（每筆 reviewed 都有 `verified`、沒有 `review`）、經 pre-push hook push 既有簽章歷史（預期 `REGISTRY_COMMITS` = 7 行）；（五）第 3 節的字串。不改 Repo、不用私鑰，約 2 分鐘。

| 版本 | 結果（Windows） |
|---|---|
| 0.27.2（2026-10-16，JSON bundle） | 29 PASS |
| 0.28.0（`5f6e046f6`，2026-10-16） | 28 PASS、1 CHANGED（dmlib 未列 `export`） |
| 0.33.0（`b00228f49` 匯出，遷移前，2026-10-17） | 26 PASS、3 CHANGED：dmlib 少 `export`、`compare-registry`、`change-coupling`；參考 Registry 仍有 `review` 區塊，`validate --require-reviewed` 失敗 |
| 0.33.0（封裝 ZIP，遷移後，2026-10-17） | 29 PASS、0 CHANGED |

## 6. 下次換版的步驟

1. **評估**：讀 CHANGELOG；`git -C <SkillHub> archive <commit> .claude/skills/domain-memory` 匯出到暫存資料夾（不要用 SkillHub 工作區）；跑相容性檢查，CHANGED 清單就是待辦。
2. **工具**：dmlib 三組指令集合依檢查結果更新；`doctor.PLUGIN_VERSION`；第 4 節的版本字串與檔案數；以 `vendor_dlc_plugin.py --source` 封裝新 ZIP、刪舊 ZIP。
3. **參考 Registry（只有資料格式改變時）**：在暫存區 clone bundle、checkout `dlc-d2-reviewed`（`core.autocrlf=false`）、設定 `gpg.format ssh`、`gpg.ssh.allowedSignersFile`（`keys/maintainer.allowed_signers`）與 `user.signingkey`（Maintainer-2 私鑰原處：`%USERPROFILE%\.dlc-keys\maintainer-2\id_ed25519`，指紋 `SHA256:GtKS8fEN…MueCs`）→ Plugin 指令 → `validate --require-reviewed`、`verify-evidence`、`verify-sources`、`verify-audit` → 簽章 commit → `verify-git-governance --commit HEAD` → push 到全新的 bare remote，hook 行數＝Registry commit 數 → tag 改指向新 commit → 重做 bundle → `git archive` 重新匯出快照 → 相容性檢查的 `REGISTRY_COMMITS`、`make_recovery.py` 與主持指南的 commit 數、參考 README 的歷史與預期結果。
   - 私鑰**不得**複製進 Repo、OneDrive、沙箱或對話，也不要重產 Maintainer 金鑰；手邊沒有私鑰時照參考 README「遺失時」以 `amend-policy` 授權新金鑰（再多一個 commit），不要用 `--no-verify`。
   - 證據雜湊取決於來源檔的原始位元組。保持 `* -text`、`core.autocrlf=false`，不要用 `sed -i` 或編輯器另存；遷移後確認 `git diff HEAD~1 -- . ':!domain-memory'` 是空的、162 個引用仍是 current。
4. **Recovery**：重跑 `make_recovery.py d1 d2 d3a d3b d3c`；還原後量 current／shifted／stale（d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32）。
5. **參考解答**：資料格式改變時三個 `domain-memory/` 各跑一次 Plugin 的遷移指令（不用金鑰），核對 SOLUTION-NOTES 的數字。
6. **學員內容**：只改會壞的步驟；新功能的教法另開設計。
7. **驗證**：相容性檢查全部 PASS → `release_materials.py` 到 `RELEASE PIPELINE PASS` → Windows 與 macOS 各演練一次：D1 檢查點 2–3、D2 檢查點 1–6（含 push）、D2 Recovery、D3a 檢查點 5、D4 檢查點 1；並把結果依「Plugin 版本政策」寫進 `decisions-and-open-issues.md`。

## 7. 主要風險

| 風險 | 影響 | 對策 |
|---|---|---|
| Agent 直接讀概念檔 | 看到 `status: stable`／`draft`，對不上提示詞的 reviewed／candidate | 提示詞用 `export`、`get-context`、`resolve-terms`；第二階段改寫「讀 domain-memory/ 裡的詞彙紀錄」 |
| `export` 輸出很長（D1 重播的 57 筆約 78 KB） | Agent 漏列候選，`validate --require-reviewed` 回「not reviewed」 | D2 第一步要求依類別回報筆數；第二階段考慮存檔再摘要 |
| 簽章歷史新增 commit 需要 Maintainer 私鑰 | 沒有私鑰就無法讓 hook 接受新的 Registry commit | 照 README 保管；遺失時授權新金鑰 |
| 換行被轉換 | 162 個證據引用全部 stale，簽章 commit 內容不符 | `* -text`、只用位元組層級的工具搬動 |
| 學員手動編輯 `.md` | 超出 frontmatter 子集（單引號、`[a, b]`）會被拒並附行號；編輯器改換行的影響未實測 | 第二階段補進主持人常見問題 |
