# D3b 會員點數折抵：主持人參考解答說明

本目錄是 DDD DLC 情境 D3b（需求卡 02：會員點數折抵）的參考解答，也是 D3c（團體部分取消退款）的 Recovery 起點。起點為 D3a 參考解答（`../d3a-e-invoice`，電子發票已上線），只加入點數折抵；刻意保留的邊界洩漏（付款閘道無 Port、Service 依賴具體 Store、字串事件名、三份複製的計價迴圈、一般付款失敗停在 PENDING）原樣不動。

## 驗證方式

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 -m pytest -q          # 156 passed（D3a 的 118 + 新 38）
.\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\integration\test_points_redemption.py   # 38 passed
# 反事實檢查（需 domain-memory 外掛），結果寫入 evidence\counterfactual\*.json
py -3.13 -X utf8 evidence\run_counterfactuals.py .venv\Scripts\python.exe <SkillHub>\.claude\skills\domain-memory\scripts\registry_tools.py
```

## 1. 設計摘要

| 檔案 | 角色 | 變更 |
|---|---|---|
| `src/smart_ticket/domain/members.py` | Membership Domain：四個商業數字（`POINT_VALUE_TWD`、`MIN_REDEMPTION_POINTS`、`REDEMPTION_UNIT_POINTS`、`MAX_REDEMPTION_PERCENT`）、`points_value`、`redemption_cap`、`Member.reserve_points`（PTS-003～005，餘額唯一會減少的地方）、`Member.restore_points` | +30 |
| `src/smart_ticket/application/member_service.py` | `reserve_points(booking)`：PTS-002、扣點、Audit `POINTS_RESERVED`；`restore_points(booking)`：加回、Audit `POINTS_RESTORED` | +18 |
| `domain/models.py` | `Booking.redeemed_points` 欄位、`Booking.payable_amount` 推導屬性（`total_fare` − 點數價值） | +7 |
| `application/booking_service.py`、`group_booking_service.py` | 各多一個參數，並在「座位規劃之後、寫入之前」呼叫一次 `self.members.reserve_points(booking)` | +2／+3 |
| `application/payment_service.py` | `_charge` 扣款與 Order.amount 改用 `payable_amount`；團體付款失敗分支呼叫 `restore_points` | +4／−2 |
| `application/refund_service.py` | 退款金額改為該 Booking 的 Order.amount；呼叫 `restore_points` | +4／−1 |
| `schemas/contracts.py`、`api/routes.py` | 請求選填 `redeemed_points`；Booking 回應多 `redeemed_points`、`payable_amount` | +3／+2 |
| `tests/integration/test_points_redemption.py` | 每個 AC 至少一個 `test_pts_0xx_*`，共 19 個函式／38 個案例 | 247 |
| `docs/adr/006-membership-owns-points-redemption.md`、`docs/requirements/business-rules.md`（新增 PTS 規則表，ORDER-002／MEMBER-004 加註）、`docs/architecture.md`、`docs/api-examples.md`、`README.md`、`docs/version-history.md`、`pyproject.toml`／`main.py`（1.6.0） | 團隊文件與版本 | |

正式程式約 +80／−10 行。**三條計價迴圈（一般、團體、改票）與 `DiscountPolicy` 一行都沒改**；`ChangeBookingService` 完全沒有點數程式碼。

流程：

1. 建立（一般／團體）：既有檢查 → 逐位優惠計價 → 座位規劃 → `MemberService.reserve_points(booking)`（PTS-002 → 003 → 004 → 005，通過就扣餘額、記 Audit）→ 寫入 Booking 與座位。全部在全域鎖內，預留是最後一道會拒絕的檢查，所以失敗時什麼都沒留下（PTS-008），並發時不會超扣（PTS-014）。
2. 付款：閘道扣 `payable_amount`，Order.amount＝`payable_amount`；發票（D3a）取 Order.amount，自動是 500 → 476＋24。
3. 團體付款失敗：原本的取消補償多一行 `restore_points`。一般付款失敗不動（PTS-011）。
4. 退票：退 Order.amount（實付），點數全數 `restore_points`。
5. 改票：不動點數；Fare Difference 照舊用 `total_fare` 相減（PTS-013）。

`grep -rn "MAX_REDEMPTION_PERCENT\|MIN_REDEMPTION_POINTS\|REDEMPTION_UNIT_POINTS\|POINT_VALUE_TWD" src` 只命中 `domain/members.py`，可當作「商業數字只有一個家」的證據。

## 2. Context 劃分與理由

| Context | 本次持有 | 理由 |
|---|---|---|
| **Membership** | 點數餘額、「不得為負」、折抵規則（最低、單位、30% 上限、換算率）、預留與歸還 | 點數是會員的資產，折抵條件是會員權益的使用條款。上限雖以總額為輸入，但決定「這位會員這次能用多少點」的是 Membership。 |
| Pricing（Discount Policy） | 不變：逐位最有利單一優惠、`total_fare`、`applied_discounts` | PTS-006 明說點數不是優惠。Pricing 只交出「優惠後總額」，不知道點數存在。 |
| Booking | 記錄事實「這筆訂票折抵了多少點」（`redeemed_points`），推導 `payable_amount` | Booking 是預留點數的理由與歸還的依據；不另建 Reservation 紀錄。 |
| Payment／Order | 扣款金額與 Order.amount＝應付金額 | Order 是「實際收了多少錢」的唯一來源；退款與發票都從它讀。 |
| Refund | 退 Order.amount；觸發歸還點數 | 現金退實付、點數退點數，兩條路徑互不換算，避免重複或漏退。 |
| Invoicing（D3a） | 不變 | 發票取 Order.amount，D3a 的設計讓本次零修改。 |
| Audit（Generic） | `POINTS_RESERVED`、`POINTS_RESTORED`，detail `points=N` | 沿用 ADR 003 同步紀錄。 |

需求卡待決問題的參考答案：

1. **點數歸誰**：Membership。30% 上限也屬於 Membership（使用條款），不屬於 Pricing；不另開 Loyalty Context（本期沒有累積、到期、等級，新 Context 只會多一層轉手）。見 ADR 006 第 1 點。
2. **預留是否獨立概念**：不需要。直接扣餘額、失敗加回；「預留了多少」記在 Booking，Audit 提供追溯。全域鎖下兩者並發行為相同；獨立 Reservation 紀錄的價值在多程序／非同步釋放，本期沒有。
3. **加在哪裡才不漏改**：不加在計價。折抵在 Booking 建立時「計價完成之後」以單一入口 `MemberService.reserve_points(booking)` 處理；一般與團體各呼叫一次，改票依 PTS-013 不需要。不需要第四份計價程式碼，也不需要先收斂三份計價迴圈（那是另一個重構，與本需求無關）。
4. **直接呼叫還是事件**：直接呼叫（ADR 003 沒有事件機制）。呼叫點只有三處：建立（一般／團體）、團體付款失敗、退票。
5. **逐位分攤**：本期不做。需求卡 03 明確把「有點數折抵的團體部分取消」排除（回 409），所以不需要預留設計空間（YAGNI）。
6. **PENDING 逾時釋放**：未規定，列為 Unknown，不實作。

## 3. Implementation handoff

**Domain facts**
- Membership 擁有 `points_balance`；1 點＝1 元；折抵點數 ≥ 100、為 100 的倍數、價值 ≤ ⌊優惠後總額 × 30 ÷ 100⌋。
- 優惠後總額＝`total_fare`（現行逐位最有利單一優惠加總），不因折抵改變；`applied_discounts` 不變。
- 應付金額＝`total_fare` − 折抵點數價值；付款扣款與 Order.amount 皆為應付金額。
- 預留在建立成功時；團體付款失敗與退票歸還全部；一般付款失敗與改票不動點數。
- 退款現金＝Order.amount；點數另行歸還。

**Forces**
- 三條複製的計價路徑（一般、團體、改票）：改計價就會漏改。
- 全域 `store.lock`（RLock）：所有 Use Case 序列化；檢查與扣除必須在同一把鎖內。
- PTS-008：任何折抵失敗不得留下 Booking、座位、扣點 → 預留必須是寫入前最後一道檢查。
- 團體建立在規劃座位時可能失敗（`CONSECUTIVE_SEATS_UNAVAILABLE`）→ 預留必須在規劃之後。
- D3a：發票取 Order.amount；D3c：有折抵的團體不可部分取消。
- 改票後 `total_fare` 會變，Order.amount 不變 → 退款不能從 `total_fare` 推。

**Decision**
- 沒有新的 Aggregate、Repository、Event 或 Policy 類別：`Member` 加兩個方法守住餘額，`MemberService` 加兩個入口，Booking 加一個欄位和一個推導屬性。
- 被否決的較簡單方案 A：付款時才扣點（`PaymentService` 裡 `member.points_balance -= x`）。無法保證 PTS-008「建立時立即預留」，也讓同一會員兩筆 PENDING 訂票合計超過餘額（PTS-014）。
- 被否決的較簡單方案 B：把點數從 `total_fare` 直接扣掉。破壞 PTS-006（優惠後總額語意）、PTS-013（Fare Difference 用錯基準）、上限（以扣後金額算 30% 會循環），且發票與退款再也分不清楚「優惠」和「點數」。
- 被否決的方案 C：`PointsRedemptionPolicy` 放在 Pricing、或新 Loyalty Context＋事件。沒有任何 AC 需要它保護的行為，只增加轉手。

**External systems**：無（付款閘道沿用，只改傳入金額）。

**Unknowns（本解答的假設）**
- 多個違規同時成立的回報順序：假設 PTS-002 → 003 → 004 → 005，且在既有檢查之後（缺陷 D2）。
- 改票後 `payable_amount`：以新 `total_fare` 推導（750 − 200 ＝ 550），僅顯示；Order.amount 仍 500（缺陷 D6）。
- 退款＝Order.amount 適用於**所有**訂票，含未折抵、已改票者（原本退新票價；缺陷 D3）。
- Audit detail 格式：`points=N`（缺陷 D7）。
- 一般 PENDING 訂票點數永久預留：本期不處理。
- 多程序部署：全域鎖不成立時需要原子條件扣除（ADR 006 Consequences）。

**Proof obligations → 測試**

| 義務 | 測試 |
|---|---|
| 不填或 0：行為與現行相同（一般／團體） | `test_pts_001_*`（4 案例） |
| 無會員要求折抵 409 | `test_pts_002_*`（一般／團體） |
| −100、50、99、150、250 → 409 INVALID | `test_pts_003_*` |
| 超過餘額 409；同時超過餘額與上限時回 INSUFFICIENT | `test_pts_004_*` |
| 超過 30%；665 的上限是 199 不是 200（向下取整、以優惠後總額計）；剛好等於上限可以 | `test_pts_005_*`（兩個） |
| 折抵不改 `applied_discounts`／`total_fare` | `test_pts_006_*` |
| 四個試算值、建立與查詢一致、餘額立即減少 | `test_pts_007_*` |
| 任何折抵失敗：無 Booking、無座位、無 Audit、未扣點；團體無連續座位時未扣點 | `test_pts_008_*`（兩個） |
| 閘道扣應付金額、Order.amount、發票 500 → 476＋24、2,500 → 2,381＋119 | `test_pts_009_*` |
| 團體付款失敗歸還 | `test_pts_010_*` |
| 一般付款失敗不歸還、再付款仍扣應付金額 | `test_pts_011_*` |
| 退款＝Order.amount＋點數全還（一般／團體）；改票後仍退 500 | `test_pts_012_*`（兩個） |
| 改票點數不變、差額 50、Order 500 | `test_pts_013_*` |
| 依序預留至餘額 0；8 個執行緒同時搶 1,200 點只成功 6 筆 | `test_pts_014_*`（兩個） |
| Audit `POINTS_RESERVED`／`POINTS_RESTORED` 含點數 | `test_pts_015_*` |

`test_pts_014_concurrent_bookings_cannot_overdraw` 用 monkeypatch 讓 `redemption_cap` 睡 50 ms，把「檢查餘額」與「扣除」之間的空隙放大；有鎖時結果確定，拿掉鎖時穩定失敗（連跑 8 次皆通過）。

## 4. 反事實檢查（counterfactual）

每條新規則各破壞一次、跑聚焦測試、還原。23／24 killed，`failing_evidence` 皆為斷言失敗（不是 import／語法錯誤），`restoration_result.restored` 皆為 true；1 個是可證明的等價 mutant。JSON 在 `evidence/counterfactual/`。

| AC | 規則 | 破壞方式 | 結果 |
|---|---|---|---|
| PTS-001 | 0 表示不使用 | 移除 `reserve_points` 的 `if not booking.redeemed_points: return` | killed |
| PTS-002 | 需要會員 | 檢查 → `if False:` | killed（變成 404 MEMBER_NOT_FOUND） |
| PTS-003 | 最低點數擋負數 | 移除 `points < MIN_REDEMPTION_POINTS or ` | killed（−100 會讓餘額變多） |
| PTS-003 | 最低 100 | `MIN_REDEMPTION_POINTS = 100` → `200` | killed |
| PTS-003 | 最低 100 | `MIN_REDEMPTION_POINTS = 100` → `1` | **survived，等價**（見下） |
| PTS-003 | 100 的倍數 | `REDEMPTION_UNIT_POINTS = 100` → `50` | killed |
| PTS-004 | 不得超過餘額 | 檢查 → `if False:` | killed |
| PTS-005 | 上限 30% | `MAX_REDEMPTION_PERCENT = 30` → `31` | killed（只有 M002 665 案例抓到） |
| PTS-005 | 向下取整 | `// 100` → `round(... / 100)` | killed（只有 M002 199.5 案例抓到） |
| PTS-005 | 上限含等號 | `>` → `>=` | killed（只有 T002 3,000 → 900 案例抓到） |
| PTS-006 | 上限以優惠後總額計 | `booking.total_fare` → 旅客數 × base fare | killed（M002 折 200、成人＋學生折 400 兩個拒絕案例抓到；卡片試算本身抓不到） |
| PTS-007 | 換算率 | `POINT_VALUE_TWD = 1` → `2` | killed |
| PTS-007 | 應付＝總額 − 點數 | `payable_amount` 回傳 `total_fare` | killed |
| PTS-008 | 預留在寫入之前 | 把 `reserve_points` 移到寫入 Booking 與座位之後 | killed |
| PTS-009 | 扣款應付金額 | `charge(..., payable_amount)` → `total_fare` | killed |
| PTS-009 | Order.amount＝應付金額 | `Order(..., payable_amount)` → `total_fare` | killed |
| PTS-010 | 團體失敗歸還 | 移除 `restore_points` | killed |
| PTS-011 | 一般失敗不歸還 | 在 `raise PAYMENT_FAILED` 前一律 `restore_points` | killed |
| PTS-012 | 現金退 Order.amount | `paid.amount` → `booking.payable_amount` | killed（**只有改票後退票**的案例抓到） |
| PTS-012 | 點數全數歸還 | 移除退票的 `restore_points` | killed |
| PTS-013 | 差額用優惠後總額 | `total - booking.total_fare` → `total - booking.payable_amount` | killed |
| PTS-014 | 鎖內檢查並扣除 | `BookingService.create` 的 `with self.store.lock:` → `if True:` | killed |
| PTS-015 | 預留 Audit 含點數 | detail → `""` | killed |
| PTS-015 | 歸還 Audit 含點數 | detail → `""` | killed |

