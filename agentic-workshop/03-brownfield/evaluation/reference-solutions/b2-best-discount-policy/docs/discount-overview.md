# B2 最有利單一優惠政策

> 讀者：參與者與Agent。時機：了解優惠資格與B2優惠政策。前置：閱讀主要Business Rules。可見性：Participant。

每位Passenger獨立列出符合資格的候選：ADULT 100%（全額預設）、STUDENT 75%、ADVANCE 85%（購票日至出發日至少14天）、CORPORATE 95%（企業會員）。加入全額預設後，選rate最低的單一候選，不疊乘、不以條件先後擋掉更有利資格；個別整數票價加總為Booking Total。

學生加提前75%、企業加提前85%、學生企業提前同時符合75%；無資格成人100%。建立與改票重新計價共用同一政策與可注入Clock。13天無提前、14／15天有提前資格，不能依當日日期判斷。

Booking根層applied_discounts逐位記錄passenger_id、discount_type、rate、amount；passengers保留原三欄。改票更新Applied Discounts及new-old Fare Difference；Order.amount仍為原付款快照，不執行補款／退款。

本版本已明確定義多種優惠同時符合時的選擇方式；通知仍維持同步紀錄。舊change-booking-guide的金額敘述仍需主要規則與API交叉核對，不以其舊文字否定Fare Difference記錄。

## 完成條件

FARE-007至010可追溯，代表組合與逐位明細、改票政策、文件均一致；實際結果以本機測試輸出為準。
