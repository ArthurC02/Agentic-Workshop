# DDD DLC 產製結果

> 本報告記錄的是 2026-10-07 以 Plugin 0.2.2、候選包 efbd1ba2c3e7b958 的驗證；0.10.15 升級與相容性見 docs/planning/decisions-and-open-issues.md（2026-10-10）。D3c datetime mutant 的判定已改為測試不足（見 observation-guide）。

> 驗證日期：2026-10-07（重驗；取代先前對 `63c281a541f2001a` 的 FAIL 判定）。驗證對象：候選包 `dist/dlc-candidate/efbd1ba2c3e7b958/`（與 `materials-dlc/edition.json` 的 `candidate_id`、`scripts/package-manifest-dlc.json` 的 sha256 前 16 碼一致）。
> 方法：只用候選包 ZIP，在短路徑 `C:/dlcv/`（簽章演練在 `C:/dlcp/`）解壓、還原與執行，驗證後刪除；Python 3.13.14、Windows 11、全新 venv、Plugin 取自學員包內的 vendor ZIP（SkillHub 原檔未動）。
> 本次只寫入兩個檔案：本報告與 `dlc-validation-evidence.json`（各項指令、exit code、輸出 sha256）。其他交付物未修改、未重新打包。
> 標示：**驗證者實跑**＝本次親自執行；**主持代理實跑**＝由協調代理先前執行，本次已重跑或以位元組比對確認。

## 產製檔案

| 項目 | 狀態 |
|---|---|
| `dist/dlc-candidate/efbd1ba2c3e7b958/`：14 個 ZIP＋`build-evidence.json` | 齊備；Python 3.13.14、zlib 1.3.1、`missing_packages` 空；14 個 ZIP 的實際 sha256 與 evidence 相符 |
| 與前一候選 `63c281a541f2001a` 的差異 | 12 個 participant／recovery ZIP **位元組相同**；只有 `facilitator-dlc-before-session`、`evaluation-dlc-private` 改變 |
| `dist/materials-dlc/participant-materials-dlc.zip` | 只含 `runbook.html`，sha256 與建置成品 `fdaba90f…b2c9` 相同 |
| `agentic-workshop/07-dlc-ddd/README.md` | **已存在**（總覽、三分目錄、建置與驗證指令） |
| `agentic-workshop/07-dlc-ddd/evaluation/dlc-validation-evidence.json` | **本次產出** |
| §2 指名腳本：`scripts/test_build_materials.py`（EditionTests）、`scripts/test_build_delivery_dlc.py`、`scripts/build_delivery_dlc.py`、`scripts/vendor_dlc_plugin.py`、`facilitator/recovery/make_recovery.py` | 齊備（§1 第 13 項(c) 已對齊實際檔名） |
| 參考解答 `d3a`／`d3b`／`d3c` | 各含 `src/ tests/ docs/ domain-memory/ evidence/`、`evidence/registry-candidates.json`、`SOLUTION-NOTES.md` 第 9 節 |

## Plugin 封裝與 SHA 核對（§7.1，驗證者實跑）

- `participant-dlc-open.zip` → `vendor/domain-memory-0.2.2.zip`（`de6aad75…c89dc`）；`sha256sum -c domain-memory-0.2.2.zip.SHA256SUMS`：**130／130 OK**（129 檔＋整包）。
- `.claude-plugin/plugin.json` 版本 `0.2.2`；`vendor_dlc_plugin.py --check` UP-TO-DATE。**PASS**

## 起始 Repo 檢查（§7.2，驗證者實跑）

- 全新 venv、`pip install -r requirements.txt`、`pytest -q -rsx`：**76 passed**，無 skip／xfail（唯一警告為 Starlette／AnyIO DeprecationWarning）。
- §5.1 殘留字詞 grep（排除 `.venv`、`__pycache__`、`.pyc`）：**0 命中**。**PASS**

## Reference Registry 驗證（§7.3，驗證者實跑）

由 `smart-ticket-dlc-reference.bundle` clone，`gpg.ssh.allowedSignersFile` 指向 `keys/maintainer.allowed_signers`，經學員 `tools/dmlib.py` 執行：

