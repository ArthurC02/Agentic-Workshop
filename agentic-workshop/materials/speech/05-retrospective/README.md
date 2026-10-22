# 第五階段：Retrospective 回顧與組織導入講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：全部階段結束後的 25 分鐘概念講解。前置：聽眾聽過前四段，或手邊有自己的 `notes/` 與 `skills/` 紀錄。

本段只用一頁回顧，其餘講組織導入：用公開研究看清 AI 的效益與代價（DORA、METR、Faros AI、Stack Overflow）、怎麼量、從紀錄寫自己的 Skill、團隊規則的維護責任、認知債的團隊補法（後三者是前幾場的加深一層），最後排出 30 天導入計畫。

## 成品與操作

- `retrospective-deck.html`：14 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `retrospective-handout.md`：可提供學員的逐頁重點與人工確認；不含講者備註。
- 無練習檔。第 9 頁的範例提示詞選用，貼給學員自己的 Coding Agent，現場不保證執行。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。

## 25 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–03 | 1–2 | 請聽眾選一件真實工作；唯一的回顧頁：三種介入方式與 notes/、skills/ 紀錄。 |
| 03–07 | 3–4 | DORA 2025：回扣第一場的放大器結論；七項 AI 能力。 |
| 07–12.5 | 5–7 | METR 2025 研究與 2026 更新一起講；Faros AI 審查瓶頸；回扣第一場 Stack Overflow「差一點就對」，談量測要算驗證時間。 |
| 12.5–14.5 | 8 | 量什麼：先建基準；每項做法配它自己的領先與落後指標（照 playbook 原文），不量程式碼產出量。 |
| 14.5–18.5 | 9–10 | 從紀錄寫自己的 Skill（示範提示詞），改了就試跑（最小的評估）；團隊規則誰維護、多久修剪（加深一層）。 |
| 18.5–20 | 11 | 從哪一項開始：五項不用先做別的做法，各自的第一步；對應提示詞清單的「回到工作」。 |
| 20–21.5 | 12 | 風險：認知債的團隊補法（加深一層）。 |
| 21.5–25 | 13–14 | 30 天導入計畫（先只讀、再逐個環境放權）；每人寫下一項行動。 |

時間不足時第 4、7 頁各縮為 30 秒，保留第 5、6、8、11、13 頁。

## 內容依據與邊界

- 外部來源：`docs/research/speech-agentic-sources.md`「第五場」與「2026-10-22 AI-native SDLC 查核」段落（只用標為已查核的項目）。METR 兩份研究一定一起講，並說明時間點與限制；Faros AI、CodeRabbit 是廠商報告，備註已標限制。學員可見文字不放網址，引用格式為「📖 延伸閱讀：〈標題〉（發布者, 年份）」，只放在講者備註。
- 回顧 Runbook（`agentic-workshop/materials/participant-runbook/content/80-retrospective.md`）、交付 Runbook（`70-delivery.md`）、詞彙表（`agentic-workshop/00-governance/glossary.md`）、組織導入討論提示（主持用）（`agentic-workshop/05-retrospective/facilitator/organization-adoption-prompts.md`）。

只談概念與判斷，不含 B1 根因、B2 折扣順序、B3／SQLite 答案。簡報不把效率或自主率數字當成本課程的結果；外部案例數字一律註明是對方自稱，研究數字都註明出處。工具中立：規則檔與 Skill 以通用說法講，產品名只出現在來源。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 05-retrospective
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 05-retrospective
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 05-retrospective
```

## 完成條件

14 頁與講義可重建；建置檢查與瀏覽器驗證通過；內容與主課程回顧、交付頁一致，無答案洩漏。25 分鐘為教學配置，實際時間需現場確認。
