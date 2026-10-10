# B1 → B2 案例歷史與差異證據

> 讀者：Evaluation與素材維護者。時機：核對演化、Recovery來源與後續打包。
> 前置：已驗收B1及[實測B2報告](15-b2-validation-report.md)。可見性：Evaluation限定；不發Participant。

## 真實演化

以B1案例Bundle建立獨立案例Repository，checkout正式B1 Tag後，分核心、測試與文件三次真實提交，建立B2 Tag。未覆寫B1或將作者Repository歷史冒作案例歷史。

| 項目 | 實際值 |
|---|---|
| B1祖先 | `a1c1d45a26875feb2635f211059db5e8980035f7` |
| 核心提交 | `a4ea373` |
| 測試提交 | `4ad205b` |
| B2 Tag | `b2-best-single-discount` |
| B2完整Commit | `cee098acc303398bfa1db0e130e09effeee25828` |
| 歷史總數 | 14個Commit，包含G0→G1→B0→B1→B2 |
| Bundle | [b2-case-history.bundle](b2-case-history.bundle)，62,064 bytes |
| 驗證 | Bundle verify、Clone、Tag checkout及B1祖先檢查exit0；54來源檔雙向清單與內容比對零差異（僅正規化LF／CRLF） |

所有Refs與歷史均無B3。來源檔排除`.git`、venv與pytest／Python cache；原B1的52檔SHA256完整保留，B2來源雜湊見[JSON證據](16-b2-validation-evidence.json)。

## 差異範圍

- Domain建立所有合格候選，採最低整數rate單次計價；新增DiscountResult.rate及逐旅客AppliedDiscount。
- Booking／Change共用政策與明細，先完成計算再修改座位與狀態；Schema根層增加applied_discounts，原passengers合約保持。
- App標示B2，套件版本0.2.2；新增兩測試檔共11案例，原test_advance只遷移與新規則衝突的一項期待。
- README、業務規則、優惠文件、API、架構、ADR與歷史同步。同步通知及既有改票文件指定落差保留。

沒有團體API、5–20人、連續座位或B3付款失敗補償。案例Bundle與標準解答均僅Evaluation使用；主持Recovery應另按發放時間輸出受控起點。

完成條件：可從B1祖先還原B2、Tag與快照一致、Delta可判讀且歷史不洩漏後續版本。本次全部通過。
