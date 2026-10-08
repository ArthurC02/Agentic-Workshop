# D1 模型畫布：Context、詞彙與規則候選

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員。使用時機：D1 檢查點 3–6（D1–D4 是今天四段的代號；D3 再分 a、b、c 三張需求；檢查點步驟見 Runbook（課堂操作手冊） D1 頁），建立候選之前先在這裡寫下你的判斷。

候選（candidate）是「有證據的主張」，還不是事實。每一筆都要有至少一段 `路徑:起-迄` 證據（例如 `src/smart_ticket/domain/discounts.py:30-31`，表示該檔第 30 到 31 行），而且證據要落在你在來源選擇表確認過的路徑內：`docs/requirements/`、`docs/adr/`、`src/`，以及 `tests/` 底下的 `test_*.py`（`conftest.py` 不算）。數量下限：**詞彙 ≥ 5、Context ≥ 2、規則 ≥ 2**。

## 1. 先找矛盾，再寫定義

讀證據時，把下面這類情況記下來。它們是 Domain Memory 最有價值的地方，不要自己「修好」再寫進去：

- **同一件事兩個名字**：比對 `docs/adr/` 與 `src/smart_ticket/domain/` 裡計價相關的命名，文件說的名字在程式裡是不是同一個東西？
- **文件有、程式沒有**：在 `docs/requirements/business-rules.md` 與 ADR 裡出現的名詞，能不能在程式裡找到對應的類別或函式？（例如「Compensation／補償」）
- **邊界洩漏**：一個模組直接讀寫另一個模組該管的資料。

| 發現 | 證據 A（路徑:起-迄） | 證據 B（路徑:起-迄） | 你的處理（記為候選／記為未知／不建模） |
|---|---|---|---|
| 〈發現〉 | 〈 〉 | 〈 〉 | 〈 〉 |
| 〈發現〉 | 〈 〉 | 〈 〉 | 〈 〉 |

## 2. Context

| id（小寫、連字號，例如 `pricing`） | 名稱 | 職責（一句話，說它決定什麼） | 證據 |
|---|---|---|---|
| 〈id〉 | 〈名稱〉 | 〈職責〉 | 〈路徑:起-迄〉 |
| 〈id〉 | 〈名稱〉 | 〈職責〉 | 〈路徑:起-迄〉 |

## 3. 詞彙（Ubiquitous Language）

| id | 名稱 | 定義（一句寫錯就能被文件或程式指出來的明確定義） | 所屬 Context | 證據 |
|---|---|---|---|---|
| 〈id〉 | 〈名稱〉 | 〈定義〉 | 〈context id〉 | 〈路徑:起-迄〉 |
| 〈id〉 | 〈名稱〉 | 〈定義〉 | 〈context id〉 | 〈路徑:起-迄〉 |
| 〈id〉 | 〈名稱〉 | 〈定義〉 | 〈context id〉 | 〈路徑:起-迄〉 |
| 〈id〉 | 〈名稱〉 | 〈定義〉 | 〈context id〉 | 〈路徑:起-迄〉 |
| 〈id〉 | 〈名稱〉 | 〈定義〉 | 〈context id〉 | 〈路徑:起-迄〉 |

## 4. 規則

| id（沿用文件的規則編號，例如 `FARE-005`） | 敘述（寫成可以被測試推翻的句子） | 所屬 Context | 證據（規則文件＋測試或程式） |
|---|---|---|---|
| 〈規則 id〉 | 〈敘述〉 | 〈context id〉 | 〈路徑:起-迄〉、〈路徑:起-迄〉 |
| 〈規則 id〉 | 〈敘述〉 | 〈context id〉 | 〈路徑:起-迄〉、〈路徑:起-迄〉 |

## 5. 轉成批次檔 `d1-records.json`

在 Repo 根目錄（`repository/smart-ticket-dlc-base/`）建立 `d1-records.json`，把上面的表格逐列轉成下面的格式。**Context 放在最前面**，因為詞彙與規則會參照它。`evidence` 寫 `路徑:起-迄`，`make_record.py` 會替每一段呼叫 `cite`，記下那幾行內容的 SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同），之後內容被改就能發現。

```json
[
  {"asset": "contexts", "id": "〈context id〉", "name": "〈名稱〉", "responsibility": "〈職責〉",
   "evidence": ["〈路徑:起-迄〉"]},
  {"asset": "contexts", "id": "〈context id〉", "name": "〈名稱〉", "responsibility": "〈職責〉",
   "evidence": ["〈路徑:起-迄〉"]},
  {"asset": "vocabulary", "id": "〈詞彙 id〉", "name": "〈名稱〉", "definition": "〈定義〉",
   "context": "〈context id〉", "evidence": ["〈路徑:起-迄〉"]},
  {"asset": "rules", "id": "〈規則 id〉", "statement": "〈敘述〉",
   "context": "〈context id〉", "evidence": ["〈路徑:起-迄〉", "〈路徑:起-迄〉"]}
]
```

- 同義詞或「不是同一件事」可加欄位：`"synonyms": ["〈別名〉"]`、`"not_same_as": ["〈另一個詞彙 id〉"]`。
- 一個詞跨兩個 Context 時，`"context": ["〈id〉", "〈id〉"]`。
- 行號用編輯器左側的行號；證據段落越短越好，只框住支持這句話的那幾行。
