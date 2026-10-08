# D1 候選紀錄格式：Context、詞彙與規則

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員與你的 Agent。使用時機：D1 檢查點 3–6（D1–D4 是今天四段的代號；步驟見 Runbook（課堂操作手冊）D1 頁）。Agent 提草稿與證據，你回一句話決定；Agent 再依這裡的格式寫紀錄。格式已寫在 Runbook 的提示詞裡，不用另外貼。

候選（candidate）是「有證據的主張」，還不是事實。每一筆都要有至少一段 `路徑:起-迄` 證據（例如 `src/smart_ticket/domain/discounts.py:30-31`，表示該檔第 30 到 31 行），而且證據要落在已確認的來源內：`docs/requirements/`、`docs/adr/`、`src/`，以及 `tests/` 底下的 `test_*.py`（`conftest.py` 不算）。數量下限：**詞彙 ≥ 5、Context ≥ 2、規則 ≥ 2**。

## 要 Agent 先找的三種情況

它們是 Domain Memory 最有價值的地方，不要讓 Agent 自己「修好」再寫進去：

- **同一件事兩個名字**：文件說的名字，在程式裡是不是同一個東西？
- **文件有、程式沒有**：需求文件或 ADR 裡的名詞，在程式裡找不到對應的類別或函式。
- **邊界洩漏**：一個模組直接讀寫另一個模組該管的資料。

處理方式由你選：記成兩個詞並互標「不是同一件事」（`not_same_as`）、記成同一個詞的別名（`synonyms`），或先記為未知、不建模。

## `notes/d1.md`（Agent 寫）

依檢查點分段：來源決定、初始化與確認來源、詞彙（採用的定義、沒採用的候選與理由、名稱矛盾與處理）、Context 與規則（含缺口）、缺口與查詢、Context 與邊界（含 D1 總結）。

## `d1-records.json`（Agent 寫，放在 Repo 根目錄）

一個 JSON 陣列，**Context 放在最前面**，因為詞彙與規則會參照它。`make_record.py` 會替每一段 `evidence` 呼叫 `cite`，記下那幾行內容的 SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同），之後內容被改就能發現。

```json
[
  {"asset": "contexts", "id": "pricing", "name": "計價", "responsibility": "決定每位旅客的票價與適用優惠",
   "evidence": ["src/smart_ticket/domain/discounts.py:30-31"]},
  {"asset": "vocabulary", "id": "advance-purchase-discount", "name": "提前購票優惠",
   "definition": "購票日至出發日至少 14 天時的 85% 票價資格",
   "context": "pricing", "evidence": ["docs/requirements/business-rules.md:29-30"]},
  {"asset": "rules", "id": "FARE-005", "statement": "購票日至出發日至少 14 天才有 85% 提前購票資格",
   "context": "pricing", "evidence": ["docs/requirements/business-rules.md:29-30", "src/smart_ticket/domain/discounts.py:30-31"]}
]
```

- 同義詞或「不是同一件事」可加欄位：`"synonyms": ["別名"]`、`"not_same_as": ["另一個詞彙 id"]`。
- 一個詞跨兩個 Context 時：`"context": ["pricing", "booking"]`。
- 證據段落越短越好，只框住支持這句話的那幾行。上例取自輔助工具說明，行號以實際檔案為準。
