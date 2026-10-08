---
id: b3
title: B3 團體訂票：Digital Worker 流程
minute: 63-76
group: b3
section: B3｜Digital Worker
---

# B3｜Digital Worker：由 Agent 主導交付

本段共 **13 分鐘**（第 63–76 分鐘），任務是 `TASK-B3-001` 團體訂票。Agent 的角色是 **Digital Worker**（數位員工）：今天 Agent 從工具、隊友，走到這一段能獨立執行任務的數位員工。Agent 主導分析、設計、實作、測試、文件及交付；人設定邊界、核准、挑戰與驗證，承擔最終提交責任。

```callout danger
人員不得直接修改程式
人員不得直接修改程式，只能挑戰假設、審查、核准或拒絕，並要求補證或修正。Agent 負責分析、設計、實作、測試、文件與摘要。

工具不支援自動修改時，Agent 可產生 Patch（修改檔），由環境套用；人員仍不得自行補寫程式或測試。
```

```callout warning
不要讓 Agent 跳過 Gate
本段分成 6 個檢查點，其中三個的「確認」就是人員核准關卡（Gate 1、Gate 2、Gate 3）。每個檢查點結束時 Agent 必須停下；由人填好該檢查點的確認，才交代下一步。Gate 2 核准且相關條件解除前，Agent 不得修改程式。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要貼給 Agent 的提示詞、要填的表單，全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。每個 Gate 控制 1–3 分鐘；例外判斷含在此時間，不額外加時。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 交辦 | 63–64 | 00–01 | 讀操作規則、填 Approved Context、把 Work Order 交給 Agent |
| 2 · Gate 1 需求理解 | 64–66 | 01–03 | 審查 Agent 的需求理解；第 66 分做 Gate 1 決策 |
| 3 · Gate 2 影響分析與設計 | 66–70 | 03–07 | 審查影響與設計；第 69 分做 Gate 2 決策、填核准範圍 |
| 4 · 依核准計畫執行 | 70–74 | 07–11 | Agent 在核准範圍內修改、測試、更新文件；人審查，不寫程式 |
| 5 · 停止擴充、整理證據 | 74–75 | 11–12 | 停止新增；記錄實際測試命令與結果；Agent 交 Gate 3 Input |
| 6 · Gate 3 與交付 | 75–76 | 12–13 | Gate 3 交付審查；Agent 交 Delivery Summary（交付摘要）與 Level（完成等級） |

## 本段文件

| 文件 | 用途 | 使用方式 |
|---|---|---|
| [B3 任務卡](#b3-task-card) | `TASK-B3-001` 需求、邊界與驗收條件（AC） | 必讀 |
| [Digital Worker 操作規則](#b3-operating-rules) | 人與 Agent 的可以／不得 | 必讀，目標 2 分鐘內讀完 |
| [Work Order](#b3-work-order)（工作命令） | 交給 Agent 的工作命令；填 Approved Context（已核准的背景資料）與 Gate 2 核准範圍 | 必讀；檢查點 1、3 填寫 |
| [Approval Gates](#b3-approval-gates)（核准關卡） | 三個人員核准關卡與決策短格式 | 必讀；檢查點 2、3、6 填寫 |
| [Review Checklist](#b3-review-checklist)（交付審查檢核表） | Gate 3 交付審查 | 按需使用（檢查點 6） |
| [Delivery Summary](#delivery) | Gate 3 及 B3 結束時的交付摘要 | 按需使用（檢查點 6） |
| [Exception Response 卡](#b3-exception-card)（例外回應卡） | 例外回應與 Escalation（升級處理：停下來交給人決定）短格式 | 按需使用 |

## 檢查點 1 · 交辦（第 63–64 分鐘）

- [ ] 讀 [Digital Worker 操作規則](#b3-operating-rules) 與 [B3 任務卡](#b3-task-card)。操作規則目標 2 分鐘內讀完，可在 Agent 準備 Gate 1 Input（Agent 交給 Gate 1 審查的資料）時讀完。

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

- [ ] 在 [Work Order](#b3-work-order) 先填小組與 Context（Approved Context）。「Gate 2 核准範圍」留到檢查點 3 再填。未填資料由小組確認，不由 Agent 猜測。
- [ ] 把下列內容交給主要 Agent。依操作規則的前置條件，Agent 需要已核准的 Shared Context、B2 接手版本與 B3 任務卡：

1. 已核准的 Shared Context 與 B2 接手版本。
2. [B3 任務卡](#b3-task-card) 全文。
3. [Digital Worker 操作規則](#b3-operating-rules) 全文。
4. [Work Order](#b3-work-order) 全文，加上已填寫的 Approved Context（可用表單的「複製 Markdown」）。
5. [Approval Gates](#b3-approval-gates) 全文，讓 Agent 知道每個 Gate 要提交的 Input。

- [ ] 連同上述內容貼上下方提示詞（文字取自上述文件，可依小組需要調整）。最後一句讓 Agent 這一次只做 Gate 1：

```text
請依附上的 Digital Worker Work Order 執行 TASK-B3-001，並遵守 Digital Worker 操作規則與 B3 人員核准 Gate。
1. 先提交 Gate 1 Input：需求摘要、規則清單、關鍵假設、資訊缺口、Out of Scope、需要人決定的問題。等待人員決策，核准需求才進入設計。
2. Gate 1 核准後提交 Gate 2 Input：受影響／不受影響模組、API Contract、Domain 變更、Seat Assignment 方案、Atomicity／Compensation 方案、測試策略、文件清單、主要風險與預計修改檔案。Gate 2 核准後才可改程式。
3. 遇 Work Order 的 Stop and Escalate Conditions，停止受影響動作，使用 Escalation 範本提出證據與決策需求，等待人員決策後才續行。
4. Gate 決策由人填寫，Agent 不代填核准。實際執行命令、結果與未執行部分均須記錄，不以預期代替實測。

