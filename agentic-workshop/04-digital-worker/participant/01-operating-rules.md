# Digital Worker 操作規則

> 讀者：B3 小組與主要 Coding Agent。
> 使用時機：B3 開始時，連同任務卡、工作命令與三道 Gate 整份交給 Agent；人只需掌握下方重點。
> 前置條件：已有核准的 Shared Context、B2 接手版本與 [B3 任務卡](../../03-brownfield/participant/task-cards/03-b3-group-booking.md)。

Agent 主導分析、設計、實作、測試、文件及交付；人設定邊界、核准、挑戰與驗證，承擔最終提交責任。

- 全程人本來就不寫程式、不讀程式；到 B3 連核准方式也變：人只透過三道 Gate 管 Agent。
- 人可以提供需求、要求解釋假設、Challenge、審查驗收對照表／變更審查答案／文件、在 /docs 試 API、Approve／Reject、要求補證與修正，或中止 Agent。
- 人不寫程式、不讀程式、不修改程式，也不替 Agent 補測試；不跳過 Gate，也不因時間壓力接受未驗證說法。
- Agent 可以理解 Repository、分析影響、提出選項，按核准計畫修改、建立與執行測試、更新文件及揭露未完成事項；每次修改後用白話說明改了什麼、為什麼，每次測試後用驗收對照表回報，沒實際執行的一律標「未驗證」。
- Agent 不得越過核准範圍、未核准變更 API、自行改商業規則、加入外部服務／資料庫／規則引擎、刪弱測試、捏造通過結果或在 Gate 未核准前前進。
- 紀錄交給 Agent：已核准背景、各 Gate 提交資料、人員決策原文、升級處理、驗收對照表與變更審查答案，都由 Agent 寫進 `notes/b3.md`；人只做決定，Agent 照原文記錄，不代填核准。
- 回報固定格式、對話只給摘要：每道 Gate 用 [Approval Gates](03-approval-gates.md) 的「Gate 回報格式」；完整內容寫進 `notes/b3.md`，對話不貼完整輸出，省 Token 也方便人比對。

先 Gate 1 核准需求，再 Gate 2 核准影響與設計；Gate 2 核准後才改程式。Gate 3 看驗收對照表與變更審查答案（不看程式），核對未完成事項後決定交付。衝突、資訊不足或超權限立即停止並升級，見 [工作命令](02-agent-work-order.md)。

工具不支援自動修改時，Agent 可產生 Patch，由環境套用；人員仍不得自行補寫程式或測試。

必讀限本規則、[Work Order](02-agent-work-order.md)、[Approval Gates](03-approval-gates.md) 與 B3 任務卡。[Review](04-review-checklist.md)、[Delivery](05-delivery-template.md) 與 [Exception Card](06-exception-response-card.md) 按需使用。

## 完成條件

13 分鐘內保留三 Gate 與真實證據；時間不足保留 Gate 1／2，Gate 3 至少審查測試及未完成事項，例外可縮短為 30 秒判斷。依 Level 1–3 如實交付，不強求完整程式量。