教學提示（值得在 Review 時拿出來討論「測試證明的是什麼」）：

- **最低 100 → 1 是等價 mutant**（`min-points-1-EQUIVALENT-survived.json`，38 個 PTS 測試全過）。「至少 100 點」和「100 的倍數」重疊：任何正的 100 倍數本來就 ≥ 100，最低值唯一的作用是擋掉 0 以下（−100 在 Python 裡 `% 100 == 0`）。所以 100 → 1 對所有輸入結果相同，但「整個拿掉最低檢查」會被 −100 殺死。卡片的兩個數字其實只描述一條規則（見缺陷 D5）。
- **四個試算中只有 M002（665）對上限敏感**。700／3,500／1,225 的上限是 210／1,050／367，而折抵是 100 的倍數，所以把 30% 改成 31%、`//` 改 `round`、以 base fare 算上限，這三個 mutant 都會在只測卡片前三個試算時存活。665 × 30% ＝ 199.5 是唯一能區分「向下取整」與「四捨五入」（Python 的 `round(199.5)` 是 200）以及「優惠後總額」與「原價」（700 → 210）的數字。
- **上限的等號**只有在上限剛好是 100 的倍數時可觀察；卡片沒有這種試算，本解答補了 T002 成人 2 位 3,000 → 900。
- **退款 `booking.payable_amount`** 在沒有改票時等於 Order.amount，所以「整筆退票」測試全部通過；只有「改票後退票」能證明退款必須讀 Order（750 − 200 ＝ 550 ≠ 實付 500）。

