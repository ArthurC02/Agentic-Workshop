# domain-memory 觸及點與 OKF 升級計畫

> 讀者：DLC 維護者。時機：domain-memory 換版前（特別是 Registry 改存 OKF，Open Knowledge Format）。可見性：內部，不發學員。
> 更新日期：2026-10-16。目前固定 0.27.2（SkillHub `214f269f5`），本文件不改固定版本。

## 0. 方向與結論

SkillHub 0.28.0（`5f6e046f6`）是 OKF 的第一步：Plugin 內所有 Registry 讀寫改走單一 store，新增 `export --registry-root <root>`（以資產名為鍵，印出每種資產目前形狀的文件）；只有 `init` 與 `migrate-registry` 仍建立 JSON 版面，OKF 版面上線時改掉。SkillHub 工作區另有未 commit 的 0.29.0 草稿（`okf.py`），可看出版面方向，**但尚未定案**：

| 項目 | 0.27.2／0.28.0 | OKF 草稿（未 commit） |
|---|---|---|
| Registry 版面 | `domain-memory/registry/<資產>.json`＋`manifest.json` | `registry/index.md`＋`registry/<資產>/index.md`＋每筆一個 `registry/<資產>/<id>.md`（YAML 開頭區塊＋內文） |
| 狀態 | `status`（decisions 用 `review_status`）：candidate／reviewed | 開頭區塊 `status`：draft／stable／deprecated（讀出時換回 candidate／reviewed） |
| 證據 | `evidence[]`：`path`＋`lines` | 開頭區塊 `sources[]`：`resource: "path#L起-迄"`，雜湊欄位原樣保留 |
| 新增 Registry 時 | `init-domain-memory` 寫 JSON | 寫 OKF 版面 |
| 舊 Registry | — | 沒有 `index.md` 時照舊讀 JSON；`migrate-registry` 一次轉換，audit 加 1 筆 event（`migrate-registry`、`layout: okf`） |
| Git 歷史 | — | 舊 commit 仍以 JSON 讀（`verify-git-governance` 舊 commit 照常通過） |
| 不動的檔案 | policy、source map、`audit/`、`changes/` 都在 `domain-memory/` 根，不在 `registry/` 下 | 同左 |
| 換行 | JSON 由寫入時的平台決定（參考 Registry 多數 CRLF） | 概念檔一律 LF |

結論：DLC 自己的工具已不直接開 Registry 資產檔（讀取改走 `dmlib.registry_documents()`）；學員路徑上**唯一**寫死 JSON 版面的是 D2 檢查點 3 第一步與 `d2-signing-checklist.md` 第 2 節；簽章歷史與證據雜湊不受版面影響，但參考 Registry 與 Recovery 要加一個 Maintainer 簽章的 migrate commit。

標記：**不受影響**＝版面改變後照常；**需 migrate**＝內容要用 `migrate-registry` 轉換或重產；**需改寫**＝文字或程式要改。

## 1. Plugin 指令與旗標

學員都經 `dm.ps1`／`dm.sh`（→ `dmlib.py`）呼叫；`dmlib.expand()` 自動補 `--registry-root domain-memory`、`--repo-root .`，`verify-sources` 另補 `--source-map`、`--policy`，`init-signing-key` 補 `--key-file`。這三組指令集合（`REGISTRY_REQUIRED`／`REGISTRY_OPTIONAL`／`REPO_ROOT`）依 0.27.2 的 `cli_parser.py` 整理，相容性檢查會逐一比對。

