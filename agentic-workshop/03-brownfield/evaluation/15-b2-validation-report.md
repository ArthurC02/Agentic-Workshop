# B2 Validation Report

> 讀者：Evaluation、主持人與素材維護者。時機：P7驗收與進入P8前。
> 前置：已驗收B1、[B2影響分析](06-b2-expected-impact-analysis.md)及[AC Map](09-b2-acceptance-test-map.md)。可見性：Evaluation限定。

2026-10-05實測結論：**B2個別Gate PASS**。正式[B2快照](reference-solutions/b2-best-discount-policy/)共54個來源檔，從B1延續逐旅客最有利單一優惠；B3與整體`PASS FOR WORKSHOP USE`尚未驗收。

## 實際環境與結果

獨立`.codex-tmp/b2-env`，Python3.13.15。依`requirements.txt`安裝FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1成功；Starlette0.46.2、AnyIO4.15.1。

從B2根目錄設定`PYTHONPATH=src`，以獨立環境執行pytest，收集逐案例結果：**55 passed、0 failed、0 skipped、0 XFail，exit0，1.21秒**。未過濾Warning：唯一既知Starlette引用`anyio.abc.BlockingPortal`的DeprecationWarning，與B1相同，未影響測試。機器可讀結果與54來源檔SHA256見[證據](16-b2-validation-evidence.json)。

| 實測項目 | 結果與證據 |
|---|---|
| Import／Health／OpenAPI | App正常載入；Health200；11 API路徑；實際Uvicorn子程序HTTP Health通過，2.18秒 |
| 候選規則 | 成人100、學生75、提前14天85、企業95；七組Domain候選與API補足企業學生組合，均取最低rate、不疊加 |
| 逐旅客與可見明細 | 企業會員＋提前14天，成人595／ADVANCE85，學生525／STUDENT75，總額1120；根層applied_discounts含旅客ID、type、rate、amount，原passengers保持三欄 |
| 改票與整數 | 同一訂票改至基價750，成人637＋學生562＝1199，差額79；每旅客整數截尾再加總，與原付款Order分開保存 |
| 付款／退票／紀錄／Reset | 付款與退票成功；通知3筆、Audit4筆；Reset恢復固定種子、Clock及可控Gateway |
| 失敗原子性 | 新增integration測試核對失敗改票不修改Booking優惠／金額、Order、座位、通知或Audit |
| Regression | B1來源52檔SHA不變；原28項G1測試不變；原13測試檔僅一項first-match期待依法遷移，其餘保持，原44＋新增11＝55 |
| 歷史／隔離 | B1是B2案例祖先；Tag／Bundle及54檔比對通過，無B3歷史；Task卡13AC且無解答路徑 |

## 政策測試遷移

原`test_corporate_first_match_precedes_more_favorable_advance`要求企業95%優先，即665元。B2明確改為最有利單一優惠，故改名`test_corporate_advance_uses_best_single_discount`並期待提前85%即595元。這是需求變更後的合法測試遷移；其他學生75%及回歸斷言保留，未刪除、Skip或XFail測試。

## 文件、限制與決策

FARE-001–006、MEMBER-003及新增FARE-007–010在業務文件、政策實作與AC Map一致。DEBT-001的優惠優先順序與文件缺口已處理；DEBT-002同步通知保留。一般1–4人訂票、In-Memory、模擬金流及非連續座位的既有邊界保持；未產製團體訂票。

55項自動測試時間不代表學員11分鐘或完整90分鐘演練已通過。實際學員演練、交付包隔離與全域驗證仍留待後續。

完成條件：B2政策、13AC與完整Regression有實測證據；B1凍結；文件、歷史與來源快照一致。本版達成，允許下一個授權目標進入P8 B3。
