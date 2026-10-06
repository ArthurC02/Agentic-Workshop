# 素材產製路線與驗收順序

> 目標讀者：Repo 維護者、素材產製 Agent、工作坊設計者與主持人。
> 使用時機：安排後續產製任務、判定階段是否可往下推進，以及規劃演練與交付時。
> 前置條件：閱讀 [Repo 結構規劃](repository-structure.md)、[總控指令書](../instructions/00_Agentic工作坊素材產製總控指令書.md) 與本階段適用的產製規格。
> 狀態：2026-10-05 更新；P0–P6已完成，P7 B2已產製並實測通過；P8 B3已實測，P9文件基線已完成並驗證，P10文件基線已完成並驗證，P11真實演練／打包未完成。

## 目前進度

2026-10-05 P7 B2實測完成、個別B2 Gate PASS：獨立Python3.13.15環境依賴安裝成功，55 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（1.21s）。Health／11個OpenAPI路徑、企業＋提前混合成人595／學生525／Total1120、付款、改票至T005新價1199／差額79、退票、通知3／Audit4及Reset Smoke通過。B1原52檔雜湊不變；B2快照54檔，保留原28項G1正確斷言，原13測試檔只有test_advance政策案例遷移，新增11項B2測試。逐旅客最低rate、不疊加、Applied Discounts、改票共用政策與折扣文件同步；TASK-B2-001、13項AC及主持材料已建立。案例Tag `b2-best-single-discount`與Bundle已驗證：14個真實Commit，54檔Clone比對零差異，B1為祖先且無B3歷史。詳見 [B2 Validation Report](../../agentic-workshop/03-brownfield/evaluation/15-b2-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/16-b2-validation-evidence.json) 與 [案例歷史／Delta](../../agentic-workshop/03-brownfield/evaluation/17-b2-case-history-and-delta.md)。此為P7當時範圍與證據；目前B3與B1–B3素材驗收見下方P8紀錄，真實演練及最終交付仍待完成。

B0前置協調[方案A](b0-regression-gate-proposal.md)已於2026-10-05由使用者「套用」核准，指令書與治理Gate已同步：一個Bug、完整明列失敗manifest、零非預期失敗、B1全部恢復。O-04規格衝突已解除；P5已實際產製与驗收：38實質Python檔／44測試；正式5failed39passed（0.44s）全部與manifest相等，診斷只修一行44passed（0.32s）；API Smoke／Uvicorn Health、36規則追溯、52檔clean-copySHA256一致，案例Tag392d920／Bundle續G1。詳見B0 Validation Report。P6正式B1已完成：44passed／1已知Warning（1.00s），五項失敗恢復，原測試／優惠順序不變、52檔來源与案例Tag a1c1d45／Bundle核對。Task卡／主持提示／七AC追溯／版本矩陣已產製，P7 B2已產製並實測通過，P9完整Digital Worker治理文件基線已完成，P10文件基線已完成，P11尚未啟動。

P3 G0 Starter Kit已建立：Participant五文件與26檔Starter、Facilitator四文件、Evaluation三文件。Python版本依使用者新授權統一3.13；隔離環境實測3.13.15，依賴安裝與pip check成功，Health／OpenAPI／Uvicorn／Seed Reset通過，pytest為1 passed、8 skipped、1項已記錄相容Warning。保留11主要TODO與未實作核心功能。完整證據見[G0 Validation Report](../../agentic-workshop/01-greenfield/evaluation/03-g0-validation-report.md)。22分鐘是活動設計，未完成真實學員演練。P4 G1已完成：獨立Python3.13.15環境安裝與pip check成功，28 passed／0 Skip／0 XFail／1已知Warning（0.21s），Import／Health／OpenAPI／端到端Smoke／Reset通過，16Rule／15AC追溯齊備，Final Decision PASS。真實案例Bundle包含G0→G1五提交，Tag G1=361bf00，重新Clone與30檔快照內容一致。詳見G1 Validation Report及Case History。

P0 結構規劃已完成。P1 已建立 [Manifest](../../agentic-workshop/00-governance/workshop-manifest.md)、[Glossary](../../agentic-workshop/00-governance/glossary.md)、[一致性規則](../../agentic-workshop/00-governance/consistency-rules.md) 與 [Acceptance Gates](../../agentic-workshop/00-governance/acceptance-gates.md)。本階段檢查涵蓋四份文件的目標、版本、詞彙、責任、可見性、來源與 Gate；沒有執行程式測試或活動演練。

