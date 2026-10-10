# Workshop Manifest

> 目標讀者：工作坊設計者、主持人、評估者與素材產製 Agent。
> 使用時機：產製任一階段素材、整合主持流程或判定範圍時。
> 前置條件：閱讀[總控指令書](../../docs/instructions/00_Agentic工作坊素材產製總控指令書.md)與[產製路線](../../docs/planning/production-roadmap.md)。
> 版本：P1 治理基線，2026-10-05。
> 可見性：Facilitator／Evaluation／Agent Production；含受控 Bug 與後續任務資訊，不整份發給學員。

## 1. 目標與固定條件

以 **Smart Ticket Platform** 的演化呈現 **Tool → Teammate → Digital Worker**。目標依序是練習 Agentic Coding 技巧、體驗 Tool → Teammate → Digital Worker、由 Agent 留下證據；組織導入在回顧時討論（2026-10-09 已核准變更）。

活動長度 90 分鐘，對象為一般工程師。Greenfield 一人一組；Brownfield 多人一組，個人先用自己的 Agent 分析，小組整合後由主要 Agent 執行。不採角色扮演型競賽，不以程式量或自主率作唯一成功指標。

全部教材工具中立；可要求 Plan、Diff Review、Test 與交付說明，不要求某產品專屬功能。真實交通規則、品牌、金流、個資與外部 API 不屬於案例。環境與帳號先準備，核心操作使用本機資料、固定 Clock 與 Mock Payment。

## 2. 故事線與人機責任

| 階段 | 人員責任 | Agent 責任 | 必要產出 |
|---|---|---|---|
| Greenfield／Tool | 理解需求、選擇方向、拆解工作、Review 與驗收 | 協助完成程式、測試與文件，依人員計畫執行 | MVP、測試紀錄、文件與變更摘要 |
| Time Skip | 停用個人 Greenfield；接手統一 B0、重新分組 | 依接手資料了解新基線 | 統一版本識別與接手資料 |
| Brownfield／Teammate | 比較獨立分析、核對證據、建立 Shared Context、核准方案 | 分析 Repository、影響、風險與缺口；提供選項及取捨 | 個人分析、Shared Context、影響分析與核准計畫 |
| B3／Digital Worker | 設定邊界、Challenge、Review、Approve／Reject、要求補充證據並承擔交付責任 | 主導需求分析、設計、實作、測試、文件與交付；遇到超範圍或矛盾時升級 | 三個 Human Gate 決策、測試與 Diff 證據、交付摘要 |

Time Skip 固定為 G1 上線後 12 個月，所有人使用主持人提供的同一 B0；不由每個人的 Greenfield 成果各自演化。依[B0 指令](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)自然延續 G1 架構與詞彙。

B1 為 Bug Fix 暖身；B2 為 Business Rule Change 與 Teammate→Digital Worker 過渡；B3 為 New Feature 與 Digital Worker。B3 人員不得直接改程式或補測試，主要 Agent 必須先通過需求理解與設計 Gate，再執行，最後提交交付 Review。主持人控制節奏、提示、例外與 Recovery，不直接解題。

## 3. 90 分鐘配置

依[B1–B3 任務指令](../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)採以下基準；這是活動配置，尚未實際演練：

| 起訖分鐘 | 長度 | 活動 |
|---|---:|---|
| 00–07 | 7 | 開場與共同認知 |
| 07–29 | 22 | Greenfield／Tool |
| 29–33 | 4 | Time Skip 與重新分組 |
| 33–39 | 6 | 個人 Agent 分析 B0，不修改程式 |
| 39–44 | 5 | 比較分析、建立 Shared Context |
| 44–52 | 8 | B1 Bug Fix |
| 52–63 | 11 | B2 Rule Change |
| 63–76 | 13 | B3 與 Digital Worker 三 Gate、例外、執行及測試 |
| 76–80 | 4 | 交付摘要與階段收斂 |
| 80–90 | 10 | 回顧與組織導入收斂 |

總計 90 分鐘，Time Skip 加 Brownfield 為 51 分鐘。任務卡按 Shared Context→B1→B2→切換操作規則→B3 揭露。時間到立即收斂；B1／B2 可依 Runbook 使用 Recovery Baseline，但需保留未完成與切換紀錄，不記成小組自行完成。

## 4. 功能與版本邊界

