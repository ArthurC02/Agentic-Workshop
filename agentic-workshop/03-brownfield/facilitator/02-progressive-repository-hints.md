# 漸進 Repository 提示

> 讀者：主持人。時機：分析遇到停滯或錯誤方向時。前置：已觀察具體卡點。可見性：Facilitator。

| 卡點 | Hint 1：方向 | Hint 2：請Agent對照規則 | Hint 3：請Agent解釋（主持參考位置） |
|---|---|---|---|
| 不知從哪開始 | 請Agent用白話概述核心流程，再說明失敗是否相關。 | 請Agent跑pytest並用驗收對照表對照Rule ID及ADR。 | 請Agent解釋計價流程經過哪些模組（參考：Application與Domain計價群組）。 |
| 只看文件 | 文件結論如何驗證？ | 請Agent找對應測試並附實際輸出。 | 請Agent比對改票實際行為與docs說法，列出不一致處（參考：改票Application）。 |
| 只改測試 | 公開規則與現在期望一致嗎？ | 請Agent對照business-rules與原測試期待值，說明哪一邊有根據。 | 請Agent解釋Fare／Discount Policy目前怎麼算，不給修正碼。 |
| 找到85但不知規則 | 折扣適用對象是否相同？ | 請Agent對照FARE-002與學生票測試。 | 請Agent說明Passenger Type如何影響Fare／Discount計價。 |
| 建議全面重寫 | 哪些差異是本任務必要？ | 以失敗集合及最小Diff評估。 | 先限制到計價Policy與受影響服務。 |
| 小組結論矛盾 | 區分事實、假設與缺口。 | 要求各自的Agent附來源及實際輸出。 | 請Agent用白話說明同一請求的API→Service→Policy路徑。 |

依停滯程度逐級提示，不一次發全表、不提供完整Code。提示一律是「請Agent解釋／請Agent對照規則」，不要求學員自己查程式。提示後要求小組請Agent補證據，不替小組核准計畫。

## 完成條件

提示與觸發原因有紀錄，學員仍依Agent提供的證據自行判斷並作出範圍與核准決策。
