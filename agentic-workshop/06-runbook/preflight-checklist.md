# 主持Preflight清單

> 讀者：主持人及環境準備人員。時機：正式活動及演練前。前置：[環境準備](environment-setup.md)、已核對版本與受控材料。可見性：Facilitator。

空表是待執行清單，不是通過報告。記錄執行人／時間、Python、來源Tag／Hash、命令、退出碼、輸出證據與判定；未驗證不放行，已知Warning與未知問題分開。

## 版本Gate

| 版本 | 已驗收基線／本次須核對 | 證據來源 |
|---|---|---|
| G0 | 1 passed、8受控Skip、11主要TODO；Health可用，不宣稱MVP完整。 | [G0報告](../01-greenfield/evaluation/03-g0-validation-report.md) |
| G1 | 28 passed、無Skip／XFail。 | [G1報告](../01-greenfield/evaluation/04-g1-validation-report.md) |
| B0 | 5 failed／39 passed，一個受控Bug，全部失敗node ID精確等Manifest；零未知、無Skip／XFail。 | [B0報告](../03-brownfield/evaluation/01-b0-validation-report.md)、[Manifest](../03-brownfield/evaluation/06-intentional-failure-manifest.json) |
| B1 | 44 passed、Manifest五失敗恢復，無Skip／XFail。 | [B1報告](../03-brownfield/evaluation/12-b1-validation-report.md) |
| B2 | 55 passed、逐人最有利不疊加，無Skip／XFail。 | [B2報告](../03-brownfield/evaluation/15-b2-validation-report.md) |
| B3 | 75 passed、完整連續與付款補償，無Skip／XFail。 | [B3報告](../03-brownfield/evaluation/18-b3-validation-report.md) |

B0 pytest非零是已核准例外，只有失敗集合完全符合Manifest才可接受，不以「剛好五個失敗」判定；不接受新增失敗或刪弱正確測試。唯一既知Starlette／AnyIO BlockingPortal DeprecationWarning已記錄，新Warning先核實。

- [ ] 六版獨立安裝、pip check、Import及Python3.13可核對。
- [ ] Health200／status=ok、OpenAPI及正確App版本可核對，未讀舊Server。
- [ ] 實際pytest結果符合各版Gate；node IDs與B0 Manifest集合已核對。
- [ ] 代表API Smoke及Reset成功；B3失敗取消／全釋放／無Order與Audit／通知有證據。
- [ ] Seed與Clock可控；無真實資料、付款、外部DB／服務核心依賴。

## 發放、治理與復原

- [ ] G0／統一B0／B1／B2／B3及治理材料按時點分包，不提前揭露。
- [ ] 學員包無Evaluation／Facilitator、答案連結、Bundle／Git歷史、未來解答；來源及白名單有記錄。
- [ ] 29分鐘初始B0摘要不指出學生票Bug或優惠答案順序；保留兩份受控落差指南及三份當時B0安全ADR，與分析指引一致。Recovery包從各自參考版附上同樣的兩份指南與三份ADR（B2另附API範例），B1包不出現B2規則。
- [ ] B1 Recovery只於52分鐘接續B2，B2 Recovery只於63分鐘接續B3，包已驗證且保留原成果／Context。
- [ ] 若包未備妥，分析／Review降級可用，不分享Evaluation目錄。
- [ ] Agent可用；個人分析、小組Shared Context及主要Agent／人員核准者已確認。
- [ ] 每台學員電腦：貼上環境準備提示後，Agent能代為建立.venv、安裝依賴並回報pytest結果；能在背景啟動伺服器（埠號8000）、確認/health為status=ok；瀏覽器能開http://127.0.0.1:8000/docs並用Try it out執行一次（/docs的畫面從cdn.jsdelivr.net載入，需要網路；沒有網路時頁面空白，改請Agent用httpx實際呼叫API並列出狀態碼與回應）。學員全程不需自己打指令。
- [ ] Agent能停止自己啟動的伺服器並換版重啟；Port佔用時Agent能改埠並告知新網址。
- [ ] 三Gate與條件結案、唯一EXCEPTION-DW-001、60秒含69–70／可縮30秒已準備。
- [ ] 90分鐘計時、觀察／提示／停止、收件與回顧材料可用；不排名、不強求Level3。

## 本次執行紀錄

| 項目 | 命令／證據位置 | 退出碼／結果 | 執行人／時間 | 缺項／決策 |
|---|---|---|---|---|
| 安裝／啟動／版本 | 待填 | 未執行 | 待填 | 待填 |
| pytest／Manifest／Smoke | 待填 | 未執行 | 待填 | 待填 |
| 包／Recovery／Agent | 待填 | 未執行 | 待填 | 待填 |
| 學員電腦Agent代建環境／啟動／瀏覽器/docs | 待填 | 未執行 | 待填 | 待填 |
| 時程／治理／回顧 | 待填 | 未執行 | 待填 | 待填 |

完成條件：必要檢查有本次真實證據，未知問題已處理或採記錄在案的降級；空表不可當正式活動放行。候選包以[一致性修正報告](evaluation/consistency-correction-report.md)及實際包證據為準；真人演練與現場Preflight仍待執行。
