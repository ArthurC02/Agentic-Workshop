# 第一階段：Greenfield 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：主課 Greenfield（從頭開始的新專案，第 07–29 分鐘）之後的 45 分鐘講解。前置：學員已體驗 G0（Greenfield 起始程式包）；講者備妥 G0 資料夾與通用 Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）供示範。

## 成品與操作

- `greenfield-deck.html`：20 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `greenfield-handout.md`：可提供學員的逐頁重點、示範提示詞與人工確認；不含講者備註。
- `practice/idea.md`：示範「構想放入 docs」時使用的需求摘要（取自 Greenfield 需求、驗收條件與 G1）。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停全段計時。重設按鈕清除計時。備註為同頁覆蓋，投影時關閉。底部提供 Idea 範例與操作講義下載；提示詞頁可複製。若瀏覽器禁止剪貼簿，會選取文字供手動複製；禁止下載時由講者提供對應檔案。

本場講概念與 Agentic 開發技巧，不是實作課：學員不寫、不讀程式，也不打指令。頁面上的提示詞由講者示範，學員可選擇貼給自己的 Agent。

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–07 | 1–3 | 回看準備：G0 先備好了什麼；Tool＝人一步一步介入。第 7 分鐘前收齊白板上的卡點。 |
| 07–13 | 4–6 | 準備工作鏈總覽、構想與來源、MVP（最小可行產品）範圍。只講人判斷什麼，不現場建資料夾。 |
| 13–22 | 7–10 | 使用者故事／使用案例、驗收條件、業務流程；第 20–22 分鐘兩人討論，時間到就收。 |
| 22–26 | 11–12 | Gherkin 情境與分層架構：情境如何追回驗收條件、架構如何變成工作規則。 |
| 26–34 | 13–15 | 工作規則、五段式提示詞、小步放行。 |
| 34–41 | 16–18 | 驗收對照表（結構化輸出）、變更審查四題、在 /docs 親自試用。 |
| 41–45 | 19–20 | notes/ 紀錄與交付摘要；交棒 Speech 02 Time Skip。第 45 分鐘結束，不延長。 |

時間不夠時，第 10 頁討論改為講者念三題、不分組；第 5、8 頁的示範提示詞可只口述。

## 內容依據與邊界

- Greenfield Runbook（`agentic-workshop/materials/participant-runbook/content/10-greenfield.md`）：工作規則、計畫提示詞（五段式）、驗收對照表、變更審查四題、/docs 試用與 `notes/greenfield.md` 段落。
- Greenfield 回顧與交付決定（`agentic-workshop/materials/participant-runbook/content/15-gf-submission.md`）
- 歡迎與使用方式（`agentic-workshop/materials/participant-runbook/content/00-welcome.md`）：Tool → Teammate → Digital Worker。
- Greenfield 需求（`agentic-workshop/01-greenfield/participant/02-business-requirements.md`）、驗收條件（`agentic-workshop/01-greenfield/participant/03-acceptance-criteria.md`）、Agent 操作指南（`agentic-workshop/01-greenfield/participant/04-agent-usage-guide.md`）、提交清單（`agentic-workshop/01-greenfield/participant/05-submission-checklist.md`）
- G0 架構（`agentic-workshop/01-greenfield/participant/starter-repository/docs/architecture.md`）
- 引用書目僅用 `.claude/skills/course-authoring/references.md` 已列標題，寫在講者備註。

本場第一次介紹：Tool 階段、工作規則、五段式提示詞、結構化輸出（驗收對照表）、變更審查、notes/ 決策紀錄。只預告、不教：開新對話與交接檔（Speech 02）、模型選擇與推論強度、共用規則檔（Speech 03）、核准關卡（Speech 04）。

準備工作鏈中的使用者故事、業務流程與 Gherkin 在主課沒有獨立檔案；本場說明新專案沒有這些文件時如何請 Agent 補上，不宣稱主課做過。驗收對照表畫面是示意，不是實際輸出。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 01-greenfield
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 01-greenfield
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 01-greenfield
```

修改 `src/slides.json` 的內容與備註後重建；`../shared/` 的版型不在本資料夾維護。主課 Greenfield 的工作規則、提示詞或 `notes/` 段落改動時，同步第 13–19 頁與備註。溢出時刪字，不縮小字級。

## 完成條件

20 頁與講義可重建、`--check` 通過、瀏覽器檢查無溢出或裁切；每頁的人工確認都說得出人判斷什麼；事實與主課 Greenfield 現行來源一致。45 分鐘為教學配置，實際節奏需現場確認。
