# 全域一致性規則

> 目標讀者：素材產製 Agent、Repo 維護者、主持與評估者。
> 使用時機：建立／修改規格、程式、測試、文件或交付包前後。
> 前置條件：閱讀[Manifest](workshop-manifest.md)、[Glossary](glossary.md)及本階段正式規格。
> 版本：P1 治理基線，2026-10-05。
> 可見性：Facilitator／Evaluation／Agent Production；不直接發給學員。

## 1. 來源與變更

使用者明確指示與已核准變更優先；其次是[總控](../../docs/instructions/00_Agentic工作坊素材產製總控指令書.md)，再依本階段專屬指令。治理文件整理既有要求，不能用來暗中重編規則、降低門檻或刪除交付物。

有衝突時在[決策清單](../../docs/planning/decisions-and-open-issues.md)記錄來源、適用版本、影響、選項與解除條件。已核准變更才可同步改原規格；未核准建議保留為待協調。需實測才能解除的條件不能用文件敘述代替。

## 2. Domain 與命名

- 同一詞彙使用 Glossary 的同一意義；新增或改義先同步 Glossary。
- Trip、Booking、Order 不混用；Passenger 是搭乘者，Member 是可選會員關係。
- Request／Response 與 Domain Model 分離；Router 不承擔票價、座位或狀態政策。
- 名稱與分層在 G0→G1→B0→B3 延續；B0 的理解難度來自功能、依賴與有限文件落差，不靠混亂命名或無內容檔案。

## 3. Rule ID 與追溯

每個規則有唯一識別碼與明確適用版本／Use Case；每個 Acceptance Criterion 有固定 ID。`TRIP-*`、`BOOKING-*`、`FARE-*`、`PAYMENT-*`、`ORDER-*` 等前綴依原指令沿用；B3 的 `GROUP-*`、`GROUP-PAY-*`、`GROUP-FARE-*`、`GROUP-AUDIT-*`、`GROUP-NOTIFY-*` 不與一般訂票限制混用。

追溯紀錄至少包含：

| 欄位 | 要求 |
|---|---|
| Rule ID／版本／用途 | 規則原文、版本差異、一般或團體適用範圍 |
| Source／Requirement | 正式來源與需求段落 |
| Acceptance ID | `AC-G-*`／`AC-B1-*`／`AC-B2-*`／`AC-B3-*` 對應 |
| Code Area | 實際 Domain／Application 位置；未實作時標明未建立 |
| Test／Validation | 測試檔、名稱、驗證方式與實際結果 |
| Documentation／Evaluation | 商業規則、API 範例、評估表位置與一致性 |

O-03 已於 P2 對齊：`BOOKING-002` 為一般單筆最多 4 人，`BOOKING-003` 為不得超過剩餘座位；舊技術標準的座位限制引用映射為 `BOOKING-003`。正式來源已同步，完整規則與預期追溯見[Rule Registry](rule-traceability-baseline.md)。沒有變更商業限制，也沒有程式驗證結果。

不得只把規則保存在 Prompt。規則變更時檢查 Requirement→Code→Test→Document→Evaluation 全鏈與受影響 API。B2 最有利政策包含改票重新計價，不能只改新建 Booking。

## 4. 版本、基線與資料

版本按 G0→G1→B0→B1→B2→B3 演化，每版有自身 README、依賴、測試、文件與報告，不從其他版本 Import。學員實作可不同於 Reference，但 API、規則與基本責任分離須符合驗收。

各版使用固定 Seed、可注入 Clock、可控 Payment Gateway 與獨立 Reset。不得用當日日期、測試順序或隨機狀態製造問題。案例保持本機可執行，禁止真實付款／個資／憑證或核心外部 API 依賴。

G0 保留受控 TODO 與明確 Feature Skip；G1 完成且無 Skip／XFail；B0 僅有已記錄學生票 Bug、3 項債務、2 項落差；B1 最小修復；B2 不疊加優惠；B3 增加團體完整流程。不得提前洩漏／實作下一版答案。

