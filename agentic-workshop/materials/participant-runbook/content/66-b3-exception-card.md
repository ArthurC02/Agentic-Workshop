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

主持人宣布例外事件後，貼下方提示詞：Agent 先停下、把提議與證據整理好再問你，你在 60 秒內回一句決定。時間緊可用 30 秒口頭判斷，再請 Agent 補一行紀錄；不預填答案。

```text
先停止所有修改。主持人剛宣布了一個例外事件；如果這個提議不是你自己提出的，先問我事件卡上的內容。請用白話說明這個提議：要做什麼、會影響哪些檔案或功能、為什麼，並對照工作單（Work Order）與 Gate 2 核准範圍，指出相關的那一句原文。把以上內容寫進 notes/b3.md 的「例外事件」段落。
然後問我：這個提議在核准範圍內嗎（是／否／不確定）？我的決定是核准、附條件核准還是拒絕？條件、決策者與現在第幾分鐘？
我回答後，照原文記進同一段落，並依我的決定告訴我下一步：要停止什麼、允許做什麼、需要回到哪個 Gate。附條件核准時，條件解除前不要續行。
```

**看到什麼算過關**：`notes/b3.md` 的「例外事件」段落有提議、對照的原文、你的決定與條件；Agent 在你決定前沒有繼續修改。

```form
{"id": "exception-response", "title": "例外回應（例外 ID：EXCEPTION-DW-001）","fields":[
{"id": "within-scope", "label": "這項提議在核准範圍內嗎？", "type": "select", "options": ["是（YES）", "否（NO）", "不確定（UNCLEAR）"]},
{"id": "decision", "label": "你的決定", "type": "select", "options": ["核准（APPROVE）", "附條件核准（APPROVE WITH CONDITIONS）", "拒絕（REJECT）"], "hint": "附條件核准時，條件解除後才可續行。"}
]}
```

## Agent 自己停下來時（Escalation）

Agent 遇到 [Work Order](#b3-work-order) 的停止條件時會自己停下，這不是主持人宣布的例外事件。它會依上方 Escalation 範本把觸發原因、證據、影響、可選方案、建議與需要你決定的事寫進 `notes/b3.md`；你讀完回一句決定（例如「照建議做」），不需要另外填表。

> 這段學到的技巧：例外時先叫 Agent 停下、把證據寫下來，人只做「在不在範圍內、要不要放行」的決定。
