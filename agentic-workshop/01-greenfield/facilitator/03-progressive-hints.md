# Greenfield 三級提示

> 讀者：Facilitator。時機：學員已描述卡點並嘗試後，逐級提供。
> 前置：閱讀需求／AC、[主持指南](01-facilitation-guide.md)及 [G0 指令](../../../docs/instructions/02_Greenfield_Starter_Kit產製指令書.md)。
> 可見性：Facilitator 內部；一次只口頭提供一級，不整表發放。

每次提示後請學員說明下一步，再交給 Agent 操作；不得直接給完整程式碼或完整解題 Prompt。全程人不碰程式：提示一律是「請 Agent 解釋／請 Agent 對照規則」，不要求學員自己查程式、讀檔案或打指令。下表的檔案路徑是給主持人判斷用，不直接念給學員。

| 卡點 | Hint 1：請 Agent 解釋 | Hint 2：請 Agent 對照規則 | Hint 3：指出檢查方向（主持參考路徑） |
|---|---|---|---|
| 找不到入口 | 請 Agent 列出 Greenfield TODO 與 Rule ID，用白話說明每個 TODO 對應哪條需求。 | 請 Agent 說明一個 API 請求從進來到存資料經過哪幾層、各負責什麼。 | 請 Agent 依 TODO 群組提出分段計畫，學員決定先做哪段（參考：`src/smart_ticket/main.py`、`api/`、`application/`）。 |
| Fare 不正確 | 學員用固定 Seed 的成人與學生例子手算總額，在 /docs 建一筆 Booking 比對。 | 請 Agent 對照 FARE-001–004 逐條說明目前怎麼算，哪條不符。 | 請 Agent 在驗收對照表列出 Fare 各條規則與對應測試，並說明乘率、整數與總額怎麼驗（參考：`domain/` Fare Policy、Fare 單元測試）。 |
| Fixture 無法重置 | 請 Agent 單獨重跑失敗測試，用白話說明結果是否依賴執行順序。 | 請 Agent 對照「每個測試前重置資料」的要求，說明目前有沒有共享資料。 | 請 Agent 提出最小修正計畫並說明不會改既有測試期待值（參考：`tests/conftest.py`、Store／Seed／Reset）。 |
| Payment／Order 關係 | 學員用白話描述成功與重複付款應該發生什麼，在 /docs 付款兩次看結果。 | 請 Agent 對照 PAYMENT-001–003、ORDER-001–002 逐條說明目前行為。 | 請 Agent 說明付款失敗時會不會產生 Order 或誤轉 PAID，並附測試名稱（參考：付款用例、Mock Gateway、整合測試）。 |
| 時間不足 | 列出已完成、未驗證與尚未開始項目，回到核心 AC。 | 停止擴充，先驗證已做流程，再補最少文件與限制。 | 17 分鐘收斂、20 分鐘摘要、22 分鐘停止；用提交清單整理計畫、變更審查回答與驗收對照表，未完成如實標記。 |

環境問題可請學員把錯誤交給 Agent 診斷（標準文字 A），主持也可直接協助；商業決策仍由人員主導。記錄卡點與已給級別，以便交接而不重複洩漏更多提示。

完成條件：五項卡點皆具三級提示，逐級使用且無完整解答；學員仍能說明需求、自己決定修改，並依驗收對照表與 /docs 試用結果接受或退回。
