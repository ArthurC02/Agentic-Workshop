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

| 編號 | 安排 | 來源與依據 | 影響與實施條件 |
|---|---|---|---|
| D-01 | 既有概念與產製規格留在 `docs/contents/`、`docs/instructions/`；規劃留在 `docs/planning/`；正式素材放在 `agentic-workshop/` | [總控 §6](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[Agent §4](../../Agent.md) | 維持規格來源單一，避免把指令書複製到學員包；後續依階段建立素材，P0 僅建立規劃文件；P1 進度另見本次適用紀錄。 |
| D-02 | 採 `00-governance` 至 `06-runbook` 主線，以及 `participant`、`facilitator`、`evaluation` 可見性分層 | [總控 §5.4、§6](../instructions/00_Agentic工作坊素材產製總控指令書.md) | 階段規格指定的詳細檔名與子目錄仍須保留；總控的概要樹不能用來省略階段交付物。 |
| D-03 | G0、G1、B0–B3 使用可獨立安裝、啟動及測試的版本目錄；演化順序固定 | [技術標準](../instructions/01_技術棧與Repository標準指令書.md)、[G1](../instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)、[B0](../instructions/04_B0_Brownfield_Repository演化產製指令書.md)、[B1–B3](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md) | 每版有自身文件與驗證證據；獨立目錄不代表允許重建或偽造歷史，具體歷史策略見 O-05。 |
| D-04 | 交付包依受眾與階段使用允許清單；B1、B2、B3 任務分批發放 | [總控 §5.4](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[B1–B3 §28](../instructions/05_Brownfield任務卡與B1-B3產製指令書.md)、[Agent §8](../../Agent.md) | 資料夾名稱不構成權限。學員不取得完整作者 Repo、Evaluation、主持提示或含未來答案的 Git 歷史。後續打包需驗證內容、引用連結與歷史可見性。 |
| D-05 | 後續驗證與打包工具集中於 `scripts/`，生成交付物集中於 `dist/` | [Agent §4、§8](../../Agent.md) 及本次結構方案 | 後續建立打包工具時才落實允許清單及排除 Git 追蹤；目前不建立腳本、交付包或修改 Git 設定。 |
| D-06 | 分階段產製並通過 Gate 後再往下：治理／技術 → G0 → G1 → Time Skip／B0 → B1–B3 → 治理素材整合 → 回顧／Runbook → 全域驗證與打包 | [總控](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[Agent §7](../../Agent.md) | B3 開始產製之前就須納入 Digital Worker 操作規則；後面的治理素材整合不是延後治理設計。缺少的階段規格須先補齊。 |
| D-07 | P12 主持簡報與學員 Runbook 放在 `agentic-workshop/materials/`，只存本機；學員只發一次檔案（單一 Runbook，內嵌 G0／B0），B0 與 Time Skip 之後的學員內容以編碼隱藏內嵌於 Runbook，用寫死的解鎖碼依揭露時點開啟；標準答案只放在主持簡報，於各段時間截止後揭曉；視覺參考台北富邦銀行官網風格（不使用標誌） | 使用者於 2026-10-05 對話中明確核准（已核准變更） | 取代 D-04 對學員「多包分批發放」的實體形式，但保留分批揭露的意圖：解鎖前原始碼不出現明文內容。編碼只防隨手偷看，不是密碼學保護；Runbook 不含 Evaluation 原稿；2026-10-05材料修正另允許兩份已驗收受控 Recovery ZIP，依52／63分鐘視需要獨立碼提供，不以基線當小組成果；原始碼編碼只防隨手偷看。規格見 [P12 指令書](../instructions/10_主持簡報與學員Runbook產製指令書.md)。 |

## 3. 待協調的規格差異

### O-01：一日／半日時程與角色交接，和 90 分鐘主線不同

- **狀態與來源**：P10新素材已按總控完成90分鐘／角色的文件對齊，P10靜態驗證已通過，真實演練證據仍待P11；不宣稱整體已解除。[時程與主持指南 §1–2](../contents/08_時程安排與主持指南.md) 提供一日及半日安排；[角色分工](../contents/03_角色分工與治理原則.md) 與 [執行流程 Phase 5](../contents/05_工作坊執行流程.md) 採跨角色及跨 Session 交接（2026-10-09 註：上述三份 contents 已改寫為現行 90 分鐘設計，一日／半日安排、PO／QA 等角色與 Phase 5 已刪除）。[總控 §1–2](../instructions/00_Agentic工作坊素材產製總控指令書.md) 固定 90 分鐘，且不採角色扮演型活動。
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

### O-04：B0 失敗數與G1 Regression（規格衝突已解除）

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

- **O-05：G0／G1已落實，後續延續待驗證。** 在使用者授權P4範圍內採純實作策略：獨立案例Repo→真實Commit／Tag→Evaluation限定Bundle→獨立版本快照。`g0-starter=ee5c126`、`g1-greenfield-reference=361bf00`；Bundle驗證、Clone與30檔內容比對0差異。共五個實際提交，明示是本次按成果階段組裝歷史，不虛構過去開發時程。詳見[G1 Case History](../../agentic-workshop/01-greenfield/evaluation/reference-solution/greenfield-reference-mvp/docs/case-history.md)。B0必須承接G1祖先並另驗證安全可見歷史；尚未聲稱B0或學員包已存在。
- **O-07：G1前置條件已滿足。** [G1報告](../../agentic-workshop/01-greenfield/evaluation/04-g1-validation-report.md)為PASS：28passed／無Skip／XFail，僅規格允許且已記錄的第三方相容Warning。未修改原Gate；本次案例固定邊界不代表未完成功能。
- **O-04：仍阻擋B0 Bug注入，已有具體影響清單。** 75%改85%會破壞五項G1測試：`test_student_fare_is_seventy_five_percent`、`test_mixed_passenger_fares_sum_as_integers`、`test_successful_mixed_booking_reserves_seats_and_starts_pending`、`test_student_booking`、`test_mixed_booking_reserves_seats`。525→595、1225→1295；不得弱化這些Regression以湊一項失敗。此為實作路徑與斷言盤點，尚未注入B0 Bug或取得B0測試結果。
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

## 複製提示詞即可通關（主課與 DLC）

2026-10-09 使用者要求：學員複製 Prompt 就能逐步通關並學到技巧；可提醒討論但不要大量表格；盡量減少手動輸入，多給指示與說明；主課與 DLC 同一標準；修改時刪除不再需要或矛盾的內容。DLC 原本由學員自行輸入 Plugin 指令並填寫每段約 6 張表單，改為 Agent 依提示詞執行指令、學員以短回覆決定；D2 核准仍由夥伴本人在自己開的 Agent 對話中簽章（同一台電腦，因 D3 沿用同一 Repo 與 Maintainer 金鑰）。

依據：[總控指令書設計規則](../instructions/00_Agentic工作坊素材產製總控指令書.md#1-專案目標)；DLC 指令書（11）第 1 節第 8 點。

## 主課埋入六項 Agentic Coding 技巧

2026-10-09 使用者要求主課帶到 Skill、Token 節費、Prompt、Structured Output、模型選擇與推論強度，埋入任務協助學員解題，並體會三階段所需技巧。做法：不加時間與檢查點；Greenfield（Tool）練 Prompt 結構、結構化輸出、推論強度；Time Skip 到共同脈絡（Teammate）練 Token 節費、模型選擇並建立 `skills/team-rules.md`；B1／B2 用 Skill 與結構化方案比較；B3（Digital Worker）以 Work Order 當 Skill、Gate 回報用固定格式、自主執行選較強模型並控管 Token。維持工具中立：通用概念描述，工具功能僅作選用。

依據：[總控指令書 2.2 工具中立](../instructions/00_Agentic工作坊素材產製總控指令書.md#22-工具中立)。

## 由淺入深、知識點於首次需要處介紹

2026-10-09 使用者要求：工作坊以由淺入深引導為核心，新知識點必須在真正需要處出現並附官方資訊引導，不得要求學員使用未介紹過的知識點。做法：依 Runbook 順序稽核「首次介紹 vs 首次使用」，開場只留路線圖，完整說明搬到首次使用處；技巧類 callout 附「延伸閱讀」出處名稱（多家廠商官方文件、DDD 經典書目、Plugin 自帶說明），因安全檢查禁止學員頁外部網址，只列名稱不列網址。主課與 DLC 都適用。

## 實跑演練（rehearsal）與 DLC 工具修正授權

2026-10-09 以候選包實跑主課與 DLC 開場～D2 提示詞（`.claude/skills/rehearsal`），依結果修正教材。DLC 工具原屬不修改範圍；使用者授權調整後修正：工具說明與 `--help` 路徑改為 `../../tools/`（實際相對 Repo 根目錄）、`dm.sh` 在 py launcher 沒有 3.13 時改用 python3、`write_scm_attestation.py` 的下一步提示標明 finalize-proposal 由提案者執行。程式庫（repository）與 recovery bundle 內的 README 未改。

未驗證：D2 檢查點 6 夥伴的 `git push`（演練環境安全檢查擋下本機 bare repo 推送），需在實機補跑一次。

## 程式包修正授權（2026-10-09）

使用者授權「全部修復」原本鎖定的程式包問題，並授權 Commit 與 Push：Greenfield／B0／參考解答 README 的虛擬環境啟用說明（Windows Git Bash 路徑錯誤）、Brownfield Recovery 包補齊 docs（ADR、改票指南、優惠說明、API 範例）、DLC 程式庫與 Recovery bundle 統一 LF 行尾並鎖定 anyio 版本以消除 DeprecationWarning。修正後重新量測頁面引用的數字並以候選包實跑驗證。D2 檢查點 6 夥伴推送改在沙箱內推送到本機 bare repo 驗證。

結果與已知限制：DLC 起始 Repo 改 LF、釘選 anyio 4.9.0／starlette 0.46.2；`make_recovery.py` 重建 d1–d3c（d3 參考實作疊加時保留每個檔案原本的行尾，d3c verify-evidence 由 93／69 變為 99／63），D2 Recovery 新增選做的 push 檢查（步驟 4）。d2 Recovery 與 d2／d3 的 Registry 歷史來自 Maintainer 已簽章的 bundle，改行尾或釘選需要原私鑰重簽，維持原樣（d2 Recovery 可能出現一個無害的 DeprecationWarning）。

## domain-memory Plugin 升級 0.10.15（2026-10-10）

由 0.2.2 升級到 0.10.15。相容性評估：沒有移除或改名的指令與參數、預設值不變；簽章的參考 Registry、d1–d3c Recovery 與 D1→D2 全流程在兩版結果一致；頁面引用的輸出字串都還在。帶來的修正：Plugin 寫檔改 LF、OneDrive 唯讀資料夾不再讓 apply 失敗、檔案系統錯誤只印一行 ERROR、scan-secrets 讀不到檔案時不再中斷、核准證明必須對應同一個 Change Package。學員包只放執行用的檔案：依 Plugin README 排除 `evals/`、`scripts/test_*.py` 與開發用的 `README.md`、`ruff.toml`（由 `scripts/vendor_dlc_plugin.py` 產生，70 個檔案、`SHA OK 71 files`；0.2.2 是 129 個檔案）。另外撤回起始 Repo `.gitignore` 的 `records/`：被忽略的路徑會讓 `git add -A -- . ':!records'` 結束碼為 1。

## domain-memory 0.16.0：暫不升級（2026-10-12）

評估 0.10.15 → 0.16.0（在暫存沙箱用兩版實跑 D1、D2 全流程與 Recovery）。沒有指令、參數或輸出字串被移除，但 0.11 起 `validate` 會檢查 `synonyms`／`not_same_as`，而課程的已簽章參考 Registry 有兩筆在新版不合格（`discount-rate` 的同義詞重複、`best-single-discount` 的 `not_same_as` 指向非詞彙 id），連帶 d1–d3c Recovery 與三份參考解答的 `validate` 都會失敗；D1 檢查點 3 的「互加 not_same_as」在 `make_record.py` 逐筆登記時也會失敗。

決定：維持 0.10.15。理由：0.15／0.16 是當天發布、尚未經過穩定期；升級需重簽參考資料、重建全部 Recovery 與參考解答並重新演練（約一個工作天），而學員用得到的功能沒有增加。教材目前與 0.10.15 一致（例如 resolve-terms「不比對同義詞」在 0.10.15 為真）。先做一項兩版都正確的修正：D1 檢查點 3 提示詞註明 `not_same_as` 填對方那筆的 id、別名不可重複或與詞彙名稱相同。

升級時的工作清單（下一次交付前、且新版已穩定一段時間再做）：
- 資料：修正 `reference-registry/inputs/d1-records.json` 兩筆；以 CP-CORE-002 取代 CP-CORE-001（需新增授權簽章者）；重跑 `make_recovery.py d1 d2 d3a d3b d3c`、重產參考解答並更新數字。
- 工具：`make_record.py` 改為每個資產一次批次 upsert；`50-d3c.md` 的「批次在第一個錯誤停下」改為「同一資產全部登記或全部不登記」。
- 機械：`vendor_dlc_plugin.py` 重產 ZIP 並刪除舊版；版本字串（build_delivery_dlc、dmlib、doctor、README、指令書）；`SHA OK 73 files`。
- 內容：resolve-terms 會比對同義詞並標示 `match_kind`（10-d1 檢查點 5、30-d3a、20-d1 投影備註、tools/README）。可選加深：D1 檢查點 5 的別名比對、D3a 檢查點 5 的 Contract `idempotency`；D4 檢查點 2 的 `relocate-evidence` 需先向 Plugin 作者確認 `--from src --to src` 是支援的用法。不教：`boundary-impact`、`unhashed`。
- 之後跑 release-materials 並演練 D1、D2、D4。

## domain-memory 0.22.0：仍暫不升級（2026-10-14）

評估 0.10.15 → 0.22.0（暫存沙箱用兩版實跑 D1 重播、D2–D3c Recovery 接手、簽章 commit、push、`validate --require-reviewed`、`verify-audit`、`verify-evidence`、`verify-sources`、`quality-gates`，另比對指令參數與頁面引用的輸出字串）。指令、參數、預設值與頁面引用的成功字串都沒有變，D2 Change Package 流程（`fill_package.py`）在新版也是 `Change package is valid.`。阻擋點與 0.16.0 相同：兩筆詞彙資料讓 9 份 Registry 的 `validate` 失敗；修好資料後，D1 重播仍停在互標 `not_same_as` 的 `advance-purchase-discount`（逐筆 upsert）。

決定：維持 0.10.15，教材不為 Plugin 改版而改。理由：0.16–0.22 在兩天內連發 7 版，尚未穩定；升級成本與 2026-10-12 的清單相同，且 D4 需要改寫。

新版對課程的影響（補充 2026-10-12 的工作清單）：
- D4 受益最大：行號只是移動的引用改報 `shifted`、不算失敗；`verify-evidence` 每筆附 asset、id 與 `cited_lines`。實測 current／shifted／stale：d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（0.10.15 為 147／15、108／54、99／63）。升級時要改：`39/49/59-recovery-*.md` 的數字、`60-d4.md` 檢查點 2（不必再從 `notes/` 反查 id；「只是行號移動而 stale」改為 `shifted`）、詞彙表的狀態列與主持指南。`relocate-evidence --from . --to .` 自 0.20.1 起涵蓋整個 Repo，同一路徑會重新引用 shifted 的證據，可取代 2026-10-12 清單中「先向 Plugin 作者確認」那一項。
- `resolve-terms`：0.19 起查不到詞彙時回傳非權威的 `mentioned`（不一定是 `[]`），0.20 起只比對完整單字；`10-d1.md`、`30-d3a.md`、`40-d3b.md`、`50-d3c.md` 對 `[]` 的說明要一併改。
- pre-push hook：0.21.1 起先找 `python3` 再找 `python`。實測 0.10.15 的 hook 在 PATH 沒有裸 `python` 時 push 失敗（`python: not found`）；Runbook 的 push 步驟都先啟用 `.venv`，所以目前學員不會遇到，升級後可刪去相關提醒（`20-d2.md`、`tools/README.md`、主持指南常見問題第 4 條）。
- `dmlib.py` 的指令集合未包含 0.14 起新增的 `boundary-impact`、`recite`、`relocate-evidence`（都需要兩個 root），D4 若教 `relocate-evidence` 要一併加入。

同時修正一處兩版都不對的說明：`30-d3a.md` 延伸閱讀原寫 `pattern-verification.md`「最後一段講反事實檢查」，實際在〈Evidence matrix〉一段的最後一列（最後一段是〈Review outcome〉）。

## domain-memory 升級 0.22.0（2026-10-15）

使用者核准升級，固定在 0.22.0（SkillHub `bdd994626`，與目前 HEAD 的 Plugin 內容相同）。

做了什麼：
- 機械：`vendor_dlc_plugin.py` 產生 `domain-memory-0.22.0.zip`（72 個 Plugin 檔案；學員核對印出 `SHA OK 73 files`，含 ZIP 本身），刪除 0.10.15 的 ZIP 與 SHA256SUMS；版本字串與檔案數同步到 build_delivery_dlc（含測試）、dmlib、doctor、tools／DLC README、01-environment、開場投影片、主持指南、觀察指南與 11 號指令書。`dmlib.py` 的指令集合改成與 0.22.0 的 `cli_parser` 完全一致（補上 `attest-signed-commit`、`audit-attestations`、`boundary-impact`、`promote-candidate`、`recite`、`record-test-result`、`recover-registry-update`、`relocate-evidence`、`validate-change-package` 缺的固定參數）。
- 工具：`make_record.py --upsert` 改為每種資產一次 `upsert-candidate`（依 ASSETS 順序），互標 `not_same_as` 的兩筆才能一起登記；同一種資產全部登記或全部不登記（實測：規則批次裡有一筆 reviewed id 時，同批新規則也不登記，之前的種類已登記、之後的種類停下）。`test_tools.py` 加了互標 `not_same_as` 的一對詞彙，舊版逐筆 upsert 會失敗。`doctor.py` 改用與 hook 相同的規則檢查 PATH 上的 `python3`／`python` ≥ 3.10。
- 資料：`d1-records.json` 修兩筆（`discount-rate` 別名去重、`best-single-discount` 的 `not_same_as` 清空：`fare-policy` 不是詞彙 id，定義已說明不依條件先後取第一個）。參考 bundle 不重建（參考解答與 Recovery 的證據雜湊建立在原本 23 個 CRLF 檔案上，重建會全部失效），改在 tag 上加三個簽章 commit：以 `amend-policy` 授權第二把 Maintainer 金鑰（原私鑰不在產製機，新私鑰只在暫存區），再以 CP-CORE-002（`supersedes` CP-CORE-001，反事實檢查 `not_applicable`）修正兩筆詞彙；tag `dlc-d2-reviewed` 移到新 HEAD，`keys/` 附兩把公鑰。重跑 `make_recovery.py d1 d2 d3a d3b d3c` 與三份參考解答的 `domain-memory/`。
- 內容：D4 檢查點 1–2 改用 `shifted` 與每筆結果的 asset／id／`cited_lines`，不再從 `notes/` 反查 id；`resolve-terms` 的說明改為依名稱、id 或別名比對並附 `match_kind`，查不到時可能回非權威的 `mentioned`（10-d1、30／40／50、20-d1 備註、tools README）；50-d3c 的「批次在第一個錯誤停下」改為「同一種資產一起登記」；詞彙表加 `shifted`；Recovery 頁的數字與「三個金鑰指紋」。push 前啟用 `.venv` 保留：0.21.1 的 hook 先找 `python3` 再找 `python`，但 Windows 的 python.org 安裝沒有 `python3`、`python` 可能不在 PATH 或是 Store 捷徑，只改了理由的說法（01-environment、20-d2、開場投影片、主持指南常見問題第 4 條、tools README、11 號指令書）。D4 不教 `relocate-evidence`（檢查點 2 的 shifted 新行號已在 verify-evidence 輸出裡；它的 `registry_updates` 只對下一次核准有用），寫進參考解答的 D4 待辦。

量測（0.22.0）：
- 參考 Registry：162 個引用全部 current；verify-audit 64 events（原 62），head `sha256:955311a5…34260`；兩個 attestation commit 都 `Git governance is valid.`；推到本機 bare remote 時 hook 印六行。
- D1 重播（`make_recovery.py d1`，57 筆、互標 `not_same_as`）：`Registry is valid.`、162 current，約 55 秒（原約 100 秒）。
- Recovery current／shifted／stale：d2 162／0／0；d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（0.10.15 為 147／15、108／54、99／63）。Recovery 的 Registry commit 由 3 個變 6 個，接手後 `authorized_signers` 由 2 個變 3 個，D2 Recovery push 的 hook 印七行。
- 參考解答：d3a 192 個引用 177／12／3、69 events；d3b 225 個 168／35／22、73 events；d3c 248 個 171／16／61、77 events（原 72／82／90 events：同一種資產一次登記，事件變少）。
- `relocate-evidence --from . --to .`（D3a Recovery）：12 筆 `registry_updates`、`supersedes` CP-CORE-001、3 筆 unmatched，與 shifted／stale 一致。

驗證：已實跑工具自檢（5 tests OK，含互標 `not_same_as`；以舊版 make_record 重跑會失敗）、D1 重播、參考 Registry 的完整簽章與 push（本機 bare remote，未被擋）、d1–d3c Recovery 重建與量測、`relocate-evidence`，以及 `release_materials.py`（RELEASE PIPELINE PASS，DLC 候選 `23f432cf92c2153b`）。未驗證：以候選包貼 Runbook 提示詞逐頁演練（開場＋D1＋D2、D2／D3 Recovery 接手、D4 檢查點 1–3）已在沙箱啟動，但交回時結果尚未取得；交付前須補跑一次 rehearsal 並在此補記。

## domain-memory 升級 0.27.2（2026-10-16）

由 0.22.0 升級，現固定 0.27.2（SkillHub `214f269f5`）。過程：先固定 0.26.1（`6fe26ead1`）並完成全部驗證；作業期間作者 commit 了 0.27.0（`492af5a28`），預先檢查通過後改固定 0.27.0 並重跑驗證；同日再改固定 0.27.2。0.27.1 與 0.27.2 都是只修錯的 patch 版：0.27.1 讓 macOS／Linux 的 `cannot run <程式>`（簽章程式啟動不了）也報成「未檢查」，0.27.0 只認 Windows 的 `cannot spawn`；0.27.2 讓已安裝的 pre-push hook 在串接的舊 hook（`pre-push.domain-memory-existing`）存在卻失去執行權限時停下 push，原本是默默跳過。兩者都落在學員路徑上（macOS 學員、解壓或同步後的 Repo），依下方版本政策採用。Plugin 以 `git archive <commit> .claude/skills/domain-memory` 匯出到暫存區再封裝，不用 SkillHub 的工作目錄（裡面有未發布的修改）；`vendor_dlc_plugin.py` 的說明已補上這個做法。

做了什麼：
- 機械：產生 `domain-memory-0.27.2.zip`（73 個 Plugin 檔案；學員核對印出 `SHA OK 74 files`），刪除舊版的 ZIP 與 SHA256SUMS；版本字串與檔案數同步到 build_delivery_dlc（含測試、manifest）、dmlib、doctor、tools／DLC README、materials-dlc README、01-environment、開場投影片、主持指南、觀察指南、11 號指令書（順手修正 SHA256SUMS 檔名少了 `.zip`）、參考 Registry README。`dmlib.py` 的指令集合比對 `cli_parser`：只差 `init-change-package` 自 0.26.0 新增的可選 `--registry-root`（給 `--recitation` 用），已加入 `REGISTRY_OPTIONAL`；0.26.1、0.27.0 與 0.27.2 比對後三組都完全一致（0.27.1／0.27.2 沒有改 `cli_parser`）。
- 資料：參考 Registry、d2–d3c Recovery 與三份參考解答的 `domain-memory/` 都不重建。0.23–0.27.2 沒有改資料格式，`validate`、`verify-evidence`、`verify-audit` 結果與 0.22.0 完全相同；d2–d3c Recovery 由簽章 bundle 產生、不經 Plugin，重建只會讓 bundle 位元組變動，而它們的證據雜湊建立在原本 23 個 CRLF 檔案上（見 2026-10-15）。只重跑 d1（Plugin 產生的內容只差時間戳記；順帶把 d1 的起始 Repo README 同步為現行版本，原本落後一版）。
- 內容（只改學員會讀到的輸出或主持人會看到的訊息）：D4 檢查點 1 的回報多列 `verify-sources` 新增的 `discovered_but_gone`（D1 盤點時有、現在已不存在的檔案）；主持指南常見問題第 5 條改成 0.25.1 的訊息（`carries no signature`／`signature does not verify`，並說明 rebase／amend 會拿掉簽章、改用 merge），第 7 條加上 `Git commit signature was not checked`（Windows 接 `cannot spawn ssh-keygen`、macOS 自 0.27.1 接 `cannot run ssh-keygen`；開場 `doctor.py` 已檢查 `ssh-keygen`）；新增第 19 條：串接的舊 pre-push hook 失去執行權限時 0.27.2 停下 push 的訊息與修正（macOS `chmod +x`、Windows 看第一行 `#!`、不需要就刪掉、`pre-push` 遺失就重跑 `install-git-hitl-hook`）。DLC 的步驟都在剛 `git init` 或剛從 bundle clone 的 Repo 安裝 hook，只有學員機器原本就有別的 pre-push hook（例如 Git LFS）才會串接，所以列為主持人排錯項，不改 Runbook；Recovery 包不含 `.git`（hook 一律在接手時用封裝的 Plugin 重裝），沒有舊版 hook 需要重裝；三份 SOLUTION-NOTES 的 D4 待辦改用 `recite --onto` 把 stale 疊加到 `relocate-evidence` 的輸出。
- 不改：`shifted` 的說法（詞彙表與 D4 檢查點 2 已寫「只是移動、不算失敗、留給下一次核准的提案重新引用」，與 0.23 一致）；push 前設 `PYTHONUTF8` 與 dm 腳本固定 `-X utf8`（cp950 下 0.22.0 與 0.26.1 直接呼叫都沒出錯、hook 不設 `PYTHONUTF8` 也都通過，沒有證據顯示這些提醒已過時，而且無害）；DLC 原本就沒有非 ASCII 路徑的提醒可刪。

`init-change-package --recitation` 不放進 D4：D4 只有 10 分鐘、沒有成對簽章，而且實測（D3a Recovery 沙箱，0.26.1 與 0.27.0 結果相同：`relocate-evidence` 12 筆＋`recite --onto` 3 筆 stale＝15 筆 updates、0 unmatched，package 建立成功、`validate-change-package` 通過）發現 recitation package 無法走完：它唯一的測試義務是 cited paths 的 `verify-evidence`，Registry 還留著 stale 引用時結束碼為 1，`record-test-result` 不記錄，`verify-proposal` 因此拒絕；而引用要等套用後才會更新。只有 shifted 時 `verify-evidence --path` 結束碼為 0，可以走完，但 shifted 本來就通過所有檢查。這是 Plugin 的問題，應回報給 Plugin 作者。

量測（0.27.0，與 0.26.1、0.22.0 完全相同；0.27.2 重測的差異見下）：
- 工具自檢：7 tests OK（含 D1＋D2 簽章整合測試）。
- 參考 Registry：`Registry is valid.`（`--require-reviewed`）；162 個引用全部 current；verify-sources `current`、`discovered_but_gone` 空；verify-audit 64 events、head `sha256:955311a5…34260`；兩個 attestation commit `Git governance is valid.`；quality-gates 只有 pytest；pytest 76 passed；以第二把 Maintainer 金鑰（暫存區）做一個簽章 commit、推到本機 bare remote，hook 印六行 `Git governance is valid.`。參考 Registry 不必重簽。
- D1 重播（`make_recovery.py d1`）：57 筆，`Registry is valid.`，162 current，約 52 秒（0.26.1 約 64 秒）。
- Recovery current／shifted／stale：d2 162／0／0；d3a 147／12／3；d3b 108／32／22；d3c 99／31／32。
- 參考解答：d3a 192 個引用 177／12／3、69 events；d3b 225 個 168／35／22、73 events；d3c 248 個 171／16／61、77 events；`discovered_but_gone` 都是空的。
- D3a Recovery 的 recitation 試跑：見上；簽章 commit 與 push（八行 `Git governance is valid.`）都正常。

0.27.0 的新規則：material proposal 的 `implementation_design` 需要 `domain_forces`、`invariants_preserved`、`rejected_alternatives` 各至少一筆。DLC 會產生或附帶的 material Change Package 都已符合：CP-CORE-001（3／4／2）、CP-CORE-002（1／1／1，參考 Registry、d2–d3c Recovery 與三份參考解答裡的副本相同）、`inputs/package-spec.json`、學員範本 `worksheets/d2-signing-checklist.md`（三欄各一筆）、`test_tools.py` 的整合測試；Recovery 與參考解答的 `validate-change-package` 都通過。`fill_package.py` 沒有給這三欄時會寫空陣列，由 Plugin 擋下並說明，所以不另加檢查。

0.27.2 重測（與 0.27.0 相同，只列差異）：ZIP SHA256 `4057b081…6100ff`，仍是 73 個 Plugin 檔案、`SHA OK 74 files`；工具自檢 7 tests OK；參考 Registry 各項檢查結果相同，簽章 commit 這次改到 `domain-memory/`，push 時 hook 印七行 `Git governance is valid.`（六個 Registry commit＋新 commit）；D1 重播約 46 秒；Recovery 與參考解答數字不變。另實測 0.27.2 的新行為（Windows Git Bash）：串接的 hook 沒有 `#!` 第一行時被視為不可執行，push 停下並印出新訊息；補上 `#!/bin/sh` 後照常執行、push 通過。D3a Recovery 的 recitation 試跑沒有重跑（0.27.1／0.27.2 沒有改到 `recite`、`relocate-evidence`、`init-change-package`）。

驗證：已實跑上述全部項目與 `release_materials.py`（RELEASE PIPELINE PASS，DLC 候選 `3e468118f398ecdd`）。未驗證：以候選包貼 Runbook 提示詞逐頁演練（rehearsal），尤其 D4 檢查點 1 的新增欄位；2026-10-15 記錄的演練缺口仍未補。

Plugin 版本政策（2026-10-16 起）：一、固定一個確切的已 commit 版本，以 `git archive` 匯出後封裝，附逐檔與整包 SHA256，封裝的位元組不改。二、修正學員路徑上錯誤的 patch 版，重跑驗證（工具自檢、參考 Registry、D1 重播、`release_materials.py`）後採用；只動開發用檔案或與 DLC 無關的 patch 版可以不跟。三、minor 版（新增或改變行為）先讀 CHANGELOG 評估影響、在沙箱演練過再固定。四、排定的工作坊前 7 天凍結版本，凍結期間只接受安全性修正或會擋住學員的錯誤修正。五、每次改版都在本紀錄寫下 commit、採用理由與量測（與前一版的差異），並把版本字串與檔案數同步到所有出處（以舊版本號全文搜尋）。

## domain-memory OKF 改版準備（2026-10-16）

SkillHub 0.28.0（`5f6e046f6`）開始把 Registry 改存 OKF（Open Knowledge Format）：Plugin 讀寫改走單一 store，新增 `export`；版面本身之後才改。DLC 仍固定 0.27.2，先做準備：`docs/planning/domain-memory-touchpoints.md` 列出 DLC 依賴 Plugin 的每個地方（指令與旗標、直接讀寫的路徑、學員看到的輸出字串、隨包的 Registry 與簽章歷史），逐項標記不受影響／需 migrate／需改寫，並寫下 OKF 上線時的步驟與風險；DLC 工具讀 Registry 一律經 `dmlib.registry_documents()`（有 `export` 就用，0.27.2 退回讀檔）；三處學員文字的「JSON 檔」改為「檔案」；新增 `scripts/check_dlc_plugin_compat.py`。實測 0.27.2 為 29 PASS，0.28.0 只有「dmlib 尚未列入 `export`」一項 CHANGED。學員路徑上唯一寫死版面的是 D2 檢查點 3 第一步與簽章流程清單，換版時一起改；參考 Registry 的 migrate commit 需要 Maintainer 私鑰，只能在保管者的電腦執行。

## domain-memory 升級 0.33.0（OKF）（2026-10-17）

由 0.27.2 升級，現固定 0.33.0（SkillHub `b00228f49`，以 `git archive` 匯出；SkillHub 工作區另有未 commit 的修改，沒有使用）。0.28–0.33 都是 minor 版，依版本政策第三條先讀 CHANGELOG、在沙箱跑相容性檢查再固定。這是第一階段（技術基礎）：Plugin、DLC 工具、參考 Registry、Recovery 與參考解答全部改成 OKF 版面；學員內容只改不改就會壞的步驟，其餘列在下方「第二階段重新設計清單」。

採用理由：0.29 起 Registry 存成 OKF（Open Knowledge Format）概念檔，每筆紀錄一個 `registry/<類別>/<id>.md`，紀錄間的參照是 `# Relations` 底下的連結；0.31 起 reviewed 紀錄改帶 `verified`（誰、何時核准），不再有 `review` 區塊，審查它的提案改記在 audit log，引用只留 `path`、`lines`、`excerpt_sha256`；0.30 加 `export --commit`，0.32 加 `compare-registry`（以已審查的 Registry 為標準答案替抽取結果打分），0.33 加 `domain-memory-extract` Skill（`references/extraction.md`）與 `change-coupling`（從 Git 歷史找一起變動的模組）。學員用新 Plugin 做的 D1 一定是 OKF，參考 Registry 與 Recovery 若不跟著 migrate，同一班會出現兩種版面（見 `domain-memory-touchpoints.md` 第 8 節）。

相容性檢查（`check_dlc_plugin_compat.py --source <0.33.0 匯出>`，遷移前）：26 PASS、3 CHANGED。`dmlib.REGISTRY_REQUIRED` 少 `export`；`dmlib.REPO_ROOT` 少 `change-coupling`、`compare-registry`、`export`；參考 Registry 的 `validate --require-reviewed` 失敗（`holds a legacy review block; run migrate-registry`、`is reviewed but missing verified`）。其餘都通過，包括工具自檢、D1 重播（已是 OKF，57／57 筆經 export 讀到）、`verify-evidence`、`verify-audit`、兩個 attestation commit、兩個 Change Package、經 hook push 舊的簽章歷史（六行）。修正後以封裝的 ZIP 重跑：29 PASS、0 CHANGED。

做了什麼：
- 機械：`domain-memory-0.33.0.zip`（79 個 Plugin 檔案；學員核對印出 `SHA OK 80 files`；ZIP SHA256 `f53aefc0…eca751`），刪除 0.27.2 的 ZIP 與 SHA256SUMS；版本字串與檔案數同步到 build_delivery_dlc（含測試、manifest）、check_dlc_plugin_compat、dmlib、doctor、tools／DLC README、materials-dlc README、01-environment、開場投影片、主持指南、觀察指南、11 號指令書、參考 Registry README。主持指南常見問題第 19 條「Plugin 0.27.2 起改成停下 push」是行為的起始版本，保留。`dmlib.py` 三組指令集合改成與 0.33.0 的 `cli_parser` 完全一致；`registry_documents()` 只走 `export`，刪掉 0.27.2 的讀檔備援。
- 工具：`make_record.py` 與 `fill_package.py` 送出紀錄前也拿掉 `verified`（只能由 `apply-approved-updates` 寫入）；`test_tools.py` 的 D1＋D2 整合測試多驗 reviewed 紀錄帶 `verified`、沒有 `review` 區塊（讀取經 export）；相容性檢查改驗參考 Registry 的 OKF 紀錄形狀，hook 預期七行。其他工具不用改：`cite` 仍回 `source_kind`（Plugin 寫入時自己去掉衍生欄位），Change Package 範本格式沒變，`write_scm_attestation.py` 只讀寫 `changes/` 下的 JSON。
- 參考 Registry：在暫存區 clone bundle、checkout `dlc-d2-reviewed`（`core.autocrlf=false`，`* -text` 不變）→ `migrate-registry`（11 個 JSON 換成 69 個 `.md`：57 筆紀錄、11 個類別 `index.md`、1 個 `registry/index.md`；audit event 65 為 `migrate-registry`、`layout: okf`，`reviewed_by` 記每筆的審查提案 CP-CORE-001／002）→ `validate --require-reviewed`、`verify-evidence`、`verify-sources`、`verify-audit`、`quality-gates` → 由 Maintainer-2 金鑰簽章 commit `de53623`「Registry 改存 OKF 版面（domain-memory 0.33.0 migrate-registry）」→ `verify-git-governance --commit HEAD` → push 到全新的本機 bare remote（hook 七行）→ tag 移到 `de53623` → 重做 bundle、以 `git archive` 重新匯出 `domain-memory/` 快照。私鑰沿用暫存區 `up22/keys-ref/signing-key`（`%USERPROFILE%\.dlc-keys\maintainer-2\` 不存在），以 `user.signingkey` 在原處讀取，沒有複製、搬移、commit 或重產；指紋 `SHA256:GtKS8fEN…MueCs`。這個 commit 只動 `domain-memory/`：起始程式的 22 個 CRLF 檔與 `.gitignore`（CRLF／LF 混合）位元組不變，舊的 7 個 commit 與兩個 attestation 雜湊不變。
- Recovery：`make_recovery.py` 的「Registry 的六個 commit」改為七個（最上面一個是改存 OKF 版面）、push 檢查由七行改為八行；主持指南第 284 行同步；重跑 `make_recovery.py d1 d2 d3a d3b d3c`。Runbook 的 Recovery 頁沒有寫數字，不用改。
- 參考解答：三份 `domain-memory/` 各跑一次 `migrate-registry`（不是 Git repo，不用金鑰）；SOLUTION-NOTES 的 events 與 head 更新。
- 學員內容（只改會壞的）：D2 檢查點 3 第一步原本讀 `domain-memory/registry/*.json`，OKF 版面下 Agent 找不到 JSON、`promote` 會漏列，改為執行 `dm export`（兩個系統的指令寫在同一段），依類別記下 `status` 是 candidate 的 id；第二步兩個分頁的「每個有候選的檔案一個同名的鍵（檔名去掉 .json）」改為「每個有候選的類別一個同名的鍵（export 輸出的頂層鍵）」；`worksheets/d2-signing-checklist.md` 第 2 節同步。都以位元組層級修改，20-d2.md 保持 CRLF。
- 檢查程式：OKF 的紀錄連結是概念 ID（`/contexts/booking`），不是相對路徑；`validate_workshop.py` 與 `build_delivery_dlc.dlc_link_check` 原本把它當成檔案連結而失敗，改為在 `domain-memory/registry/` 底下把 `/<類別>/<id>` 對到 `<類別>/<id>.md` 再檢查（仍會擋斷掉的連結；`test_build_delivery_dlc.py` 加一個測試）。
- 其他：`materials-dlc/README.md` 的 `vendor_dlc_plugin.py` 範例補上必填的 `--source`；參考 Registry README（歷史、版面、預期結果、換行說明）、`dlc-validation-evidence.json` 加 `plugin_0_33_0_remeasure`、course-authoring Skill 的 DLC Plugin 規則（OKF 已上線、磁碟上 `status` 是 draft／stable、簽章歷史的新 commit 只能用 Maintainer-2 金鑰）、`domain-memory-touchpoints.md`。

量測（0.33.0，Windows；與 0.27.2 的差異）：
- 工具自檢：7 tests OK，約 23 秒。
- 參考 Registry：`Registry is valid.`（`--require-reviewed`）；162 個引用全部 current；verify-sources `discovered_but_gone` 空；verify-audit 65 events（原 64）、head `sha256:f53095a8…04b0`；兩個 attestation commit `Git governance is valid.`；push 到全新 bare remote，hook 印七行（原六行）。
- D1 重播（`make_recovery.py d1`）：57 筆，OKF 版面，`Registry is valid.`，162 current，約 60 秒。
- Recovery current／shifted／stale：d2 162／0／0；d3a 147／12／3；d3b 108／32／22；d3c 99／31／32（與 0.27.2 相同）。Registry commit 7 個都是 `G`；d2 依 RECOVERY.md 接手（另產生的練習金鑰、`amend-policy` 兩個→三個 fingerprint、簽章 commit）後 push，hook 印八行。
- 參考解答：d3a 177／12／3、70 events；d3b 168／35／22、74 events；d3c 171／16／61、78 events（引用數字不變，events 各多 1 筆）。
- `compare-registry`：D1 重播對參考 Registry 快照，11 類的 precision／recall／F1 都是 1.0（輸入相同，預期）；d3a 參考解答對 `--gold-commit dlc-d2-reviewed`（在參考 clone 內執行）precision 0.851、recall 1.0，extra 正好是 D3a 的 10 筆候選。`--gold-commit 22de5e4`（JSON 版面的舊 commit）也讀得到。
- `change-coupling`：起始 Repo 只有一個 commit，超過 30 個檔案被略過，輸出全空；d3c Recovery（9 個 commit）把門檻全部放到最低才有結果，而且只有 `api`／`application`／`domain`／`infrastructure` 四個分層資料夾彼此 degree 100（分層架構，看不出 Context）。

驗證：已實跑上述全部項目與 `release_materials.py`（RELEASE PIPELINE PASS，DLC 候選 `214e9bf877f22902`；主課程候選也會變，因為主課程打包清單釘選本紀錄）。未驗證：Windows 與 macOS 各以候選包演練 D1 檢查點 2–3、D2 檢查點 1–6（尤其新的 `dm export` 第一步與 push）、D2 Recovery、D3a 檢查點 5、D4 檢查點 1；macOS 完全沒有實跑；Agent 讀約 78 KB 的 export 輸出是否穩定列出全部候選，也還沒驗證。

第二階段重新設計清單：
1. D2 檢查點 3 第一步：export 輸出約 78 KB（57 筆含證據）。考慮 `--save` 到暫存檔再摘要，或請 Plugin 作者加只列 candidate 的篩選。
2. 磁碟上 `status` 是 draft／stable／deprecated，指令與 export 說 candidate／reviewed。「讀 domain-memory/ 裡的詞彙紀錄」（10-d1 檢查點 5 失敗時、30／40／50 第 2 步與失敗提示）應改用 `dm export` 或 `resolve-terms`，或在詞彙表說明兩套說法；30-d3a 第 3 步「看每筆紀錄自己的 status」目前靠 `get-context` 輸出（reviewed），Agent 若直接讀檔會看到 stable。
3. 新概念：OKF 概念檔（一筆一檔、`# Relations` 連結、PR diff 可讀）、`verified` 與審查提案記在 audit（取代 `review` 區塊）、引用只留雜湊；詞彙表 Registry 列與相關卡片。
4. `compare-registry`：設計 D1 結束或揭曉時的打分（學員包不能帶參考 Registry，可在主持人端或 Recovery 歷史上用 `--gold-commit`）；D3 可用來看「新增了哪些」。
5. `change-coupling`：起始 Repo 沒有可用的歷史，若要教，起始 Repo 需要一段依功能切的 commit 歷史；或改成「分層 Repo 上這個訊號不準」的反例。
6. `domain-memory-extract` Skill 與 `references/extraction.md`（語言→邊界→關係→戰術，紀錄不寫怎麼找到的）可作為 D1 的骨架，對照目前 D1 檢查點重排。
7. `export --commit`（0.30）：D4 可對照 D2 tag 與目前的事實。
8. 簡報、主持人指南、觀察指南：OKF 檔案的截圖與說明；主持人常見問題補「手動編輯 `.md` 超出 frontmatter 子集被拒（附行號）」與編輯器換行的處理（未實測）。
9. 學員包 `references/registry-schema.md` 新增「Concept files」一節；詞彙表或延伸閱讀引用章節時要核對。
10. `dlc-final-report.md` 首段只記到 0.27.2。

## DLC 第二階段改寫：Agentic DDD × domain-memory 0.33.0（2026-10-17）

依 `dlc-okf-redesign.md` 改寫學員內容；段落時間、檢查點分鐘、解鎖碼、表單 id、Recovery 都沒動，檢查點標題也沒改。指令名稱只出現在提示詞、④ 與備註。第一階段清單的處理：

- 1（export 約 78 KB）：D2 檢查點 3 第一步改為 `export --save ../../tmp/export-d2.json`（學員包根目錄的 `tmp/`，在 Repo 外），再用一行 Python 只印各類別候選 id；D1 失敗時、D3a–D3c 第 2 步同樣存檔後只列 Context 與詞彙名稱。PowerShell 5.1 與 Git Bash 實跑（D1 Recovery 的 57 筆：contexts 5、vocabulary 21、aggregates 2、rules 16、interactions 5、decisions 8）。
- 2（draft／stable 與 candidate／reviewed）：提示詞不再叫 Agent 讀 `domain-memory/` 的檔案找詞彙；D3a 第 3 步註明以 `get-context` 輸出為準；詞彙表 Registry 列說明兩套說法。
- 3（OKF、`verified`）：D1 檢查點 2 候選小卡、檢查點 4 登記後學員打開一份規則紀錄檔；D2 檢查點 4 夥伴自己打開要核准的紀錄檔；D2 檢查點 6 Agent 用 `get-record` 回報 `verified`（實測 `by: human:maintainer@example.com`），④ 加深一層小卡對照 ADR 的 Accepted 與決策者（Nygard、MADR）。
- 4（`compare-registry`）：學員包不能帶參考 Registry，改用學員自己的歷史：回顧檢查點 2 以 git log 最上面（最新）一個訊息含「套用」的 commit 為基準答案（自己做的 D2 是「D2：套用 CP-D2-001」，Recovery 是「CP-CORE-002：finalize 並套用」），對現在的工作區打分，extra＝核准後 Agent 新寫、待審的候選，missed＝核准過卻不見的。新概念小卡「評估 Agent 的成果」。實測 D3c Recovery 對 `fc9efe2`：1.0；加一筆候選後 rules extra＝[TEST-001]、precision 0.983；PowerShell `--save` 正常。
- 5（`change-coupling`）：不做主步驟；D1 Bounded Context 小卡加「資料夾不是證據：這個 Repo 依技術分層」，「說不出東西的訊號不是證據」寫在簡報備註與主持人指南。
- 6（擷取順序、元素定義）：D1 檢查點 3 ①「先統一名詞再劃邊界」、同字異義標「邊界訊號」；檢查點 4 ① 與提示詞要求每個 Context 列出訊號種類（只有一種標「證據薄弱」），規則「不是測試名稱、記錄訊息或願望」；D3c 檢查點 2 Aggregate「不是資料表、不是有子物件的類別」。
- 紀錄只放元素、關係、證據：D1 候選小卡與檢查點 5 ①；D2 `cp-d2.json` 新增 `open_questions`（`fill_package.py` 已支援，實測寫入 `domain-change-proposal.json`），簽章流程清單第 2 節同步。
- 7（`export --commit`）：D4 交接單 Domain facts 第一行寫模型版本（最後一個「套用」commit），Agent 以 `export --commit … --save ../../tmp/model-reviewed.json` 確認讀得到；③ 與 D4 範本同步。
- 重構 ≠ 模型變更：D3a–D3c 檢查點 5 提示詞先逐項判斷模型有沒有變；D3a ① 一句，D3b 檢查點 5 新概念小卡（Fowler〈Definition Of Refactoring〉）；D4 檢查點 1 小卡、檢查點 2 B 類條件。
- 8（主持人與觀察）：主持人指南 D1–回顧各表、「一筆紀錄長什麼樣」文字說明（代替截圖）、change-coupling 說明、陷阱 #20（手改紀錄檔：單引號被拒並附行號，實測 `frontmatter line 4: write this value plainly or in double quotes`；手改不留稽核事件）與 #21（存成 CRLF：實測 `validate`、`get-record` 正常，diff 整檔）；觀察指引 D1 O5–O6、D2 O6、D4 D2／D3、回顧 R4。
- 10：`dlc-final-report.md` 首段補 0.33.0。
- 未做：9（`registry-schema.md` 的 Concept files 已在 vendored Plugin 內，詞彙表直接引用〈Concept files〉）；Speech 由另一個工作改寫。

驗證（Windows，沙箱 `C:\tmp\dlc33`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL）：D1 Recovery 為底跑完 D2 檢查點 1–6 第一步（新的第一步、含 `open_questions` 的 `fill_package.py`、`submit-proposal`、`record-approval`、簽章 commit、attestation、`verify-git-governance`、finalize、apply、`validate --require-reviewed`、`get-record` 的 `verified`）；D2 第二步的套用 commit 與 push 沒有重跑（步驟未改）。D3 第 2 步的列出指令、D4 的 `export --commit`、回顧的 `compare-registry` 在 D3c Recovery 實跑。macOS 只做靜態檢查。`release_materials.py` RELEASE PIPELINE PASS；`check_dlc_plugin_compat.py` 29 PASS。

## DLC 學員包改為扁平結構，不再要求解壓到 C:\dlc（2026-10-17）

使用者要求：DLC 不再強調把 Repo 放到 C:\dlc，專注在 Agentic DDD。

- 根因：Plugin 寫入 Registry 時在 `domain-memory/` 下建 `.domain-registry-stage-<32 碼>/registry/<asset>/<id>.md`（Repo 根目錄之後約 125 字元，Plugin 位元組不改）；學員包又多包了 `agentic-workshop/07-dlc-ddd/participant/` 40 字元。深層基準 `C:\tmp\pl\OneDrive - Contoso Workshop\Desktop\some folder\Downloads\`（67 字元，比 `C:\Users\<名>\OneDrive - <公司>\Desktop\` 還深）加「全部解壓縮」預設的 `participant-dlc-open\`：最長路徑 286（.venv 的 pip 檔 266），超過 Windows 260 上限。
- 修正：`participant-dlc-open` 以 `destination_root` `"to": ""` 打包，ZIP 根目錄就是 `repository/`、`tools/`、`vendor/`（`..\..\tools` 相對位置不變）；同一基準最長 246（.venv 226）。Recovery 改解到學員包裡的 `recovery-<段>`（相對路徑，兩個 OS 一樣），D2 範本解到 `pkg-d2`。下載 id、解鎖碼、表單 id、include 路徑不變；D2–D4 範本包與 Recovery 包結構不變。
- 驗證（Windows，本機 LongPathsEnabled=1，所以以稽核鉤子量測每個被開啟／建立的路徑長度，而非等它報錯）：深層基準下 D1 環境（76 passed、SHA OK 80 files）、init／confirm／make_record／validate／verify-evidence；D2 Recovery 三步（簽章接手、`Git governance is valid.`、76 passed 1 warning、`Registry is valid.`、verify-audit valid、verify-evidence 全 current）；D3a Recovery 的 bash 解壓與歷史還原。macOS 靜態檢查（封存工具程式解開多項目 ZIP 會包 `participant-dlc-open/`，與 Windows 預設同一路徑）。

## domain-memory 升級 0.52.0（2026-10-17）

由 0.33.0 升級，現固定 0.52.0（SkillHub `ed3edd700`，以 `git archive` 匯出；沒有使用 SkillHub 工作區）。0.34–0.52 有 minor 版，依版本政策第三條先讀 CHANGELOG、跑相容性檢查、在沙箱演練再固定。Registry 版面（OKF）沒有再改：參考 Registry、bundle、tag `dlc-d2-reviewed`、`REGISTRY_COMMITS` = 7、參考解答的 `domain-memory/` 都不動，不需要 Maintainer 金鑰或簽章 commit。DLC 主軸仍是 Agentic DDD：新概念只放在能讓 DDD 判斷更清楚的地方，每個檢查點最多一個，指令名稱只出現在提示詞、④ 與備註。

相容性檢查（`check_dlc_plugin_compat.py --source <0.52.0 匯出>`，修改前）：24 PASS、5 CHANGED。dmlib 三組集合（新 `harvest-candidates`；`change-coupling` 改為可選 `--registry-root`）；tools 自檢失敗（`verify-proposal` 拒絕 evidence 不等於 obligation 的 check）；`QUOTED` 少 `failing_evidence`、`authoritative`。修正後以封裝的 ZIP 重跑：29 PASS、0 CHANGED。

會壞的地方與修法：
- 0.34 `counterfactual` 不經 shell、以 shlex 拆字：`.venv\Scripts\python.exe` 的反斜線被吃掉。實測 `.venv/Scripts/python.exe` 在 Windows 也失敗（`[WinError 2]`：CreateProcess 只把 `./` 開頭的相對路徑當成路徑），`./.venv/Scripts/python.exe` 才行，所以 Runbook 20／30／40／50 的 Windows `--test-command`、D3 工作規則第 2 條、tools README、主持指南常見問題第 2 條都改成 `./.venv/Scripts/python.exe`（PowerShell 與 Git Bash 相同；macOS 仍是 `.venv/bin/python`）。參考解答的 `run_counterfactuals.py` 把測試路徑改成斜線（直譯器路徑本來就加引號）。計畫原本寫 make_recovery 與 Recovery 頁有 `--test-command`，查證後沒有，不用改。
- 新 verdict `inconclusive`（逾時、改壞後無法載入、失敗不符 `--expect`）：D2 提示詞與小卡、D3 工作規則第 11 條、詞彙表、主持指南說明。
- 0.45 `failing_evidence` 改名 `failure_evidence`：`fill_package.py` 改讀新鍵；Runbook、詞彙表、簡報備註、主持指南改名；三份 SOLUTION-NOTES 註明 `evidence/counterfactual/*.json` 是 0.33.0 存檔、保留舊鍵。
- 0.51 `verify-proposal` 要求測試紀錄的 `evidence` 等於 obligation 的 `check`：`fill_package.py` 的 `check` 改為完整測試指令（前綴＋測試路徑），也以 shlex、不經 shell 執行（與 Plugin 相同），預設前綴 Windows `./.venv/Scripts/python.exe -m pytest -q`。`test_tools.py` 不用改（它傳加引號的絕對路徑），修正後 7 tests OK。
- 0.52 `resolve-terms` 移除 `authoritative`：D3a 兩個分頁與 tools README 刪掉；`QUOTED` 同步。
- 0.35–0.38 `compare-registry` 加 `overall_independent`、`copied_matches`、`copied_evidence`：回顧檢查點 2 的基準與候選是同一個 Registry 的兩個版本，核准後沒動過的紀錄全部標 `copied_evidence`，`overall` 1.0 幾乎全靠它們，提示詞與 ③ 改為也回報 `overall_independent`。

新概念與位置（每個都綁一個 DDD 判斷）：
- `proven_by`（規則有多可信，看證明它的測試）：D2 檢查點 6 新概念小卡，`get-record --changes-root domain-memory/changes` 回報 `verified` 與 `proven_by`；D4 檢查點 1 加深：stale 的規則重跑 `proven_by` 的測試，通過＝行為多半沒變，失敗或沒有測試＝模型真的落後（併進原本的加深小卡，① 仍 3 句）。
- `counterfactual --expect`（因為對的原因 killed）：D2 檢查點 3，併進原本的「反事實檢查」技巧小卡（不新增小卡）；方案多一欄「改壞後該看到的斷言」，範例 `--expect "700 == 595"`。D3 不加 `--expect`，仍由 Agent 看 `failure_evidence`。
- `also_covers`（一個測試守住幾條規則）：D3a 檢查點 5，候選清單把同一個測試守住的規則排在一起，④ 新增「新概念・加深一層：一個測試守住幾條規則」（加深不變量；D3a 已有 3 個新概念，所以用加深）；詞彙表「一致性邊界」補一句。
- 誠實的評估排除照抄的證據：回顧檢查點 2，併進原本的 eval 小卡；詞彙表 eval 列補一句。
- `change-coupling` 的 `explained_by`：查證後**不放進學員路徑**。D1 只有起始 commit；D3c Recovery 歷史上 D3 每段只有一個大 commit（被略過），把門檻放到最低也只有分層資料夾互相耦合，`explained_by` 對不上 Context，說不出東西。只在 D1 簡報備註與主持指南補一句 `explained_by` 的意思。
- Speech 只改備註：02 場反事實「要因為對的原因失敗」、04 場 eval「照抄的配對要排除」。

機械：`domain-memory-0.52.0.zip`（80 個 Plugin 檔案；學員核對印出 `SHA OK 81 files`；ZIP SHA256 `02df4401…39436a`），刪除 0.33.0 的 ZIP 與 SHA256SUMS；版本字串同步到 dmlib（三組集合與 `cli_parser` 一致）、doctor、build_delivery_dlc（含測試）、check_dlc_plugin_compat（`QUOTED` 49 個、學員旗標加 `--expect`、`--changes-root`、`export --commit`、`compare-registry`）、tools／DLC README、materials-dlc README、01-environment、開場投影片、主持指南（含「73 個檔案＝74 行」舊數字）、觀察指引、11 號指令書、course-authoring Skill。主持指南常見問題第 18 條「實測 0.33.0」是當時的量測，保留。

量測（0.52.0，Windows）：
- 工具自檢：7 tests OK，約 19 秒。
- Recovery：`make_recovery.py d1 d2 d3a d3b d3c` 重跑，d2–d3c 的 `repo.bundle` 與樹位元組不變（可重現），d1 只有 Plugin 時間戳變；current／shifted／stale：d1 162／0／0、d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（與 0.33.0 相同）。
- 參考解答反事實（`run_counterfactuals.py`，暫存複本）：d3a 25／25、d3b 23／24、d3c 37／38 killed，存活的都是已記錄的等價或測試不足那一個，沒有 `inconclusive`。
- D2 範例反事實：`--expect "700 == 595"` → killed、reason `the tests failed with output matching --expect 700 == 595`；`--expect "== 640"` → inconclusive；改成語法錯誤 → inconclusive；`--expect FAIL` 被拒。
- D3c Recovery：5 條 stale 規則都有 `proven_by`（CP-CORE-001 的測試路徑），重跑都通過；`compare-registry` 對 `fc9efe2`：overall 1.0、`copied_matches` 52、`overall_independent` 5／5；D3a Recovery 加 3 筆候選後 overall precision 0.95、`overall_independent` precision 0.625。

演練（Windows，沙箱 `C:\tmp\dm52`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包；沙箱產物：`py -3.13` 以 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`）：開場檢查點 1–4（76 passed、`SHA OK 81 files`、`"version": "0.52.0"`、brownfield／high、pytest）；D1 檢查點 2–4（PowerShell：11 筆候選、`Registry is valid.`、32 current）；D2 檢查點 1–6（PowerShell；反事實 PowerShell 與 Git Bash 都 killed；`fill_package.py` 的 check 與 evidence 都是 `./.venv/Scripts/python.exe -m pytest -q …`；`Proposal test evidence verified.`；`Git governance is valid.`；`proven_by` 列出 OB-FARE-005；push hook 兩行、`[new branch]`）；D2 Recovery（Git Bash 步驟 1、PowerShell 步驟 2–3；76 passed 1 warning；162 current；push hook 八行）；D3a 檢查點 4 一條反事實（PowerShell，killed）與檢查點 5（同一個測試守住兩條候選規則，`make_record --allow-unclassified`、`Registry is valid.`、夥伴簽章 commit）；D4 檢查點 1（PowerShell，含 `proven_by` 重跑）；回顧檢查點 2（PowerShell 與 Git Bash）。macOS 只做靜態檢查。

未驗證：macOS 實機；Agent 在真實對話中會不會為自訂方案寫出好的 `--expect`；D3b／D3c 檢查點 4 的新 `--test-command` 只以參考解答腳本間接驗證。

## domain-memory 升級 0.61.0（2026-10-17）

由 0.52.0 升級，現固定 0.61.0（SkillHub `0a40b5b48`，以 `git archive` 匯出；沒有使用 SkillHub 工作區）。0.53–0.61 都是 minor 版，依版本政策第三條讀 CHANGELOG 與 `git diff ed3edd700 0a40b5b48`、跑相容性檢查、在沙箱演練後固定。Registry 版面（OKF）沒有改：參考 Registry、bundle、tag `dlc-d2-reviewed`、`REGISTRY_COMMITS` = 7、參考解答的 `domain-memory/` 都不動，不需要 Maintainer 金鑰或簽章 commit。主軸仍是 Agentic DDD：新概念只放在能讓 DDD 判斷更清楚的地方，每個檢查點最多一個，指令名稱只出現在提示詞、④ 與備註；時間、分鐘、解鎖碼與表單 id 不變。

相容性檢查（`check_dlc_plugin_compat.py --source <0.61.0 匯出>`，修改前）：25 PASS、4 CHANGED。dmlib 兩組集合（`redraft-proposal`、`supersede-proposal` 接受可選 `--registry-root`；`coverage`、`promote-candidate`、`redraft-proposal`、`supersede-proposal` 接受 `--repo-root`）；經 pre-push hook push 參考歷史只印一行；`QUOTED` 找不到 `Git governance is valid.`。修正後以封裝的 ZIP 重跑：29 PASS、0 CHANGED（`QUOTED` 57 個，push 檢查改為「恰好一行 `Git governance is valid for 7 commits.`」）。

各版與學員路徑：
- 0.58 `verify-git-governance` 的訊息改成 `Git governance is valid for N commit(s).`，pre-push hook 一次檢查整個 push、只印一行（會壞）。Runbook D2 檢查點 5 的提示詞與 ③、檢查點 6 的回報（改問「for N commits. 裡 N 是多少」）、四個 Recovery 頁的 ③、`make_recovery.py`（RECOVERY.md「接著 … for 1 commit.」、push 一行 `… for 8 commits.`）、簡報 30-d2 備註、主持指南 D2 檢查點 6、參考 README（`for 1 commit.`、push 一行 `for 7 commits.`）都改。實測自己做的 D2 push：`Git governance is valid for 2 commits.`；D2 Recovery push：`for 8 commits.`。
- 0.58 聚焦測試 survived 時 reason 建議對整個測試套件重跑：與 D3 工作規則第 11 條「survived 不要換字串」不衝突，但 Agent 會猶豫，所以第 11 條加一項：同一組字串、TEST 換成 tests、存成下一個編號再跑一次，整套 killed 才算有測試守著。實測 D3b 的等價 mutant（`MIN_REDEMPTION_POINTS = 1`）整套仍 survived，照原規則記為等價。
- 0.59 `submit-proposal` 拒絕引用已確認來源以外路徑的升級紀錄（原本到 `apply-approved-updates` 才拒絕）：不會壞。自己做的 D1（11 筆）送出成功；D1 Recovery 的 162 個引用全部有 source kind，沒有未分類路徑；D3 的 `--allow-unclassified` 候選只到候選、不送審。`validate`／`verify-git-governance` 對已核准未套用的提案印 NOTE：D2 檢查點 5 時提案狀態是 `verified`，實測不會出現，提示詞不改。
- 0.53 `get-record` 沒給 `--changes-root` 也讀 `domain-memory/changes`：候選規則多一行 NOTE（沒有測試證明它），D2 檢查點 4 審查時看得到，是事實，不改。`coverage` 在沒有 `changes/` 時印 NOTE 請加 `--changes-root`：D1 檢查點 5 提示詞加一句「這是正常的，D2 才會有」。
- 0.54 `counterfactual` 多 `failing_tests`：D3a–D3c 檢查點 4 回報加一項「failing_tests 列出哪個測試抓到它」，D3a 檢查點 5 的「守住它的測試」改為取自 `failing_tests`（讓「一個測試守住幾條規則」有證據，不靠 Agent 猜）。只改提示詞，不是新概念。
- 0.55 `fill-harvest-package`、0.60–0.61 `supersede-proposal`／`redraft-proposal`：不在學員路徑。`fill_package.py` 照用：`fill-harvest-package` 要求每條規則都有 killed 的反事實，D2 只做一條。
- 0.56–0.57 `promote-candidate --amend`／`--cite`：學員不執行；只當 D4 檢查點 2 新概念的做法說明。

新概念與位置（每個都綁一個 DDD 判斷）：
- 「模型在哪些 Context 說了算」（`coverage` 的 `rule_totals`、`rules_by_context`，0.53／0.54／0.58）：D4 檢查點 1 多跑一個唯讀的 `coverage`，回報每個 Context 的已審查與候選規則、`proven`／`unproven`／`unknown`，列出沒有已審查規則的 Context；④ 新概念小卡；交接單 Unknowns 加「沒有已審查規則的 Context」。實測 D2 Recovery＋D3a 候選（新 Context `invoicing` 與兩條候選規則）：`contexts_without_reviewed_rules` 1；D3c Recovery：16 條全部 proven、0。D1 已有 3 個新概念、D2 檢查點 6 已有一個，所以放在 D4（本頁原本 0 個新概念）。
- 「重新證明同一條規則，還是寫一條新規則」（0.56–0.57 `promote-candidate --amend --cite`）：D4 檢查點 2 新增 ④ 新概念小卡；C 類理由改為「意思沒變：reviewed 不能覆寫，下一次核准沿用同一個 id 重新證明」；詞彙表「已審查事實」補一句；簡報 70-d4 與主持指南各補一句。
- 詞彙表「已審查事實」另補 `coverage` 的 `rules_by_context`。

機械：`domain-memory-0.61.0.zip`（81 個 Plugin 檔案，0.55 加 `harvest_package.py`；學員核對印出 `SHA OK 82 files`；ZIP SHA256 `71f345f9…388510`），`git rm` 0.52.0 的 ZIP 與 SHA256SUMS；版本字串同步到 dmlib（集合與 `cli_parser` 一致）、doctor、build_delivery_dlc（含測試）、check_dlc_plugin_compat、package-manifest-dlc、tools／DLC README、materials-dlc README、01-environment、主持指南、觀察指引、11 號指令書、course-authoring Skill（`.claude` 與 `.agents`）。主持指南 change-coupling 段的「0.52.0 實測」與常見問題第 18 條「實測 0.33.0」是當時的量測，保留；`dlc-final-report.md` 是歷史報告，不改。

量測（0.61.0，Windows）：
- Recovery：`make_recovery.py d1 d2 d3a d3b d3c` 重跑（d1 要 `--plugin` 指向解開的 ZIP），d2–d3c 的 `repo.bundle` 與樹位元組不變，只有 RECOVERY.md 的文字變；d1 只有 Plugin 時間戳變。current／shifted／stale：d1 162／0／0、d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（不變）。
- 參考解答反事實（`run_counterfactuals.py`，暫存複本）：d3a 25／25、d3b 23／24、d3c 37／38 killed，存活的仍是已記錄的等價 mutant，沒有 `inconclusive`；每個 killed 都有 `failing_tests`。
- D4 檢查點 1（D3c Recovery）：5 條 stale 規則都有 `proven_by`、重跑都通過；`coverage` 16 條全部 proven。回顧檢查點 2（D2 Recovery＋D3a 候選，對 `fc9efe2`）：overall precision 0.95、`copied_matches` 52、`overall_independent` precision 0.625（與 0.52.0 相同）。

演練（Windows，沙箱 `C:\tmp\dm61`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包；沙箱產物：`py -3.13` 以小 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`）：開場檢查點 1–4（76 passed、`SHA OK 82 files`、`"version": "0.61.0"`、brownfield／high、pytest）；D1 檢查點 2–4（PowerShell：11 筆候選、`Registry is valid.`、31 current；`coverage` 的 NOTE 與 `rules_by_context`）；D2 檢查點 1–6（PowerShell；反事實 PowerShell 與 Git Bash 都 killed、`failing_tests` 列出兩個測試；`Change package is valid.`；`Proposal submitted for human review.`；`Proposal test evidence verified.`；`Git governance is valid for 1 commit.`；`proven_by` 列出 OB-FARE-005；push `Git governance is valid for 2 commits.`、`[new branch]`）；D2 Recovery（Git Bash 步驟 1、PowerShell 步驟 2–3：76 passed 1 warning、`Registry is valid.`、66 events、162 current；Git Bash push `for 8 commits.`）；D3a 檢查點 4（PowerShell 兩條 killed，`failing_tests` 有參數化測試名）與 5（`make_record --allow-unclassified`、`Registry is valid.`、夥伴簽章 commit）；D3b 檢查點 4（PowerShell 兩條 killed：預留與歸還各一；另以等價 mutant 驗證整套重跑仍 survived）；D3c 檢查點 4（Git Bash 兩條 killed）；D4 檢查點 1（D3a 狀態與 D3c Recovery，含 `coverage` 與 `proven_by` 重跑）；回顧檢查點 2（PowerShell 與 Git Bash）。D3b／D3c 檢查點 4 以 Recovery 的參考實作代替學員實作。macOS 只做靜態檢查。

未驗證：macOS 實機；Agent 在真實對話中會不會照第 11 條把 survived 改跑整套、會不會把參數化的 `failing_tests` 收斂成測試名；D4 多一個指令後 3 分鐘是否夠（D4 原本就常超時，維持最低完成線）。

## domain-memory 升級 1.1.0（2026-10-19）

由 0.61.0 升級，現固定 1.1.0（SkillHub `8c7a8a47c`，以 `git archive` 匯出；沒有使用 SkillHub 工作區）。原本先以 1.0.0（`8ccb13ec0`）評估與修改，未提交前 1.1.0 釋出，改固定 1.1.0；1.0.0 的 ZIP 從未提交，直接刪除。1.0 是 major 版，依版本政策讀 CHANGELOG 與 `git diff 0a40b5b48 8c7a8a47c`、跑相容性檢查、在沙箱演練後固定。Registry 版面（OKF）、稽核事件名稱與證據包格式都沒有改：參考 Registry、bundle、tag `dlc-d2-reviewed`、`REGISTRY_COMMITS` = 7、參考解答都不用遷移，不需要新的簽章 commit，也沒有動用 Maintainer 金鑰。Plugin 維護者的檢查在匯出上重跑：`uvx ruff@0.16.7 check .` 全部通過；`run_tests.py --jobs 4` 41 個模組中 40 個 OK，`test_support` 是沒有測試的輔助模組，Python 3.12 起 `unittest` 對「沒有測試」回 exit 5，所以在 3.12／3.13 被算成失敗（3.11 回 0）：回報給維護者，不影響執行。

相容性檢查（`check_dlc_plugin_compat.py --source <1.0.0 匯出>`，修改前）：24 PASS、5 CHANGED。dmlib 三組集合（加 `brief`、`dependents`、`harvest`、`install-pre-commit-hook`、`mcp-serve`、`refresh-listing`、`ship-package`；刪 `apply-approved-updates`、`attest-signed-commit`、`finalize-proposal`）；學員指令 `finalize-proposal`、`apply-approved-updates` 不存在；tools 自檢失敗（`write_scm_attestation.py` 呼叫的 `attest-signed-commit` 已刪）。1.1.0 只在 `harvest` 與新指令 `discard-harvest` 上不同（執行檔只差 `cli_parser.py`、`commands/lifecycle.py`、`harvest_run.py`），dmlib 加 `discard-harvest` 後：30 PASS、0 CHANGED。

各版與學員路徑：
- 1.0 刪除 `attest-signed-commit`、`finalize-proposal`、`apply-approved-updates`，改用 `ship-package --package-root … --commit <sha>` 一步做完（會壞）。D2 檢查點 5 改成夥伴的 Agent 只驗證簽章 commit（`git log -1`＋`verify-git-governance --commit HEAD`）：這個 commit 就是核准紀錄；檢查點 6 由提案者跑 `ship-package --commit HEAD`（回報 `completed` 三步、`status` `applied`）→ `validate --require-reviewed` → `verify-audit`。刪除 `write_scm_attestation.py`；簽章流程清單、角色卡、`test_tools.py`（未簽章 commit 必須被 `ship-package` 拒絕）、簡報 30-d2、主持指南、詞彙表同步。
- 1.0 起 `ERROR:` 拒絕訊息與 NOTE 印在 stderr：dmlib 的 `--save` 只存 stdout，另把 stderr 照印；tools README 補一句。
- `counterfactual` 拒絕執行改成 JSON，`verdict` 是 `error`、exit 3（會壞）：D3 工作規則第 11 條改為 error 的 cf-*.json 刪掉重跑、killed／survived／inconclusive 保留；D2 檢查點 3、主持指南的介入句同步。
- `analyze-boundary` 一次回報兩個方向（`source_depends_on_target`、`target_depends_on_source`）：刪掉「對調再查一次」（D1 檢查點 6、D3 工作規則第 10 條、主持指南）。
- `verify-sources` 多 `discovered_but_unlisted` 與 discovery drifted 的 NOTE：D4 檢查點 1 的狀態仍是 `stale`（exit 1），提示詞已說只讀、不要試著修好，不改。
- `harvest`、`discard-harvest`、`mcp-serve`、`refresh-listing`、`list-proposals`：不在學員路徑。`fill_package.py` 照用：`harvest` 要求每條規則都有 killed 的反事實，D2 只做一條。
- 維護者提醒的 `shared-kernel`（Context 子領域）與 `separate-ways`（Interaction 關係）拒絕：參考 Registry、bundle、Recovery 與學員提示詞都沒有用到。

新概念與位置（Agentic DDD 為主，每個檢查點最多一個新想法）：
- Context Map 的上游／下游（`analyze-boundary` 兩個方向）：D1 檢查點 6 ④ 加深一層補一點；詞彙表新增「Context Map（上游／下游）」；簡報 20-d1 備註、演講 01 的 context-map 備註。Context Map 的 `relationship` 欄位（例如 customer-supplier）延後：D3 頁面已滿。
- 從變更簡報問起（`brief --base HEAD --markdown`）：D3b、D3c 檢查點 5 讓 Agent 只讀 Attention，逐筆判斷改動碰到引用行的已審查紀錄是模型變更還是重構；D3b ④「模型變更與重構」補一點。實測 Attention 列得到 REFUND-004（D3b、D3c），列不到 MEMBER-004：它沒有引用被改的行，要靠提示詞「被改變的已審查事實」那一步從需求卡找，簡報 55-d3b 備註照實寫。
- 規則守的是哪個 Aggregate（規則的 `aggregate` 欄位）：D3c 檢查點 5 的 d3c-records.json 範本加 `aggregate`，新增 ④「新概念・加深一層」；規則和 Aggregate 不在同一個 Context 時 Plugin 拒絕（`… belongs to context …, which the record does not name`），提示詞要 Agent 停下讓學員決定。觀察指南加 C6。
- 讓模型擋住讓引用失效的 commit（`install-pre-commit-hook`）：D4 檢查點 3 夥伴 commit 後裝上，`git mv discounts.py` 示範被擋下再搬回；④ 新概念小卡（Git〈githooks〉pre-commit；`--no-verify` 可繞過，回顧說明）。觀察指南加 D4。

刪除的概念：`analyze-boundary` 的「對調再查」；獨立的「寫出核准證明」步驟與 `write_scm_attestation.py`；counterfactual 的 `ERROR:` 文字拒絕。

順帶修正：兩版簡報 `src/deck.css`、`src/js/10-deck-core.js`、`src/js/20-deck-features.js` 重複貼上的區塊（HEAD 的 `test_deck_sources_have_no_pasted_duplicates` 因此失敗，擋住發布流程），只留最後一份，畫面不變；主持指南的 Plugin 檔案數（80／81 行）與開場簡報的 `SHA OK 81 files` 原本就過期，改成 94／95。

機械：`domain-memory-1.1.0.zip`（94 個 Plugin 檔案；學員核對印出 `SHA OK 95 files`；ZIP SHA256 `32e53e66…f60320`），`git rm` 0.61.0 的 ZIP 與 SHA256SUMS；版本字串同步到 dmlib（集合與 `cli_parser` 一致）、doctor、build_delivery_dlc（含測試）、check_dlc_plugin_compat（`QUOTED` 68 個，新增 pre-commit hook 擋下改名的檢查）、package-manifest-dlc、tools／DLC README、materials-dlc README、Runbook 開場、主持指南、觀察指南、指令書 11、course-authoring 技能。

量測（1.1.0，Windows）：
- Recovery：`make_recovery.py` 對 d1–d3c 各跑一次，d2–d3c 位元組不變；d1 只有事件 id 與時間戳變，還原為原版（1.1.0 下 `validate`、`verify-audit`、`verify-sources` 都通過）。current／shifted／stale：d1 162／0／0、d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（不變）。
- 參考解答反事實（暫存複本）：d3a 25／25、d3b 23／24、d3c 37／38 killed，存活的仍是已記錄的等價 mutant（PTS-003 min-points-1、PCR-004 days-by-datetime）。
- 回顧檢查點 2（D2 Recovery＋D3a–D4 候選，對 `fc9efe2`）：overall precision 0.90、recall 1.0、`copied_matches` 52、`overall_independent` precision 0.45（候選多了 D3b–D4 的紀錄）。

演練（Windows，沙箱 `C:\tmp\dm100\rh`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包；沙箱產物：`py -3.13` 以編譯的小 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`）：開場檢查點 1–4（76 passed；換 1.1.0 後重跑檢查點 2：`SHA OK 95 files`、`"version": "1.1.0"`）；D1 檢查點 2–6（12 筆候選、`Registry is valid.`、`analyze-boundary` 兩個方向、`no_registered_collaboration`）；D2 檢查點 1–6（`ready`、反事實 killed、4 個 obligation passed、`Change package is valid.`、`Good "git" signature`、`Git governance is valid for 1 commit.`、`ship-package` `completed` 三步、`status` `applied`、`verify-audit` 8 個事件、push `for 2 commits.`、`[new branch]`）；D2 Recovery（沿用金鑰、`ready`、簽章 commit、76 passed、162／0／0）；D3a 檢查點 1–5（反事實 killed、改壞前測試沒過時 `verdict` `error`）；D3b 檢查點 4–5（`brief` Attention 14 筆，含 REFUND-004）；D3c 檢查點 2–5（`brief` 列出 REFUND-004、規則帶 `aggregate`、放錯 Context 被拒絕）；D4 檢查點 1–3（`stale`、44 筆 stale 引用、16 條規則全部 proven、pre-commit 擋下改名並給出 relocate-evidence 那一行、搬回後狀態乾淨）；回顧檢查點 2。D1–D3b 以 1.0.0 執行、D3c 起以 1.1.0 執行（兩版執行檔只差 `harvest`）。Git Bash 變體只由相容性檢查以 bash 跑過 pre-push 與 pre-commit。

未驗證：macOS 實機（只做靜態檢查）；Agent 在真實對話中會不會只讀 Attention、不照 NOTE 執行 refresh-sources 或 recite；D4 檢查點 3 多一段 hook 示範後時間是否夠（D4 原本就常超時）。

## domain-memory 1.1.1（patch）（2026-10-19）

由 1.1.0 換成 1.1.1（SkillHub `accf3235f`，以 `git archive` 匯出；SkillHub HEAD 已往後走，不用工作區）。依版本政策，patch 修的是學員路徑上的提示文字，重跑檢查後採用。`git diff 8c7a8a47c accf3235f` 與 CHANGELOG 一致：沒有改指令、旗標、exit code 或版面；只改三處。
- `run_tests.py` 把沒有測試的模組標成 `skip`（1.1.0 回報給維護者的 `test_support` exit 5 問題）。匯出上重跑：40 個模組 ok、`test_support` skip、failed: none；`uvx ruff@0.16.7 check .` 全部通過。
- pre-commit 拒絕訊息結尾改為資訊句「details: verify-evidence … --staged … prints the full report, as this hook does when DOMAIN_MEMORY_HOOK_VERBOSE is set」，不再叫人帶變數重新 commit。
- `verify-sources` 的 drift NOTE：`discovery_drifted` 才指向 `refresh-listing`，其他狀態寫「the selection is <status>, so run refresh-sources, then confirm-sources」。

相容性檢查（封裝 ZIP）：30 PASS、0 CHANGED，`QUOTED` 仍 68 個。兩段改過的文字學員頁、簡報備註、主持指南都沒有引用，不用改。執行檔清單與 1.1.0 相同：94 個 Plugin 檔案，學員核對仍印 `SHA OK 95 files`；ZIP SHA256 `496c7926…6f5716`。`git rm` 1.1.0 的 ZIP 與 SHA256SUMS；版本字串同步到 1.1.0 升級時列的同一批檔案。Registry、bundle、Recovery、參考解答都不用動，沒有用到 Maintainer 金鑰。

提示詞：
- D4 檢查點 1 保留「出現 shifted、stale 或 exit 1 是預期中的結果，不要試著修好。」新 NOTE 仍是命令句（`so run refresh-sources, then confirm-sources`），`verify-evidence` 也印 `run recite on each to cite its current lines`；只靠「只讀不改」不夠。演練中 Agent 照提示詞沒有執行，所以不再加字。
- D4 檢查點 3 本來就沒有針對舊提示的防護，新結尾只指向唯讀的報告指令，演練沒有誘發重新 commit；「萬一示範的 commit 成功了」與同一次執行啟用 venv 仍需要（hook 要在 PATH 上找 Python）。不改。

演練（Windows，沙箱 `C:\tmp\dm111`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包 `9508f433ffb1dfd7`，結束後刪除）：
- 開場檢查點 2：`SHA OK 95 files`、`"version": "1.1.1"`，③ 成功（PowerShell 與 Git Bash）。
- D2 檢查點 1–6（由 D1 Recovery 起）：`ready`、反事實 killed、`Change package is valid.`、`Good "git" signature`、`Git governance is valid for 1 commit.`、`ship-package` `completed` 三步、`status` `applied`、`Registry is valid.`、`verify-audit` 11 個事件、push `for 2 commits.`、`[new branch]`；檢查點 5、6 的 ③ 成功；重跑 `ship-package` 回 `already applied; nothing was written`。
- D4 檢查點 1–3（由 D3c Recovery 起）：`verify-sources` `stale`、exit 1，NOTE 為新文字；`verify-evidence` 99／31／32；coverage 16 條已審查規則全部 proven；5 條 stale 規則的測試都通過；檢查點 2 登記 1 筆候選（REFUND-004 → REFUND-005）；交接單七段、簽章 commit、pre-commit 擋下改名（14 筆紀錄、relocate-evidence 那一行、新結尾），搬回後只剩 `?? records/`；三個 ③ 都成功。

未驗證：macOS 實機（只做靜態檢查）。

## domain-memory 升級 1.2.2（2026-10-19）

由 1.1.1 升級，現固定 1.2.2（SkillHub `42819a57e`，以 `git archive` 匯出；沒有使用 SkillHub 工作區）。1.2 是 minor 版，依版本政策讀 `git diff accf3235f 42819a57e -- .claude/skills/domain-memory` 與 CHANGELOG 1.2.0–1.2.2、跑相容性檢查、在沙箱演練後固定。Registry 版面、稽核事件與證據包格式都沒有改：參考 Registry、bundle、tag `dlc-d2-reviewed`、`REGISTRY_COMMITS` = 7、參考解答都不用遷移，不需要新的簽章 commit，沒有動用 Maintainer 金鑰。維護者的檢查在匯出上重跑：`uvx ruff@0.16.7 check .` 全部通過；`run_tests.py --jobs 4` 40 個模組 ok、`test_support` skip、failed: none。

相容性檢查（`check_dlc_plugin_compat.py`）：匯出、修改前 28 PASS、2 CHANGED（dmlib `REGISTRY_REQUIRED`、`REPO_ROOT` 少 `rebase-proposal`）；封裝 ZIP、修改後 32 PASS、0 CHANGED。dmlib 兩組集合加 `rebase-proposal`（`cli_parser` 62 → 63 個指令）；`QUOTED` 68 → 71（`nothing was written`、`proposal base revision is stale; rebase-proposal`、`approvals_retired`）；參考 Registry 兩個 applied 套件加跑 `verify-proposal`。`test_tools.py` 加一行：送出並驗證後重跑 `verify-proposal` 要印 `already verified at revision 1; nothing was written`。

逐項對照程式（維護者的摘要都屬實）：
- 1.2.1／1.2.2 `verify-proposal`：狀態是 verified、approved、applied 時印 `already <status> at revision <n>; nothing was written`、exit 0；draft 仍拒絕。1.1.1 是 `ERROR: only a submitted proposal may be verified`、exit 1，所以 D2 檢查點 4 的 ③（重跑 `verify-proposal`、等 `Proposal test evidence verified.`）原本會誤判失敗，簡報備註因此寫「不重跑」。修正：③ 第 1 項改等 `already verified at revision 1; nothing was written`（實測 ③ 成功）。
- 1.2.0 `rebase-proposal`：`proposal_revision` 加 1、`scm_attestation` 清空、`status` 回 `submitted`、`verified_at` 清空，保留測試結果，只寫審查包；印 `package`、`status`、`proposal_revision`、`base_registry_revision`、`approvals_retired`、`attestation_removed`、`next`。拒絕 draft、approved、applied、superseded 與「base 已是現在」的提案。
- 1.2.0 訊息：過期 `proposal base revision is stale; rebase-proposal, then obtain fresh approval: <原因>`；自己寫的紀錄被改 `<asset>/<id>, which this proposal writes, changed since it was reviewed`；套用時的競態 `registry revision changed before update; run ship-package again`。學員頁、簡報都沒有引用舊字串。
- 1.2.0 `committed_digest`：只有提交時 HEAD 裝著 Registry 才寫。自己做的 D2 在檢查點 3 提交時 HEAD 是「起始 Repo」，沒有 Registry，所以沒有這個欄位，之後任何 Registry 變動都會以「the base Registry cannot be rebuilt from its observed commit」判為過期（與 1.1.1 相同）。1.1.x 的套件照舊驗證：參考 Registry、d2–d3c Recovery 與三份參考解答的 CP-CORE-001／002 都是 `Change package is valid.`，`verify-proposal` 回 `already applied at revision 1; nothing was written`，`validate`、`verify-audit` 通過。
- 1.2.0 `discard-harvest` 也收 verified 的套件；`registry.as_stored` 是新函式，沒有新檔案（仍 94 個 Plugin 檔案）。都不在學員路徑。

`rebase-proposal` 放哪裡：只寫進主持指南常見問題第 19 條，不進 Runbook。學員路徑上唯一的提案是 D2 的 CP-D2-001，提交到套用之間 Registry 只靠提案本身改變；D3、D4 只登記候選，沒有待審的提案。要教「核准綁定的是那一版模型」，得在最緊的 D2（規格 R1）刻意製造一次過期再重新核准，多一次簽章 commit，又沒有現成的手動繞法可以取代。第 19 條給兩條路：提交後誤加的候選用 `retract-candidate` 撤回，模型回到核准的那一版，`ship-package` 直接通過；改動要留下才 `rebase-proposal`，夥伴重做檢查點 4 第二段與檢查點 5，push 時是 `for 3 commits.`。

機械：`domain-memory-1.2.2.zip`（94 個 Plugin 檔案；學員核對仍印 `SHA OK 95 files`；ZIP SHA256 `fcd47910…edb047`），`git rm` 1.1.1 的 ZIP 與 SHA256SUMS；版本字串同步到 1.1.0 升級時列的同一批檔案（另含 `.agents/skills/course-authoring/SKILL.md` 鏡像）；觸及點文件更新，並把「常見問題第 19 條」的舊指涉改為第 16 條（0.27.2 那條）。

量測（1.2.2，Windows）：
- Recovery：`make_recovery.py` 對 d1–d3c 各跑一次，d2–d3c 位元組不變；d1 只有稽核事件 id、head 雜湊與 `confirmed_at` 變，還原為原版。current／shifted／stale：d1 162／0／0、d2 162／0／0、d3a 147／12／3、d3b 108／32／22、d3c 99／31／32（不變）。
- 參考解答反事實（暫存複本）：d3a 25／25、d3b 23／24、d3c 37／38 killed，存活的仍是已記錄的等價 mutant（PTS-003 min-points-1、PCR-004 days-by-datetime）。

演練（Windows，沙箱 `C:\tmp\dm122`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包 `59548f1ea4ab637d`，結束後刪除；沙箱產物：`py -3.13` 以編譯的小 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`；Recovery 與 D2 範本的 zip 直接從候選資料夾解，不經真實下載資料夾）：
- 開場檢查點 2：`SHA OK 95 files`、`"version": "1.2.2"`（PowerShell 與 Git Bash）。
- D2 檢查點 1–6（由 D1 Recovery 起）：`ready`、反事實 killed、17 個 obligation passed、`Change package is valid.`、`Proposal submitted for human review.`、`Good "git" signature`、檢查點 4 ③ 重跑得到 `already verified at revision 1; nothing was written`、`Git governance is valid for 1 commit.`、`ship-package` `completed` 三步、`status` `applied`、`Registry is valid.`、`verify-audit` 11 個事件、push `for 2 commits.`、`[new branch]`；套用後 `verify-proposal` 回 `already applied at revision 1`。
- 過期演練（從檢查點 5 之後的複本）：核准 commit 後再登記一筆候選，`ship-package` 停在 `finalize-proposal`，errors 是新訊息，`status` `verified`；`rebase-proposal` 回 `submitted`、`proposal_revision` 2、`approvals_retired` 1、`attestation_removed` true；再跑一次被拒（`the proposal base is current`）；未重新核准就 `verify-proposal` 被拒；拿舊的核准 commit `ship-package` 被拒（`carries another proposal or revision`）；重新核准、新簽章 commit 後 `applied`，push `for 3 commits.`。另一份複本改用 `retract-candidate` 撤回那筆候選，`ship-package` 直接 `applied`、`validate --require-reviewed` 通過。
- D2 Recovery（步驟 2 用 PowerShell）：沿用金鑰、`ready`、簽章 commit、76 passed（1 warning）、162／0／0。
- D3a 檢查點 5（在 D2 Recovery 上放入參考實作）：反事實 killed、登記 1 個 Context 與 1 條規則、`Registry is valid.`、夥伴簽章 commit。
- D4 檢查點 1–3（由 D3c Recovery 起）：`verify-sources` `stale`、exit 1；99／31／32；16 條已審查規則全部 proven；5 條 stale 規則的測試都通過；登記 REFUND-005 候選；交接單簽章 commit；pre-commit 擋下改名（14 筆紀錄、relocate-evidence 那一行），搬回後只剩 `?? records/`。

回報給維護者：
- `rebase-proposal` 的「base 已是現在」比較整個 revision（含 `observed_commit`）：Registry 沒變、只是多了一個 commit（例如核准 commit 本身）時，它照樣 rebase 並作廢有效的核准（實測 `approvals_retired` 1）。CHANGELOG 說它拒絕 base 仍是現在的提案；建議改以 `require_current_registry_revision` 通過與否判斷。
- `ship-package` 因過期停在 `finalize-proposal` 時，`next` 仍寫「the proposal is verified; ship-package --commit …」，沒有指向 `rebase-proposal`；而且第一步已寫入 attestation。
- 由程式推論、未實測：1.1.x 提交、base 裡沒有 `committed_digest` 的提案，只要 HEAD 裝著 Registry，即使 HEAD 沒動，`rebase-proposal` 也會因為多出 `committed_digest` 而視為不同、照樣 rebase。

未驗證：macOS 實機（只做靜態檢查：這次改的是 ```text 的 ③ 與主持指南，沒有 macOS 專屬指令）；Agent 在真實對話中看到過期訊息會不會自行執行 `rebase-proposal`（D2 檢查點 6 ② 與「失敗時」都要它停下）。

## domain-memory 1.2.4（patch）（2026-10-19）

由 1.2.2 換成 1.2.4（SkillHub `089b50321`，以 `git archive` 匯出；只讀 commit 過的內容：`git diff 42819a57e 089b50321 -- .claude/skills/domain-memory` 與 CHANGELOG 1.2.3、1.2.4）。依版本政策，patch 修的是主持指南第 19 條碰到的 `rebase-proposal`／`ship-package` 行為，重跑檢查後採用。改動只在 `hitl.py`、`ship.py`、`script-api.md` 與測試：指令仍 63 個，沒有新檔案（94 個 Plugin 檔案，學員核對仍印 `SHA OK 95 files`；ZIP SHA256 `96f22ad6…19a20e9`），版面、稽核事件、證據包格式都沒變，不需要遷移，沒有用到 Maintainer 金鑰。維護者的檢查在匯出上重跑：`uvx ruff@0.16.7 check .` 全部通過；`run_tests.py --jobs 4` 41 個模組，`test_support` skip，failed: none。

逐項對照程式與演練（維護者的摘要都屬實）：
- 1.2.4：base 沒過期時 `rebase-proposal` exit 0，印 JSON（`package`、`status`、`proposal_revision`、`base_registry_revision`、`note` `the proposal base is current; nothing was written`、依狀態的 `next`），什麼都不寫；`nothing to rebase` 已不在原始碼裡。
- 1.2.3：「是否過期」交給和 verify／finalize／apply 相同的過期檢查（`require_current_registry_revision`），不再比對整個 base revision；拒絕訊息是 `a draft proposal is not rebased; submit-proposal stamps its base`、`an applied proposal is not rebased; it is applied; supersede it and open a new draft`、`a superseded proposal is not rebased; it is retired; redraft-proposal opens a new draft from it`；approved 的提案也收，回 `submitted`、清 `finalized_at`（Plugin 測試涵蓋，學員路徑碰不到 approved 停留的狀態）。
- 1.2.3：verified 的提案在寫 attestation 之前先做過期檢查；過期時 `completed` 是 `[]`、不寫 attestation，errors 是 `finalize-proposal: proposal base revision is stale; rebase-proposal, then obtain fresh approval: …`，`next` 是 `the proposal base is stale; rebase-proposal, then record-approval, verify-proposal, sign a commit holding the package, and ship-package --commit <that commit>`。這三點修掉 1.2.2 回報給維護者的前兩項。

相容性檢查（`check_dlc_plugin_compat.py`，封裝 ZIP）：版本字串換好後第一次就是 32 PASS、0 CHANGED，dmlib 不用改；`QUOTED` 71 → 73，加上主持指南新引用的 `the proposal base is stale; rebase-proposal` 與 `the proposal base is current; nothing was written`，`proposal base revision is stale; rebase-proposal` 仍找得到。`git rm` 1.2.2 的 ZIP 與 SHA256SUMS；版本字串同步到 1.2.2 升級時的同一批檔案。

主持指南常見問題第 19 條：原本照 1.2.2 寫（`ship-package` 先寫 attestation、再停在 finalize）。改為 errors 帶 `finalize-proposal:` 前綴、`completed` 是 `[]`（什麼都沒寫入），改動要留下時照 `next` 跑 `rebase-proposal`；並註明 base 沒過期時它只回 `the proposal base is current; nothing was written`、不動核准。Runbook 與簡報不用改。Recovery 與參考解答反事實沒有重跑：這次只改 `rebase-proposal` 與 `ship-package` 的過期判斷，相容檢查的 D1 重播 57／57、參考 Registry 全部通過。

演練（Windows，沙箱 `C:\tmp\dm124r`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包 `bebcc1e7bbd5547b`，結束後刪除；沙箱產物：`py -3.13` 以編譯的小 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`；Recovery 與 D2 範本的 zip 從沙箱的下載資料夾解，不讀登錄檔的真實下載資料夾）：
- 開場檢查點 1–4：76 passed；`SHA OK 95 files`、`"version": "1.2.4"`（PowerShell 與 Git Bash）；brownfield／high、只有 pytest；起始 commit。
- D1 Recovery 步驟 1–2（PowerShell）：`?? domain-memory/`、`?? notes/`、76 passed、`Registry is valid.`、162／0／0。
- D2 檢查點 1–6：`ready`；候選 contexts 5、vocabulary 21、aggregates 2、rules 16、interactions 5、decisions 8；反事實 killed；17 個 obligation passed、`Change package is valid.`、`Proposal submitted for human review.`；`Good "git" signature`；檢查點 4 ③ `already verified at revision 1; nothing was written`；`Git governance is valid for 1 commit.`；`ship-package` `completed` 三步、`applied`；`Registry is valid.`；`verify-audit` 11 個事件；套用 commit 已簽章、`verify-git-governance` 通過。`git push` 被這次執行環境的權限檢查擋下，沒有跑（hook 的 `for 2 commits.`／`for 3 commits.` 沿用 1.2.2 的實測）。
- 過期（核准 commit 之後再登記一筆候選）：`ship-package` exit 1，`completed` `[]`，errors 與 `next` 如上，`scm_attestation` 仍是 null，審查包沒有變動。路一：`retract-candidate` 撤回後 `ship-package` 直接 `applied`、`validate --require-reviewed` 通過。路二：`rebase-proposal` → `submitted`、`proposal_revision` 2、`approvals_retired` 1、`attestation_removed` false（1.2.3 起本來就沒寫）；再跑一次回 `note`（base current）、exit 0；未重新核准就 `verify-proposal` 被拒；拿舊核准 commit `ship-package` 被拒（`carries another proposal or revision`）；夥伴重做檢查點 4 第二段、新簽章 commit、檢查點 5 通過後 `applied`；晚加的候選照預期 `not reviewed`；對 applied 的提案 `rebase-proposal` 回 `an applied proposal is not rebased; …`。
- base 沒過期（核准 commit 之後、Registry 沒動）：`rebase-proposal` exit 0、`note` `the proposal base is current; nothing was written`、`next` `sign a commit holding the package, then ship-package --commit <that commit>`；`status` 仍 verified、`proposal_revision` 1、核准仍 1 筆；接著 `ship-package` 直接 `applied`（1.2.2 在這裡會作廢核准）。

回報給維護者：
- 自己做的 D2 在檢查點 3 提交時 HEAD 沒有 Registry，所以過期原因一律是 `the base Registry cannot be rebuilt from its observed commit, so the records this proposal touches cannot be compared`，不會說是哪一筆變了；這不影響補救，但學員看不出是哪個改動造成的。
- 由程式推論、未實測：`ship-package` 只對 verified 先做過期檢查；approved（定案後套用失敗）的過期仍由 apply 拒絕，`next` 是否同樣指向 `rebase-proposal` 沒有測到。

未驗證：macOS 實機（這次只改主持指南，沒有 macOS 專屬指令）；`git push`（權限檢查擋下）。

## domain-memory 1.2.8（patch）（2026-10-19）

由 1.2.4 換成 1.2.8（SkillHub `7d2c73c6f`，以 `git archive` 匯出；只讀 commit 過的內容：`git diff 089b50321 7d2c73c6f -- .claude/skills/domain-memory` 與 CHANGELOG 1.2.5–1.2.8）。依版本政策，四個都是 patch，重跑檢查後採用。`cli_parser.py` 沒變，指令仍 63 個；沒有新增或刪除的檔案（94 個 Plugin 檔案，學員核對仍印 `SHA OK 95 files`；ZIP SHA256 `6544504b…74397b58`）；版面、稽核事件、證據包格式都沒變，不需要遷移，沒有用到 Maintainer 金鑰。維護者的檢查在匯出上重跑：`uvx ruff@0.16.7 check .` 全部通過；`run_tests.py --jobs 4` 41 個模組，`test_support` skip，failed: none。

逐項對照程式（維護者的摘要都屬實）：
- 1.2.5：只動 `ruff.toml` 與測試，兩者都不進 ZIP。
- 1.2.6：`probe` 過期那一行由「…; refresh before trusting it.」改成「Domain Memory at <root>: stale. <n> sources moved (<names>); run refresh-sources, then have a developer run confirm-sources.」（`commands/read.py`）。其他是文件：`readiness` 的範例帶 `--registry-root`、依賴政策的值寫 `forbidden`、引用的指令補上必填旗標。
- 1.2.7：新的拒絕訊息有三個：`ERROR: <commit>:<path> is not valid JSON`（commit 裡的政策 JSON，`revision.py`）、`ERROR: Command '[...]' timed out after 15 seconds`（git 與 ssh-keygen 的呼叫加上 `GIT_COMMAND_TIMEOUT_SECONDS = 15`，`cli.py` 接住 `subprocess.SubprocessError`，exit 1）、`ERROR: invalid JSON: <path>`（巢狀過深，接住 `RecursionError`）。行為的改變：`init-domain-memory` 的政策被拒時，用 `remove_tree` 刪掉剛建的輸出；`verify-proposal` 與 `finalize-proposal` 先驗證再寫入；`discard-harvest` 在寫入鎖內先記稽核事件再刪套件；GitHub 回傳的 `user`／`head` 是 null 時不再當掉；從 `DOMAIN_MEMORY_SIGNING_KEY` 寫出的金鑰一建立就是 0600；過期改用 `StaleBaseError` 判斷，`STALE_BASE` 訊息不變。摘要沒提的一項：輸出資料夾已有內容時，三處原本丟 `FileExistsError`，現在一律 `ValueError`，訊息仍是 `output directory is not empty: <path>`。
- 1.2.8：只改文件。script-api 最長的幾列只留契約；`Package a re-citation`、`Preview the next stage` 兩個列名消失，改成 `init-change-package`、`validate-change-package` 各一列；`probe` 那列寫明 exit code（0 current、1 其他狀態、2 absent），理由移到其他頁與新的〈Notes on single commands〉。

DLC 碰到的地方（逐一 grep 過）：
- `probe` 不在學員路徑（Runbook、Recovery、簡報、主持指南、tools 都沒有，只列在 dmlib 的指令集合），新句子沒有地方要改。D4 檢查點 1 跑的是 `verify-sources`，它的 NOTE 沒變（`… the selection is stale, so run refresh-sources, then confirm-sources`），仍是命令句，所以保留「出現 shifted、stale 或 exit 1 是預期中的結果，不要試著修好。」新的 `probe` 句子也是命令句，日後放上學員路徑時同樣要配這句。
- DLC 引用的 script-api 列（`get-record`、`coverage`、`install-pre-commit-hook`）與各頁標題都還在；被刪的兩個列名 DLC 沒有引用，相容性檢查也不讀列名。
- `doctor.py` 只讀 `plugin.json` 的版本，不解析 `probe` 輸出或 traceback；`test_tools.py` 沒有引用改動的字串；`QUOTED` 不用增減。
- D1 檢查點 2 的「失敗時」原本就要 Agent 先解釋錯誤、等同意再處理。1.2.7 起政策被拒不會留下半成品，修正參數後直接重跑即可；1.2.4 會留下 `domain-memory/`，重跑時回 `output directory is not empty`。學員頁不用改。

相容性檢查（`check_dlc_plugin_compat.py`）：1.2.8 匯出在改版本字串之前就是 32 PASS、0 CHANGED，INFO 仍只有 `list-proposals`；封裝 ZIP 後同樣 32 PASS、0 CHANGED，`QUOTED` 73 個全部找得到（本次輸出看到 32 個）。腳本只改 `VENDOR_ZIP`。`git rm` 1.2.4 的 ZIP 與 SHA256SUMS；版本字串同步到 1.2.4 換版時的同一批檔案；`SHA OK 95 files` 不變。

演練（Windows，沙箱 `C:\tmp\dm128r`，隔離 HOME／USERPROFILE／GIT_CONFIG_GLOBAL／APPDATA／LOCALAPPDATA，DLC 候選包 `e89553db35eb4508`，結束後刪除；沙箱產物：`py -3.13` 以編譯的小 shim 指向 uv 的 Python，doctor 因此報 py launcher `[!!]`。登錄檔的下載資料夾是 `%USERPROFILE%\Downloads`，在沙箱裡展開成沙箱的下載資料夾，所以 Recovery 與 D2 範本的指令原樣執行）：
- 開場檢查點 1–4：76 passed；`SHA OK 95 files`、`"version": "1.2.8"`（PowerShell 與 Git Bash）；`"state": "brownfield"`、`"confidence": "high"`，quality-gates 只有 pytest、`"standard": "none"`；python 在 `.venv\Scripts`；起始 commit 不含 domain-memory/，`git status --short` 是空的。
- 刻意讓政策被拒的 init（`--exclude " "`）：`ERROR: invalid policy: policy requires include patterns and valid exclude patterns`、exit 1、沒有留下 `domain-memory/`（同一個指令換 1.2.4 會留下）；接著照 Runbook 的參數重跑成功。
- D1 檢查點 2–3：`Domain Memory initialized. …`、`Sources confirmed by DLC Proposer <proposer@example.com>: docs/adr, docs/requirements, src, tests`、`selection_status` developer-confirmed、`status` current；domain-memory/ 未 commit。`make_record.py --batch` 6 筆詞彙全部寫出 `records/vocabulary-<id>.json`。
- D1 Recovery 步驟 1–2（PowerShell，D2 的起點）：`?? domain-memory/`、`?? notes/`、76 passed、`Registry is valid.`、162／0／0。
- D2 檢查點 1–6：金鑰 `source` generated；三次 amend-policy、hook 安裝、`{"status": "ready", "blocks": []}`；候選 contexts 5、vocabulary 21、aggregates 2、rules 16、interactions 5、decisions 8；反事實 killed、`the tests failed with output matching --expect 700 == 595`、restored true；19 個 obligation 全部 passed（cp-d2.json 以參考套件描述改寫）、`Change package is valid.`、`Proposal submitted for human review.`；`Human approval recorded.`、`Proposal test evidence verified.`、`Good "git" signature for maintainer@example.com`、Author DLC Maintainer；檢查點 4 ③ 重跑 `already verified at revision 1; nothing was written`、exit 0；`Git governance is valid for 1 commit.`；`ship-package` `completed` 三步、`applied`；`Registry is valid.`；`verify-audit` valid、11 個事件；`get-record` 有 `verified` 的 by／at 與 `proven_by`；套用 commit 已簽章，push 到本機 bare remote：hook 印 `Git governance is valid for 2 commits.`、`[new branch]`。
- D3c Recovery 步驟 1–3（D4 的起點）：簽章接手、`ready`、`Git governance is valid for 1 commit.`；179 passed；`Registry is valid.`；verify-audit 66 個事件；verify-evidence 99／31／32（exit 1，預期）。
- D4 檢查點 1：`verify-sources` stale、exit 1，NOTE 如上；changed_sources 是 docs/adr、src、tests，content_changed 是 docs/requirements；verify-evidence exit 1；verify-audit valid；coverage 已審查 16 條、proven 16；stale 規則 GROUP-001、GROUP-PAY-002、MEMBER-004、ORDER-002、REFUND-004，抽 GROUP-001 的 `proven_by` 測試照跑通過；`git status --short` 沒有變動。另外在同一處跑 `probe`：印出 1.2.6 的新句子、exit 1。

回報給維護者：
- 15 秒的 git／ssh-keygen 逾時：教室的 Windows 若有防毒掃描或 OneDrive 同步，`git verify-commit`、`ssh-keygen` 偶爾可能超過 15 秒；演練中都沒有逾時。逾時時只印 `ERROR: Command '[...]' timed out after 15 seconds`，沒有說可以重跑，也不能調整秒數。
- `probe` 的過期句把 `changed_sources` 一律說成「sources moved」：D3c 之後 docs/adr、src、tests 是多了新檔案，不是搬移；只改內容的 docs/requirements 也沒有出現在句子裡。
- `init-domain-memory` 的旗標組合大多在 CLI 先擋下、什麼都不建；只有通過 CLI 檢查、卻被政策驗證拒絕的情況（例如空白的 `--exclude`）才走到 1.2.7 的清除路徑。

未驗證：macOS 實機（這次學員頁只改版本字串，沒有 macOS 專屬指令改動）；git 逾時本身（沒有在教室等級的慢機器上重現）。

## domain-memory 1.2.18（patch）（2026-10-19）

由 1.2.8 換成 1.2.18（SkillHub `f76ca1e54`，以 `git archive` 匯出），使用者指定為工作坊前的穩定版；維護者同意工作坊結束前只通知學員路徑的缺陷。維護者的檢查在匯出上重跑：ruff 全部通過；`run_tests.py --jobs 4` 42 個模組，failed: none。指令仍 63 個；新增執行期檔案 `git.py`、`search.py`、`locate.py`（維護者摘要說 1.2.14 檔數不變，實為多了 `locate.py`），Plugin 97 個檔案，學員核對改印 `SHA OK 98 files`。不需遷移，沒有用到 Maintainer 金鑰。

DLC 的改動：
- 版本字串與 `SHA OK 98 files`。
- `dmlib.env()` 在學員沒設定時給 `DOMAIN_MEMORY_GIT_TIMEOUT=60`（教室機器的防毒或 OneDrive 會拖慢 `git verify-commit`、`ssh-keygen`）；已設定的值優先；有測試。push 時的 pre-push hook 不經過 dmlib，仍是 15 秒，主持指南常見問題第 20 條寫明。
- `dmlib --save`：指令沒有輸出（被拒絕）時不再留下空檔、也不再說「輸出已存到」；有測試。
- 主持指南常見問題第 19 條列出學員 D2 會遇到的兩種過期原因；第 20 條說明逾時訊息與調整方式。
- D2 檢查點 4 的 ③ 接受任何 revision（重新定基後是 revision 2）。
- 誤打 `--registry-root`：課程沒有任何提示叫 Agent 在找不到時建立 Domain Memory，只有 D1 檢查點 2 會 init，dmlib 一律補 `--registry-root domain-memory`；1.2.14 起拒絕訊息改成先檢查參數並建議正確路徑，演練中沒有建出第二個 Registry。

相容性檢查：32 PASS、0 CHANGED；`QUOTED` 73 → 79（兩種過期原因、逾時訊息的片段、`must be a positive number of seconds`）。

演練（Windows，兩個隔離沙箱，候選包 `62ca9530171475fd`，結束後刪除）：開場檢查點 1–4（`SHA OK 98 files`、1.2.18）；D1 Recovery 162／0／0；D2 檢查點 1–6（17 個 obligation、applied、11 個事件、push `for 2 commits.`）；過期情境得到 `commit … does not hold the Registry at domain-memory/registry …`，`rebase-proposal` 後 revision 2、重新核准與簽章、applied、push `for 3 commits.`；誤打 `domain-memry` 時 validate、probe、confirm-sources 都建議 `domain-memory`，沒有建立任何資料夾；D3c Recovery 99／31／32、66 個事件；D4 檢查點 1 coverage 已審查 16、proven 16；回顧檢查點 2 precision 1.0、copied 52、independent 5／5；`DOMAIN_MEMORY_GIT_TIMEOUT=abc` 被拒，`0.001` 逾時並說 `nothing was written, so it is safe to run again`。

回報給維護者：檔數；`git ls-files '*source-map.json'` 也會比對到 `foo-source-map.json`；validate 的建議是絕對路徑、probe 與 confirm-sources 是相對路徑；pre-push hook 無法套用外層預設逾時。

未驗證：macOS 實機。
