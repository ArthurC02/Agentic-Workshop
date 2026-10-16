# 第二階段：Time Skip 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：Time Skip（時間快轉：專案假設已開發一段時間）後的 25 分鐘觀念與技巧講解。前置：學員已聽過 Greenfield 講解，備妥通用 Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）。

## 成品與操作

- `time-skip-deck.html`：11 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `time-skip-handout.md`：可提供學員的逐頁摘要與人工確認；不含講者備註。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。本段偏重觀念與技巧，不要求學員寫程式或打指令；提示詞頁僅供示範，未實際執行的結果一律說「未驗證」。

本段首次介紹 Token 節費（開新對話、指名要讀的檔、用摘要代替重讀、留交接檔）；深化 Greenfield 已教的提示詞結構（背景・要讀的檔）。不教模型選擇、共同脈絡與 Skill（技能檔），這些屬於 03 Brownfield。

## 25 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–04 | 1–2 | Time Skip 是什麼、12 個月後的成長；說出一件最不確定的事就轉場。 |
| 04–08 | 3–4 | 換專案開新對話；Token 是什麼、四個省法。 |
| 08–11 | 5 | 指名要讀的檔，並請 Agent 列出沒讀的部分。 |
| 11–13 | 6 | 貼工作規則與背景，請 Agent 複述，確認三個重點。 |
| 13–16 | 7 | 不信舊記憶：程式、測試、規則三方對照。 |
| 16–18 | 8 | 記下起點（版本、測試數字、版本紀錄）。 |
| 18–23 | 9–10 | 交接檔的內容；人要查數字依據、範圍、缺口。 |
| 23–25 | 11 | 帶走四個做法，銜接 03 Brownfield／Teammate。 |

時間不足時先砍第 8 頁示範，保留第 7、9、10 頁。

## 內容依據與邊界

- Runbook：Time Skip：12 個月後（`agentic-workshop/materials/participant-runbook/content/30-time-skip.md`）
- 時間快轉公告（`agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md`）
- 公司與系統成長摘要（`agentic-workshop/02-time-skip/participant/02-company-growth-summary.md`）
- Brownfield 接手說明（`agentic-workshop/02-time-skip/participant/03-brownfield-handover.md`）
- 詞彙表（`agentic-workshop/00-governance/glossary.md`）（交接資訊）

只講公開的成長背景，不提任何失敗原因、修正方式或後續任務解法。簡報未實測 B0（剛接手、已上線的既有程式）；數字範例只示範格式。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 02-time-skip
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 02-time-skip
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 02-time-skip
```

修改 `src/slides.json` 後重建；溢出時刪減文字，不縮小版型。

## 完成條件

11 頁與講義可重建、檢查與瀏覽器驗證通過；節奏合計 25 分鐘；最後一頁銜接 03 Brownfield／Teammate。
