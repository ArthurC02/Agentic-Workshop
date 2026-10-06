# Agent 工作指引

> 目標讀者：協助本 Repo 規劃與產製素材的 Coding Agent。
> 使用時機：開始任務、切換產製階段或接手既有工作時。
> 前置條件：閱讀本文件、使用者本次指示及任務涉及的規格。

## 1. 專案目標

本 Repo 用於產製 **Agentic Software Development Evolution Workshop** 的教材、程式案例、主持指南、評估與交付素材。

- 固定案例：Smart Ticket Platform。
- 工作坊長度：90 分鐘。
- 對象：一般工程師，不預設高階架構或演算法能力。
- 學習主線：**Tool → Teammate → Digital Worker**。
- 優先目標：體驗 Agentic SDLC、萃取組織導入方法與治理需求、練習通用 Coding Agent 操作。
- 素材保持工具中立，不要求特定廠商的指令、設定檔、Plan Mode 或 Subagent 功能。

## 2. 指示與規格的適用順序

在遵守執行環境與上層指示的前提下，依下列順序處理專案要求：

1. 使用者於目前對話中的明確指示與已授權範圍。
2. 使用者已核准的規格變更。
3. [素材產製總控指令書](docs/instructions/00_Agentic工作坊素材產製總控指令書.md)。
4. `docs/instructions/` 中與本次任務相關的產製指令書；教材一致性修正依 [09](docs/instructions/09_教材一致性修正與交付重驗指令書.md)，全域驗證與打包依 [08](docs/instructions/08_全域驗證與受控打包產製指令書.md)，主持簡報與學員 Runbook 依 [10](docs/instructions/10_主持簡報與學員Runbook產製指令書.md)。
5. `docs/contents/` 的概念、流程、範本與參考內容。
6. `docs/planning/` 的結構、路線與決策紀錄，以及本文件。

本文件是工作入口，不取代詳細規格。規劃中的建議不等同「已核准變更」。發現衝突時，記錄來源、影響與建議；不得默默修改商業規則或測試期待值。

## 3. 工作範圍與文件入口

依使用者本次授權處理指定素材，不自行啟動其他產製階段或整套重製。進度、已核准決策與驗證證據各有維護位置：

| 要確認的資訊 | 文件入口 |
|---|---|
| Repository 結構 | [結構規劃](docs/planning/repository-structure.md) |
| 產製階段與進度 | [產製路線](docs/planning/production-roadmap.md) |
| 已核准決策、衝突與待辦 | [決策與待協調事項](docs/planning/decisions-and-open-issues.md) |
| 主持簡報與學員 Runbook 建置／操作 | [Materials 操作說明](agentic-workshop/materials/README.md) |
| 教材對齊、版面與閱讀問題 | [教材交叉審查](agentic-workshop/materials/cross-review-2026-10-06.md) |
| 獨立操作教學內容 | [Speech 說明](agentic-workshop/materials/speech/README.md) |
| 打包、驗證工具與證據 | [工具說明](scripts/README.md) 與各階段 `evaluation/` |
| 規格、案例與驗收證據查找 | [決策與驗證參考索引](docs/planning/agent-work-history.md) |

本文件只維護持續適用的工作規範與入口，不追加日期日誌、Commit／Tag、測試耗時、檔案數或逐輪驗收摘要。真人演練與正式放行必須查核實際紀錄，不以文件或程式測試通過代稱完成。

## 4. Repo 結構與文件責任

