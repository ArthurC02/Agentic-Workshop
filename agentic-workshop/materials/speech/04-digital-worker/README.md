# 第四階段：Digital Worker 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：B3（Brownfield 最後一個大任務：團體訂票）與交付之後的 45 分鐘概念講解。前置：聽眾做過 B3（工作單＋三道 Gate）與交付，或手邊有自己的 `notes/b3.md`、`notes/delivery.md` 與 `skills/b3-work-order.md`。

Digital Worker（數位員工：在核准範圍內獨立完成整件任務的 Agent）。本段只用一頁回看 B3，其餘講業界怎麼安全地委派整件工作：委派與工作單、自主等級、核准關卡與核准疲勞、最小權限與沙箱、提示詞注入與供應鏈風險、例外與升級、評估產出、治理，以及大規模委派的真實案例。

## 成品與操作

- `digital-worker-deck.html`：21 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `digital-worker-handout.md`：可提供學員的逐頁重點與人工確認；不含講者備註。
- 無練習檔。第 4、10、16 頁的範例提示詞是選用示範，貼給學員自己的 Coding Agent；現場不保證執行，結果由學員檢查。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停計時。備註為同頁覆蓋，投影時關閉。

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–03 | 1–2 | 路線；唯一的 B3 回顧頁：授權、關卡、憑證據簽收。 |
| 03–07.5 | 3–4 | 從問答到交辦；好工作單回答五個問題（示範：先訪談再寫工作單）。 |
| 07.5–12.5 | 5–6 | 自主等級五級（人扮演的角色）；有效監督的實際使用數據。 |
| 12.5–16.5 | 7–8 | 關卡設在哪裡（需求確認、動手修改前、上線放行）；核准疲勞。 |
| 16.5–21.5 | 9–10 | 最小權限（OWASP Excessive Agency）；沙箱與平台護欄（示範：列出需要的權限）。 |
| 21.5–30 | 11–14 | Replit 刪庫事故、三缺一（提示詞注入）、Amazon Q 供應鏈事故、護欄做在平台。 |
| 30–36.5 | 15–17 | 例外與升級；寫的人不能核准自己（示範：只讀審查對話依審查準則寫審查紀錄）；要證據不要「已完成」。 |
| 36.5–43.5 | 18–20 | 留下紀錄與治理（每一步留一個檔案，下一步先讀它；出事時查得到誰核准了什麼）
；Stripe Minions；GitHub 的大數字怎麼讀（Spotify 只回扣第三場）。 |
| 43.5–45 | 21 | 委派前檢核卡；交接到 Speech 05。 |

時間不足時，第 8、14、17 頁各縮為 30 秒，第 20 頁只講 GitHub；保留第 5、7、9、11、12、19 頁。

## 內容依據與邊界

- 外部來源：`docs/research/speech-agentic-sources.md`「第四場」與「2026-10-22 AI-native SDLC 查核」段落（只用標為已查核的項目；數字照該文件，日期寫在備註）。學員可見文字不放網址，引用格式為「📖 延伸閱讀：〈標題〉（發布者, 年份）」，只放在講者備註。
- B3 與交付：Runbook `agentic-workshop/materials/participant-runbook/content/60-b3-overview.md`–`66-b3-exception-card.md`、`70-delivery.md`；Digital Worker 學員文件（`agentic-workshop/04-digital-worker/participant/`）。
- 主持文件（`agentic-workshop/04-digital-worker/facilitator/`）只用於節奏，不搬進學員可見文字。

邊界：工具中立，產品名只出現在案例與來源。不說出 B3 的實作做法與例外事件內容（含備註，因簡報可能給之後的學員看）。Escalation 六標題照來源原文。研究文件「不要宣稱」清單裡的數字（Stripe 每週 1,300 個、Spotify 10 天 1,000 個、Replit 4,000 筆假資料、Amazon Q 安裝數、OWASP Agentic 各項名稱）不上投影片。範例提示詞是示範，不屬於主課程步驟，未在本次產製中實際執行。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 04-digital-worker
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 04-digital-worker
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 04-digital-worker
```

修改 `src/slides.json` 的內容與備註後重建；版面溢出時刪減文字，不縮小樣式。主課程的 Escalation 格式變動時，同步第 15 頁；案例數字上台前依研究文件重新確認。

## 完成條件

21 頁與講義可重建並通過瀏覽器檢查；學員能說出工作單五部分、適合的自主等級、關卡設在哪、最小權限與三缺一、怎麼獨立評估交付，以及大規模案例共同的三層（隔離環境、自動驗證、人審）。45 分鐘為教學配置，實際節奏需現場確認。
