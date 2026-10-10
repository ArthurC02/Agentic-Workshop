# B1 Expected Participant Behavior

> 讀者：主持人與觀察人員。時機：Shared Context後第44–52分鐘。前置：了解B1規則與範圍。可見性：Facilitator。

| 觀察面向 | 預期行為 | 需要介入的訊號 |
|---|---|---|
| Teammate分析 | 用上「讓Agent帶你讀陌生專案」：`notes/analysis.md` 有系統地圖、規則位置與不一致處並標事實／假設／缺口；用上「把共識寫成檔案給Agent」：主要Agent寫出 `notes/shared-context.md`，B1開始時先請Agent讀它。 | 直接採最肯定的摘要，未查來源；共識只停在口頭；B1開始時沒有先讀 skills/team-rules.md。 |
| B1技巧：用失敗測試找Bug | 先要Agent用失敗測試重現（測試名稱、期待值、實際值）並定位原因，再核准最小修正；修完用同一批測試證明修前失敗、修後通過；`notes/b1.md`逐步有重現、修正、審查、驗證四段紀錄。用上Agent技巧：提示詞以「請先讀skills/team-rules.md」開頭、測試只要摘要（Token節費），結束時有`skills/fix-bug-with-test.md`（Skill）。 | 一開始就叫Agent「修好」；修完只看總數，沒對照同一批測試；notes只有結論沒有證據；又整段重貼規則或貼完整測試輸出。 |
| 人員責任 | 人核准修改範圍、計畫，選主要Agent執行。 | 未核准即修改；人員只接受結果不審查。 |
| 最小安全修復 | 針對學生計價，維持成人與既有優惠／順序。 | 全面重寫，提早新增多優惠政策或不相關API變更。 |
| Regression | 正確斷言保留，完整套件真實執行，原相關失敗全部恢復；學員從變更審查第2、3題確認。 | 只跑單一測試、改期待值或Skip／XFail；學員沒問就接受。 |
| Review | 貼Runbook提示詞→看Agent回報→回一句決定→讓Agent記進notes/b1.md；看變更審查答案與驗收對照表（可在/docs試金額）逐題判斷後再接受或要求修正。 | Agent說完成就直接交付；審查答案有「否／不確定」仍放行；學員自己打指令或手抄輸出。 |
| 誠實交付 | 摘要包含Root Cause、Impact、結果及缺項，時間到收斂。 | 把診斷或Recovery算作自行完成。 |

可接受不同分析順序與摘要形式；需要有來源、核准和可重現結果。B1的學習成功含有效分析與協作，不以速度評分；以是否用上技巧、證據（`notes/b1.md`、驗收對照表、/docs試用）是否齊全判斷，不因學員沒讀程式、沒自己打指令或表單少填而扣分。宣稱軟體修復完成仍須全部AC與全套測試符合。

全程人不寫程式也適用B1；B1與B3的差別是人介入方式：B1仍以Teammate定位觀察，Agent一起分析、人比較、核准計畫與做變更審查；三道Gate的核准方式留到B3。

## P7：B2 過渡成熟度觀察

技巧：請Agent提2–3個方案並比較，人來選。Agent主動分析規則交互作用、跨模組影響，把2–3方案及影響、風險的比較寫進`notes/b2.md`；人不接受第一個答案，至少Challenge一個假設、選方案、核准Task Breakdown，選擇理由寫得出來。Agent技巧證據：比較表欄位固定（方案／改動範圍／風險／測試影響／建議，結構化輸出），比較時調高推論強度、實作時調回低。主要Agent在核准後主導實作、測試與文件，人透過變更審查回答、驗收對照表與/docs試用確認Rule／AC，並決定接受或修正。

觀察是否逐旅客最有利、不疊加、改票與建立一致、Applied Discount真實、折扣文件同步且完整Regression保留。舊第一匹配測試（`test_corporate_first_match_precedes_more_favorable_advance`，665）與FARE-008衝突：預期Agent先停下列出測試名稱、舊期待與Rule ID，由人核准後才改成新規則的結果（595）；直接改期待值未經核准、或改到其他期待值，需介入。只改一個分支、忽略Change、未比較方案、以全團共同優惠或疊乘計價、全面Engine重構均需介入。記錄核准、提示、實際結果與未完成，不把Recovery視為原小組完成。

本段是Teammate→Digital Worker過渡；B3正式操作限制待下一階段材料，不把後續答案提前加入。

## P8：Digital Worker觀察

Agent主導需求、Impact、設計、Task Breakdown、Code／Test／Docs／摘要，人主導Challenge與Gate核准。觀察是否先Gate1核需求再設計、Gate2核範圍再修改、Gate3核變更審查回答／結果再交付，沒有把核准當形式。Agent技巧證據：`skills/b3-work-order.md`存在（工作單＝Skill）、Gate回報每次同一組標題、自主執行選較強模型、細節在`notes/b3.md`而對話只回摘要。

關鍵證據為5／20及4／21界線、同車廂完整區段、建立失敗不留狀態、付款失敗整筆取消／全釋放／無Order、B2個別價及Audit／通知。人直接改Code、Agent跳Gate、Agent未附指令與輸出就宣稱通過、隱藏缺項或將Level2當完整交付均需介入。

如實區分Level1分析、Level2核心、Level3完整交付，保留未完成與核准／拒絕證據；不要求學員在13分鐘無條件達標準答案全部規格。

## 完成條件

留下有證據的觀察、提示與核准／拒絕紀錄，分清分析完成、修復完成、Recovery和未完成。
