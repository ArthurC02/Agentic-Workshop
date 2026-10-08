# D1 來源選擇原則

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員與你的 Agent。使用時機：D1 檢查點 1（D1–D4 是今天四段的代號；步驟見 Runbook（課堂操作手冊）D1 頁）。Agent 執行 `discover-sources` 後依這些原則提出建議；選哪些由你回一句話決定，Agent 再把結果寫進 `notes/d1.md`（標題「來源決定」）。

`discover-sources` 只列出「可能的來源」，不替你決定哪些可信。選進來的路徑，之後每一條已審查（reviewed）事實都必須能在裡面找到證據。

## 建議

- **必選**：`docs/requirements/`（產品規則與驗收條件）、`docs/adr/`（已核准的架構決策）、`src/`（目前實際執行的行為）、`tests/`（哪些行為有被測試檢查；之後只有 `test_*.py` 能當證據）。
- **建議不選**：`docs/architecture.md`、`docs/api-examples.md`、`docs/version-history.md`、`README.md`、`notes/` 等未分類的檔案。即使選入，`make_record.py` 也不接受拿它們當證據，引用它們的內容無法升為 reviewed。
- **一律排除**：`**/__pycache__/**`（執行測試後產生的快取檔，內容每次都會變）。`.venv/` 不是來源。

## 判斷時問自己

1. 這份文件描述的是**應該怎樣**（規則）、**決定了什麼**（ADR），還是**現在實際怎樣**（程式、測試）？三者衝突時，要記錄衝突，不是挑一個相信。
2. 選太廣的代價：之後選入的路徑只要有檔案新增或改名，來源就會被標為過期（stale），需要重新確認。

## Agent 寫進紀錄的內容

最後選入的路徑、排除規則、沒選的路徑與一句理由、確認人（固定的練習身分 `DLC Proposer <proposer@example.com>`；名稱中的 DLC 指延伸課程，原指遊戲的追加內容，這裡指主課之後的加課）。
