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
{"id": "exception-response", "title": "例外回應（例外 ID：EXCEPTION-DW-001）","fields":[
{"id": "within-scope", "label": "這項提議是否在核准範圍內？", "type": "select", "options": ["是（YES）", "否（NO）", "不確定（UNCLEAR）"], "hint": "YES＝在範圍內；NO＝超出範圍；UNCLEAR＝尚不清楚。"},
{"id": "within-scope-basis", "label": "選擇與依據", "type": "textarea", "suggestions": [{"label": "依據", "text": "〈YES／NO／UNCLEAR〉：依〈Work Order／Gate 2 核准範圍／操作規則〉，〈理由〉"}]},
{"id": "evidence-proposal", "label": "證據｜提議內容", "type": "textarea", "suggestions": [{"label": "提議內容", "text": "Agent 提議〈做什麼〉，影響〈檔案／模組〉，理由：〈Agent 的說法〉"}]},
{"id": "evidence-rule", "label": "證據｜核准規則、限制與範圍", "type": "textarea", "suggestions": [{"label": "規則與範圍", "text": "〈規則／限制〉（來源：〈Work Order／操作規則／Gate 2 核准範圍〉）"}]},
{"id": "evidence-location", "label": "證據｜證據位置", "type": "text", "suggestions": [{"label": "證據位置", "text": "〈Agent 回覆／檔案／Gate 紀錄〉"}]},
{"id": "risk", "label": "風險｜可能影響與資訊缺口", "type": "textarea", "suggestions": [{"label": "影響與缺口", "text": "可能影響：〈…〉\n資訊缺口：〈…〉"}]},
{"id": "decision", "label": "決策", "type": "select", "options": ["核准（APPROVE）", "附條件核准（APPROVE WITH CONDITIONS）", "拒絕（REJECT）"], "hint": "附條件核准時，相關條件解除後才可續行。"},
{"id": "decision-text", "label": "決策｜理由", "type": "textarea", "suggestions": [{"label": "決策理由", "text": "〈APPROVE／APPROVE WITH CONDITIONS／REJECT〉，理由：〈…〉"}]},
{"id": "decision-conditions", "label": "決策｜條件／修正", "type": "textarea", "suggestions": [{"label": "條件", "text": "條件：〈…〉；解除前不得〈動作〉"}, "無"]},
{"id": "decision-owner-minute", "label": "決策｜決策者與分鐘", "type": "text", "suggestions": [{"label": "決策者與分鐘", "text": "〈姓名〉，第〈分〉分"}]},
{"id": "instruction-next", "label": "給 Agent 的指令｜下一步指令", "type": "textarea", "suggestions": [{"label": "下一步", "text": "請〈停止／修正／依原核准計畫繼續〉〈動作〉，完成後停下回報"}]},
{"id": "instruction-allowed", "label": "給 Agent 的指令｜允許範圍", "type": "textarea", "suggestions": [{"label": "允許範圍", "text": "只可修改〈檔案／範圍〉"}, "維持 Gate 2 核准範圍，不擴大"]},
{"id": "instruction-stop", "label": "給 Agent 的指令｜仍需停止的動作", "type": "textarea", "suggestions": [{"label": "停止動作", "text": "停止〈動作〉，等人員決策"}, "無"]},
{"id": "instruction-gate", "label": "給 Agent 的指令｜須回到的 Gate", "type": "text", "suggestions": ["Gate 1", "Gate 2", "Gate 3", "不需回到 Gate"]}
]}
```

## 填寫：停止與升級處理（Escalation）

一般停止條件使用以下升級短格式；不等同新增第二個主持例外事件。Agent 提出證據，人做決策後才續行。觸發條件見 [Work Order](#b3-work-order) 的 Stop and Escalate Conditions。

```form
{"id": "escalation", "title": "停止與升級處理","fields":[
{"id": "trigger", "label": "觸發原因", "type": "textarea", "suggestions": [{"label": "觸發條件", "text": "觸發 Stop and Escalate Condition：〈條件〉，發生於〈動作／檔案〉"}]},
{"id": "evidence", "label": "證據", "type": "textarea", "suggestions": [{"label": "證據", "text": "〈檔案／測試輸出／規則〉：〈實際看到的內容〉"}]},
{"id": "impact", "label": "影響", "type": "textarea", "suggestions": [{"label": "影響", "text": "影響〈模組／AC／時程〉：〈…〉"}]},
{"id": "options", "label": "可選方案", "type": "textarea", "suggestions": [{"label": "方案 A／B", "text": "A：〈方案〉（風險：〈…〉）\nB：〈方案〉（風險：〈…〉）"}]},
{"id": "recommendation", "label": "建議方案", "type": "textarea", "suggestions": [{"label": "建議", "text": "建議〈A／B〉，理由：〈…〉"}]},
{"id": "decision-needed", "label": "需要人員決定的事項", "type": "textarea", "suggestions": [{"label": "決定事項", "text": "請決定〈問題〉，在決定前 Agent 停止〈動作〉"}]}
]}
```
