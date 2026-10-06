# B3 Approval Gate主持Cue

> 讀者：主持人。時機：活動第63–76分鐘。前置：B3與治理材料已發放，主要Agent及人員核准者已選定。可見性：Facilitator。

| B3相對分鐘 | 活動分鐘 | Cue與決策 |
|---|---|---|
| 0 | 63 | 發B3與Operating Rules，宣布人不直接改Code。 |
| 1 | 64 | Agent開始Gate1：摘要、假設、缺口、Out of Scope。 |
| 3 | 66 | 人做Gate1決策；核准才進Gate2設計。 |
| 3 | 66 | Agent開始Gate2：Impact、API／Seat／Atomicity、測試及風險。 |
| 6 | 69 | 人做Gate2決策，處理唯一SQLite例外。 |
| 7 | 70 | 例外與條件已解除，Agent才按核准計畫執行。 |
| 11 | 74 | 停止擴充；已有程式時執行測試，整理證據、文件與缺項。尚無程式則明記未執行及原因。 |
| 12 | 75 | Gate3 Review：有修改／實測時審Diff、實際結果、Rule與文件；Level 1 無修改／未執行時審Gate1／2、合理Impact、完整Test Strategy與缺項，不宣稱功能PASS。 |
| 13 | 76 | Agent交摘要與Level，停止新增功能。 |

Gate回覆採短格式：

```text
Decision: APPROVE | APPROVE WITH CONDITIONS | REJECT AND REVISE
Evidence Reviewed:
Conditions / Required Corrections:
Approver:
Timestamp / Workshop Minute:
```

條件核准不等於可忽略條件直接執行：條件必須具體、可驗證且先解除；若SQLite仍在方案，不能改Code。例外處理占相對6–7分鐘內最多60秒，必要縮為30秒但不刪事件或再注入。若Gate或條件未完成，仍維持停止線與誠實成果分級，不假核准趕進度。

## 完成條件

0／1／3／6／7／11／12／13節奏及活動63–76對應清楚，核准、條件解除、實際執行與Review時間有紀錄。
