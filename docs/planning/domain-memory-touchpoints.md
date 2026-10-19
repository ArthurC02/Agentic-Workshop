# domain-memory 觸及點與換版步驟

> 讀者：DLC 維護者。時機：domain-memory 換版前。可見性：內部，不發學員。
> 更新日期：2026-10-19。目前固定 1.2.18（SkillHub `f76ca1e54`），Registry 是 OKF（Open Knowledge Format）版面（0.33.0 起，之後的版本都沒有再改）；升級紀錄見 `decisions-and-open-issues.md`〈domain-memory 升級 0.33.0（OKF）〉〈domain-memory 升級 0.52.0〉〈domain-memory 升級 0.61.0〉〈domain-memory 升級 1.1.0〉〈domain-memory 1.1.1（patch）〉〈domain-memory 升級 1.2.2〉〈domain-memory 1.2.4（patch）〉〈domain-memory 1.2.8（patch）〉〈domain-memory 1.2.18（patch）〉。

## 0. 現況

| 項目 | 0.27.2（舊） | 0.33.0 起（現行 1.2.18） |
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

標記：**不受影響**＝換版後照常；**已處理**＝0.33.0 升級時改過；**0.52 已處理**＝0.52.0 升級時改過；**0.61 已處理**＝0.61.0 升級時改過；**1.1 已處理**＝1.1.0 升級時改過；**1.2 已處理**＝1.2.2 升級時改過（1.2.4 patch 只改主持指南第 19 條；1.2.8 patch 不用改學員內容；1.2.18 patch 只改主持指南第 19、20 條與 dmlib 的逾時預設）；**第二階段**＝留給內容重新設計（清單在升級紀錄）。

## 1. Plugin 指令與旗標

學員都經 `dm.ps1`／`dm.sh`（→ `dmlib.py`）呼叫；`dmlib.expand()` 自動補 `--registry-root domain-memory`、`--repo-root .`，`verify-sources` 另補 `--source-map`、`--policy`，`init-signing-key` 補 `--key-file`。三組指令集合（`REGISTRY_REQUIRED`／`REGISTRY_OPTIONAL`／`REPO_ROOT`）與 1.2.18 的 `cli_parser.py` 完全一致（1.2.0 加 `rebase-proposal`，63 個指令，1.2.3–1.2.18 沒有增減；1.2.10 起 dmlib 在 `DOMAIN_MEMORY_GIT_TIMEOUT` 沒設時給 60 秒，使用者設的值優先；1.0 起 `ERROR:` 拒絕訊息與 NOTE 都印在 stderr，`--save` 只存 stdout），相容性檢查會逐一比對（0.52.0 加了 `harvest-candidates`；`change-coupling` 改為可選 `--registry-root`，Registry 存在時 dmlib 會補，輸出多 `explained_by`；0.61.0 的 `redraft-proposal`、`supersede-proposal` 接受可選 `--registry-root` 與 `--repo-root`，`coverage`、`promote-candidate` 接受 `--repo-root`）。

