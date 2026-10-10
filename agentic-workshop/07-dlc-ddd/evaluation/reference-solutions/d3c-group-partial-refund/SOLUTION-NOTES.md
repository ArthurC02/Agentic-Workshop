# D3c 團體部分取消退款：主持人參考解答說明

本目錄是 DDD DLC 情境 D3c（需求卡 03：團體訂票部分取消退款）的參考解答，也是 D4 交接的 Recovery 起點。起點為 D3b 參考解答（`../d3b-points-redemption`，電子發票與點數折抵已上線），只加入部分取消；刻意保留的邊界洩漏（付款閘道無 Port、Service 依賴具體 Store、字串事件名、三份複製的計價迴圈、團體付款失敗的補償仍由 `PaymentService` 直接改 Booking 欄位、座位庫存多份資料）原樣不動。

## 驗證方式

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 -m pytest -q          # 179 passed（D3b 的 156 + 新 23）
.\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\integration\test_partial_cancellation.py   # 23 passed
# 反事實檢查（需 domain-memory 外掛），結果寫入 evidence\counterfactual\*.json
py -3.13 -X utf8 evidence\run_counterfactuals.py .venv\Scripts\python.exe <SkillHub>\.claude\skills\domain-memory\scripts\registry_tools.py
```

D3b 原有的 156 個測試一個都沒改，全部通過（含 `test_refunds.py` 的「只能退一次」與 `len(memory_store.refunds) == 1`：`refunds` 改成清單後語意相同）。

## 1. 設計摘要

| 檔案 | 角色 | 變更 |
|---|---|---|
| `src/smart_ticket/domain/models.py` | Booking Aggregate：`MIN_GROUP_SIZE`／`MAX_GROUP_SIZE`、`cancelled_passenger_ids` 欄位、`active_passenger_ids`、`cancel_passengers(ids, D)`（PCR-001～005、008、009，旅客離開團體的唯一入口）、`refund_in_full()`（整筆退票的入口，守 PCR-012） | +52 |
| `domain/cancellation.py`（新） | 取消條款：`CANCELLATION_FEE_BANDS`（14/10、7/20、1/30）、`cancellation_fee_percent(D)`（含 `REFUND_WINDOW_CLOSED`）、`cancellation_fee`（逐位向下取整）、值物件 `PassengerCancellation` | +27 |
| `application/refund_service.py` | `cancel_passengers`：鎖內算 D → Booking 決定 → 只釋放這些人的座位 → 新增退款紀錄 → Audit／通知；`refund` 改由 `booking.refund_in_full()` 判斷與改狀態；`list_for` | +26／−8 |
| `application/seat_service.py` | `release_passengers(booking_id, trip_id, ids)`：`store.seat_assignments` 與 `Trip.available_seats` 一起改 | +8 |
| `domain/records.py`、`infrastructure/store.py` | `RefundRecord` 多 `passenger_ids`、`fee`、`created_at`；`store.refunds` 改成 append-only 清單 | +4／+1−1 |
| `application/group_booking_service.py` | 5–20 人檢查改用 `MIN_GROUP_SIZE`／`MAX_GROUP_SIZE`（商業數字只有一個家） | +5／−3 |
| `schemas/contracts.py`、`api/routes.py` | `POST /group-bookings/{id}/cancel-passengers`、`GET /bookings/{id}/refunds`；Booking 回應多 `cancelled_passenger_ids`；退款回應多三欄 | +7／+10−1 |
| `tests/integration/test_partial_cancellation.py` | 每個 AC 至少一個 `test_pcr_0xx_*`，共 18 個函式／23 個案例 | 275 |
| `docs/adr/007-group-booking-owns-passenger-cancellation.md`、`docs/requirements/business-rules.md`（新增 PCR 規則表；REFUND-004、GROUP-001 加註）、`change-booking-guide.md`、`docs/architecture.md`、`docs/api-examples.md`、`README.md`、`docs/version-history.md`、`pyproject.toml`／`main.py`（1.7.0） | 團隊文件與版本 | |

正式程式約 +141／−14 行。**三條計價迴圈、`DiscountPolicy`、`PaymentService`、`MemberService` 一行都沒改**；`total_fare`、`applied_discounts`、Order.amount 永遠不因取消而改變。

流程（`RefundService.cancel_passengers`，全部在全域鎖內）：

1. 取 Booking（404）；以「班次出發日（+08:00 的日期）− Clock 今天」算 D。
2. `booking.cancel_passengers(ids, D)`：類型／點數 → 狀態 → 清單格式（空或重複 422）→ D（`REFUND_WINDOW_CLOSED`）→ 逐位「已取消／不屬於此訂票」→ 剩餘人數 ≥ 5 或 0。**全部通過之後**才逐位算手續費、記為已取消、刪掉自己的座位副本、沒人了就轉 `REFUNDED`，回傳 `PassengerCancellation(ids, fee, refund)`。
3. `SeatService.release_passengers`：只拿掉這些旅客的 `SeatAssignment`，`Trip.available_seats` 加回相同數量；其他人不動、不重新配位。
4. `store.refunds.append(RefundRecord(...))`；Audit `PASSENGERS_CANCELLED`（`passenger_ids=P0,P1 refund=980 fee=420`）與通知。不呼叫付款閘道。

整筆退票（`RefundService.refund`）改成先呼叫 `booking.refund_in_full()`：部分取消過就 409；否則把全部旅客記為已取消、`REFUNDED`、清座位副本，退款紀錄 fee 0、passenger_ids 為全部旅客。這讓 PCR-008 在「整筆退票之後」也成立（3,500 + 0 + 0 = 3,500），且整筆與部分兩條路徑的「誰被取消」只由 Booking 決定。

`grep -rn "CANCELLATION_FEE_BANDS\|MIN_GROUP_SIZE" src` 只命中 `domain/cancellation.py`、`domain/models.py` 與使用它們的 `group_booking_service.py`，可當作「商業數字只有一個家」的證據。

## 2. Context 劃分與理由

| Context | 本次持有 | 理由 |
|---|---|---|
| **Booking（Aggregate Root：團體 Booking）** | 誰已取消（`cancelled_passenger_ids`）、取消的所有前提、人數下限、手續費計算、狀態轉換、自己的座位副本、整筆退票的守門 | PCR-005／008／009／011／012 全部是「這一筆訂票現在的組成」的規則；要讓恆等式在一個地方成立，旅客狀態、票價與金額拆分必須在同一個方法裡一起決定。 |
| Booking 的取消條款（`domain/cancellation.py`） | 費率帶、D ≤ 0 不受理、逐位向下取整 | 這是「退訂條款」，不是售價：Pricing 在售票時定下每位旅客的票價就結束了。放在 Booking 旁的獨立模組，是為了讓商業數字可被 grep 到唯一出處。 |
| Pricing（Discount Policy） | 不變 | 手續費的基準是已存在的 `applied_discounts[*].amount`，不重新計價。 |
| Inventory（Seat） | `release_passengers`：`seat_assignments` 與 `Trip.available_seats` 一起動 | 庫存仍是 Inventory 的；Booking 只決定「誰的座位要還」。 |
| Refund | 退款紀錄清單（append-only），每次一筆 | Refund 是紀錄者，不是決策者：金額由 Booking 給，Refund 不重算。 |
| Payment／Order | 不變；Order.amount 是恆等式右邊 | 部分取消不動 Order、不呼叫閘道（PCR-014）。 |
| Membership | 不變 | 有點數的團體直接 409，不做點數分攤（D3b 第 8 節）。 |
| Audit／Notification（Generic） | `PASSENGERS_CANCELLED` | 沿用 ADR 003 同步紀錄。 |

需求卡待決問題的參考答案：

1. **一致性邊界畫在哪**：團體 Booking。它擁有「哪些旅客有效」與「每位旅客的票價」，所以恆等式 `Σ退款 + Σ手續費 + Σ有效票價 = Order.amount` 能在 `cancel_passengers` 內以結構保證（每位被取消旅客的票價恰好拆成 fee + refund、`total_fare` 不變、每位只能取消一次）。「座位數 = 有效旅客數」跨 Booking 與 Inventory 兩邊：Booking 決定，Inventory 在同一把鎖、同一個 Use Case 內跟著改；**不**把 Inventory 收進 Booking（TripInventory 是另一個 Aggregate，合併它是另一個重構）。
2. **手續費歸誰**：Booking 的取消條款（ADR 007 第 2 點）。不是 Pricing（不重新計價），也不是 Refund（Refund 只記錄）。
3. **退款紀錄**：`store.refunds` 改成 append-only 清單、紀錄多 `passenger_ids`／`fee`／`created_at`。「只能退一次」改由 Booking 守（`REFUNDED` 狀態＋`refund_in_full` 的檢查），既有測試不需要改。
4. **低於 5 人**：本期直接拒絕；不為「降級為一般訂票」預留任何程式（YAGNI）。將來要改，只改 `cancel_passengers` 的一條規則，金額恆等式不受影響。
5. **整筆退票全額 vs 部分取消收手續費**：不統一（卡片「不在本期範圍」）；以 PCR-012 讓兩者互斥，避免「先部分取消，再整筆退全額」的重複退款。列為 Unknown。
6. **閘道退款失敗而座位已釋放**：本期不呼叫閘道，不發生。將來接閘道時，座位釋放與退款不再能在一把本機鎖內完成，需要「退款中」狀態或補償（ADR 007 Consequences）。

## 3. Implementation handoff

**Domain facts**
- 團體 Booking 擁有旅客與其取消狀態；旅客票價＝`applied_discounts[*].amount`，`total_fare`＝其加總，未折抵團體的 Order.amount＝`total_fare`（團體不能改票、有點數者被排除）。
- D＝班次出發日（台灣日期）− Clock 今天；D ≥ 14 → 10%、7–13 → 20%、1–6 → 30%、≤ 0 不受理。
- 手續費逐位：⌊票價 × 費率 ÷ 100⌋；退款＝票價 − 手續費。
- 取消後有效旅客 ≥ 5 或 0；最後一位取消後 `REFUNDED`。
- 每次部分取消一筆退款紀錄；部分取消過不可整筆退票。

**Forces**
- 座位資料四份（Booking 的 `seat_ids`、`assigned_seats`；Inventory 的 `store.seat_assignments`、`Trip.available_seats`；`seat_capacity` 不動）；`SeatService.release` 只會整筆釋放（as-is 觀察 ASIS-001）。
- `store.refunds` 以 booking_id 為鍵，一筆訂票一筆紀錄（ASIS-004）。
- 全域 `store.lock`：「剩幾人」與「標記取消」必須在同一把鎖內（check-then-act）。
- PCR-011：任何拒絕都不得留下變更 → 所有拒絕必須在第一個寫入之前。
- 整筆退票路徑已存在且有測試；部分取消後它會變成重複退款的漏洞。
- 既有測試 `test_best_discount_api.py` 斷言 `booking["passengers"] == body["passengers"]`：不能在 `passengers` 上加狀態欄位。

**Decision**
- Booking Aggregate 加兩個方法（`cancel_passengers`、`refund_in_full`）與一個欄位（`cancelled_passenger_ids`）；一個取消條款模組；`SeatService` 加一個按旅客釋放；退款紀錄改清單。沒有新的 Repository、Event、Saga、Refund Aggregate。
- 被否決的較簡單方案 A：全部寫在 `RefundService`（transaction script）。可以通過大部分 AC，但恆等式、狀態轉換與座位副本會在整筆與部分兩條路徑各寫一份，沒有任何一個地方能保證 PCR-008；整筆退票的 PCR-012 守門也容易漏。
- 被否決的較簡單方案 B：把被取消旅客的票價從 `total_fare` 扣掉。Order.amount 不變，恆等式左右兩邊從此對不上，發票與整筆退票的基準也會錯。
- 被否決的方案 C：整筆 `release` 後重新 `reserve` 剩下的人。兩步之間失敗會遺失座位，且可能重新配位（違反 PCR-006）。
- 被否決的方案 D：在 `Passenger` 上加 `status`。改變了 `passengers` 的公開合約（既有測試會失敗），且 `Passenger` 同時是請求的值，客戶端可能把狀態送進來。取消是「這筆訂票對這位旅客的事實」，屬於 Booking。

**External systems**：無（PCR-014：不呼叫付款閘道）。

**Unknowns（本解答的假設）**
- API 路徑、請求與回應欄位（缺陷 D1）：採 `POST /group-bookings/{id}/cancel-passengers`、`{"passenger_ids": [...]}`、回傳退款紀錄；`cancelled_passenger_ids`；`GET /bookings/{id}/refunds`。
- 多個違規同時成立的回報順序（缺陷 D2）：類型／點數 → 狀態 → 清單格式 → D → 逐位旅客 → 人數下限。
- 422 的錯誤碼（缺陷 D8）：`INVALID_PASSENGER_IDS`，由 Domain 拋出（不是 Pydantic），因為重複 id 會讓手續費重算兩次，屬於恆等式的保護。
- Audit detail 格式（缺陷 D7）：`passenger_ids=P0,P1 refund=980 fee=420`。
- 整筆退票把全部旅客記為已取消、退款紀錄 fee 0（缺陷 D3、D11）。一般訂票整筆退票後 `cancelled_passenger_ids` 也是全部旅客。
- passenger_id 在同一訂票內唯一（缺陷 D9）：建立時沒有檢查；重複時人數下限會少算。
- 多程序部署、閘道退款、發票折讓：不處理。

**Proof obligations → 測試**

| 義務 | 測試 |
|---|---|
| 一般訂票、有點數團體 409 `PARTIAL_CANCEL_NOT_SUPPORTED`；PENDING／CANCELLED／REFUNDED 409 `BOOKING_NOT_REFUNDABLE`；不存在 404；皆無變更 | `test_pcr_001_*`（兩個） |
| 單位／多位以 id 指定；未知 id、他團的 id 404；已取消 409；空清單、重複、缺欄位 422；皆無變更 | `test_pcr_002_*` |
| D ＝ 0、−1 → 409 `REFUND_WINDOW_CLOSED`，無變更 | `test_pcr_003_*`（2 案例） |
| 卡片試算 59／536、119／476、178／417 與邊界 D＝13、6；成人 210、學生 157；兩位學生 314／736（不是 315）；不以平均 | `test_pcr_004_*`（6 案例） |
| 剩 4 人、剩 1 人 409 且無變更；一次取消剩下全部可以；6 個執行緒同時各取消 1 位只成功 1 筆 | `test_pcr_005_*`（兩個） |
| 只釋放 S003、可售 +1、其他人 seat／carriage 不變、Inventory 與 Booking 副本一致、新訂票拿到 S003 | `test_pcr_006_*` |
| 兩次取消兩筆紀錄、第一筆未被覆寫、欄位齊全、`created_at` | `test_pcr_007_*` |
| 卡片範例 4,200：490＋210＋3,500 → 拒絕不變 → 2,940＋1,260＋0；跨費率帶多次取消；整筆退票後 3,500＋0＋0 | `test_pcr_008_*`（兩個） |
| 有人時 `PAID`，最後一位後 `REFUNDED` 且 `seat_ids` 為空 | `test_pcr_009_*` |
| `cancelled_passenger_ids`、`passengers` 仍列出全部、只列出本訂票的退款紀錄 | `test_pcr_010_*` |
| 清單中混有未知、已取消、會低於下限：整個請求無變更 | `test_pcr_011_*` |
| 部分取消過不可整筆退；未取消過的團體整筆退 3,500、fee 0 | `test_pcr_012_*` |
| Audit detail 與通知 | `test_pcr_013_*` |
| 閘道被替換成「一呼叫就失敗」，取消仍成功；Order 仍一筆 | `test_pcr_014_*` |

`test_pcr_005_concurrent_cancellations_cannot_break_the_minimum` 用 monkeypatch 讓 `cancellation_fee` 睡 50 ms，把「檢查剩幾人」與「標記取消」之間的空隙放大；有鎖時結果確定（1 筆成功、5 筆 `GROUP_BELOW_MINIMUM`，連跑 6 次皆通過）；拿掉鎖時 6 筆全部成功，每一筆都以為自己取消後還剩 5 人。

## 4. 反事實檢查（counterfactual）

每條新規則各破壞一次、跑聚焦測試、還原。37／38 killed，`failing_evidence` 皆為斷言失敗（不是 import／語法錯誤），`restoration_result.restored` 皆為 true；1 個存活（D 用 datetime 相減），依 D3 工作規則第 11 條判定為測試不足，不是等價 mutant（見下）。JSON 在 `evidence/counterfactual/`，重跑用 `evidence/run_counterfactuals.py`。

| AC | 規則 | 破壞方式 | 結果 |
|---|---|---|---|
| PCR-001 | 只有團體 | `booking_type != "GROUP" or redeemed_points` → 只看點數 | killed（一般訂票變成 `GROUP_BELOW_MINIMUM`） |
| PCR-001 | 排除有點數團體 | → 只看類型 | killed |
| PCR-001 | 只有 PAID | 狀態檢查 → `if False:` | killed |
| PCR-002 | 空清單 422 | 移除 `not passenger_ids or` | killed（空清單變成 200、退 0 元的紀錄） |
| PCR-002 | 重複 422 | 移除重複檢查 | killed（變成 409 下限，若人數夠則手續費算兩次） |
| PCR-002 | 不屬於此訂票 404 | → `if False:` | killed |
| PCR-002 | 已取消 409 | → `if False:` | killed（變成 404） |
| PCR-003 | D ≤ 0 不受理 | 最後一帶 `(1, 30)` → `(0, 30)` | killed |
| PCR-004 | 14 天門檻 | `(14, 10)` → `(15, 10)` | killed |
| PCR-004 | 7 天門檻 | `(7, 20)` → `(8, 20)` | killed |
| PCR-004 | 費率 10／20／30 | 各 +1 | 3 個皆 killed |
| PCR-004 | 門檻含等號 | `>=` → `>` | killed |
| PCR-004 | 向下取整 | `// 100` → `round(/ 100)` | killed（59.5、157.5） |
| PCR-004 | 逐位取整 | `sum(fee(f))` → `fee(sum(f))` | killed（**只有兩位學生 314 vs 315** 抓到） |
| PCR-004 | 以自己的票價 | 改為 `total_fare // 人數` 平均 | killed（**只有成人＋學生混合團**抓到） |
| PCR-004 | D 的計算 | `.days` → `.days + 1` | killed |
| PCR-004 | D 以日期計 | 改為 `(departure_time − clock.now()).days` | **survived，測試不足**（見下） |
| PCR-005 | 剩 0 人可以 | 移除 `0 <` | killed |
| PCR-005 | 下限 5 | `MIN_GROUP_SIZE = 5` → `4` | killed |
| PCR-005 | 鎖內檢查並標記 | `cancel_passengers` 的 `with self.store.lock:` → `if True:` | killed（並發 6 筆全成功） |
| PCR-006 | 其他人保留座位 | `kept = []`（整筆釋放） | killed |
| PCR-006 | 班次計數器 | `+= len(assignments) − len(kept)` → `+= 0` | killed |
| PCR-006 | 有呼叫釋放 | 移除 `release_passengers` | killed |
| PCR-006 | Booking 副本 | `assigned_seats` 不刪 | killed |
| PCR-007 | 不覆寫 | `append(record)` → `refunds[:] = [record]` | killed |
| PCR-008 | 退款＝票價 − 手續費 | 改為 `Σ票價 × (100 − 費率) // 100`（退款向下取整） | killed（595 → 535 vs 536） |
| PCR-008 | 整筆退票也記為已取消 | `cancelled_passenger_ids = []` | killed（整筆退票後有效票價 3,500，等式變 7,000） |
| PCR-009 | 最後一位後 REFUNDED | `if not active` → `if False:` | killed |
| PCR-009 | 仍有人時 PAID | → `if True:` | killed |
| PCR-010 | 回應顯示已取消 | 欄位 `exclude=True` | killed |
| PCR-010 | 只列本訂票 | `if record.booking_id == booking_id` → `if True` | killed（需要第二個團體才抓得到） |
| PCR-011 | 先決定再釋放 | 把 `release_passengers` 移到 `cancel_passengers` 之前 | killed |
| PCR-012 | 部分取消後不可整筆退 | 移除 `or self.cancelled_passenger_ids` | killed（多退 4,200） |
| PCR-013 | Audit detail | → `""` | killed |
| PCR-013 | 通知 | 移除 | killed |
| PCR-014 | 不呼叫閘道 | 在通知後插入 `gateway.charge(booking_id, -amount)` | killed |

