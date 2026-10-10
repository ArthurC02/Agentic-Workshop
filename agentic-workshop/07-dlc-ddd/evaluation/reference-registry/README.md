# 參考 Domain Registry（主持人專用）

`smart-ticket-dlc-base` 的完整 reviewed Domain Registry，以學員輔助工具（`participant/tools/`）照 D1＋D2 流程實際做出來。用途：D2 預設降級與 Recovery（`dlc-rec-d2`）、主持人簽章示範、揭曉時對照。**不得放進任何學員包或 Runbook。**

## 內容

| 路徑 | 內容 |
|---|---|
| `smart-ticket-dlc-reference.bundle` | 參考 Repo 的完整 git 歷史（`git bundle`），保留 SSH 簽章；**還原以它為準** |
| `domain-memory/` | 最終 Registry 的檔案快照（policy、source map、registry、audit chain、`changes/CP-CORE-001/`），方便直接閱讀 |
| `domain-memory/changes/CP-CORE-001/` | 已 `applied` 的 Change Package（proposer：Proposer，reviewer：Maintainer） |
| `keys/maintainer.pub`、`keys/maintainer.allowed_signers` | Maintainer 的**公鑰**與 allowed signers（沒有私鑰；私鑰從未離開產製機） |
| `counterfactual/cf-*.json` | 四條規則的 counterfactual 原始輸出（全部 killed、原檔已還原） |
| `inputs/d1-records.json`、`inputs/package-spec.json` | 產生本 Registry 的工具輸入（`make_record.py --batch`、`fill_package.py`） |

歷史（`git log --format='%h %G? %GS %s'`）：

```
3cb6e74 G maintainer@example.com CP-CORE-001：finalize 並套用，核心模型升為 reviewed   ← tag dlc-d2-reviewed
5538b6d G maintainer@example.com CP-CORE-001：maintainer 核准 Change Package          ← attestation 指向此 commit
22de5e4 G maintainer@example.com D1：候選 Domain Registry（5 Contexts、21 詞、16 規則）
21fe6da N                        Smart Ticket DLC base（起始 Repo 原樣＋.gitattributes）
```

第一個 commit 未簽章是刻意的：它不碰 Registry，hook 只檢查觸及 Registry 的 commit。簽章在第一個 Registry commit（22de5e4）之前就以 `init-signing-key --sign-every-commit` 設好。

## 模型摘要

- Contexts（5）：`booking`（core）、`pricing`（core）、`inventory`、`membership`、`payment`（supporting）。程式是分層結構而非依 Context 切目錄，所以刻意不填 `implementation_path`。
- Vocabulary 21 詞；Rules 16 條（FARE-002/003/005/008、MEMBER-003/004、BOOKING-002/003、SEAT-001、GROUP-001/004、GROUP-PAY-002、PAYMENT-001、ORDER-002、REFUND-004、CHANGE-004），每條都有測試 obligation。
- Aggregates 2：`booking`、`order`。`pricing` 以 `confirmed_absences` 記錄「無狀態政策，沒有 Aggregate」。
- Interactions 5：booking→pricing、membership→pricing、booking→inventory、booking→payment、inventory→payment（`analyze-boundary` 的 `--source-context` 是 producer）。
- Decisions 8：ADR-001～004（accepted），以及 ASIS-001～004：**現況設計洩漏的觀察**（三份座位真相、三處複製計價迴圈與 FarePolicy 死碼、Payment 無 Port 且內含補償、退款以 booking_id 為鍵）。狀態為 `observed-design-leak`，不是已核准決策；`review_status` 為 reviewed 只表示「這個觀察經過審查屬實」。
- `coverage` 刻意保留的缺口：`inventory`、`membership` 無 Aggregate（現況沒有守一致性的擁有者，留給 D3）；五個 Context 都無 Contract（沒有對外版本化契約）；Trip 查詢、通知、稽核未建模為 Context。
- 證據只引用已確認來源（`docs/requirements/`、`docs/adr/`、`src/`、`tests/test_*.py`）。`docs/architecture.md`、`tests/**/conftest.py` 是 unclassified，未引用。

## 還原（D2 Recovery）

需求：Git ≥ 2.34、Python 3.13、domain-memory Plugin 0.10.15（下以 `tools/` 指學員包的 `participant/tools/`，Plugin 依 tools README 的位置規則尋找）。

PowerShell：