| 指令 | 用到的旗標 | 出處 | 標記 |
|---|---|---|---|
| `readiness`、`quality-gates` | — | Runbook 01；`CHECKPOINTS.md`；主持人指南 | 不受影響 |
| `init-domain-memory` | `--output --source --exclude --storage-mode tracked --data-classification internal --review-mode local-draft-only --source-authority` | Runbook 10；`make_recovery.py` d1；`test_tools.py`；參考 README | 不受影響（產出 OKF；1.2.7 起政策被拒時會刪掉剛建的輸出，修正參數後直接重跑，不會再回 `output directory is not empty`） |
| `discover-sources`、`confirm-sources` | `--confirmed-by` | Runbook 10；`make_recovery.py`；`test_tools.py` | 不受影響 |
| `verify-sources`、`verify-evidence`、`coverage` | （dmlib 補 `--source-map`、`--policy`；`coverage` 另補 `--repo-root`） | Runbook 10／19／29–59／60；RECOVERY.md；參考 README | 1.1 已處理：`verify-sources` 多 `discovered_but_unlisted` 與 NOTE「discovery drifted … run refresh-sources」（1.1.1 起寫成「the selection is stale, so run refresh-sources, then confirm-sources」）；D3 之後仍是 `stale`（exit 1），D4 檢查點 1 只讀不改，提示詞已說不要試著修好 0.61 已處理：0.53 起 `coverage` 多 `rules_by_context`，0.54 起每個 Context 的已審查規則依證明分 `proven`／`unproven`／`unknown`，0.58 起多 `rule_totals`（D4 檢查點 1 新教「模型在哪些 Context 說了算」）；沒有 `changes/` 時 stderr 印 NOTE 請加 `--changes-root`（D1 檢查點 5 提示詞註明正常） |
| `probe` | （dmlib 補 `--registry-root`、`--repo-root`） | 不在學員路徑（只列在 dmlib 的指令集合） | 1.2.10 起過期時印 `Domain Memory at <root>: stale. <n> selected sources gained, lost or renamed files (<names>); run refresh-sources, then have a developer run confirm-sources.`；current 時若有只改內容的來源，加 `; <n> selected sources changed inside (<names>); verify-evidence checks the citations`；1.2.11 起清單漂移也算 current（exit 0），句尾加 `; discovery drifted: … ; run refresh-listing --registry-root <路徑> --repo-root <路徑> (no confirmation needed)`（1.2.13 起印實際路徑）；1.2.14 起沒有 Domain Memory 時印 `Domain Memory at <root>: none; check --registry-root (a Registry holds registry/ and source-map.json); initialize one only if this repository has none yet`，找得到別處的 Registry 時加 `; did you mean <path>?`（1.2.17 起問 git 找整個 Repo 的 source-map.json，1.2.18 起 <root> 是相對 Repo 根目錄的正斜線路徑）；exit 0 current、1 其他狀態、2 absent。這句是命令句：放上學員路徑時要和 D4 檢查點 1 一樣加「不要試著修好」 |
| `cite` | `--path --start --end` | `make_record.py`、`fill_package.py` | 不受影響（仍回 `source_kind`，寫入時 Plugin 去掉衍生欄位） |
| `upsert-candidate` | `--asset --record-file`（多個） | `make_record.py --upsert` | 不受影響 |
| `resolve-terms`、`get-context`、`get-record`、`analyze-boundary` | `--query`；`--id`；`--asset --id`（`--changes-root` 可選）；`--source-context --target-context` | Runbook 10／20／30／40／50／60；`fill_package.py`（`get-record`）；tools README | 1.1 已處理：`analyze-boundary` 一次回報 `source_depends_on_target` 與 `target_depends_on_source`，`status` 是 `known`／`policy_only`／`no_registered_collaboration`，不用對調再查（D1 檢查點 6、D3 工作規則第 10 條） 0.52 已處理：`resolve-terms` 的 mention 不再有 `authoritative`（0.52），改為每筆一次並列 `fields`、`summary`；`get-record --changes-root` 多 `proven_by`（D2 檢查點 6、D4 檢查點 1） 0.61：0.53 起沒給 `--changes-root` 也讀 `domain-memory/changes`，候選規則多一行 NOTE（沒有測試證明它，正常）；`proven_by` 每筆多 `working_directory`；0.54 起重新引用、沒有測試的提案不會讓規則失去證明 |
| `counterfactual` | `--file --find --replace --test-command --expect`（＋dmlib `--save`） | Runbook 20／30／40／50；`test_tools.py`；tools README；參考解答 `run_counterfactuals.py` | 1.1 已處理：拒絕執行（找不到字串、改壞前測試就沒過、無法啟動）也輸出 JSON，`verdict` 是 `error`、exit 3、原因在 `reason`（D3 工作規則第 11 條：error 的 cf-*.json 刪掉重跑） 0.52 已處理：0.34 起不經 shell、以 shlex 拆字，Windows 寫 `./.venv/Scripts/python.exe`（反斜線被吃掉，沒有 `./` 時 CreateProcess 找不到）；`inconclusive`（逾時、改壞後無法載入、失敗不符 `--expect`）；0.45 起 `failure_evidence`（原 `failing_evidence`）；D2 用 `--expect` 0.61 已處理：0.54 起多 `failing_tests`（抓到它的測試；D3 檢查點 4 回報、D3a 檢查點 5 取「守住它的測試」）；0.58 起聚焦測試 survived 時 reason 建議對整個測試套件重跑（D3 工作規則第 11 條：同一組字串、TEST 換成 tests，存成下一個編號；實測 D3b 的等價 mutant 在整套仍 survived）；0.59 起 `--find` 重複時列出行號 |
| `init-change-package`、`validate-change-package` | `--output`；`--package-root` | `fill_package.py` | 不受影響 |
| `submit-proposal`、`record-approval`、`verify-proposal`、`ship-package` | `--package-root`；`--role --reviewer --scope`；`ship-package --commit HEAD` | Runbook 20；`d2-signing-checklist.md`、`d2-role-cards.md`；`test_tools.py` | 1.2 已處理：1.2.1／1.2.2 起 `verify-proposal` 對 verified、approved、applied 的提案印 `already <status> at revision <n>; nothing was written`、exit 0（原本 `ERROR: only a submitted proposal may be verified`、exit 1），D2 檢查點 4 的 ③ 改等這一行，`test_tools.py` 驗證；1.2.0 提交時 base 多 `committed_digest`（HEAD 有 Registry 時才有；自己做的 D2 在檢查點 3 提交時 Registry 還沒 commit，所以沒有），過期訊息改為「proposal base revision is stale; rebase-proposal, then obtain fresh approval: …」，套用時的競態改為「run ship-package again」；學員路徑碰不到過期，只寫進主持指南常見問題第 19 條 1.1 已處理：1.0 刪除 `attest-signed-commit`、`finalize-proposal`、`apply-approved-updates`（exit 2），改用 `ship-package --commit <sha>` 一步做完（確認簽章 commit 有授權且帶著提案 → 寫 attestation → 定案 → 套用；回 `completed`、`status` `applied`、`errors`）；DLC 刪除 `write_scm_attestation.py`，D2 檢查點 5 只驗證簽章 commit，檢查點 6 由提案者跑 `ship-package` 0.52 已處理：0.51 起 `verify-proposal` 要求測試紀錄的 `evidence` 與 obligation 的 `check` 相同，`fill_package.py` 的 `check` 改為完整測試指令並以 shlex、不經 shell 執行 0.61：0.59 起 `submit-proposal` 拒絕引用已確認來源以外路徑的升級紀錄（原本到 `apply-approved-updates` 才拒絕）；自己做的 D1 與 D1 Recovery 的證據都在已確認來源內，沒有碰到；`validate`、`verify-git-governance` 對已核准未套用的提案印 NOTE，D2 檢查點 5 時提案是 `verified`、不會出現 |
| `install-pre-commit-hook` | （dmlib 補 `--registry-root`、`--repo-root`） | Runbook 60（檢查點 3）；簡報 70-d4；主持指南 | 1.1 已處理：D4 檢查點 3 新概念，夥伴裝上後以 `git mv` 示範被擋下（每筆一行「… is not in this commit」，最後一行「… is renamed to … run relocate-evidence --from … --to …」），再搬回原位；1.1.1 起拒絕訊息結尾改為資訊句「details: verify-evidence … --staged … prints the full report, as this hook does when DOMAIN_MEMORY_HOOK_VERBOSE is set」，不再叫人帶變數重新 commit |
| `init-signing-key`、`amend-policy`、`install-git-hitl-hook`、`governance-readiness`、`verify-git-governance`、`verify-audit`、`scan-secrets` | `--principal --key-file --sign-every-commit`；`--field --value --reason --verifier`；`--commit` | Runbook 20／29–59／60／70；RECOVERY.md；`make_recovery.py`；參考 README；簡報 30-d2 | 不受影響 0.61 已處理：0.58 起 `verify-git-governance` 的訊息帶 commit 數（`Git governance is valid for 1 commit.`），pre-push hook 一次檢查整個 push、只印一行（自己做的 D2：`for 2 commits.`；D2 Recovery：`for 8 commits.`） |
| `validate` | `--require-reviewed` | 幾乎每一頁；簡報 20／30／40 | 不受影響 |
| `export` | `--registry-root`（`--commit --repo-root` 可選） | Runbook 20-d2 檢查點 3；`d2-signing-checklist.md`；`dmlib.registry_documents()`；相容性檢查 | 已處理 |
| `migrate-registry` | `--registry-root` | 只在維護時（參考 Registry、參考解答） | 已處理 |
| `compare-registry` | `--gold-root --gold-commit --candidate-root`（＋dmlib `--save`） | Runbook 70 回顧檢查點 2（基準＝最後一個「套用」commit） | 0.52 已處理：回報 `overall_independent`、`copied_matches`、配對的 `copied_evidence`；D3c Recovery 對 `fc9efe2` 實測 57 個配對有 52 個照抄，`overall_independent` 只剩 5 個 Context 配對 |
| `change-coupling` | `[--root --depth --since --min-*]`（`--registry-root` 由 dmlib 補） | 不在學員路徑；只在簡報備註與主持人指南當反例 | 0.52 已處理：`explained_by` 只在模組對得上 Context 時有意義；這個分層 Repo 在 D3c Recovery 仍沒有可用配對 |
| `harvest-candidates`、`list-proposals` | — | 不在學員路徑 | 0.52 新增，dmlib 集合已列入 `harvest-candidates` |
| `rebase-proposal`（1.2.0） | `--package-root`（dmlib 補 `--registry-root`、`--repo-root`） | 主持指南常見問題第 19 條（D2 檢查點 6 `ship-package` 回報過期時） | 1.2 已處理：提案者的 Agent 執行，只改審查包：`proposal_revision` 加 1、`status` 回 `submitted`、`verified_at` 與 `scm_attestation` 清空，印 `package`、`status`、`proposal_revision`、`base_registry_revision`、`approvals_retired`、`attestation_removed`、`next`；之後要重新核准、新的簽章 commit。1.2.3 起「是否過期」用和 verify／finalize／apply 相同的過期檢查（1.2.2 在只多一個 commit、Registry 沒變時也會 rebase 並作廢核准），也收 approved（回 submitted、清 `finalized_at`）；1.2.4 起 base 沒過期時 exit 0、只印 `note` `the proposal base is current; nothing was written` 與該狀態的 `next`（原本 `ERROR: … nothing to rebase`、exit 1）。不在 Runbook |
| `harvest`／`discard-harvest`（1.0／1.1，取代 `fill-harvest-package`；1.2.0 起 `discard-harvest` 也收 verified 的套件）、`brief` 的 `registry_changes`、`mcp-serve`、`refresh-listing`、`list-proposals`、`promote-candidate --amend`（0.56）／`--cite`、`--cite-function`（0.57）、`supersede-proposal`／`redraft-proposal` 的旗標（0.60–0.61） | — | 不在學員路徑；`--amend` 只在 D4 檢查點 2 的新概念小卡與主持指南當「同一條規則重新證明」的做法 | DLC 的 `fill_package.py` 照用，不換成 `harvest`（它要求每條規則都有 killed 的反事實，D2 只做一條）；1.1.0 的改動全在 `harvest`（可續跑、`discard-harvest` 復原），不在學員路徑 |