B0 僅有一個 `BUG-B0-001`，保留全部 28 項 G1 Regression 與正確斷言；實測失敗 node ID 集合須與已核實 Intentional Failure Manifest 完全一致，其餘全通過、零非預期失敗，無 Skip／XFail／未知 Warning。B1 修復後全部 28 項 G1 及全部 B0 新增測試恢復通過。不以 Skip／XFail、改期待值或刪測試壓低失敗數。B0 clean-copy 保留原交付路徑，內容是原始 B0，不是已修正的 B1。來源、同步或生成與比對方式按 O-06 定義後落實。

案例 Git History／Tag 與作者 Repo 版本是不同層次。G1 案例歷史／Tag 與 Bundle 已建立；B0 須延續其來源並驗證交付包隔離。若提供模擬歷史須明確標示。學員歷史不得含未發放任務答案的 Branch、Tag 或可達 Commit。

2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)，O-04 規格衝突已解除；B0已按方案A實測驗收。Manifest 須以逐項 node ID、Diff／呼叫路徑及修復驗證證明單一 Bug 因果，不接受模糊「學生票相關」分類。

## 5. 人機與 Gate

產製驗收 Gate A–E、各版本交付判定，與活動內 B3 三個 Human Approval Gate 分開記錄；定義見[Acceptance Gates](acceptance-gates.md)。通過其中一種不代表另一種通過。

B3 人員只進行 Challenge／Review／Approve／Reject；Agent 依核准需求、範圍與計畫執行。重大範圍變更、規則衝突、未知測試失敗、外部依賴提議與時間不足應升級，不自行猜測或隱藏。固定例外僅有 SQLite 提議，按[Digital Worker 指令](../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)在 Gate 2 處理，不真的新增資料庫。

學員 Level 1／2 成果與未完成事項保留原貌，Recovery 不記成自行完成。Reference 的完整驗收不可用活動分級取代。時程以 90 分鐘演化活動為本次範圍，不把通用一日流程或額外角色輪轉列為必做；O-01／O-02 的來源文件仍待後續對齊。

## 6. 可見性與文件品質

Participant 只包含當階段需求、最低 API 要求、驗收條件與必要操作背景；不包含完整解答、完整影響分析、主持提示、標準實作或例外標準回應。Facilitator、Evaluation、Agent Production 不因存放同一 Repo 而可對學員開放。

交付用允許清單，按階段分包；檢查正文、測試、連結、隱藏檔、歷史與範例是否洩漏後續答案。不得整份複製治理文件到學員包。Recovery 另受主持人控制；`dist/` 是可重建輸出，不當成第二份權威來源。

文件預設繁體中文，開頭含讀者／時機／前置，結尾列產出或完成條件。Participant 簡潔；Facilitator 含時間點、觀察、提示與停止條件；Evaluation 含可判定標準。基準檔、報告與版本矩陣不得互相抄成「已驗證」卻無實際證據。

## 7. 差異的適用狀態

| 問題 | 本治理基線採用方式 | 後續條件 |
|---|---|---|
| O-01 時程／角色 | 90 分鐘與個人→混合小組適用；通用一日／半日為方法參考 | Runbook、角色與發放流程需對齊並演練 |
| O-02 完整 DoD／分級 | 區分學員學習、完整程式交付與 Reference 驗收 | B3 與評估表需沿用對象區分 |
| O-03 Rule ID | P2 已完成編號對齊與來源同步 | 後續 Code／Test／Document 沿用 Registry，實際追溯仍待產製 |
| O-04 B0 失敗／Regression | 方案 A 已核准，規格衝突解除 | B0完整Manifest集合實測已通過，B1正式全恢復待驗收 |
| O-05 歷史策略 | G1 案例歷史／Tag 與 Bundle 已建立 | B0 歷史延續與打包隔離 |
| O-06 基線副本 | 保留原交付要求 | B0 前定義生成／同步及一致性驗證 |
| O-07 G1 限制 PASS | G1 已 PASS，B0 前置滿足 | 一般門檻保留，B0已驗收，後續B1仍待產製 |

