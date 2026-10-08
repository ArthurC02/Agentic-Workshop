---
id: b3-work-order
title: Digital Worker Work Order
minute: 63-76
group: b3
section: B3｜Digital Worker
---

> 本頁上半部取自 B3 參與者文件 `02-agent-work-order.md`，B3 發放後交給 Agent。先填小組與 Context（[B3 流程](#b3)檢查點 1）；Gate 2 範圍待設計核准時填寫（檢查點 3）。下方表單會自動暫存，可用「複製 Markdown」連同本頁全文交給主要 Agent。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/02-agent-work-order.md
```

## 填寫：已核准的背景資料與允許修改範圍

原文中的 Approved Context 指已核准的背景資料；Allowed Change Scope 指允許修改的範圍。Gate 2 若附帶條件，相關條件解除後才可修改程式。

```form
{"id": "work-order", "title": "工作命令：已核准的背景資料與允許修改範圍","fields":[
{"id": "team", "label": "小組", "type": "text"},
{"id": "agent-session", "label": "主要 Agent／對話工作階段", "type": "text", "suggestions": [{"label": "Agent 與電腦", "text": "〈誰〉的 Agent，在〈誰〉的電腦執行（工作階段：〈名稱〉）"}]},
{"id": "context-version", "label": "背景資料版本", "type": "text", "suggestions": [{"label": "Shared Context", "text": "Shared Context（第〈分〉分核准版本）"}]},
{"id": "repository-version", "label": "接手的程式庫版本", "type": "text", "suggestions": [{"label": "B2 接手", "text": "B2 接手版本（〈commit／資料夾〉）"}, {"label": "B2 Recovery", "text": "B2 Recovery 版本（〈來源〉）"}]},
{"id": "confirmed-assumptions", "label": "已確認假設／限制", "type": "textarea", "suggestions": [{"label": "假設與來源", "text": "〈假設〉：已確認（來源：〈任務卡／Rule ID／小組確認〉）"}, {"label": "限制", "text": "限制：〈不得做的事〉（來源：〈操作規則／任務卡〉）"}, "不新增未核准的外部套件、服務或資料庫"]},
{"id": "pending-decisions", "label": "尚待決定事項", "type": "textarea", "hint": "未填資料由小組確認，不由 Agent 猜測。", "suggestions": [{"label": "待決事項", "text": "〈問題〉：待〈誰〉於〈Gate 1／Gate 2〉決定"}, "無"]},
{"id": "gate2-scope", "label": "Gate 2 核准範圍", "type": "textarea", "hint": "Gate 2 範圍待設計核准時填寫。允許為團體流程所需的 API、Domain（業務模型）、Application（應用服務層）、座位配置、付款補償、測試與文件修改；每個預計檔案均須先提出影響理由。", "suggestions": [{"label": "核准檔案", "text": "〈檔案〉：允許修改，理由：〈影響理由〉"}, {"label": "不得修改", "text": "不得修改：〈檔案／模組〉"}, {"label": "附帶條件", "text": "條件：〈條件〉；解除前不得修改〈範圍〉"}]}
]}
```
