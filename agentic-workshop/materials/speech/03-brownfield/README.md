# 第三階段：Brownfield／Teammate 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：Brownfield（已有程式碼的既有專案）各段實作後的 45 分鐘講解。前置：學員做過個人 Agent 分析、共同脈絡、B1 與 B2（Brownfield 的第一、第二個變更任務）。

## 成品與操作

- `brownfield-deck.html`：18 頁、16:9、單檔離線簡報。以 Edge／Chrome 從本機開啟。
- `brownfield-handout.md`：可提供學員的逐頁重點、示範指令與人工確認；不含講者備註。

本場講概念與技巧，不是重做任務：學員不讀程式、不打指令。投影片上的指令是示範用，講者可貼給自己的 Agent；沒有實際執行就說未驗證。不需要練習檔。

方向鍵／Space 翻頁；O 總覽；N 顯示講者備註；F 全螢幕；T 開始／暫停全段計時。

主軸是 Tool（工具）→ Teammate（隊友）→ Digital Worker（數位員工）的第二步：人改成**核准計畫**，不再盯每一步。約四分之一連回剛才的分析、共同脈絡、B1、B2，其餘是新內容，每個要點附官方來源或有日期的公開案例。

| 技巧 | 本場 |
|---|---|
| 讀舊系統 | 把 Agent 當資深同事問；沒有出處的結論當假設；Spotify 背景 Agent 案例 |
| 模型選擇／推論強度 | 第一次介紹：按工作分工、推論強度是微調旋鈕、答不好時的排查順序 |
| 團隊規則 | 加深 02 的規則檔：進版本控制、六個面向、三層邊界 |
| Skill（技能檔） | 第一次介紹：開放格式、逐步揭露、何時寫、只裝信任來源 |
| 測試先行 | 先紅再綠、修根本原因；事前引導與事後感測 |
| 比較方案 | 加深結構化輸出：唯讀研究、可逆性欄位、人怎麼選 |
| 認知債 | 警示與補法：人要能說出改了什麼、為什麼 |

## 45 分鐘節奏

| 段落經過時間 | 頁面 | 重點與停止條件 |
|---|---|---|
| 00–02 | 1 | Tool → Teammate：人核准計畫；問「最不放心的那段」。 |
| 02–09 | 2–4 | 讀舊系統：問資深同事的問法、事實／假設／缺口、Spotify 案例。 |
| 09–15 | 5–7 | 模型分工、推論強度、答不好時先查四樣。 |
| 15–24 | 8–11 | 團隊規則與三層邊界、Skill 是什麼、何時寫 Skill。 |
| 24–31 | 12–13 | 先紅再綠；事前引導與事後感測。 |
| 31–36 | 14–15 | 比較方案（可逆性）；人怎麼選。 |
| 36–40 | 16 | 認知債；兩兩討論一分鐘。 |
| 40–45 | 17–18 | 人判斷的四件事；交給 04 Digital Worker。 |

時間不夠時，先縮第 4 頁（案例）與第 7 頁（排查順序），再縮第 11 頁。

## 內容依據與邊界

- Runbook：個人 Agent 分析（`agentic-workshop/materials/participant-runbook/content/33-individual-analysis.md`）、共同脈絡（`agentic-workshop/materials/participant-runbook/content/39-shared-context.md`）、B1（`agentic-workshop/materials/participant-runbook/content/44-b1.md`）、B2（`agentic-workshop/materials/participant-runbook/content/52-b2.md`）、詞彙表（`agentic-workshop/materials/participant-runbook/content/88-glossary.md`）
- 學員資料：B0 系統概況（`agentic-workshop/03-brownfield/participant/01-system-context.md`）、B0 已知限制（`agentic-workshop/03-brownfield/participant/02-known-constraints.md`）、B1 任務卡（`agentic-workshop/03-brownfield/participant/task-cards/01-b1-student-fare-bug.md`）、B2 任務卡（`agentic-workshop/03-brownfield/participant/task-cards/02-b2-discount-policy-change.md`）
- 主持資料：B0 主持注意事項（`agentic-workshop/03-brownfield/facilitator/01-b0-facilitation-notes.md`）、預期學員行為（`agentic-workshop/03-brownfield/facilitator/07-expected-participant-behavior.md`）
- 技巧對照：course-authoring 技能的六技巧表與已查證出處清單

外部來源只用 `docs/research/speech-agentic-sources.md` 第三場已查核的項目，避開「不要宣稱」清單；不寫模型名稱、預設值或價格。講者備註寫出處標題、發布者與日期，不放網址。

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

18 頁與講義可重建，瀏覽器檢查無溢出；每頁有人工確認；講者備註與講義都不含任務答案。