教學提示（值得在 Review 時拿出來討論「測試證明的是什麼」）：

- **D 用日期還是 datetime 的 mutant 存活，是測試不足**（23 個 PCR 測試全過）。現有 FixedClock 的 `now()` 固定 09:00、只能設日期，所有班次 09:00 出發，所以現有測試分辨不出「日期相減」與「時間差取整天」；但測試把 `clock.now` 換成出發時刻之後（例如 09:01）就分辨得出，所以不是等價 mutant（依 D3 工作規則第 11 條）。卡片的定義（台灣日期相減）是對的，缺的是一個調整時刻的測試；改成 UTC 日期計算同理。證據檔名 `days-by-datetime-EQUIVALENT-survived.json` 反映的是先前的判定，為了可追溯而保留原名。
- **卡片範例全是成人團（或單人）**：6 成人 × 700 × 30% = 1,050 剛好整除，平均票價也等於每人票價。所以「在總額上取整一次」與「以 `total_fare` 平均分攤」兩個最常見的錯誤，**只測卡片範例時都會存活**。只有混合團（成人＋學生）與「兩位學生一起取消」（157.5 × 2）能抓到。
- **整筆退票路徑是本卡最容易漏的地方**：沒有任何 AC 直接說「整筆退票要把旅客記為已取消」，但沒有它，PCR-008「任何時刻」在整筆退票後就不成立；沒有 PCR-012 的守門，「先取消 1 位退 490，再整筆退 4,200」會多退錢。
- **`refunds-of-this-booking`** 在只有一個團體有退款時會存活；測試必須讓另一筆訂票也有退款紀錄。