## 5. Agent 常見錯誤（巡堂檢查清單）

1. **把點數放進 `DiscountPolicy`**（當成候選或直接減 amount）：破壞 PTS-006，`applied_discounts` 被改。
2. **從 `total_fare` 直接扣點數**：之後改票的 Fare Difference、退款、上限（以扣後金額算 30%）全部錯；發票與退款分不出優惠與點數。
3. **在三條計價迴圈各加一份折抵**，或只加在一般訂票、漏了團體；或在改票路徑也重算點數（PTS-013 說不動）。
4. **付款時才扣點**：違反 PTS-008，且同一會員兩筆 PENDING 可合計超過餘額。
5. **驗證放在寫入之後**（Booking 與座位已寫入才丟 409），或**扣點放在座位規劃之前**（團體無連續座位時點數已扣）。
6. **上限用 base fare 或 `round()`**：通過 700 試算、在 M002 665 失敗；只測前三個試算時完全看不出來。
7. **用 Pydantic `Field(ge=100, multiple_of=100)` 驗證**：回 422 而不是卡片要求的 409，且規則搬到 schema，商業數字有兩個家。
8. **退款退 `total_fare`**（現金 700＋點數 200，重複退）或 `total_fare − 點數`（改票後錯）。
9. **一般付款失敗也歸還點數**（違反 PTS-011），或團體付款失敗忘了歸還。
10. **檢查在鎖外**（例如在 route 先查餘額）：check-then-act 競態。
11. **改了 Order.amount 卻沒改閘道扣款金額**（或相反）。D3a 的發票若被改成 `booking.total_fare` 也會在這裡露餡。
12. **魔術數字散落**：30、100 寫在 Service、錯誤訊息、測試常數各一份。
13. **過度設計**：新 Loyalty Context＋Domain Event＋Reservation Repository＋Saga；沒有任何 AC 需要它，且違反 ADR 003 卻沒寫新 ADR。
14. **順手收斂三份計價迴圈**：方向正確但不是這張卡的範圍，擴大變更且讓 Review 失焦。
15. **測試只驗卡片試算**：會讓第 4 節列出的 5 個 mutant 存活。

