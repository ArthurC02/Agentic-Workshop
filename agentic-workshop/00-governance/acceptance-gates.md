# 產製驗收與人員核准 Gate

> 目標讀者：素材產製 Agent、維護者、主持人與評估者。
> 使用時機：驗收素材版本、判斷是否進入下一階段或 Review B3 時。
> 前置條件：閱讀[Manifest](workshop-manifest.md)、[Glossary](glossary.md)、[一致性規則](consistency-rules.md)及本版指令。
> 版本：P1 治理基線，2026-10-05。
> 可見性：Facilitator／Evaluation／Agent Production；含內部驗收與問題位置，不整份發給學員。

## 1. Gate 判定與證據

Gate 是有前置、檢查項、實際證據與決策的關卡，不以 Agent 的「已完成」代替。未執行的程式測試標為未驗證，不判通過；文件基線完成不表示 App、測試或演練已通過。

產製者記錄版本、來源、環境、檢查或命令、實際結果、已知限制、未完成、差異及判定者。版本 Final Decision 使用原指令指定的字串；不得自創可忽略失敗的通過類別。

## 2. 各程式版本共通 Gate A–E

依[技術標準 §15](../../docs/instructions/01_技術棧與Repository標準指令書.md)，G0／G1／B0–B3 都須取得下列證據：

| Gate | 必要檢查與證據 | 阻擋條件 |
|---|---|---|
| A：檔案與依賴 | 必要檔案、Import、Python 與依賴版本、乾淨環境安裝結果；無外部憑證 | 檔案缺失、依賴／Import 不可用或核心依賴外部服務 |
| B：啟動 | App 載入、`GET /health` 為 200 與 `{"status":"ok"}`、OpenAPI 可產生 | 未執行或結果錯誤 |
| C：測試 | 實際 pytest 命令與版本預期；失敗／Skip／XFail／Warning 均可識別 | 未知失敗、掩蓋失敗或不符合本版例外 |
| D：規則追溯 | Requirement→Rule ID→Code→Test→Document→Evaluation；規則與版本差異有紀錄 | 同 ID 異義、商業政策不一致、AC 無驗證或資料缺漏 |
| E：工作坊適配 | 一般工程師可理解、無外部服務、無答案洩漏、符合時間限制 | 需高階演算法或複雜設施、洩漏答案、素材量超時 |

典型程式驗證為 `python --version`、安裝 `requirements.txt`、`pytest -q`、App Import 與 TestClient API Smoke。各版 README 的 `src` Import Path、啟動與測試方式須一致；本 P1 沒有執行上述命令或安裝依賴。

## 3. 階段輸入、專屬證據與進入條件

