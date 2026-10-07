# ADR 006：點數折抵由 Membership 擁有，Pricing 不知道點數


## Context

需求卡 02 讓會員在訂票時用點數折抵票款：1 點 = 1 元、單筆至少 100 點且為 100 的倍數、不得超過優惠後總額 30%（向下取整）；建立時預留，團體付款失敗與退票歸還，一般付款失敗不歸還，改票不動點數。點數餘額已在 `Member.points_balance`（MEMBER-004），但沒有任何行為。

現況的力量：
- 計價有三條複製的路徑（一般建立、團體建立、改票），各自呼叫 `DiscountPolicy`。PTS-006 明說折抵「不是優惠」，不參與單一優惠比較。
- 所有 Use Case 在同一把全域 `store.lock`（RLock）內執行；沒有 Domain Event，事件是同步的字串紀錄（ADR 003）。
- 付款扣款與 Order.amount 都取 `booking.total_fare`；電子發票取 Order.amount（ADR 005）。

## Decision

Status：Accepted。

1. **Membership 擁有點數與折抵規則**。餘額、「不得為負」、最低點數、折抵單位、30% 上限、換算率都在 `domain/members.py`，各有一個名字（`MIN_REDEMPTION_POINTS`、`REDEMPTION_UNIT_POINTS`、`MAX_REDEMPTION_PERCENT`、`POINT_VALUE_TWD`），只有一個家。`Member.reserve_points(points, total_fare)` 是餘額唯一會減少的地方，`restore_points` 是唯一會增加的地方。
   - 上限 30% 雖然以「優惠後總額」為輸入，但它是會員權益的使用條款，不是票價規則：Pricing 不需要知道點數存在，只要交出總額。放進 Pricing 會讓 `DiscountPolicy` 或第四份計價程式碼承擔一個它不擁有的餘額。
   - 不另立 Loyalty Context：本期只有「使用」，沒有累積、到期、等級；一個新 Context 只會多一層轉手。累積規則出現時再評估拆分。
2. **預留＝直接扣餘額，失敗時加回**，不建立獨立的 Reservation 紀錄。預留了多少點記在 `Booking.redeemed_points`（Booking 記錄「這筆訂票用了多少點」這個事實），歸還時依此加回；Audit `POINTS_RESERVED`／`POINTS_RESTORED`（detail `points=N`）提供可追溯性。
3. **單一入口，兩個時機**：`MemberService.reserve_points(booking)` 在一般與團體建立中各被呼叫一次，位置在「所有既有檢查與座位規劃之後、寫入 Booking 與座位之前」，因此任何折抵失敗都不會留下 Booking、座位或扣點（PTS-008）。改票路徑不呼叫它（PTS-013），三條計價迴圈都沒有被修改。`MemberService.restore_points(booking)` 在團體付款失敗與退票時呼叫。
4. **應付金額由 Booking 推導**：`Booking.payable_amount = total_fare − 點數價值`。`total_fare` 與 `applied_discounts` 保持「優惠後總額」語意不變（PTS-006）。付款扣款與 Order.amount 改用 `payable_amount`（PTS-009）；發票因取 Order.amount 而自動正確。
5. **退款取 Order.amount**（PTS-012），不取 `total_fare` 或 `payable_amount`：改票後兩者都可能與實付不同。這也修正了「未折抵、已改票的訂票退的是新票價」的舊行為。
6. **同步直接呼叫，不引入事件**：Booking／Payment／Refund 直接呼叫 `MemberService`，與 ADR 003 一致。並發由既有全域鎖保證：檢查餘額與扣除在同一把鎖內（PTS-014）。

## Consequences

- 點數規則可以用 `grep -n "MAX_REDEMPTION_PERCENT\|MIN_REDEMPTION_POINTS" src` 找到唯一一處；Discount Policy 與三條計價迴圈沒有任何點數程式碼。
- Audit 中 `POINTS_RESERVED` 會排在 `BOOKING_CREATED` 之前（預留是最後一道會拒絕的檢查，必須在寫入之前）。
- 一般訂票付款失敗後一直停在 `PENDING_PAYMENT`，點數也一直被預留（需求卡待決問題 6）；本期不做逾時釋放。
- 改票後 `payable_amount` 依新 `total_fare` 重新推導（例如 750 − 200 = 550），但 Order.amount 仍是 500，改票不補不退。這是顯示值，不產生金流。
- 沒有逐位旅客的點數分攤。需求卡 03（部分取消）若需要按旅客退點，再決定分攤規則與餘數歸屬；`redeemed_points` 記在 Booking 層級，屆時需要新增分攤，而不是修改本 ADR 的規則。
- 若改為多程序部署，全域鎖不再成立；需要以 Member 為單位的條件更新（例如 `balance >= points` 的原子扣除）或樂觀版本。
