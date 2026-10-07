# 最有利單一優惠政策

每位 Passenger 獨立列出符合資格的候選：ADULT 100%、STUDENT 75%、ADVANCE 85%（購票日至出發日至少 14 天）、CORPORATE 95%（企業會員）。加入全額預設後，選 rate 最低的單一候選，不疊乘、不以條件先後擋掉更有利資格；個別整數票價加總為 Booking Total。

學生加提前 75%、企業加提前 85%、學生企業提前同時符合 75%；無資格成人 100%。建立與改票重新計價共用同一政策與 Clock。13 天無提前、14／15 天有提前資格，以系統 Clock 判斷，不依實際當日日期。

Booking 根層 applied_discounts 逐位記錄 passenger_id、discount_type、rate、amount；passengers 保留原三欄。改票更新 Applied Discounts 及 new-old Fare Difference；Order.amount 仍為原付款快照，不執行補款／退款。

相關規則：FARE-001 至 FARE-010、MEMBER-003、GROUP-FARE-001／002，見 [Business Rules](business-rules.md)。