## 6. 需求卡檢查結果

**數字與範例全部正確**：700 → 上限 210 → 200 → 應付 500；665 → 199（199.5 向下取整）→ 100 → 565；3,500 → 1,050 → 1,000 → 2,500；1,225 → 367 → 300 → 925；M003 餘額 0 無法折抵。665 可由 M002 企業 95% 重現，3,500 為 T001 成人 5 位團體，1,225 為成人＋學生 75%，皆與現行優惠政策與 Seed 一致；M001 1,200 點足以涵蓋 1,000（團體）。上限 30% 保證應付金額 ≥ 70% 總額，不會出現 0 或負數。與 D3a 一致：發票取 Order.amount ＝ 應付金額，500 → 476＋24、565 → 538＋27、2,500 → 2,381＋119、925 → 881＋44。

**缺陷與建議修正**（依影響排序）：

| # | 問題 | 影響 | 建議修正文字 |
|---|---|---|---|
| D1 | 沒有定義 API 欄位：請求怎麼帶折抵點數、回應的「折抵點數」「應付金額」欄位名。 | 各組介面不同，主持人無法用同一份驗收測試；Agent 自己發明。 | 新增「API」小節：「`POST /bookings`、`POST /group-bookings` body 選填 `redeemed_points`（整數，預設 0）；Booking 回應（建立、查詢、改票）新增 `redeemed_points` 與 `payable_amount`；`total_fare` 維持優惠後總額。非整數回 422。」 |
| D2 | 多個違規同時成立時回哪個錯誤碼未定義（例：M001 團體 3,500 折 1,300 同時超過餘額與上限；M003 折 50 同時無效與不足；無會員折 50）；與既有錯誤（`INSUFFICIENT_SEATS`、`MEMBER_NOT_FOUND`、`CONSECUTIVE_SEATS_UNAVAILABLE`）的先後也未定義。 | 測試結果因實作順序而異。 | 加一句：「同時違反時依 PTS-002、003、004、005 的順序回報第一個；點數檢查在既有班次、人數、座位、會員檢查之後。」 |
| D3 | PTS-012「退款金額為 Order.amount」沒有限定範圍，等於改變**未折抵、已改票**訂票的退款：現行退的是改票後的新 `total_fare`（T001 700 改 T005 → 退 750，比實付多 50）。卡片 PTS-009 有「僅適用於有折抵的訂票」，PTS-012 沒有。 | 學員不知道該不該動既有退款；若只對有折抵者用 Order.amount，同一個 Service 會出現兩套退款規則。 | PTS-012 改為：「整筆退票的退款金額一律為 Order.amount（實付金額），包含未折抵的訂票；改票後不再退新票價。有折抵者另將折抵點數全數歸還。」（本解答採此版本） |
| D4 | PTS-003「小於 100」字面上包含 0 與負數，與 PTS-001「填 0 表示不使用」矛盾；負數沒有明說。 | 有人把 0 判成 409；有人沒擋負數（−100 是 100 的倍數，會讓餘額變多）。 | PTS-003 改為：「折抵點數不為 0，且小於 100（含負數）或不是 100 的倍數時，回 409 `POINTS_INVALID_AMOUNT`。」 |
| D5 | 「最低 100 點」與「100 的倍數」重疊：正的 100 倍數必然 ≥ 100，最低值只多擋了負數。 | 不是錯誤，但會產生等價 mutant（第 4 節），且讓人以為有兩條獨立規則。 | 可選：商業數字合併為「折抵點數為 100 的正整數倍（100、200、300…）」。 |
| D6 | 改票後的「應付金額」未定義：依定義是新總額 − 點數（750 − 200 ＝ 550），但實付是 500，PTS-013 又說不退不補。 | 回應中出現 550 會被誤解為要補 50。 | PTS-013 加一句：「改票後 `payable_amount` 依新總額重算，僅供顯示；Order.amount 不變，不產生金流。」（或改為凍結在付款時的值） |
| D7 | PTS-015「detail 含點數數量」沒有格式。 | 無法寫一致的驗收斷言。 | 改為：「detail 為 `points=<折抵點數>`，例如 `points=200`。」 |
| D8 | 試算缺少兩種邊界：上限剛好是 100 的倍數（測「不得超過」的等號），以及被拒絕的例子。卡片的四個試算中只有 665 對上限規則敏感。 | 以原價算上限、用 `round()`、`>=` 等錯誤只靠卡片試算抓不到。 | 試算加三行：「M001，T002 成人 2 位：3,000 → 上限 900 → 可折 900 → 應付 2,100」「M002，T001 成人 1 位折 200 → 409 `POINTS_EXCEED_LIMIT`（上限以優惠後 665 計為 199，不是以原價 700 計的 210）」「M001，T001 成人 1 位折 300 → 409 `POINTS_EXCEED_LIMIT`」。 |
| D9 | M003 那一列只寫「—」，沒說要求折抵時的結果。 | 有人回 `POINTS_INVALID_AMOUNT`、有人回 `POINTS_INSUFFICIENT`。 | 改為：「M003，T001 成人 1 位折 100 → 409 `POINTS_INSUFFICIENT`」。 |
| D10 | PTS-008 只說「PTS-002～005 任一失敗時」不扣點，沒涵蓋既有失敗（例如團體無連續座位）。 | 有人在座位規劃前就扣點，團體建立失敗時點數消失。 | 改為：「建立訂票任何原因失敗（含 PTS-002～005 與既有檢查）時，不建立 Booking、不保留座位、不扣點數。」 |
| D11 | 卡片沒提電子發票（D3a 已上線）。 | 學員不確定發票開實付還是原價。 | 背景加一句：「電子發票金額為 Order.amount（應付金額），見 EINV-003。」 |
| D12 | 一般訂票付款失敗後點數永久預留（PTS-011＋待決問題 6），而一般訂票沒有取消 API，會員無法自行解除。 | 不是錯誤（已列待決），但主持人要知道這是刻意留白。 | 「不在本期範圍」加：「一般訂票 `PENDING_PAYMENT` 的點數逾時釋放。」 |

