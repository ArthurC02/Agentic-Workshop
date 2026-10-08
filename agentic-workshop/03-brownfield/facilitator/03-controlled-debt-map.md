# Controlled Debt Map

> 讀者：主持人與驗收人員。時機：B0驗收、觀察Context Verification。前置：熟悉Repository與規則。可見性：Facilitator／Evaluation。

| Debt ID | Location | Historical Reason | Learning Purpose | Participant Visibility | Must Fix Now | Acceptable Handling |
|---|---|---|---|---|---|---|
| DEBT-001 | Domain Discount／Fare Policy | 優惠陸續加入，依既有條件選首個符合 | 理解政策成長及跨模組影響 | 可請Agent從程式與測試找出並說明，不直接標答案 | 否，B0保留 | B1不改順序；規則政策任務另行處理 |
| DEBT-002 | Payment／Change／Refund→Notification | MVP以同步本機紀錄降低複雜度 | 說明耦合與歷史取捨 | 可見ADR與呼叫關係 | 否 | 保留同步紀錄，不要求Queue／外部服務 |
| DEBT-003 | docs/change-booking-guide.md | 程式新增Fare Difference，舊指南未更新 | Context Verification | 不主動揭露文件位置 | 否，B0保留 | 主要規則與API正確；學員交叉核對，不全面改寫 |

文件落差精確兩項：上列改票指南未記Fare Difference，以及 `docs/discount-overview.md` 未清楚定義多優惠優先順序。實際目前Policy為CORPORATE→ADVANCE→STUDENT→ADULT首個符合，不是最有利政策。這兩處以外的README、Contract、核心與主要Business Rules不得刻意寫錯。

唯一Bug `BUG-B0-001` 為學生率85%而非正確75%；其失敗Manifest與因果驗證在Evaluation，不是技術債追加項。禁止把Bug、文件落差與三項債混計。

## 完成條件

精確三項債、兩項落差與一個Bug各有範圍、歷史與處理界線；學員包不含此答案地圖。