| 位置 | 用途 |
|---|---|
| `docs/contents/` | 既有工作坊概念、流程與範本 |
| `docs/instructions/` | 素材產製規格 |
| `docs/planning/` | 目錄規劃、產製路線與待協調事項 |
| `agentic-workshop/00-governance/` | Manifest、Glossary、一致性規則與驗收 Gate |
| `agentic-workshop/01-greenfield/` | G0 Starter Kit、G1 標準實作及相關教材 |
| `agentic-workshop/02-time-skip/` | 12 個月時間快轉與交接素材 |
| `agentic-workshop/03-brownfield/` | B0、分階段任務卡、B1–B3 標準實作 |
| `agentic-workshop/04-digital-worker/` | 工作命令、核准 Gate、Review、例外事件與治理評估 |
| `agentic-workshop/05-retrospective/` | 回顧與組織導入收斂 |
| `agentic-workshop/06-runbook/` | 主持流程、環境準備、Preflight 與復原方案 |
| `agentic-workshop/materials/` | 主持簡報、單檔學員 Runbook 與獨立操作教學原稿／成品 |
| `scripts/` | 驗證與打包工具 |
| `dist/` | 生成的交付包，排除於 Git 追蹤之外 |
| `.codex-tmp/` | 本機虛擬環境、檢查副本與暫存，排除於 Git 追蹤之外 |

教材依 `participant/`、`facilitator/`、`evaluation/` 分層。產製指令留在 `docs/instructions/`，避免多份規格副本失去同步。

## 5. 工作坊故事線與版本

Greenfield 為個人活動；時間快轉後，所有人改用統一 B0。Brownfield 先由每位成員使用自己的 Agent 獨立分析，再由小組建立 Shared Context，選定主要 Agent 執行。

| 版本 | 定位 | 預期測試狀態 |
|---|---|---|
| G0 | 可啟動的骨架；提供型別、方法簽章與受控 TODO，保留 MVP 實作任務 | Health 通過；未完成功能可明確 Skip |
| G1 | 查詢班次、訂票、模擬付款與查詢訂單的完整 MVP | 全部通過，無 Skip／XFail |
| B0 | 從 G1 演化，增加會員、優惠、改退票、通知、座位與 Audit | 一個刻意Bug，所有失敗與已核實manifest一致；零非預期失敗，保留完整Regression |
| B1 | 修復學生票 85% 錯誤，恢復正確 75% | 全部通過，無 Skip／XFail |
| B2 | 不疊加優惠，逐位旅客選最有利單一優惠 | 全部通過，無 Skip／XFail |
| B3 | 5–20 人團體訂票、同車廂連續座位與付款失敗補償 | 全部通過，無 Skip／XFail |

各版本須能獨立安裝、啟動與測試，並保留合理演化關係。不得在 G0、G1 或 B0 提前實作後續任務答案。

B3 中人員只進行 Challenge、Review、Approve／Reject 及要求補充證據，不直接補寫程式或測試。學員成果可分為分析完成、核心流程完成、完整交付三個等級；標準實作仍須符合完整驗收規格。

`materials/speech/` 為獨立的概念與操作教學；與 90 分鐘主持流程的整合需由使用者另行安排，不自行追加議程或合併教材。

## 6. 技術與資料基線

- Python 3.13、FastAPI、Pydantic 2、pytest、Uvicorn。
- 使用 `venv`、`pip`、`requirements.txt` 與 `src/smart_ticket/` layout。
- 採 API、Application、Domain、Infrastructure、Schemas 的輕量分層。
- Domain 不依賴 FastAPI 或 HTTP；Router 不承擔票價、座位與交易狀態規則。
- Persistence 固定使用 In-Memory Repository；Fixture、Clock 與付款結果必須可控制及重置。
- 不新增必要前端、外部資料庫、外部 API、付費服務、微服務或 Kubernetes。
- 不使用真實個資、付款資訊、品牌內部資料或憑證。
- 不以隨機失敗、當日日期或測試順序製造教學難度。

## 7. 產製方式

1. 確認使用者授權範圍，檢查當前檔案與相關文件。一般文件工作直接讀寫檔案，只有任務需要版本控制時才使用 Git，避免反覆查詢狀態。
2. 先閱讀總控與本階段規格，整理輸入、輸出、規則及完成條件。
3. 確認上階段驗證通過，再產製本階段內容。
4. 同步維護 Requirement、Rule ID、Code、Test、Document 與 Evaluation 的追溯關係。
5. 執行適合本階段的驗證，記錄實際結果與未完成事項。
6. 完成一致性與答案洩漏檢查後，回報成果。