此表記錄適用規則與處理時點。O-03於P2同步技術標準編號並建立Registry，其他問題不因此解除；`docs/contents/`未改寫，商業規則與測試門檻未變更。

## 完成條件

每次變更都可從來源、詞彙、版本、規則與驗收追溯到文件及交付對象；本階段只完成治理文件檢查。程式與包的實際證據需由後續階段取得，未執行不得宣稱通過。

2026-10-05 P5實測紀錄：B0為38實質Python／測試檔、44項測試；正式5failed／39passed符合完整manifest且零非預期，隔離一行學生率修復44passed。52檔clean-copy雜湊一致、B0 Tag392d920與Bundle續G1，已知相容Warning保留。詳見[B0 Validation Report](../03-brownfield/evaluation/01-b0-validation-report.md)。B1正式版本、真實學員與90分鐘演練仍未完成。

2026-10-05 P7 B2實測完成、個別B2 Gate PASS：獨立Python3.13.15環境依賴安裝成功，55 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（1.21s）。Health／11個OpenAPI路徑、企業＋提前混合成人595／學生525／Total1120、付款、改票至T005新價1199／差額79、退票、通知3／Audit4及Reset Smoke通過。B1原52檔雜湊不變；B2快照54檔，保留原28項G1正確斷言，原13測試檔只有test_advance政策案例遷移，新增11項B2測試。逐旅客最低rate、不疊加、Applied Discounts、改票共用政策與折扣文件同步；TASK-B2-001、13項AC及主持材料已建立。案例Tag `b2-best-single-discount`與Bundle已驗證：14個真實Commit，54檔Clone比對零差異，B1為祖先且無B3歷史。詳見 [B2 Validation Report](../03-brownfield/evaluation/15-b2-validation-report.md) 與 [案例歷史／Delta](../03-brownfield/evaluation/17-b2-case-history-and-delta.md)。此為P7當時範圍與證據；目前B3與B1–B3素材驗收見下方P8紀錄，真實演練及最終交付仍待完成。

2026-10-05 P8正式B3已產製並實測，個別Gate PASS：獨立Python3.13.15環境安裝成功，75 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（0.58s），55原案例＋20團體新增。Import／Health／13個OpenAPI路徑／Uvicorn Health（2.17s）及Smoke通過：5人混合團體總價2905（學生75%、成人提前85%）、同車廂連續、成功唯一Order、已付款退票、付款失敗CANCELLED／全釋放／無Order、Audit2／通知1與Reset。57規則、19項AC、三Gate、任務卡與主持節奏齊備；案例Tag b3-group-booking=`ca3e5de7adca290f555d9ab96f322f65345b3e90`；Bundle73,670 bytes、17個真實Commit，Clone59來源檔比對零差異；B2來源54檔雜湊凍結、原55案例對應15測試檔字節一致。B1–B3標準素材Final Decision為PASS FOR WORKSHOP USE，僅代表三版標準實作素材；不代表P9完整Operating Rules／Work Order／治理模板、13分鐘或90分鐘真實演練、打包與正式交付已完成。這是P8當時的範圍界線；目前P9狀態見後續紀錄。

詳見 [B3 Validation Report](../03-brownfield/evaluation/18-b3-validation-report.md) 與 [B1–B3素材驗收](../03-brownfield/evaluation/21-b1-b3-production-result.md)。

