# 第三階段：Brownfield／Teammate 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：Brownfield（已有程式碼的既有專案）各段實作後的 45 分鐘講解。前置：學員做過個人 Agent 分析、共同脈絡、B1 與 B2（Brownfield 的第一、第二個變更任務）。

## 成品與操作

- `brownfield-deck.html`：19 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `brownfield-handout.md`：可提供學員的逐頁重點、示範指令與人工確認；不含講者備註。

本場講概念與技巧，不是重做任務：學員不讀程式、不打指令。投影片上的指令是示範用，講者可貼給自己的 Agent；沒有實際執行就說未驗證。不需要練習檔。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停全段計時。

主軸是 Tool（工具）→ Teammate（隊友）→ Digital Worker（數位員工）的第二步：人改成**核准計畫**，不再盯每一步。

| 技巧 | 本場 |
|---|---|
| 模型選擇／推論強度 | 分析段第一次介紹；B2 加深（比較調高、實作調回） |
| Token 節費 | 加深 02：先列目錄再挑檔、只要摘要、5 行摘要交接 |
| 結構化輸出 | 加深：分析固定標題、5 行摘要、B2 固定欄位比較表 |
| Skill（技能檔，簡化版） | 第一次介紹 `skills/team-rules.md`；B1 加深為做法 `skills/fix-bug-with-test.md` |

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–04 | 1–2 | 開場；Tool → Teammate：人核准計畫。 |
| 04–14 | 3–6 | 讀懂既有系統：先要地圖、模型選擇與推論強度、指名檔案、事實／假設／缺口。第 14 分鐘轉共同脈絡。 |
| 14–21 | 7–9 | 共同脈絡：比證據、寫成 `notes/shared-context.md`、Skill `skills/team-rules.md`。 |
| 21–31 | 10–13 | B1：用失敗測試找 Bug、核准小計畫、變更審查三題、做法存成 Skill。不講原因。 |
| 31–41 | 14–17 | B2：要 2–3 個方案、固定欄位比較表、推論強度切換、過時期待值須核准。不講計算結果。 |
| 41–45 | 18–19 | 每一步人判斷什麼；交給 04 Digital Worker。 |

時間不夠時，先縮第 5 頁（Token 節費）與第 16 頁（推論強度切換），兩頁都是加深，重點已在第 4 頁。

## 內容依據與邊界

- Runbook：個人 Agent 分析（`agentic-workshop/materials/participant-runbook/content/33-individual-analysis.md`）、共同脈絡（`agentic-workshop/materials/participant-runbook/content/39-shared-context.md`）、B1（`agentic-workshop/materials/participant-runbook/content/44-b1.md`）、B2（`agentic-workshop/materials/participant-runbook/content/52-b2.md`）、詞彙表（`agentic-workshop/materials/participant-runbook/content/88-glossary.md`）
- 學員資料：B0 系統概況（`agentic-workshop/03-brownfield/participant/01-system-context.md`）、B0 已知限制（`agentic-workshop/03-brownfield/participant/02-known-constraints.md`）、B1 任務卡（`agentic-workshop/03-brownfield/participant/task-cards/01-b1-student-fare-bug.md`）、B2 任務卡（`agentic-workshop/03-brownfield/participant/task-cards/02-b2-discount-policy-change.md`）
- 主持資料：B0 主持注意事項（`agentic-workshop/03-brownfield/facilitator/01-b0-facilitation-notes.md`）、預期學員行為（`agentic-workshop/03-brownfield/facilitator/07-expected-participant-behavior.md`）
- 技巧對照：course-authoring 技能的六技巧表與已查證出處清單

不揭露 B1 原因、B2 的優惠計算結果或任何過時測試的名稱與數值；只講找出它們的方法。比較表與審查題只示範格式。不教工作單、關卡或例外處理，那屬於 04 Digital Worker；最後一頁只留問題。

## 維護

從 Repo 根目錄執行：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py 03-brownfield
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check 03-brownfield
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py 03-brownfield
```

修改 `src/slides.json` 或 `src/stage.json` 後重建。Runbook 的檔名、檢查點或工作規則改動時，同步核對本簡報。

## 完成條件

19 頁與講義可重建，瀏覽器檢查無溢出；每頁有人工確認；講者備註與講義都不含任務答案。
