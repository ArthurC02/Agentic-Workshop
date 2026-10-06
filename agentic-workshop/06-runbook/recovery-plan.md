# 受控Recovery計畫

> 讀者：主持人與準備人員。時機：事前備援及階段停止點。前置：版本已驗收，準備受控包並實際核對。可見性：Facilitator，含內部來源，不發Participant。

## 觸發與發放時間

| 觸發／時點 | 可用來源 | 處置與界線 |
|---|---|---|
| G0環境／進度阻擋，29分鐘前 | 重新取得乾淨G0；G1只供必要主持受控示範 | 留原成果／缺項；不拿G1當個人已完成，不提前發Brownfield答案。 |
| 29–33 Time Skip／B0來源或啟動異常 | 正式B0或同源clean-copy，保留Bug | 全員統一B0；不可發診斷修復副本或B1替代初始分析。 |
| 52分鐘B1未完成但需進B2 | 已驗收B1受控Recovery | 只提供已結束B1能力，不含B2／B3；原B1成果保留，不算自行修復。 |
| 63分鐘B2未完成但需進B3 | 已驗收B2受控Recovery | 只提供B2能力，不含B3團體解答；重新確認Context再做三Gate。 |
| B3阻擋／76分鐘到 | 保留當前學員成果與Gate | 分析／Review降級或Level1／2摘要，不發B3標準解答充作起點，不由人補Code。 |

先提醒Rule→要求證據→回到Gate→漸進Hint→合格Recovery。若條件未解除或受控包未驗證，直接採分析／Review降級；不為接續而分享完整Evaluation或作者Repo。

## 已驗收來源

| 來源 | 作者Repo內部位置 | 案例識別 |
|---|---|---|
| B0 | `03-brownfield/participant/repository/smart-ticket-b0/`；clean-copy在Evaluation/reference-baseline | b0：`392d920ce4510e5c2dd5df5ae2db25e9ab3b87e6` |
| B1 | `03-brownfield/evaluation/reference-solutions/b1-student-fare-fixed/` | b1-student-fare-fixed：`a1c1d45a26875feb2635f211059db5e8980035f7` |
| B2 | `03-brownfield/evaluation/reference-solutions/b2-best-discount-policy/` | b2-best-single-discount：`cee098acc303398bfa1db0e130e09effeee25828` |

來源Tag／Commit以[B0來源報告](../03-brownfield/evaluation/05-case-history-and-copy-evidence.md)、[B1案例歷史](../03-brownfield/evaluation/14-b1-case-history-and-delta.md)、[B2案例歷史](../03-brownfield/evaluation/17-b2-case-history-and-delta.md)核對；各檔雜湊另見[B1證據](../03-brownfield/evaluation/13-b1-validation-evidence.json)、[B2證據](../03-brownfield/evaluation/16-b2-validation-evidence.json)。來源路徑不是直接分享學員的目錄。版本缺失或Hash不符先停止，不能用不明副本。

## Recovery包白名單與排除

P11生成包時，逐版只取`src/smart_ticket/**`、`tests/**`、`requirements.txt`、`pyproject.toml`及已審查的`docs/business-rules.md`／`docs/architecture.md`。測試呈現本階段起點的既有規則，不加入未來版本案例。主持另生成角色安全README、操作與Context摘要，不直接複製原Evaluation版README。

不直接複製`docs/api-examples.md`；B2原例曾使用FULL_FARE但實際enum為ADULT，摘要應依已驗證Contract與測試生成並核對，舊快照不在本階段修改。文件不是自動正確的事實；程式、規則與Test需交叉確認。

排除版本歷史、ADR、案例Bundle、Evaluation報告／影響分析／AC Map／答案索引、產製指令、Facilitator、`.git`、隱藏歷史、venv、Python／pytest cache及未來版本。白名單是候選，不代表跳過內容審查；生成後檢查每檔、相對連結與隱藏檔，移除或改寫指向未納入／內部內容的連結。

保留來源Tag／Hash、輸出檔清單、文件轉換、角色／階段及驗證結果。再於乾淨目錄確認安裝、Health／OpenAPI、版本Gate及Smoke。P10只完成此計畫，尚未生成或驗證Recovery包，不能聲稱已可直接發放。

## 切換與紀錄

1. 保存原成果、Diff、測試輸出／退出碼、Gate與未完成；記錄觸發、提示、階段／時間與主持決策。
2. 核對已驗收來源及合格受控包，在新目錄開啟；不覆寫或刪除學員原Repo。
3. 停止自己啟動的舊Server，啟動新版本，確認Health與App版本／來源。
4. 建立新Agent Session或明確重建Context；記錄接手版本、完成／未完成、已確認規則及核准範圍。版本切換後不得沿用未確認的舊假設。
5. 用下一段任務與Gate接續；把Recovery來源能力與本組實際成果分開，核准人／時間／證據留存。

若Server、Agent或包仍不可用，以現有材料完成需求、Impact、測試策略或證據Review並列缺項。時間不足仍保留三Gate最低要求與唯一例外，停止擴充，不延長90分鐘。

完成條件：來源、白名單、角色安全內容、實際包驗證與切換紀錄齊備才可發放。包與Recovery技術結果見[一致性修正報告](evaluation/consistency-correction-report.md)；真人切換、新Session／Context及現場可用性仍待演練。初始B0的兩份受控指南與三份安全ADR例外不套用於Recovery。
