# Digital Worker Work Order

> 讀者：小組與主要 Coding Agent。
> 使用時機：B3 發放後交給 Agent；先填小組與 Context，Gate 2 範圍待設計核准時填寫。
> 前置條件：核准 Shared Context 及 [B3 任務卡](../../03-brownfield/participant/task-cards/03-b3-group-booking.md)。

## Mission

執行 `TASK-B3-001` 團體訂票；Agent 主導交付，人負責三個 Approval Gate。

## Approved Requirements

5–20 人搭同一 Trip；必須同車廂連續空位，找不到完整區段整筆拒絕。建立成功仍待付款；付款成功整筆成立且一筆 Order，失敗整筆取消、釋放全部座位且無 Order。每位旅客沿用 B2 個別最有利單一優惠並加總，不疊加。保留一般訂票與既有會員、改退票、通知、Audit 能力。無部分成功、分次付款、候補或特定座位偏好。

## Business Rules

- `GROUP-001`：至少 5 人；`GROUP-002`：最多 20 人。
- `GROUP-003`：同一 Trip；`GROUP-004`：同車廂連續座位。
- `GROUP-005`：無完整配置不建立；`GROUP-006`：一次保留全部；`GROUP-007`：建立失敗不保留任何座位。
- `GROUP-PAY-001`：成功轉 PAID；`GROUP-PAY-002`：失敗轉 CANCELLED；`GROUP-PAY-003`：失敗釋放全部；`GROUP-PAY-004`：失敗無 Order；`GROUP-PAY-005`：成功唯一 Order。
- `GROUP-FARE-001`：逐人沿用 B2；`GROUP-FARE-002`：總價逐人加總。
- `GROUP-AUDIT-001`：建立、付款成功／失敗留存 Audit。
- `GROUP-NOTIFY-001`：成功通知；`GROUP-NOTIFY-002`：失敗取消通知。

B2 的 `FARE-007`–`FARE-010` 持續適用：不可疊加、最低合格單一折扣率、逐旅客判定、記錄實際 Type／Rate。成人 100%、學生 75%、提前至少 14 天 85%、企業會員 95% 為優惠資格。

## Approved Context

小組：____；主要 Agent／Session：____；Context 版本：____；接手 Repository 版本：____；已確認假設／限制：____；尚待決定事項：____。未填資料由小組確認，不由 Agent 猜測。

## Allowed Change Scope

Gate 2 核准範圍：____。允許為團體流程所需的 API、Domain、Application、座位配置、付款補償、測試與文件修改；每個預計檔案均須先提出影響理由。

## Prohibited Change Scope

不全面重寫一般 Booking、不修改不相關 API、不移除既有功能／Regression、不引入外部服務、資料庫或第三方規則引擎；不自行改商業規則、技術棧或既定容量。API Contract 改動須先取得核准。

## Required Deliverables

需求理解、Impact Analysis、核准計畫與 Gate 證據、核准範圍內 Diff、測試結果、文件、Rule／Acceptance 對照，以及 [Delivery Summary](05-delivery-template.md) 與未完成事項。來源與結果須可追查。

## Required Tests

5／20 合法、4／21 非法，同廂連續與無完整區段，建立失敗無殘留，逐人 B2 計價，付款成功唯一 Order，失敗取消／全釋放／無 Order，Audit／通知與既有 Regression。實際執行命令、結果與未執行部分均須記錄，不以預期代替實測。

## Approval Gates

依 [三 Gate](03-approval-gates.md)：Gate 1 需求、Gate 2 影響與設計、Gate 3 交付 Review。決策含審查證據、條件、核准人與分鐘；條件未滿足不得擴大核准。

## Stop and Escalate Conditions

以下任一觸發即停止受影響動作，提出證據與決策需求：

1. Requirement 與 Rule ID 衝突。
2. Participant 文件與程式衝突且 Test 無法判定。
3. 需修改核准範圍外 API Contract。
4. 需新增外部服務或套件。
5. 需移除既有 Regression Test。
6. 無法確認付款失敗的正確狀態。
7. 找不到同時滿足座位與 Atomicity 的方案。
8. 測試有與任務無關的新失敗。
9. 修改檔案數顯著超過 Gate 2 預估。
10. 剩餘時間不足完成承諾交付。

使用 [Escalation 範本](06-exception-response-card.md#escalation)，等待人員決策後才續行。

## Timebox

B3 13 分鐘；每 Gate 控制 1–3 分鐘。第 3 分鐘 Gate 1 決策、第 6 分鐘 Gate 2 決策，第 7 分鐘起執行、第 11 分鐘停止擴充測試、第 12 分鐘 Review、第 13 分鐘交付。例外判斷含在此時間，不額外加時。

完成條件：小組先確認 Context，於 Gate 2 填妥核准範圍；Agent 理解規則與停止條件，保留核准證據與誠實完成度，未完成部分不宣稱驗收通過。
