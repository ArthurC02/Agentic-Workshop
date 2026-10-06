# Repository 資料夾結構規劃

> 目標讀者：Repo 維護者與素材產製 Agent。
> 使用時機：規劃素材存放位置、開始各階段產製或準備交付包時。
> 前置條件：閱讀[總控指令書](../instructions/00_Agentic工作坊素材產製總控指令書.md)與本階段產製指令。
> 狀態：2026-10-05 更新；P0–P6已完成；P7 B2已產製並實測通過，B3已完成，P9治理模板已完成並通過文件驗證，最終工具／交付仍待產製。

## 1. 結構原則

保留既有 `docs/contents/` 與 `docs/instructions/`，正式教材集中於 `agentic-workshop/`。P0–P2規劃與治理／技術文件已建立；P3 G0學員素材與骨架、P4 G1隔離解答與實測證據已完成。P5 Time Skip／B0已驗收并含原要求clean-copy、隔離診斷及案例Bundle。P6正式B1与其任務卡／主持／評估已完成，P7 B2快照／任務卡及主持材料已建立並實測通過，P8 B3與本任務Gate素材已完成，P9完整治理文件基線已完成，正式打包工具與交付包尚未建立。

本規劃沿用總控的階段目錄，階段內檔名與細節以專屬指令書為準。規劃建議不得覆蓋未調整的正式規格；差異記錄於[決策與待協調事項](decisions-and-open-issues.md)。

## 2. 預定目錄

```text
/
├── Agent.md                         # Agent 工作入口（已建立）
├── README.md                        # 後續 Repo 導覽
├── .gitignore                       # 後續排除環境與生成檔
├── docs/
│   ├── contents/                    # 既有概念、流程與範本
│   ├── instructions/                # 既有及後續產製指令
│   └── planning/
│       ├── repository-structure.md
│       ├── production-roadmap.md
│       └── decisions-and-open-issues.md
├── agentic-workshop/
│   ├── 00-governance/
│   │   ├── workshop-manifest.md
│   │   ├── glossary.md
│   │   ├── consistency-rules.md
│   │   ├── acceptance-gates.md
│   │   ├── technical-baseline.md
│   │   ├── rule-traceability-baseline.md
│   │   └── version-validation-requirements.md
│   ├── 01-greenfield/
│   │   ├── participant/
│   │   │   ├── 01-mission-brief.md
│   │   │   ├── 02-business-requirements.md
│   │   │   ├── 03-acceptance-criteria.md
│   │   │   ├── 04-agent-usage-guide.md
│   │   │   ├── 05-submission-checklist.md
│   │   │   └── starter-repository/   # G0
│   │   ├── facilitator/
│   │   └── evaluation/
│   │       └── reference-solution/
│   │           └── greenfield-reference-mvp/ # G1
│   ├── 02-time-skip/
│   │   ├── participant/
│   │   └── facilitator/
│   ├── 03-brownfield/
│   │   ├── participant/
│   │   │   ├── repository/
│   │   │   │   └── smart-ticket-b0/   # B0
│   │   │   ├── 01-system-context.md
│   │   │   ├── 02-known-constraints.md
│   │   │   ├── 03-individual-analysis-sheet.md
│   │   │   ├── 04-shared-context-template.md
│   │   │   └── task-cards/
│   │   │       ├── 01-b1-student-fare-bug.md
│   │   │       ├── 02-b2-discount-policy-change.md
│   │   │       └── 03-b3-group-booking.md
│   │   ├── facilitator/
│   │   └── evaluation/
│   │       ├── reference-baseline/
│   │       │   └── smart-ticket-b0-clean-copy/
│   │       └── reference-solutions/
│   │           ├── b1-student-fare-fixed/
│   │           ├── b2-best-discount-policy/
│   │           └── b3-group-booking/
│   ├── 04-digital-worker/
│   │   ├── participant/
│   │   ├── facilitator/
│   │   └── evaluation/
│   ├── 05-retrospective/
│   │   ├── participant/
│   │   └── facilitator/
│   └── 06-runbook/
│       ├── workshop-runbook.md
│       ├── environment-setup.md
│       ├── preflight-checklist.md
│       └── recovery-plan.md
├── scripts/
│   ├── validate_structure.py
│   ├── validate_versions.py
│   └── build_packages.py
└── dist/
    ├── participant/
    ├── facilitator/
    └── evaluation/
```

