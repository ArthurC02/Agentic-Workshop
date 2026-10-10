---
id: gf-submission
title: 提交清單與交付摘要
minute: 27-29
group: greenfield
section: Greenfield｜Tool
---

> 本頁上半部取自 G0 參與者文件 `05-submission-checklist.md`。交付摘要由 Agent 寫進 `notes/greenfield.md`，你不用逐項勾。有時間的話，貼下方提示詞請 Agent 依清單自我檢查，你只核對它的回報（固定欄位的表格，技巧：結構化輸出，缺項一眼就看得到）；第 29 分鐘快到時，跳過這步，直接在表單選交付決定。

```text
請讀上一層資料夾（或 docs\ 副本）的 05-submission-checklist.md（提交清單），依清單逐項檢查 notes/greenfield.md、README 與 docs/，用固定三欄的表格回報：清單編號、結果（有證據／缺）、證據在哪一段或缺什麼。缺的項目先不要補，列給我看，等我決定。不要修改程式。
```

```include
zip=participant-07-g0.zip path=agentic-workshop/01-greenfield/participant/05-submission-checklist.md
```

## Greenfield 交付決定

```form
{"id": "greenfield-delivery", "title": "Greenfield 交付決定","fields":[
{"id": "accept", "label": "我接受這份交付嗎？", "type": "select", "options": ["接受：完整 MVP", "接受：部分完成，未完成已寫進 notes", "不接受，已請 Agent 修正"]},
{"id": "docs-flow", "label": "我在 /docs 親自走過完整流程，結果符合需求嗎？", "type": "select", "options": ["是", "部分符合", "否／沒走到"]},
{"id": "unsure", "label": "還有什麼不確定、要再問 Agent 的？（選填）", "type": "text", "suggestions": ["沒有"]}
]}
```

判斷依據（驗收對照表、/docs 試用結果）已由 Agent 寫進 `notes/greenfield.md` 的「交付摘要」，表單不用再寫理由。
