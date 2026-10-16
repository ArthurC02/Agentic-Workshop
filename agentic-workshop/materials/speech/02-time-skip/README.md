# 第二階段：Time Skip 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：Time Skip（時間快轉：專案假設已開發一段時間）後的 25 分鐘觀念與技巧講解。前置：學員已聽過 Greenfield 講解，備妥通用 Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）。

## 成品與操作

- `time-skip-deck.html`：12 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `time-skip-handout.md`：可提供學員的逐頁摘要與人工確認；不含講者備註。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。本段偏重觀念與技巧，不要求學員寫程式或打指令；提示詞頁僅供示範，未實際執行的結果一律說「未驗證」。

本段講脈絡管理的原理與做法，約四分之一連回剛才的 Time Skip，其餘是新內容：脈絡視窗與脈絡劣化、Token 成本、子 Agent 摘要、何時重開、壓縮、交接檔、規則檔（AGENTS.md 等）與規則檔膨脹。每個要點附官方來源與有日期的公開案例。不教模型選擇、團隊規則的維護方式與 Skill（技能檔），這些屬於 03 Brownfield。

## 25 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–01.5 | 1 | 連回剛才：為什麼 Agent 會「越聊越笨」；請兩三人舉例。 |
| 01.5–05.5 | 2–3 | 脈絡視窗是工作桌；脈絡劣化與「少而準」。 |
| 05.5–09.5 | 4–5 | Token 成本跟著脈絡變大；大量讀檔交給子 Agent 或另一個對話摘要。 |
| 09.5–14 | 6–7 | 糾正兩次就重開（示範重開用的提示詞）；壓縮的好處與代價。 |
| 14–18.5 | 8–9 | 交接檔欄位與人要查的三件事；兩個長任務案例與平衡提醒。 |
| 18.5–23.5 | 10–11 | 規則檔（AGENTS.md 開放慣例）是脈絡不是開關；規則檔要短（示範逐行審查提示詞）。 |
| 23.5–25 | 12 | 五個習慣，銜接 03 Brownfield／Teammate。 |

時間不足時先砍第 9 頁案例（重點已在第 8 頁），再縮第 5 頁示範。

## 內容依據與邊界

- Runbook：Time Skip：12 個月後（`agentic-workshop/materials/participant-runbook/content/30-time-skip.md`）
- 時間快轉公告（`agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md`）
- 公司與系統成長摘要（`agentic-workshop/02-time-skip/participant/02-company-growth-summary.md`）
- Brownfield 接手說明（`agentic-workshop/02-time-skip/participant/03-brownfield-handover.md`）
- 詞彙表（`agentic-workshop/00-governance/glossary.md`）（交接資訊）

只講公開的成長背景，不提任何失敗原因、修正方式或後續任務解法。簡報未實測 B0（剛接手、已上線的既有程式）；示範提示詞沒有實際執行就說未驗證。

外部來源只用 `docs/research/speech-agentic-sources.md` 第二場已查核的項目，以及其中「不要宣稱」清單以外的說法；講者備註寫出處標題、發布者與日期，不放網址。成本數字只講量級並註明會變；不寫模型名稱或價格。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 02-time-skip
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 02-time-skip
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 02-time-skip
```

修改 `src/slides.json` 後重建；溢出時刪減文字，不縮小版型。

## 完成條件

12 頁與講義可重建、檢查與瀏覽器驗證通過；節奏合計 25 分鐘；最後一頁銜接 03 Brownfield／Teammate。
