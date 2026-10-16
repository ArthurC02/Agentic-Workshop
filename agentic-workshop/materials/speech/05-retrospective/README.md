# 第五階段：Retrospective 回顧與組織導入講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：全部階段結束後的 25 分鐘概念講解。前置：聽眾聽過前四段，或手邊有自己的 `notes/` 與 `skills/` 紀錄。

## 成品與操作

- `retrospective-deck.html`：11 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `retrospective-handout.md`：可提供學員的逐頁重點與人工確認；不含講者備註。
- 無練習檔。第 6 頁的範例提示詞選用，貼給學員自己的 Coding Agent，現場不保證執行。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。

## 25 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–01 | 1 | 請聽眾選一件真實工作；不展開。 |
| 01–06 | 2–3 | 三種介入方式與選擇判準（風險、可逆性、證據）；口頭套用自己的工作。 |
| 06–09 | 4 | 六技巧簡短回顧，只談加深一層，不重教。 |
| 09–14 | 5–6 | 本段技巧：把重複做法寫成 Skill（技能檔，簡化版）；說明何時值得寫。 |
| 14–22 | 7–9 | 證據支持導入、量測口徑、先試哪裡；未量測就不報數字。 |
| 22–24 | 10 | 誠實的限制：只看證據的盲點與仍需人的事項。 |
| 24–25 | 11 | 系列收尾；每人寫下一項行動。 |

時間不足時省略第 4 頁，保留第 3、6、9 頁。

## 內容依據與邊界

- 回顧 Runbook（`agentic-workshop/materials/participant-runbook/content/80-retrospective.md`）
- 交付 Runbook（`agentic-workshop/materials/participant-runbook/content/70-delivery.md`）
- 我的提示詞清單（`agentic-workshop/05-retrospective/participant/reflection-sheet.md`）
- 詞彙表（`agentic-workshop/00-governance/glossary.md`）
- 組織導入討論提示（主持用）（`agentic-workshop/05-retrospective/facilitator/organization-adoption-prompts.md`）

只談概念與判斷，不含 B1 根因、B2 折扣順序、B3／SQLite 答案。本工作坊未量測效率或自主率，簡報不引用此類數字。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 05-retrospective
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 05-retrospective
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 05-retrospective
```

## 完成條件

11 頁與講義可重建；建置檢查與瀏覽器驗證通過；內容與主課程回顧、交付頁一致，無答案洩漏。25 分鐘為教學配置，實際時間需現場確認。