| 指令 | 用到的旗標 | 出處 | 標記 |
|---|---|---|---|
| `readiness`、`quality-gates` | — | Runbook 01；`CHECKPOINTS.md`；主持人指南 | 不受影響 |
| `init-domain-memory` | `--output --source --exclude --storage-mode tracked --data-classification internal --review-mode local-draft-only --source-authority` | Runbook 10；`make_recovery.py` d1；`test_tools.py`；參考 README | 不受影響（產出版面跟著 Plugin） |
| `discover-sources`、`confirm-sources` | `--confirmed-by` | Runbook 10；`make_recovery.py`；`test_tools.py` | 不受影響 |
| `verify-sources`、`verify-evidence`、`coverage` | （dmlib 補 `--source-map`、`--policy`） | Runbook 10／19／29–59／60；RECOVERY.md；參考 README | 不受影響 |
| `cite` | `--path --start --end` | `make_record.py`、`fill_package.py` | 不受影響 |
| `upsert-candidate` | `--asset --record-file`（多個） | `make_record.py --upsert` | 不受影響（寫入經 Plugin） |
| `resolve-terms`、`get-context`、`get-record`、`analyze-boundary` | `--query`；`--id`；`--asset --id`；`--source-context --target-context` | Runbook 10／30／40／50／60；`fill_package.py`（`get-record`）；tools README | 不受影響 |
| `counterfactual` | `--file --find --replace --test-command`（＋dmlib `--save`） | Runbook 20／30／40／50；`test_tools.py`；tools README | 不受影響 |
| `init-change-package`、`validate-change-package` | `--output`；`--package-root` | `fill_package.py` | 不受影響 |
| `submit-proposal`、`record-approval`、`verify-proposal`、`finalize-proposal`、`apply-approved-updates` | `--package-root`；`--role --reviewer --scope` | Runbook 20；`d2-signing-checklist.md`；`test_tools.py` | 不受影響 |
| `init-signing-key`、`amend-policy`、`install-git-hitl-hook`、`governance-readiness`、`verify-git-governance`、`verify-audit`、`scan-secrets` | `--principal --key-file --sign-every-commit`；`--field --value --reason --verifier`；`--commit` | Runbook 20／29–59／60／70；RECOVERY.md；`make_recovery.py`；參考 README；簡報 30-d2 | 不受影響 |
| `validate` | `--require-reviewed` | 幾乎每一頁；簡報 20／30／40 | 不受影響 |
| `export`（0.28.0 起） | `--registry-root` | `dmlib.registry_documents()`；`check_dlc_plugin_compat.py` | 換版時把 `export` 加進 `dmlib.REGISTRY_REQUIRED` |

## 2. 直接讀寫的檔案路徑

| 路徑 | 誰、怎麼用 | 標記 |
|---|---|---|
| `domain-memory/registry/<資產>.json` | **學員**：Runbook 20-d2 檢查點 3 第一步「讀 `domain-memory/registry/` 底下每一個 JSON 檔（manifest.json 除外）」列全部候選；`worksheets/d2-signing-checklist.md` 第 2 節「每個有候選的 JSON 檔……一個同名的鍵」 | **需改寫**（見第 5 節） |
| 同上 | `dmlib.registry_documents()`：有 `export` 就用，0.27.2 才退回讀這些檔（唯讀） | 不受影響 |
| 同上 | `check_dlc_plugin_compat.py`：比對 export 與檔案內容；沒有 JSON 檔（已轉 OKF）時改查 export 列出全部資產 | 不受影響 |
| `domain-memory/registry/manifest.json` | 只出現在打包清單與快照 | 需 migrate（OKF 變成 `index.md`） |
| `domain-memory/domain-memory-policy.json` | Recovery 步驟 2 讀 `review_governance.authorized_signers`（`make_recovery.py`、RECOVERY.md、Runbook 29／39／49／59 三個分頁）；D2 檢查點 2 的 ③ 讀 `review_mode` 等；dmlib 補 `--policy` | 不受影響（草稿仍在 `domain-memory/` 根） |
| `domain-memory/source-map.json` | dmlib 補 `--source-map` | 不受影響 |
| `domain-memory/audit/events.jsonl`、`audit/manifest.json` | 只經 `verify-audit`；參考 README 記「64 events、head `sha256:955311a5…`」 | 格式不受影響；migrate 加 1 筆 event，數字需改寫 |
| `domain-memory/changes/<CP>/*.json` | `fill_package.py`、`write_scm_attestation.py` 直接讀寫（Plugin 的設計：`init-change-package` 產生範本，由人或 Agent 填寫） | 不受影響（草稿未動；OKF 定案時再確認） |
| `records/<資產>-<id>.json`、`cf-*.json`、`cp-d2.json` | DLC 工具自己的輸入輸出 | 不受影響 |
| `.git/hooks/pre-push` | D2 檢查點 2 的 ③；Recovery | 不受影響 |