O-01／O-02 已界定本次適用對象，原概念文件及後續主持／評估教材仍需對齊。O-03 已於 P2 完成編號對齊，O-05已落實G0／G1歷史、O-07已有G1 PASS；O-04規格衝突已核准解除，O-06及B0本階段驗收已完成。已建立 [技術基線](../../agentic-workshop/00-governance/technical-baseline.md)、[Rule Registry](../../agentic-workshop/00-governance/rule-traceability-baseline.md) 與 [版本驗證要求](../../agentic-workshop/00-governance/version-validation-requirements.md)。P2當時只驗證文件；後續P3／P4已有實測結果，本次Gate同步不代表B0已驗收。

P1 文件驗證紀錄（2026-10-05）：四份治理文件具讀者、時機、前置、可見性與完成條件；治理／規劃／Agent 共 98 個相對連結有效；Markdown 區塊平衡；Manifest 十段時程加總 90 分鐘。獨立審查對照原規格，B0 Gate 已明寫保留全部 G1 Regression 且全部通過，同時保留 O-04 衝突未解除不得宣稱符合的限制。這些證據支持P1文件交付完成，不支持後續程式或演練通過；其中B0失敗門檻已由2026-10-05核准方案A取代。

P2 文件驗證紀錄（2026-10-05）：Registry 的57個唯一 Rule ID 與 G0／B0／B1–B3 來源規則集合逐項一致，無漏項或重複；技術標準與 G0／G1 的 BOOKING-002／003 定義已對齊。治理／規劃／Agent 的134個相對連結有效，Markdown區塊平衡。子代理審查已修正錯誤格式的例示說明，未發現業務語意或版本門檻變更；O-04–O-07保留。下一階段為P3 G0產製，不由文件檢查推定Runtime已通過。

## 1. 推進原則

產製順序固定為治理基線 → 技術標準確認 → G0 → G1 → Time Skip／B0 → B1 → B2 → B3 → Digital Worker 治理 → 主持與回顧 → 全域驗證、演練與打包。每階段完成後先檢查一致性與實際證據，再進入下一階段。

`docs/instructions/` 已有 00–06 指令書，後續依其要求產製成果，不重複建立同義規格。總控另要求的主持 Runbook、Evaluation 與全域驗證指令仍須在正式產製時補齊或明確界定適用要求。各階段 Evaluation 與 Reference Solution 應隨該階段建立，最後再整合驗證，不延後到全部教材寫完才驗收。

規格差異集中記錄於 [決策與待協調事項](decisions-and-open-issues.md)。它們不阻擋目前規劃文件落地，但涉及規則編號、測試期待或交付目錄的差異，須在相應產製階段前協調；規劃建議不等同已核准變更。發現新衝突時記錄來源、影響與待決策內容，不自行修改需求或弱化測試。

## 2. 分階段輸入、輸出與 Gate

下表中的階段成果位於 `agentic-workshop/`；目前P0–P6已驗收、P7已產製並實測通過，P8 B3已驗收，P9文件基線已完成並驗證，P10文件基線已完成並驗證，P11是後續要求。Gate 指素材產製驗收，不是 B3 活動中的人員核准 Gate。

