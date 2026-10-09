# B2 預期影響分析

> 讀者：Evaluation、Facilitator、Agent Production。時機：B2 設計與交付審查。
> 前置：已驗收 B1、[B2 指令 §10–16](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。可見性：Evaluation 內部，不放 Participant Package。

B2 從凍結的正式 B1 延續，將會員 → 提前 → 學生 → 成人的第一匹配政策，改成「建立所有符合的候選、選最低折扣率、每人只用一項」。學生75%、提前85%、Corporate95%、成人100%數值不變；無疊乘、無團體功能。

| 影響區域 | 需要核對的行為 |
|---|---|
| Domain DiscountPolicy | 候選資格維持有效會員／固定Clock／≥14天／旅客型別；選數值最低rate，回傳amount、discount_type、整數rate |
| BookingService.create | 每位Passenger獨立選擇，總額為每人amount加總；同一次計算產生明細，驗證後才寫Booking／座位 |
| ChangeBookingService.change | 目標Trip及當前Clock用同政策重新計價；同步total_fare、fare_difference、applied_discounts；原Order付款金額不變 |
| Domain／Schema／API | Booking根層applied_discounts陣列：passenger_id、discount_type、rate、amount；原passengers三欄保持不變 |
| 文件 | business-rules.md新增FARE-007–010，discount-overview.md與API Examples改成最有利且不疊加；ADR記錄候選選擇，不引入複雜規則引擎 |
| Regression | 原28 G1 body／assert與B1學生修復保留；新增組合、API明細、改票與原子性驗證 |

## 一項合法的政策測試遷移

原B1 `tests/integration/test_advance.py::test_corporate_first_match_precedes_more_favorable_advance` 以665驗證第一匹配，與B2新規則衝突。僅在B2副本將它改名 `test_corporate_advance_uses_best_single_discount`，Corporate＋提前期待665→595，無會員提前仍595；原B1與B0檔案凍結不改。這是明確的新需求遷移，不是刪除覆蓋、降低要求或為湊通過弱化斷言。

原44中其餘43項測試保留；新增Unit七組候選與Integration四項，實際完整執行55有效案例。Unit分別驗證無優惠、學生、提前、Corporate、學生＋提前、Corporate＋提前、三者同時符合；API另驗Corporate學生無提前、逐人不同優惠及相同政策改票。每項都核對實際rate／type／amount，不能只核對總額。

改票原子性新增case先建立／付款，再使目標容量不足；核對Booking（含票價與Applied Discount）、Order、Seat ledger、Audit／通知與兩班容量均未發生部分變更。成功改票則更新明細及差額並維持已付Order金額。

主代理於2026-10-05使用獨立Python3.13.15環境完成正式B2安裝、Import、Health、OpenAPI（11個paths）、uvicorn Health及API Smoke，混合優惠、改票、退款、通知／Audit均通過；完整pytest為 `55 passed, 1 warning in 1.21s`，零failed／skip／xfail。詳見[正式B2報告](15-b2-validation-report.md)與[機器可讀證據](16-b2-validation-evidence.json)。Warning及來源／版本metadata／Tag／Bundle依本版報告記錄，不以B1報告替代。

唯讀文件核對：B2 business-rules.md共有40個唯一Rule ID，集合完全等於B0原36＋FARE-007／008／009／010；未遺漏或重編。AC Map引用的10個不同函式均存在於B2測試，七個Unit param ID及新增API路徑與正式程式相符。

完成條件：新政策及唯一舊測試遷移有明確原因，原28及其他B1測試保留；[13項AC映射](09-b2-acceptance-test-map.md)與正式B2實測吻合，零失敗、無Skip／XFail，文件及API明細同步，不提前實作B3。