## 7. 30 分鐘可行性與建議切片

參考解答規模：正式程式約 +80／−10 行（比 D3a 小很多）、測試約 250 行；完整 15 條 AC 加上 24 個反事實檢查。

| 時段 | 活動 |
|---|---|
| 0–5 分 | 讀卡、回答待決問題 1–3（點數歸誰、預留怎麼做、加在哪裡不漏改）；主持人先公布 D1 API 與 D2 錯誤順序 |
| 5–8 分 | 寫 handoff／指示 Agent（facts、forces、「不要動計價迴圈」、proof obligations） |
| 8–20 分 | Agent 實作與測試（核心切片） |
| 20–27 分 | Review：上限以優惠後總額、預留在寫入前、退款讀 Order；跑 3–4 個 counterfactual |
| 27–30 分 | 緩衝 |

**判定：核心切片在 30 分鐘內可行；完整 15 條 AC 勉強可實作完成，但沒有時間做 Review 與反事實檢查**（而這兩者才是教學重點）。

- **核心（必做）**：PTS-001、003、004、005、006、007、008、009、010、012、014。這些構成「歸屬＋不變量＋生命週期」：規則住在 Membership、不碰計價、餘額不為負、寫入前預留、付款扣應付、失敗與退票歸還、現金與點數不重複退。
- **延伸（加分）**：PTS-002（一行檢查）、PTS-011、PTS-013（現行行為自然滿足，只需測試）、PTS-015（Audit，機械性）。
- **反事實檢查只做 4 個**：`cap-on-discounted-total`（PTS-006，只有 665 能抓到）、`reserve-before-commit`（PTS-008）、`group-failure-restores`（PTS-010）、`refund-cash-is-order-amount`（PTS-012，沒有改票後退票的測試就會存活）。前者與後者都是「先 survived 再補測試」的好示範。
- 段落結束時發放本目錄作為 Recovery 起點。

