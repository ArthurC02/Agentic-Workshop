# 第一階段：Greenfield 講解簡報（Speech Deck）

> 讀者：講者與教材維護者。時機：Greenfield（從頭開始的新專案）Workshop後的45分鐘操作教學。前置：學員已體驗G0（Greenfield 起始程式包）、備妥編輯器與通用Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）；每人使用獨立練習目錄。

## 成品與操作

- `greenfield-deck.html`：18頁、16:9、單檔離線簡報。以Edge／Chrome從本機開啟。
- `greenfield-handout.md`：可提供學員的逐頁指令與人工確認；不含講者備註。
- `practice/idea.md`：複製到新專案的 `docs/idea.md` 作為演練來源。
- `practice/booking.feature`：混合訂票、邊界、容量與付款的Gherkin（用 Given／When／Then 寫測試情境的格式）參考；供完成草稿後比較，尚未連接可執行測試。

方向鍵／Space翻頁；O總覽；N顯示講者備註；F全螢幕；T開始／暫停全段計時。重設按鈕清除計時。備註為同頁覆蓋，投影時關閉。底部提供Idea、Gherkin參考與操作講義下載；指令頁可複製。若瀏覽器禁止剪貼簿，會選取文字供手動複製；禁止下載時由講者提供對應檔案。

本段是使用者指定的獨立45分鐘教學時段；與既有90分鐘活動合併的完整議程尚待安排，未改寫原主持簡報或Runbook時程。

## 45分鐘節奏

| 段落經過時間 | 頁面 | 操作與停止條件 |
|---|---|---|
| 00–03 | 1–3 | 回看準備，指出來源或真實卡點；第3分鐘轉新目錄。 |
| 03–06 | 4 | 建立資料夾、連接Agent、複製Idea；位置確認後繼續。 |
| 06–10 | 5 | 整理專案摘要；區分來源、假設與缺口。 |
| 10–15 | 6–7 | 拆MVP（Minimum Viable Product，最小可行產品），細化一個訂票工作；不新增範圍。 |
| 15–20 | 8 | 細化使用者故事（User Story）或使用案例（Use Case）；確認角色、價值與例外。 |
| 20–25 | 9 | 細化AC（Acceptance Criteria，驗收條件）；人手算1225並核對邊界。 |
| 25–30 | 10–11 | 畫業務流程（Business Flow），反查AC；未決問題保留。 |
| 30–36 | 12–14 | 寫Gherkin並對應pytest；文件情境不算實測。 |
| 36–42 | 15–16 | 審架構與檔案計畫；核准後才建骨架目錄。 |
| 42–45 | 17–18 | 核對追溯鏈與交接；時間到交真實現況與缺項。 |

講者先簡短示範再讓學員操作。每段結束前請學員指出一項來源與一個確認結果。Agent回應太慢時只完成核心混合訂票情境，其餘列待辦；卡在環境可改手動寫文件。業務矛盾或無來源的結論未解決前，保持待確認，先處理可獨立完成的文件。學員不需在此45分鐘內重建完整G0或完成業務程式。

## 內容依據與邊界

- [Greenfield需求](../../../01-greenfield/participant/02-business-requirements.md)
- [驗收條件](../../../01-greenfield/participant/03-acceptance-criteria.md)
- [Agent操作指南](../../../01-greenfield/participant/04-agent-usage-guide.md)
- [G0架構](../../../01-greenfield/participant/starter-repository/docs/architecture.md)
- [G0至G1差異說明（Delta）](../../../01-greenfield/evaluation/05-g0-to-g1-delta.md)

M1–M4 與 TASK-GF-02 只是本講解課拆的練習單位，不是新版本，也沒有改正式任務清單。Idea提供既有需求摘要；付款失敗仍待付款且保留座位。Gherkin參考只涵蓋選定情境，不宣稱完整15項AC覆蓋。pytest 程式只示範情境怎麼對應到測試，空資料夾尚無App或fixture（pytest的測試前置準備）。文件審查與MVP程式驗收分開。

## 維護

從Repo根目錄執行：

```powershell
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 agentic-workshop/materials/speech/build_decks.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 agentic-workshop/materials/speech/build_decks.py --check
```

修改 `src/slides.json` 的內容與備註，或 `../shared/` 的版型，再重建。練習檔與操作講義會內嵌於HTML供下載。建置不需候選包（凍結的教材版本包）、網路或外部前端套件。

## 完成條件

18頁與講義可重建；指令可取得；至少一個情境可追溯至規則、AC、Gherkin與模組。45分鐘為教學配置，實際學員時間與公司瀏覽器下載政策需現場確認。