## 2. 直接讀寫的檔案路徑

| 路徑 | 誰、怎麼用 | 標記 |
|---|---|---|
| `domain-memory/registry/**` | 沒有任何 DLC 工具或學員提示詞直接開；讀取一律 `export` | 已處理 |
| `domain-memory/domain-memory-policy.json` | Recovery 步驟 2 讀 `review_governance.authorized_signers`（`make_recovery.py`、RECOVERY.md、Runbook 29／39／49／59 兩個分頁）；D2 檢查點 2 的 ③ 讀 `review_mode` 等；dmlib 補 `--policy` | 不受影響 |
| `domain-memory/source-map.json` | dmlib 補 `--source-map` | 不受影響 |
| `domain-memory/audit/events.jsonl`、`audit/manifest.json` | 只經 `verify-audit`；參考 README 與 SOLUTION-NOTES 記 events 數與 head | 已處理（數字已更新） |
| `domain-memory/changes/<CP>/*.json` | `fill_package.py` 直接讀寫（Plugin 的設計：`init-change-package` 產生範本，由人或 Agent 填寫） | 不受影響 |
| `records/<資產>-<id>.json`、`cf-*.json`、`cp-d2.json` | DLC 工具自己的輸入輸出 | 不受影響 |
| `.git/hooks/pre-push` | D2 檢查點 2 的 ③；Recovery | 不受影響 |
| 「讀 domain-memory/ 裡的詞彙紀錄」 | 已改為 `export --save ../../tmp/registry.json` 後只列 Context 與詞彙名稱（Runbook 10 檢查點 5 失敗時、30／40／50 第 2 步與失敗提示）；學員只「打開來讀」紀錄檔（D1 檢查點 4、D2 檢查點 4） | 已處理（第二階段） |