產製依存順序為：治理基線 → 技術基線 → G0 → G1 → Time Skip／B0 → B1–B3 → Digital Worker 治理 → 回顧與 Runbook → 全域驗證、時間演練與打包。所需指令書應先補齊；不得一次產製所有素材。

## 8. 驗證與交付

實際建立程式版本時，須驗證依賴安裝、App 載入、`/health`、OpenAPI、pytest 及本版本核心 API Smoke Test。典型指令如下；必須在對應版本根目錄依其 README 的 Import Path 設定執行：

```text
python --version
python -m pip install -r requirements.txt
pytest -q
uvicorn smart_ticket.main:app --app-dir src --reload
```

- 不將預期結果寫成已執行結果，也不聲稱未執行的測試通過。
- B0 僅注入一個受控 Bug；所有實測失敗node ID須與已核實manifest集合一致，其餘通過，無Skip／XFail。B1須恢復全部28項G1 Regression及B0新增測試；新增未知失敗不得交付。
- 不刪除、弱化或隱藏測試以符合通過率或失敗數量要求。
- Participant 不得含標準答案、完整影響分析、主持提示或 Evaluation 文件。
- 資料夾分層不等於權限隔離；學員交付包應採明確允許清單，排除正式答案及可暴露答案的 Git History。
- B1／B2／B3 任務按時段揭露；Materials 學員版只發成品 HTML 或單檔 ZIP，以活動碼解鎖，原稿不發學員。B1／B2 Recovery 使用獨立碼，由主持人於 52／63 分鐘按需核准，保留原成果與切換紀錄；一般活動碼不開 Recovery，B3 開始後不換版，也不提供 B3 解答。
- 規劃文件修改以內容、一致性、連結及 Diff 檢查驗證，不需為純文字變更安裝應用依賴。

### 8.1 Clone 後生成 `dist`

`dist/` 與 `.codex-tmp/` 均由 `.gitignore` 排除，不需提交或 Push。已提交的主持簡報與學員 Runbook HTML 可直接離線開啟；重新建置 Runbook 或打包學員 HTML 時，才需要下列候選包。

前置條件：取得完整作者 Repo，安裝 Python 3.13，確認 `python --version` 為 3.13，並在 Repo 根目錄執行。以下建置／打包工具只使用 Python 標準函式庫，不需要現有 `.codex-tmp/b3-env`，也不需安裝案例的 FastAPI 等依賴；案例執行與完整技術驗證另需各版本的獨立環境。

1. **生成受控候選包**：來源與雜湊由 `scripts/package-manifest.json` 明確指定。

   ```powershell
   python --version
   python -X utf8 scripts/build_delivery.py
   ```

   輸出為 `dist/p11-candidate/<Manifest雜湊前16碼>/`，含各角色／時段 ZIP 與 `build-evidence.json`。同名目錄已存在時會停止，不覆寫；不要為了重建刪除不明生成物。相同 Manifest 的重新生成請使用另一個乾淨工作區；既有包的重驗方式見 [打包與驗證工具說明](scripts/README.md)。若來源雜湊不符，先核對變更與允許清單，不為了讓建置通過而直接重設雜湊。

2. **重建並核對教材 HTML**：必須先有上一個步驟的候選包。

   ```powershell
   python -X utf8 scripts/build_materials.py
   python -X utf8 scripts/build_materials.py --check
   ```

   更新 `agentic-workshop/materials/facilitator-deck/facilitator-deck.html` 與 `agentic-workshop/materials/participant-runbook/runbook.html`。候選 ID 以 `scripts/build_materials.py` 的 `CANDIDATE_ID` 為準；建置器輸出的目錄須與此 ID 一致。若已核准的 Manifest 改變，須審查並同步候選 ID 與教材說明，不直接改用任意 ZIP。此文件本身也屬打包來源，因此不在此寫死候選 ID，避免修改 ID 再次改變 Manifest 雜湊。

