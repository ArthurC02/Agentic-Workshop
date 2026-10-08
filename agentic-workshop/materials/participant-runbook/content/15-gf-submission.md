---
id: gf-submission
title: 提交清單與交付摘要
minute: 27-29
group: greenfield
section: Greenfield｜Tool
---

> 本頁上半部取自 G0 參與者文件 `05-submission-checklist.md`，在提交之前使用。交付摘要由 Agent 寫進 `notes/greenfield.md`；你只填下方 4 欄的交付表單，記下你的決定。表單會自動暫存，可匯出或複製 Markdown 後依主持人指定方式交付。

原文中的 AC（Acceptance Criteria）是驗收條件，Rule ID 是商業規則編號。你不需要讀程式：請依 `notes/greenfield.md` 裡的驗收對照表、變更審查答案與你在 /docs 的實際操作核對，再勾選完成。

```include
zip=participant-07-g0.zip path=agentic-workshop/01-greenfield/participant/05-submission-checklist.md
```

## Greenfield 交付決定

```form
{"id": "greenfield-delivery", "title": "Greenfield 交付決定","fields":[
{"id": "accept", "label": "我接受這份交付嗎？", "type": "select", "options": ["接受：完整 MVP", "接受：部分完成，未完成已寫進 notes", "不接受，已請 Agent 修正"]},
{"id": "docs-flow", "label": "我在 /docs 親自走過完整流程，結果符合需求嗎？", "type": "select", "options": ["是", "部分符合", "否／沒走到"]},
{"id": "reason", "label": "一句理由（我是依什麼證據決定的）", "type": "text", "suggestions": [{"label": "理由範本", "text": "驗收對照表〈數字〉項通過、我在 /docs 看到〈結果〉"}]},
{"id": "unsure", "label": "還有什麼不確定、要再問 Agent 的？", "type": "text", "suggestions": ["沒有"]}
]}
```