## 3. 學員看到或 ③ 檢查的 Plugin 輸出

全部列在 `check_dlc_plugin_compat.py` 的 `QUOTED`；檢查時在本次執行的輸出或 Plugin 原始碼裡找得到才算 PASS。1.2.18 全部找得到（79 個：1.2.10 加過期基準的兩種原因 `does not hold the Registry at`、`does not reproduce the recorded base digest` 與逾時的三段 `nothing was written, so it is safe to run again`、`DOMAIN_MEMORY_GIT_TIMEOUT`、`to a larger number of seconds to wait longer`、`must be a positive number of seconds`（原始碼用變數組句，所以變數名與句子分開比對），都只在主持指南；1.2.8 是 73 個，1.2.5–1.2.8 沒有增減；1.2.4 加 `the proposal base is stale; rebase-proposal`、`the proposal base is current; nothing was written`；1.2.2 是 71 個，1.2 加 `nothing was written`、`proposal base revision is stale; rebase-proposal`、`approvals_retired`；1.1.0、1.1.1 是 68 個；1.0 起新增 `ship-package` 的 `completed`／`applied`、`analyze-boundary` 兩個方向的鍵、`brief` 的 Attention 與 lies outside every Context、規則 `aggregate` 的拒絕訊息、pre-commit hook 的安裝與改名提示）。

