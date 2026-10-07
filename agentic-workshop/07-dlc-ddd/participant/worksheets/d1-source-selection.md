# D1 來源選擇表

> 讀者：DDD 延伸課程學員。使用時機：D1 檢查點 1，看完 `discover-sources` 輸出之後。

`discover-sources` 只列出「可能的來源」，不替你決定哪些可信。由你逐列判斷：這個路徑能不能當作 Domain Memory 的證據來源？選進來的路徑，之後每一條 reviewed 事實都必須能在裡面找到證據。

## 1. 逐列勾選

| 路徑 | `discover-sources` 的分類 | 選入？ | 理由（一句話） |
|---|---|---|---|
| `docs/requirements/` | requirements | 必選 | 產品規則與驗收條件 |
| `docs/adr/` | decisions | 必選 | 已核准的架構決策 |
| `src/` | implementation | 必選 | 目前實際執行的行為 |
| `tests/` | tests | 必選 | 哪些行為有被測試檢查 |
| `docs/architecture.md` | （未分類） | 〈是／否〉 | 〈理由〉 |
| `docs/api-examples.md` | （未分類） | 〈是／否〉 | 〈理由〉 |
| `docs/version-history.md` | （未分類） | 〈是／否〉 | 〈理由〉 |
| `README.md` | （未分類） | 〈是／否〉 | 〈理由〉 |

一律排除：`**/__pycache__/**`（執行測試後產生的快取檔，內容每次都會變）。`.venv/` 不是來源。

## 2. 判斷時問自己

1. 這份文件描述的是**應該怎樣**（規則）、**決定了什麼**（ADR），還是**現在實際怎樣**（程式、測試）？三者衝突時，你要記錄衝突，不是挑一個相信。
2. 未分類的檔案即使選入，引用它的證據之後也無法升為 reviewed，`make_record.py` 會直接拒絕引用它。可引用的是 `docs/requirements/`、`docs/adr/`、`src/`，以及 `tests/` 底下的 `test_*.py`。
3. 選太廣的代價：之後只要有檔案新增或改名，來源就會變成 stale，需要重新確認。

## 3. 確認

| 項目 | 內容 |
|---|---|
| 最後選入的路徑 | 〈列出〉 |
| 排除規則 | `**/__pycache__/**` |
| 確認人（`--confirmed-by`） | `DLC Proposer <proposer@example.com>` |
| 確認時間 | 第 〈 〉 分鐘 |
