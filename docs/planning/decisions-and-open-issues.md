# 結構規劃決策與待協調事項

> 目標讀者：Repo 維護者、教材產製 Agent、工作坊負責人及驗收人員。
> 使用時機：確認資料夾方案、啟動各產製階段、調整規格或準備交付包之前。
> 前置條件：閱讀 [Agent 工作指引](../../Agent.md)、[總控指令書](../instructions/00_Agentic工作坊素材產製總控指令書.md) 及相關階段規格。
> 更新日期：2026-10-05。此文件只記錄規劃；未變更原始規格，也不代表下列建議已獲核准。

## 1. 如何使用本紀錄

P0–P4已完成，G0／G1程式與學員素材已有實測證據；G0→G1案例歷史以Evaluation Bundle保存。Brownfield、打包與真實演練仍屬後續工作。本機作者Repo Commit依使用者授權於目標收尾執行。

「已採用的規劃安排」是本次結構方案的安排；「待協調」表示仍須釐清規格或落實方法，不能以本文件取代核准。若建議涉及商業規則、測試預期、驗收門檻或原規格交付物變更，應先記錄決策、核准者及日期，更新受影響規格，再進入產製。尚未決定的事項不阻擋本次規劃文件完成，但應阻擋其對應階段的矛盾要求被直接實作。

本文件搭配 [資料夾結構](repository-structure.md) 與 [分階段產製路線](production-roadmap.md) 使用。

## 2. 已採用的規劃安排