## 8. 對 D3c 的影響（Recovery 注意事項）

- 需求卡 03 明確排除「有點數折抵的團體訂票」：部分取消時若 `booking.redeemed_points > 0` 回 409 `PARTIAL_CANCEL_NOT_SUPPORTED`。這是 D3c 唯一需要讀點數的地方；**不要**在 D3c 做點數分攤。
- PCR-008 的恆等式 `Σ 已退款 + Σ 手續費 + Σ 有效旅客票價 = Order.amount` 只在 Order.amount ＝ `total_fare` 時成立，正好就是未折抵的團體（團體不能改票，所以 Order.amount 不會與 `total_fare` 脫鉤）。上一條 409 守住了這個前提。
- 整筆退票現在退 **Order.amount**（`RefundService` 以 booking_id 找 Order）。PCR-012「從未部分取消的團體整筆退票維持現行全額」與此相容：未折抵團體的 Order.amount 就是全額。已部分取消過的團體整筆退票要回 409，守門要加在 `RefundService.refund` 的既有檢查旁。
- `store.refunds` 目前以 booking_id 為鍵、一筆 Booking 一筆紀錄；PCR-007 需要多筆退款紀錄，D3c 必須改這個結構（並保留「整筆退票只能一次」的檢查）。
- 每位旅客票價在 `booking.applied_discounts[*].amount`，PCR-004 應以此為基準。
- `PaymentService`、`RefundService` 都多了 `MemberService` 依賴（建構子內建立，沒有改建構子參數，`tests/unit/test_services.py` 不受影響）。

