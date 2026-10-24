# 120分鐘工作坊主持Runbook

> 讀者：主持人與協同觀察者。時機：準備及活動全程。前置：[環境準備](environment-setup.md)、[Preflight](preflight-checklist.md)及按角色準備的材料。可見性：Facilitator，不整份發學員。

本機案例Smart Ticket，主線Tool→Teammate→Digital Worker。下表為計畫，不是已執行紀錄。開場前選定計時者及證據記錄者；Greenfield個人，Brownfield先個人分析再小組整合，選主要Agent，不安排額外角色輪轉。

全程人不碰程式：學員不寫程式、不讀程式、不自己打終端機指令；環境建立、啟動伺服器、跑測試與修改都由Agent代做，學員負責決定、核准，用計畫、驗收對照表、變更審查回答與/docs試用驗收。三段的差別是人介入方式：Tool＝人逐步下指令、每步驗收；Teammate＝Agent一起分析、人核准計畫；Digital Worker＝Agent自主執行、人只在Gate核准。盲點：只看證據抓不到「測試全過但寫法有問題」，留到105–120回顧討論。

| 分鐘 | 長度 | Cue／本段發放 | 觀察與提示條件 | 停止／降級 |
|---|---:|---|---|---|
| 00–07 | 7 | 口頭說明目標順序（技巧優先→體驗Tool→Teammate→Digital Worker→證據由Agent寫進notes）、技巧路線圖（九段各練一個流程技巧；提示詞裡埋的六個Agent技巧：Prompt結構、結構化輸出、Skill、Token節費、模型選擇、推論強度，只念名稱與第一次學到的段落，定義留到首次使用的檢查點）與120分鐘流程；任務文件於7分鐘統一發放。 | 確認 Agent 能對話、能讀寫本機資料夾；建環境與 /docs 留到檢查點 1／4；不比較Coding速度。 | 7分鐘進任務；環境未備妥按Recovery分析降級。 |
| 07–30 | 23 | 統一發[G0 Mission](../01-greenfield/participant/01-mission-brief.md)、[需求](../01-greenfield/participant/02-business-requirements.md)／[AC](../01-greenfield/participant/03-acceptance-criteria.md)及骨架。技巧：給Agent規則、先要計畫再動手、小步執行每步驗收（Prompt結構、結構化輸出；模型選擇與推論強度留到個人分析）；四個檢查點07規則與環境（Agent照`04-agent-usage-guide.md`寫專案根目錄的`AGENTS.md`並建`check` Skill，之後每個③只貼一行「用check檢查剛才這一段」）、12先要計畫（計畫開頭先寫三行：要什麼、為什麼、限制）、17小步驗收（放行第1、2步後一起做第3、4步）、24親自驗證交付（一段提示詞補測試、文件與交付摘要，學員等Agent時填交付表單）。 | 看學員是否先讓Agent寫好`AGENTS.md`與check Skill、先要計畫、一次只放行一小步並看驗收對照表與變更審查答案、在/docs親自試；Agent把計畫與每步紀錄寫進notes/greenfield.md。停滯按[Greenfield提示](../01-greenfield/facilitator/03-progressive-hints.md)。 | 30分鐘留成果／缺項，不強修完整MVP；收notes與交付表單（兩個下拉＋選填短答）。 |
| 30–39 | 9 | 技巧「開新對話，確認 Agent 讀到規則檔」（Token節費：舊對話不帶過來）。[Time Skip宣告](../02-time-skip/participant/01-time-skip-announcement.md)，停止個人Repo，全員換統一B0；B0已附前任同事的`AGENTS.md`；學員在B0開新對話，先請Agent只引用`AGENTS.md`原文說出工作規則，再說背景，Agent照它建環境並寫`notes/time-skip.md`。 | 看新對話第一件事是否確認Agent讀到`AGENTS.md`（讀不到就貼Runbook那一句補救，見[環境準備](environment-setup.md)「AGENTS.md與Skill自動載入」）；確認來源；不發B1／B2／B3或Bug根因。 | 檢查點1–3排在30–32、32–37、37–39分，39分鐘進分析；不能用個人G1或已修B1代替B0。 |
| 39–46 | 7 | 技巧「讓Agent帶你讀陌生專案」（Token節費：先列目錄只讀重點檔；較強模型／高推論強度；固定標題的結構化輸出）。發[分析紀錄格式](../03-brownfield/participant/03-individual-analysis-sheet.md)，每人請自己的Agent畫系統地圖、指出規則在哪、標出文件與程式不一致處，寫進`notes/analysis.md`。 | 結論是否標事實／假設／缺口並附來源，是否追問一個結論的證據，先不修改；停滯時按[Repository提示](../03-brownfield/facilitator/02-progressive-repository-hints.md)提醒技巧並給提示詞。 | 分析檢查點39–43、43–46；46分鐘收分析，未查清如實記錄。 |
| 46–52 | 6 | 技巧「把共識寫成檔案給Agent」。發[共同脈絡格式](../03-brownfield/participant/04-shared-context-template.md)，各人Agent把分析濃縮成5行（等待時先選主要Agent與核准者），小組口頭比較（Runbook「💬 討論一下」，不用寫），分工一兩句先打進聊天室；主要Agent收到一次貼齊的分工、共識與摘要後寫`notes/shared-context.md`，在`AGENTS.md`加「開工先讀notes/shared-context.md」與「審查準則」一節，把「檢查一段工作」搬成`check` Skill，並複述（Skill第一次教；之後各段提示詞不再叫Agent先讀規則，新對話會自己讀`AGENTS.md`）。 | 核對共同事實、來源、分歧、限制與待決事項，檢查點1在48分鐘收斂、檢查點2為48–52分；尚未揭露B1，不核准任務修改。 | 52分鐘留`notes/shared-context.md`及角色；任務範圍、計畫與核准待揭露後由Agent寫進該段notes檔，不以口頭補充取代紀錄。 |
| 52–62 | 10 | 只發[B1任務](../03-brownfield/participant/task-cards/01-b1-student-fare-bug.md)；技巧「用失敗測試找Bug：重現→定位→最小修正→驗證」：Agent先重現並定位、寫進notes/b1.md，人核准最小修正計畫後才修改。Agent技巧：Skill與Token節費（規則已在`AGENTS.md`不重貼、測試要摘要，修完Agent建`fix-bug-with-test` Skill，description用第三人稱寫做什麼＋什麼時候用、帶進學員回報Bug時會說的話，學員讀一遍不像就請它改），並教「同一個錯第二次，就寫進AGENTS.md」。 | 52–55重現與核准、55–58最小修正與變更審查、58停止擴充並用同一批測試證明修好；按[Brownfield三級提示](../03-brownfield/facilitator/05-task-progressive-hints.md)。 | 62分鐘停止；需接續時用已驗證B1 Recovery，原成果另留。 |
| 62–79 | 17 | 再發[B2任務](../03-brownfield/participant/task-cards/02-b2-discount-policy-change.md)；技巧「請Agent提2–3個方案並比較，人來選」，紀錄寫進notes/b2.md。Agent技巧：結構化輸出（固定欄位比較表）與推論強度（比較時高、實作時低）；建議開新對話。 | 62–66 Agent比較2–3方案、人選擇核准（未確認假設會改變選擇且未到65分才追問）；66–74只實作一段並做變更審查；74起測試／文件與交付，78提醒檢視逐人優惠與改票。 | 79分鐘停止；缺完成保留方案／Test Cases，按B2 Recovery接續。 |
| 79–99 | 20 | 技巧「委派整件任務：工作單＋三道關卡」。宣布到B3連核准方式也要變：人只透過三道Gate管Agent，發[B3任務](../03-brownfield/participant/task-cards/03-b3-group-booking.md)與B3文件包（[工作單](../04-digital-worker/participant/b3-work-order.md)，學員不讀，由Agent解開存成Skill）。Agent技巧：工作單＝Skill（存成`b3-work-order` Skill）、Gate回報固定格式、新對話選較強模型、細節寫進notes對話只回摘要（Token）。 | 四個檢查點：79交辦、85 Gate1、88 Gate2及唯一例外（例外提示詞與投影的「事件：……」同一則訊息貼）、91起實作（Agent做完計畫就自己交Gate 3卡，97停止擴充只是安全停止線；98 Gate3）；Gate 2沒有條件時可回「核准，例外處理完就開始執行」；看工作單是否存成Skill、只在Gate介入（Agent依工作單交Gate卡、人只回「核准／附條件／退回」）、`notes/b3.md`有決策原文與證據；Cue見下節。 | 99分鐘停止，Level1–3如實交付；人不補Code／Test。 |
| 99–105 | 6 | 技巧「請Agent整理交付摘要，人核對」：Agent依[Delivery](../04-digital-worker/participant/05-delivery-template.md)固定十二標題（結構化輸出）寫`notes/delivery.md`，每欄附證據（提示詞先核對B3 Gate 3紀錄，取代回B3貼③；等Agent寫時小組聊Level）；同時在同一台電腦另開只讀的審查對話，照`AGENTS.md`的審查準則寫`notes/b3.md`「審查紀錄」（寫程式的Agent不核准自己；工具不能同時開兩個對話就寫完再審）；審查紀錄有「重要」時學員貼固定提示詞：Agent把「重要」項目抄進Risks and Limitations，對不上的句子標未驗證，並說改了哪些；審查與Gate 3「核准」相反時，Level跟證據走，Gate 3紀錄照舊，分歧寫進Risks and Limitations；未完成欄附下一輪任務三行（要什麼、為什麼、限制）；收表單與notes資料夾，主要Agent那位同時把notes、`AGENTS.md`與Skill資料夾傳給組員供回顧使用。 | 看學員是否追問「證據在哪」、未驗證如實標示；Recovery、風險與偏差，功能Level與治理證據分開。 | 105分鐘進回顧，不追加Demo美化或修Code。 |
| 105–120 | 15 | 技巧「把今天的技巧變成自己的提示詞清單」：發[提示詞清單](../05-retrospective/participant/reflection-sheet.md)（Maturity只供主持口述）。 | 按[Debrief](../05-retrospective/facilitator/debrief-guide.md)：Agent依notes、`AGENTS.md`與Skill回顧前八段技巧（每段一行，標出用上的Agent技巧）並推薦、學員勾3個（回「同意」後Agent只記下、等下一段）；109–116創作自己的Skill：步驟最固定的一個（已有Skill的技巧如B1的fix-bug-with-test不重寫，改進它或換一個）由Agent先問學員3題再寫成標準格式的Skill（name和資料夾同名，description用第三人稱寫做什麼＋什麼時候用），另外2個寫進`notes/my-prompts.md`；學員用Agent給的3句（2句該用上、1句不該用上，都不提Skill名稱）試跑，每句單獨開一個新對話、只貼那一句，看Agent有沒有用上那份Skill（測的是description），判斷錯就回原對話只改description；116–120小組口頭討論盲點題，再由Agent列3個行動候選寫進`notes/my-prompts.md`、小組選一行直接抄進表單（責任人、時間，從提示詞清單「回到工作：從哪一項開始」五項挑一項的第一步，附那一項自己的領先與落後指標）。 | 120分鐘準時結束；未觀察不編數據，不排名。 |

