---
id: b3-exception-card
title: Exception Response 與 Escalation
minute: 63-76
group: b3
section: B3｜Digital Worker
---

> 本頁上半部取自 B3 參與者文件 `06-exception-response-card.md`。這是空白範本，按需使用；填寫時已有核准 Work Order、Context 與當前 Gate 證據。下方兩份表單會自動暫存，可匯出或複製 Markdown。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/06-exception-response-card.md
```

## 填寫：例外回應（Exception Response）

先核對當時提議、授權與證據；60 秒內提出治理決策與給 Agent 的指令。時間緊可用 30 秒口頭判斷並留下簡短紀錄，不預填答案。

```form
{"id":"exception-response","title":"例外回應（例外 ID：EXCEPTION-DW-001）","fields":[
{"id":"within-scope","label":"這項提議是否在核准範圍內？","type":"select","options":["YES","NO","UNCLEAR"],"hint":"YES＝在範圍內；NO＝超出範圍；UNCLEAR＝尚不清楚。"},
{"id":"within-scope-basis","label":"選擇與依據","type":"textarea"},
{"id":"evidence-proposal","label":"證據｜提議內容","type":"textarea"},
{"id":"evidence-rule","label":"證據｜核准規則、限制與範圍","type":"textarea"},
{"id":"evidence-location","label":"證據｜證據位置","type":"text"},
{"id":"risk","label":"風險｜可能影響與資訊缺口","type":"textarea"},
{"id":"decision","label":"決策","type":"select","options":["APPROVE","APPROVE WITH CONDITIONS","REJECT"],"hint":"APPROVE＝核准；APPROVE WITH CONDITIONS＝附條件核准；REJECT＝拒絕。相關條件解除後才可續行。"},
{"id":"decision-text","label":"決策｜決策","type":"textarea"},
{"id":"decision-conditions","label":"決策｜條件／修正","type":"textarea"},
{"id":"decision-owner-minute","label":"決策｜決策者與分鐘","type":"text"},
{"id":"instruction-next","label":"給 Agent 的指令｜下一步指令","type":"textarea"},
{"id":"instruction-allowed","label":"給 Agent 的指令｜允許範圍","type":"textarea"},
{"id":"instruction-stop","label":"給 Agent 的指令｜仍需停止的動作","type":"textarea"},
{"id":"instruction-gate","label":"給 Agent 的指令｜須回到的 Gate","type":"text"}
]}
```

## 填寫：停止與升級處理（Escalation）

一般停止條件使用以下升級短格式；不等同新增第二個主持例外事件。Agent 提出證據，人做決策後才續行。觸發條件見 [Work Order](#b3-work-order) 的 Stop and Escalate Conditions。

```form
{"id":"escalation","title":"停止與升級處理","fields":[
{"id":"trigger","label":"觸發原因","type":"textarea"},
{"id":"evidence","label":"證據","type":"textarea"},
{"id":"impact","label":"影響","type":"textarea"},
{"id":"options","label":"可選方案","type":"textarea"},
{"id":"recommendation","label":"建議方案","type":"textarea"},
{"id":"decision-needed","label":"需要人員決定的事項","type":"textarea"}
]}
```