2026-10-05 P9治理文件基線完成，Final Decision為PASS FOR GOVERNED DIGITAL WORKER EXERCISE：15份規定輸出加追溯／驗證報告／證據共18份（17 Markdown＋1 JSON）。17份Markdown的40個相對連結有效、UTF-8無BOM、Code Fences平衡；Participant無答案或內部越界連結。唯一EXCEPTION-DW-001、Work Order17項Group Rule與B3精確相等、Work Order11／Delivery12／Audit13個規定欄位均符合；Operating Rules約384個中文字。B3原59來源檔SHA256全部不變。獨立審查22項指令映射、三人員Gate及時程一致，無阻擋問題。此PASS只涵蓋治理文件一致性及時程設計，不等於學員Gate1／2／3已實際核准；兩分鐘閱讀、13分鐘活動與60秒例外尚未真實演練，Rehearsal／Package為NOT RUN。此為P9當時範圍，P10目前進度見後續紀錄；P11全域驗證與交付包未完成。

證據依[P9 Governance Validation Report](../04-digital-worker/evaluation/06-governance-validation-report.md)核對，判定及實際靜態結果已核對；真實演練與打包仍未執行。

2026-10-05 P10主持／回顧文件基線PASS：新07指令整合既有要求；11份輸出為10 Markdown＋1 JSON（回顧學員2／主持2／評估索引1、Runbook4、Validation Report及證據JSON）。10份Markdown的131個相對連結有效、UTF-8無BOM、Code Fences平衡，Participant無答案或越界內部連結。主流程十段連續且無重疊加總90分鐘；Time Skip至Brownfield交付51分鐘、B3 13分鐘、回顧10分鐘；唯一EXCEPTION-DW-001包含於69–70分鐘。B3原59來源檔與P9原17份Markdown雜湊不變。O-01時程／角色及O-02完整Reference DoD／學員Level在新文件對齊；此PASS僅文件一致性與時程設計，不以空Preflight表當已執行證據。實際Preflight、真人90分鐘／13分鐘演練、Recovery演練與受控包生成均NOT RUN；O-01／O-02的演練解除證據仍待P11。下一階段P11全域驗證、受控打包與真人演練未啟動。

來源與已核對的文件驗證證據：[P10產製指令](../../docs/instructions/07_主持Runbook與回顧整合產製指令書.md)；[P10 Validation Report](../06-runbook/evaluation/p10-validation-report.md)。

## P11 本輪執行狀態

2026-10-05 使用者「進入下一個目標」啟動P11，並選擇本次安排真人演練。六版本輪pip check、pytest、API Smoke與實際Uvicorn Health／OpenAPI通過；G0為1pass／8受控skip，G1為28pass，B0為39pass／5精確Manifest失敗，B1／B2／B3為44／55／75pass。已生成13份受控候選ZIP，B1／B2解壓Recovery副本44／55測試與Smoke通過；使用既有獨立venv，未宣稱新安裝。候選包以最終白名單／Hash與本輪報告為準；真人演練人員、時段與記錄者尚待提供，未執行90分鐘活動。P10及先前紀錄中的未啟動／未打包均為當時狀態，不作本輪結果。P11整體與正式發布仍待驗收；O-01／O-02真人證據解除條件保留。

依據：[P11指令](../../docs/instructions/08_全域驗證與受控打包產製指令書.md)；[本輪驗證報告](../06-runbook/evaluation/p11-validation-report.md)。

## 一致性審查後的優先修正

2026-10-05 使用者要求設為新目標並優先處理審查發現。先前候選360cb551f76eeb73的清單／Hash／連結與Recovery技術通過不涵蓋教學語意；該包已停止用於本次演練。修正初始B0答案洩漏、恢復兩份受控落差與三份安全ADR，並對齊任務揭露、Level1交付、Recovery、B2合約勘誤、Mission／空白例外卡發放與歷史狀態。凍結程式／測試／案例來源保持，P9／P10歷史JSON不改寫。新候選與實際驗證以本輪報告為準；真人演練及正式放行仍待驗收，O-01／O-02真人證據解除條件保留。

依據：[修正指令](../../docs/instructions/09_教材一致性修正與交付重驗指令書.md)；[一致性修正報告](../06-runbook/evaluation/consistency-correction-report.md)。
