# B1 Expected Participant Behavior

> 讀者：主持人與觀察人員。時機：Shared Context後第44–52分鐘。前置：了解B1規則與範圍。可見性：Facilitator。

| 觀察面向 | 預期行為 | 需要介入的訊號 |
|---|---|---|
| Teammate分析 | 比較個人Agent結果，要求規則及測試證據，保留分歧與假設。 | 直接採最肯定的摘要，未查來源。 |
| 人員責任 | 人核准修改範圍、計畫，選主要Agent執行。 | 未核准即修改；人員只接受結果不審查。 |
| 最小安全修復 | 針對學生計價，維持成人與既有優惠／順序。 | 全面重寫，提早新增多優惠政策或不相關API變更。 |
| Regression | 正確斷言保留，完整套件真實執行，原相關失敗全部恢復。 | 只跑單一測試、改期待值或Skip／XFail。 |
| Review | 人核對Diff、規則、金額與AC，再接受或要求修正。 | Agent說完成就直接交付。 |
| 誠實交付 | 摘要包含Root Cause、Impact、結果及缺項，時間到收斂。 | 把診斷或Recovery算作自行完成。 |

可接受不同分析順序與摘要形式；需要有來源、核准和可重現結果。B1的學習成功含有效分析與協作，不以速度評分；宣稱軟體修復完成仍須全部AC與全套測試符合。

本文件不要求Digital Worker的人不得改Code限制提前套用到B1；B1仍以Teammate定位觀察，人負責比較、核准與Review。

## P7：B2 過渡成熟度觀察

Agent主動分析規則交互作用、跨模組影響，提出2–3方案及取捨；人Challenge假設、選方案、核准Task Breakdown。主要Agent在核准後主導實作、測試與文件，人Review Diff／Rule／AC並決定接受或修正。

觀察是否逐旅客最有利、不疊加、改票與建立一致、Applied Discount真實、折扣文件同步且完整Regression保留。只改一個分支、忽略Change、未比較方案、以全團共同優惠或疊乘計价、全面Engine重構均需介入。記錄核准、提示、實際結果與未完成，不把Recovery視為原小組完成。

本段是Teammate→Digital Worker過渡；B3正式操作限制待下一階段材料，不把後續答案提前加入。

## P8：Digital Worker觀察

Agent主導需求、Impact、設計、Task Breakdown、Code／Test／Docs／摘要，人主導Challenge與Gate核准。觀察是否先Gate1核需求再設計、Gate2核範圍再修改、Gate3核Diff／結果再交付，沒有把核准當形式。

關鍵證據為5／20及4／21界線、同車廂完整區段、建立失敗不留狀態、付款失敗整筆取消／全釋放／無Order、B2個別價及Audit／通知。人直接改Code、Agent跳Gate、隱藏缺項或將Level2當完整交付均需介入。

如實區分Level1分析、Level2核心、Level3完整交付，保留未完成與核准／拒絕證據；不要求學員在13分鐘無條件達標準答案全部規格。

## 完成條件

留下有證據的觀察、提示與核准／拒絕紀錄，分清分析完成、修復完成、Recovery和未完成。