| 階段 | 前置輸入 | 預定輸出 | 驗收 Gate 與進入下一階段條件 |
|---|---|---|---|
| P0：結構規劃 | 既有 docs、已提出的目錄方案、使用者授權範圍 | `docs/planning/` 三份規劃文件 | 位置、版本、交付隔離、產製順序與待協調差異均可追溯；不建立教材或程式 |
| P1：治理基線 | 總控、規劃文件、已核准決策 | `00-governance/` 的 Manifest、Glossary、Consistency Rules、Acceptance Gates | 案例、90 分鐘、工具中立、人機角色、Rule ID 與可見性一致；差異有狀態與處理時點 |
| P2：技術基線確認 | P1、[技術標準](../instructions/01_技術棧與Repository標準指令書.md) | 技術標準適用紀錄、版本驗證要求與規則追溯基線 | Python 3.13／FastAPI／Pydantic 2／pytest／Uvicorn、venv／pip、`src/smart_ticket/` 與 In-Memory 邊界確立；沒有外部 API 或真實付款依賴；Rule ID 衝突已協調 |
| P3：G0 Starter Kit | P1–P2、[G0 指令](../instructions/02_Greenfield_Starter_Kit產製指令書.md) | `01-greenfield/participant/` 教材與 `starter-repository/`；主持指南、評估表與 G0 驗證報告 | 乾淨環境可安裝、啟動及檢查健康；未完成功能以受控 TODO 與明確理由的 Skip 表示；不含 G1 答案；22 分鐘任務範圍合理 |
| P4：G1 Reference MVP | 已驗收 G0、[G1 指令](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md) | `01-greenfield/evaluation/reference-solution/greenfield-reference-mvp/`、G0→G1 Delta、驗證與追溯文件 | 查詢、訂票、模擬付款、訂單查詢可驗證；完整測試通過、無 Skip／XFail；驗證報告記錄實際結果。進 B0 前依 B0 的較嚴前置要求取得 PASS |
| P5：Time Skip 與 B0 | 已 PASS 的 G1、[B0 指令](../instructions/04_B0_Brownfield_Repository演化產製指令書.md) | `02-time-skip/`；`03-brownfield/participant/repository/smart-ticket-b0/`；接手分析教材、主持提示、B0 評估報告與規格要求的基線副本 | 自然延續 G1，具35–45個實質Python／測試檔；僅BUG-B0-001，實測失敗集合與已核實manifest一致、零非預期失敗，保留完整G1 Regression與正確斷言；無Skip／XFail／未知Warning，B1須全部恢復；Final Decision為 `PASS AS BROWNFIELD BASELINE` |
| P6：B1 Bug Fix | 已驗收 B0、[任務與版本指令](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md) | B1 任務卡、漸進提示、影響分析、驗收對照與 `03-brownfield/evaluation/reference-solutions/b1-student-fare-fixed/` | 學生票由錯誤 85% 修為 75%；保留 B0 其他能力；完整測試通過，無 Skip／XFail；任務卡沒有標準答案位置 |
| P7：B2 規則變更 | 已驗收 B1、同一任務指令 | B2 任務卡、跨模組影響與追溯、`reference-solutions/b2-best-discount-policy/` | 提前 14 天 85%、企業會員 95%、學生 75% 的優惠不疊加，取旅客最有利單一優惠；Pricing、Booking、Member、Test、Document 一致；保留 B1 修復與 Regression |
| P8：B3 新功能 | 已驗收 B2、同一任務指令 | B3 任務卡、測試與文件對照、`reference-solutions/b3-group-booking/`、B0–B3 版本矩陣與驗證報告 | 5–20 人、同車廂連續座位、不得部分成功、付款失敗整筆取消與座位釋放、B2 旅客優惠及 Audit／Notification 規則均有證據；Reference 完整測試通過、無 Skip／XFail／未知失敗；B1–B3 整體 Final Decision 為 `PASS FOR WORKSHOP USE` |
| P9：Digital Worker 治理 | B0–B3 規格與解答已確立、[治理指令](../instructions/06_Digital_Worker治理與操作規則產製指令書.md) | `04-digital-worker/` 的操作規則、Work Order、三 Gate、Review、交付／升級範本、例外卡、主持觀察與 Rubric | 人員僅 Challenge／Review／Approve／Reject；Gate 有提交、決策與證據；唯一 SQLite 超範圍例外在時間內可判斷；不變更 B3 需求；Final Decision 為 `PASS FOR GOVERNED DIGITAL WORKER EXERCISE` |
| P10：主持、回顧與評估整合 | P1–P9 成果、[既有主持內容](../contents/08_時程安排與主持指南.md)、[評估參考](../contents/07_評估指標與回顧方法.md) | `05-retrospective/`、`06-runbook/`、完整主持節奏、Preflight、Recovery、提示與評估索引 | 全流程按 90 分鐘重新組織；按階段發任務；主持文件具時間點、觀察、提示與中止條件；Recovery 可接續體驗且不洩漏答案；評估包含治理與未完成事項 |
| P11：全域驗證、時間演練與打包 | 各階段已驗收成果、整合評估與 Runbook | 未來 `scripts/` 驗證／打包工具；未來 `dist/` 分角色、分階段交付包；演練與隔離報告 | 各版本獨立安裝／啟動／測試與 API Smoke；Requirement→Rule→Code→Test→Document→Evaluation 可追溯；90 分鐘演練有實際記錄；包內容與歷史均無答案洩漏；未完成或失敗不宣稱通過 |

