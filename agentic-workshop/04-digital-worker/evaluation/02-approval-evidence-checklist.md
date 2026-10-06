# Approval Evidence Checklist

> 讀者：Evaluation、Facilitator。時機：每個Gate及最終Review。
> 前置：已取得Agent提交、Work Order及Approved Context。可見性：Evaluation內部。
> 來源：[治理指令 §6–7／18](../../../docs/instructions/06_Digital_Worker治理與操作規則產製指令書.md)。

Gate 1 Requirement Understanding → Gate 2 Impact and Design → Gate 3 Delivery Review。Gate 1前不得跳過理解；Gate 2明確核准且前置條件已滿足後才修改程式；Gate 3Review後才接受交付。保留短紀錄，不要求完整會議逐字稿。

每Gate複製以下七欄，並補核准人、時間及Context／Submission版本；空白不代表核准。

| 必要欄位 | 待填內容／核對要求 |
|---|---|
| Gate ID | 待填；1／2／3及名稱 |
| Agent Submission | 待填；提交連結／版本與時間 |
| Evidence Reviewed | 待填；實際查看的需求、選項、Diff、Test、文件或風險 |
| Human Decision | 待填；APPROVE／APPROVE WITH CONDITIONS／REJECT AND REVISE |
| Conditions | 待填；條件、負責人、證據、截止／復核；無條件須明記 |
| Observed Deviation | 待填；偏差、處理、是否停止；未觀察到則明記 |
| Final Status | 待填；未核准／待條件／已閉環可前進／退回修正／交付接受或拒絕 |

Approver：待填。Timestamp／Workshop Minute：待填。Approved Context Version／Work Order ID：待填。條件閉環證據與復核人／時間：待填。

- [ ] 核准針對當前提交及Context；修改需求、API或範圍須重新升級審查。
- [ ] APPROVE WITH CONDITIONS的前置條件由人員復核完成才進入下一階段；不能先Coding後補核准。
- [ ] Reject SQLite方案不代表Reject整個任務；回到In-Memory重提Gate 2方案，不以條件式核准放行SQLite。
- [ ] Gate 3有實際Diff／完整Test結果、未完成及風險；時間不足仍保留最小Review，不接受口頭「全過」。
- [ ] 未執行命令／測試明記未執行；已執行保留退出碼、summary及證據連結。

完成條件：三Gate七欄與核准人／時間／版本可核對，所有條件閉環、不跳Gate，最終交付決定有證據；本表尚未填入真實工作坊紀錄。