| 指令 | 結果 |
|---|---|
| `git log --format='%h %G? %GS %s'` | 3 個 Registry commit `G maintainer@example.com`、起始 commit `N` |
| `validate --require-reviewed` | `Registry is valid.` |
| `verify-evidence` | 162／162 `current` |
| `verify-sources` | `current`／`developer-confirmed` |
| `verify-audit` | `valid`，62 events，head `sha256:4d82bb43…6affa` |
| `verify-git-governance --commit 5538b6d…` | `Git governance is valid.` |
| `install-git-hitl-hook` → `governance-readiness` | `{"status": "ready", "blocks": []}`（先前 NOT_RUN，本次補驗） |
| `scan-secrets` | complete，0 findings |
| `coverage` | 5 Contexts、21 詞、2 Aggregates、16 規則；缺口 `without_aggregate: [inventory, membership]`、5 個 Context 無 Contract；`confirmed_absent: pricing` 無 Aggregate；`evidence_gaps: []`。皆為 reference-registry README「刻意保留的缺口」所列 |

**PASS**

## 參考解答驗證（§7.4，驗證者實跑）

依 §1 第 13 項(a)：Registry 狀態＝D2 reviewed Registry＋D3 候選，不產出新的 Change Package。

| 參考解答 | pytest（全新 venv） | `validate` | `verify-audit` | `coverage` | 候選／Change Package | 預期 stale（exit 1，留給 D4） |
|---|---|---|---|---|---|---|
| d3a-e-invoice | **118 passed** | valid | valid，72 events | 6 Contexts、24 詞、20 規則，`evidence_gaps []` | +10 候選；`changes/` 只有 D2 的 `CP-CORE-001` | 15／192（`payment_service.py` 11、`store.py` 4）；sources：`docs/adr`、`src`、`tests` 變更 |
| d3b-points-redemption | **156 passed** | valid | valid，82 events | 6 Contexts、26 詞、26 規則 | D3a 的 10 筆＋D3b 10 筆＝20 候選；同上 | 57／225（`payment_service` 14、`models` 13、`booking_service` 8、`business-rules.md` 7 等） |
| d3c-group-partial-refund | **179 passed** | valid | valid，90 events | 6 Contexts、27 詞、30 規則、3 Aggregates（含候選 `booking-v2`） | 前兩段 20 筆＋D3c 8 筆＝28 候選；同上 | 77／248（`models` 15、`payment_service` 14、`business-rules.md` 12、`seat_service` 8 等） |

- 三者都沒有 skip／xfail；reviewed 記錄數與 D2 相同（新增事實全為 `candidate`）；被推翻的 reviewed 事實以新 id 候選（如 `REFUND-004-V2`、`booking-v2`）描述。
- stale 數量與檔案和各 `SOLUTION-NOTES.md` 第 9 節的列表一致。**PASS**

## Counterfactual 對照表（§7.5，驗證者實跑）

在解壓複本上重跑三支 `evidence/run_counterfactuals.py` 的全部案例（cmd.exe 執行、venv python 絕對路徑）：

| 情境 | 結果 | 未 killed |
|---|---|---|
| d3a | **25／25 killed** | 無（另有 shipped 的等價 mutant 紀錄 `vat-half-boundary-EQUIVALENT-survived`，SOLUTION-NOTES §4 有證明） |
| d3b | **23／24 killed** | `min-points-1-EQUIVALENT-survived`（PTS-003 另有 3 次 killed；SOLUTION-NOTES §4 證明為等價） |
| d3c | **37／38 killed** | `days-by-datetime-EQUIVALENT-survived`（PCR-004 另有 10 次 killed；在 Seed Clock 下等價） |

規則 id → killed 次數（修改點與測試逐案列在 evidence JSON 的 `rows`）：

- d3a：EINV-001→2、002→3、003→2、004→2、005→1、006→2、007→1、008→2、009→1、010→1、011→2、013→4、014→2（EINV-001／006 已補上）。
- d3b：PTS-001→1、002→1、003→3、004→1、005→3、006→1、007→2、008→1、009→2、010→1、011→1、012→2、013→1、014→1、015→2。
- d3c：PCR-001→3、002→4、003→1、004→10、005→3、006→4、007→1、008→2、009→2、010→2、011→1、012→1、013→2、014→1。

