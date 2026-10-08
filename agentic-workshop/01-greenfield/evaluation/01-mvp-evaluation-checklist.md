# Greenfield MVP 評估清單

> 讀者：Evaluation、Facilitator。時機：20 分鐘摘要、22 分鐘收件後評估。
> 前置：取得本次提交、Participant 需求／AC、測試輸出與人機分工摘要；閱讀 [G0 指令](../../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)。
> 可見性：Evaluation／Facilitator 內部；不將內部驗收說明當解答發放。

各列記錄「符合／部分符合／未符合／未驗證」、證據位置及限制；空白或 Agent 自述不能代替實際驗證。這是評估清單，不是已完成的 validation report。

全程人不碰程式：不因學員沒讀程式或沒自己打指令而扣分或判失敗。功能類的證據可由 Agent 代為執行並附指令與輸出，或來自學員在 /docs 的實際試用；Agentic 行為類看學員是否先要計畫、核准後才動、要求並檢查驗收對照表與變更審查答案、用 /docs 驗證行為、如實標示未驗證。

| 類別 | 核對項目 | 應留證據 |
|---|---|---|
| Functional | App／Health／OpenAPI 正常；可售 Trip 與精確站名篩選 | /docs 實際回應或 Agent 執行的指令與輸出 |
| Functional | 1–4 人、座位足夠、成功保留座位、PENDING_PAYMENT | Happy Path 與人數／座位邊界結果 |
| Functional | 成人 100%、學生 75%、逐人計價後加總、整數金額 | Fare 測試及混合 Booking 金額 |
| Functional | 成功付款 PAID、唯一 Order／金額一致；拒絕重複付款 | Payment／Order 整合與失敗結果 |
| Test | Unit 與 Integration 覆蓋核心 Rule／AC；每次重置資料 | test node ID、Fixture／Reset 與追溯 |
| Test | 提供實際執行命令、summary、失敗／Skip／Warning 原因 | 完整輸出；未執行明記未驗證 |
| Test | 不刪除／弱化測試來湊通過；已完成功能無 Feature Skip | 變更審查第 2、3 題回答（含 Agent 附的 git diff 輸出）、Skip 待辦清單 |
| Documentation | README 可讓 Agent 重現安裝／啟動／測試；業務規則與 API 範例一致 | 文件路徑、實際範例與 Rule ID |
| Documentation | 交付摘要列完成／未完成／已知限制與下一步 | 摘要與可驗證證據連結 |
| Agentic Behavior | 修改前先請 Agent Plan，由人確認任務順序與範圍 | Plan、人的確認與調整 |
| Agentic Behavior | 人要求變更審查，逐題判斷後才核准；能用白話說明改了什麼、對應哪條規則 | 變更審查回答與審查卡 |
| Agentic Behavior | 人要求驗收對照表，並在 /docs 試過行為後接受或要求修正；未驗證項如實標示 | 驗收對照表、/docs 試用記錄與後續決策 |
| Agentic Behavior | 能說明人做什麼、Agent 做什麼，仍由人主導驗收 | 人機分工摘要／簡短口述記錄 |

功能完成度與 Agentic 行為分開判讀：功能未完成仍可具備良好的計畫／變更審查／驗收對照表行為；功能跑通也不代表人已審查。此階段 Agent 是 Tool，不評自主率高低、不以提示次數、程式碼量或速度競賽。

區分初始 G0 與學員提交：G0 的未實作 Feature Skip 是骨架設計；不得因此判定學員 MVP 已完成。部分交付列出實際完成範圍，不抹除失敗或把未驗證項寫成通過。

完成條件：四類均有判讀、證據與限制；計畫、變更審查、驗收對照表、/docs 試用與角色說明可核對；結果如實記錄並維持素材隔離，不代替後續實際 validation report。
