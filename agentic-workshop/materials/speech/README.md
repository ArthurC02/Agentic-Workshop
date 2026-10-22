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
| `01-greenfield/` | 從 Idea 到可開發的專案；Tool | 45 分鐘 | 21 | 先給可執行的檢查、規格驅動與驗收條件、脈絡工程、工作規則、五段式提示詞、先計畫、小步驗證、結構化輸出（驗收對照表）、看證據審查變更 |
| `02-time-skip/` | 系統演化與接手；脈絡管理 | 25 分鐘 | 12 | 脈絡視窗與脈絡劣化、Token 成本、子 Agent 摘要、何時重開、壓縮與交接檔、規則檔（AGENTS.md）與規則檔膨脹 |
| `03-brownfield/` | 既有系統理解、共同脈絡與變更；Teammate | 45 分鐘 | 18 | 讓 Agent 帶讀舊系統、模型選擇與推論強度、團隊規則與三層邊界、Skill（開放格式）、測試先行、事前引導與事後感測、比較方案與可逆性、認知債（附 Spotify 案例） |
| `04-digital-worker/` | 工作授權、審查與治理；Digital Worker | 45 分鐘 | 21 | Work Order（工作單）、自主等級、核准關卡與上線放行、最小權限與沙箱、提示詞注入防護、寫的人不核准自己（審查準則、審查紀錄）、每一步留下紀錄（下一步先讀它，出事時查得到誰核准了什麼）（附 Stripe、GitHub 案例） |
| `05-retrospective/` | 回顧與組織導入 | 25 分鐘 | 14 | 量測成效（DORA 能力模型、METR、Faros AI 等研究）、每項做法自己的領先與落後指標、評估（改了設定就試跑）、從五項不用先做別的做法開始、
先只讀再逐個環境放權的 30 天導入計畫；Skill、團隊規則與認知債只加深一層 |

各場的節奏、內容依據與邊界見該資料夾的 `README.md`。

## 建置與檢查

從 Repo 根目錄執行；不帶資料夾名稱時處理全部五場：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py [01-greenfield …]
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py [01-greenfield …]
```

每場的來源是 `src/stage.json`（標題、長度、輸出檔名、講義開頭與完成條件、可下載檔）與 `src/slides.json`（逐頁內容與講者備註）；`shared/` 是共用版型。建置產生單檔離線 HTML（`*-deck.html`）與不含講者備註的講義（`*-handout.md`），兩者都不要手改。DLC 的四場講解（`materials-dlc/speech/`）共用同一套腳本與版型，不帶資料夾名稱時一併處理。`verify_browser.py` 以無頭瀏覽器逐頁檢查溢出與裁切，並測試翻頁、備註、計時、複製與下載。發布時由 `release-materials` 一併執行。
