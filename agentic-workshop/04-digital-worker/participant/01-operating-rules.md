# Digital Worker 操作規則

> 讀者：B3 小組與主要 Coding Agent。
> 什麼時候用：B3 開始時，連同任務卡、工作單與三道核准關卡（Gate）文件，整份交給 Agent；人只需掌握下方重點。
> 開始前要有：已核准的共同脈絡（Shared Context）、B2 接手的程式版本，以及 [B3 任務卡](../../03-brownfield/participant/task-cards/03-b3-group-booking.md)。

本段 Agent 是 Digital Worker（數位員工：在核准範圍內獨立完成整件任務的 Agent）。Agent 主導分析、設計、實作、測試、文件與交付；人設定邊界、核准、提出質疑、驗證結果，並承擔最終交付責任。全程人本來就不寫程式、不讀程式；到 B3 連核准方式也變：人只透過三道 Gate 管 Agent。

- 人可以：提出需求、要求 Agent 說明假設、質疑（Challenge）、審查驗收對照表／變更審查答案／文件、在 /docs 試 API、核准或退回、要求補證據或修正，或叫 Agent 停下。
- 人不做：不寫、不讀、不改程式，也不替 Agent 補測試；不跳過 Gate，也不因時間壓力接受沒驗證過的說法。
- Agent 可以：讀懂整個程式庫（Repository）、分析影響、提出選項，照核准的計畫修改程式、建立與執行測試、更新文件、說出還沒完成的事。每次修改後用白話說明改了什麼、為什麼；每次測試後用驗收對照表回報；沒有實際執行的一律標「未驗證」。
- Agent 不得：超出核准範圍、未經核准變更 API、自行改商業規則、加入外部服務／資料庫／規則引擎、刪除測試或降低測試標準、捏造通過結果，或在 Gate 核准前往下做。
- 紀錄由 Agent 寫：已核准背景、每道 Gate 提交的資料、人的決策原文、升級處理（Escalation：Agent 遇到停止條件時停下，提出證據交給人決定）、驗收對照表與變更審查答案，都由 Agent 寫進 `notes/b3.md`。人只做決定，Agent 照原文記錄，不代人填核准。
- 回報用固定格式、對話只給摘要：每道 Gate 都用 [三道 Gate](03-approval-gates.md) 文件裡的「Gate 回報格式」；完整內容寫進 `notes/b3.md`，對話不貼完整輸出，省 Token，人也方便比對。

順序：先過 Gate 1 核准需求，再過 Gate 2 核准影響分析與設計；Gate 2 核准後才改程式。Gate 3 看驗收對照表與變更審查答案（不看程式），核對還沒完成的事後，決定是否交付。遇到衝突、資訊不足或超出權限，立即停止並升級，條件見 [工作單](02-agent-work-order.md)。

工具不支援自動修改檔案時，Agent 可以產生修改檔（Patch），由環境套用；人仍不得自己補寫程式或測試。

必讀只有本規則、[工作單（Work Order）](02-agent-work-order.md)、[三道 Gate](03-approval-gates.md) 與 B3 任務卡。[交付審查檢核表](04-review-checklist.md)、[交付摘要範本](05-delivery-template.md) 與 [例外回應卡](06-exception-response-card.md) 需要時再用。

## 完成條件

13 分鐘內保留三道 Gate 與真實證據。時間不夠時，保留 Gate 1／2；Gate 3 至少審查測試結果與還沒完成的事；例外事件可縮短為 30 秒判斷。依完成等級 Level 1–3（Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付）如實交付，不硬要做完全部程式。