這一次只做第 1 項：提交 Gate 1 Input 後停下，等我做 Gate 1 決策。不要開始設計，也不要修改任何檔案。
```

**確認**：[Work Order](#b3-work-order) 表單的小組、Agent／工作階段、背景資料版本、程式庫版本、已確認假設、尚待決定事項已填寫。

## 檢查點 2 · Gate 1 需求理解（第 64–66 分鐘）

Agent 交出 Gate 1 Input 後停下。**換你審查並決策**，決策前不要讓它進入設計。

- [ ] 確認 Agent 提交了 Gate 1 Input：需求摘要、規則清單、關鍵假設、資訊缺口、Out of Scope（不在範圍內的項目）、需要人決定的問題。
- [ ] 人員檢視（Review）：5–20 人邊界、同班次（Trip）／同車廂連續、無部分成功、失敗整筆取消及全釋放、B2 個別旅客優惠是否理解一致。
- [ ] 回答 Agent 列出的問題；查不到依據時由小組確認，不讓 Agent 自行假設。
- [ ] 最晚全場第 66 分鐘，在 [Gate 1 表單](#b3-approval-gates) 記錄決策。核准需求才進入設計；拒絕時要求修正。條件核准需說明哪些活動已允許、哪些仍被阻擋。三種決策：APPROVE＝核准；APPROVE WITH CONDITIONS＝附條件核准；REJECT AND REVISE＝退回修正。
- [ ] 用下方格式回覆 Agent。`〈 〉` 的內容由你填寫：

```text
Gate 1 決策：〈APPROVE／APPROVE WITH CONDITIONS／REJECT AND REVISE〉
審查依據：〈我核對了哪些規則與假設〉
條件／修正：〈沒有就寫「無」〉
我對你的問題的決定：〈逐項列出〉

