# 第一階段：Greenfield 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：主課 Greenfield（從頭開始的新專案，第 07–29 分鐘）之後的 45 分鐘講解。前置：學員已體驗 G0（Greenfield 起始程式包）；講者備妥 G0 資料夾與通用 Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）供示範。

## 成品與操作

- `greenfield-deck.html`：21 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `greenfield-handout.md`：可提供學員的逐頁重點、示範提示詞、人工確認與延伸閱讀標題；不含講者備註。
- `practice/idea.md`：示範「請 Agent 訪談你、寫短規格」時使用的需求摘要（取自 Greenfield 需求、驗收條件與 G1）。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停全段計時。重設按鈕清除計時。備註為同頁覆蓋，投影時關閉。底部提供 Idea 範例與操作講義下載；提示詞頁可複製。若瀏覽器禁止剪貼簿，會選取文字供手動複製；禁止下載時由講者提供對應檔案。

本場講概念與 Agentic 開發技巧，不是實作課：學員不寫、不讀程式，也不打指令。頁面上的提示詞由講者示範，學員可選擇貼給自己的 Agent。約四分之一連回剛才的 Greenfield，其餘是做法背後的原理、官方建議、怎麼用在自己的工作，以及有日期與數字的業界案例。

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–04 | 1–2 | 剛才順利的原因、本場三個問題；Tool＝人一步一步介入。第 4 分鐘前收齊白板上的卡點。 |
| 04–12 | 3–6 | Agent 怎麼知道做對了：Agent 迴圈與真實結果、先給可執行的檢查（示範）、可判定的驗收條件、Given／When／Then。 |
| 12–25 | 7–12 | Agent 怎麼知道要做什麼：規格驅動開發三種深度、請 Agent 訪談你寫短規格（示範）、Airbnb 案例、脈絡工程、工作規則、五段式提示詞。 |
| 25–35 | 13–16 | 人怎麼確認：先探索再計畫（示範）、小步驗證與大型遷移案例、結構化輸出、看證據審查變更（示範）。 |
| 35–39 | 17–18 | 業界現況：大規模案例的共同點（數字與細節留到 Speech 03、04）；平衡提醒（Stack Overflow 調查、DORA 報告）。 |
| 39–45 | 19–21 | 決定寫進 notes/；兩人討論「交辦前的五個問題」3 分鐘；交棒 Speech 02 Time Skip。第 45 分鐘結束，不延長。 |

時間不夠時：第 20 頁討論改為講者用一個學員的例子帶過；第 4、13、16 頁的示範提示詞只口述，第 8 頁保留示範。

## 內容依據與邊界

- 主課事實：Greenfield Runbook（`agentic-workshop/materials/participant-runbook/content/10-greenfield.md`：`AGENTS.md`（怎麼跑＋工作規則 8 條，範本在 `01-greenfield/participant/04-agent-usage-guide.md`）、check Skill、計畫提示詞、驗收對照表、變更審查、/docs 試用、`notes/greenfield.md`）、`15-gf-submission.md`、`00-welcome.md`（Tool → Teammate → Digital Worker）、Greenfield 需求與驗收條件（`agentic-workshop/01-greenfield/participant/02-business-requirements.md`、`03-acceptance-criteria.md`）、G0 架構（`starter-repository/docs/architecture.md`）。
- 外部論點與案例：只用 `docs/research/speech-agentic-sources.md` 第一場與相關場次標為「已查核」的項目；「不要宣稱」清單中的說法一律不用。Airbnb 原頁面沒有日期，投影片不寫年份；Anthropic 遷移案例是廠商自家案例，備註要說明。
- 學員看得到的文字（標題、內文、卡片、提示詞、人工確認）不放網址；延伸閱讀寫成「📖 延伸閱讀」卡片，只列〈標題〉（發布者，年份）。講者備註可寫發布者、日期與論點，同樣不放網址。
- 工具中立：先講做法，產品只當例子（例如規則檔 AGENTS.md、CLAUDE.md、GEMINI.md）；不寫死模型名稱、價格或預設推論強度。

本場第一次介紹：Tool 階段、Agent 迴圈、先給可執行的檢查、規格驅動開發、脈絡工程、工作規則、交辦式提示詞、先探索再計畫、小步驗證、結構化輸出（驗收對照表）、看證據審查、notes/ 決策紀錄。只預告、不教：Context Window 與開新對話、交接檔（Speech 02）、模型選擇與推論強度、共用規則檔（Speech 03）、核准關卡與權限（Speech 04）、量測成效（Speech 05）。

使用者故事、業務流程與 Gherkin 在主課沒有獨立檔案；本場說明怎麼請 Agent 補上，不宣稱主課做過。驗收對照表畫面是示意，不是實際輸出。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 01-greenfield
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 01-greenfield
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 01-greenfield
```

修改 `src/slides.json` 的內容與備註後重建；`../shared/` 的版型不在本資料夾維護。主課 Greenfield 的工作規則、提示詞或 `notes/` 段落改動時，同步第 1、5、11、12、15、16、19 頁與備註。案例數字以研究文件的查核日為準，上台前若引用工具文件，重新確認一次。溢出時刪字，不縮小字級。

## 完成條件

21 頁與講義可重建、`--check` 通過、瀏覽器檢查無溢出或裁切；每頁的人工確認都說得出人判斷什麼；事實與主課 Greenfield 現行來源一致，外部數字都來自已查核項目。45 分鐘為教學配置，實際節奏需現場確認。
