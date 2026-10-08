# D1 來源選擇表

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員。使用時機：D1 檢查點 1（D1–D4 是今天四段的代號；D3 再分 a、b、c 三張需求；步驟見 Runbook（課堂操作手冊） D1 頁），看完 `discover-sources` 輸出之後。

`discover-sources` 只列出「可能的來源」，不替你決定哪些可信。由你逐列判斷：這個路徑能不能當作 Domain Memory 的證據來源？選進來的路徑，之後每一條已審查（reviewed）事實都必須能在裡面找到證據。

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
2. 上表 4 個未分類的檔案建議選「否」：即使選入，`make_record.py` 也不接受拿它們當證據，引用它們的內容無法升為 reviewed。可引用的是 `docs/requirements/`、`docs/adr/`、`src/`，以及 `tests/` 底下的 `test_*.py`。
3. 選太廣的代價：之後只要有檔案新增或改名，來源就會被標為過期（stale），需要重新確認。

## 3. 確認

| 項目 | 內容 |
|---|---|
| 最後選入的路徑 | 〈列出〉 |
| 排除規則 | `**/__pycache__/**` |
| 確認人（`--confirmed-by`；固定的練習身分；名稱中的 DLC 指延伸課程，原指遊戲的追加內容，這裡指主課之後的加課） | `DLC Proposer <proposer@example.com>` |
| 確認時間 | 課程開始後第 〈 〉 分鐘 |
