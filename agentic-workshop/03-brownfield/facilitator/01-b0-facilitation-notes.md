# B0 主持注意事項

> 讀者：主持人。時機：第33–44分鐘分析／整合、第44–52分鐘B1暖身。前置：B0已驗收且內部Manifest可查。可見性：Facilitator，不給學員。

API／Schemas處理Contract，Application協調Domain、Repository及Clock／Gateway；Fare與Discount集中計價。唯一受控Bug是學生率85%，公開正確規則75%，成人加學生700基價應為1225。多項失敗有共同原因，按核實Manifest判讀，不以數量猜Bug數。

三項債：首個符合的優惠Policy、同步Notification、改票指南未記Fare Difference。兩項落差：`docs/change-booking-guide.md` 未描述差額紀錄；`docs/discount-overview.md` 未清楚說明優先順序。主要business-rules與API Contract必須正確。

先講情境與技巧，再講步驟。33–39分鐘技巧是「讓Agent帶你讀陌生專案」：觀察學員是否請Agent畫系統地圖、指出規則在哪、標出文件與程式不一致處，並追問至少一個結論的證據（Runbook提示詞讓Agent先列出結論，學員只回「追問第N個」）；證據看 `notes/analysis.md` 是否每個結論標事實／假設／缺口。同時看三個Agent技巧：Token節費（Agent先列目錄、只讀重點檔並列出讀了哪些檔，不是「讀整個專案」）、模型選擇與推論強度（工具可設定時分析用較強模型／高推論強度）、結構化輸出（照固定標題寫，小組才比得起來）。39–44分鐘技巧是「把共識寫成檔案給Agent」：觀察小組是否在等Agent濃縮時就選定主要Agent與核准者、真的口頭比對各人5行摘要（Runbook「💬 討論一下」，口頭即可、不用寫），並在檢查點1就把分工一兩句打進聊天室，並由主要Agent收到一次貼齊的分工、共識與5行摘要（缺的才問）後寫出 `notes/shared-context.md`，在 `AGENTS.md` 加「開工先讀 notes/shared-context.md」與「審查準則」一節，把「檢查一段工作」搬成 `check` Skill（AGENTS.md 那一節改成一行 Skill 的完整路徑）、複述後停下；之後各段提示詞不再叫Agent先讀規則、也不重貼規則，新對話會自己讀 `AGENTS.md`（技巧：Skill、Token節費）。不因學員表單少填扣分；44–52分鐘依任務卡核准最小修復，停止不必要擴充。一般工程師應能在Agent協助下理解，不以隱晦知識設障。全程人不碰程式：學員不讀程式、不自己跑pytest，分析證據由Agent附來源與實際輸出、用白話說明；學員判斷證據是否對得上公開規則。

首次介紹與收尾：39–44分鐘共同脈絡檢查點2第一次介紹Skill（一個資料夾裡的 `SKILL.md`，開頭 name、description；放在工具會自動載入專案Skill的位置，例如 Claude Code 的 `.claude/skills/`、Codex 的 `.agents/skills/`，學員頁不寫路徑），指著Runbook「技巧：Skill」小卡花約30秒講；Agent 找不到放 Skill 的位置時，請學員貼「放在你這個工具會自動載入專案 Skill 的位置，告訴我完整路徑」；個人分析與共同脈絡時間已滿，段落交界不另開全場分享；學員趁等Agent時看Runbook「完成後想一想」、和旁邊的人聊。

常見誤判：把學生率85當合法規則、改測試期待值、以多項失敗認為多Bug、全面重寫Pricing、提早做最有利優惠、把同步通知視為環境故障。可接受不同調查順序、圖表格式及合理架構摘要，但不接受無證據結論或弱化測試。

介入條件：版本／環境錯誤（請Agent代為重建環境）、提前修改、刪弱測試、分析停滯或分歧無法收斂、學員自己翻程式卡住；依漸進提示處理。時間到立即收斂成果，後續恢復基線安排另依Runbook，不在本階段發B1答案。

## 完成條件

提示、介入與時間紀錄可追查，答案不流入學員包，Shared Context有證據；任務揭露後才核准修改計畫。
