# TASK-B2-001：導入不可疊加的最有利優惠政策

> 讀者：Brownfield小組與主要Agent。時機：第52–63分鐘，11分鐘。前置：使用已完成或主持人提供的已驗收B1，更新Shared Context。可見性：Participant；本階段才發放。
> Agent角色：Teammate→Digital Worker過渡。

## 情境與規則

Smart Ticket要求多項優惠同時符合時，採對該旅客最有利的單一優惠，不可疊加。成人Base Fare100%、學生75%、提前至少14天85%、企業會員95%；各旅客獨立評估後加總Booking Total。

例如學生加提前採75%，企業加提前採85%，三項同時符合採75%；不把75%與85%相乘，成人無資格時100%。

| Rule ID | 新政策 |
|---|---|
| FARE-007 | 多項優惠不可疊加。 |
| FARE-008 | 多項同時符合採數值最低的單一折扣率。 |
| FARE-009 | 每位Passenger獨立決定優惠。 |
| FARE-010 | Fare Result記錄實際採用Discount Type與Rate。 |

## 人與Agent合作及交付

先要求Agent分析規則交互作用與跨模組影響，提出2–3個可行方案、取捨與風險。由人Challenge假設、選方案並核准Task Breakdown，再由主要Agent主導實作；人審查規則、測試、文件與Diff。

交付Impact Analysis（一定要改／可能影響／不應改）、方案比較、核准計畫、程式Diff、代表組合與完整Regression結果、更新文件及摘要。Booking建立與改票重新計價須政策一致，API需呈現實際採用優惠。保留原旅客Request／Response三欄；如擴充Booking回應，以根層applied_discounts明細包含passenger_id、discount_type、rate、amount。

不可疊乘、不對整筆訂票只選同一優惠、不將政策塞入Router、不引入Rule Engine／第三方規則套件、不全面重寫、不新增團體功能。原付款／改退票、座位、Audit與同步通知應保留；學生修復與原正確Regression不可弱化。

## 驗收條件

| AC ID | 條件 |
|---|---|
| AC-B2-001 | 成人無資格100%。 |
| AC-B2-002 | 學生75%。 |
| AC-B2-003 | 提前購票成人85%。 |
| AC-B2-004 | 企業會員成人95%。 |
| AC-B2-005 | 學生加提前75%。 |
| AC-B2-006 | 企業會員加提前85%。 |
| AC-B2-007 | 學生、企業、提前同時符合75%。 |
| AC-B2-008 | 不疊加。 |
| AC-B2-009 | 不同旅客可採不同優惠。 |
| AC-B2-010 | 結果含實際Discount Type與Rate。 |
| AC-B2-011 | 改票重新計價遵循相同政策。 |
| AC-B2-012 | B1與原G1 Regression通過。 |
| AC-B2-013 | 折扣文件與程式同步。 |

## 完成條件

核准紀錄、政策、實際測試及文件一致。63分鐘到停止擴充；未完成時保留Policy Design、Test Cases、文件清單與缺項，不宣稱完整交付。
