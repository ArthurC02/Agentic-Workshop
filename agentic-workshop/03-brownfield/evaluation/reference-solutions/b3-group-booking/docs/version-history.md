# G1 → B0 → B1 → B2 → B3 Version History

> 讀者：主持人、驗收人員與產製Agent。時機：來源與版本差異核對。前置：閱讀README及本版驗證報告。可見性：Evaluation／Agent Production。

G1核心MVP；B0會員／優惠／售後／座位／紀錄；B1學生率修復；B2逐旅客最有利單一優惠與Applied Discounts。B3 - Group Booking從已驗收B2延伸5–20人團體、同車廂完整連續區段、一次保留與付款失敗補償，B2計價與原一般能力保留。

固定Seed容量不變，幾何映射以每車廂20個Position分配既有Seat IDs；可支援多車廂搜尋，但不把所有Trip容量變40。Group Change明確不支援、Paid Group Refund保留；此邊界促使Change指南同步Fare Difference。Tag為b3-group-booking；實際Commit／Bundle及快照核對由維護者留正式證據，本頁不代替驗證。

## 完成條件

演化祖先、Code／Test／Docs差異與Tag來源可追查，標準實作完整驗收與學員Level1／2／3分開判定。