| 產製階段 | 前置與必需證據 | 通過／後續條件 |
|---|---|---|
| P1 治理文件 | 四份文件存在；目標、90 分鐘、責任、詞彙、版本、可見性、Rule 追溯與本 Gate 一致；來源連結存在；O-01–O-07 狀態明確 | 文件一致性與連結檢查完成可交付 P1；不判定程式通過，不自動解除後續阻擋 |
| P2 技術基線 | P1、Python／FastAPI／Pydantic／pytest／In-Memory 與分層要求；Rule ID 適用紀錄 | O-03 已對齊並同步來源；核對技術基線、Rule Registry 與版本驗證要求，不視為 Runtime 已通過 |
| G0 Starter | P1／P2；依[G0 指令](../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)驗證 Health、固定 Seed／Reset、10–16 個主要 TODO、骨架、需求與 AC、隔離與初始測試報告 | Health 通過；未實作 Feature 可明確 Skip 並引用規則／功能，無未知失敗。不提供完整答案；22 分鐘範圍合理 |
| G1 Reference | 已驗收 G0；依[G1 指令](../../docs/instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)完成 API Happy Path、75% 學生票、建立失敗不扣座位、付款失敗不建 Order／不轉 PAID、AC Map 與 Delta | 全測試通過、無 Skip／XFail；至少 18 個有效測試、目標小於 5 秒；Final Decision 為 `PASS`／`PASS WITH DOCUMENTED LIMITATION`／`FAIL`。B0 前置仍要求 `PASS` |
| B0 Baseline | G1 PASS；依[B0 指令](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)新增功能、35–45 個實質 Python／測試檔、3 債務、2 文件落差、原始基線副本、Delta 與 Module Map | 僅一個 `BUG-B0-001`；保留全部 28 項 G1 Regression 與正確斷言，完整實測失敗 node ID 集合須與已核實 Intentional Failure Manifest 完全一致，其餘全部通過、零非預期失敗、無 Skip／XFail／未知 Warning；決策為 `PASS AS BROWNFIELD BASELINE` 或 `FAIL`。B0已按方案A實測驗收 |
| B1 Reference | 已驗收 B0；學生票最小修復、Manifest 全部失敗恢復、成人與混合 Passenger 正確、不改既有優惠順序 | 全部 28 項 G1 Regression 及全部 B0 新增測試通過、無 Skip／XFail；修改和規則可追溯，不弱化測試；28 並非 B1 全套數 |
| B2 Reference | 已驗收 B1；逐位最有利、不疊加、各優惠代表組合、Applied Discount、改票重新計價與文件同步 | 全套與 Regression 通過、無 Skip／XFail；不提前完成團體功能 |
| B3 Reference | 已驗收 B2；5／20 與4／21人邊界、同車廂完整連續區段、建立失敗不保留座位、付款失敗整筆取消／全釋放／無Order、單一成功Order、B2計價、Audit／通知與文件 | 全套與 Regression 通過、無 Skip／XFail／未知失敗；B1–B3 整體決策 `PASS FOR WORKSHOP USE` 或 `FAIL`；完整套件建議55–75內、目標小於10秒 |
| Digital Worker 治理 | B0–B3 規格確立；依[治理指令](../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)提供 Work Order、三 Gate、Review、升級、交付、唯一SQLite例外、Rubric與Audit範本 | 與 B3 規則一致、不改商業需求、13分鐘可用、素材隔離；決策 `PASS FOR GOVERNED DIGITAL WORKER EXERCISE` 或 `FAIL` |
| Runbook／回顧 | 已驗收階段材料；時程、提示／中止、發放、Recovery、回顧與組織導入問題 | 90分鐘配置完整、O-01／O-02對象對齊、主持可執行；演練時間另取實際證據 |
| 全域與打包 | 所有版本與教材已驗收；允許清單、角色／階段包、來源識別、檔案／連結／歷史隔離與乾淨環境／Recovery／90分鐘演練記錄 | 無洩漏、無未知失敗、實測問題已處理；未驗證的包或演練不宣稱可正式交付 |

B1–B3 詳細 AC 與 API 以[任務指令](../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)為準；本表是 Gate 摘要，不省略原指令逐項驗收。測試數／效能目標按原指令區分最低要求、建議範圍與目標，不以湊數取代功能證據。

## 4. B3 活動的三個 Human Gate

| Gate | Agent 提交 | 人員必查與決策 |
|---|---|---|
| 1：Requirement Understanding | 需求、規則、假設、缺口、Out of Scope | 5–20人、同車廂連續、不部分成功、付款補償及B2政策；核准後才設計 |
| 2：Impact and Design | 影響／不影響模組、API、座位與補償方案、測試、文件、風險、預計修改檔案 | 範圍、Regression、失敗狀態與座位釋放、外部依賴；核准後才改程式 |
| 3：Delivery Review | 實際Diff、測試指令與結果、AC／Rule對照、文件、偏差、未完成與建議 | 證據、範圍、補償、文件一致與透明性；決定核准、條件核准或要求修正 |

決策使用 `APPROVE`／`APPROVE WITH CONDITIONS`／`REJECT AND REVISE`，短格式記錄已審證據、條件、核准者與時間。這三關不是 Gate A–E，也不等同標準實作驗收。

唯一例外 `EXCEPTION-DW-001` 在 Gate 2 提議 SQLite；與 In-Memory 邊界衝突。人員應辨識越界、拒絕或要求修正，不真的安裝或更改技術組合。Agent 發現未核准需求／API範圍變更、規則矛盾、未知測試失敗、外部依賴或時間不足需停止升級。完整條件沿用治理指令。

