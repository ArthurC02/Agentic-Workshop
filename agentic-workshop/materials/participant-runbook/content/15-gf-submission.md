---
id: gf-submission
title: 提交清單與交付摘要
minute: 27-29
group: greenfield
section: Greenfield｜Tool
---

> 本頁上半部取自 G0 參與者文件 `05-submission-checklist.md`，在最後 2 分鐘及提交之前使用。下方表單用來整理交付摘要，會自動暫存，可匯出或複製 Markdown 後依主持人指定方式交付。

原文中的 AC（Acceptance Criteria）是驗收條件，Rule ID 是商業規則編號，變更內容（Diff）是 Agent 實際修改的內容。你不需要讀程式：請依驗收對照表、變更審查答案與你在 /docs 的實際操作核對，再勾選完成。

```include
zip=participant-07-g0.zip path=agentic-workshop/01-greenfield/participant/05-submission-checklist.md
```

## Greenfield 交付摘要

```form
{"id": "greenfield-delivery", "title": "Greenfield 交付摘要","fields":[
{"id": "done", "label": "完成的功能／商業規則／驗收條件", "type": "textarea", "hint": "只列已實際驗證的項目，並標出對應的商業規則編號（Rule ID）與驗收條件編號（AC ID）。", "suggestions": [{"label": "功能與對應", "text": "〈功能〉：Rule 〈Rule ID〉、AC 〈AC ID〉（驗證方式：〈測試／手動流程〉）"}]},
{"id": "files", "label": "修改檔案", "type": "textarea", "hint": "列出主要修改的檔案。", "suggestions": [{"label": "檔案與用途", "text": "〈檔案路徑〉：〈改了什麼〉"}]},
{"id": "tests", "label": "測試指令與結果", "type": "textarea", "hint": "依 Agent 的驗收對照表填寫：實際執行的指令，以及通過／失敗／Skip 數；未執行的請寫「未驗證」。", "suggestions": [{"label": "指令與結果", "text": "指令：〈pytest 指令〉\n結果：〈數字〉 passed、〈數字〉 failed、〈數字〉 skipped"}, {"label": "未驗證", "text": "未驗證：〈項目〉（原因：〈…〉）"}]},
{"id": "docs", "label": "文件更新", "type": "textarea", "hint": "例如 README、docs/business-rules.md、docs/api-examples.md。", "suggestions": [{"label": "文件更新", "text": "〈文件路徑〉：〈更新內容〉"}, "沒有更新文件"]},
{"id": "todo", "label": "尚未完成事項", "type": "textarea", "hint": "包括核心未完成項目與仍被 Skip 的測試。", "suggestions": ["沒有", {"label": "未完成項目", "text": "〈項目〉：〈完成到哪裡〉"}, {"label": "Skip 測試", "text": "〈測試名稱〉仍被 Skip"}]},
{"id": "risks", "label": "風險與限制", "type": "textarea", "suggestions": [{"label": "風險範本", "text": "〈風險〉：〈可能影響〉"}, {"label": "測試缺口", "text": "〈情境〉沒有測試涵蓋"}, "無已知風險"]},
{"id": "roles", "label": "人和 Agent 各做什麼", "type": "textarea", "hint": "例如：誰拆解工作、誰核准計畫、誰做變更審查、誰執行測試與指令。", "suggestions": [{"label": "分工範本", "text": "我：拆解工作、核准計畫、做變更審查、手算 1225、在 /docs 走完整流程\nAgent：〈產生程式／測試／文件、執行指令〉\n測試由〈誰〉實際執行"}]},
{"id": "diff-reviewed", "label": "我已完成變更審查（Agent 回答審查問題、我填審查卡），確認符合核准計畫，未擴大範圍或修改商業規則", "type": "checkbox"}
]}
```
