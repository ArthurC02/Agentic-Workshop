# ADR 007：團體 Booking 是部分取消的一致性邊界


## Context

需求卡 03 讓已付款團體只取消部分旅客：依出發前天數收 10%／20%／30% 手續費、只釋放被取消旅客的座位、剩餘人數須 ≥ 5 或 0、同一筆訂票可多次取消，且任何時刻 `Σ 退款 + Σ 手續費 + Σ 有效旅客票價 = Order.amount`。

現況的力量：
- 「這筆訂票現在有哪些人、各自多少錢、坐哪裡」散在四處：Booking 的 `passengers`／`applied_discounts`／`seat_ids`／`assigned_seats`，Inventory 的 `store.seat_assignments`、`Trip.available_seats`（另有 `store.seat_capacity`）。`SeatService.release` 只會整筆釋放。
- `store.refunds` 以 booking_id 為鍵，一筆訂票只能一筆退款；整筆退票的 Service 自己改 Booking 的狀態與座位欄位。
- 所有 Use Case 在同一把全域 `store.lock` 內；沒有 Domain Event（ADR 003）。
- 有點數折抵的團體被卡片排除（ADR 006 沒有逐位分攤）；團體不能改票，所以未折抵團體的 Order.amount 恆等於 `total_fare`。

## Decision

Status：Accepted。

1. **團體 Booking 是 Aggregate Root，擁有旅客的取消狀態與恆等式**。`Booking.cancelled_passenger_ids` 記錄誰已取消；`Booking.cancel_passengers(passenger_ids, days_before_departure)` 是旅客離開已付款團體的唯一入口。它先完成所有拒絕（PCR-001 類型與點數 → 狀態 → 清單格式 → PCR-003 → PCR-002 → PCR-005），之後才改狀態、刪掉自己的座位副本、必要時轉 `REFUNDED`，回傳 `PassengerCancellation(passenger_ids, fee, refund)`。
   - 恆等式不是事後檢查，而是結構保證：每位被取消旅客的票價在同一行拆成手續費與退款（`refund = Σ票價 − fee`），`total_fare` 與 `applied_discounts` 永不改變，每位旅客只能被取消一次。三者都只在這個方法裡。
   - 整筆退票改走 `Booking.refund_in_full()`：同一個 Aggregate 守住 PCR-012（部分取消過就不可整筆退），並把全部旅客記為已取消，讓整筆退票後恆等式也成立（退款＝Order.amount、手續費 0、有效票價 0）。
2. **手續費規則屬於 Booking 的取消條款，不屬於 Pricing 或 Refund**。Pricing 在售票時定下每位旅客的票價（`applied_discounts`）就結束了；Refund 只記錄結果。費率帶 `CANCELLATION_FEE_BANDS` 與 `cancellation_fee` 在 `domain/cancellation.py`；團體人數下限 `MIN_GROUP_SIZE`（與 `MAX_GROUP_SIZE`）在 `domain/models.py`，團體建立與部分取消共用。D 由 Application 以「班次出發日（+08:00 的日期）− Clock 今天」算好傳入，Aggregate 不讀時鐘。
3. **座位：只做按旅客釋放，不合併四份座位資料**。`SeatService.release_passengers(booking_id, trip_id, passenger_ids)` 在 Inventory 一側把 `store.seat_assignments` 與 `Trip.available_seats` 一起改；Booking 一側由 Aggregate 改自己的 `seat_ids`／`assigned_seats`。兩側在同一個 Use Case、同一把鎖、Aggregate 決定之後才動，所以不會出現部分釋放。合併成單一真相（TripInventory Aggregate）是另一個重構，會牽動既有建立、付款、改票與大量直接戳 store 的測試，不在本卡範圍。
4. **退款紀錄改為 append-only 清單**。`store.refunds: list[RefundRecord]`，一筆紀錄含 refund_id、booking_id、passenger_ids、fee、amount、created_at；整筆退票也是一筆（fee 0、passenger_ids 為全部旅客）。原本「一筆訂票只能退一次」改由 Booking 狀態（`REFUNDED`）與 `refund_in_full` 守住，不再靠 dict 的鍵。
5. **一致性靠既有全域鎖**。「剩幾人」的檢查與「標記取消」在同一把鎖內；不引入版本號或樂觀鎖。
6. **同步直接呼叫，不引入事件**；Audit／通知 `PASSENGERS_CANCELLED` 與既有寫法相同（ADR 003）。不呼叫付款閘道（PCR-014）。

被否決的方案：
- **在 Service 裡算錢、改欄位**（最直接的 transaction script）：恆等式、狀態轉換、座位副本分散在 Service 的多行之間，整筆退票與部分取消各寫一份；任何一條路徑漏改就破壞 PCR-008，而且沒有一個地方能指著說「這裡保證它」。
- **把 `total_fare` 減掉被取消旅客的票價**：看似讓「總額＝有效票價」，但 Order.amount 不變，恆等式與發票、整筆退票的金額基準全部錯開。
- **整筆 `SeatService.release` 再重新 reserve 剩下的人**：兩步之間失敗就遺失座位，也可能把剩下的人重新配到別的座位（違反 PCR-006）。
- **新的 Refund Aggregate／Cancellation 事件／Saga**：沒有任何 AC 需要非同步或跨程序；本期退款只寫本機紀錄。

## Consequences

- `grep -n "CANCELLATION_FEE_BANDS\|MIN_GROUP_SIZE" src` 找到唯一的家；團體建立的 5–20 人檢查改用同一組常數。
- Booking 回應多 `cancelled_passenger_ids`；`passengers`、`applied_discounts`、`total_fare` 保持原付款內容，`seat_ids`／`assigned_seats` 只剩有效旅客。整筆退票後 `cancelled_passenger_ids` 為全部旅客（一般訂票亦同）。退款回應多 `passenger_ids`、`fee`、`created_at`。
- 座位仍有四份資料，只是這次新增的寫入點在同一個 Use Case 內一起改；未來改為多程序或真實閘道退款時，需要把 Inventory 收斂成一個 Aggregate，或以事件／補償處理「座位已釋放但閘道退款失敗」（需求卡待決問題 6）。
- 團體旅客 passenger_id 在建立時沒有驗證唯一；若同一團體出現重複 id（例如 6 人中兩位都叫 P0），取消 `P0` 會一次取消兩人、釋放兩個座位、退兩份錢（金額恆等式仍成立），但人數下限以 1 人計算，結果剩 4 人仍 `PAID`，退款紀錄也只寫一個 id。本期假設 id 在訂票內唯一（見參考解答說明缺陷）。
- 剩 1–4 人直接拒絕；若未來改成「降級為一般訂票」，改的是 `cancel_passengers` 的這一條規則與 `booking_type`，不影響金額恆等式。
