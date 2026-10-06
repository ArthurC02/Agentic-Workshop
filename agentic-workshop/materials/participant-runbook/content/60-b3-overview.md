---
id: b3
title: B3 團體訂票：Digital Worker 流程
minute: 63-76
group: b3
section: B3｜Digital Worker
---

# B3｜Digital Worker：由 Agent 主導交付

本段共 **13 分鐘**（第 63–76 分鐘），任務是 `TASK-B3-001` 團體訂票。Agent 的角色是 **Digital Worker**：Agent 主導分析、設計、實作、測試、文件及交付；人設定邊界、核准、挑戰與驗證，承擔最終提交責任。

## 規則改變：人不直接寫程式

```callout danger
人員不得直接修改程式
人員不得直接修改程式，只能挑戰假設、審查、核准或拒絕，並要求補證或修正。Agent 負責分析、設計、實作、測試、文件與摘要。

工具不支援自動修改時，Agent 可產生 Patch，由環境套用；人員仍不得自行補寫程式或測試。
```

本段人員可以做的事：

- **挑戰假設（Challenge）**：要求 Agent 解釋假設，挑戰方案與風險。
- **審查（Review）**：檢查程式差異（Diff）、測試與文件。
- **核准／拒絕（Approve／Reject）**：在三個核准關卡（Approval Gate）做決策。
- **要求補證或修正**：證據不足時要求補證，或要求 Agent 修正。
- **中止 Agent**：衝突、資訊不足或超權限時停止並升級。

| 角色 | 可以 | 不得 |
|---|---|---|
| 人 | 提供需求、要求解釋假設、Challenge、Review Diff／測試／文件、Approve／Reject、要求補證與修正，或中止 Agent。 | 直接 Coding、修改程式或替 Agent 補測試，不跳過 Gate，也不因時間壓力接受未驗證說法。 |
| Agent | 理解 Repository、分析影響、提出選項，按核准計畫修改、建立與執行測試、更新文件及揭露未完成事項。 | 越過核准範圍、未核准變更 API、自行改商業規則、加入外部服務／資料庫／規則引擎、刪弱測試、捏造通過結果或在 Gate 未核准前前進。 |

## 本段文件

