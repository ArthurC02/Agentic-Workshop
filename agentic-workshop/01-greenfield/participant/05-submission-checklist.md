# Greenfield Submission Checklist

> 讀者：參與者。時機：提交之前。前置：已完成實作，Agent 已把交付摘要寫進 `notes/greenfield.md`。可見性：Participant。

- [ ] 你在 `/docs` 親自走過：查詢→訂票→模擬付款→查詢 Order，`/health` 正常。
- [ ] `notes/greenfield.md` 有你核准的計畫，以及每一步的驗收對照表與變更審查答案。
- [ ] 最終驗收對照表附實際執行的 `pytest -q` 指令與通過／失敗／跳過數；已涵蓋人數、剩餘座位、75% 學生票及付款邊界（對照 [驗收條件](03-acceptance-criteria.md)）。
- [ ] 交付摘要已如實列出未完成項目、仍被跳過的測試、風險，以及人和 Agent 各做了什麼；沒執行過的標「未驗證」。
- [ ] README 與 `docs/` 已依實際結果更新。

## 完成條件

清單與證據一致；勾選只代表已實際確認。若時間已到仍有缺項，請 Agent 記錄當前完成度與未完成項目後提交，不把部分完成描述為完整交付。