## 5. 學員完成度與完整交付

| 對象／等級 | 判定證據 | 可宣稱範圍 |
|---|---|---|
| 學員 Level 1 | Gate 1／2 完成，影響分析合理、測試策略完整，程式尚未完成 | 分析完成，不宣稱功能驗收通過 |
| 學員 Level 2 | 團體建立與連續座位完成、主要單元測試通過，付款失敗的補償（Compensation）或文件仍有缺項 | 核心流程完成，明列缺口 |
| 學員 Level 3 | 建立、付款成功與付款失敗的補償都完成，回歸測試（Regression）通過，文件與交付摘要都完整；另需 Review 證據 | 完整交付，仍需人員核准 |
| Reference Solution | 原指令全部AC、Regression、追溯、文件與實際驗證 | 標準實作完整驗收，不受學員有限時間分級豁免 |

學習成功不是只有Level3。Recovery、未完成、失敗、條件核准與人員介入需如實保留；不可將演練時間壓力轉成跳過Gate／測試的理由。

## 6. 待協調事項與阻擋時點

依[差異清單](../../docs/planning/decisions-and-open-issues.md)：

| 問題 | P1適用狀態 | 後續前置／解除證據 |
|---|---|---|
| O-01 時程／角色 | 使用90分鐘及個人→混合小組；原通用內容未改 | Runbook與角色／發放對齊、實際演練 |
| O-02 完整DoD／學員分級 | 依上表區分學習與完整交付 | B3任務與評估表對象一致；Reference門檻不降低 |
| O-03 Rule ID | P2 已統一一般最多4人為002、座位容量為003並同步來源 | G0 起實際 Code／Test／Document 應沿用唯一映射 |
| O-04 B0失敗數／Regression | 規格衝突已依方案 A 核准解除；B0已按方案A實測驗收 | 一個 Bug、完整 Manifest 集合一致、零非預期；B1 全恢復；不刪／弱化／隱藏測試 |
| O-05 案例歷史 | G1 案例歷史／Tag 與 Bundle 已建立 | B0 仍須延續 G1 歷史並提供來源及打包隔離證據 |
| O-06 clean-copy | 原路徑與交付要求保留 | B0前來源、生成／同步、內容比對與本版測試預期 |
| O-07 跨階段PASS | G1 已取得 PASS，B0 前置已滿足 | 含限制通過不等於 PASS 的一般門檻保留；不代表 B0 已驗收 |

2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)。Manifest 須逐項記錄 node ID、Rule／AC、Diff／呼叫路徑及修復驗證；不得將任意學生票失敗自動列為預期，pytest 非零退出碼亦不等於一般通過。

本表不核准任何商業或測試門檻變更。P1可完成，對應後續階段仍受問題與證據限制。

## 完成條件

產製 Gate、Human Gate 與學員分級對象明確，證據／判定／阻擋條件可追溯到原指令；四份文件一致且連結有效，才能交付 P1。程式、包與演練的通過結果僅可由後續實際驗證取得。

2026-10-05 P5實測紀錄：B0為38實質Python／測試檔、44項測試；正式5failed／39passed符合完整manifest且零非預期，隔離一行學生率修復44passed。52檔clean-copy雜湊一致、B0 Tag392d920與Bundle續G1，已知相容Warning保留。詳見[B0 Validation Report](../03-brownfield/evaluation/01-b0-validation-report.md)。B1正式版本、真實學員與90分鐘演練仍未完成。

2026-10-05 P6正式B1驗收：獨立環境44passed／1已知Warning（1.00s），全部28G1與16B0新增通過、五Manifest失敗全部恢復，原測試／優惠順序不變。案例Tag a1c1d45與52檔來源核對通過，個別B1 Gate PASS；詳見[B1 Validation Report](../03-brownfield/evaluation/12-b1-validation-report.md)。B2／B3與B1–B3整體驗收、真實8分鐘／90分鐘演練仍待完成。

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