## 9. Registry 參考狀態

`domain-memory/` 是表現良好的一組在 D3b 檢查點 5 結束時的 Registry：D3a 結束時的 Registry（D2 reviewed＋D3a 的 10 筆候選，見 `../d3a-e-invoice/SOLUTION-NOTES.md` 第 9 節）再加上 10 筆 D3b **候選**。輸入檔是 `evidence/registry-candidates.json`：

```powershell
py -3.13 -X utf8 ..\..\tools\make_record.py --batch registry-candidates.json --allow-unclassified --upsert
```

reviewed 事實不能覆寫（`upsert-candidate` 回 `cannot overwrite reviewed record`），所以被需求改變的事實以**新 id** 的候選描述新行為，舊事實留給 D4。

| 候選 | 內容 | 取代的 reviewed 事實 |
|---|---|---|
| `vocabulary:redeemed-points` | 折抵點數（1 點＝1 元、100 起、100 的倍數、≤ 30%、建立即預留） | 補 `points-balance`「沒有使用點數的功能」 |
| `vocabulary:payable-amount` | 應付金額＝total_fare − 點數價值；扣款與 Order.amount 用它 | 補 `vocabulary:order`「amount 等於訂票總票價」 |
| `rules:PTS-003` | 最低 100、100 的倍數（含負數） | |
| `rules:PTS-005` | 上限＝優惠後總額 30% 向下取整，等於上限可以 | |
| `rules:PTS-008` | 建立時預留，是寫入前最後一道檢查；失敗不留任何東西 | |
| `rules:PTS-009` | 扣款與 Order.amount＝應付金額，發票跟著 | `rules:ORDER-002`（有折抵時） |
| `rules:PTS-012` | 退款一律退 Order.amount，點數另還 | `vocabulary:refund-record`「金額為訂票總票價」 |
| `rules:PTS-014` | 餘額永不為負、全域鎖內檢查並扣除 | `rules:MEMBER-004`「沒有使用點數的功能」 |
| `interactions:booking-reserves-member-points` | membership（producer）→ booking；團體付款失敗與退票呼叫 restore | |
| `decisions:ADR-006` | Membership 擁有點數折抵，Pricing 不知道點數 | |

