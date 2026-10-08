# 主持簡報與學員 Runbook 產製指令書（P12）

> 讀者：產製主持簡報、學員 Runbook 與其建置工具的 Coding Agent，以及驗收者。
> 時機：P11 受控候選包與 09 一致性修正完成之後，真人演練之前。
> 前置：00 總控、05、06、07、08、09 指令書；`agentic-workshop/` 現行素材；最新受控候選包 `dist/p11-candidate/f6127e67546395c5/`；[D-07](../planning/decisions-and-open-issues.md)。

## 1. 已核准變更（2026-10-05，使用者於對話中核准）

1. 成品放在 `agentic-workshop/materials/`，只存本機，不發布到外部平台。
2. 學員只發一次檔案：單一 `runbook.html`。G0 Starter 與 B0 Repository 以 ZIP 形式內嵌在 Runbook 中供下載。
3. 分批揭露改以「編碼隱藏＋寫死解鎖碼」落實：鎖定章節在 HTML 原始碼中不出現明文，學員輸入主持人在揭露時點公布的解鎖碼後才解開。此機制只防隨手偷看，不是密碼學保護。
4. 標準答案只放在主持簡報，於各段時間截止後揭曉；Runbook 不含 Evaluation 原稿；僅允許本輪補充的受控 Recovery 接續基線。
5. 視覺參考台北富邦銀行官網的配色與元件風格，不使用標誌、行名或品牌圖像。

以上取代 D-04 中「學員多包分批發放」的實體形式，不改變任何商業規則、時程、版本或測試期待值。