## 5. Agent 常見錯誤（巡堂檢查清單）

1. **改 `total_fare` 或 Order.amount**（扣掉被取消的票價）：恆等式右邊被改掉，PCR-008 永遠「成立」但失去意義；發票、整筆退票基準跟著錯。
2. **手續費以 `total_fare` 平均或在加總後取整一次**：通過全成人的卡片範例，在混合團失敗。
3. **整筆 `SeatService.release` 再重新 reserve 剩下的人**：重新配位（違反 PCR-006）、兩步間失敗遺失座位。
4. **四份座位資料只改一兩份**：只改 `Trip.available_seats`（座位沒真的空出來，新訂票拿不到 S003），或只改 `store.seat_assignments`、忘了 Booking 的 `seat_ids`／`assigned_seats`（或反過來）。
5. **邊驗證邊修改**：在迴圈中逐位標記取消，第三位才發現 404 → 前兩位已被取消（PCR-011）。
6. **`store.refunds[booking_id] = record`** 原樣沿用：第二次取消覆寫第一次（PCR-007）。有趣的是，若保留 `booking_id in self.store.refunds` 的整筆退票檢查，PCR-012 會「意外地」通過。
7. **人數下限寫成 `remaining < 5`**：不能一次取消全部（PCR-005 的「或 0 人」）；或拿「請求人數」而不是「剩餘人數」比。
8. **忘了整筆退票路徑**：部分取消後整筆退票仍可退全額（重複退款）；或整筆退票後旅客仍顯示有效。
9. **只靠 Pydantic 擋重複 id**：路由之外（Service、測試、未來的批次）呼叫時手續費會算兩次；而且回 422 的規則在 schema、409 的規則在 Domain，同一個「清單合法嗎」有兩個家。
10. **在 `Passenger` 上加 `status`**：破壞 `passengers` 的公開合約（`test_best_discount_api` 失敗），並讓請求可以送入狀態。
11. **有點數的團體沒有排除**：恆等式右邊（Order.amount＝應付）與左邊（以 `applied_discounts` 計的票價）不同基準，第一筆取消就對不上。
12. **D 的計算錯一天或用 UTC 現在時刻**：前者被 D＝7／14 範例抓到；後者在 Seed 下看不出來（第 4 節）。
13. **檢查在鎖外**（例如在 route 先查剩幾人）：check-then-act 競態。
14. **呼叫付款閘道退款**（`gateway.charge(-amount)` 或新增 `refund` 方法）：違反 PCR-014，且閘道失敗時座位已釋放。
15. **魔術數字散落**：10／20／30、14／7、5 寫在 Service、錯誤訊息、測試常數各一份；團體建立的 `5 <= len <= 20` 與新規則的 `< 5` 各一份。
16. **過度設計**：Refund Aggregate＋`PassengersCancelled` Domain Event＋Saga＋Repository Protocol；沒有任何 AC 需要非同步，且違反 ADR 003 卻沒寫新 ADR。
17. **順手合併四份座位資料成 TripInventory**：方向正確但不是這張卡的範圍，會牽動建立、付款、改票與大量直接戳 store 的測試。
18. **測試只驗卡片範例**：會讓第 4 節粗體的兩個 mutant 存活，也抓不到整筆退票的重複退款。

