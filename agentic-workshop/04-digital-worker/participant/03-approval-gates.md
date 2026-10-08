# B3 人員核准 Gate

> 讀者：小組審查者與主要 Coding Agent。
> 使用時機：需求、設計與交付三個決策點。
> 前置條件：已有 [Work Order](02-agent-work-order.md)；人員仍承擔責任。

每 Gate 使用 1–3 分鐘與下方短格式，記錄真實審查證據。三 Gate 是執行中的人員核准，不取代程式驗收。

## Gate 1：Requirement Understanding

Agent Input：需求摘要、規則清單、關鍵假設、資訊缺口、Out of Scope、需要人決定的問題。

Human Review：5–20 邊界、同 Trip／同車廂連續、無部分成功、失敗整筆取消及全釋放、B2 個別旅客優惠是否理解一致。

Decision：核准需求才進入設計；拒絕時要求修正。條件核准需說明哪些活動已允許及仍被阻擋。

Evidence：需求摘要版本、所審規則與假設、未解問題與實際人員決策。

## Gate 2：Impact and Design

Agent Input：受影響／不受影響模組、API Contract、Domain 變更、Seat Assignment 方案、Atomicity／Compensation 方案、測試策略、文件清單、主要風險與預計修改檔案。

Human Review：範圍是否合理、避免全面重寫、建立與付款失敗均處理、座位釋放、既有功能沒被改壞（既有測試保留）與未核准外部依賴；不以方案看似合理取代授權檢查。

Decision：此 Gate 核准後才可改程式。條件未滿足的範圍先停止；偏差需補證或重新核准。

Evidence：核准方案、修改範圍、風險／測試對應、條件及回覆；例外時使用 [Response Card](06-exception-response-card.md)。

## Gate 3：Delivery Review

Agent Input：當前成果摘要、Acceptance Criteria 對照、Rule Traceability、未完成事項、已知風險及交付建議；有修改時附實際檔案，有測試時附命令與真實結果。Level 1 附需求／設計與完整測試策略，無修改或未執行明記，不預填成功。

Human Review：是否越界、成果證據與未完成是否誠實揭露。人不看程式：有修改時請 Agent 回答變更審查問題（改了哪些檔案與原因、測試數有沒有變少或新增跳過、有沒有刪測試或改既有期待值），已執行測試時看驗收對照表核對結果、跳過或未知失敗，並在 /docs 試主要行為；完整軟體交付仍需付款補償、Regression與文件。Level 1 Review分析／Gate／完整測試策略與未驗證範圍，不能將活動收件視為功能通過。

Decision：依實際成果核准、條件核准或拒絕並修正；Level 1／2 可如實作為活動成果，但不得冒稱完整程式交付。

Evidence：實際成果／對照表、審查結論與 [Delivery Summary](05-delivery-template.md)；有修改或實測時附變更審查答案、驗收對照表與 /docs 實測結果。Level 1 尚無修改或未執行測試時，審核Gate1／2、合理Impact、完整Test Strategy、未驗證範圍與未完成原因，明記「無修改／未執行」，不能宣稱功能PASS。時間不足仍審已有證據與缺項，不因缺少程式排除合法分析成果。

## Gate Decision

```text
Gate ID:
Decision: APPROVE | APPROVE WITH CONDITIONS | REJECT AND REVISE
Evidence Reviewed:
Conditions / Required Corrections:
Approver:
Timestamp / Workshop Minute:
```

由人填寫決策，Agent 不代填核准。無須電子簽章；條件含完成方式與需回到哪個 Gate。缺證據不得把核准當作測試通過。

## 完成條件

三 Gate 均有 Input、Review、Decision 與實際 Evidence；先核准再執行，偏差可追查，未完成與風險留在交付紀錄。
