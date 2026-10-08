# TASK-B3-001：新增團體訂票能力

> 讀者：Brownfield小組與主要Agent。時機：第63–76分鐘，13分鐘。前置：已驗收B2或正式Recovery、Shared Context與主要Agent可用。可見性：Participant，本階段才揭露。
> Agent角色：Digital Worker。

## 需求與邊界

團體訂票一次5–20人，所有旅客同一Trip。必須取得同一車廂足以容納整團的連續空位，否則整筆拒絕，不拆散、不部分成立；成功建立為PENDING_PAYMENT並一次保留全部座位。各旅客沿用B2最有利單一優惠，個別票價加總。

付款成功整筆PAID且只建立一筆Order；付款失敗整筆CANCELLED、全部座位釋放、無Order，留下Audit及取消通知。建立失敗無Booking、無Order、無座位殘留。

新增團體建立與付款入口；查詢可沿用既有Booking。最低回應需求為Booking ID、Type、Status、Total Fare、個別票價與Applied Discount明細、Assigned Seats，不在本卡規定完整Response或座位演算法。

保留一般1–4人及B2既有能力。不跨Trip或車廂，不提供候補、部分付款、特定座位偏好、前端、外部資料庫、真實金流或複雜最佳化套件。

## 人機責任與三個Gate

全程人本來就不寫程式、不讀程式；到B3連核准方式也變：人只透過三道Gate管Agent，只能Challenge、Review、Approve／Reject、要求補證或修正，判斷依據是驗收對照表、變更審查答案與 /docs 實測結果。Agent負責分析、設計、實作、測試、文件與摘要。

| Gate | Agent提交 | 人員決策與下一步 |
|---|---|---|
| 1 Requirement Understanding | 需求摘要、假設、資訊缺口、Out of Scope。 | 核准後才設計；未核准先補缺口。 |
| 2 Impact and Design | 影響模組、API、座位與Atomicity方案、測試策略及風險。 | 核准後才改程式；不一次跳到完成實作。 |
| 3 Code and Test Review | 驗收對照表、變更審查答案（白話說明改了哪些檔案、為什麼）、實際測試、規則追溯、文件與未完成項目。 | 人看驗收對照表與變更審查答案（不看程式）後Approve／Reject或要求修正。 |

使用短格式回覆，保留核准紀錄。

## 驗收與交付

| AC ID | 條件 |
|---|---|
| AC-B3-001 | 4人拒絕。 |
| AC-B3-002 | 5人可建立。 |
| AC-B3-003 | 容量足夠時20人可建立。 |
| AC-B3-004 | 21人拒絕。 |
| AC-B3-005 | 同車廂連續座位。 |
| AC-B3-006 | 無完整區段整筆拒絕。 |
| AC-B3-007 | 建立失敗無座位殘留。 |
| AC-B3-008 | 成功一次保留全部座位。 |
| AC-B3-009 | 逐旅客沿用B2政策。 |
| AC-B3-010 | 個別票價加總。 |
| AC-B3-011 | 成功付款整筆PAID。 |
| AC-B3-012 | 成功只一筆Order。 |
| AC-B3-013 | 付款失敗整筆CANCELLED。 |
| AC-B3-014 | 失敗釋放全部座位。 |
| AC-B3-015 | 失敗不建立Order。 |
| AC-B3-016 | 必要成功／失敗Audit。 |
| AC-B3-017 | 付款結果通知紀錄。 |
| AC-B3-018 | 原G1／B1／B2既有功能沒被改壞（既有測試通過）。 |
| AC-B3-019 | 文件、API Example與規則同步。 |

## 完成條件

交付Gate紀錄、Impact／方案、驗收對照表、變更審查答案、/docs 實測結果、實際測試、文件及摘要。Level1：Gate1／2、合理Impact與完整Test Strategy，Code未完成；Level2：團體建立及連續座位與主要Unit Test完成，補償或文件仍有缺項；Level3：建立、付款成功／失敗補償、Regression、文件及摘要完整。學習成果可為Level1／2，只有完整證據才能宣稱完整軟體交付。76分鐘到停止擴充並列缺項。
