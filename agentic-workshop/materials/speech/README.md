# Speech：概念與技術操作教學

> 目標讀者：講者與教材維護者。
> 使用時機：規劃各階段 Workshop 後的概念、技術講解與引導操作。
> 前置條件：閱讀既有 Workshop 任務與 `materials` 教材。

本資料夾存放 Speech 的內容規劃、操作指令、投影片原稿與講者備註。

## 教學方式

以學員實作為重點。每個主題提供操作步驟、可複製的 Agent 指令、預期產出與人工確認事項；概念搭配操作講解。

## 第一階段：Greenfield

從「Greenfield（從空資料夾開始的新專案）為什麼這麼順利？做了哪些準備？」出發，帶學員理解如何從空資料夾逐步建立開發依據：

1. 從空資料夾開始。
2. 將專案構想（Idea）相關文件放入 `docs/`。
3. 從文件細化 MVP（Minimum Viable Product，最小可行產品）各階段應有的工作項目。
4. 將工作項目轉為使用者故事（User Story）或使用案例（Use Case）。
5. 定義驗收條件（AC，Acceptance Criteria）。
6. 理解業務情境與流程（Business Flow）。
7. 使用 Gherkin（用 Given／When／Then 寫測試情境的格式）撰寫測試情境。
8. 設計分層式架構（依責任把程式分成幾層）。

第一階段採45分鐘完整操作與審查，詳見 [Greenfield操作說明](01-greenfield/README.md)。既有G0（Greenfield 起始包）作為回看準備工作的案例，再由學員在新目錄重建文件流程。

## 各階段獨立簡報（Deck）

主題中的 Tool → Teammate → Digital Worker，指 Agent 從工具、隊友到能獨立執行任務的數位員工。

| 存放位置 | 主題 | 狀態 |
|---|---|---|
| `01-greenfield/` | 從Idea到可開發專案；Greenfield／Tool | 本輪產製 |
| `02-time-skip/` | 系統演化與接手 | 預留，尚未產製 |
| `03-brownfield/` | 既有系統理解、共同背景與變更；Teammate | 預留，尚未產製 |
| `04-digital-worker/` | 工作授權、審查與治理；Digital Worker | 預留，尚未產製 |
| `05-retrospective/` | 回顧與組織導入 | 預留，尚未產製 |

每個階段使用各自的HTML與內容原稿；`shared/`存放共用呈現元件。後續各階段的內容與時間於產製時細化。

## 目前產出

第一階段提供單檔HTML、逐頁操作講義、Idea與Gherkin參考。`build_decks.py`目前只建置已完成內容的Greenfield，不自動產製後續階段。
