# P11 全域驗證與候選交付報告

> 讀者：維護者、主持人與驗收人員。時機：候選包驗證及真人演練準備。
> 前置：[P11指令](../../../docs/instructions/08_全域驗證與受控打包產製指令書.md)、P0–P10已驗收來源。可見性：Evaluation，不發學員。

## 判定範圍

P11已啟動；本輪執行自動化版本驗證與受控候選包建置。使用者已選擇本次安排真人演練，參與人員與可用時段尚待提供。真人90分鐘、B3的13分鐘活動與現場Agent／人員Gate目前未執行，整體發布Gate保持待驗收。

本報告的原候選包結果為歷史機械驗證：後續發現初始B0答案洩漏、必要教材缺失及跨文件前置矛盾，`360cb551f76eeb73`不再用於本次演練。修正與新候選以[本輪一致性報告](consistency-correction-report.md)為準；原六版技術結果保持有效，但不能以清單／Hash／連結PASS推論教學語意完全一致。

## 技術驗證

以 [validate_workshop.py](../../../scripts/validate_workshop.py) 在六個既有獨立venv執行；Python3.13.15。並未重裝依賴，以pip check驗證既有環境，保留每次命令／退出碼／時間／輸出與SHA256，見[本輪JSON](p11-validation-evidence.json)及其列出的原始log／JUnit XML。

| 版本 | 本輪pytest結果 | 判定 |
|---|---|---|
| G0 | 1 passed／8受控skip | PASS，核對Skip名稱與型別，不宣稱完整MVP |
| G1 | 28 passed | PASS，無skip／xfail |
| B0 | 39 passed／5 failed，exit1 | PASS AS BROWNFIELD BASELINE，失敗node集合精確等核實Manifest，零未知 |
| B1 | 44 passed | PASS，無skip／xfail |
| B2 | 55 passed | PASS，無skip／xfail |
| B3 | 75 passed | PASS，無skip／xfail |

六版pip check、Import／代表API Smoke、實際Uvicorn隨機本機Port Health／OpenAPI通過，僅停止工具自己啟動的子程序。保留既有Starlette／AnyIO BlockingPortal DeprecationWarning；未知Warning會拒絕。本輪以既有環境驗證，並非演練現場新安裝或Agent可用性證據。

另以[依賴核對工具](../../../scripts/verify_runtime_baselines.py)驗證六venv的五項requirements固定版本均相等，Python3.13.15；[Runtime證據](p11-runtime-baseline-evidence.json)保存來源26／30／52／52／54／59檔在本次依賴核對前後Hash一致。此檢查不冒稱不存在的G0／G1歷史Hash清單。

全域靜態檢查範圍為Agent.md、docs與agentic-workshop Markdown；檢查連結、UTF-8、Fences及Participant內部引用。G1四份既有BOM文件列為凍結來源，不改寫；新文件無BOM。57項Registry與G1／B0／B2／B3的16／36／40／57規則、映射及引用測試函式可定位；這是追溯定位，不能代替全部子情境語意審查。B0／B1／B2／B3原52／52／54／59來源檔雜湊相等。最終數量與定位細節見JSON。

驗證器拒絕測試涵蓋同數量但不同B0失敗集合、xfail偽裝skip、已知與未知Warning混合；靜態限定執行寫獨立STATIC_PASS證據，不以空versions集合宣稱六版通過。

## 候選包與Recovery

本輪使用[白名單](../../../scripts/package-manifest.json)及[建置工具](../../../scripts/build_delivery.py)生成13份分受眾／時點候選ZIP，輸出位於忽略追蹤的dist；重建與包定位見[操作說明](../../../scripts/README.md)及[包驗證JSON](p11-package-validation-evidence.json)。發布核准前僅供演練準備。

原候選學員材料依G0、Time Skip統一B0、個人分析、Shared Context、B1、B2、B3與治理、回顧分批；主持與Evaluation為私有包。B0是過濾匯出，保留原程式／測試與Bug，不等同作者Repo的52檔clean-copy。原過濾排除ADR及兩項受控落差，與教學輸入不一致；新候選須恢復兩份學員指南及三份當時B0安全ADR精確白名單，移除生成Context提前診斷。本報告保留原打包結果作歷史，不把原「安全摘要」名稱當內容通過證據。

B1 Recovery限52分鐘接續B2，B2 Recovery限63分鐘接續B3；不提供B3答案作Recovery。實際解壓副本以各自既有venv執行pip check、pytest 44／55 passed及Health、11路徑OpenAPI、建立／付款／改票／退票Smoke通過。這是交付副本技術驗證；真人切換、新Session／Context確認仍未執行。包內容／Hash／連結、拒絕篡改測試與審查修正結果見包JSON。

獨立審查發現的包ID／角色／時點、生成檔隔離、API折扣名稱及Warning辨識缺口已納入修正與拒絕案例。候選建置證據以審查過的來源白名單作信任依據；外置P11證據不塞回自己的ZIP形成循環雜湊。私有主持／Evaluation連結需按操作說明掛載相依材料，不能預發給學員。

## 真人演練與發布缺項

真人演練依[演練紀錄](../rehearsal-record.md)填實際時間、成果與偏差；依[發布清單](../release-checklist.md)核對版本、候選包雜湊、Agent可用性、分批發放、Gate、唯一例外與Recovery。未觀察記未執行，O-01／O-02真人證據解除條件保留。

完成條件：本輪技術結果與原始證據可重跑；候選包隔離可核對，真人與發布待驗項明列。只有真人結果、必要修正及最終驗收齊備，才能宣稱P11整體完成。