| 版本 | 必要能力與狀態 | 不得提前加入 |
|---|---|---|
| G0 | 可啟動骨架、Health、固定 Seed、測試 Fixture、型別與 TODO | 完整 MVP 答案或 Brownfield 功能 |
| G1 | 查詢班次、1–4 人一般訂票、成人與學生個別計價、模擬付款、Order 查詢、文件與完整測試 | 會員、提前優惠、改退票、團體訂票或學生票 Bug |
| B0 | G1 自然成長：會員、提前優惠、改退票、通知、座位與 Audit；35–45 個實質 Python／測試檔，3 項受控技術債、2 項文件落差 | B2 最有利政策或 B3 團體功能 |
| B1 | 最小修復學生票從錯誤 85% 恢復 75%；保留既有優惠選擇順序 | B2／B3 答案 |
| B2 | 逐位旅客收集優惠資格，不疊加，選最有利單一優惠；記錄 Applied Discount，改票重新計價共用政策 | 團體訂票 |
| B3 | 5–20 人、同一 Trip／車廂連續空位，不部分成立；付款失敗整筆取消、釋放全部座位、不建立 Order，保留必要 Audit 與 Notification | 外部資料庫、通用 Workflow／Transaction Framework |

優惠資格為學生 75%、提前至少 14 天 85%、企業會員 95%，成人基準 100%。B3「盡量相鄰」依專屬指令固定解釋為必須有同車廂完整連續區段，找不到就拒絕；不引入最佳化演算法。每版獨立安裝、啟動與測試；現階段沒有程式或測試驗收結果。

固定技術為 Python 3.13、FastAPI、Pydantic 2、pytest、Uvicorn、venv／pip、In-Memory 與 `src/smart_ticket/` 分層；詳見[技術標準](../../docs/instructions/01_技術棧與Repository標準指令書.md)。

## 5. 素材可見性

| 類型 | 內容 | 發放方式 |
|---|---|---|
| Participant | 任務需求、驗收條件、學員用程式、分析與操作範本 | 按階段允許清單發放，不給完整產製 Repo |
| Facilitator | 節奏、提示、介入、Bug／債務地圖與 Recovery 操作 | 主持人持有，提示逐級提供 |
| Evaluation | 標準實作、完整影響分析、測試映射、評分與驗證報告 | 主持人與評估者持有 |
| Agent Production | 產製指令、治理基線、規劃及一致性檢查 | 產製 Agent 與維護者使用 |

目錄分層不構成權限；包內連結、測試、隱藏檔與案例歷史也要檢查。不能將本治理目錄直接列入學員包；若需要共同語言，另取不揭露後續答案的摘要。詳見[一致性規則](consistency-rules.md)。

## 6. 成功標準與已知差異

工作坊成功包含有效體驗、可追溯分析、核准與 Review、實際測試證據、誠實披露缺口，以及回顧所得的 Context／Rule／Skill／平台改善事項。B3 學員 Level 1 分析完成與 Level 2 核心流程完成可作學習成果；只有 Level 3 可依完整證據宣稱完整交付。Reference Solution 必須達全部驗收，不能用學員分級降低標準。

[待協調清單](../../docs/planning/decisions-and-open-issues.md) O-01／O-02 在本基線中按總控與專屬任務規格界定適用範圍：一日／半日與角色輪轉是參考內容；通用完整 DoD 不作為學員活動成功的唯一門檻。原 `contents` 文件沒有改寫，後續主持／評估素材仍要驗證對齊。

O-03 規則編號已於 P2 完成對齊與來源同步，見[技術基線](technical-baseline.md)。2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)，O-04 規格衝突解除：B0 僅一個 `BUG-B0-001`，保留全部 28 項 G1 Regression 與正確斷言，完整實測失敗 node ID 集合須與已核實 Intentional Failure Manifest 完全一致、零非預期失敗，其餘全通過，無 Skip／XFail／未知 Warning；B1 修復後全部 G1 及 B0 新增測試恢復通過。Manifest 以 Diff／呼叫路徑及修復驗證證明因果，B0已按方案A實測驗收。O-05 的 G1 案例歷史／Tag 與 Bundle 已建立，B0 須延續並驗證隔離；O-07 的 G1 已 PASS 前置滿足，含限制通過不等於 PASS 的一般門檻保留。O-06 clean-copy已建立與核對，B0 必須保留原基線副本要求。文件完成不等於後續程式可驗收。

## 完成條件

此 Manifest 固定活動目標、故事線、時程、人機責任、版本與可見性；詞彙見[Glossary](glossary.md)，驗收與階段阻擋條件見[Acceptance Gates](acceptance-gates.md)。四份治理文件一致、來源可追溯且差異狀態明確，才可判定 P1 文件交付完成。

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