| 字串 | 出處 | 標記 |
|---|---|---|
| `Registry is valid.` | Runbook 01／10／19／20／29–59／60；RECOVERY.md；簡報 30-d2；tools README | 不受影響 |
| `Change package is valid.`、`Proposal submitted for human review.`、`Proposal test evidence verified.` | Runbook 20 | 不受影響 |
| `already verified at revision 1; nothing was written`（重跑 `verify-proposal`）、`proposal base revision is stale; rebase-proposal`、`approvals_retired`、`the proposal base is stale; rebase-proposal`（過期時 `ship-package` 的 `next`，1.2.3）、`the proposal base is current; nothing was written`（1.2.4） | Runbook 20 檢查點 4 的 ③；主持指南常見問題第 19 條 | 1.2 已處理（`QUOTED` 收 `nothing was written`；完整的一行由 `test_tools.py` 驗證） |
| `does not hold the Registry at`、`does not reproduce the recorded base digest`（過期基準的原因，1.2.9）；`nothing was written, so it is safe to run again`、`set DOMAIN_MEMORY_GIT_TIMEOUT to a larger number of seconds to wait longer`、`must be a positive number of seconds`（git 逾時，1.2.10） | 主持指南常見問題第 19、20 條 | 1.2.18 已處理 |
| `Git governance is valid for 1 commit.`（push 時一行 `… for N commits.`：D2 是 2，D2 Recovery 是 8） | Runbook 20／29–59；RECOVERY.md；簡報 30-d2；參考 README；主持指南 | 0.61 已處理（0.58 起訊息帶 commit 數、一次 push 一行） |
| `That is reach, not an error.` | Runbook 30／40／50／60；簡報 70-d4 | 不受影響 |
| `the tests do not pass before anything is broken`、`Git commit signature is invalid`、`not reviewed` | tools README；RECOVERY.md；簡報 30-d2 | 不受影響 |
| `{"status": "ready", "blocks": []}`、`"status": "valid"` | Runbook 20／29–59／60；RECOVERY.md | 不受影響 |
| `verdict`／`killed`／`survived`／`inconclusive`、`failure_evidence`、`restoration_result.restored`、`matching --expect`（`reason`） | Runbook 20／30／40／50；詞彙表；worksheets | 0.52 已處理（`failing_evidence` 改名；`inconclusive` 與 `--expect`） |
| `match_kind`、`mentioned`、`no_registered_collaboration` | Runbook 30／40／50；tools README；主持人指南 | 0.52 已處理（`authoritative` 已移除） |
| `proven_by`、`also_covers`、`copied_evidence`、`copied_matches`、`overall_independent` | Runbook 20／30／60／70；詞彙表；簡報備註；主持人指南 | 0.52 新教 |
| `failing_tests`、`rule_totals`、`rules_by_context`、`reviewed_rules`、`contexts_without_reviewed_rules`、`proven`／`unproven`／`unknown` | Runbook 30／40／50（檢查點 4、5）／60（檢查點 1）；詞彙表；簡報 70-d4 備註；主持人指南 | 0.61 新教 |
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
| Plugin ZIP 與逐檔 SHA256 | `participant/vendor/domain-memory-1.2.18.zip(.SHA256SUMS)` | 97 個 Plugin 檔案（1.0 起含 `scripts/domain_registry/commands/`、`mcp_server.py`；1.2.9 加 `git.py`、`search.py`，1.2.14 加 `locate.py`），`SHA OK 98 files` |
| 打包清單 | `scripts/package-manifest-dlc.json` | 由 `release_materials.py` 自動 `--pin` |
| 驗證證據 | `evaluation/dlc-validation-evidence.json` 的 `plugin_0_33_0_remeasure`、`plugin_0_52_0_remeasure`、`plugin_0_61_0_remeasure`、`plugin_1_1_0_remeasure`、`plugin_1_1_1_remeasure`、`plugin_1_2_2_remeasure`、`plugin_1_2_4_remeasure`、`plugin_1_2_8_remeasure` | 已記 |