## 3. 學員看到或 ③ 檢查的 Plugin 輸出

全部列在 `check_dlc_plugin_compat.py` 的 `QUOTED`；檢查時在本次執行的輸出或 Plugin 原始碼裡找得到才算 PASS。

| 字串 | 出處 | 標記 |
|---|---|---|
| `Registry is valid.` | Runbook 01／10／19／20／29–59／60；RECOVERY.md；簡報 30-d2；tools README | 不受影響 |
| `Change package is valid.`、`Proposal submitted for human review.`、`Proposal test evidence verified.` | Runbook 20 | 不受影響 |
| `Git governance is valid.`（Recovery 推送時「七行」） | Runbook 20／29–59；RECOVERY.md；簡報 30-d2；參考 README | 字串不受影響；行數需改寫（migrate 多一個 Registry commit） |
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

| 內容 | 位置 | 版面與位元組 | 標記 |
|---|---|---|---|
| 參考 Registry 的 Git 歷史 | `evaluation/reference-registry/smart-ticket-dlc-reference.bundle`，tag `dlc-d2-reviewed` | JSON（多數 CRLF）；6 個 Maintainer SSH 簽章的 Registry commit；證據雜湊依起始 Repo 原始位元組（23 個 CRLF 檔） | **需 migrate**：加一個簽章 commit，舊 commit 不動 |
| 參考 Registry 快照 | `evaluation/reference-registry/domain-memory/` | 同上 | 需 migrate（從新 tag 重新匯出） |
| D1 輸入、套件描述、反事實結果 | `reference-registry/inputs/`、`counterfactual/` | DLC 自己的格式 | 不受影響 |
| Recovery d1 | `facilitator/recovery/d1/`（`make_recovery.py d1` 以 Plugin 現場產生，未簽章、未 commit Registry） | 跟著 Plugin 版面 | 需 migrate（重產即可） |
| Recovery d2～d3c | `facilitator/recovery/d2…d3c/`（從 bundle tag 重產，`repo.bundle` 帶簽章歷史） | JSON | 需 migrate（改用新 tag 重產） |
| 參考解答 d3a～d3c 的 `domain-memory/` | `evaluation/reference-solutions/*/domain-memory/`（含 D3 候選；不是 Git repo，沒有簽章） | JSON | 需 migrate（各跑一次 `migrate-registry`，不用金鑰） |
| Plugin ZIP 與逐檔 SHA256 | `participant/vendor/domain-memory-0.27.2.zip(.SHA256SUMS)` | — | 換版用 `vendor_dlc_plugin.py --source <匯出資料夾>` |
| 打包清單 | `scripts/package-manifest-dlc.json`（逐檔列出 Registry 路徑與雜湊） | — | 重產後由 `release_materials.py` 自動 `--pin` |
| 驗證證據與報告 | `evaluation/dlc-validation-evidence.json`、`dlc-final-report.md` | — | 需改寫（重測數字） |

版本字串 `0.27.2`（換版時全文搜尋）：`07-dlc-ddd/README.md`、`participant/tools/{dmlib.py,doctor.py,README.md}`、`facilitator/facilitator-guide.md`、`evaluation/{dlc-final-report.md,observation-guide.md,dlc-validation-evidence.json,reference-registry/README.md}`、`materials-dlc/README.md`、Runbook `01-environment.md`、`docs/instructions/11_DDD_DLC產製指令書.md`、本資料夾 `decisions-and-open-issues.md`、`scripts/{build_delivery_dlc.py,test_build_delivery_dlc.py}`。`doctor.py` 的 `PLUGIN_VERSION` 會把其他版本判為 `[!!]`。

## 5. 學員提示詞：改用 Plugin 指令的候選

