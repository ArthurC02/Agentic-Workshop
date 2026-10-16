# Greenfield Speech 驗證紀錄

> 讀者：講者與維護者。時機：使用與修改 Deck 後。前置：已建置本階段 HTML 與操作講義。

驗證日期：2026-10-16（Asia/Taipei）。本輪範圍為 45 分鐘、21 頁的 Greenfield 講解 Deck；依 2026-10-16 使用者回饋（內容太少、多為回顧）改寫：約四分之一連回 Greenfield，其餘補上 Agentic 開發的原理、官方建議、應用提示詞與已查核的近期案例（Airbnb、Anthropic 遷移、Stripe、Spotify、GitHub、Stack Overflow、DORA）。

## 已執行

- `build_decks.py 01-greenfield` 與 `--check 01-greenfield`：HTML 與講義對應來源一致。
- `verify_browser.py 01-greenfield`（無頭 Chrome）：21 頁的內容、水平與舞台溢出量均為 0，無裁切元素；翻頁、備註、總覽、跳頁、計時、重設、複製與下載內容檢查通過。結果存於 [validation-evidence.json](validation-evidence.json)。
- 講義不含禁用標記或網址（以文字搜尋確認）。
- 人工核對事實與主課現行來源：四個 API、16 條規則、15 項驗收條件、11 個 TODO 標記、起始 1 通過 8 跳過、計畫固定 4 步、工作規則 7 條、驗收對照表欄位、變更審查四題、/docs 試用兩項、交付摘要七項。外部數字逐項對照 `docs/research/speech-agentic-sources.md` 的「已查核」項目，未查核與「不要宣稱」的說法未使用。

## 範圍與限制

示範提示詞未在本輪實際貼給 Agent 執行；驗收對照表畫面是示意。45 分鐘真人講解、投影現場、剪貼簿與下載政策需現場確認。

## 完成條件

技術建置與上述瀏覽器檢查通過，限制與實際範圍如實記錄；可開始內容審閱與現場演練。