- 本次 verdict 與 shipped JSON 逐案相同；跑完後 `src/ tests/ docs/ domain-memory/` 與原檔逐位元組相同，全套仍為 118／156／179 passed。
- 每條登記為 Registry 候選的新規則（EINV-002/003/005/008、PTS-003/005/008/009/012/014、PCR-004/005/008、REFUND-004-V2 經 PCR-007/012）都至少有一次 killed。
- 殘留缺口（非阻擋）：EINV-012（延伸 AC）與 EINV-015（測試替身要求）在交付物中沒有 counterfactual JSON。本次以臨時 mutant 補驗，不寫入交付物：EINV-012 付款時丟棄購票人資訊 → killed；EINV-015 Adapter 漏判 1002 → killed（皆為斷言失敗）。**PASS**

## 成對簽章演練（§7.6，驗證者實跑；主持代理先前對 63c281a541f2001a 跑過同一腳本）

`scratchpad/push_test.sh` 只改候選路徑，對 `efbd1ba2c3e7b958` 的 `participant-dlc-open`＋`recovery-dlc-d2` 照 RECOVERY.md 逐行執行。git 使用者為 `DLC Proposer`，簽章者 `maintainer@example.com`，新金鑰放在重導後的 `HOME/.dlc-keys`：

- 76 passed；歷史 3×`G`＋`N`；`init-signing-key --sign-every-commit` → `amend-policy authorized_signers` → `install-git-hitl-hook` → `governance-readiness` **ready** → 簽章 commit `G`。
- `setup_remote.py` 建 bare remote；**簽章 push exit 0**（`* [new branch] HEAD -> main`）。
- 未簽章 Registry commit：**push 被 pre-push hook 拒絕**，`ERROR: Git commit signature is invalid`，exit 1。
- 演練後對該 Repo 執行 `scan-secrets`：complete，0 findings（金鑰在 Repo 外）。
- 兩個 ZIP 與 63c281a541f2001a 位元組相同，所以主持代理先前的結果也適用。
- 兩個身分完整走 D2（submit → 夥伴 `record-approval` → 簽章核准 commit → attestation → finalize → apply）以 reference bundle 為證：`CP-CORE-001` 的 proposer 為 Proposer、reviewer 為 Maintainer，`verify-git-governance` valid。本次沒有從頭重跑整段 D2。**PASS**

## 輔助腳本與計時實測（§7.7）

- `participant/tools/test_tools.py`：**5 tests OK**（驗證者實跑，Plugin 取自 vendor ZIP；主持代理以 SkillHub Plugin 跑也得到 5 OK）。
- 以腳本重做 D1、D2 的計時：**NOT_RUN**。
- 檢查點時窗超過 5 分鐘：D3a／b／c 步驟 3（7／8／9 分）、D3c 步驟 4（6 分），屬 §1 第 13 項(d) 已接受的例外。

## 建置、打包與主課回歸（§7.8–7.10，驗證者實跑）

| 檢查 | 結果 |
|---|---|
| `build_materials.py --edition dlc` 連建兩次 | deck `f87b1bd1…69da`、runbook `fdaba90f…b2c9`，兩次相同，且與建置前磁碟相同 |
| `--edition dlc --check` | UP-TO-DATE；72 張投影片；runbook 用本候選 12 個 ZIP；safety：codes／plaintext clean、forbidden 0、external URL 0 |
| 主課 `build_materials.py --check` | UP-TO-DATE；safety clean |
| `build_delivery_dlc.py --verify dist/dlc-candidate/efbd1ba2c3e7b958` | 14 包 verified，`missing: []` |
| `unittest discover -s scripts -p "test_*.py"` | **Ran 165 tests OK**（含 EditionTests、test_build_delivery_dlc） |
| `validate_workshop.py --static-only` | `STATIC_PASS`（403 md、869 links、0 errors） |
| `validate_consistency_corrections.py` | `PASS`（C-01～C-09） |
| 主課保護 | `scripts/package-manifest.json` 未改；`c841f2424d256c28` 的 13 個 ZIP 與其 evidence 相符；`dist/` 未被追蹤；無私鑰檔或私鑰內容被追蹤 |

