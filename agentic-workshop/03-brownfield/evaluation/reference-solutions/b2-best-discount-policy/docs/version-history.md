# G1 → B0 → B1 → B2 Version History

> 讀者：主持人、驗收人員與教材產製Agent。時機：版本來源查核。前置：閱讀README與本版驗證報告。可見性：Evaluation／Agent Production。

G1提供核心MVP；B0在12個月故事中新增會員、提前優惠、改退票、座位、Notification與Audit；B1修復學生票率並保留既有優惠順序。

B2 - Best Single Discount Policy延續已驗收B1，導入FARE-007至010：逐旅客全候選最低rate、不可疊加、結果記Type／Rate／Amount。建立與改票共用政策，Booking根層新增applied_discounts，原Passenger合約保留。折扣文件同步、DEBT-001局部改善；DEBT-002同步通知與未涉及的舊改票指南落差保留，未提前實作團體功能。

本版Tag指定 `b2-best-single-discount`；實際案例Commit、Bundle與快照一致性由維護者完成後留證，不以本敘述宣稱已建立歷史或驗收。全套與原G1／B1 Regression須完整執行，結果見本版Validation Report。

## 完成條件

來源祖先、政策與API差異可追查，文件與metadata一致，實際歷史與驗證證據另核實。
