---
id: delivery
title: Delivery Summary 與交付
minute: 76-80
group: b3
section: Delivery
---

# 交付：留下可供審查的成果

全場第 76 分鐘停止擴充並列出缺項，第 76–80 分鐘整理交付。交付摘要（Delivery Summary）由主要 Agent 提交、小組審查者核對；Agent 的建議不等於人員決策，人員最後決策由 [Gate 3](#b3-approval-gates) 記錄。

```callout warning
如實交付
- 填實際成果，不預填成功。
- Completion Level 擇一並說明證據，不自動選 Level 3。
- 未驗證不能寫 PASS。
- Gate 核准代表人員接受下一步或目前成果，不能代替驗收或測試 PASS。
- 已完成分析時，可交付 Level 1；無程式修改或未執行測試也可提交活動成果，但須列明原因、未驗證範圍與後續工作。
- 測試通過還須核對需求、範圍、文件及未完成事項。
- 活動成果可接受不等於完整軟體交付。
```

## 交付步驟

- [ ] 76 分鐘到停止擴充並列缺項。
- [ ] Agent 依下方 Delivery Summary 十二欄提交實際成果；無修改、未執行或未驗證的部分寫明原因。
- [ ] 小組審查者核對 Delivery Summary，必要時以 [Review Checklist](#b3-review-checklist) 逐項檢核。
- [ ] 在 [Gate 3 表單](#b3-approval-gates) 記錄人員決策。
- [ ] 匯出本段所有表單（見下方「匯出與交付」）。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/05-delivery-template.md
```

## 填寫：交付摘要（Delivery Summary）

```form
{"id":"delivery-summary","title":"交付摘要（任務 ID：TASK-B3-001）","fields":[
{"id":"mission-result","label":"任務成果｜結果","type":"textarea","hint":"任務 ID：TASK-B3-001。填實際成果，不預填成功。"},
{"id":"mission-basis","label":"任務成果｜依據","type":"textarea"},
{"id":"completion-level","label":"完成程度","type":"select","options":["Level 1: Analysis Complete","Level 2: Core Flow Complete","Level 3: Delivery Complete"],"hint":"Level 1＝分析完成；Level 2＝核心流程完成；Level 3＝完整交付。依實際證據擇一，不自動選 Level 3。"},
{"id":"completion-reason","label":"完成程度｜實際等級與原因","type":"textarea"},
{"id":"implemented-scope","label":"已完成範圍｜已完成","type":"textarea"},
{"id":"not-implemented","label":"未完成事項｜未完成／未驗證","type":"textarea"},
{"id":"not-implemented-impact","label":"未完成事項｜影響","type":"textarea"},
{"id":"not-implemented-next","label":"未完成事項｜下一步","type":"textarea"},
{"id":"files-changed","label":"修改檔案｜實際檔案與主要變更","type":"textarea","hint":"無修改時寫「無修改」及原因，不虛構 Diff。"},
{"id":"rules-covered","label":"涵蓋的商業規則｜Rule ID 與實作、測試、文件證據","type":"textarea"},
{"id":"ac-results","label":"驗收結果｜各項驗收條件的狀態與實際證據","type":"textarea","hint":"驗收條件編號（AC ID）見 B3 任務卡。PASS＝通過；FAIL＝失敗；NOT VERIFIED＝未驗證。未驗證不能寫 PASS，人員核准關卡（Gate）核准也不等於 PASS。"},
{"id":"test-workdir","label":"實際測試｜工作目錄／版本","type":"text"},
{"id":"test-command","label":"實際測試｜實際命令","type":"textarea"},
{"id":"test-result","label":"實際測試｜結果／exit code","type":"textarea"},
{"id":"test-issues","label":"實際測試｜Fail／Skip／XFail／Warning","type":"textarea"},
{"id":"test-not-run","label":"實際測試｜未執行及原因","type":"textarea"},
{"id":"docs-updated","label":"文件更新｜文件與內容","type":"textarea"},
{"id":"docs-not-synced","label":"文件更新｜仍未同步","type":"textarea"},
{"id":"risks","label":"風險與限制｜已知風險、限制與責任影響","type":"textarea"},
{"id":"deviations","label":"核准計畫的偏差｜Gate 2 計畫與實際差異","type":"textarea","hint":"沒有偏差也須明寫。"},
{"id":"deviations-escalation","label":"核准計畫的偏差｜升級與人員決策","type":"textarea"},
{"id":"recommended-decision","label":"建議決策","type":"select","options":["APPROVE","CONDITIONAL APPROVAL","REJECT"],"hint":"APPROVE＝核准；CONDITIONAL APPROVAL＝附條件核准；REJECT＝拒絕。這是 Agent 的建議；人員最後決策由 Gate 3 記錄。"},
{"id":"recommended-reason","label":"建議決策｜Agent 建議與理由","type":"textarea","hint":"測試通過還須核對需求、範圍、文件及未完成事項。"}
]}
```

## 匯出與交付

每份表單都會自動暫存在瀏覽器中。請在本段（第 76–80 分鐘）逐一匯出 B3 的表單：

1. 在每份表單按「匯出 Markdown」下載 `.md` 檔，或按「複製 Markdown」。
2. 依主持人指定方式交付；交付內容為 Gate 紀錄、Impact／方案、Diff、實際測試、文件及摘要。
3. 本段需要匯出的表單：

- [ ] [Work Order](#b3-work-order)：Approved Context 與 Gate 2 核准範圍
- [ ] [Gate 1、Gate 2、Gate 3 決策紀錄](#b3-approval-gates)
- [ ] [Review Checklist](#b3-review-checklist)（有使用時）
- [ ] [Exception Response 與 Escalation](#b3-exception-card)（有使用時）
- [ ] 本頁的 Delivery Summary

```callout tip
功能 Level 與治理證據分開
Level 1／2 可如實作為活動成果，但不得冒稱完整程式交付。Gate 紀錄、條件與未完成事項本身就是交付的一部分，請一併保留。
```
