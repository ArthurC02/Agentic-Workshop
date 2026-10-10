# Digital Worker Delivery Summary

> 讀者：主要 Coding Agent 與小組審查者。
> 什麼時候用：B3 結束後（第 76–78 分鐘），由 Agent 依此格式把交付摘要（Delivery Summary）寫進 `notes/delivery.md`，人核對。這是結構化輸出，規則：
> - 固定十二個英文標題，名稱與順序都不變（主管才能逐欄比對）；每個標題下第一句是中文意思。
> - 每一欄都附證據來源（`notes/b3.md` 哪一段、哪個測試指令或文件）。
> - 沒有證據的寫「未驗證」。
> 開始前要有：目前的分析／設計成果與核准關卡（Gate）紀錄；有修改或已執行指令時，附實際紀錄。Level 1 可無修改、無已執行測試，但要寫明原因與未驗證範圍。照實際成果填寫，不預先填「成功」。

## Mission Result

任務結果。任務 ID：TASK-B3-001；結果：____；依據：____。

## Completion Level

完成等級。擇一並說明證據，不自動選 Level 3：

- Level 1：分析完成（Analysis Complete）— Gate 1／2 完成，影響分析合理、測試策略完整，程式尚未完成。
- Level 2：核心流程完成（Core Flow Complete）— 團體建立與連續座位完成、主要單元測試通過，付款失敗的補償（Compensation）或文件仍有缺項。
- Level 3：完整交付（Delivery Complete）— 建立、付款成功與付款失敗的補償都完成，回歸測試（Regression）通過，文件與交付摘要都完整。

實際等級與原因：____。

## Implemented Scope

已完成的範圍：____。

## Not Implemented

未完成的範圍。未完成／未驗證：____；影響：____；下一步：____。

## Files Changed

修改的檔案。每個實際修改的檔案改了什麼、為什麼（白話）：____；Gate 3 變更審查答案：____。沒有修改時寫「無修改」與原因，不虛構變更。

## Business Rules Covered

涵蓋的商業規則。規則編號（Rule ID）與對應的程式／測試／文件證據：____。

## Acceptance Criteria Results

驗收條件（AC）結果。用驗收對照表列出每條 AC 的結果：PASS（通過）／FAIL（失敗）／NOT VERIFIED（未驗證），以及依據的測試名稱：____；人在 /docs 實測的結果：____。沒驗證的不能寫 PASS。

## Test Command and Actual Result

測試指令與實際結果。工作目錄／版本：____；實際指令：____；結果與結束代碼（exit code）：____；失敗／跳過（skip）／預期失敗（xfail）／警告（warning）：____；未執行的部分與原因：____。

## Documentation Updated

已更新的文件。文件與內容：____；還沒同步的：____。

## Risks and Limitations

風險與限制。已知風險、限制與對責任的影響：____。

## Deviations from Approved Plan

和核准計畫的差異。Gate 2 計畫與實際的差異：____；升級處理與人的決策：____。沒有差異也要寫明。

## Recommended Decision

建議決策（核准／附條件核准／退回修正）：

APPROVE | APPROVE WITH CONDITIONS | REJECT AND REVISE

Agent 的建議與理由：____。人的最後決策記在 Gate 3；摘要裡的 Gate 決策必須和 `notes/b3.md` 的原文一致。測試通過之外，還要核對需求、範圍、文件與還沒完成的事。

完成條件：十二欄都用實際證據，或用「未修改／未執行／未驗證」加原因填寫；Level 1／2 如實寫出差距。活動成果可以接受，不等於完整軟體交付；要宣稱 Level 3，仍須有完整功能、回歸測試、文件與審查證據。最終責任由人承擔。