| 文件 | 用途 | 使用方式 |
|---|---|---|
| [B3 任務卡](#b3-task-card) | `TASK-B3-001` 需求、邊界與驗收條件（AC） | 必讀 |
| [Digital Worker 操作規則](#b3-operating-rules) | 人與 Agent 的可以／不得 | 必讀，目標 2 分鐘內讀完 |
| [Work Order](#b3-work-order) | 交給 Agent 的工作命令；填 Approved Context 與 Gate 2 核准範圍 | 必讀 |
| [Approval Gates](#b3-approval-gates) | 三個人員核准 Gate 與決策短格式 | 必讀 |
| [Review Checklist](#b3-review-checklist) | Gate 3 交付審查 | 按需使用 |
| [Delivery Summary](#delivery) | Gate 3 及 B3 結束時的交付摘要 | 按需使用 |
| [Exception Response 卡](#b3-exception-card) | 例外回應與 Escalation 短格式 | 按需使用 |

## B3 的 13 分鐘安排

B3 13 分鐘；每 Gate 控制 1–3 分鐘。例外判斷含在此時間，不額外加時。

| B3 開始後幾分鐘 | 全場第幾分鐘 | 節點 |
|---:|---:|---|
| 0 | 63 | 發放 B3 文件，填 Work Order 並交給 Agent |
| 3 | 66 | Gate 1 決策 |
| 6 | 69 | Gate 2 決策 |
| 7 | 70 | 開始執行 |
| 11 | 74 | 停止擴充測試 |
| 12 | 75 | Gate 3 Review |
| 13 | 76 | 交付 |

### B3 開始時（全場第 63 分鐘）：閱讀與交辦

- [ ] 2 分鐘內讀完 [Digital Worker 操作規則](#b3-operating-rules)，並閱讀 [B3 任務卡](#b3-task-card)。
- [ ] 在 [Work Order](#b3-work-order) 先填小組與 Context（Approved Context）。未填資料由小組確認，不由 Agent 猜測。
- [ ] 將 Work Order 與相關文件交給主要 Agent（見下方「交給 Agent 的內容」）。

### B3 開始後 0–3 分鐘（全場第 63–66 分鐘）：Gate 1 需求理解

- [ ] Agent 提交 Gate 1 Input：需求摘要、規則清單、關鍵假設、資訊缺口、Out of Scope、需要人決定的問題。
- [ ] 人員 Review：5–20 邊界、同 Trip／同車廂連續、無部分成功、失敗整筆取消及全釋放、B2 個別旅客優惠是否理解一致。
- [ ] B3 開始後第 3 分鐘，在 [Gate 1 表單](#b3-approval-gates) 記錄決策。核准需求才進入設計；拒絕時要求修正。

### B3 開始後 3–6 分鐘（全場第 66–69 分鐘）：Gate 2 影響分析與設計

- [ ] Agent 提交 Gate 2 Input：受影響／不受影響模組、API Contract、Domain 變更、Seat Assignment 方案、Atomicity／Compensation 方案、測試策略、文件清單、主要風險與預計修改檔案。
- [ ] 人員 Review：範圍是否合理、避免全面重寫、建立與付款失敗均處理、座位釋放、Regression 保留與未核准外部依賴；不以方案看似合理取代授權檢查。
- [ ] B3 開始後第 6 分鐘，在 [Gate 2 表單](#b3-approval-gates) 記錄決策，並在 [Work Order](#b3-work-order) 填妥「Gate 2 核准範圍」。核准且相關條件已解除後，才可修改程式。

### B3 開始後 7–11 分鐘（全場第 70–74 分鐘）：依核准計畫執行

- [ ] Gate 2 核准後，Agent 才按核准計畫修改、建立與執行測試、更新文件。條件未滿足的範圍先停止；偏差需補證或重新核准。
- [ ] 人員不寫程式、不替 Agent 補測試，持續挑戰假設與審查成果。
- [ ] 遇工作命令中的停止與升級條件（Stop and Escalate Conditions），Agent 停止受影響動作，使用 [升級處理範本](#b3-exception-card) 提出證據與決策需求；取得人員決策且相關條件解除後才續行。

### B3 開始後第 11 分鐘（全場第 74 分鐘）：停止擴充測試

- [ ] 停止擴充。實際執行命令、結果與未執行部分均須記錄，不以預期代替實測。
- [ ] 尚無修改或未執行測試時，明記「無修改／未執行」及原因與未驗證範圍，不預填成功。

### B3 開始後第 12 分鐘（全場第 75 分鐘）：Gate 3 交付審查

- [ ] Agent 提交 Gate 3 Input：當前成果摘要、Acceptance Criteria 對照、Rule Traceability、未完成事項、已知風險及交付建議；有修改時附實際檔案，有測試時附命令與真實結果。
- [ ] 人員審查（可用 [交付審查檢核表](#b3-review-checklist)）：是否越界、成果證據與未完成事項是否如實揭露。
- [ ] 在 [Gate 3 表單](#b3-approval-gates) 記錄決策：依實際成果核准、條件核准或拒絕並修正。

### B3 開始後第 13 分鐘（全場第 76 分鐘）：交付

- [ ] Agent 交付 [Delivery Summary](#delivery) 與 Completion Level（Level 1–3 擇一並說明證據，不自動選 Level 3）。
- [ ] 全場第 76 分鐘到，停止擴充並列出缺項。

```callout warning
時間不足時
13 分鐘內保留三個核准關卡與真實證據；時間不足保留 Gate 1／2，Gate 3 至少審查測試及未完成事項，例外可縮短為 30 秒判斷。依 Level 1–3 如實交付。若已完成分析，可交付 Level 1；即使無程式修改或未執行測試，也須交付分析、核准紀錄、未驗證範圍與原因，不宣稱功能已通過驗收。
```

```callout info
例外與升級
需要例外判斷時，使用 [Exception Response 卡](#b3-exception-card) 記錄提議、證據、決策與給 Agent 的指令；例外判斷含在 Timebox 內，不額外加時。一般停止條件使用同頁的 Escalation 短格式。
```

## 交給 Agent 的內容

依 [操作規則](#b3-operating-rules) 的前置條件，Agent 需要已核准的 Shared Context、B2 接手版本與 B3 任務卡。請提供：

1. 已核准的 Shared Context 與 B2 接手版本。
2. [B3 任務卡](#b3-task-card) 全文。
3. [Digital Worker 操作規則](#b3-operating-rules) 全文。
4. [Work Order](#b3-work-order) 全文，加上已填寫的 Approved Context（可用表單的「複製 Markdown」）。
5. [Approval Gates](#b3-approval-gates) 全文，讓 Agent 知道每個 Gate 要提交的 Input。

交辦時可參考下列說明（文字取自上述文件，可依小組需要調整）：

```text
請依附上的 Digital Worker Work Order 執行 TASK-B3-001，並遵守 Digital Worker 操作規則與 B3 人員核准 Gate。
1. 先提交 Gate 1 Input：需求摘要、規則清單、關鍵假設、資訊缺口、Out of Scope、需要人決定的問題。等待人員決策，核准需求才進入設計。
2. Gate 1 核准後提交 Gate 2 Input：受影響／不受影響模組、API Contract、Domain 變更、Seat Assignment 方案、Atomicity／Compensation 方案、測試策略、文件清單、主要風險與預計修改檔案。Gate 2 核准後才可改程式。
3. 遇 Work Order 的 Stop and Escalate Conditions，停止受影響動作，使用 Escalation 範本提出證據與決策需求，等待人員決策後才續行。
4. Gate 決策由人填寫，Agent 不代填核准。實際執行命令、結果與未執行部分均須記錄，不以預期代替實測。
```

```callout tip
決策紀錄由人填寫
三個 Gate 的決策請在 [Approval Gates](#b3-approval-gates) 頁面的表單中由人員填寫；表單會自動暫存，可匯出或複製 Markdown 保留核准紀錄。
```

## 必要時受控接續

未完成前一段時，主持人只於進入本段時按需核准並提供獨立解鎖碼。到 [B2 Recovery](#recovery-b2) 下載及切換；保留原成果、未完成及來源，Recovery不算小組自行完成。B3開始後不再換版，改採分析／Review成果。
