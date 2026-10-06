# 主持簡報與學員 Runbook

> 目標讀者：主持人與素材維護者。
> 使用時機：工作坊事前準備、現場主持，以及修改簡報或 Runbook 之後重新建置。
> 前置條件：已閱讀 [P12 指令書](../../docs/instructions/10_主持簡報與學員Runbook產製指令書.md)；建置需要作者 Repo 中的 Python 3.13 環境與最新受控候選包 `dist/p11-candidate/c841f2424d256c28/`。
> 可見性：本目錄除 `participant-runbook/runbook.html` 外，都是主持與維護用，不發給學員。

## 1. 成品

各階段的概念與操作教學Deck另存於 [speech/](speech/README.md)。第一階段Greenfield採45分鐘、18頁獨立Deck與操作講義；與下列90分鐘主持流程的整合時間另行安排。

| 檔案 | 用途 | 發給誰 |
|---|---|---|
| `facilitator-deck/facilitator-deck.html` | 90 分鐘主持簡報，含講者視窗、計時器、解鎖碼頁與答案揭曉頁 | 只給主持人 |
| `participant-runbook/runbook.html` | 學員從頭用到尾的單一檔案；內嵌 G0／B0 與按需 B1／B2 Recovery 下載 | 開場前發給每位學員 |
| `unlock-codes.json` | 各揭露時點的寫死解鎖碼 | 只給主持人 |

兩個 HTML 都是單一檔案，不需要網路或安裝任何東西，直接用瀏覽器開啟（建議 Edge 或 Chrome）。

## 2. 現場操作：主持簡報

- 開啟 `facilitator-deck.html`，按 `F` 全螢幕投影。
- 按 `P` 開啟講者視窗，拖到主持人自己的螢幕。講者視窗顯示講者備註（cue、觀察、提示條件、降級規則）、下一頁、計時器、時鐘與全部解鎖碼；兩個視窗同步翻頁。
- 每段的倒數計時以段落為單位：在該段任何一頁按 `T` 開始或暫停、`R` 重設；最後 20% 轉橘色，超時轉紅色並往上計。
- 例外卡60秒倒數：`T`開始／暫停／繼續，`R`重設；講者按鈕控制本頁同一倒數。B3段落計時持續，不因暫停例外倒數而暫停活動。
- 其他按鍵：`→`／`Space` 下一步、`←` 上一步、`O` 總覽、`B` 黑畫面、`?` 說明、`Esc` 關閉覆蓋層。
- 細節頁預設一次顯示完整內容，按一次下一步即翻頁。只有「今日旅程」「Agent 的分工改變」「規則改變：人不直接改程式」保留逐步顯示，方便引導角色轉換。維護時只在需要分段講解的頁面加 `data-fragments="step"`，其 `.fx` 才會消耗下一步按鍵。
- 解鎖碼頁會以大字顯示該時點的解鎖碼；答案揭曉頁前一定有一張「請先停手」頁，請在該段時間截止後才翻過去。

## 3. 學員 Runbook 的發放

1. 開場前，執行 `scripts/package_materials.py`，生成 `dist/materials/participant-materials.zip`（只含 `runbook.html`）。只發此 ZIP 或 HTML，不發整個 `participant-runbook/`（`content/`會提前透露任務）、`materials/`或作者 Repo。把成品放到共用資料夾、Teams 檔案區或 USB 發給學員。銀行郵件閘道可能擋 `.html` 附件，不建議用 Email。
2. 提醒學員：先把檔案存到本機（不要直接在壓縮檔或郵件附件預覽中開啟），並整場使用同一個瀏覽器，表單暫存與解鎖狀態存在該瀏覽器中。
3. 第 07 分鐘公布 Greenfield 解鎖碼後，學員在 Runbook 下載 G0；第 29 分鐘公布 Time Skip 解鎖碼後下載 B0。
4. 學員晚到或換電腦時，再念一次已公布的活動解鎖碼即可補上。
5. 52分鐘進B2／63分鐘進B3，主持人按需向核准小組提供講者視窗／`unlock-codes.json`中的獨立Recovery碼，學員到相應Recovery頁下載並依步驟切換。保留原成果、未完成、來源與核准原因，接續基線不算小組自行完成；B3開始後不再換版。

解鎖碼只防止學員提早翻看，不是密碼學保護。Runbook 不含主持提示或 Evaluation 原稿；另內嵌已驗收 B1／B2 Recovery 接續基線，由主持人只於52／63分鐘按需提供獨立碼，不向全場公布 Recovery 碼，不提供 B3 解答。編碼不構成權限安全。

## 4. 事前 Preflight 補充項

除 [Preflight Checklist](../06-runbook/preflight-checklist.md) 外，請用學員實際使用的電腦與瀏覽器確認：

- [ ] 從本機開啟 `runbook.html`，輸入一組解鎖碼可以解開章節。
- [ ] 解鎖後可以下載 G0／B0 ZIP，且解壓縮後能依 Runbook 指令啟動與測試。
- [ ] 一般B2／B3碼不解開Recovery；獨立碼能下載正確B1／B2並完成版本／測試／Health／Context切換。
- [ ] 例外倒數可暫停／繼續／重設，B3段落計時持續。
- [ ] 表單會自動暫存，關閉再開仍保留；「匯出 Markdown」可以下載 `.md` 檔。
- [ ] 主持電腦可以開啟講者視窗（瀏覽器未封鎖彈出視窗）並同步翻頁。

若公司政策封鎖瀏覽器下載，改由主持人在第 07、29 分鐘從共用資料夾提供候選包中的 `participant-07-g0.zip`、`participant-29-b0.zip`；兩者與 Runbook 內嵌版本的 SHA256 相同。

## 5. 修改與重新建置

- 簡報原稿：`facilitator-deck/src/`（`deck.template.html`、`deck.css`、`js/*.js`、`slides/*.html`）。每頁的主持專用內容放在 `<aside class="notes">`，主畫面不顯示。
- Runbook 原稿：`participant-runbook/content/*.md`（章節，學員內容以 `include` 直接取自受控候選包的學員 ZIP）與 `participant-runbook/template/`。
- 建置與檢查（在 Repo 根目錄執行）：

```powershell
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/build_materials.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/build_materials.py --check
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/package_materials.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 -m unittest discover -s scripts -p 'test_*materials*.py'
```

建置會驗證候選包雜湊、時程連續加總 90 分鐘、解鎖碼與鎖定內容不以明文出現、Runbook 不含主持／評估內容或外部網址；任何一項失敗都不會產出檔案。修改解鎖碼只需改 `unlock-codes.json` 後重新建置。

## 完成條件

主持人能用簡報走完 90 分鐘並在正確時點公布解鎖碼與揭曉答案；學員只拿到一個 `runbook.html` 即可完成全部活動；修改後重新建置與檢查通過。真人演練結果另記於 [演練紀錄](../06-runbook/rehearsal-record.md)。
