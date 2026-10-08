# Brownfield 接手說明

> 讀者：參與者。時機：第29–33分鐘接手、第33–39分鐘個人分析。前置：取得統一 B0 與可用環境。可見性：Participant。

版本為 **B0 - Brownfield Baseline**。使用主持人提供的同一份 Repository，請 Agent 依其中 README 安裝、啟動與執行 `pytest -q`，並用白話回報結果。核心功能含班次、訂票、付款、Order、會員、改退票、通知、座位與 Audit。

目前有若干測試失敗，需要小組分析是否具有共同原因。請先不要修改程式，各自使用自己的 Agent 完成分析；測試結果、規則來源與推論依據由 Agent 寫進 `notes/` 資料夾（`notes/time-skip.md`、`notes/analysis.md`）。第39–44分鐘比較分析，由主要 Agent 寫成 `notes/shared-context.md`，第44–52分鐘再依發放的任務與核准計畫進行工作。

文件是線索，重要結論仍須請 Agent 說明程式、規則、測試三者是否一致，再由你判斷事實、假設與缺口。只有經確認的共同事實才能成為主要 Agent 的執行依據。

## 完成條件

已確認 B0 版本、知道測試結果，完成個人分析的準備，尚未直接修改程式。
