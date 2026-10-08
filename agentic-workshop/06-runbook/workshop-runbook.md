# 90分鐘工作坊主持Runbook

> 讀者：主持人與協同觀察者。時機：準備及活動全程。前置：[環境準備](environment-setup.md)、[Preflight](preflight-checklist.md)及按角色準備的材料。可見性：Facilitator，不整份發學員。

本機案例Smart Ticket，主線Tool→Teammate→Digital Worker。下表為計畫，不是已執行紀錄。開場前選定計時者及證據記錄者；Greenfield個人，Brownfield先個人分析再小組整合，選主要Agent，不安排額外角色輪轉。

全程人不碰程式：學員不寫程式、不讀程式、不自己打終端機指令；環境建立、啟動伺服器、跑測試與修改都由Agent代做，學員負責決定、核准，用計畫、驗收對照表、變更審查回答與/docs試用驗收。三段的差別是人介入方式：Tool＝人逐步下指令、每步驗收；Teammate＝Agent一起分析、人核准計畫；Digital Worker＝Agent自主執行、人只在Gate核准。盲點：只看證據抓不到「測試全過但寫法有問題」，留到80–90回顧討論。

| 分鐘 | 長度 | Cue／本段發放 | 觀察與提示條件 | 停止／降級 |
|---|---:|---|---|---|
| 00–07 | 7 | 口頭說明目標順序（技巧優先→體驗Tool→Teammate→Digital Worker→證據由Agent寫進notes）、今天9個技巧與90分鐘流程；任務文件於7分鐘統一發放。 | 確認每位學員的Agent能代為建環境、啟動伺服器，瀏覽器能開/docs；不比較Coding速度。 | 7分鐘進任務；環境未備妥按Recovery分析降級。 |
| 07–29 | 22 | 統一發[G0 Mission](../01-greenfield/participant/01-mission-brief.md)、[需求／AC](../01-greenfield/participant/03-acceptance-criteria.md)及骨架。技巧：給Agent規則、先要計畫再動手、小步執行每步驗收；四個檢查點07規則與環境、09先要計畫、11小步驗收、24親自驗證交付。 | 看學員是否先貼規則、先要計畫、一次只放行一小步並看驗收對照表與變更審查答案、在/docs親自試；Agent把計畫與每步紀錄寫進notes/greenfield.md。停滯按[Greenfield提示](../01-greenfield/facilitator/03-progressive-hints.md)。 | 29分鐘留成果／缺項，不強修完整MVP；收notes與4欄交付表單。 |
| 29–33 | 4 | 技巧「開新對話先給規則與脈絡」。[Time Skip宣告](../02-time-skip/participant/01-time-skip-announcement.md)，停止個人Repo，全員換統一B0；學員在B0開新對話，先貼規則與背景，Agent建環境並寫`notes/time-skip.md`。 | 看新對話第一件事是否貼規則與背景、Agent有無複述；確認來源；不發B1／B2／B3或Bug根因。 | 33分鐘進分析；不能用個人G1或已修B1代替B0。 |
| 33–39 | 6 | 技巧「讓Agent帶你讀陌生專案」。發[分析紀錄格式](../03-brownfield/participant/03-individual-analysis-sheet.md)，每人請自己的Agent畫系統地圖、指出規則在哪、標出文件與程式不一致處，寫進`notes/analysis.md`。 | 結論是否標事實／假設／缺口並附來源，是否追問一個結論的證據，先不修改；停滯時按[Repository提示](../03-brownfield/facilitator/02-progressive-repository-hints.md)提醒技巧並給提示詞。 | 39分鐘收分析，未查清如實記錄。 |
| 39–44 | 5 | 技巧「把共識寫成檔案給Agent」。發[共同脈絡格式](../03-brownfield/participant/04-shared-context-template.md)，比較各人摘要、選主要Agent，由它寫`notes/shared-context.md`並複述。 | 核對共同事實、來源、分歧、限制與待決事項，42分鐘提醒收斂；尚未揭露B1，不核准任務修改。 | 44分鐘留`notes/shared-context.md`及角色；任務範圍、計畫與核准待揭露後由Agent寫進該段notes檔，不以口頭補充取代紀錄。 |
| 44–52 | 8 | 只發[B1任務](../03-brownfield/participant/task-cards/01-b1-student-fare-bug.md)；技巧「用失敗測試找Bug：重現→定位→最小修正→驗證」：Agent先重現並定位、寫進notes/b1.md，人核准最小修正計畫後才修改。 | 44–46重現與核准、46–49最小修正與變更審查、49停止擴充並用同一批測試證明修好；按[Brownfield三級提示](../03-brownfield/facilitator/05-task-progressive-hints.md)。 | 52分鐘停止；需接續時用已驗證B1 Recovery，原成果另留。 |
| 52–63 | 11 | 再發[B2任務](../03-brownfield/participant/task-cards/02-b2-discount-policy-change.md)；技巧「請Agent提2–3個方案並比較，人來選」，紀錄寫進notes/b2.md。 | 52–55 Agent比較2–3方案、人質疑假設並選擇核准；55–59分段實作與變更審查；59起測試／文件與交付，62提醒檢視逐人優惠與改票。 | 63分鐘停止；缺完成保留方案／Test Cases，按B2 Recovery接續。 |
| 63–76 | 13 | 技巧「委派整件任務：工作單＋三道關卡」。宣布到B3連核准方式也要變：人只透過三道Gate管Agent，發[B3任務](../03-brownfield/participant/task-cards/03-b3-group-booking.md)、[操作規則](../04-digital-worker/participant/01-operating-rules.md)、[Work Order](../04-digital-worker/participant/02-agent-work-order.md)與[Gate](../04-digital-worker/participant/03-approval-gates.md)。 | 四個檢查點：63交辦、66 Gate1、69 Gate2及唯一例外、70起實作（74停止擴充、75 Gate3）；看是否整份交工作單、只在Gate介入、`notes/b3.md`有決策原文與證據；Cue見下節。 | 76分鐘停止，Level1–3如實交付；人不補Code／Test。 |
| 76–80 | 4 | 技巧「請Agent整理交付摘要，人核對」：Agent依[Delivery](../04-digital-worker/participant/05-delivery-template.md)寫`notes/delivery.md`，每欄附證據；收表單與notes資料夾。 | 看學員是否追問「證據在哪」、未驗證如實標示；Recovery、風險與偏差，功能Level與治理證據分開。 | 80分鐘進回顧，不追加Demo美化或修Code。 |
| 80–90 | 10 | 技巧「把今天的技巧變成自己的提示詞清單」：發[提示詞清單](../05-retrospective/participant/reflection-sheet.md)與[Maturity](../05-retrospective/participant/maturity-comparison.md)。 | 按[Debrief](../05-retrospective/facilitator/debrief-guide.md)：每人3段提示詞進`notes/my-prompts.md`，小組討論盲點題與一項行動（責任人／驗證）。 | 90分鐘準時結束；未觀察不編數據，不排名。 |