2026-10-09 已核准變更：Runbook 改為「技巧優先，紀錄交給 Agent」。每個檢查點是可複製的提示詞，指令由 Agent 執行；分析、計畫、審查與交付紀錄由 Agent 寫進 `notes/*.md`、`skills/*.md`；表單每段最多一張、以下拉／勾選為主。詳見 [00 總控指令書 §1](00_Agentic工作坊素材產製總控指令書.md#1-專案目標)；下方第 3、5 節已依此更新。

## 2. 產出

| 位置 | 內容 | 受眾 |
|---|---|---|
| `agentic-workshop/materials/README.md` | 使用方式、建置指令、解鎖碼清單位置、Preflight 補充項 | 主持人／維護者 |
| `materials/facilitator-deck/src/` | 簡報模板、CSS、JS、逐段投影片片段 | 維護者 |
| `materials/facilitator-deck/facilitator-deck.html` | 建置後的單檔簡報（含講者視窗） | 主持人（不發學員） |
| `materials/participant-runbook/content/` | Runbook 章節原稿（含提示詞與每段最多一張的決定表單） | 維護者 |
| `materials/participant-runbook/template/` | Runbook 模板、CSS、JS | 維護者 |
| `materials/participant-runbook/runbook.html` | 建置後的學員單檔 Runbook | 學員 |
| `materials/unlock-codes.json` | 各揭露時點的寫死解鎖碼 | 主持人（不發學員） |
| `scripts/build_materials.py`、`scripts/test_build_materials.py` | 建置與檢查工具 | 維護者 |

## 3. 揭露時點與解鎖群組

| 分鐘 | 解鎖群組 | 解開內容 |
|---|---|---|
| 00 | 不鎖 | 開始之前、環境準備、Runbook 使用方式、開場、詞彙表 |
| 07 | Greenfield | G0 Mission 與學員文件、G0 Starter 下載 |
| 29 | Time Skip | Time Skip 公告與交接、B0 下載、個人分析與 Shared Context 頁（含 Agent 紀錄格式） |
| 44 | B1 | B1 任務卡 |
| 52 | B2 | B2 任務卡 |
| 63 | B3 | B3 任務卡、Digital Worker 操作規則、Work Order、三個 Gate、Review、Delivery、空白例外回應卡 |
| 80 | 回顧 | 提示詞清單格式、成熟度比較 |

學員內容一律取自最新受控候選包的學員 ZIP，沿用其白名單與安全改寫；不得直接讀取作者 Repo 的 facilitator／evaluation 目錄；Recovery只讀凍結候選的兩份受控ZIP。唯一例外事件情境只在 69–70 分鐘由主持簡報呈現，不預放在 Runbook。

## 4. 主持簡報要求

- 單一 HTML、零外部依賴，可由 `file://` 離線開啟；16:9 投影。
- 依 90 分鐘十段時程組織；每段有可啟動的倒數計時與超時提示；底部顯示全場時間軸位置。
- 每個揭露時點有一頁大字顯示解鎖碼。
- B3 頁面內建 13 分鐘 Gate 節奏（3／6／7／11／12／13 分）；69–70 分鐘有 SQLite 例外事件卡與 60 秒倒數。
- 揭曉頁放在對應段落時間截止之後，前面先有「請先停手」過場頁。
- 講者視窗另開、同步翻頁，顯示 cue、觀察重點、提示條件、降級規則、下一頁預覽與解鎖碼；主畫面不顯示主持專用內容。
- 鍵盤操作：翻頁、總覽、講者視窗、全螢幕、計時器控制。

## 5. 學員 Runbook 要求

- 單一 HTML、零外部依賴，可由 `file://` 離線開啟；版型參考 AWS Workshop Studio：左側章節導覽、上一頁／下一頁、進度、章節內步驟。
- 每段頁首有「現在在做什麼」卡（情境、目標、技巧、完成的樣子）；每個檢查點提供可複製的提示詞區塊與複製按鈕，終端機指令寫在提示詞中由 Agent 執行，學員不自行輸入；每段任務後有「完成後想一想」反思題。
- 提示框分 Info、Tip、Warning、Danger。
- 表單每段最多一張、最多 4 欄，以下拉／勾選為主，只記錄人的決定（例如交付決定、B1／B2 決定、B3 Gate 決策、例外回應、交付核對、回顧）；自動暫存於瀏覽器，並可匯出 Markdown。分析、Shared Context、Review、Delivery 與提示詞清單由 Agent 依格式寫進 `notes/`，不做成學員表單。
- 鎖定章節顯示標題與鎖頭；解鎖狀態記在瀏覽器中，重新開啟仍保留。
- 工具中立，不要求任何特定 Agent 產品的指令或功能。

## 6. 驗證

1. 建置可重跑，相同輸入產生相同輸出。
2. 解碼全部鎖定章節後，Runbook章節不含 facilitator／evaluation 來源文字、標準答案或主持提示；受控Recovery ZIP依補充規則獨立鎖定；未解碼時原始碼不出現鎖定章節明文與解鎖碼明文。
3. 內嵌 G0／B0 ZIP 的內容與受控候選包對應學員 ZIP 的雜湊一致。
4. 簡報十段時程連續無重疊，合計 90 分鐘；揭露分鐘與第 3 節一致。
5. 兩份 HTML 內部錨點與章節連結有效；無外部網路請求。
6. 以實際瀏覽器開啟、翻頁、解鎖、下載、表單暫存與匯出完成冒煙檢查，並截圖審視版面。

## 完成條件

兩份單檔成品與建置工具完成；第 6 節檢查通過並如實記錄未執行項（例如目標瀏覽器的檔案下載政策）；凍結的程式、測試、候選包與既有教材未被修改；Agent.md 與規劃文件同步，並完成本機 Commit。真人演練與正式放行仍待真實證據。

## 本輪補充：Recovery與安全發放

2026-10-05使用者授權補齊審查問題。單檔Runbook另內嵌凍結候選的兩份已驗收Recovery ZIP，只於52／63分鐘由主持人按需提供獨立碼，與一般B2／B3任務碼分開；不得以Recovery當小組成果，不含B3接續解答。僅此兩份基線例外允許內嵌，仍禁止Evaluation原稿／完整參考答案目錄。

解鎖頁統一29分鐘；60秒倒數支援開始／暫停／繼續／重設且保持B3段落計時。package_materials.py生成只含runbook.html的ZIP，不發content／template原稿。瀏覽器下載與真人演練仍依實際Preflight驗收。
