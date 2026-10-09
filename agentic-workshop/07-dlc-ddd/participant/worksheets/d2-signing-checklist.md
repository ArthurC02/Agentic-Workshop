# D2 簽章流程與 Change Package 描述檔

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員與你們的 Agent。使用時機：D2（今天第二段）。提示詞在 Runbook（課堂操作手冊）的 D2 頁；這份是給 Agent 照著做的固定順序與描述檔格式，學員不用手填。

## 1. 固定順序（不能調換）

1. **夥伴**：`init-signing-key --sign-every-commit`。必須在**第一個**含 `domain-memory/` 的 commit 之前，否則之前的未簽章 commit 會讓 push 被拒。
2. **夥伴**：`amend-policy authorized_signers`（填金鑰指紋 fingerprint，辨識是哪一把金鑰，可公開）。先決定誰可以簽。
3. **夥伴**：`amend-policy review_trigger git-push`。再決定何時檢查：每次 push 時。
4. **夥伴**：`amend-policy review_mode scm-verified --verifier git-signed-commit`。最後才離開「只能草稿」模式，改成必須有 Git 簽章核准才能升級。
5. **夥伴**：`install-git-hitl-hook`（HITL＝Human-in-the-loop，人工把關；pre-push hook 是 push 前 Git 自動執行的檢查腳本），`governance-readiness` 回報 `ready` 才往下。
6. **提案者**：反事實檢查（counterfactual：故意改壞一處程式，確認測試會失敗；抓到就顯示 killed）→ `fill_package.py` → `submit-proposal`。變更審查包（Change Package）放在 `domain-memory/changes/<id>/`，不會動到已審查的內容。
7. **夥伴**：讀過審查包、回「核准」後，`record-approval` → `verify-proposal`。提案者不得核准自己的提案。
8. **夥伴**：簽章 commit → `write_scm_attestation.py` → `verify-git-governance`。簽章 commit 寫成核准證明（attestation），是外部可驗證的證據。
9. **提案者**：`finalize-proposal` → `apply-approved-updates` → `validate --require-reviewed` → `verify-audit`。只有核准且有簽章證據的提案能套用。
10. **夥伴**：簽章 commit 套用結果並 push；hook 會再檢查一次簽章。

核准、簽章、push 只在夥伴自己的 Agent 對話裡執行；提案者的 Agent 不碰 `.dlc-keys`。

## 2. Change Package 描述檔 `cp-d2.json`

提案者的 Agent 在 Repo 根目錄（`repository/smart-ticket-dlc-base/`）依下列格式建立 `cp-d2.json`，`〈 〉` 依 D1 的 Registry 與反事實結果填入。編號前綴：CP＝Change Package、REQ＝需求、AC＝驗收條件、OB＝obligation（要通過的檢查）、INV＝不變量。`promote` 要列出 Registry 的**全部**候選：`domain-memory/registry/` 底下每個有候選的 JSON 檔（`manifest.json` 除外）都要有一個同名的鍵。自己做的 D1 通常只有 `contexts`、`vocabulary`、`rules`；用過 D1 Recovery 的話，`aggregates`、`interactions`、`decisions` 也有候選，一樣要列。少列任何一個，`validate --require-reviewed`（檢查是否全部已審查）都會回報該筆「not reviewed」而不通過。

```json
{
  "package": "domain-memory/changes/CP-D2-001",
  "requirement_id": "REQ-D2-001",
  "proposal_id": "CP-D2-001",
  "proposer": "proposer@example.com",
  "intent": "把 D1 已檢查證據的候選升為 reviewed 事實",
  "acceptance_criteria": [
    {"id": "AC-D2-001", "statement": "〈一句可觀察的驗收條件〉", "test": "〈測試檔路徑〉", "expected": "passed"}
  ],
  "rules": [
    {"id": "〈規則 id〉", "test": "〈證明這條規則的測試檔路徑〉", "expected": "passed"},
    {"id": "〈規則 id〉", "test": "〈測試檔路徑〉", "expected": "passed"}
  ],
  "promote": {
    "contexts": ["〈context id〉", "〈context id〉"],
    "vocabulary": ["〈詞彙 id〉", "〈詞彙 id〉", "〈詞彙 id〉", "〈詞彙 id〉", "〈詞彙 id〉"],
    "rules": ["〈規則 id〉", "〈規則 id〉"],
    "aggregates": ["〈aggregate id；這個檔沒有候選就刪掉這一行〉"],
    "interactions": ["〈interaction id；沒有候選就刪掉這一行〉"],
    "decisions": ["〈decision id；沒有候選就刪掉這一行〉"]
  },
  "owner_context": "〈主要 context id〉",
  "invariant": "〈這次升級要守住的一條不變量〉",
  "design": {
    "domain_forces": ["〈為什麼現在要把這些事實定下來〉"],
    "decision": "只升級事實，不改程式",
    "invariants_preserved": ["〈規則 id〉"],
    "rejected_alternatives": ["〈例如：全部維持候選，Agent 繼續靠猜〉"],
    "counterfactual_check": "〈要改壞的保護與預期會失敗的測試〉"
  },
  "counterfactual": {"obligation_id": "OB-〈做過 counterfactual 的規則 id〉", "result_file": "cf-d2.json"}
}
```

- `test` 寫測試檔路徑（例如 `tests/integration/<檔名>.py`），工具會**實際執行**並記錄 exit code 與輸出雜湊；失敗就記 failed，不會幫你填 passed。
- 每條驗收條件與規則各產生一個 obligation，id 是 `OB-<原 id>`。
- `counterfactual.obligation_id` 必須是上面某條規則的 `OB-<規則 id>`。

## 3. `notes/d2.md` 要留下什麼

兩個 Agent 每做完一個檢查點，就用檢查點名稱當標題寫進 `notes/d2.md`。結束時應該看得到：fingerprint 前 12 碼（不含私鑰）、`governance-readiness` 結果、反事實的 verdict 與斷言、每個 obligation 的結果、夥伴的審查摘要與「核准／退回」決定、核准 commit 前 12 碼與簽章行、`validate --require-reviewed` 與 `verify-audit` 結果、push 結果。
