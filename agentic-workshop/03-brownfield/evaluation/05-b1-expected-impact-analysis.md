# B1 預期影響分析

> 讀者：Evaluation、Facilitator、Agent Production。時機：B1 設計審查與交付驗收。
> 前置：正式 B0、[Manifest](06-intentional-failure-manifest.md)、[任務指令 §5–9](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)。可見性：Evaluation 內部，不發 Participant。

## 最小修改與邊界

B1 來源為正式 B0 的獨立快照 [b1-student-fare-fixed](reference-solutions/b1-student-fare-fixed/)。業務邏輯僅修 `src/smart_ticket/domain/fare_policy.py` 的一行：`STUDENT_FARE_RATE = 85` → `75`。App 的 `main.py` 版本 metadata 另由主代理改為 B1，屬版本識別，不改 HTTP 或商業流程。此文件只做唯讀來源核對，未執行程式，不宣稱 B1 已通過。

| 影響 | 預期 |
|---|---|
| FarePolicy.calculate | 無其他優惠的學生 Base Fare 700：595 恢復 525；成人仍 700 |
| DiscountPolicy.calculate | 同一學生分支取得正確 Fare；原 member → advance → student → adult 第一匹配順序保留 |
| BookingService.create／change | 逐人加總，成人＋學生 1295 恢復 1225；座位、狀態及已存在付款金額行為保留 |
| API BookingResponse | 序列化正確總額；不在 Router 增加另一套計價 |
| 原 28 G1＋16 B0 測試 | 原 44 函式、body／assert／fixture 全保留；五個 Manifest 失敗預期恢復，無新增測試壓低失敗數 |
| 文件 | Business Rules 原已寫 75%，核對一致即可；版本來源／識別與歷史更新由主代理負責 |
| 不改 | 成人 100%、提前 85%、Corporate 95%、會員／Seed／Clock、改票／退款／通知／Audit、API／Seat 契約 |

B1 不提前實作 B2 最有利單一優惠。Corporate 學生或同時提前購票的學生，仍可能由較早分支取得 95%／85%，不能用「所有學生永遠最低 75%」擴大 B1 AC；學生率修復與多優惠選擇是不同規則。新增測試 `test_corporate_first_match_precedes_more_favorable_advance` 保留為此邊界的 Regression。

## 驗證與恢復要求

先比較正式 B0／B1 source 差異、44個測試案例／13個測試Python檔與原 28 body／assert；保留 conftest 的 G1 Seed／固定 Clock 適配。正式 B1 須獨立環境完成 Import／Health／OpenAPI／完整 pytest／API Smoke，再確認全部 Manifest node ID 恢復、零失敗、無 Skip／XFail。B0 的隔離診斷副本不是正式 B1 驗證證據。

唯讀確認 B1 rate 已是 75，44 測試函式可辨識；App metadata 須識別 B1，並納入最終來源比對。正式B1獨立環境已44通過（1.00秒），五項恢復，App版本B1；52檔來源与B0祖先／Bundle比對通過，詳見12-b1-validation-report.md及14-b1-case-history-and-delta.md。

完成條件：最小業務 Diff、版本識別與來源可核對，七項 AC 在[測試映射](08-b1-acceptance-test-map.md)有證據，正式 B1 全 44 通過及五項恢復，不改 B0 第一匹配政策、不提供後續階段答案。
