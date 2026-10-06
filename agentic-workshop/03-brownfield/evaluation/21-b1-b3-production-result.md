# Brownfield任務卡與B1–B3產製結果

> 讀者：Evaluation、主持人與素材維護者。時機：P6–P8累積驗收與進入P9。
> 前置：已验收B0、B1、B2及[B3報告](18-b3-validation-report.md)。可見性：Evaluation限定。

## 產製檔案與任務揭露順序

三張Participant任務卡、四份分階段Facilitator指南、各版影響分析／AC Map、[版本矩陣](11-b0-to-b3-version-matrix.md)、三份獨立Reference Solution及分版Validation／History證據均已建立。

揭露順序：Shared Context完成→B1→B2→宣布Digital Worker操作規則→B3→交付摘要。任务分批，Recovery保留原成果及缺項；Evaluation與Bundle不整份交给學員。

## B1摘要與驗證結果

学生率85→75最小安全修復；不改首個匹配政策。Python3.13.15獨立安裝／啟動／Smoke，44 passed、無Skip／XFail，五個Manifest失敗全部恢復；原13測試檔不變，1既知Warning。見[正式報告](12-b1-validation-report.md)。

## B2摘要與驗證結果

逐旅客最低rate單一優惠、不疊加，Applied Discount含Type／Rate／Amount，改票共用政策。獨立安裝／啟動／Smoke，55 passed、無Skip／XFail，1既知Warning；只有與新規則衝突的企業優先測試合法遷移。見[正式報告](15-b2-validation-report.md)。

## B3摘要與驗證結果

5–20人團體、同車廂完整連續區段、建立原子性、付款失敗CANCELLED／全釋放／無Order及必要Audit／Notification。獨立環境75 passed、無Skip／XFail、1既知Warning，0.58秒；13API與付款成功／失敗Smoke通過。見[正式報告](18-b3-validation-report.md)。

## Regression與Acceptance Traceability

G1原28項正確斷言延續，B1恢復B0全部失敗；B2的需求遷移有明確記錄，B3完整保留B2的55案例與測試檔。7項B1 AC、13項B2 AC、19項B3 AC均有對照；完整57Rule IDs與治理Registry一致，新增17個團體規則有程式／測試／文件定位。

參考[ B1 AC Map](08-b1-acceptance-test-map.md)、[B2 AC Map](09-b2-acceptance-test-map.md)、[B3 AC Map](10-b3-acceptance-test-map.md)與各版JSON實測證據。

## Timebox校正

B1 44–52分鐘8分鐘、B2 52–63分鐘11分鐘、B3 63–76分鐘13分鐘。B3第3／6分鐘做Gate1／2，第11分鐘收斂、第12分鐘Review、第13分鐘停止並Delivery Summary；時間到標Level1／2／3，不要求人員補程式。主持三級提示、停止條件與Recovery流程已定義，未執行真實學員演練，不宣稱時間適配已實測。

## Participant Leakage與一致性檢查

Task卡不含Reference路徑、完整影響分析或座位演算法；主持提示與AC Map／答案分層，三版案例Bundle僅Evaluation。Participant Package尚未產出，正式允許清單打包及包內歷史掃描留待P11。

固定Smart Ticket／90分鐘／Tool→Teammate→Digital Worker、Python3.13／In-Memory、B0核准Manifest Gate及不刪弱測試等上位要求保持。B1→B2→B3案例歷史實際延續，前版來源雜湊凍結；各版能力差異可辨認。

## 已知限制與Final Decision

付款／通知僅本機模擬、一般座位不保證相鄰、團體改票明確不支援；無外部DB與真實金流。唯一Starlette／AnyIO相容Warning已識別。完整Digital Worker Work Order／治理模板屬P9，Runbook／回顧屬P10，包與真實時間演練屬P11，均尚未完成。

本[任務與版本產製指令](../../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)要求的三版標準解答與漸進教材驗收已完成：**Final Decision：PASS FOR WORKSHOP USE**。此判定不代表整套工作坊已正式打包或演練驗收。

完成條件：三版與分批素材各自有真實驗證、Regression及隔離證據；剩餘治理、演練與交付範圍明列。