驗證（產製時實測）：

| 指令 | 結果 |
|---|---|
| `validate` | `Registry is valid.`（`--require-reviewed` 預期失敗） |
| `verify-audit` | `valid`，82 events，head `sha256:f3f25677…63c8` |
| `coverage` | 6 Contexts、26 詞、26 規則、2 Aggregates；缺口與 D3a 相同（Membership 仍刻意沒有 Aggregate：ADR 006 只在 `Member` 加兩個方法） |
| `verify-evidence` | 225 個引用：168 current、57 stale（exit 1，預期） |
| `verify-sources` | `stale`（同 D3a） |

**stale**（引用行因 `booking_service.py`、`group_booking_service.py`、`members.py`、`models.py`、`payment_service.py`、`refund_service.py`、`store.py`、`business-rules.md` 的修改而改變）：

- reviewed（36）：`contexts:booking`、`contexts:membership`、`contexts:payment`；vocabulary `base-fare`、`applied-discount`、`total-fare`、`booking`、`booking-status`、`group-booking`、`passenger`、`refund-record`、`available-seats`、`member`、`points-balance`、`order`、`group-payment-compensation`；`aggregates:booking`、`aggregates:order`；rules `FARE-003`、`BOOKING-002`、`BOOKING-003`、`GROUP-001`、`GROUP-PAY-002`、`PAYMENT-001`、`ORDER-002`、`REFUND-004`、`MEMBER-004`；interactions `booking-uses-pricing`、`pricing-reads-membership`、`booking-reserves-inventory`、`payment-settles-booking`、`payment-compensates-inventory`；decisions `ASIS-001`～`ASIS-004`。
- D3a 的候選（2）：`rules:EINV-002`、`interactions:payment-triggers-invoicing`（`payment_service.py` 行號移動；候選可以直接用 `make_record.py --upsert` 重新引用）。
- 其中**內容已不成立**的只有：`rules:ORDER-002`、`rules:MEMBER-004`、`vocabulary:order`、`vocabulary:points-balance`、`vocabulary:refund-record`（金額）、`aggregates:order`（「amount 為付款當時的訂票總票價」）。其餘只是行號移動。

**D4 要做的事**：

- 以 Change Package 升級 D3a＋D3b 候選；新測試檔 `test_e_invoice.py`、`test_points_redemption.py` 先 `confirm-sources`。
- 上面 6 筆內容已不成立的 reviewed 事實：在 proposal 以 `registry_updates` 用**原 id** upsert 新內容（例如 ORDER-002 改為「Order.amount＝應付金額」），並以 `supersedes` 指名 CP-CORE-001；之後 `PTS-009`、`PTS-014` 等新 id 可保留為獨立規則，或在同一 proposal 移除重複者。
- 其餘 stale 的 reviewed 事實在同一 proposal 重新引用（內容不變）。
- 交接 Unknowns：一般 PENDING 訂票點數永久預留（無逾時釋放）、多程序部署需原子條件扣除（第 3 節）。