註：兩個主課 validator 會改寫 `06-runbook/evaluation/` 的兩個 evidence JSON（時間戳與計數），本次執行後已用 `git checkout` 還原。

## Participant Leakage Check（§7.11，驗證者實跑；主持代理先前得到同一結果）

- `zip_leak_scan.py` 掃描全部 participant-*／recovery-* ZIP（含內層 ZIP）：**659 檔、0 problem**。掃描項目：路徑段 facilitator／evaluation／instructions／reference-*／rubric／observation*／.dlc-keys／.venv／.git、私鑰標頭、禁用片語、13 組解鎖碼（正規化後比對）。
- headless 解開 13 個群組後的 Runbook 文字共 131,771 字：9 個 forbidden marker 0 命中、解鎖碼 0 命中。
- Recovery 包與前一候選位元組相同，結構符合 §3.2：`RECOVERY.md`、`repo.bundle`、Repo；d2 起另有公鑰 `keys/maintainer.allowed_signers`（§1 第 13 項(e)）。make_recovery 會略過參考解答的 `domain-memory/` 候選。**PASS**

## 瀏覽器冒煙（§7.12，驗證者實跑 headless）

headless Edge 以 `file://` 開啟目前的 `runbook.html`：

- 21 頁全部解鎖且有內容；8 個檢查點頁的導覽步驟數與 `.rb-step` 相同（environment 5、d1／d2／d3a／d3b／d3c 各 8、d4 4、retro 5）。
- 點膠囊後表單存入 `stwdlc:form:*`；「全部匯出」產生 `smart-ticket-dlc-runbook-<stamp>.zip`，`testzip()` 為 None。
- 預設的 3 個主課 `stw:` 鍵沒有被改動；新增的鍵全部以 `stwdlc:` 開頭。
- 非 headless 的實際瀏覽器操作、手動輸入解鎖碼與截圖審視：**NOT_RUN**。

## NOT_RUN 項目與補驗方式

| 項目 | 原因 | 補驗方式 |
|---|---|---|
| §7.7 以腳本重做 D1、D2 的計時 | 未做計時演練 | 以 `make_record.py --batch`、`fill_package.py` 依 CHECKPOINTS.md 實跑並記錄分鐘數 |
| §7.6 從頭重跑兩個身分的完整 D2 | 本次只重跑 Recovery 接手、push 與拒絕；完整流程以 reference bundle 為證 | 在乾淨的起始 Repo 依 Runbook D2 由兩人實跑一次 |
| §7.12 實際瀏覽器操作與版面截圖 | 只做了 headless | 以 `file://` 開啟 deck 與 Runbook，手動走一遍並截圖 |
| 真人演練（各段每人耗時） | 尚無真實場次 | 至少一場 pilot，記錄每個檢查點的實際分鐘數 |

## 與上位規格的一致性檢查

| 規格 | 結果 |
|---|---|
| §2 產出清單 | 符合（README、evidence JSON、實際腳本名稱依 §1 第 13 項(c)） |
| §3.1 時程連續、合計 180、九段 id；Python／JS PLAN 一致 | 符合（edition.json；EditionTests 通過） |
| §3.2 環境／下載頁屬 `dlc-opening` | 已接受的偏差，§1 第 13 項(b) |
| §4.1 開場四個檢查點 | 已接受的偏差，§1 第 13 項(b) |
| §4 每步 ≤ 5 分鐘 | 已接受的例外：D3a／b／c 步驟 3、D3c 步驟 4（§1 第 13 項(d)） |
| §4.4／§7.4 參考解答＝D2 reviewed＋候選，不產出新 Change Package | 符合（§1 第 13 項(a)） |
| §7.5 每條新規則有 killed counterfactual | 符合；AC 層級 EINV-012／015 的證據檔仍缺（見下方「待辦」第 1 項） |
| §3.2 RECOVERY 會複製維護者公鑰到 `~/.dlc-keys` | 已接受，§1 第 13 項(e)（只有公鑰） |
| §3.3 操作順序、§5.2 Windows 陷阱 | Recovery、Runbook 與參考解答處理一致（簽章先於 Registry commit、`-X utf8`、cmd.exe 絕對路徑、看到 `killed` 才算、push 前啟用 .venv、金鑰放 Repo 外） |
| §6 主課保護 | 符合 |
| §1 第 12 項(a) 起始 Repo `.gitattributes`、76 個測試 | 符合 |

