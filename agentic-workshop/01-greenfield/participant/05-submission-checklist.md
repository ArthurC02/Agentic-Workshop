# Greenfield Submission Checklist

> 讀者：參與者。時機：提交之前。前置：已完成實作，Agent 已把交付摘要寫進 `notes/greenfield.md`。可見性：Participant。

不用自己逐項勾選：請 Agent 依下列項目逐項回報「有證據（在哪一段）」或「缺（缺什麼）」，你核對它的回報。

1. `notes/greenfield.md` 記錄了你在 `/docs` 親自走過的流程：查詢→訂票→模擬付款→查詢 Order；Agent 啟動伺服器時確認過 `/health` 正常。
2. `notes/greenfield.md` 有你核准的計畫，以及每一步的驗收對照表與變更審查答案。
3. 最終驗收對照表附實際執行的 `pytest -q` 指令與通過／失敗／跳過數；已涵蓋人數、剩餘座位、75% 學生票及付款邊界（對照 [驗收條件](03-acceptance-criteria.md)）。
4. 交付摘要已如實列出未完成項目、仍被跳過的測試、風險，以及人和 Agent 各做了什麼；沒執行過的標「未驗證」。
5. README 與 `docs/` 已依實際結果更新。

## 完成條件

Agent 的回報與證據一致。若時間已到仍有缺項，請 Agent 記錄當前完成度與未完成項目後提交，不把部分完成描述為完整交付。
