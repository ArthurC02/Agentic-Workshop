---
id: gf-submission
title: 提交清單與交付摘要
minute: 27-29
group: greenfield
section: Greenfield｜Tool
---

> 本頁上半部取自 G0 參與者文件 `05-submission-checklist.md`，在最後 2 分鐘及提交之前使用。下方表單用來整理交付摘要，會自動暫存，可匯出或複製 Markdown 後依主持人指定方式交付。

原文中的 AC 是驗收條件，Rule ID 是商業規則編號，Diff 是程式修改差異。請核對實際修改與測試證據，再勾選完成。

```include
zip=participant-07-g0.zip path=agentic-workshop/01-greenfield/participant/05-submission-checklist.md
```

## Greenfield 交付摘要

```form
{"id":"greenfield-delivery","title":"Greenfield 交付摘要","fields":[
{"id":"done","label":"完成的功能／商業規則／驗收條件","type":"textarea","hint":"只列已實際驗證的項目，並標出對應的商業規則編號（Rule ID）與驗收條件編號（AC ID）。"},
{"id":"files","label":"修改檔案","type":"textarea","hint":"列出主要修改的檔案。"},
{"id":"tests","label":"測試指令與結果","type":"textarea","hint":"貼上實際執行的指令，以及通過／失敗／Skip 數與輸出摘要；未執行的請寫「未驗證」。"},
{"id":"docs","label":"文件更新","type":"textarea","hint":"例如 README、docs/business-rules.md、docs/api-examples.md。"},
{"id":"todo","label":"尚未完成事項","type":"textarea","hint":"包括核心未完成項目與仍被 Skip 的測試。"},
{"id":"risks","label":"風險與限制","type":"textarea"},
{"id":"roles","label":"人和 Agent 各做什麼","type":"textarea","hint":"例如：誰拆解工作、誰核准計畫、誰審查 Diff、誰執行測試。"},
{"id":"diff-reviewed","label":"我已審查主要 Diff，確認符合核准計畫，未擴大範圍或修改商業規則","type":"checkbox"}
]}
```
