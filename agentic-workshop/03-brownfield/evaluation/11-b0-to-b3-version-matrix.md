# B0–B3 版本矩陣

> 讀者：Evaluation、Facilitator、Agent Production。時機：逐版交付、Recovery 選擇與包隔離。
> 前置：閱讀各版指令及正式來源／驗證報告。可見性：Evaluation 內部，不放 Participant Package。

B1、B2、B3正式標準實作均已獨立驗收；B3 75項通過，B1–B3標準素材Final Decision為PASS FOR WORKSHOP USE。本表能力／實測數據保存截至P8的版本基線；P9治理文件與P11候選技術驗證已完成，原候選的教材問題正依[一致性修正報告](../../06-runbook/evaluation/consistency-correction-report.md)重驗。真實13分鐘／90分鐘演練與正式放行仍未完成，候選結果不能替代活動驗收。

| 能力／Rule ID | B0 | B1 | B2（個別Gate PASS） | B3（個別Gate PASS） | Primary Tests | Primary Documents |
|---|---|---|---|---|---|---|
| TRIP-001／002 | 完整8Trip；G1 fixture原4Trip | 原樣保留 | 保留 | 保留 | test_features.py、test_seed.py | business-rules.md、api-examples.md |
| BOOKING-001–005 | 一般1–4人／立即保留座位／pending | 原樣保留 | 保留 | 新增5–20團體及原子性 | test_services.py、test_features.py、test_group_creation.py、test_group_payment.py | business-rules.md、architecture.md |
| FARE-001–004 | 成人100%；學生錯85%，正確期待75%；五預期失敗 | 只修學生75%；五失敗已實測恢復 | 各人最有利單一優惠 | 延用B2逐人政策 | test_fare_policy.py、test_services.py、test_features.py | business-rules.md、Failure Manifest |
| PAYMENT-001–003／ORDER-001–002 | 付款唯一Order；失敗pending／保留座位 | 原樣保留 | 保留 | 團體失敗取消／全釋放／無Order，成功單一Order | test_services.py、test_features.py | api-examples.md、business-rules.md |
| MEMBER-001–003 | optional會員／Corporate95%先匹配 | 原樣保留 | 與其他優惠比較不疊加 | 延用B2 | test_members.py、test_advance.py | business-rules.md |
| FARE-005／006 | 固定Clock、≥14天85%；first match | 原樣保留 | 比較各優惠選最低且揭露Applied Discount | 延用B2 | test_advance.py | business-rules.md、discount-overview.md |
| FARE-007–010 | 尚無最低rate政策 | 未提前改政策 | 實作並實測逐旅客全候選最低rate、不疊加、Discount Type／Rate／Amount明細 | 沿用B2政策且團體逐位明細驗證 | tests/unit/test_best_discount_policy.py、tests/integration/test_best_discount_api.py | discount-overview.md、business-rules.md、api-examples.md |
| CHANGE-001–004 | paid才改、容量／座位轉移、差額記錄 | 原樣保留 | 改票重新計價最有利政策 | 一般改票保留；Group改票409不支援；Paid Group Refund保留 | test_changes.py、test_b0_api.py | business-rules.md、change-booking-guide.md |
| REFUND-001–004 | paid退票、REFUNDED、全釋放、唯一記錄 | 原樣保留 | 保留 | 依本版規格保留 | test_refunds.py、test_seats.py | business-rules.md |
| NOTIFY-001–003／AUDIT-001／002 | payment/change/refund通知；建立及成功操作Audit | 原樣保留 | 文件／實作同步 | 團體行為有Audit／通知 | test_records.py、test_changes.py | business-rules.md、architecture.md |
| SEAT-001／002 | 同Trip唯一Seat，不保證相鄰 | 原樣保留 | 原樣保留 | 同車廂完整連續區段 | test_seats.py | business-rules.md |
| GROUP-001–007／GROUP-PAY-001–005／GROUP-FARE-001–002／GROUP-AUDIT-001／GROUP-NOTIFY-001–002 | 無團體功能 | 無團體功能 | 無團體功能 | 5–20人、同廂完整區段、建立失敗無殘留、成功唯一Order、失敗取消／全釋放／Audit與通知，沿用B2計價 | tests/integration/test_group_creation.py、tests/integration/test_group_payment.py | business-rules.md、api-examples.md、ADR004 |
| 受控債／文件落差 | 3債／2落差；核心規則正確 | 不以BugFix全面重構或清債 | 折扣文件已同步最低rate；同步通知及改票指南舊落差保留 | 同步團體與Change邊界；改票指南明示Fare Difference，保留同步通知 | Source／文件Diff審查 | B0 Debt／Delta及ADR |
| 測試預期 | 44＝28原＋16新增；5 Manifest失敗其餘39過 | 全44通過、Manifest5項恢復 | 全套實測55 passed（28原G1＋16B0＋11B2），0 failed／Skip／XFail，1已知Warning，1.21s | 75 passed＝55原＋20新增，0failed／Skip／XFail，1已知Warning，0.58s | 全tests；Manifest集合 | validation report／AC map |
| 來源與交付 | 正式B0＋clean-copy／Bundle | 獨立正式B1，非B0診斷副本 | B2獨立54檔快照；b2-best-single-discount Tag／Bundle驗證通過 | B3獨立59檔快照，b3-group-booking Tag／Bundle與Clone比對通過 | 快照／Tag／Bundle比對 | version-history.md／來源證據 |
| 本次狀態 | 實際前版結果見[報告](01-b0-validation-report.md)，本次來源核對由主代理確認 | PASS：正式獨立環境44項通過，五項失敗恢復；見12-b1-validation-report.md | **個別B2 Gate PASS**：55項通過、API Smoke與來源核對；見15-b2-validation-report.md | **個別B3 Gate PASS**：75項與API Smoke通過；見18-b3-validation-report.md | 不由文件推定實測PASS | 主代理本版驗證報告 |

B0 `PASS AS BROWNFIELD BASELINE` 依 Manifest Gate，不能等同 pytest 全通過。B1 必須零失敗，B1–B3標準素材判定 `PASS FOR WORKSHOP USE`，詳見21-b1-b3-production-result.md；此名稱只驗收標準案例。P9與候選包的後續成果另有報告，活動演練及正式放行仍待驗收。學員時間到可在指定52／63分鐘用已驗收Recovery推進，但不等於Reference Solution AC豁免。B2原名稱誤文以[勘誤](22-b2-documentation-errata.md)查證。

來源：[Brownfield 指令](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)、[B0 追溯](04-b0-rule-traceability.md)、[B1 AC Map](08-b1-acceptance-test-map.md)、[方案 A](../../../docs/planning/b0-regression-gate-proposal.md)。

完成條件：B0/B1來源、差異與測試預期明確，B2標示已實測個別Gate PASS、B3標示已實測個別Gate PASS，版本狀態更新只能根據各版實際證據；Evaluation與Reference Solution保持隔離。