## 6. 需求卡檢查結果

**數字與範例全部正確**（出發日 2030-01-15、預設 Clock 2030-01-14 → D＝1 → 30%）：成人 700 → ⌊210⌋、490；學生 525 → ⌊157.5⌋＝157、368；2030-01-01 提前票 595（85%）在 2030-01-08 取消 → D＝7 → 20% → 119、476；在 2030-01-01 取消 → D＝14 → 10% → ⌊59.5⌋＝59、536。範例團體 6 成人 4,200：取消 1 位（D＝1，30%）→ 490＋210，剩 5 人 `PAID`；再取消 1 位會剩 4 人 → 409；一次取消 5 位 → 2,450＋1,050、`REFUNDED`；490＋2,450＋210＋1,050＋0＝4,200。範例中的 D 由卡片「所有 Seed 班次出發日為 2030-01-15」與「預設 Clock」推得，日期是明確的；時刻不影響（D 以台灣日期相減）。T001 有 20 座，6 人團可建立。

**缺陷與建議修正**（依影響排序）：

| # | 問題 | 影響 | 建議修正文字 |
|---|---|---|---|
| D1 | 沒有定義 API：部分取消的路徑、請求格式、成功回應；PCR-010 的「可分辨每位旅客」與「可查到全部退款紀錄」在哪個欄位／端點。 | 各組介面不同，主持人無法用同一份驗收測試；Agent 自己發明。 | 新增「API」小節：「`POST /group-bookings/{booking_id}/cancel-passengers`，body `{"passenger_ids": ["P0", ...]}`，200 回傳這次的退款紀錄 `{refund_id, booking_id, passenger_ids, fee, amount, created_at}`。Booking 回應新增 `cancelled_passenger_ids`；`passengers`、`applied_discounts`、`total_fare` 不變，`seat_ids`／`assigned_seats` 只含有效旅客。`GET /bookings/{booking_id}/refunds` 依時間列出全部退款紀錄（含整筆退票）。」 |
| D2 | 多個違規同時成立時的回報順序未定義（例：一般訂票且未付款；PENDING 團體帶未知 id；D＝0 且會低於 5 人；清單同時有未知與已取消的 id）。 | 測試結果因實作順序而異。 | 加一句：「依序檢查並回報第一個：PCR-001（類型與點數，再狀態）→ 清單格式（422）→ PCR-003 → PCR-002（依清單順序逐位）→ PCR-005。」 |
| D3 | PCR-008「任何時刻」沒有說整筆退票後如何成立：整筆退票的團體若旅客仍算「有效」，等式變成 3,500＋0＋3,500 ≠ 3,500。也沒有限定只適用於團體（一般訂票改票後 `total_fare` ≠ Order.amount）。 | 有人只在部分取消路徑維持恆等式；整筆退票後查詢結果自相矛盾。 | PCR-008 改為：「適用於團體訂票。…整筆退票視為全部旅客取消、手續費 0。」 |
| D4 | 取消後 Booking 回應的欄位沒有規定：`total_fare` 要不要減？`passengers` 要不要移除被取消的人？`seat_ids` 呢？ | 有人改 `total_fare`（破壞恆等式語意），有人從 `passengers` 刪人（查不到誰被取消，違反 PCR-010）。 | PCR-010 加：「`total_fare`、`passengers`、`applied_discounts` 保持原付款內容；`seat_ids`／`assigned_seats` 只列有效旅客。」 |
| D5 | PCR-004「逐位計算」與「不得平均分攤」沒有任何範例能區分：所有範例都是單人或全成人（6 × 700 × 30% 整除、平均票價＝每人票價）。 | 「總額取整一次」與「平均分攤」兩個錯誤只靠卡片範例抓不到（見第 4 節）。 | 試算加兩行：「預設 Clock，成人＋學生混合團取消 1 位學生 → 手續費 157、退款 368（不是以平均票價計）」「同時取消兩位學生 → 手續費 157＋157＝314、退款 736（不是 1,050 × 30%＝315）」。 |
| D6 | 費率邊界缺少範例：沒有 D＝13、D＝6、D＝0 的列，也沒有 `REFUND_WINDOW_CLOSED` 的例子。 | `>=`／`>`、門檻差一天、D＝0 是否受理等錯誤只抓得到一半。 | 試算加：「2030-01-02 取消（D＝13）595 → 119／476」「2030-01-09 取消（D＝6）595 → 178／417」「2030-01-15 取消（D＝0）→ 409 `REFUND_WINDOW_CLOSED`」。 |
| D7 | PCR-013「detail 含 passenger_ids 與退款金額」沒有格式。 | 無法寫一致的驗收斷言。 | 改為：「detail 為 `passenger_ids=<以逗號分隔> refund=<退款合計> fee=<手續費合計>`，例如 `passenger_ids=P0,P1 refund=980 fee=420`。」 |
| D8 | PCR-002 的 422 沒有錯誤碼；專案其他 422（`INVALID_INVOICE_INFO`）都有。重複 id 不只是格式問題：放過它會讓手續費算兩次。 | 有人用 Pydantic（FastAPI 預設 `{"detail": ...}` 格式），有人用 DomainError，回應形狀不一。 | 改為：「清單為空或重複列出同一位旅客回 422 `INVALID_PASSENGER_IDS`。」 |
| D9 | passenger_id 在同一訂票內唯一沒有被要求，團體建立也不檢查。重複時（6 人中兩位都叫 P0）取消 `P0` 會一次取消兩人，人數下限以 1 人計算，結果剩 4 人仍 `PAID`。 | PCR-005 可被繞過；退款紀錄的 passenger_ids 無法對應到人。 | 名詞表「部分取消」加：「passenger_id 在同一筆訂票內唯一。」並在「不在本期範圍」或 GROUP 規則補上建立時的檢查（建立時重複回 422）。 |
| D10 | 「有點數折抵的團體回 409 `PARTIAL_CANCEL_NOT_SUPPORTED`」寫在「不在本期範圍」，實際上是一條要實作、要測的行為。 | 有人當成「不用做」而漏掉；恆等式在有點數的團體不成立。 | 移到 PCR-001：「一般訂票或有點數折抵（`redeemed_points > 0`）的團體回 409 `PARTIAL_CANCEL_NOT_SUPPORTED`。」 |
| D11 | PCR-007 只定義部分取消紀錄的欄位；整筆退票紀錄的 `passenger_ids`／手續費未定義，而 PCR-010 要「全部退款紀錄」一起列出。 | 兩種紀錄形狀不同，查詢端要分支處理。 | PCR-012 加：「整筆退票的退款紀錄 passenger_ids 為全部旅客、手續費 0。」 |
| D12 | 沒有提到同一訂票的並發請求。PCR-011 只保證單一請求原子。 | 兩個各取消 1 位的請求同時送達，6 人團可能剩 4 人。 | PCR-005 加：「同一訂票的部分取消依序處理；人數以處理當下的有效旅客計。」 |

