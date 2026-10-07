# 產品演進：12 個月

| 時期 | 新增或調整 |
|---|---|
| 第 1–3 個月 | 首版上線：班次查詢、一般訂票（1–4 人）、模擬付款、Order 查詢。 |
| 第 4–6 個月 | 會員（一般／企業）、提前購票優惠、改票、退票、座位配置、通知紀錄與稽核紀錄。 |
| 第 7 個月 | 修正學生票價計算，學生票統一為 Base Fare 75%。 |
| 第 8–9 個月 | 優惠政策改為「逐旅客最有利單一優惠」，Booking 回應新增 applied_discounts 明細；見 [ADR 002](adr/002-introduce-discount-policy.md)。 |
| 第 10–12 個月 | 團體訂票（5–20 人、同車廂連續座位、付款失敗取消並釋放座位）；見 [ADR 004](adr/004-group-seat-atomicity.md)。會員資料加入點數餘額欄位，供後續會員權益使用。 |
| 第 13 個月 | 付款成功後開立電子發票（外部服務商經 Port／Adapter 接入，失敗可重試且不影響付款）；見 [ADR 005](adr/005-issue-e-invoices-through-a-port.md)。 |
| 第 14 個月 | 會員點數折抵：訂票時可用點數折抵票款（建立時預留，團體付款失敗與退票歸還）；見 [ADR 006](adr/006-membership-owns-points-redemption.md)。 |
| 第 15 個月 | 團體部分取消：已付款團體可取消部分旅客，依出發前天數收 10%／20%／30% 手續費後退款，只釋放被取消旅客的座位，一筆訂票可有多筆退款紀錄；見 [ADR 007](adr/007-group-booking-owns-passenger-cancellation.md)。 |

目前版本 1.7.0。各項規則以 [Business Rules](requirements/business-rules.md) 為準。