樹狀圖省略各專屬指令已列出的主持文件、評估矩陣、驗證報告與 ADR；省略不表示取消。完整檔案要求分別見 [G0](../instructions/02_Greenfield_Starter_Kit產製指令書.md)、[G1](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)、[B0](../instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[B1–B3](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md)與[治理素材](../instructions/06_Digital_Worker治理與操作規則產製指令書.md)。

## 3. 各層責任與可見性

| 位置／類型 | 責任 | 交付對象 |
|---|---|---|
| `docs/contents/` | 通用工作坊概念與方法參考 | 維護者；經整理後再選入教材 |
| `docs/instructions/` | Agent Production 的正式產製依據 | 維護者與產製 Agent |
| `docs/planning/` | 存放、產製順序、決策與規格差異 | 維護者與產製 Agent |
| `00-governance/` | 全域詞彙、版本、Rule ID 與驗收要求 | 維護者；學員只取得明確選定的通用摘要 |
| `participant/` | 業務需求、任務卡、操作指引與學員程式 | 依活動階段提供學員 |
| `facilitator/` | 節奏、提示、介入與復原操作 | 主持人 |
| `evaluation/` | 答案、完整影響分析、追溯矩陣及驗證證據 | 主持人與評估者 |
| `06-runbook/` | 全場執行與復原 | 主持人；環境準備文件可另選入學員包 |
| `scripts/` | 結構檢查、版本驗證及打包 | 維護者 |
| `dist/` | 從明確來源生成的交付物 | 依權限與階段分發 |

同一規格只維護於正式來源，教材引用相同 Rule ID。程式版本自己的 `docs/` 說明該版本行為，不複製整份產製指令。

## 4. 程式版本的共同結構

每個版本目錄都是獨立執行單位，不依賴其他版本目錄的 Import 或共享可變資料：

```text
<版本目錄>/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── docs/
├── src/
│   └── smart_ticket/
│       ├── main.py
│       ├── api/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       └── schemas/
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

使用 Python 3.13、FastAPI、Pydantic 2、pytest、In-Memory Repository。B0 自 G1 自然擴充；固定 Seed、可注入 Clock、可控制付款結果及測試重置機制應保持可追溯。

## 5. 版本與副本管理

| 版本 | 正式來源（皆位於 `agentic-workshop/`） | 演化與驗證 |
|---|---|---|
| G0 | `01-greenfield/participant/starter-repository/` | 骨架、Health 通過、明確 Feature Skip |
| G1 | `01-greenfield/evaluation/reference-solution/greenfield-reference-mvp/` | 從 G0 完成 MVP；無 Skip／XFail |
| B0 | `03-brownfield/participant/repository/smart-ticket-b0/` | 從G1成長；方案A已核准，一個Bug、全部實測失敗符合已核實manifest、零非預期失敗；保留完整Regression |
| B1 | `03-brownfield/evaluation/reference-solutions/b1-student-fare-fixed/` | 從 B0 最小修復；全部通過 |
| B2 | `03-brownfield/evaluation/reference-solutions/b2-best-discount-policy/` | 從 B1 導入逐位最有利單一優惠；全部通過 |
| B3 | `03-brownfield/evaluation/reference-solutions/b3-group-booking/` | 從 B2 加入團體訂票與補償；全部通過 |

每個版本以 README、版本歷史與 Validation Report 明確識別。跨版本以 G0→G1 Delta、G1→B0 Delta、B0→B3 Matrix 記錄演化，不要求獨立版本間逐行同步。正式規則變更後要檢查所有受影響版本及文件。

B0 Evaluation 的 clean-copy 暫保留原規格路徑，作為不可直接人工修改的基線副本；生成與一致性檢查方式應於 B0 產製前定義。移除該副本或改用版本標記屬待協調建議，尚未生效。

目前的獨立目錄不等同 Git 分支或 Tag。後續如需教材 Git History，須讓隔離的案例歷史延續 G0→G1→B0→B3，並明確指出每個 Tag 指向哪個案例版本。根 Repo 的 Tag 不能直接當成可獨立使用的案例 Repository。若無法建立真實歷史，依指令提供明確標為模擬的 commit plan／timeline，不宣稱已建立 Commit。不執行案例歷史相關 Git 操作；作者 Repo 的本機文件 Commit 依使用者收尾授權執行。

## 6. 交付包隔離與發放

學員不取得完整產製 Repo。單純拆目錄無法防止學員看到標準答案；後續打包應以檔案允許清單產生各階段資料：

| 包／階段 | 選入內容 | 排除內容 |
|---|---|---|
| Greenfield | G0、任務簡介、需求、驗收與操作指南 | G1、Evaluation、Facilitator、產製指令 |
| Time Skip／B0 | 時間快轉、B0、已知限制、分析表與 Shared Context 範本 | clean-copy、答案地圖、B1–B3、尚未發放任務卡 |
| B1 任務包 | 第一張任務卡 | B2／B3 任務卡及答案 |
| B2 任務包 | 第二張任務卡 | B3 任務卡及答案 |
| B3／Digital Worker | 第三張任務卡與治理操作文件 | 治理評估答案、例外標準回應、標準實作 |
| 回顧 | 學員反思表與成熟度比較 | 主持人觀察與評分紀錄 |
| Facilitator | 主持指南、發放節奏、提示與受控 Recovery Package | 無必要公開的工作環境資料 |
| Evaluation | 標準實作、追溯矩陣與驗證報告 | 個人憑證與私人 Session 資料 |

打包時排除 `.git/`、`.venv/`、快取、未選入檔案及指向答案的連結。需要教學歷史時僅提供經檢查、不含後續答案的隔離案例歷史。G1／B1／B2 復原版本由主持人按需發放。

`dist/` 是可重新生成的輸出，不是第二份教材來源；後續 `.gitignore` 應排除它。包內記錄版本識別、來源、允許清單與驗證摘要，以便重建與核對。

## 7. 本階段完成條件

- 目錄、責任、版本來源與可見性已定義。
- 版本可獨立執行及跨版本追溯方式已規劃。
- 交付包與分階段發放規則已定義。
- 規格變更建議清楚列為待協調。
- 產製步驟另見[產製路線](production-roadmap.md)；本文件不表示已完成任何教材、程式或打包工具。

2026-10-05 P7 B2實測完成、個別B2 Gate PASS：獨立Python3.13.15環境依賴安裝成功，55 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（1.21s）。Health／11個OpenAPI路徑、企業＋提前混合成人595／學生525／Total1120、付款、改票至T005新價1199／差額79、退票、通知3／Audit4及Reset Smoke通過。B1原52檔雜湊不變；B2快照54檔，保留原28項G1正確斷言，原13測試檔只有test_advance政策案例遷移，新增11項B2測試。逐旅客最低rate、不疊加、Applied Discounts、改票共用政策與折扣文件同步；TASK-B2-001、13項AC及主持材料已建立。案例Tag `b2-best-single-discount`與Bundle已驗證：14個真實Commit，54檔Clone比對零差異，B1為祖先且無B3歷史。詳見 [B2 Validation Report](../../agentic-workshop/03-brownfield/evaluation/15-b2-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/16-b2-validation-evidence.json) 與 [案例歷史／Delta](../../agentic-workshop/03-brownfield/evaluation/17-b2-case-history-and-delta.md)。此為P7當時範圍與證據；目前B3與B1–B3素材驗收見下方P8紀錄，真實演練及最終交付仍待完成。

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