## 7. 30 分鐘可行性與建議切片

參考解答規模：正式程式約 +141／−14 行（比 D3b 大，且是三張卡裡唯一需要改既有資料結構的）、測試約 275 行；14 條 AC 加上 38 個反事實檢查。

| 時段 | 活動 |
|---|---|
| 0–6 分 | 讀卡、回答待決問題 1–3（一致性邊界、手續費歸誰、退款紀錄結構）；主持人先公布 D1 API、D2 錯誤順序、D3 整筆退票的處理 |
| 6–9 分 | 寫 handoff／指示 Agent（facts、forces「四份座位資料」「先拒絕再修改」「不要動 total_fare」、proof obligations 含混合團範例） |
| 9–22 分 | Agent 實作與測試（核心切片） |
| 22–28 分 | Review：恆等式在哪裡被保證、整筆退票路徑、座位四份是否一致；跑 3–4 個 counterfactual |
| 28–30 分 | 緩衝 |

**判定：核心切片在 30 分鐘內勉強可行，前提是主持人先公布 D1～D3；完整 14 條 AC 無法同時完成實作、Review 與反事實檢查。**這是三張卡中最重的一張，建議把延伸 AC 明確標為加分，Review 時間不可壓縮（本卡的教學重點全在 Review）。

- **核心（必做）**：PCR-001、003、004、005、006、007、008、009、011、012。這些構成「Aggregate 一致性邊界」：誰擁有旅客狀態、恆等式在哪裡成立、先拒絕再修改、座位只還被取消的人、退款紀錄可多筆、整筆與部分互斥。卡片範例 4,200 的三步正好覆蓋 004／005／007／008／009。
- **延伸（加分）**：PCR-002 的完整驗證（404／409／422）、PCR-010（查詢欄位與端點，機械性）、PCR-013（Audit／通知，機械性）、PCR-014（現行行為自然滿足，只需測試）、並發測試。
- **反事實檢查只做 4 個**：`fee-on-own-fare` 或 `fee-per-passenger`（PCR-004，全成人測試會存活，示範「先 survived 再補混合團測試」）、`decide-before-release`（PCR-011）、`no-whole-refund-after-partial`（PCR-012，多退 4,200）、`inventory-keeps-others`（PCR-006）。
- 段落結束時發放本目錄作為 Recovery 起點。

