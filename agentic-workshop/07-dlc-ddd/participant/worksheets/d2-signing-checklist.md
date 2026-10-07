# D2 簽章流程清單與 Change Package 描述檔

> 讀者：DDD 延伸課程學員。使用時機：D2 全程，依序打勾；指令在 Runbook 的 D2 頁。

## 1. 固定順序（不能調換）

| # | 步驟 | 誰做 | 為什麼是這個順序 | 完成 |
|---|---|---|---|---|
| 1 | `init-signing-key --sign-every-commit` | Maintainer | 必須在**第一個**含 `domain-memory/` 的 commit 之前；否則之前的未簽章 commit 會讓 push 被拒 | [ ] |
| 2 | `amend-policy authorized_signers`（填 fingerprint） | Maintainer | 先決定誰可以簽 | [ ] |
| 3 | `amend-policy review_trigger git-push` | Maintainer | 再決定何時檢查 | [ ] |
| 4 | `amend-policy review_mode scm-verified --verifier git-signed-commit` | Maintainer | 最後才離開「只能草稿」模式 | [ ] |
| 5 | `install-git-hitl-hook`，`governance-readiness` 回報 `ready` | Maintainer | 沒有 `ready` 不要往下 | [ ] |
| 6 | counterfactual → `fill_package.py` → `submit-proposal` | Proposer | 套件放在 `domain-memory/changes/<id>/`，簽章 commit 會碰到 Registry 路徑，但不改變 Registry digest | [ ] |
| 7 | `record-approval` → `verify-proposal` | Maintainer | Proposer 不得核准自己的提案 | [ ] |
| 8 | 簽章 commit → `write_scm_attestation.py` → `verify-git-governance` | Maintainer | 簽章是外部可驗證的證據 | [ ] |
| 9 | `finalize-proposal` → `apply-approved-updates` | Proposer | 只有核准且有簽章證據的提案能套用 | [ ] |
| 10 | `validate --require-reviewed`、`verify-audit`、push | 兩人一起看 | push 時 hook 會再檢查一次簽章 | [ ] |

## 2. Change Package 描述檔 `cp-d2.json`

在 Repo 根目錄建立 `cp-d2.json`。`〈 〉` 由 Proposer 填寫；`promote` 要列出 D1 的**全部**候選，否則 `validate --require-reviewed` 不會通過。

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
    "rules": ["〈規則 id〉", "〈規則 id〉"]
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

## 3. 收尾紀錄

| 項目 | 實際結果 |
|---|---|
| Maintainer fingerprint（只記前 12 碼） | `SHA256:〈 〉…` |
| `governance-readiness` | 〈ready／其他〉 |
| 核准 commit（前 12 碼） | 〈 〉 |
| `git log --show-signature -1` | 〈Good "git" signature for maintainer@example.com…〉 |
| `validate --require-reviewed` | 〈Registry is valid.／錯誤〉 |
| `verify-audit` | 〈status、events 數〉 |
| push | 〈成功／被拒，原因〉 |
