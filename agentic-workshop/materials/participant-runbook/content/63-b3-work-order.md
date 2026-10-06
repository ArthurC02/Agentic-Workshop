---
id: b3-work-order
title: Digital Worker Work Order
minute: 63-76
group: b3
section: B3｜Digital Worker
---

> 本頁上半部取自 B3 參與者文件 `02-agent-work-order.md`，B3 發放後交給 Agent。先填小組與 Context；Gate 2 範圍待設計核准時填寫。下方表單會自動暫存，可用「複製 Markdown」連同本頁全文交給主要 Agent。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/02-agent-work-order.md
```

## 填寫：已核准的背景資料與允許修改範圍

原文中的 Approved Context 指已核准的背景資料；Allowed Change Scope 指允許修改的範圍。Gate 2 若附帶條件，相關條件解除後才可修改程式。

```form
{"id":"work-order","title":"工作命令：已核准的背景資料與允許修改範圍","fields":[
{"id":"team","label":"小組","type":"text"},
{"id":"agent-session","label":"主要 Agent／對話工作階段","type":"text"},
{"id":"context-version","label":"背景資料版本","type":"text"},
{"id":"repository-version","label":"接手的程式庫版本","type":"text"},
{"id":"confirmed-assumptions","label":"已確認假設／限制","type":"textarea"},
{"id":"pending-decisions","label":"尚待決定事項","type":"textarea","hint":"未填資料由小組確認，不由 Agent 猜測。"},
{"id":"gate2-scope","label":"Gate 2 核准範圍","type":"textarea","hint":"Gate 2 範圍待設計核准時填寫。允許為團體流程所需的 API、Domain、Application、座位配置、付款補償、測試與文件修改；每個預計檔案均須先提出影響理由。"}
]}
```