## 8. 對 D4 的影響（交接注意事項）

- **已不成立、需要新提案取代的 reviewed 事實**：
  - `REFUND-004`（「退票建立唯一退款紀錄…同一訂票不可再退」）→ 改為「每次退款一筆紀錄；整筆退票只能一次且只限未部分取消過」。
  - Aggregate `booking` 的不變量「已付款訂票只能退一次」與「團體 5–20 人」→ 改為「團體建立時 5–20 人；部分取消後有效旅客 ≥ 5 或 0」「Σ退款＋Σ手續費＋Σ有效票價＝Order.amount」；commands 新增 `cancel_passengers`；狀態轉換「PAID →（部分取消仍 PAID）→ REFUNDED」。
  - `ASIS-004`（退款以 booking_id 為鍵）不再描述現況；`ASIS-001`（座位多份資料、無單一擁有者）仍成立，本次只是讓新寫入點在同一 Use Case 內一起改。
  - ADR-004「已付款團體退票保留」需加註「未部分取消過時」。
- **D3c 新增的候選**（請以 `make_record.py --allow-unclassified --upsert` 登記為 candidate，不可當成限制）：PCR-001～014、取消費率帶與 D 的定義、`MIN_GROUP_SIZE` 由建立與取消共用、ADR 007（Booking 是部分取消的一致性邊界）、事件 `PASSENGERS_CANCELLED`。
- **verify-evidence／verify-sources 會回報 stale 的檔案**：`domain/models.py`、`domain/records.py`、`infrastructure/store.py`、`application/refund_service.py`、`application/seat_service.py`、`application/group_booking_service.py`、`schemas/contracts.py`、`api/routes.py`、`main.py`；新檔 `domain/cancellation.py` 尚未經過來源確認。exit 1 屬預期，留給 D4 以 `upsert-candidate` 更新。
- **Unknowns 要原樣交出**（不要寫成已決定）：卡片待決問題 4（低於 5 人是否降級）、5（整筆退票是否收手續費）、6（閘道退款失敗而座位已釋放）；passenger_id 唯一性（缺陷 D9）；發票折讓。
- **Forces 的一句話版本**：一致性＝「團體 Booking 決定、Inventory 與 Refund 在同一把全域鎖內跟著改」；失敗與重試＝「本期無外部呼叫，任何拒絕都不留下變更」；生命週期＝「PAID →（部分取消 n 次）→ REFUNDED；部分取消過就不能整筆退」。
- **測試戳 store 的地方**：`memory_store.refunds` 現在是清單（`len()`、`not` 照常可用，但不能再用 `booking_id in refunds`）；`transaction_snapshot` 仍可用來證明「無變更」。
- `Booking.cancelled_passenger_ids` 在整筆退票後為全部旅客（一般訂票亦同）；團體付款失敗（`CANCELLED`）不記錄被取消旅客，因為沒有付款也沒有 Order。