G1 指令允許記錄不影響工作坊的限制，但 B0 指令明定前置報告為 PASS；因此 `PASS WITH DOCUMENTED LIMITATION` 不直接視為已通過 B0 前置條件，須先解除限制或取得明確核准。

## 3. 版本與證據的累積

G0 → G1 → B0 → B1 → B2 → B3 為固定來源鏈。每版是可獨立安裝、啟動與測試的完整快照，與上一版的差異由 Delta、版本矩陣與規則追溯記錄。B1–B3 各自保留前版能力，避免把修復、政策與團體功能混成無法辨識的單一成果。

後續可在受控產製流程加入版本標記與內容雜湊，供打包工具追溯快照來源；G0／G1案例歷史已由獨立Git Repository建立並保存Evaluation Bundle；本機文件 Commit 依使用者收尾授權執行。B0 Evaluation 基線副本的保留與去重方案尚待協調，先依現行 B0 指令保留產製需求，不自行取消。

每版驗證報告至少記錄來源版本、環境／依賴、執行命令、實際通過／失敗／Skip／XFail、API Smoke 結果、Rule 與 Acceptance 對照、隔離檢查、已知限制及 Final Decision。B0 的預期失敗須具明確身分，不能只接受「測試有一個失敗」。G0 的受控 Skip、B0 的刻意失敗與 G1／B1–B3 全通過是不同 Gate，不用單一全綠條件取代。

## 4. 90 分鐘活動配置

以下沿用任務指令的基準，時間採自活動開始起算的分鐘區間。這是素材適配與演練目標，不代表已完成演練。

| 工作坊分鐘 | 長度 | 活動 | 素材與發放條件 |
|---|---:|---|---|
| 00–07 | 7 分鐘 | 開場、目標與操作說明 | 工具中立說明、任務邊界 |
| 07–29 | 22 分鐘 | Greenfield／Tool，個人 MVP | G0 Starter Kit；G1 不發給學員 |
| 29–33 | 4 分鐘 | Time Skip、重新分組、統一接手 B0 | 停用個人 Greenfield，發統一 B0 與接手資料 |
| 33–39 | 6 分鐘 | 個人 Agent 獨立分析 | 個人分析表；每人使用自己的 Agent |
| 39–44 | 5 分鐘 | 小組比較、建立 Shared Context | 整合證據與資訊缺口，選主要 Agent |
| 44–52 | 8 分鐘 | B1／Teammate：Bug Fix | Shared Context 完成後發 B1 |
| 52–63 | 11 分鐘 | B2／Teammate：規則變更 | B1 通過或時間到後發 B2；需要時按 Runbook 切換 Recovery |
| 63–76 | 13 分鐘 | B3／Digital Worker：團體訂票 | B2 通過或時間到後切換治理規則，發 B3 與 Work Order |
| 76–80 | 4 分鐘 | 交付摘要與階段收斂 | 實際測試結果、完成度、風險與交付決策 |
| 80–90 | 10 分鐘 | 回顧與組織導入 | 成熟度比較、控制點、平台與治理需求 |

Time Skip 加 Brownfield 共 51 分鐘；Digital Worker 是其中 B3 的 13 分鐘，不額外增加另一段活動。Runbook 可按規格微調 1–2 分鐘，但仍須總計 90 分鐘並保留三種成熟度體驗。

B3 的 13 分鐘包含 Gate 1 需求理解、Gate 2 影響與設計、執行、Gate 3 交付審查，以及一個 SQLite 例外。依治理指令以第 3 分鐘作 Gate 1 決策、第 6 分鐘作 Gate 2 決策與例外、第 7 分鐘開始執行、第 11 分鐘收斂測試、第 12 分鐘 Review、第 13 分鐘交付摘要。演練須驗證短格式和提示足以支援此節奏，不能藉增加活動時間掩蓋素材過量。

