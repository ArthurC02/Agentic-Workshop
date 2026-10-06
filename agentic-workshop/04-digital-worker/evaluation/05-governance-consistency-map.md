# Digital Worker 治理一致性映射

> 讀者：Evaluation、Facilitator、Agent Production。時機：素材靜態驗收及真實演練前。
> 前置：[治理指令](../../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)、B3任務／Rule Registry及本輪15必要輸出。可見性：Evaluation內部。

本表為文件靜態一致性檢查，不代表真實13分鐘工作坊已演練、已有人員Gate核准或已取得學員行為分數。B3程式驗證與治理活動驗證分開記錄。

| 06來源節 | 文件定位 | 可判定檢查 |
|---|---|---|
| §3 固定原則 | participant/01-operating-rules.md；03-approval-gates.md | Agent主導／不越界、人不Coding仍理解、重大動作有Gate、實際證據、停止升級、責任由人承擔 |
| §4 Operating Rules | participant/01-operating-rules.md | 人／Agent可做與不可做、先Gate再執行；目標2分鐘閱讀，真實閱讀時間尚未測 |
| §5 Work Order | participant/02-agent-work-order.md | 固定Mission／Requirements／Rules／Context／Allowed／Prohibited／Deliverables／Tests／Gates／Stop／Timebox，Context留空而非猜測 |
| §6 三Gate | participant/03-approval-gates.md | Gate1理解／Gate2設計／Gate3交付均有Input、Human Review、Decision、Evidence；Gate2核准才改Code |
| §7 短格式 | participant/03-approval-gates.md；facilitator/02-approval-gate-cues.md | 三種Decision、Reviewed Evidence、Conditions、Approver、Timestamp／Minute，不由Agent代核准 |
| §8 停止升級 | participant/02-agent-work-order.md；06-exception-response-card.md | 10個停止條件及Escalation六heading，衝突或超權不猜測 |
| §9 Review | participant/04-review-checklist.md | Requirement／Scope／Quality／Evidence四類，未完成保持未勾 |
| §10 Delivery | participant/05-delivery-template.md | 十二欄、Level1–3、真實Test與未驗證、風險／偏差、Agent建議不等於人員決策 |
| §11 唯一事件 | facilitator/03-exception-injection.md | EXCEPTION-DW-001 SQLite；自然提出即不再注入，假設卡不冒稱真實提議，不安裝資料庫 |
| §12 Response | participant/06-exception-response-card.md | 5欄Scope／Evidence／Risk／Decision／Instruction空白，未嵌入SQLite標準答案 |
| §13 觀察 | facilitator/01-governance-observation-guide.md | Agent／人員行為、Challenge／Review／條件、Audit／Context／Session／成本時間觀測需求 |
| §14 Cue | facilitator/02-approval-gate-cues.md | 相對0／1／3／6／7／11／12／13對應活動63–76；三Gate／例外含在13分鐘 |
| §15 Injection | facilitator/03-exception-injection.md | Gate2相對6–7分鐘；60秒可縮30秒，一件事件、剔除SQLite、先解除條件才開工 |
| §16 介入 | facilitator/04-intervention-rules.md | 越界／人Coding／跳Gate／核准SQLite／假通過／超時介入；正常選項比較不代解 |
| §17 Rubric | evaluation/01-autonomy-and-governance-rubric.md | A–E各0–3完整anchor、總15只回顧、不排名、不以程式量為唯一成功 |
| §18 Approval Evidence | evaluation/02-approval-evidence-checklist.md | 七欄＋Approver／時間／Context；條件閉環證據可核對，未核准不前進 |
| §19 Audit | evaluation/03-digital-worker-audit-template.md | 13heading，Session／Context／Rules／Gates／Files／Commands／Tests／Exceptions／Interventions／Decision／Risk皆待真實填寫 |
| §20 Exception Reference | evaluation/04-exception-reference-answer.md | Reject方案非Reject任務；In-Memory Reservation／Compensation，可選Snapshot／Token／Rollback，不強制通用框架 |
| §21 Debrief | facilitator/05-digital-worker-debrief-notes.md | Review負擔、Gate價值、證據／平台Audit、自動約束與人的責任；不以自主率競賽 |
| §22 工具中立 | 全15必要文件 | 無特定產品必要流程，Agent／Tool／Session為通用角色 |
| §23 時間壓力 | participant/01-operating-rules.md、02-agent-work-order.md；facilitator/02-approval-gate-cues.md | 必讀僅Operating／Work Order／Gates／B3任務卡；其他按需；每Gate1–3分鐘，時間不足保留Gate1／2及Gate3最小Review，例外不刪 |
| §24 一致性 | 本表；participant/02-agent-work-order.md | 17 B3新增Rule與Registry精確一致、三Gate與AC對齊、材料角色隔離、Level1–3、責任不消失 |

## 已完成的靜態核對

- 必要輸出為Participant六檔＋Facilitator五檔＋Evaluation四檔，15個來源要求檔名皆已建立；本映射與後續Validation Report為附加Evaluation文件。
- Work Order列出的17個GROUP／GROUP-PAY／GROUP-FARE／GROUP-AUDIT／GROUP-NOTIFY ID，與Rule Registry的17項集合精確一致、沒有遺漏或額外ID；B2 FARE-007–010與四票率及資格不改。
- Participant六檔唯讀檢查未出現SQLite標準回應、Reference Solution／Evaluation答案連結或完整Python實作；Exception Card是空白判讀，完整SQLite答案留在Evaluation。
- 三Gate與短格式、七欄核准證據、唯一事件、13分鐘Cue與條件閉環可在各文件定位。Rubric與Audit為空模板，未造作實際學員核准、命令、分數或Session。
- 真實2分鐘閱讀／13分鐘演練、參與者是否遵守Gate、Level1–3分布及Rubric得分尚未執行；文件靜態通過不能代替活動實證。

需要在真實演練記錄：核准Context、每Gate Approver／時間／Evidence／Conditions閉環、唯一事件來源、Agent偏差／停止、實際Test與交付範圍。最終文件驗收結果由[治理驗證報告](06-governance-validation-report.md)統一記錄。

完成條件：§3–24可對到文件及可判定檢查，15必要檔存在、17Rule集合一致、Participant無答案；實際演練未做明確揭露，所有條件未閉環不得開始對應受阻動作。
