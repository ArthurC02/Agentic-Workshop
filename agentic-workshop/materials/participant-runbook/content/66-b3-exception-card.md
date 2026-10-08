---
id: b3-exception-card
title: Exception Response 與 Escalation
minute: 63-76
group: b3
section: B3｜Digital Worker
---

> 本頁上半部取自 B3 參與者文件 `06-exception-response-card.md`，是空白範本，按需使用。例外發生時，人只做決定；提議內容、證據與風險由 Agent 寫進 `notes/b3.md`。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/06-exception-response-card.md
```

## 例外事件：60 秒內做決定

主持人宣布例外事件後，先請 Agent 停下並整理證據，你在 60 秒內決定。時間緊可用 30 秒口頭判斷，事後補一行紀錄；不預填答案。

```text
先停止所有修改。請用白話說明你的提議：要做什麼、會影響哪些檔案或功能、為什麼，並對照 Work Order 與 Gate 2 核准範圍說明它是否在範圍內。把以上內容寫進 notes/b3.md 的「例外事件」段落，然後等我決定。
```

```form
{"id": "exception-response", "title": "例外回應（例外 ID：EXCEPTION-DW-001）","fields":[
{"id": "within-scope", "label": "這項提議在核准範圍內嗎？", "type": "select", "options": ["是（YES）", "否（NO）", "不確定（UNCLEAR）"]},
{"id": "decision", "label": "你的決定", "type": "select", "options": ["核准（APPROVE）", "附條件核准（APPROVE WITH CONDITIONS）", "拒絕（REJECT）"], "hint": "附條件核准時，條件解除後才可續行。"},
{"id": "decision-owner-minute", "label": "決策者與分鐘", "type": "text", "suggestions": [{"label": "決策者與分鐘", "text": "〈姓名〉，第〈分〉分"}]},
{"id": "instruction-next", "label": "給 Agent 的一句指令", "type": "text", "suggestions": [{"label": "下一步", "text": "請〈停止／修正／依原核准計畫繼續〉〈動作〉，把決定記進 notes/b3.md，完成後停下回報"}]}
]}
```

## Agent 自己停下來時（Escalation）

Agent 遇到 [Work Order](#b3-work-order) 的停止條件時會自己停下，這不是主持人宣布的例外事件。請它依範本格式把觸發原因、證據、影響、可選方案、建議與需要你決定的事寫進 `notes/b3.md`，你讀完再決定是否續行，不需要另外填表。

> 這段學到的技巧：例外時先叫 Agent 停下、把證據寫下來，人只做「在不在範圍內、要不要放行」的決定。
