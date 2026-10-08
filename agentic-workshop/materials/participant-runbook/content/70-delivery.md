---
id: delivery
title: Delivery Summary 與交付
minute: 76-80
group: b3
section: Delivery
---

# 交付：留下可供審查的成果

全場第 76 分鐘停止擴充，接下來 **3 分鐘**定稿交付摘要（Delivery Summary）、匯出並交件。交付摘要由主要 Agent 提交、小組審查者核對；Agent 的建議不等於人員決策，人員最後決策由 [Gate 3](#b3-approval-gates) 記錄。

```callout warning
如實交付，交件後不再修改
- 填實際成果，不預填成功。
- 完成等級（Completion Level：Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付）擇一並說明證據，不自動選 Level 3。
- 未驗證不能寫 PASS（通過）。
- Gate 核准代表人員接受下一步或目前成果，不能代替驗收或測試 PASS。
- 已完成分析時，可交付 Level 1；無程式修改或未執行測試也可提交活動成果，但須列明原因、未驗證範圍與後續工作。
- 測試通過還須核對需求、範圍、文件及未完成事項。
- 活動成果可接受不等於完整軟體交付。
- 交件後，交付摘要與 Level 保持交件時的樣子；人不補寫程式或測試。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**；要做什麼、要貼給 Agent 的提示詞、要填的表單，全部在本頁。全員交件後，主持人會在投影上說明 B3 的對照重點，這時請看投影。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 定稿交付摘要 | 76–78 | 00–02 | 停止擴充；Agent 交出交付摘要後停下；你核對並填表 |
| 2 · 匯出與交件 | 78–79 | 02–03 | 匯出 B3 所有表單與交付摘要，依主持人指定方式交件 |
| 看投影 | 79–80 | 03–04 | 交件後不再修改；第 80 分鐘進入回顧 |

## 檢查點 1 · 定稿交付摘要（第 76–78 分鐘）

- [ ] 76 分鐘到，停止擴充並列出缺項。
- [ ] 已在 [B3 檢查點 6](#b3) 請 Agent 交出交付摘要的，直接進入下一項核對；還沒交出的，把下方提示詞貼給主要 Agent，並附上本頁下方的 Delivery Summary 範本全文。

```text
停止新增功能與測試，不要再修改任何檔案。請依附上的 Delivery Summary 範本十二欄，用實際證據整理交付摘要：
- Completion Level 擇一並說明證據，不自動選 Level 3。
- 測試只寫實際執行過的命令與完整結果；沒執行的寫「未執行」及原因，未驗證不能寫 PASS。
- 沒有修改時寫「無修改」及原因，不虛構 Diff。
- 寫出與 Gate 2 核准計畫的偏差；沒有偏差也要明寫。
整理完就停下，等我們核對。不要自行修正或補做任何項目。
```

- [ ] 小組審查者核對 Agent 的摘要：Level 是否有證據、測試是否為實際輸出、未完成與偏差是否寫出。必要時以 [Review Checklist](#b3-review-checklist)（交付審查檢核表）逐項檢核。與你們的實際紀錄不一致時，以人員確認為準。
- [ ] 把核對後的內容填入下方「交付摘要」表單。
- [ ] [Gate 3 表單](#b3-approval-gates) 還沒記錄人員決策的，現在補記。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/05-delivery-template.md
```

### 填寫：交付摘要（Delivery Summary）

```form
{"id": "delivery-summary", "title": "交付摘要（任務 ID：TASK-B3-001）","fields":[
{"id": "mission-result", "label": "任務成果｜結果", "type": "textarea", "hint": "任務 ID：TASK-B3-001。填實際成果，不預填成功。", "suggestions": [{"label": "結果範本", "text": "實際成果：〈完成了什麼〉；尚未完成：〈缺項〉"}, {"label": "僅完成分析", "text": "僅完成分析：〈分析結論〉；未修改程式，原因：〈原因〉"}]},
{"id": "mission-basis", "label": "任務成果｜依據", "type": "textarea", "suggestions": [{"label": "依據來源", "text": "依據：〈Gate 紀錄／測試輸出／Diff／文件〉（〈檔案或紀錄位置〉）"}]},
{"id": "completion-level", "label": "完成程度", "type": "select", "options": ["Level 1：分析完成（Analysis Complete）", "Level 2：核心流程完成（Core Flow Complete）", "Level 3：交付完成（Delivery Complete）"], "hint": "Level 1＝分析完成；Level 2＝核心流程完成；Level 3＝完整交付。依實際證據擇一，不自動選 Level 3。"},
{"id": "completion-reason", "label": "完成程度｜實際等級與原因", "type": "textarea", "suggestions": [{"label": "等級與證據", "text": "實際等級：Level 〈1／2／3〉；證據：〈測試輸出／Diff／文件〉；未達下一級的原因：〈原因〉"}]},
{"id": "implemented-scope", "label": "已完成範圍｜已完成", "type": "textarea", "suggestions": [{"label": "已完成項", "text": "〈完成項目〉（證據：〈檔案／測試／紀錄〉）"}, "無"]},
{"id": "not-implemented", "label": "未完成事項｜未完成／未驗證", "type": "textarea", "suggestions": [{"label": "未完成項", "text": "未完成：〈項目〉"}, {"label": "未驗證項", "text": "未驗證：〈項目〉，原因：〈原因〉"}, "無"]},
{"id": "not-implemented-impact", "label": "未完成事項｜影響", "type": "textarea", "suggestions": [{"label": "影響範本", "text": "〈未完成項目〉：影響〈功能／使用者／規則〉"}, "無"]},
{"id": "not-implemented-next", "label": "未完成事項｜下一步", "type": "textarea", "suggestions": [{"label": "下一步", "text": "〈項目〉：由〈誰〉〈做什麼〉，以〈測試／審查〉確認"}, "無"]},
{"id": "files-changed", "label": "修改檔案｜實際檔案與主要變更", "type": "textarea", "hint": "無修改時寫「無修改」及原因，不虛構 Diff。", "suggestions": [{"label": "檔案與變更", "text": "〈檔案路徑〉：〈主要變更〉"}, {"label": "無修改", "text": "無修改，原因：〈原因〉"}]},
{"id": "rules-covered", "label": "涵蓋的商業規則｜Rule ID 與實作、測試、文件證據", "type": "textarea", "suggestions": [{"label": "Rule 證據", "text": "Rule 〈Rule ID〉：實作〈檔案〉、測試〈測試名稱〉、文件〈路徑〉"}, {"label": "部分涵蓋", "text": "Rule 〈Rule ID〉：僅〈實作／測試／文件〉，缺〈…〉"}]},
{"id": "ac-results", "label": "驗收結果｜各項驗收條件的狀態與實際證據", "type": "textarea", "hint": "驗收條件編號（AC ID）見 B3 任務卡。PASS＝通過；FAIL＝失敗；NOT VERIFIED＝未驗證。未驗證不能寫 PASS，人員核准關卡（Gate）核准也不等於 PASS。", "suggestions": [{"label": "AC 狀態", "text": "〈AC ID〉：〈PASS／FAIL／NOT VERIFIED〉（證據：〈測試輸出／檔案〉）"}, {"label": "未驗證 AC", "text": "〈AC ID〉：NOT VERIFIED，原因：〈原因〉"}]},
{"id": "test-workdir", "label": "實際測試｜工作目錄／版本", "type": "text", "suggestions": [{"label": "目錄與版本", "text": "〈工作目錄〉／〈版本或 commit〉"}]},
{"id": "test-command", "label": "實際測試｜實際命令", "type": "textarea", "suggestions": [{"label": "實際命令", "text": "〈實際執行的命令〉"}, "未執行"]},
{"id": "test-result", "label": "實際測試｜結果／exit code", "type": "textarea", "suggestions": [{"label": "結果範本", "text": "〈數字〉 passed、〈數字〉 failed；exit code 〈數字〉"}, "未執行"]},
{"id": "test-issues", "label": "實際測試｜Fail／Skip／XFail／Warning", "type": "textarea", "suggestions": [{"label": "問題項目", "text": "〈Fail／Skip／XFail／Warning〉：〈測試名稱〉，〈訊息摘要〉"}, "無"]},
{"id": "test-not-run", "label": "實際測試｜未執行及原因", "type": "textarea", "suggestions": [{"label": "未執行原因", "text": "〈測試範圍〉未執行，原因：〈原因〉"}, "無"]},
{"id": "docs-updated", "label": "文件更新｜文件與內容", "type": "textarea", "suggestions": [{"label": "文件更新", "text": "〈文件路徑〉：〈更新內容〉"}, {"label": "未更新", "text": "未更新文件，原因：〈原因〉"}]},
{"id": "docs-not-synced", "label": "文件更新｜仍未同步", "type": "textarea", "suggestions": [{"label": "未同步項", "text": "〈文件路徑〉：〈尚未同步的內容〉"}, "無"]},
{"id": "risks", "label": "風險與限制｜已知風險、限制與責任影響", "type": "textarea", "suggestions": [{"label": "風險範本", "text": "風險：〈…〉；限制：〈…〉；責任影響：〈由誰承擔／確認〉"}, "未發現已知風險（依據：〈…〉）"]},
{"id": "deviations", "label": "核准計畫的偏差｜Gate 2 計畫與實際差異", "type": "textarea", "hint": "沒有偏差也須明寫。", "suggestions": [{"label": "偏差範本", "text": "Gate 2 計畫：〈…〉；實際：〈…〉；原因：〈…〉"}, "無偏差，實際執行與 Gate 2 核准計畫一致"]},
{"id": "deviations-escalation", "label": "核准計畫的偏差｜升級與人員決策", "type": "textarea", "suggestions": [{"label": "已升級", "text": "已升級給〈誰〉；人員決策：〈決策〉（第〈分〉分）"}, "無需升級（無偏差）"]},
{"id": "recommended-decision", "label": "建議決策", "type": "select", "options": ["核准（APPROVE）", "附條件核准（CONDITIONAL APPROVAL）", "拒絕（REJECT）"], "hint": "這是 Agent 的建議；人員最後決策由 Gate 3 記錄。"},
{"id": "recommended-reason", "label": "建議決策｜Agent 建議與理由", "type": "textarea", "hint": "測試通過還須核對需求、範圍、文件及未完成事項。", "suggestions": [{"label": "建議與理由", "text": "建議：〈APPROVE／CONDITIONAL APPROVAL／REJECT〉；理由：〈證據〉；條件／未完成：〈…〉"}]}
]}
```

## 檢查點 2 · 匯出與交件（第 78–79 分鐘）

每份表單都會自動暫存在瀏覽器中，但要匯出才算交件。按下方按鈕（或右上角下載圖示）一次下載所有已填寫的表單；也可以在個別表單按「匯出 Markdown」。

```exportall
```

- [ ] 確認 ZIP 內有下列 B3 表單（或已逐一匯出）：
  - [Work Order](#b3-work-order)：Approved Context 與 Gate 2 核准範圍
  - [B3 檢查點 4、5 確認](#b3)
  - [Gate 1、Gate 2、Gate 3 決策紀錄](#b3-approval-gates)
  - [Review Checklist](#b3-review-checklist)（有使用時）
  - [Exception Response 與 Escalation](#b3-exception-card)（有使用時）
  - 本頁的 Delivery Summary
- [ ] 依主持人指定方式交件；交付內容為 Gate 紀錄、影響分析（Impact）／方案、Diff（程式修改內容）、實際測試、文件及摘要。

```callout tip
功能 Level 與治理證據分開
Level 1／2 可如實作為活動成果，但不得冒稱完整程式交付。Gate 紀錄、條件與未完成事項本身就是交付的一部分，請一併保留。
```

```form
{"id":"delivery-cp2","title":"檢查點 2 確認","fields":[
{"id":"exported","label":"已匯出的表單","type":"checklist","items":["Work Order（工作指令單）","B3 檢查點 4、5 確認","Gate 1／2／3 決策紀錄","Review Checklist（有使用時）","Exception Response 與 Escalation（有使用時）","Delivery Summary（交付摘要）"],"hint":"只勾實際已匯出的項目；沒有使用的表單不用勾。"},
{"id":"handed-in","label":"已依主持人指定方式交件","type":"checkbox"}
]}
```

```callout warning
交件後停止修改
交件後不再修改交付摘要、Level 或任何表單，接下來看投影。未完成如實列為缺項，不把部分完成描述為完整交付。第 80 分鐘進入回顧。
```