```powershell
git clone smart-ticket-dlc-reference.bundle smart-ticket-dlc-base
cd smart-ticket-dlc-base
git remote remove origin
git config --local gpg.format ssh
git config --local gpg.ssh.allowedSignersFile "<本資料夾絕對路徑>\keys\maintainer.allowed_signers"
git log --format='%h %G? %GS %s'          # 三個 Registry commit 都應為 G maintainer@example.com
py -3.13 -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\tools\dm.ps1 validate --require-reviewed
..\tools\dm.ps1 verify-evidence
..\tools\dm.ps1 verify-sources
..\tools\dm.ps1 verify-audit
..\tools\dm.ps1 verify-git-governance --commit 5538b6dbcba9e5c4468ceddec72b75b231f9688d
..\tools\dm.ps1 install-git-hitl-hook        # hook 不在 bundle 內
..\tools\dm.ps1 governance-readiness         # 安裝 hook 後為 ready
```

Git Bash 相同，改用 `../tools/dm.sh` 與 `source .venv/Scripts/activate`。

預期結果（產製時實測）：`Registry is valid.`；verify-evidence 162 個引用全部 `current`；verify-sources `current`／`developer-confirmed`；verify-audit `valid`、62 events、head `sha256:4d82bb43…6affa`；`Git governance is valid.`；pytest 76 passed。還原（不含 venv）約 10 秒。

## 學員從 Recovery 接續（D3 之後還要 push）

還原的 Repo 只授權 maintainer 的金鑰，學員沒有私鑰。成對組要接手時：

```bash
../tools/dm.sh init-signing-key --principal partner@example.com --key-file ~/.dlc-keys/partner/id_ed25519 --sign-every-commit
../tools/dm.sh amend-policy --field authorized_signers --value "SHA256:Zgznp4qU2GZH6Vmr2/RHtQzVnE+CbK2meH71Cq9BAH0,<新 fingerprint>" --reason "Recovery 後由本組接手簽章"
cat <本資料夾>/keys/maintainer.allowed_signers >> ~/.dlc-keys/partner/id_ed25519.allowed_signers
../tools/dm.sh install-git-hitl-hook
git add domain-memory && git commit -m "接手 Recovery：授權本組金鑰"
```

第三行不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 指向只含新金鑰的檔案，歷史上 maintainer 簽的 commit 就驗不過，push 會被 hook 以「Git commit signature is invalid」拒絕（產製時實測過，補上這行後 push 成功）。

## 與 `facilitator/recovery/` 的對應

| Recovery 群組 | 來源 | 做法 |
|---|---|---|
| `dlc-rec-d2` | 本 bundle 的 tag `dlc-d2-reviewed` | 依上面「還原」前四行 clone 成 `smart-ticket-dlc-base/`（保留 `.git` 才能驗簽章），附 `keys/maintainer.allowed_signers` 與「學員從 Recovery 接續」那段指令，壓成 ZIP 放在 `facilitator/recovery/dlc-rec-d2/`。不放 `counterfactual/`、`inputs/` 與本 README（第 3.2 節：Recovery 不含 counterfactual 證據原稿與 evaluation 檔案）。 |
| `dlc-rec-d1` | `inputs/d1-records.json` | 在起始 Repo 的乾淨複本上執行 `init-domain-memory`（`--review-mode local-draft-only`）＋`confirm-sources`，再 `make_record.py --batch d1-records.json --upsert`（57 筆約 100 秒）。得到「已確認 source map＋D1 候選集」，不含簽章設定。bundle 的 22de5e4 已經是 scm-verified policy，不適合直接當 D1 Recovery。 |

`domain-memory/changes/CP-CORE-001/evidence-bundle.json` 內含 counterfactual 摘要（屬於 Change Package 本身），會跟著 Repo 進 `dlc-rec-d2`；`counterfactual/` 的原始輸出不會。

## 已知限制（照實告知學員）

- `record-approval` 只比對身分字串：proposer 字串完全相同才會被拒，同機雙身分仍可通過。治理強度來自「誰持有簽章私鑰」，不是 `record-approval`。
- 單機成對時，`--sign-every-commit` 讓夥伴的金鑰簽每一個 commit（含 proposer 的）；commit 作者可以是 proposer，但簽章者一定是持鑰夥伴。
- Plugin 以原始位元組計算引用雜湊。本 bundle 保留產製時起始 Repo 的原始位元組（23 個檔案 CRLF、其餘 LF；學員包的起始 Repo 之後已統一為 LF，重簽需要 Maintainer 私鑰，所以 bundle 未跟著改），本 bundle 的 Registry JSON 由 Plugin 0.2.2 在 Windows 寫出，是 CRLF（0.10.15 之後新寫的是 LF；兩者都能驗證）。本 Repo 以 `.gitattributes`（`* -text`）停用換行轉換，否則在 `core.autocrlf=true` 的機器上 clone 後引用會全部變成 changed。
- `scan-secrets` 掃的是工作目錄（含已忽略的資料夾）。金鑰放在 Repo 外的 `~/.dlc-keys/`（`%USERPROFILE%\.dlc-keys\`），所以 `scan-secrets` 預期 exit 0；不要把金鑰放進 Repo 內。