## 5. 時間到、Recovery 與完成度

任務按 Shared Context → B1 → B2 → Digital Worker 規則 → B3 順序發放。若 B1／B2 未完成而時間到，由主持人依 Recovery Plan 決定是否發受控下一階段起點；保留原始成果、失敗與切換紀錄，不把 Recovery 視為小組完成任務。

B3 學員可以交付 Level 1（分析完成）、Level 2（核心流程完成）或 Level 3（完整交付），並據實揭露測試、缺口與風險。學員有限時間中的完成度，不降低 B3 Reference Solution 的完整驗收要求。時間不足仍保留 Gate 1／2，Gate 3 至少審查測試證據與未完成事項；例外可縮為 30 秒判斷，不直接刪除。

主持與 Evaluation 用完成度及治理證據回顧，不以程式量或競賽名次代替學習成果。

## 6. 交付前隔離與演練

後續打包依明確允許清單產生 Participant、Facilitator、Evaluation 包；Participant 再依 G0、B0 接手、B1、B2、B3 與治理材料分批發放。文件目錄分層不代表存取控制，學員不應取得含全部解答的製作 Repo、產製指令或完整歷史。

檢查每個包的文件、程式、測試、隱藏檔、指向外部答案的相對連結與 Git 歷史。測試中用於學員驗收的規則可保留，但不能混入主持提示、完整影響分析、Reference Solution 或例外標準答案。B1／B2 Recovery 起點若要提供，應按發放時機另行整理，不直接發 Evaluation 目錄。

演練至少驗證乾淨環境安裝、各版本 Gate、無外部服務的核心流程、統一 B0 交接、分批任務發放、Recovery 路徑、13 分鐘 B3 治理及完整 90 分鐘節奏。記錄實測時間與問題後修正素材，再決定交付；`dist/` 為可重新產生的成果，未來不納入版本追蹤。

## 完成條件

本規劃完成的條件是：產製先後與來源版本明確；每階段具有輸入、輸出位置與驗收條件；90 分鐘配置可加總且 B3 治理納入其中；版本測試差異、分批發放、隔離、Recovery 與實際證據要求明確；待協調規格保留待決策狀態；P0 僅建立規劃文件；P1 進度另見本次適用紀錄。

未來整套素材完成則須逐階段通過 Gate，具備獨立可執行的 G0／G1／B0–B3、完整治理／主持／回顧與評估成果、實際驗證及時間演練記錄、通過隔離檢查的交付包。這些是未來驗收要求，並非本次已完成項目。

2026-10-05 P8正式B3已產製並實測，個別Gate PASS：獨立Python3.13.15環境安裝成功，75 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（0.58s），55原案例＋20團體新增。Import／Health／13個OpenAPI路徑／Uvicorn Health（2.17s）及Smoke通過：5人混合團體總價2905（學生75%、成人提前85%）、同車廂連續、成功唯一Order、已付款退票、付款失敗CANCELLED／全釋放／無Order、Audit2／通知1與Reset。57規則、19項AC、三Gate、任務卡與主持節奏齊備；案例Tag b3-group-booking=`ca3e5de7adca290f555d9ab96f322f65345b3e90`；Bundle73,670 bytes、17個真實Commit，Clone59來源檔比對零差異；B2來源54檔雜湊凍結、原55案例對應15測試檔字節一致。B1–B3標準素材Final Decision為PASS FOR WORKSHOP USE，僅代表三版標準實作素材；不代表P9完整Operating Rules／Work Order／治理模板、13分鐘或90分鐘真實演練、打包與正式交付已完成。這是P8當時的範圍界線；目前P9狀態見後續紀錄。

詳見 [B3 Validation Report](../../agentic-workshop/03-brownfield/evaluation/18-b3-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/19-b3-validation-evidence.json)、[案例歷史／Delta](../../agentic-workshop/03-brownfield/evaluation/20-b3-case-history-and-delta.md) 與 [B1–B3素材驗收](../../agentic-workshop/03-brownfield/evaluation/21-b1-b3-production-result.md)。

