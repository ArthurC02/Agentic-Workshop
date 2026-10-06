---
id: b3-review-checklist
title: B3 交付審查檢核表
minute: 75-80
group: b3
section: B3｜Digital Worker
---

> 本頁上半部取自 B3 參與者文件 `04-review-checklist.md`，於 Gate 3 按需使用。下方表單會自動暫存，可匯出或複製 Markdown；Gate 3 決策請記在 [Gate 3 表單](#b3-approval-gates)。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/04-review-checklist.md
```

## 填寫：交付審查檢核

```form
{"id":"review-checklist","title":"B3 交付審查檢核表","fields":[
{"id":"requirement","label":"需求","type":"checklist","items":["5–20 人邊界。","不允許部分成功。","同車廂連續座位。","付款失敗整筆取消。","每人 B2 最有利單一優惠仍適用。"],"hint":"逐項依證據勾選；未完成或未驗證保持未勾並說明，不由 Agent 自動全勾。"},
{"id":"scope","label":"範圍","type":"checklist","items":["未新增外部資料庫或服務。","未全面重寫一般 Booking。","未修改不相關 API。","修改檔案與 Gate 2 核准計畫一致，偏差已回報。"]},
{"id":"quality","label":"品質","type":"checklist","items":["建立失敗不保留座位。","付款失敗釋放全部座位。","付款失敗不建立 Order。","成功僅一筆 Order。","Audit 與 Notification 依規則留下紀錄。"]},
{"id":"evidence","label":"證據","type":"checklist","items":["實際命令與結果可追查。","無 Skip／XFail／未知失敗，未執行部分已揭露。","Acceptance Criteria 可追溯 Test。","文件與實作同步。","未完成事項及已知風險已揭露。"]},
{"id":"completion","label":"完成度","type":"text"},
{"id":"evidence-location","label":"證據位置","type":"textarea"},
{"id":"not-met","label":"不符合／未驗證","type":"textarea"},
{"id":"corrections","label":"要求 Agent 修正","type":"textarea"},
{"id":"reviewer","label":"審查者","type":"text"}
]}
```