## 9. Registry 參考狀態

`domain-memory/` 是表現良好的一組在 D3c 檢查點 5 結束時的 Registry：D3b 結束時的 Registry（D2 reviewed＋D3a 10 筆＋D3b 10 筆候選，見 `../d3b-points-redemption/SOLUTION-NOTES.md` 第 9 節）再加上 8 筆 D3c **候選**。輸入檔是 `evidence/registry-candidates.json`（即 Runbook 的 `d3c-records.json`）：

```powershell
py -3.13 -X utf8 ..\..\tools\make_record.py --batch registry-candidates.json --allow-unclassified --upsert
```

第 8 節列出的已不成立 reviewed 事實不能覆寫，以新 id 的「取代候選」描述新行為；decision 用 `supersedes` 指出被取代者。

| 候選 | 內容 | 取代的 reviewed 事實 |
|---|---|---|
| `aggregates:booking-v2` | 團體 Booking 是部分取消的一致性邊界：狀態、5–20／≥ 5 或 0、金額恆等式、每人只取消一次、部分取消過不可整筆退；commands 加 `cancel_passengers`、`refund_in_full` | `aggregates:booking`（「已付款訂票只能退一次」） |
| `vocabulary:passenger-cancellation` | 旅客部分取消、D 與手續費率帶 | |
| `rules:PCR-004` | 手續費逐位以自己的票價計、向下取整 | |
| `rules:PCR-005` | 有效旅客 ≥ 5 或 0，鎖內檢查，與建立共用 `MIN_GROUP_SIZE` | 補 `rules:GROUP-001`（文件已加註部分取消） |
| `rules:PCR-008` | Σ退款＋Σ手續費＋Σ有效票價＝Order.amount | |
| `rules:REFUND-004-V2` | 每次退款一筆新紀錄；整筆退票一次且限未部分取消過 | `rules:REFUND-004` |
| `decisions:ADR-007` | Booking 擁有部分取消；退款紀錄改為 append-only（`supersedes: ["ASIS-004"]`） | `decisions:ASIS-004` |
| `decisions:ADR-004-V2` | ADR-004 修訂：已付款團體整筆退票限未部分取消過（`supersedes: ["ADR-004"]`） | `decisions:ADR-004` |

