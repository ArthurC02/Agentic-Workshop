# 教材一致性修正與候選包重驗報告

> 讀者：維護者、主持人與Evaluation。時機：本輪優先修正驗收及真人演練準備。
> 前置：[修正指令](../../../docs/instructions/09_教材一致性修正與交付重驗指令書.md)、既有技術來源及本輪審查。可見性：內部。

## 範圍與先前判定

原P11候選`360cb551f76eeb73`的清單／Hash／連結及Recovery技術結果是真實證據，但未涵蓋提前透露學生票Bug、初始B0教材缺失及跨文件前置矛盾。因此不再把該候選當作本次演練材料；原紀錄保留歷史，不能以機械PASS宣稱教學語意完全一致。

本輪優先修正教材與打包，不變更業務規則、凍結程式／測試／Tag／Bundle；B0受控Bug與兩項文件落差保留。真人90分鐘、現場Agent與正式放行仍未執行。

## 修正與驗證

| 問題 | 已落實修正 | 驗證依據 |
|---|---|---|
| 初始B0提前診斷／優惠順序 | 生成Context只保留公開規則與交叉查證，不指出Bug位置或答案優先序 | 準備內容與實際ZIP的content_policy檢查；必要原文經獨立Review |
| B0教材缺失 | 恢復原字節change-booking-guide、discount-overview及三份當時B0安全ADR，README／Architecture連至實際檔 | 五項精確白名單；缺任一或改原字節拒絕，Recovery仍拒ADR |
| 任務揭露前核准 | 39–44只共同事實／分歧／責任，44揭露B1後才填任務範圍與核准計畫 | [Shared Context](../../03-brownfield/participant/04-shared-context-template.md)、[Runbook](../workshop-runbook.md)、評估索引 |
| Level1不能交付 | 前置接受分析／Gate證據；無修改／未執行明記，Level1需合理Impact及完整Test Strategy | [Delivery](../../04-digital-worker/participant/05-delivery-template.md)、[Review](../../04-digital-worker/participant/04-review-checklist.md)；完整Gate不降 |
| B3中途換版 | Recovery固定52／63切換；B3卡點保留現況分析／Review降級，不換版、不發B3答案 | [介入規則](../../04-digital-worker/facilitator/04-intervention-rules.md)、Recovery與Preflight |
| B2誤文與AC判定 | 外置勘誤對照ADULT，原FULL_FARE凍結文件保持；AC-B2-013明記舊審查漏判 | [B2勘誤](../../03-brownfield/evaluation/22-b2-documentation-errata.md)、AC Map及真實Enum／Test |
| Mission時點 | 開場口頭目標，第7分鐘統一發Mission與G0 | Runbook／Mission／評估索引及Manifest一致 |
| 例外卡發放 | 63發空白模板，69–70事件時啟用，不預發情境或答案 | [Response Card](../../04-digital-worker/participant/06-exception-response-card.md)、唯一事件Cue |
| 舊進度當現況 | 版本矩陣明標截至P8資料，鏈本輪最新報告；舊報告標歷史與缺口 | 版本矩陣、P11報告、Agent／治理／規劃 |

實際文件、凍結來源與候選內容結果見[逐項修正證據](consistency-correction-evidence.json)；候選目錄、13ZIP、清單／Hash／連結、內容策略與B1／B2解壓44／55測試／Smoke結果見[新包驗證證據](consistency-package-validation-evidence.json)。兩份JSON描述本次候選，作私有外置補充，不進自己的ZIP。

六個新打包Regression測試方法通過，涵蓋合法B0、重新注入診斷／順序、五項教材缺失與字節修改、在另份Markdown藏答案、實際ZIP自行改metadata後仍拒絕，以及ADR例外不得擴大。原三個Gate負向測試保留；機械條件只覆蓋列出的模式，不宣稱完整自然語句可由Regex證明。

## 完成界線

必要材料、內容防洩漏、凍結來源、實際ZIP與Recovery重驗證據齊備後，才可判本輪修正及候選技術完成。程式檢查只能涵蓋列出的條件；自然語句仍須獨立審查。真人演練與正式發布保持待驗收。
