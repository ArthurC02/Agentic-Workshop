# Architecture

API／Schemas 處理 HTTP Contract，Application 協調 Use Case，Domain 提供模型、Fare／Discount 規則，Infrastructure 提供 In-Memory Store、Seed、固定 Clock 與模擬付款閘道。Domain 不依賴 FastAPI。`TicketRepositories` Protocol 描述 Trip、Booking、Order 的存取邊界。共享 RLock 保護單程序狀態更新，旅客輸入會複製，避免外部修改污染 Booking。

核心流程：Trip Query 過濾可售班次；Booking 驗證 1–4 人、容量及可選 member，逐位計價並配置唯一座位；Payment 成功更新 PAID 並建立唯一 Order；Order 保存付款當時金額。一般付款失敗仍 pending、保留座位，不建立 Order。

Change 僅處理已付款 Booking，檢查目標容量後釋放原座位、保留新座位，更新班次與票價，記錄 new-old Fare Difference，不執行補款／退款；Order 仍是原付款快照。Refund（整筆）由 Booking 判斷可否退，更新 REFUNDED、釋放座位並新增一筆 Refund Record。Notification 同步建立本機事件紀錄，Audit 記錄建立及成功付款／改退票事件。

## 電子發票（Invoicing）

Invoicing 是獨立 Context：`domain/invoicing.py` 持有 Invoice（以 order_id 識別，狀態 PENDING／ISSUED／FAILED）、購票人發票資訊、稅額拆分與重試上限，並宣告 Port `InvoiceIssuer`。`application/invoicing_service.py` 把 Order／Booking／Trip 翻譯成 `InvoiceRequest`，並提供查詢與重試。服務商的欄位名稱、回應代碼、3 秒逾時與連線例外只出現在 `infrastructure/einvoice_provider.py` 的 Adapter；目前的 transport 是不連網的 `SimulatedEInvoiceProvider`，組裝在 `api/dependencies.py`。

付款在鎖內建立 Order 與 PENDING Invoice，釋放鎖後才呼叫服務商；發票任何失敗只改 Invoice 狀態，不回滾付款。重試以相同 order_id 進行，ISSUED／FAILED 不再呼叫服務商。決策見 [ADR 005](adr/005-issue-e-invoices-through-a-port.md)。

八班固定 Seed、可注入 Clock 與可控制 Gateway 便於重現測試；In-Memory 不提供持久化或跨程序交易保證。歷史決策見 [ADR](adr/)。

## 會員點數折抵（Membership）

Membership 擁有點數：餘額、折抵規則（最低 100、100 的倍數、上限 30%、1 點 = 1 元）與「餘額不得為負」都在 `domain/members.py`（`Member.reserve_points`／`restore_points` 是唯一改餘額的地方）。Pricing（Discount Policy）完全不知道點數，只交出優惠後總額。`application/member_service.py` 的 `reserve_points(booking)`／`restore_points(booking)` 是兩個入口：一般與團體建立在全域鎖內、規劃座位之後、寫入 Booking 之前各呼叫一次 `reserve_points`；團體付款失敗與退票呼叫 `restore_points`。Booking 只記錄 `redeemed_points`，`payable_amount` 由 `total_fare` 推導；付款扣款與 Order.amount 用 `payable_amount`，退款用 Order.amount。改票路徑不碰點數。決策見 [ADR 006](adr/006-membership-owns-points-redemption.md)。

## 團體部分取消（Booking Aggregate）

團體 Booking 是部分取消的一致性邊界：它擁有旅客、哪些旅客已取消（`cancelled_passenger_ids`）、自己的座位副本與狀態。`Booking.cancel_passengers(ids, D)` 是旅客離開已付款團體的唯一入口，先做完所有拒絕（類型、點數、狀態、清單、D、旅客、人數下限）才改任何東西，回傳這次的手續費與退款；`refund_in_full()` 是整筆退票的入口，守住「部分取消過就不能整筆退」。因為每位被取消旅客的票價恰好拆成手續費＋退款、`total_fare` 永不改變，PCR-008 的恆等式由這一個方法保證，不需要事後對帳。費率與天數門檻在 `domain/cancellation.py`，人數下限 `MIN_GROUP_SIZE` 在 `domain/models.py`（團體建立也用它）。

`RefundService.cancel_passengers` 在全域鎖內：算 D → 交給 Booking 決定 → `SeatService.release_passengers` 只釋放這些旅客的座位（`store.seat_assignments` 與 `Trip.available_seats` 一起動）→ 在 `store.refunds`（append-only 清單，一筆 Booking 可多筆）加一筆退款紀錄 → Audit 與通知。座位資料仍有四份（Booking 的 `seat_ids`／`assigned_seats`、`store.seat_assignments`、`Trip.available_seats`；`seat_capacity` 不動），本次沒有合併，只保證這四份在同一把鎖、同一個 Use Case 內一起改。決策見 [ADR 007](adr/007-group-booking-owns-passenger-cancellation.md)。

## 計價

Discount Policy 收集各 Passenger 符合的候選，加入 ADULT 全額預設，再選 rate 最低的單一優惠；結果包含 Type／Rate／Amount。Booking 建立、團體建立與改票都使用此政策，個別金額加總並回傳根層 Applied Discounts；Schemas 保留原 Passenger 三欄。規則見 [優惠政策](requirements/discount-overview.md)。

## 團體訂票與座位

Group API 與 Service 沿用 Store、Clock、優惠政策及個別旅客合約。座位幾何提供 carriage／row／seat／position，尋找同車廂連續可用區段；以既有固定容量為上限，不以幾何布局虛增庫存。

建立前先驗證完整人數、班次、容量及區段，成功時一次保留／建立；任何不成立都不留下 Booking／Order／座位。團體付款失敗以補償取消 Booking、全釋放、無 Order，並記錄 Audit 與通知；共用付款入口也依 Booking Type 處理，避免繞過團體補償。一般付款語意不變，未建立通用 Transaction Engine。