驗證（產製時實測）：

| 指令 | 結果 |
|---|---|
| `validate` | `Registry is valid.`（`--require-reviewed` 預期失敗） |
| `verify-audit` | `valid`，90 events，head `sha256:94032381…cdd986` |
| `coverage` | 6 Contexts、27 詞、30 規則、3 Aggregates（`booking`、`order`、候選 `booking-v2`）；缺口 inventory、membership、invoicing 無 Aggregate（ADR 007 第 3 點刻意不合併座位資料）、6 個 Context 都無 Contract |
| `verify-evidence` | 248 個引用：171 current、77 stale（exit 1，預期） |
| `verify-sources` | `stale`（同 D3a） |

**stale**（第 8 節列出的檔案，加上 `business-rules.md`、`booking_service.py`、`members.py`、`payment_service.py`）：

- reviewed（41）：D3b 的 36 筆，加上 `contexts:inventory`、`vocabulary:seat-assignment`、`vocabulary:consecutive-seat-segment`、`rules:SEAT-001`、`rules:GROUP-004`。
- 候選（7）：D3a 的 `rules:EINV-002`、`interactions:payment-triggers-invoicing`；D3b 的 `vocabulary:redeemed-points`、`vocabulary:payable-amount`、`rules:PTS-008`、`rules:PTS-012`、`interactions:booking-reserves-member-points`（行號移動，可直接重新 upsert）。
- **內容已不成立**：D3b 已列出的 `rules:ORDER-002`、`rules:MEMBER-004`、`vocabulary:order`、`vocabulary:points-balance`、`aggregates:order`，加上 `rules:REFUND-004`、`aggregates:booking`、`vocabulary:refund-record`（以 booking_id 為鍵、只能一筆）、`decisions:ASIS-004`、`rules:GROUP-001`（加註部分取消）。`decisions:ADR-004` 引用行沒變所以**不會** stale，但內容需要修訂：verify-evidence 抓不到這種情況，只能靠人審查。

**D4 要做的事**：

- 以 Change Package 升級 D3a～D3c 的候選；三個新測試檔與 `domain/cancellation.py` 先 `confirm-sources`。
- 已不成立的 reviewed 事實：在 proposal 以 `registry_updates` 用**原 id** upsert 新內容（REFUND-004、aggregate `booking`、ADR-004 等），`supersedes` 指名 CP-CORE-001；ASIS-004 以 `remove` 移除或改寫為歷史觀察。之後 `REFUND-004-V2`、`booking-v2`、`ADR-004-V2` 這類暫用 id 在同一 proposal 移除，避免同一事實兩筆。
- 其餘 stale 的 reviewed 事實在同一 proposal 重新引用（內容不變）。
- 交接 Unknowns 與 Forces：見第 8 節（待決問題 4／5／6、passenger_id 唯一性、發票折讓）。