〈核准時〉請提交 Gate 2 Input：受影響／不受影響模組、API Contract、Domain 變更、Seat Assignment 方案、Atomicity／Compensation 方案、測試策略、文件清單、主要風險與預計修改檔案。提交後停下等我做 Gate 2 決策，不要修改程式。
〈拒絕時〉請依上述修正重新提交 Gate 1 Input，然後停下等我。
```

```callout tip
決策紀錄由人填寫
三個 Gate 的決策請在 [Approval Gates](#b3-approval-gates) 頁面的表單中由人員填寫；表單會自動暫存，可匯出或複製 Markdown 保留核准紀錄。
```

**確認**：[Gate 1 表單](#b3-approval-gates)（Gate 核准決策 · GATE1）。

## 檢查點 3 · Gate 2 影響分析與設計（第 66–70 分鐘）

這一步 Agent **只提設計，不改程式**。

- [ ] 確認 Agent 提交了 Gate 2 Input：受影響／不受影響模組、API Contract（API 合約）、Domain 變更（業務模型變更）、Seat Assignment（座位分配）方案、Atomicity／Compensation（整筆成功或整筆失敗／失敗時復原已保留的座位等狀態）方案、測試策略、文件清單、主要風險與預計修改檔案。
- [ ] 人員 Review：範圍是否合理、避免全面重寫、建立與付款失敗均處理、座位釋放、Regression 保留與未核准外部依賴；不以方案看似合理取代授權檢查。
- [ ] 最晚全場第 69 分鐘，在 [Gate 2 表單](#b3-approval-gates) 記錄決策，並在 [Work Order](#b3-work-order) 填妥「Gate 2 核准範圍」。
- [ ] 第 69–70 分鐘：主持人若宣布例外事件，用 [Exception Response 卡](#b3-exception-card) 在 60 秒內記錄提議、證據、決策與給 Agent 的指令。時間緊可用 30 秒口頭判斷並留下簡短紀錄。
- [ ] Gate 2 核准且相關條件已解除後，才進入檢查點 4。條件未滿足的範圍先停止；偏差需補證或重新核准。

**確認**：[Gate 2 表單](#b3-approval-gates)（Gate 核准決策 · GATE2）與 [Work Order](#b3-work-order) 的「Gate 2 核准範圍」；有例外事件時加上 [Exception Response 卡](#b3-exception-card)。

## 檢查點 4 · 依核准計畫執行（第 70–74 分鐘）

- [ ] Gate 2 核准且條件解除後，交代 Agent 執行：

```text
Gate 2 決策：〈APPROVE／APPROVE WITH CONDITIONS〉
核准範圍：〈貼上 Work Order 的「Gate 2 核准範圍」〉
條件：〈列出條件，並說明已如何解除；沒有就寫「無」〉

請按核准計畫執行：只修改核准範圍內的檔案，建立與執行測試、更新文件。不要擴大範圍；與 Gate 2 計畫有偏差時先回報，等我核准。
遇 Work Order 的 Stop and Escalate Conditions，立即停止受影響動作，用 Escalation 短格式提出證據與決策需求，等我決定。
完成核准計畫或遇停止條件時停下，回報修改的檔案、執行的測試命令與實際結果，等我確認，不要自行進入交付。
```

- [ ] Gate 2 核准後，Agent 才按核准計畫修改、建立與執行測試、更新文件。條件未滿足的範圍先停止；偏差需補證或重新核准。
- [ ] 人員不寫程式、不替 Agent 補測試，持續挑戰假設與審查成果。
- [ ] 遇工作命令中的停止與升級條件（Stop and Escalate Conditions），Agent 停止受影響動作，使用 [升級處理範本](#b3-exception-card) 提出證據與決策需求；取得人員決策且相關條件解除後才續行。

```callout info
例外與升級
需要例外判斷時，使用 [Exception Response 卡](#b3-exception-card) 記錄提議、證據、決策與給 Agent 的指令；例外判斷含在本段限定時間（Timebox）內，不額外加時。一般停止條件使用同頁的 Escalation 短格式。
```

```form
{"id": "b3-cp4", "title": "檢查點 4 確認","fields":[
{"id": "files", "label": "Agent 修改的檔案，與 Gate 2 核准範圍對照", "type": "textarea", "hint": "超出核准範圍的檔案要註明。尚無修改就寫「無修改」及原因。", "suggestions": [{"label": "範圍內檔案", "text": "〈檔案〉：在 Gate 2 核准範圍內（〈修改目的〉）"}, {"label": "超出範圍", "text": "〈檔案〉：不在 Gate 2 核准範圍，已要求 Agent 回報理由／還原"}, {"label": "無修改", "text": "無修改，原因：〈原因〉"}]},
{"id": "escalations", "label": "偏差或停止升級事件與人員決策", "type": "textarea", "hint": "沒有就寫「沒有」。有升級時另填 Escalation 表單。", "suggestions": [{"label": "偏差與決策", "text": "〈事件〉：Agent 於第〈分〉分停止並回報；人員決策：〈核准／拒絕／要求補證〉"}, "沒有"]},
{"id": "human-no-code", "label": "人員沒有直接修改程式或補測試", "type": "checkbox"}
]}
```

## 檢查點 5 · 停止擴充、整理證據（第 74–75 分鐘）

**不再新增功能。**

- [ ] 要求 Agent 停止擴充並整理證據：

```text
停止擴充，不要再新增功能。
已有程式修改時，執行測試並貼出實際命令與完整輸出；尚無修改或未執行測試時，明記「無修改／未執行」、原因與未驗證範圍，不要預填成功。
接著提交 Gate 3 Input：當前成果摘要、Acceptance Criteria 對照、Rule Traceability、未完成事項、已知風險及交付建議；有修改時附實際修改檔案，有測試時附命令與真實結果。提交後停下，等我做 Gate 3 決策。
```

- [ ] 停止擴充。實際執行命令、結果與未執行部分均須記錄，不以預期代替實測。
- [ ] 尚無修改或未執行測試時，明記「無修改／未執行」及原因與未驗證範圍，不預填成功。

```form
{"id": "b3-cp5", "title": "檢查點 5 確認","fields":[
{"id": "test-command", "label": "實際執行的測試命令", "type": "text", "hint": "未執行就寫「未執行」。", "suggestions": ["pytest -q", "未執行"]},
{"id": "test-result", "label": "實際結果", "type": "text", "hint": "照 Agent 貼出的實際輸出填寫，例如 passed／failed／skipped 數量。", "suggestions": [{"label": "測試數量", "text": "〈數字〉 passed、〈數字〉 failed、〈數字〉 skipped"}, {"label": "未執行", "text": "未執行：〈原因〉"}]},
{"id": "not-run", "label": "未執行或未驗證的項目與原因", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": [{"label": "未驗證項目", "text": "〈項目〉：未驗證，原因：〈原因〉"}, "沒有"]}
]}
```

## 檢查點 6 · Gate 3 與交付（第 75–76 分鐘）

- [ ] 確認 Agent 提交了 Gate 3 Input：當前成果摘要、驗收條件（Acceptance Criteria）對照、規則追溯（Rule Traceability：每條規則對到哪段程式、測試與文件）、未完成事項、已知風險及交付建議；有修改時附實際檔案，有測試時附命令與真實結果。
- [ ] 人員審查（可用 [交付審查檢核表](#b3-review-checklist)）：是否越界、成果證據與未完成事項是否如實揭露。對照你在檢查點 4、5 的確認紀錄；不一致時以你的實際確認為準。
- [ ] 在 [Gate 3 表單](#b3-approval-gates) 記錄決策：依實際成果核准、條件核准或拒絕並修正。
- [ ] 要求 Agent 交付：

```text
Gate 3 決策：〈APPROVE／APPROVE WITH CONDITIONS／REJECT AND REVISE〉
條件／修正：〈沒有就寫「無」〉

請依 Delivery Summary 範本整理交付摘要。Completion Level 從 Level 1–3 擇一並說明證據，不要自動選 Level 3；沒有實際執行過的項目標為「未驗證」。交出後停止，不再新增功能。
```

- [ ] Agent 交付 [Delivery Summary](#delivery) 與 Completion Level（完成等級：Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付；擇一並說明證據，不自動選 Level 3）。
- [ ] 全場第 76 分鐘到，停止擴充並列出缺項。

```callout warning
時間不足時
13 分鐘內保留三個核准關卡與真實證據；時間不足保留 Gate 1／2，Gate 3 至少審查測試及未完成事項，例外可縮短為 30 秒判斷。依 Level 1–3 如實交付。若已完成分析，可交付 Level 1；即使無程式修改或未執行測試，也須交付分析、核准紀錄、未驗證範圍與原因，不宣稱功能已通過驗收。
```

**確認**：[Gate 3 表單](#b3-approval-gates)（Gate 核准決策 · GATE3）；有使用時加上 [交付審查檢核表](#b3-review-checklist)。

## 必要時受控接續

未完成前一段時，主持人只於進入本段時按需核准並提供獨立解鎖碼。到 [B2 Recovery](#recovery-b2) 下載及切換；保留原成果、未完成及來源；Recovery（復原包：進度落後時改用的接續基線）不算小組自行完成。B3開始後不再換版，改交分析／檢視（Review）成果。