版本字串（換版時以舊版本號全文搜尋）：`07-dlc-ddd/README.md`、`participant/tools/{dmlib.py,doctor.py,README.md}`、`facilitator/facilitator-guide.md`、`evaluation/{observation-guide.md,dlc-validation-evidence.json,reference-registry/README.md}`、`materials-dlc/README.md`、Runbook `01-environment.md`、開場投影片 `10-opening.html`、`docs/instructions/11_DDD_DLC產製指令書.md`、`scripts/{build_delivery_dlc.py,test_build_delivery_dlc.py,check_dlc_plugin_compat.py,package-manifest-dlc.json}`。`doctor.py` 的 `PLUGIN_VERSION` 會把其他版本判為 `[!!]`。主持指南常見問題第 16 條的「Plugin 0.27.2 起」是行為的起始版本，不要改。

## 5. 相容性檢查

`scripts/check_dlc_plugin_compat.py [--source <匯出的 Plugin 資料夾或 ZIP>]`：在暫存沙箱跑（一）`cli_parser` 與 dmlib 指令集合、學員用到的指令與旗標；（二）tools 自檢；（三）D1 重播（`make_recovery.build_d1`）與 D1／D3 的查詢指令；（四）參考 Registry（從 bundle 還原）唯讀驗證、兩個 attestation commit、兩個 Change Package、export 的 OKF 紀錄形狀（每筆 reviewed 都有 `verified`、沒有 `review`）、經 pre-push hook push 既有簽章歷史（預期 `REGISTRY_COMMITS` = 7 行）；（五）第 3 節的字串。不改 Repo、不用私鑰，約 2 分鐘。

