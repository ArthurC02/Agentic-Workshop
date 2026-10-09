# Digital Worker 治理素材產製結果

> 讀者：素材維護者、Evaluation與主持人。時機：P9驗收、進入P10前。
> 前置：已驗收B1–B3與[治理指令](../../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)。可見性：Evaluation限定。

2026-10-05完成文件基線及靜態一致性驗證。**Final Decision：PASS FOR GOVERNED DIGITAL WORKER EXERCISE**。這是治理素材產製驗收；沒有執行真人閱讀、例外處理或13／90分鐘演練，也未產生最終交付包。

## 建立的檔案

| 對象 | 必要文件 |
|---|---|
| Participant，6份 | [Operating Rules](../participant/01-operating-rules.md)、[Work Order](../participant/02-agent-work-order.md)、[三 Gate](../participant/03-approval-gates.md)、[Review Checklist](../participant/04-review-checklist.md)、[Delivery Template](../participant/05-delivery-template.md)、[Exception Response](../participant/06-exception-response-card.md) |
| Facilitator，5份 | [Observation](../facilitator/01-governance-observation-guide.md)、[Gate Cues](../facilitator/02-approval-gate-cues.md)、[例外注入](../facilitator/03-exception-injection.md)、[介入規則](../facilitator/04-intervention-rules.md)、[Debrief](../facilitator/05-digital-worker-debrief-notes.md) |
| Evaluation，4份 | [Rubric](01-autonomy-and-governance-rubric.md)、[核准證據](02-approval-evidence-checklist.md)、[Audit](03-digital-worker-audit-template.md)、[例外答案](04-exception-reference-answer.md) |

另附[22項一致性映射](05-governance-consistency-map.md)、本報告與[機器可讀檢查證據](07-governance-validation-evidence.json)。共15份規定文件與3份驗證附件；固定範本欄位按原規格核對。

## Operating Rules摘要

Agent負責需求、設計、實作、測試、文件與交付；人員設定邊界、Challenge、Review及核准，不能補Code或Test。無自動修改能力的工具可產生Patch由環境套用，人員不自行補寫。必讀僅Operating Rules、Work Order、Approval Gates與B3 Task Card，其餘表單按需使用。

Operating Rules為384個中文字，另含英文識別字與標點；2分鐘閱讀是設計目標，沒有以字數估算冒稱真人實測通過。素材保持工具中立，不要求特定Plan Mode、設定檔、CLI或Subagent。

## Approval Gates

Gate1完整需求、規則、假設、缺口與Out of Scope，核准後才設計；Gate2提交影響、API／Domain、座位／補償、測試、文件、風險與預計檔案，核准後才改程式；Gate3審查Diff、真實測試、AC／Rule、文件、缺項與交付建議。

各Gate有Input、Human Review、Decision與Evidence，短決策記錄核准人、時間及條件。條件有解除證據後才執行對應範圍；不由Agent代填人員核准。Work Order先確認Context，Gate2範圍在設計核准時填入，避免在Gate1前預先完成設計。

## Stop and Escalate Conditions

十項停止觸發完整：需求／規則衝突、文件／程式無法判定、範圍外API、新依賴、移除Regression、付款狀態不明、座位與Atomicity無可行方案、無關新失敗、檔數顯著超預估及時間不足。Agent停止受影響動作，提交Trigger／Evidence／Impact／Options／Recommendation／Decision Needed，等人員決策才續行。

## Exception Event

唯一`EXCEPTION-DW-001`：Gate2提議SQLite簡化Rollback，違反固定In-Memory Constraint。Agent自然提議已算本次事件；若未提，主持人誠實以假設事件卡詢問，不假冒Agent曾提出。最多60秒，時間緊可30秒，保留事件但不重複注入，不安裝SQLite。

標準處理Reject越界方案，保留任務，要求受控In-Memory補償；條件核准必須排除資料庫且先解除條件。可接受其他不新增依賴的受控方案。標準判斷留Evaluation，Participant為空白回應卡。

## Governance Rubric

五維Requirement、Plan／Scope、Evidence／Quality、Human Oversight、Transparency，每維0–3完整Anchor，共20個評分格、最高15分，只作回顧而非排名或程式量競賽。未觀察保持未填，不把缺證據直接當0分；Level1–3與治理分數分開。

Approval七個必要證據欄位加核准人／時間／Context／條件結案；Audit13個固定Heading，記錄Session、Work Order、Context、規則、Gate、檔案、命令／測試、例外／介入、交付與風險。全部為待實際活動填寫的模板，沒有虛構學員紀錄。

## Participant／Facilitator／Evaluation隔離

15個規定檔案全部存在，UTF-8無BOM、Markdown區塊平衡、相對連結有效。Participant連結僅指本層及Brownfield學員素材，沒有標準解答、Evaluation／Facilitator／產製指令連結、完整Impact或座位演算法。僅一個例外ID。

檔案分層與內容掃描通過；Participant Package尚未產生，允許清單與包內歷史隔離留待P11，不將本檢查等同正式包驗收。

## B3規則一致性

Work Order的17個Group Rule ID與正式B3／治理Registry集合精確一致，保留B2逐旅客最低單一優惠與一般功能，不修改商業需求。主代理逐檔核對B3的59來源檔SHA256全部不變，本目標只產製治理文件。

原範本核對：Work Order11個Heading、Delivery12個Heading、Audit13個Heading。子代理獨立Review核對人機責任、條件核准、唯一事件及22條指令映射；沒有新增需阻擋交付的差異。

## Timebox適配

相對分鐘0／1／3／6／7／11／12／13對應活動63–76；Gate1於66、Gate2及事件於69、70起實作、74收斂測試、75 Review、76交付停止。例外60秒包含相對6–7分鐘，不增加總長；不足時保留Gate1／2及Gate3最低證據Review，不追求Level3。

上述為流程與時間配置檢查，真人2分鐘閱讀、60秒決策、13分鐘B3及90分鐘完整演練尚未實測。

## 已知限制與Final Decision

P10完整Runbook／回顧整合、P11跨版本與包驗證／演練尚未完成；本次未重跑程式pytest，因為所有B3來源雜湊保持且此目標為文件產製。平台權限、Approval Workflow、Audit、Context Versioning、Session、成本與時間觀測是需求萃取欄位，未實作平台。

完成條件：必要15文件、責任／Gate／升級／唯一例外、評估與隔離、B3一致性及時程設計完成，未驗證事項明列。**Final Decision：PASS FOR GOVERNED DIGITAL WORKER EXERCISE**。
