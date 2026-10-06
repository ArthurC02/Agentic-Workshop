# B2 → B3 案例歷史與差異證據

> 讀者：Evaluation與素材維護者。時機：核對案例演化、Recovery來源與後續打包。
> 前置：已驗收B2及[B3報告](18-b3-validation-report.md)。可見性：Evaluation限定，不發Participant。

## 真實演化與來源

從B2案例Bundle建立獨立Repository，checkout正式B2 Tag後，以核心／測試／文件分批真實提交。來源祖先為`cee098acc303398bfa1db0e130e09effeee25828`（b2-best-single-discount）。B3 Tag固定`b3-group-booking`，歷史延續G0→G1→B0→B1→B2→B3；不虛構產品過去12個月的實際开发時間。

| 項目 | 實際證據 |
|---|---|
| B2來源祖先 | `cee098acc303398bfa1db0e130e09effeee25828` |
| 核心Commit | `89ac71d` |
| 測試Commit | `fcc828a` |
| B3 Tag／完整Commit | `b3-group-booking`／`ca3e5de7adca290f555d9ab96f322f65345b3e90` |
| 歷史 | 17個真實Commit；Refs／Log只包含G0→G1→B0→B1→B2→B3 |
| Bundle | [b3-case-history.bundle](b3-case-history.bundle)，73,670 bytes |
| 驗證 | Bundle verify、Clone、Tag checkout、B2祖先檢查全部exit0 |
| 快照比對 | [B3](reference-solutions/b3-group-booking/)59來源檔雙向清單與全內容零差異，僅正規化LF／CRLF |

來源雜湊見[JSON證據](19-b3-validation-evidence.json)。新增或變更的八份Markdown無BOM、單一結尾換行；原程式／測試未因文件整理更動。

## Delta與不變項

新增GroupBookingService、座位幾何與完整連續區段規劃；Booking Type及Assigned Seats根層欄位。先驗證／計價／規劃，再在共同RLock一次寫入Booking及全座位保留。

共享PaymentService依GROUP type實施失败補償：全部釋放、清座位欄位、CANCELLED、無Order、Audit與取消通知。group專用入口拒絕一般訂票，一般付款入口也不能繞過團體補償。原一般付款失敗保持pending與預留座位。

團體改票明確409；已付款團體退票沿用既有流程並全釋放。普通改票／退款、會員、B2優惠、通知／Audit與種子容量不變。App版本B3、專案0.2.3。

新增三個測試檔共20案例，原B2全部15個測試Python檔字節保持、55案例全部保留。新增ADR004與文件同步57規則、13API、整數逐人優惠、兩種付款失敗語意及明確範圍；優惠例採實際ADULT枚舉，改票指南補明Fare Difference。

原B2的54來源檔SHA全部保持；B3沒有隱藏Git目錄、venv或cache，59個來源檔清單與雜湊可核對。Bundle與解答僅Evaluation，正式Participant包及Recovery輸出由後續受控打包處理。

完成條件：B2祖先、B3 Tag與可還原快照一致，Delta可辨認、原版凍結、歷史不混入後續治理產物。本次全部通過。