| 位置 | 現在的寫法 | 0.27.2 能否改用 Plugin 指令 | 處理 |
|---|---|---|---|
| Runbook 20-d2 檢查點 3 第一步；`d2-signing-checklist.md` 第 2 節 | 讀 `registry/` 每個 JSON 檔列候選；`promote` 的鍵＝檔名去掉 `.json` | 不能：`export` 0.28.0 才有；`lookup` 有筆數上限（policy 的 `query_result_limit`），D1 詞彙 21 筆會被截掉 | 未改；OKF 上線時改成下方文字 |
| Runbook 20-d2 檢查點 2 的 ③；Recovery 頁（29／39／49／59）與 RECOVERY.md 步驟 2 | 讀 `domain-memory-policy.json` | 不能：`governance-readiness` 不印這些欄位 | 未改；policy 不在 `registry/`，不受影響 |
| Runbook 10（檢查點 5 失敗時）、30、40、50 | 「讀 `domain-memory/` 裡的詞彙紀錄」 | 不需要：沒寫檔名，版面中立 | 未改；換版後可改用 `export` |
| Runbook 60-d4、`d4-handoff-template.md` | 用 `get-record` 逐一查證 id | 已是 Plugin 指令 | 不受影響 |
| 詞彙表 Registry 列、`participant/README.md`、`d4-handoff-template.md` | 「`domain-memory/` 裡的 JSON 檔」 | — | **已改**為「檔案」（寫死格式但不必要） |

OKF 上線後 D2 檢查點 3 第一步的建議寫法（兩個分頁同一段）：

```text
1. 執行 ..\..\tools\dm.ps1 export（Git Bash 與 macOS：../../tools/dm.sh export），從輸出記下 Registry 裡全部候選的 id（status 是 candidate；decisions 看 review_status），依類別分開（第二步要用）……
```

`d2-signing-checklist.md` 第 2 節對應改成「每種有候選的類別一個同名的鍵（export 輸出的頂層鍵，例如 `rules`、`vocabulary`）」。先在 `dmlib.REGISTRY_REQUIRED` 加 `export`，`dm export` 才會自動補 `--registry-root`。

## 6. 相容性檢查

`scripts/check_dlc_plugin_compat.py [--source <匯出的 Plugin 資料夾或 ZIP>]`：在暫存沙箱跑（一）`cli_parser` 與 dmlib 指令集合、學員用到的指令與旗標；（二）tools 自檢；（三）D1 重播（`make_recovery.build_d1`）與 D1／D3 的查詢指令；（四）參考 Registry（從 bundle 還原）唯讀驗證、兩個 attestation commit、兩個 Change Package、export 與檔案一致、經 pre-push hook push 既有簽章歷史；（五）第 3 節的字串。不改 Repo、不用私鑰，約 2 分鐘。

| 版本 | 結果（2026-10-16，Windows） |
|---|---|
| 0.27.2（已封裝 ZIP） | 29 PASS、0 CHANGED；export 一致項目走讀檔備援 |
| 0.28.0（`git archive 5f6e046f6`） | 28 PASS、1 CHANGED：`export` 是新的 `--registry-root` 必填指令，dmlib 還沒列；其餘（含 export 與檔案內容一致）全部通過 |
| 0.29.0 草稿（SkillHub 工作區複本，僅供預測） | 同 0.28.0：D1 重播已是 OKF 版面（57／57 候選經 export 讀到），JSON 版面的參考 Registry 仍全部通過。另在沙箱試 `migrate-registry`：轉出 69 個 `.md`、audit 64→65 events，`validate --require-reviewed`、`verify-evidence`、`verify-audit`、舊 commit 的 `verify-git-governance`、`validate-change-package` 都通過 |

## 7. OKF 上線時的步驟