| 版本 | 結果（Windows） |
|---|---|
| 0.27.2（2026-10-16，JSON bundle） | 29 PASS |
| 0.28.0（`5f6e046f6`，2026-10-16） | 28 PASS、1 CHANGED（dmlib 未列 `export`） |
| 0.33.0（`b00228f49` 匯出，遷移前，2026-10-17） | 26 PASS、3 CHANGED：dmlib 少 `export`、`compare-registry`、`change-coupling`；參考 Registry 仍有 `review` 區塊，`validate --require-reviewed` 失敗 |
| 0.33.0（封裝 ZIP，遷移後，2026-10-17） | 29 PASS、0 CHANGED |
| 0.52.0（`ed3edd700` 匯出，修改前，2026-10-17） | 24 PASS、5 CHANGED：dmlib 三組集合（`harvest-candidates`、`change-coupling`）；tools 自檢（`verify-proposal` 拒絕 evidence 不等於 check）；`QUOTED` 少 `failing_evidence`、`authoritative` |
| 0.52.0（封裝 ZIP，修改後，2026-10-17） | 29 PASS、0 CHANGED（`QUOTED` 49 個；學員旗標加 `--expect`、`--changes-root`、`export --commit`、`compare-registry`） |
| 0.61.0（`0a40b5b48` 匯出，修改前，2026-10-17） | 25 PASS、4 CHANGED：dmlib 兩組集合（`redraft-proposal`、`supersede-proposal`；`coverage`、`promote-candidate` 的 `--repo-root`）；經 hook push 只印一行 `Git governance is valid for 7 commits.`；`QUOTED` 少 `Git governance is valid.` |
| 0.61.0（封裝 ZIP，修改後，2026-10-17） | 29 PASS、0 CHANGED（`QUOTED` 57 個；push 檢查改成「恰好一行 `… for 7 commits.`」） |
| 1.0.0（`8ccb13ec0` 匯出，修改前，2026-10-18） | 24 PASS、5 CHANGED：dmlib 三組集合（加 `brief`、`dependents`、`harvest`、`install-pre-commit-hook`、`mcp-serve`、`refresh-listing`、`ship-package`，刪 `apply-approved-updates`、`attest-signed-commit`、`finalize-proposal`）；學員指令 `finalize-proposal`、`apply-approved-updates` 不存在；tools 自檢失敗 |
| 1.1.0（`8c7a8a47c` 封裝 ZIP，修改後，2026-10-19） | 30 PASS、0 CHANGED（dmlib 加 `discard-harvest`；`QUOTED` 68 個；新增 pre-commit hook 擋下改名的檢查） |
| 1.1.1（`accf3235f` 封裝 ZIP，2026-10-19） | 30 PASS、0 CHANGED（不用改 dmlib 與 `QUOTED`；只改 hook 拒絕訊息結尾與 NOTE 文字，學員頁沒有引用） |
| 1.2.2（`42819a57e` 匯出，修改前，2026-10-19） | 28 PASS、2 CHANGED：dmlib `REGISTRY_REQUIRED`、`REPO_ROOT` 少 `rebase-proposal` |
| 1.2.2（封裝 ZIP，修改後，2026-10-19） | 32 PASS、0 CHANGED（dmlib 加 `rebase-proposal`；`QUOTED` 71 個；參考 Registry 兩個 applied 套件加跑 `verify-proposal`，回 `already applied at revision 1; nothing was written`） |
| 1.2.4（`089b50321` 封裝 ZIP，2026-10-19） | 32 PASS、0 CHANGED（不用改 dmlib；`QUOTED` 71 → 73：過期時 `ship-package` 的 `next` 與 base 沒過期時 `rebase-proposal` 的 `note`） |
| 1.2.8（`7d2c73c6f` 匯出與封裝 ZIP，2026-10-19） | 32 PASS、0 CHANGED（改版本字串前就全部通過；不用改 dmlib 與 `QUOTED`，只改 `VENDOR_ZIP`） |
| 1.2.10（`45c66900a` 匯出，改任何檔案前，2026-10-19） | 32 PASS、0 CHANGED（INFO 仍只有 `list-proposals`） |
| 1.2.18（`f76ca1e54` 匯出與封裝 ZIP，2026-10-19） | 32 PASS、0 CHANGED（不用改 dmlib 的指令集合；`QUOTED` 73 → 79，加主持指南第 19、20 條引用的字串） |

## 6. 下次換版的步驟

