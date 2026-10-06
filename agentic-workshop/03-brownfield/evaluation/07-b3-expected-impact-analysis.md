# B3 影響分析與驗證範圍

> 讀者：Evaluation、Facilitator、Agent Production。時機：B3 設計／交付驗收。
> 前置：正式B2已驗收、[B3指令 §17–26](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。可見性：Evaluation內部，不放Participant Package。

B3 從凍結B2延續：一般Booking維持1–4人及原付款失敗pending／保留座位；新Group Booking為5–20人、同Trip同車廂完整連續區段、無部分成立。B2逐人最有利單一優惠保留，群組不新增折扣率。

| 模組／契約 | 最終影響與核對 |
|---|---|
| application/group_booking_service.py::GroupBookingService.create | 在共同RLock內驗證Trip／5–20／容量／Member，先計價及完整plan，再一次寫Booking＋全座位保留，留下GROUP_BOOKING_CREATED |
| application/seat_service.py::SeatService.plan_group／assignment | 依capacity掃完整空位窗口，carriage每20position；不跨車廂但可跨row。第二車廂可選，42容量的第三車廂截斷保留；不更改正式Seed容量 |
| domain/models.py、records.py／schemas/contracts.py | GROUP type、Assigned Seats含seat_id/carriage_id/row_number/seat_number/position；根applied_discounts沿B2逐人rate/type/amount |
| application/payment_service.py::pay／pay_group | Group成功PAID／單一Order；失敗CANCELLED、全release、清Assigned Seats、無Order，記GROUP_PAYMENT_FAILED與GROUP_BOOKING_CANCELLED通知。一般pay路由依type同樣補償，group/pay拒ordinary |
| Change／Refund | Group改票暫不支援且409；已付Group沿退款全釋放，普通改票退款不變 |
| Store／Reset／Gateway | 原固定Clock與8Trip容量不變；reset清所有交易／座位／Audit／Notify，恢復Clock／gateway及capacity |
| API | 新POST /group-bookings、/group-bookings/{booking_id}/pay；原HTTP錯誤與一般API兼容 |
| 文件 | 原40Rule＋新17＝57Rule；API範例、團體連續定義／補償、架構、版本／來源同步 |

## 測試與實際證據

原B2全部55測試檔案字節保留；只新增integration/conftest.py、test_group_creation.py、test_group_payment.py。新Fixture無autouse，不改變原Fixture及55測試。新增20有效案例包含第一車廂已滿仍搜索C002；主代理2026-10-05獨立Python3.13.15正式完整實測 `75 passed, 1 warning in 0.58s`，零failed／skip／xfail。

主代理已取得依賴安裝／Import、TestClient Health、OpenAPI13paths、uvicorn HTTP Health，以及API混合5人（2905）、連續5席、成功Order／退款、失敗409+CANCELLED+全release+無Order、Audit／Notify與Reset證據。完整正式結果以[驗證報告](18-b3-validation-report.md)及[JSON證據](19-b3-validation-evidence.json)為準；來源／歷史／Diff見[案例證據](20-b3-case-history-and-delta.md)。既有相容性Warning須在報告列明。

新增測試獨立核對混合群組2835：3成人提前85%（各595）＋2學生75%（各525），每人明細精確一致。與主代理API Smoke使用不同旅客組成的2905不混淆。

原子性測試包括4／21人、18席不足20人、missingTrip／Member、碎片、跨車廂窗口拒絕，均比較Booking／Order／Seat／Refund／Audit／Notify及全部Trip容量的完整snapshot；成功跨row與C002搜尋則核對精確位置。Group成功／失敗／重複付款／取消後重試、一般路由防繞過、退款與Reset亦有獨立案例。

完成條件：[19 AC／57 Rule映射](10-b3-acceptance-test-map.md)與真實Code／Test／文件吻合，正式75完整通過且原55字節保留，全部補償／連續／逐人票價／Audit／Notify具證據，版本及交付隔離完成，不將Evaluation答案發給Participant。