| 編號 | 安排 | 來源與依據 | 影響與落地條件 |
|---|---|---|---|
| D-01 | 既有概念與產製規格留在 `docs/contents/`、`docs/instructions/`；規劃留在 `docs/planning/`；正式素材放在 `agentic-workshop/` | [總控 §6](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[Agent §4](../../Agent.md) | 維持規格來源單一，避免把指令書複製到學員包；後續依階段建立素材，P0 僅建立規劃文件；P1 進度另見本次適用紀錄。 |
| D-02 | 採 `00-governance` 至 `06-runbook` 主線，以及 `participant`、`facilitator`、`evaluation` 可見性分層 | [總控 §5.4、§6](../instructions/00_Agentic工作坊素材產製總控指令書.md) | 階段規格指定的詳細檔名與子目錄仍須保留；總控的概要樹不能用來省略階段交付物。 |
| D-03 | G0、G1、B0–B3 使用可獨立安裝、啟動及測試的版本目錄；演化順序固定 | [技術標準](../instructions/01_技術棧與Repository標準指令書.md)、[G1](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)、[B0](../instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[B1–B3](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md) | 每版有自身文件與驗證證據；獨立目錄不代表允許重建或偽造歷史，具體歷史策略見 O-05。 |
| D-04 | 交付包依受眾與階段使用允許清單；B1、B2、B3 任務分批發放 | [總控 §5.4](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[B1–B3 §28](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md)、[Agent §8](../../Agent.md) | 資料夾名稱不構成權限。學員不取得完整作者 Repo、Evaluation、主持提示或含未來答案的 Git 歷史。後續打包需驗證內容、引用連結與歷史可見性。 |
| D-05 | 後續驗證與打包工具集中於 `scripts/`，生成交付物集中於 `dist/` | [Agent §4、§8](../../Agent.md) 及本次結構方案 | 後續建立打包工具時才落實允許清單及排除 Git 追蹤；目前不建立腳本、交付包或修改 Git 設定。 |
| D-06 | 分階段產製並通過 Gate 後再往下：治理／技術 → G0 → G1 → Time Skip／B0 → B1–B3 → 治理素材整合 → 回顧／Runbook → 全域驗證與打包 | [總控](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[Agent §7](../../Agent.md) | B3 開始產製之前就須納入 Digital Worker 操作規則；後面的治理素材整合不是延後治理設計。缺少的階段規格須先補齊。 |
| D-07 | P12 主持簡報與學員 Runbook 放在 `agentic-workshop/materials/`，只存本機；學員只發一次檔案（單一 Runbook，內嵌 G0／B0），B0 與 Time Skip 之後的學員內容以編碼隱藏內嵌於 Runbook，用寫死的解鎖碼依揭露時點開啟；標準答案只放在主持簡報，於各段時間截止後揭曉；視覺參考台北富邦銀行官網風格（不使用標誌） | 使用者於 2026-10-05 對話中明確核准（已核准變更） | 取代 D-04 對學員「多包分批發放」的實體形式，但保留分批揭露的意圖：解鎖前原始碼不出現明文內容。編碼只防隨手偷看，不是密碼學保護；Runbook 不含 Evaluation 原稿；2026-10-05材料修正另允許兩份已驗收受控 Recovery ZIP，依52／63分鐘按需獨立碼提供，不以基線當小組成果；原始碼編碼只防隨手偷看。規格見 [P12 指令書](../instructions/10_主持簡報與學員Runbook產製指令書.md)。 |

## 3. 待協調的規格差異

### O-01：一日／半日時程與角色交接，和 90 分鐘主線不同

- **狀態與來源**：P10新素材已按總控完成90分鐘／角色的文件對齊，P10靜態驗證已通過，真實演練證據仍待P11；不宣稱整體已解除。[時程與主持指南 §1–2](../contents/08_時程安排與主持指南.md) 提供一日及半日安排；[角色分工](../contents/03_角色分工與治理原則.md) 與 [執行流程 Phase 5](../contents/05_工作坊執行流程.md) 採跨角色及跨 Session 交接。[總控 §1–2](../instructions/00_Agentic工作坊素材產製總控指令書.md) 固定 90 分鐘，且不採角色扮演型活動。
- **影響**：直接混用會使主持排程超時、角色配置不一致，亦可能把個人 Greenfield 及 Brownfield 的獨立分析／Shared Context 協作改為原本的角色輪轉。
- **建議**：本次規劃依總控的 90 分鐘演化主線安排；既有 `contents` 保留作概念來源。後續決定將一日／半日方案標示為延伸版，或更新成另附的活動格式；提取 Context、交接及 Review 的方法時，明確映射到本次活動，避免把額外活動列為必做。
- **處理階段／解除條件**：治理基線及主持時程設計之前。需明確指定本次版本適用時程、協作方式及可選活動，記錄核准與原始文件處理方式；最終 90 分鐘演練仍須另行驗證。

### O-02：通用完整 DoD 與 B3 學員成果分級不同

- **狀態與來源**：P10新素材已區分Reference完整DoD、學員Level1–3與治理觀察，P10靜態驗證已通過，真實活動評估證據仍待P11；不降低標準實作Gate。[成果物與驗收標準 §6–7](../contents/06_成果物與驗收標準.md) 要求程式完成、Acceptance Criteria 通過及交接驗證；[B1–B3 §27](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md) 因 B3 約 13 分鐘，接受 Level 1 分析完成、Level 2 核心流程完成及 Level 3 完整交付，且不只以 Level 3 判定工作坊成功。
- **影響**：若直接套用完整 DoD，Level 1／2 會被誤判為活動失敗；若反向降低全部驗收門檻，則可能交付不完整的 B3 標準實作。
- **建議**：區分「學員成果等級／治理觀察」、「可宣稱的程式交付完成」與「產製者 Reference Solution 驗收」。Level 1／2 如實列出未完成事項；只有達完整條件才能宣稱完整軟體交付。標準實作仍須符合全部 B3 Acceptance Criteria，不因學員分級而降低。
- **處理階段／解除條件**：治理 Acceptance Gates 定義時先釐清，B3 任務卡與 Evaluation 產製前完成。須建立適用對象與 DoD 對照，讓主持評分表、學員任務及標準答案共用一致定義；修改原規格須另有核准紀錄。

### O-03：`BOOKING-002` 對應不同規則

- **狀態與來源**：2026-10-05 P2 已完成編號對齊。[技術標準 §10](../instructions/01_技術棧與Repository標準指令書.md) 原將剩餘座位限制編為 `BOOKING-002`；[G0](../instructions/02_Greenfield_Starter_Kit產製指令書.md) 與 [G1](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md) 已完整定義002為最多4人、003為剩餘座位，現技術標準同步此映射。
- **影響**：同一 Rule ID 連到不同需求、測試及程式，破壞規則追溯；B3 的 5–20 人團體訂票又需要明確界定 4 人上限的適用情境。
- **處理與依據**：使用者要求啟動下一個目標（P2），在其已定義的編號協調範圍內沿用G0／G1詳細規格；屬文件識別對齊，不改商業語意、優惠、API或測試門檻，也不宣稱其他政策變更已核准。
- **完成證據／後續**：已建立[57項 Rule Registry](../../agentic-workshop/00-governance/rule-traceability-baseline.md)，同步技術標準、治理與Agent／規劃紀錄。002只限一般最多4人，B3團體採GROUP規則；舊座位限制引用映射003。後續實際Code／Test／Document仍待產製驗證，O-04–O-07不因此解除。

### O-04：B0 失敗数與G1 Regression（規格衝突已解除）

- **核准紀錄**：2026-10-05，使用者於具體提案後回覆「套用」，核准[方案A](b0-regression-gate-proposal.md)。原規格與治理、Agent／規劃同步完成。
- **原始衝突與證據**：B0原要求85%學生Bug、精確一項失敗且全部G1 Regression通過；不寫source的記憶體實驗為5 failed／23 passed／1已知Warning（0.28s）。實驗後原G1仍28passed（0.11s）。詳見提案五項影響矩陣。
- **採用規格**：僅BUG-B0-001一個Bug，保留全部28項G1測試與正確斷言。B0實測失敗node ID集合必須與已核實Intentional Failure Manifest完全一致，零非預期失敗；其餘通過、無Skip／XFail／未知Warning。不得任意將所有學生相關失敗歸類預期。
- **驗收責任**：B0產製時實測完整套件／Regression，並用Evaluation隔離診斷副本只修學生rate證明全部恢復；正式B0與clean-copy保留Bug。B1全部28項G1 Regression與B0新增測試均須通過。方案核准只解除規格矛盾，不宣稱B0／B1已驗收。
- **上下文邊界**：G1 fixture可適配原Seed／固定Clock／可選member與Seat ledger，完整B0上下文另測；不修改原業務斷言，不用fixture避開學生Bug。既有P4與先前階段紀錄保留為歷史證據。

### O-05：獨立版本目錄與真實 Git History／Tag 的關係

- **狀態與來源**：待落實版本策略。[G1 §15](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md) 建議 Commit 與 `g1-greenfield-reference` Tag，無法建立歷史時提供 `docs/commit-plan.md`；[B0 §18](../instructions/04_B0_Brownfield_Repository演化產製指令書.md) 在可建立 Repository 時要求延續 G1 History，並指定 `b0-brownfield-baseline`；[B1–B3](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md) 另指定各版本 Tag。
- **影響**：只有多份程式副本不能證明演化歷史；作者 Repo 的頂層 Tag 也不自動等於學員可用的案例 Repo 歷史。巢狀 Repository、作者 Repo、版本快照與交付包若關係不清，可能失去追溯或透過未來 Commit 洩漏答案。
- **建議**：後續在「案例演化 Repository → 固定 Commit／Tag → 匯出獨立目錄 → 驗證及交付包」的策略下定義單一權威來源，記錄每版來源及版本差異。需要真實歷史的 B0 學員包僅提供截至 B0 可見的安全歷史，並檢查 Branch、Tag 及其他可達 Commit；若無法建立真實歷史，按原規格產生並標示模擬歷史。具體保存位置、是否巢狀 Repository 及自動匯出方式尚未選定。
- **處理階段／解除條件**：G1 產製之前定案，B0 交付與最終打包再次驗證。需文件化來源、Tag 命名、版本對應、歷史保存與答案隔離策略，並依原規格驗證 G1 → B0 延續關係。案例歷史相關 Git 操作尚未執行，不聲稱案例 Commit／Tag 已存在；作者 Repo 文件提交另依收尾授權執行。

### O-06：B0 clean-copy 原規格與生成建議

- **狀態與來源**：原交付要求保留；生成方式待落實。[B0 §目錄結構](../instructions/04_B0_Brownfield_Repository演化產製指令書.md) 明定 `evaluation/reference-baseline/smart-ticket-b0-clean-copy/`。先前結構方案提出避免重複保存、由版本標記生成的想法，尚未核准為規格變更。
- **影響**：省略 clean-copy 會缺少原規格交付物；手動維護雙份程式則可能漂移，失去可靠的恢復與驗證基線。「clean」是乾淨的原始 B0 副本，不代表已修好學生票 Bug。
- **建議**：結構規劃保留 `agentic-workshop/03-brownfield/evaluation/reference-baseline/smart-ticket-b0-clean-copy/`。可於後續由同一固定 B0 來源產生此副本，核對檔案清單及雜湊、保留 B0 預期測試狀態；「不在作者 Repo 重複保存但仍在交付時生成」只是待審方案，不能直接取代原規格要求。
- **處理階段／解除條件**：B0 產製及驗收前。先明定副本來源、同步／生成時機及驗證方式；交付必須實際具備要求的副本。若要刪除或改變這項交付要求，必須先有明確核准並更新原規格。

### O-07：G1 含限制的通過與 B0 嚴格前置 Gate

- **狀態與來源**：待協調跨階段 Gate。[G1 §Validation Report、完成條件](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md) 允許 `PASS WITH DOCUMENTED LIMITATION`，完成條件可為 PASS 或只有不影響工作坊的已記錄限制；[B0 文件開頭使用時機](../instructions/04_B0_Brownfield_Repository演化產製指令書.md) 則明定 G1 完成且 Validation Report 為 PASS。
- **影響**：G1 本階段可交付不代表已符合 B0 啟動條件。忽略差異可能讓未解除的限制進入 B0，造成後續測試與交付風險。
- **建議**：規劃暫按 B0 較嚴格的前置條件執行。含限制的 G1 需先處理限制並重新驗證達 PASS，或正式釐清及核准跨階段 Gate 變更；不直接把含限制通過視為等同 PASS。
- **處理階段／解除條件**：G1 驗收與 B0 啟動之前。須有符合原規格的 G1 PASS 報告，或明確核准且同步更新兩份規格的替代 Gate，並留存限制對 B0 的影響評估。

## 4. 決策更新方式

### 2026-10-05 P6 正式B1驗收紀錄

正式B1從已驗收B0快照与案例歷史建立，不使用P5診斷副本冒充。商業邏輯僅學生率85→75一行，其餘變更為App／套件版本与README／history識別；全部13測試檔、原DiscountPolicy及其餘業務文件未變。

獨立Python3.13.15環境安裝與pip check成功，44passed／1已知相容Warning（1.00s），原28G1与16新增均通過、五Manifest失敗全恢復，學生525／混合1225与完整API Smoke通過。B0原52檔SHA256仍一致。B1 Tag a1c1d45續B0，Bundle／Clone／52檔快照比對通過；Task卡不泄解答，B2／B3未產製。

個別Gate PASS，不判定B1–B3整體 `PASS FOR WORKSHOP USE`。詳見[B1正式驗證](../../agentic-workshop/03-brownfield/evaluation/12-b1-validation-report.md)。O-04核准及B1全部恢復要求已有正式驗收證據；普通工程師8分鐘與全90分鐘演練仍待執行。

### 2026-10-05 P5 B0 實際驗收紀錄

- O-04：已依核准方案A實測，正式44項套件5failed／39passed与完整manifest node集合相等，零非預期；僅修學生率一行的Evaluation隔離副本44passed。原28G1測試body／assert比對一致，B1正式版本仍待產製。
- O-05：B0從G1案例歷史自然延續，Tag `b0-brownfield-baseline=392d920`，Bundle verify／Clone／G1祖先与52檔快照比對通過；所有10可達Commit截至G0／G1／B0，無未來解答或診斷修復Commit。
- O-06：原要求 `reference-baseline/smart-ticket-b0-clean-copy/` 已實際建立，從同一正式B0來源複製；52檔雙向清單、內容与SHA256一致，保留Bug。後續由固定版本來源重新生成並比對，不手動維護兩份不同基線。
- O-07：既有G1 PASS前置維持，本次B0決策為PASS AS BROWNFIELD BASELINE，正式pytest exit1仍如實揭露；不混用一般全綠或G1含限制通過。
- 詳見[B0驗證](../../agentic-workshop/03-brownfield/evaluation/01-b0-validation-report.md)、[來源與副本](../../agentic-workshop/03-brownfield/evaluation/05-case-history-and-copy-evidence.md)。本機啟動／測試時間已量測，但普通工程師3／5／8分鐘與完整90分鐘真實演練尚未執行，留待後續階段。

### 2026-10-05 P4 落實紀錄

- **O-05：G0／G1已落實，後续延續待驗證。** 在使用者授權P4範圍內採純實作策略：獨立案例Repo→真實Commit／Tag→Evaluation限定Bundle→獨立版本快照。`g0-starter=ee5c126`、`g1-greenfield-reference=361bf00`；Bundle驗證、Clone與30檔內容比對0差異。共五個實際提交，明示是本次按成果階段組裝歷史，不虛構過去開發時程。詳見[G1 Case History](../../agentic-workshop/01-greenfield/evaluation/reference-solution/greenfield-reference-mvp/docs/case-history.md)。B0必須承接G1祖先並另驗證安全可見歷史；尚未聲稱B0或學員包已存在。
- **O-07：G1前置條件已滿足。** [G1報告](../../agentic-workshop/01-greenfield/evaluation/04-g1-validation-report.md)為PASS：28passed／無Skip／XFail，僅規格允許且已記錄的第三方相容Warning。未修改原Gate；本次案例固定邊界不代表未完成功能。
- **O-04：仍阻擋B0 Bug注入，已有具體影響清單。** 75%改85%會破壞五项G1測試：`test_student_fare_is_seventy_five_percent`、`test_mixed_passenger_fares_sum_as_integers`、`test_successful_mixed_booking_reserves_seats_and_starts_pending`、`test_student_booking`、`test_mixed_booking_reserves_seats`。525→595、1225→1295；不得弱化這些Regression以湊一項失敗。此為實作路徑與斷言盤點，尚未注入B0 Bug或取得B0測試結果。
- **O-06：保留原交付要求，待B0實際生成及比對。** O-01／O-02的後續教材對齊与真實時間演練仍未完成。

後續每次解除待協調事項，記錄決策日期、決策者／核准者、採納方案、受影響文件與驗證證據；保留未採納建議的狀態，不把「已提出」寫成「已核准」。純實作方式的選擇可依授權範圍落實；原規格變更則遵守明確核准要求。

## 5. P1 治理基線的適用紀錄

2026-10-05：已在 [Manifest](../../agentic-workshop/00-governance/workshop-manifest.md)、[一致性規則](../../agentic-workshop/00-governance/consistency-rules.md) 與 [Acceptance Gates](../../agentic-workshop/00-governance/acceptance-gates.md) 界定本次活動與驗收對象。此紀錄是既有上位及階段規格的適用解釋，不是原規格變更核准。

- O-01：本次採總控固定的 90 分鐘與個人→混合小組主線；一日／半日、角色輪轉保留作方法參考。後續 Runbook 對齊與演練仍待執行。
- O-02：學員 Level 1／2 可構成學習成果，完整軟體交付與 Reference 仍須完整證據。後續 B3 任務與評估表需沿用此區分，未降低標準實作門檻。
- O-03–O-07：保留原狀態與解除條件；治理文件中明確指出對應階段阻擋條件。未建立程式或案例歷史，未取得測試或副本一致性證據。

本次未修改 `docs/contents/`、`docs/instructions/` 原規格；僅產製內部治理文件、同步規劃與 `Agent.md`。學員任務卡、程式、交付包及驗證腳本未建立。

## 6. P2 技術文件基線紀錄

2026-10-05：依使用者「開始下一個目標，8分鐘內完成」推進 P2；建立技術、57項規則追溯與版本驗證文件，技術標準 §10 與 G0／G1 對齊。O-03 的文件編號衝突已處理，不改商業限制；O-04–O-07 保留未解除。此次修改技術標準與相關治理／規劃紀錄，沒有建立程式、安裝依賴或取得 Runtime 證據。後續 G0 應實際補上 Code／Test／Document 追溯。

## 完成條件

2026-10-05 P3已核准變更：使用者明確允許Python3.13或3.14，採3.13統一基線並同步技術標準、治理與規劃；不是自行放寬版本。G0實際環境3.13.15與驗證結果留在Evaluation報告，原商業規則及O-04–O-07狀態不變。

- 結構安排與尚未核准的規格變更有清楚區別。
- 每項待協調事項具備真實來源連結、影響、建議、處理階段與解除條件。
- 時程／角色、B3 分級 DoD、Rule ID、B0 測試衝突、歷史策略、clean-copy 與 G1 → B0 Gate 均有紀錄。
- 原規格交付要求未因規劃建議而被默默省略；未宣稱任何尚未執行的程式、Git 或驗證成果。
- 可供後續產製者判斷各階段啟動前須處理的事項；待協調項目保留不代表本次規劃未完成。

### 2026-10-05 P7 B2產製與實測驗收紀錄

2026-10-05 P7 B2實測完成、個別B2 Gate PASS：獨立Python3.13.15環境依賴安裝成功，55 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（1.21s）。Health／11個OpenAPI路徑、企業＋提前混合成人595／學生525／Total1120、付款、改票至T005新價1199／差額79、退票、通知3／Audit4及Reset Smoke通過。B1原52檔雜湊不變；B2快照54檔，保留原28項G1正確斷言，原13測試檔只有test_advance政策案例遷移，新增11項B2測試。逐旅客最低rate、不疊加、Applied Discounts、改票共用政策與折扣文件同步；TASK-B2-001、13項AC及主持材料已建立。案例Tag `b2-best-single-discount`與Bundle已驗證：14個真實Commit，54檔Clone比對零差異，B1為祖先且無B3歷史。詳見 [B2 Validation Report](../../agentic-workshop/03-brownfield/evaluation/15-b2-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/16-b2-validation-evidence.json) 與 [案例歷史／Delta](../../agentic-workshop/03-brownfield/evaluation/17-b2-case-history-and-delta.md)。此為P7當時範圍與證據；目前B3與B1–B3素材驗收見下方P8紀錄，真實演練及最終交付仍待完成。

本次依既有B2規格實作，沒有核准新商業規則或放寬測試門檻；原B0/B1歷史證據保留，原正確斷言與13份測試來源已核對；原28項G1保持不變，只有test_advance的舊政策案例按B2政策遷移。

2026-10-05 P8正式B3已產製並實測，個別Gate PASS：獨立Python3.13.15環境安裝成功，75 passed／0 failed／0 Skip／0 XFail，1項既有BlockingPortal相容Warning（0.58s），55原案例＋20團體新增。Import／Health／13個OpenAPI路徑／Uvicorn Health（2.17s）及Smoke通過：5人混合團體總價2905（學生75%、成人提前85%）、同車廂連續、成功唯一Order、已付款退票、付款失敗CANCELLED／全釋放／無Order、Audit2／通知1與Reset。57規則、19項AC、三Gate、任務卡與主持節奏齊備；案例Tag b3-group-booking=`ca3e5de7adca290f555d9ab96f322f65345b3e90`；Bundle73,670 bytes、17個真實Commit，Clone59來源檔比對零差異；B2來源54檔雜湊凍結、原55案例對應15測試檔字節一致。B1–B3標準素材Final Decision為PASS FOR WORKSHOP USE，僅代表三版標準實作素材；不代表P9完整Operating Rules／Work Order／治理模板、13分鐘或90分鐘真實演練、打包與正式交付已完成。這是P8當時的範圍界線；目前P9狀態見後續紀錄。

詳見 [B3 Validation Report](../../agentic-workshop/03-brownfield/evaluation/18-b3-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/19-b3-validation-evidence.json)、[案例歷史／Delta](../../agentic-workshop/03-brownfield/evaluation/20-b3-case-history-and-delta.md) 與 [B1–B3素材驗收](../../agentic-workshop/03-brownfield/evaluation/21-b1-b3-production-result.md)。

2026-10-05 P9治理文件基線完成，Final Decision為PASS FOR GOVERNED DIGITAL WORKER EXERCISE：15份規定輸出加追溯／驗證報告／證據共18份（17 Markdown＋1 JSON）。17份Markdown的40個相對連結有效、UTF-8無BOM、Code Fences平衡；Participant無答案或內部越界連結。唯一EXCEPTION-DW-001、Work Order17項Group Rule與B3精確相等、Work Order11／Delivery12／Audit13個規定欄位均符合；Operating Rules約384個中文字。B3原59來源檔SHA256全部不變。獨立審查22項指令映射、三人員Gate及時程一致，無阻擋問題。此PASS只涵蓋治理文件一致性及時程設計，不等於學員Gate1／2／3已實際核准；兩分鐘閱讀、13分鐘活動與60秒例外尚未真實演練，Rehearsal／Package為NOT RUN。此為P9當時範圍，P10目前進度見後續紀錄；P11全域驗證與交付包未完成。

證據依[P9 Governance Validation Report](../../agentic-workshop/04-digital-worker/evaluation/06-governance-validation-report.md)核對，判定及實際靜態結果已核對；真實演練與打包仍未執行。

2026-10-05 P10主持／回顧文件基線PASS：新07指令整合既有要求；11份輸出為10 Markdown＋1 JSON（回顧學員2／主持2／評估索引1、Runbook4、Validation Report及證據JSON）。10份Markdown的131個相對連結有效、UTF-8無BOM、Code Fences平衡，Participant無答案或越界內部連結。主流程十段連續且無重疊加總90分鐘；Time Skip至Brownfield交付51分鐘、B3 13分鐘、回顧10分鐘；唯一EXCEPTION-DW-001包含於69–70分鐘。B3原59來源檔與P9原17份Markdown雜湊不變。O-01時程／角色及O-02完整Reference DoD／學員Level在新文件對齊；此PASS僅文件一致性與時程設計，不以空Preflight表當已執行證據。實際Preflight、真人90分鐘／13分鐘演練、Recovery演練與受控包生成均NOT RUN；O-01／O-02的演練解除證據仍待P11。下一階段P11全域驗證、受控打包與真人演練未啟動。

來源與已核對的文件驗證證據：[P10產製指令](../instructions/07_主持Runbook與回顧整合產製指令書.md)；[P10 Validation Report](../../agentic-workshop/06-runbook/evaluation/p10-validation-report.md)。

### P10 O-01／O-02適用範圍與解除條件

O-01新素材採十段90分鐘、Greenfield個人、Time Skip統一B0、個人分析→Shared Context→主要Agent執行；原contents一日／半日與跨角色流程保留參考，不列本版必做。O-02新回顧表、成熟度比較與評估索引區分學員Level、治理證據與完整Reference驗收，Recovery不算原小組完成。來源為07指令、[Runbook](../../agentic-workshop/06-runbook/workshop-runbook.md)、[回顧](../../agentic-workshop/05-retrospective/facilitator/debrief-guide.md)、[評估索引](../../agentic-workshop/05-retrospective/evaluation/workshop-evaluation-index.md)。文件對齊已通過本輪靜態查核；實際90分鐘、13分鐘任務及Recovery可行性仍須P11真人演練與發放隔離證據，不以文件完成完全解除。

## P11 本輪執行狀態

2026-10-05 使用者「進入下一個目標」啟動P11，並選擇本次安排真人演練。六版本輪pip check、pytest、API Smoke與實際Uvicorn Health／OpenAPI通過；G0為1pass／8受控skip，G1為28pass，B0為39pass／5精確Manifest失敗，B1／B2／B3為44／55／75pass。已生成13份受控候選ZIP，B1／B2解壓Recovery副本44／55測試與Smoke通過；使用既有獨立venv，未宣稱新安裝。候選包以最終白名單／Hash與本輪報告為準；真人演練人員、時段與記錄者尚待提供，未執行90分鐘活動。P10及先前紀錄中的未啟動／未打包均為當時狀態，不作本輪結果。P11整體與正式發布仍待驗收；O-01／O-02真人證據解除條件保留。

依據：[P11指令](../instructions/08_全域驗證與受控打包產製指令書.md)；[本輪驗證報告](../../agentic-workshop/06-runbook/evaluation/p11-validation-report.md)。

## 一致性審查後的優先修正

2026-10-05 使用者要求設為新目標並優先處理審查發現。先前候選360cb551f76eeb73的清單／Hash／連結與Recovery技術通過不涵蓋教學語意；該包已停止用於本次演練。修正初始B0答案洩漏、恢復兩份受控落差與三份安全ADR，並對齊任務揭露、Level1交付、Recovery、B2合約勘誤、Mission／空白例外卡發放與歷史狀態。凍結程式／測試／案例來源保持，P9／P10歷史JSON不改寫。新候選與實際驗證以本輪報告為準；真人演練及正式放行仍待驗收，O-01／O-02真人證據解除條件保留。

依據：[修正指令](../instructions/09_教材一致性修正與交付重驗指令書.md)；[一致性修正報告](../../agentic-workshop/06-runbook/evaluation/consistency-correction-report.md)。

## 來源漂移後改以行為為基準

2026-10-08 主課候選 `c841f2424d256c28` 無法重建：Manifest 釘選的位元組混用 CRLF／LF，且部分來源已修訂；B0–B3 原驗收證據的來源雜湊亦不符。以 uv 建立六版環境完整執行，G0 1 pass／8 skip、G1 28、B0 39 pass／5 精確失敗、B1 44、B2 55、B3 75 與 Health／OpenAPI 全部符合原門檻。使用者決定調整規範而非回復舊位元組：凍結改以行為驗證為準，最新完整驗證即來源基準，來源可修改但須重驗與重新釘選，Manifest 來源不轉換換行。

依據：[08 指令書規範調整](../instructions/08_全域驗證與受控打包產製指令書.md#2026-10-08-規範調整來源漂移後的基準)；[完整驗證證據](../../agentic-workshop/06-runbook/evaluation/p11-validation-evidence.json)。

## 技巧優先、紀錄交給 Agent

2026-10-09 使用者實讀 Runbook 後回饋：Brownfield 看不出「現在在做什麼」、表單太多、沒學到 Agentic Coding 技巧。實測 29–63 分共 13 張表單、86 個欄位。使用者核准「技巧優先，紀錄交給 Agent」並直接全面改版：目標順序改為技巧 → SDLC 體驗 → 組織導入；每段頁首加「現在在做什麼」卡並標示技巧；檢查點每段最多 3 個（Greenfield、B3 最多 4 個）；表單每段最多一張、最多 4 欄；分析、計畫、審查答案由 Agent 寫進 `notes/<段落>.md`。解鎖碼、時程、Gate、Level 定義、例外事件、程式與測試不變。

依據：[總控指令書目標順序](../instructions/00_Agentic工作坊素材產製總控指令書.md#1-專案目標)。