1. **評估**：讀 CHANGELOG；`git -C <SkillHub> archive <commit> .claude/skills/domain-memory` 匯出到暫存資料夾（不要用 SkillHub 工作區）；跑相容性檢查，CHANGED 清單就是待辦。
2. **工具**：dmlib 三組指令集合依檢查結果更新；`doctor.PLUGIN_VERSION`；第 4 節的版本字串與檔案數；以 `vendor_dlc_plugin.py --source` 封裝新 ZIP、刪舊 ZIP。
3. **參考 Registry（只有資料格式改變時）**：在暫存區 clone bundle、checkout `dlc-d2-reviewed`（`core.autocrlf=false`）、設定 `gpg.format ssh`、`gpg.ssh.allowedSignersFile`（`keys/maintainer.allowed_signers`）與 `user.signingkey`（Maintainer-2 私鑰原處：`%USERPROFILE%\.dlc-keys\maintainer-2\id_ed25519`，指紋 `SHA256:GtKS8fEN…MueCs`）→ Plugin 指令 → `validate --require-reviewed`、`verify-evidence`、`verify-sources`、`verify-audit` → 簽章 commit → `verify-git-governance --commit HEAD` → push 到全新的 bare remote，hook 行數＝Registry commit 數 → tag 改指向新 commit → 重做 bundle → `git archive` 重新匯出快照 → 相容性檢查的 `REGISTRY_COMMITS`、`make_recovery.py` 與主持指南的 commit 數、參考 README 的歷史與預期結果。
   - 私鑰**不得**複製進 Repo、OneDrive、沙箱或對話，也不要重產 Maintainer 金鑰；手邊沒有私鑰時照參考 README「遺失時」以 `amend-policy` 授權新金鑰（再多一個 commit），不要用 `--no-verify`。
   - 證據雜湊取決於來源檔的原始位元組。保持 `* -text`、`core.autocrlf=false`，不要用 `sed -i` 或編輯器另存；遷移後確認 `git diff HEAD~1 -- . ':!domain-memory'` 是空的、162 個引用仍是 current。
4. **Recovery**：`make_recovery.py <segment>` 對 d1、d2、d3a、d3b、d3c 各跑一次（d1 只差事件 id 與時間時還原，不提交雜訊）；還原後量 current／shifted／stale（d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32）。
5. **參考解答**：資料格式改變時三個 `domain-memory/` 各跑一次 Plugin 的遷移指令（不用金鑰），核對 SOLUTION-NOTES 的數字。
6. **學員內容**：只改會壞的步驟；新功能的教法另開設計。
7. **驗證**：相容性檢查全部 PASS → `release_materials.py` 到 `RELEASE PIPELINE PASS` → Windows 與 macOS 各演練一次：D1 檢查點 2–3、D2 檢查點 1–6（含 push）、D2 Recovery、D3a 檢查點 4–5、D3b／D3c 檢查點 4、D4 檢查點 1、回顧檢查點 2；並把結果依「Plugin 版本政策」寫進 `decisions-and-open-issues.md`。

## 7. 主要風險

| 風險 | 影響 | 對策 |
|---|---|---|
| Agent 直接讀概念檔 | 看到 `status: stable`／`draft`，對不上提示詞的 reviewed／candidate | 提示詞用 `export`、`get-context`、`resolve-terms`；第二階段改寫「讀 domain-memory/ 裡的詞彙紀錄」 |
| `export` 輸出很長（D1 重播的 57 筆約 78 KB） | Agent 漏列候選，`validate --require-reviewed` 回「not reviewed」 | D2 第一步要求依類別回報筆數；第二階段考慮存檔再摘要 |
| 簽章歷史新增 commit 需要 Maintainer 私鑰 | 沒有私鑰就無法讓 hook 接受新的 Registry commit | 照 README 保管；遺失時授權新金鑰 |
| 換行被轉換 | 162 個證據引用全部 stale，簽章 commit 內容不符 | `* -text`、只用位元組層級的工具搬動 |
| Agent 在錯的資料夾或打錯 `--registry-root`，又建了第二個空的 Registry | 之後的紀錄寫進錯的地方 | dmlib 一律補 `--registry-root domain-memory`；只有 D1 檢查點 2 跑 `init-domain-memory`；每個「失敗時」都要 Agent 解釋後停下等人；1.2.14 起 Plugin 的拒絕句改成先檢查 `--registry-root`，並指出 Repo 裡已有的 Registry |
| 學員手動編輯 `.md` | 超出 frontmatter 子集（單引號、`[a, b]`）會被拒並附行號；編輯器改換行的影響未實測 | 第二階段補進主持人常見問題 |