2026-10-05 P9治理文件基線完成，Final Decision為PASS FOR GOVERNED DIGITAL WORKER EXERCISE：15份規定輸出加追溯／驗證報告／證據共18份（17 Markdown＋1 JSON）。17份Markdown的40個相對連結有效、UTF-8無BOM、Code Fences平衡；Participant無答案或內部越界連結。唯一EXCEPTION-DW-001、Work Order17項Group Rule與B3精確相等、Work Order11／Delivery12／Audit13個規定欄位均符合；Operating Rules約384個中文字。B3原59來源檔SHA256全部不變。獨立審查22項指令映射、三人員Gate及時程一致，無阻擋問題。此PASS只涵蓋治理文件一致性及時程設計，不等於學員Gate1／2／3已實際核准；兩分鐘閱讀、13分鐘活動與60秒例外尚未真實演練，Rehearsal／Package為NOT RUN。此為P9當時範圍，P10目前進度見後續紀錄；P11全域驗證與交付包未完成。

證據依[P9 Governance Validation Report](../../agentic-workshop/04-digital-worker/evaluation/06-governance-validation-report.md)核對，判定及實際靜態結果已核對；真實演練與打包仍未執行。

2026-10-05 P10主持／回顧文件基線PASS：新07指令整合既有要求；11份輸出為10 Markdown＋1 JSON（回顧學員2／主持2／評估索引1、Runbook4、Validation Report及證據JSON）。10份Markdown的131個相對連結有效、UTF-8無BOM、Code Fences平衡，Participant無答案或越界內部連結。主流程十段連續且無重疊加總90分鐘；Time Skip至Brownfield交付51分鐘、B3 13分鐘、回顧10分鐘；唯一EXCEPTION-DW-001包含於69–70分鐘。B3原59來源檔與P9原17份Markdown雜湊不變。O-01時程／角色及O-02完整Reference DoD／學員Level在新文件對齊；此PASS僅文件一致性與時程設計，不以空Preflight表當已執行證據。實際Preflight、真人90分鐘／13分鐘演練、Recovery演練與受控包生成均NOT RUN；O-01／O-02的演練解除證據仍待P11。下一階段P11全域驗證、受控打包與真人演練未啟動。

來源與已核對的文件驗證證據：[P10產製指令](../instructions/07_主持Runbook與回顧整合產製指令書.md)；[P10 Validation Report](../../agentic-workshop/06-runbook/evaluation/p10-validation-report.md)。

## P11 本輪執行狀態

2026-10-05 使用者「進入下一個目標」啟動P11，並選擇本次安排真人演練。六版本輪pip check、pytest、API Smoke與實際Uvicorn Health／OpenAPI通過；G0為1pass／8受控skip，G1為28pass，B0為39pass／5精確Manifest失敗，B1／B2／B3為44／55／75pass。已生成13份受控候選ZIP，B1／B2解壓Recovery副本44／55測試與Smoke通過；使用既有獨立venv，未宣稱新安裝。候選包以最終白名單／Hash與本輪報告為準；真人演練人員、時段與記錄者尚待提供，未執行90分鐘活動。P10及先前紀錄中的未啟動／未打包均為當時狀態，不作本輪結果。P11整體與正式發布仍待驗收；O-01／O-02真人證據解除條件保留。

依據：[P11指令](../instructions/08_全域驗證與受控打包產製指令書.md)；[本輪驗證報告](../../agentic-workshop/06-runbook/evaluation/p11-validation-report.md)。

## 一致性審查後的優先修正

2026-10-05 使用者要求設為新目標並優先處理審查發現。先前候選360cb551f76eeb73的清單／Hash／連結與Recovery技術通過不涵蓋教學語意；該包已停止用於本次演練。修正初始B0答案洩漏、恢復兩份受控落差與三份安全ADR，並對齊任務揭露、Level1交付、Recovery、B2合約勘誤、Mission／空白例外卡發放與歷史狀態。凍結程式／測試／案例來源保持，P9／P10歷史JSON不改寫。新候選與實際驗證以本輪報告為準；真人演練及正式放行仍待驗收，O-01／O-02真人證據解除條件保留。

依據：[修正指令](../instructions/09_教材一致性修正與交付重驗指令書.md)；[一致性修正報告](../../agentic-workshop/06-runbook/evaluation/consistency-correction-report.md)。