總90分鐘；29–80共51分鐘，B3的13分鐘已包含治理，不新增另一段。原contents一日／半日與跨角色交接只作方法參考，Context交接映射到Time Skip及Shared Context。

## B3核准與唯一例外

相對0／1／3／6／7／11／12／13＝活動63／64／66／69／70／74／75／76。Gate1核准才設計，Gate2核准且條件解除才改程式；Gate3至少審實際測試及未完成。三Gate是學員決策，與素材驗收分開。

唯一`EXCEPTION-DW-001`依[主持事件卡](../04-digital-worker/facilitator/03-exception-injection.md)：若Agent已自然提SQLite不再注入；否則69分鐘用假設卡詢問，69–70最多60秒，必要縮30秒但不刪事件。不安裝SQLite，標準答案不預發Participant。未核准／未解除條件保持停止，不為趕時間假核准。

## 收件與復原

使用[評估索引](../05-retrospective/evaluation/workshop-evaluation-index.md)定位各段AC、提示、接受範圍與內部答案，勿分享該索引。保留版本、Context、Diff、測試指令／退出碼、Gate人員／時間、提示／介入、Recovery及未完成。

依[Recovery Plan](recovery-plan.md)只在時點發受控已驗收起點，未有合格包降級分析／Review。延遲不增加總90分鐘，不犧牲理解／設計Gate與最低交付Review。主持不得直接提供完整答案Code或替學員修改。

完成條件：十段完整執行紀錄、分批發放、Gate／例外／Recovery及成果與改善可追溯；本文件僅提供流程，實際90分鐘演練待執行。
