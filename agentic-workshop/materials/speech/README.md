# Speech：概念與 Agentic 開發技巧講解

> 目標讀者：講者與教材維護者。
> 使用時機：各階段 Workshop 之後，講解該階段背後的概念與 Agentic 開發技巧。
> 前置條件：閱讀既有 Workshop 任務與 `materials` 教材。

本資料夾存放五場獨立講解的投影片原稿、講者備註與學員講義。

## 教學方式

以概念和 Agentic 開發技巧為主：說明為什麼這樣問 Agent、什麼時候用、人要判斷什麼。學員不寫程式、不讀程式、不打指令；頁面上的提示詞是示範，學員想試再貼給自己的 Agent，沒有實際執行的結果一律視為未驗證。

五場依 Tool → Teammate → Digital Worker 推進，這三個階段的差別是人介入的方式：逐步確認、核准計畫、只在 Gate（關卡）決策。每個技巧只在第一次需要時講一次，之後的場次只加深。

## 五場講解

| 存放位置 | 主題 | 長度 | 頁數 | 第一次講的技巧 |
|---|---|---|---|---|
| `01-greenfield/` | 從 Idea 到可開發的專案；Tool | 45 分鐘 | 20 | 工作規則、五段式提示詞、小步放行、驗收對照表（Structured Output，結構化輸出）、變更審查 |
| `02-time-skip/` | 系統演化與接手 | 25 分鐘 | 11 | Token 節費、交接檔 |
| `03-brownfield/` | 既有系統理解、共同脈絡與變更；Teammate | 45 分鐘 | 19 | 模型選擇與推論強度、團隊規則 Skill |
| `04-digital-worker/` | 工作授權、審查與治理；Digital Worker | 45 分鐘 | 19 | Work Order（工作單）、Gate 決策、例外處理（加深前面技巧） |
| `05-retrospective/` | 回顧與組織導入 | 25 分鐘 | 11 | 寫自己的 Skill |

各場的節奏、內容依據與邊界見該資料夾的 `README.md`。

## 建置與檢查

從 Repo 根目錄執行；不帶資料夾名稱時處理全部五場：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py [01-greenfield …]
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py [01-greenfield …]
```

每場的來源是 `src/stage.json`（標題、長度、輸出檔名、講義開頭與完成條件、可下載檔）與 `src/slides.json`（逐頁內容與講者備註）；`shared/` 是共用版型。建置產生單檔離線 HTML（`*-deck.html`）與不含講者備註的講義（`*-handout.md`），兩者都不要手改。DLC 的四場講解（`materials-dlc/speech/`）共用同一套腳本與版型，不帶資料夾名稱時一併處理。`verify_browser.py` 以無頭瀏覽器逐頁檢查溢出與裁切，並測試翻頁、備註、計時、複製與下載。發布時由 `release-materials` 一併執行。
