# 第四階段：Digital Worker 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：B3（Brownfield 最後一個大任務：團體訂票）與交付之後的 45 分鐘概念講解。前置：聽眾做過 B3（工作單＋三道 Gate）與交付，或手邊有自己的 `notes/b3.md`、`notes/delivery.md` 與 `skills/b3-work-order.md`。

Digital Worker（數位員工：在核准範圍內獨立完成整件任務的 Agent）。本段主題是工作授權、審查與治理：人只在 Gate（核准關卡）介入。

## 成品與操作

- `digital-worker-deck.html`：19 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `digital-worker-handout.md`：可提供學員的逐頁重點與人工確認；不含講者備註。
- 無練習檔。第 18 頁的範例提示詞是選用示範，貼給學員自己的 Coding Agent；現場不保證執行，結果由學員檢查。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。備註為同頁覆蓋，投影時關閉。

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–01 | 1 | 路線；請聽眾選一件工作上的任務對照。 |
| 01–04 | 2 | Tool → Teammate → Digital Worker：差在人介入的方式；責任重新分配。 |
| 04–13.5 | 3–6 | 工作單：五部分放大到整件任務、授權範圍、停止條件與升級、存成 Skill（技能檔，簡化版；加深一層）。 |
| 13.5–25.5 | 7–11 | 三道 Gate：時間線、Gate 回報格式（結構化輸出，加深一層）、決策紀錄、Gate 1／Gate 2 人核對什麼。 |
| 25.5–31.5 | 12–13 | 例外事件 EXCEPTION-DW-001：只談判斷方法，不說出事件內容；有工作單與沒有工作單的對比討論。 |
| 31.5–36 | 14–15 | 放手執行與第 74 分停止擴充；何時停止、擴大範圍只能回到 Gate 2。 |
| 36–43.5 | 16–18 | Gate 3 變更審查三題、完成等級 Level 1–3、交付摘要即證據。 |
| 43.5–45 | 19 | 交接到 Speech 05 回顧。 |

時間不足時，第 13 頁討論縮為 1 分鐘、第 6 頁略過（Skill 與模型選擇已在前段講過），保留第 8、11、12、16、17 頁。

## 內容依據與邊界

- B3 流程 Runbook（`agentic-workshop/materials/participant-runbook/content/60-b3-overview.md`），以及 任務卡（`agentic-workshop/materials/participant-runbook/content/61-b3-task-card.md`）、操作規則（`agentic-workshop/materials/participant-runbook/content/62-b3-operating-rules.md`）、工作單（`agentic-workshop/materials/participant-runbook/content/63-b3-work-order.md`）、三道 Gate（`agentic-workshop/materials/participant-runbook/content/64-b3-approval-gates.md`）、交付審查檢核表（`agentic-workshop/materials/participant-runbook/content/65-b3-review-checklist.md`）、例外回應卡（`agentic-workshop/materials/participant-runbook/content/66-b3-exception-card.md`）
- 交付 Runbook（`agentic-workshop/materials/participant-runbook/content/70-delivery.md`）
- Digital Worker 學員文件（`agentic-workshop/04-digital-worker/participant/`）：操作規則、工作單、三道 Gate、交付審查檢核表、交付摘要範本、例外回應卡
- 主持文件（`agentic-workshop/04-digital-worker/facilitator/`）：只用於節奏與觀察重點，不搬進學員可見文字
- Acceptance Gates（`agentic-workshop/00-governance/acceptance-gates.md`）、詞彙表（`agentic-workshop/00-governance/glossary.md`）

邊界：Gate 時間（66／69／75，另有 63／70／74／76）、例外編號 EXCEPTION-DW-001、Level 1–3 文字、Gate 回報格式與 Escalation 六標題都照來源原文，不改寫。不說出 B3 的實作做法與例外事件內容（含備註，因簡報可能給之後的學員看）。模型選擇與 Skill 已在 Speech 03 教過，這裡只加深。第 18 頁提示詞是示範，不屬於主課程步驟，未在本次產製中實際執行。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 04-digital-worker
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 04-digital-worker
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 04-digital-worker
```

修改 `src/slides.json` 的內容與備註後重建；版面溢出時刪減文字，不縮小樣式。主課程的 Gate 時間、例外卡或 Level 文字變動時，同步本簡報第 7、12、17 頁。

## 完成條件

19 頁與講義可重建並通過瀏覽器檢查；學員能說出工作單的五部分與授權邊界、每道 Gate 核對什麼、例外怎麼判斷範圍、交付憑哪些證據選完成等級。45 分鐘為教學配置，實際節奏需現場確認。