1. **評估**：讀 CHANGELOG；`git -C <SkillHub> archive <commit> .claude/skills/domain-memory` 匯出到暫存資料夾；跑相容性檢查，CHANGED 清單就是待辦。`vendor_dlc_plugin.py` 的預設來源是 SkillHub 工作區（現在是未發布的 0.29.0 草稿），一律加 `--source`。
2. **工具**：dmlib 三組指令集合依檢查結果更新（至少加 `export`）；`doctor.PLUGIN_VERSION`；第 4 節的版本字串；`build_delivery_dlc.VENDOR_ZIP`、`test_build_delivery_dlc.py`；以 `vendor_dlc_plugin.py --source` 封裝新 ZIP、刪舊 ZIP。
3. **參考 Registry（只能在 Maintainer 的電腦做）**：clone bundle、checkout `dlc-d2-reviewed`、設定 `gpg.format ssh` 與 allowed signers → `migrate-registry` → `validate --require-reviewed`、`verify-evidence`、`verify-sources`、`verify-audit` → 由 `maintainer-2` 金鑰（`~/.dlc-keys/maintainer-2/`，指紋 `SHA256:GtKS8fEN…MueCs`）簽章 commit「Registry 改存 OKF 版面」→ `verify-git-governance --commit HEAD` → push 到暫時的 bare remote，hook 印七行 → tag 改指向新 commit → 重做 bundle → 用 `git archive` 重新匯出 `domain-memory/` 快照。
   - 私鑰**不得**複製進 Repo、OneDrive、沙箱或對話；手邊沒有私鑰時照參考 README「遺失時」以 `amend-policy` 授權新金鑰（再多一個 commit），不要用 `--no-verify`。
   - 證據雜湊取決於來源檔的原始位元組（bundle 裡 23 個 CRLF 檔）；migrate 不動來源檔，但任何換行轉換都會讓全部證據變 stale。保持 `* -text`、`core.autocrlf=false`，不要用 `sed -i` 或編輯器另存。概念檔是 LF、舊 JSON 是 CRLF，屬正常。
   - 舊的 6 個簽章 commit 與兩個 attestation 雜湊不變；README 的 commit 列表、events 數、head 雜湊、「六行／七行」要改寫。
4. **Recovery**：`make_recovery.py` 的 commit 數文字（「Registry 的六個 commit」「七行」）與主持人指南第 284 行一起更新，重跑 `make_recovery.py d1 d2 d3a d3b d3c`；Runbook 的 Recovery 頁沒寫數字，不用改。
5. **參考解答**：三個 `domain-memory/` 各跑一次 `migrate-registry`（不用金鑰），重跑各自的 `validate`、`verify-evidence`，核對 `SOLUTION-NOTES.md` 的數字。
6. **學員內容**：照第 5 節改 D2 檢查點 3 第一步與簽章流程清單；詞彙表 Registry 列的出處章節（`registry-schema.md`）若改名，`check_references.py` 會擋；tools README、主持人指南、觀察指引的版本與數字。
7. **驗證**：相容性檢查全部 PASS → `release_materials.py` 到 `RELEASE PIPELINE PASS` → Windows 與 macOS 各演練一次：D1 檢查點 2–3、D2 檢查點 1–6（含 push）、D2 Recovery、D3a 檢查點 5、D4 檢查點 1；並把結果依「Plugin 版本政策」寫進 `decisions-and-open-issues.md`。

## 8. 主要風險

| 風險 | 影響 | 對策 |
|---|---|---|
| D2 檢查點 3 第一步寫死 JSON 檔 | 學員自己的 D1 會是 OKF 版面，Agent 找不到 `*.json`，`promote` 漏列，`validate --require-reviewed` 回「not reviewed」 | 換版時同步改提示詞與簽章流程清單（第 5 節）；換版前不要讓學員用未固定的 Plugin |
| 參考 Registry 與 Recovery 只升 Plugin、不 migrate | 同一班出現兩種版面（自己做的 D1 是 OKF、Recovery 是 JSON），提示詞得同時照顧兩者 | 一律 migrate（第 7 節第 3–5 步） |
| migrate commit 需要 Maintainer 私鑰 | 沒有私鑰就無法讓 hook 接受新的 Registry commit | 照 README 保管；遺失時授權新金鑰 |
| 換行被轉換 | 162 個證據引用全部 stale，簽章 commit 內容不符 | `* -text`、只用位元組層級的工具搬動 |
| OKF 草稿尚未定案 | 第 0、6 節的預測會變 | 以定案 commit 重跑相容性檢查為準 |