## 已知限制

- 候選包 `efbd1ba2c3e7b958` 的 `evaluation-dlc-private.zip` 仍是**舊版** `dlc-final-report.md`（FAIL），而且沒有 `dlc-validation-evidence.json`。這兩個檔案在打包後才寫入，所以 manifest 的 `evaluation-dlc-private` 已與來源不一致（一個 drift、一個未 pin）。下次 `build_delivery_dlc.py` 建置前要先 `--pin`，產生新候選後再更新 `edition.json`。學員包與 Recovery 包不受影響。
- 參考解答的 `verify-evidence`／`verify-sources` 都是 stale（15／57／77），exit 1。這是預期結果，交給 D4 處理。
- `record-approval` 在同一台機器用兩個身分仍可通過（§8 R3）。這是教學示範，不是安全保證。
- headless 冒煙不能取代真人在實際瀏覽器上的操作與版面審視。
- 演練時把 HOME／USERPROFILE 重導到暫存目錄，pip 因此在 Repo 內留下 `pip/cache`，第一次 `scan-secrets` 回報 incomplete（exit 2）。刪除後重掃為 complete、0 findings。這是驗證環境造成的，學員照常操作不會遇到。

## Final Decision

**PASS FOR WORKSHOP USE**

第 7 節沒有任何項目為 FAIL。前次的兩個 blocker 都已解決：參考解答的範圍依 §1 第 13 項(a) 改為「reviewed＋候選」並逐項驗證通過；README 與本 evidence JSON 也已存在。NOT_RUN 項目已在上表列出原因與補驗方式。

非阻擋待辦：

1. 補上 EINV-012、EINV-015 的 counterfactual 證據檔（本次的臨時 mutant 都是 killed）。
2. 對 `evaluation-dlc-private` 執行 `--pin` 並重建，讓主持人包帶入本報告與 evidence JSON（只影響 evaluation 包與候選 id）。
3. 以腳本計時重做 D1／D2；在實際瀏覽器以 `file://` 審視並截圖；至少一場 pilot。
4. §9 未決事項（奇數人組的第三人角色、Python 3.13／`py` launcher 保證、D2 示範錄影）仍待使用者決定。

## 驗收後修正（commit 前審查）

上述驗收針對候選包 `efbd1ba2c3e7b958`。之後的程式碼與內容審查做了下列修正，修正後的候選包為 `edition.json` 的 `candidate_id`：

- `participant/tools/`：PowerShell 5.1 參數轉義（空字串、引號）；`--save` 失敗時把 ERROR 印到 stderr；`init-signing-key` 未給 `--key-file` 時預設 `~/.dlc-keys/<principal>/signing-key`，並拒絕 Repo 內的金鑰路徑；`doctor` 偵測 Repo 內金鑰；缺檔／缺欄位改為中文錯誤訊息。
- `scripts/build_delivery_dlc.py`：`--allow-missing` 建置不再要求 vendored Plugin；`generated` 檔名先正規化再檢查衝突；`--verify` 遇損壞目錄回報 FAIL 而非 traceback。
- 內容：主持人指引與 D2 投影片的 PowerShell `--key-file` 改用 `$env:USERPROFILE`；counterfactual 直譯器路徑錯誤時為 exit 1（非 exit 0）；D1 改為各自 Repo、D2 起兩人共用；D2 檢查點 2 角色改為 Maintainer。
- `agentic-workshop/07-dlc-ddd/.gitattributes`（`* -text`），避免 Windows checkout 換行轉換造成 pin 的 sha256 不符。

修正後重跑：主課與 DLC `--check` UP-TO-DATE；scripts 167 tests OK；tools 5 tests OK；`--verify` missing 空；participant／recovery ZIP leak scan 659 檔 0 問題；§7.6 成對簽章 push 演練：簽章 push exit 0、未簽章 Registry commit 被 hook 拒絕 exit 1。結論維持 **PASS FOR WORKSHOP USE**。