3. **生成學員單檔交付 ZIP**：工具會重新核對 Runbook 與來源是否一致；成品過期時先完成步驟 2。

   ```powershell
   python -X utf8 scripts/package_materials.py
   ```

   輸出 `dist/materials/participant-materials.zip`，精確只含 `runbook.html`，可重新生成並覆寫同名學員 ZIP。只發此 ZIP 或成品 HTML，不發作者 Repo、原稿、整個 `dist/` 或主持／評估包。

完成條件：候選包生成成功、教材 `--check` 通過、學員 ZIP 只含成品 HTML。生成成功不代表案例測試、Recovery、現場 Preflight 或真人演練已通過；完整驗證另依 [scripts/README.md](scripts/README.md) 與 [Materials 操作說明](agentic-workshop/materials/README.md) 執行。

## 9. 決策與待協調事項的維護

規格衝突、核准結果、尚待處理的差異及解除條件，統一維護在 [決策與待協調事項](docs/planning/decisions-and-open-issues.md)，不在本文件複製進度表。歷次驗證的原始結果保留在對應 `evaluation/`，不得改寫舊證據來表示新一輪已通過。

學員成果、標準實作驗收、治理表現與真人演練須分開判定；未完成或未觀察如實保留。查找規格與證據時可使用 [決策與驗證參考索引](docs/planning/agent-work-history.md)，各報告的歷史結論不得代替目前授權與狀態。

## 10. 文件與回報要求

- 主持簡報預設整頁顯示，細節表格、操作步驟、規則與揭曉頁不逐項消耗翻頁按鍵；只有需要分段引導的概念／角色轉換頁，才明確以 `data-fragments="step"` 啟用逐步顯示，避免打斷主持節奏。
- 預設繁體中文；技術識別字與 API 可用英文。
- 簡報投影文字以自然中文說明，重要術語首次出現時補充意思；保留 API、Rule ID 與任務編號。區分全場時間與段落經過時間、一般活動碼與復原碼、核准決策與功能驗收；分析成果、測試通過及完整交付不可互相代稱。講者備註須與投影內容一致，來源逐字引用與主持補充說明分清。
- Runbook 沿用相同用詞；改寫表單時保留頁面、群組、表單與欄位識別字及選項值，以維持既有暫存資料。凍結候選的引用原文與程式 ZIP 不改寫，補充說明寫在章節中；更新後重建 HTML 與只含成品的學員 ZIP。
- 文件開頭列出目標讀者、使用時機與前置條件，結尾列出產出物或完成條件。
- 學員文件簡潔可操作；主持文件包含時間點、觀察、提示與停止條件；評估文件使用可判定標準。
- 完成回報包含修改檔案、完成內容、實際驗證、規格一致性及已知限制。
- 保留使用者既有變更，避免與授權任務無關的整理或重構。

## 11. 目標完成後的收尾流程

使用者已授權：每次完成目標，先審視 `Agent.md` 是否需要更新；若不需要，直接執行 Git Commit。

1. 先確認目標產出與必要驗證已完成。
2. 審視本文件的目前範圍、工作方式與規格摘要是否需要更新；需要時先完成更新，不做無實質內容的修改。
3. 將本次目標相關且已檢查的變更提交為本機 Git Commit；若有更新本文件，一併提交。
4. 不將使用者無關變更納入提交；若沒有可提交的變更，據實回報。
5. 完成回報提供 Commit 識別碼與摘要。此授權不包含自動 Push。

這是使用者指定的收尾動作，不需每次重新詢問提交許可；目標執行途中仍避免不必要的 Git 狀態查詢。

## 完成條件

Agent 能說明本 Repo 的目標、規格來源、目前範圍、版本演化、可見性隔離、驗證責任及待協調問題，並依使用者授權完成對應產出。
