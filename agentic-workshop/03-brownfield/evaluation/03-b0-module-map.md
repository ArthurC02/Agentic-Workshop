# B0 Module Map

> 讀者：主持人與Evaluation／產製Agent。時機：評估Repository Understanding、設計後續演化。前置：閱讀B0架構與規則。可見性：內部，不提供Participant。

所有Code路徑相對`participant/repository/smart-ticket-b0/src/smart_ticket/`，Tests相對其`tests/`；Document位於該Repo `docs/`。

| Module | Responsibility | Upstream Dependency | Downstream Dependency | Primary Rules | Primary Tests | Related Documentation | Expected Future Change |
|---|---|---|---|---|---|---|---|
| api/routes.py、schemas/contracts.py | Request／Response與端點分派 | HTTP | Application、Domain型別 | API相容／錯誤 | integration/test_features.py、test_b0_api.py | api-examples.md | B3另加團體入口 |
| api/dependencies.py、main.py | 本機組裝、Reset、Health、Error mapping | Router／pytest | Store、Gateway、Services | 統一404／409／422 | test_health.py、test_seats.py | architecture.md | 保持輕量組裝 |
| application/trip_service.py | 可售班次與精確篩選 | Router | Repository／Trip | TRIP-001–002 | test_features.py、test_seed.py | business-rules.md | 保留查詢相容 |
| application/booking_service.py | 驗證會員／人數、計價、保留與Audit | Router／Change | Member、Discount、Seat、Audit、Store | BOOKING-001–005、MEMBER-001–002 | unit/test_services.py、test_members.py、test_seats.py | architecture.md | 團體另UseCase |
| domain/fare_policy.py、discounts.py | 個別票價與歷史優惠firstmatch | Booking／Change | MemberType／PassengerType | FARE-001–006、MEMBER-003 | unit/test_fare_policy.py、test_advance.py | business-rules.md、discount-overview.md、ADR002 | B1學生率／B2優惠策略 |
| domain/models.py、members.py、records.py | Booking／Order／Trip及新增紀錄型別 | Schema／Services／Store | Python dataclass／enum | 狀態與關聯 | 全套Service／Integration | architecture.md | B3團體必要擴充 |
| application/member_service.py | 固定會員查詢及有效性 | Booking／Router | Store.members | MEMBER-001–003 | test_members.py、test_seed.py | business-rules.md | B2優惠資格沿用 |
| application/seat_service.py | 規劃唯一Seat、保留與釋放 | Booking／Change／Refund | capacity／assignments／Trip | SEAT-001–002、BOOKING-003–004 | test_seats.py、test_changes.py、test_refunds.py | architecture.md | B3連續區段另設計 |
| application/payment_service.py | Pending付款、唯一Order、成功事件 | Router | Gateway、Store、Notification／Audit | PAYMENT-001–003、ORDER-001–002、NOTIFY-001 | unit/test_services.py、test_features.py、test_records.py | api-examples.md | B3補償不得提前加入 |
| application/order_service.py | 原付款快照查詢 | Router | Store.orders | ORDER-001–002 | test_features.py、test_refunds.py | business-rules.md | 保留付款語意 |
| application/change_booking_service.py | Paid改票、目標容量、差額及轉座位 | Router | Member／Discount／Seat／Notification／Audit | CHANGE-001–004、NOTIFY-002、AUDIT-002 | test_changes.py、test_b0_api.py | business-rules.md、change-booking-guide.md | B2計價沿用新策略 |
| application/refund_service.py | Paid退票一次、放座位與紀錄 | Router | Seat／Notification／Audit／Store | REFUND-001–004、NOTIFY-003、AUDIT-002 | test_refunds.py、test_records.py | business-rules.md | 不新增外部退款 |
| application/notification_service.py | 同步建立／查詢本機通知 | Payment／Change／Refund／Router | Store.notifications | NOTIFY-001–003 | test_records.py、test_changes.py | ADR003 | B3取消通知 |
| application/audit_service.py | 成功事件與查詢 | Booking／Payment／Change／Refund | Store.audit_log | AUDIT-001–002 | test_records.py、test_changes.py | architecture.md | B3建立／補償事件 |
| infrastructure/store.py、seed_data.py、clock.py | 可重置8Trip／3Member／Ledger與固定日期 | Services／Tests | Domain／RLock | 固定資料、資格與容量 | test_seed.py、test_seats.py、test_advance.py | ADR001、README | 保持In-Memory |
| infrastructure/payment_gateway.py | 可控成功／失敗的Mock | Payment／Tests | PaymentStatus | PAYMENT-002、ORDER-001 | test_features.py、unit/test_services.py | architecture.md | B3注入失敗沿用 |
| domain/repositories.py | 原G1最小結構Repository邊界 | 原讀取Services | Domain型別 | 輕量分層 | unit/test_services.py | architecture.md | 新增Service仍可沿用具體Store；不新增DB |

## 調查與核對

先讀公開契約與失敗pytest node ID，追API→Application→Policy→Store；不要只找常數。核對Booking、Order付款快照與改票差額是不同時點。對文件結論以Code／Test驗證，三債兩落差清單在主持文件，不以全面重構為學員必做。

完成條件：每主要模組具有責任、上下游、Rule／Test／Doc與預計演化範圍；評估只依證據，不要求學員猜到內部地圖。