B1、B2收尾：請學員看Runbook「完成後想一想」，挑第2題請1–2組分享（約1分鐘，含在該段時間內，不另加時；Greenfield改在揭曉時問1–2位，實作時間內不討論）；Time Skip、個人分析、共同脈絡、B3、交付時間已滿，段落交界不另開全場分享，學員趁等Agent時自己看、和旁邊的人聊；新知識點在第一次用到的檢查點才講（Runbook「技巧：…」「新概念：…」小卡，各花約30秒）。

總120分鐘；30–105共75分鐘，B3的20分鐘已包含治理，不新增另一段。原contents一日／半日與跨角色交接只作方法參考，Context交接映射到Time Skip及Shared Context。

## B3核准與唯一例外

相對0／3／6／9／12／18／19／20＝活動79／82／85／88／91／97／98／99。Gate1核准才設計，Gate2核准且條件解除才改程式；Gate3至少審實際測試及未完成。三Gate是學員決策，與素材驗收分開。

唯一`EXCEPTION-DW-001`依[主持事件卡](../04-digital-worker/facilitator/03-exception-injection.md)：若Agent已自然提SQLite不再注入；否則88分鐘用假設卡詢問（學員把例外提示詞和投影的「事件：……」一行貼在同一則訊息），88–91最多60秒，必要縮30秒但不刪事件。不安裝SQLite，標準答案不預發Participant。未核准／未解除條件保持停止，不為趕時間假核准。

## 收件與復原

使用[評估索引](../05-retrospective/evaluation/workshop-evaluation-index.md)定位各段AC、提示、接受範圍與內部答案，勿分享該索引。保留版本、Context、Diff、測試指令／退出碼、Gate人員／時間、提示／介入、Recovery及未完成。

依[Recovery Plan](recovery-plan.md)只在時點發受控已驗收起點，未有合格包降級分析／Review。延遲不增加總120分鐘，不犧牲理解／設計Gate與最低交付Review。主持不得直接提供完整答案Code或替學員修改。

完成條件：十段完整執行紀錄、分批發放、Gate／例外／Recovery及成果與改善可追溯；本文件僅提供流程，實際120分鐘演練待執行。
