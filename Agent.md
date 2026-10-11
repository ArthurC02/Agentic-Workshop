# Agent 工作指引

> 目標讀者：協助本 Repo 規劃與產製素材的 Coding Agent。
> 使用時機：開始任務、切換產製階段或接手既有工作時。
> 前置條件：閱讀本文件、使用者本次指示及任務涉及的規格；改教材前先讀 `.claude/skills/course-authoring/SKILL.md`。

## 1. 專案目標

本 Repo 產製 **Agentic Software Development Evolution Workshop** 的教材、程式案例、主持指南、評估與交付素材：90 分鐘主課與 DLC 延伸課程（DDD），固定案例 Smart Ticket Platform，學習主線 **Tool → Teammate → Digital Worker**。

優先順序（2026-10-09 起）：

1. 練習 Agentic Coding 技巧（每段標示一個技巧；主課埋入六項：Prompt 結構、Structured Output、Skill、Token 節費、模型選擇、推論強度）。
2. 體驗 Agentic SDLC：三階段差在人怎麼介入（逐步、核准計畫、只在 Gate）。
3. 萃取組織導入方法與治理需求：由 Agent 寫進 `notes/`、`skills/`，不靠學員填表。

學員規則：對象是資淺工程師，全程**不寫、不讀程式，也不打指令**；指令與程式都交給 Agent，學員只做決定、核准與依證據驗收。素材保持工具中立，不要求特定廠商的指令、設定檔、Plan Mode 或 Subagent 功能。

## 2. 指示與規格的適用順序

1. 使用者於目前對話中的明確指示與已授權範圍。
2. 使用者已核准的規格變更（記在[決策與待協調事項](docs/planning/decisions-and-open-issues.md)）。
3. [素材產製總控指令書](docs/instructions/00_Agentic工作坊素材產製總控指令書.md)。
4. `docs/instructions/` 中與本次任務相關的指令書；一致性修正依 [09](docs/instructions/09_教材一致性修正與交付重驗指令書.md)，驗證與打包依 [08](docs/instructions/08_全域驗證與受控打包產製指令書.md)，主持簡報與學員 Runbook 依 [10](docs/instructions/10_主持簡報與學員Runbook產製指令書.md)。
5. `docs/contents/` 的概念、流程與範本；`docs/planning/` 的結構、路線與決策紀錄，以及本文件。

本文件是工作入口，不取代詳細規格。發現衝突時記錄來源、影響與建議；不得默默修改商業規則或測試期待值。

## 3. 文件入口

| 要確認的資訊 | 文件入口 |
|---|---|
| Repository 結構與產製進度 | [結構規劃](docs/planning/repository-structure.md)、[產製路線](docs/planning/production-roadmap.md) |
| 已核准決策、衝突與待辦 | [決策與待協調事項](docs/planning/decisions-and-open-issues.md) |
| 主持簡報與學員 Runbook 建置／操作 | [Materials 操作說明](agentic-workshop/materials/README.md) |
| 獨立操作教學內容 | [Speech 說明](agentic-workshop/materials/speech/README.md) |
| 發布流程、打包、驗證工具與證據 | [工具說明](scripts/README.md) 與各階段 `evaluation/` |
| 規格、案例與驗收證據查找 | [決策與驗證參考索引](docs/planning/agent-work-history.md) |

本文件只維護持續適用的規範與入口，不追加日期日誌、Commit、測試耗時或逐輪驗收摘要。

## 4. Repo 結構

| 位置 | 用途 |
|---|---|
| `docs/contents/`、`docs/instructions/`、`docs/planning/` | 既有概念與範本、產製規格、規劃與決策 |
| `agentic-workshop/00-governance/`–`06-runbook/` | 主課素材：治理、G0／G1、Time Skip、B0–B3、Digital Worker、回顧、主持流程與 Recovery |
| `agentic-workshop/07-dlc-ddd/` | DLC 素材、工具與 Recovery |
| `agentic-workshop/materials/`、`materials-dlc/` | 主課與 DLC 的主持簡報、學員 Runbook 原稿與成品；`materials/speech/` 為獨立操作教學 |
| `scripts/` | 檢查、建置、打包、驗證與發布工具 |
| `.claude/` | Agent 工具正本：Skills、Workflows、Hook（見 §8.2） |
| `dist/`、`.codex-tmp/` | 生成的候選包與本機環境，排除於 Git 追蹤之外 |

教材依 `participant/`、`facilitator/`、`evaluation/` 分層；資料夾分層不等於權限隔離。

## 5. 工作坊故事線與版本

Greenfield 為個人活動；時間快轉後所有人改用統一 B0。Brownfield 先由每位成員用自己的 Agent 獨立分析，再由小組建立 Shared Context，選定主要 Agent 執行。

| 版本 | 定位 | 預期測試狀態 |
|---|---|---|
| G0 | 可啟動的骨架；保留 MVP 實作任務 | Health 通過；未完成功能可明確 Skip |
| G1 | 查詢班次、訂票、模擬付款與查詢訂單的完整 MVP | 全部通過，無 Skip／XFail |
| B0 | 從 G1 演化，增加會員、優惠、改退票、通知、座位與 Audit | 一個刻意 Bug，失敗集合與已核實 Manifest 一致，保留完整 Regression |
| B1 | 修復學生票 85% 錯誤，恢復正確 75% | 全部通過，無 Skip／XFail |
| B2 | 不疊加優惠，逐位旅客選最有利單一優惠 | 全部通過，無 Skip／XFail |
| B3 | 5–20 人團體訂票、同車廂連續座位與付款失敗補償 | 全部通過，無 Skip／XFail |

各版本須能獨立安裝、啟動與測試；不得在 G0、G1 或 B0 提前實作後續任務答案。B3 中人員只做 Challenge、Review、Approve／Reject 及要求補充證據。`materials/speech/` 與 90 分鐘流程的整合需由使用者另行安排。

## 6. 技術與資料基線

- Python 3.13、FastAPI、Pydantic 2、pytest、Uvicorn；`venv`、`pip`、`requirements.txt` 與 `src/smart_ticket/` layout。
- API、Application、Domain、Infrastructure、Schemas 輕量分層；Domain 不依賴 FastAPI 或 HTTP。
- Persistence 固定 In-Memory Repository；Fixture、Clock 與付款結果可控制及重置。
- 不新增必要前端、外部資料庫、外部 API、付費服務、微服務或 Kubernetes；不使用真實個資、付款資訊或憑證。
- 不以隨機失敗、當日日期或測試順序製造教學難度。

## 7. 產製方式

1. 確認授權範圍，先讀總控與本階段規格，整理輸入、輸出、規則及完成條件。
2. 依存順序：治理基線 → 技術基線 → G0 → G1 → Time Skip／B0 → B1–B3 → Digital Worker 治理 → 回顧與 Runbook → 全域驗證與打包；不得一次產製所有素材。
3. 同步維護 Requirement、Rule ID、Code、Test、Document 與 Evaluation 的追溯關係。
4. 完成一致性與答案洩漏檢查、執行驗證後回報；刪除因本次修改而過時、矛盾或重複的內容，不只新增。

## 8. 驗證與交付

- 不將預期結果寫成已執行結果；不刪除、弱化或隱藏測試。B0 僅一個受控 Bug；B1 須恢復全部 G1 Regression 及 B0 新增測試。
- 「凍結」以行為驗證為準（G0–B3 測試數、受控 Skip、B0 精確失敗集合與 Smoke 不變）；來源可改，但須完整驗證、重新釘選 Manifest 並重建候選（見 [08](docs/instructions/08_全域驗證與受控打包產製指令書.md)）。
- Participant 不得含標準答案、完整影響分析、主持提示或 Evaluation 文件；學員只拿成品 HTML 或單檔 ZIP，以活動碼解鎖。B1／B2 Recovery 使用獨立碼，B3 不提供解答。
- 只改建置來源，不手改生成檔：兩版 `runbook.html`／`facilitator-deck.html`、Speech `greenfield-deck.html`／`greenfield-handout.md`、`dist/`、腳本寫出的驗證證據；Hook 會擋下。
- 真人演練與正式放行須查核實際紀錄，不以文件或程式測試通過代稱完成。

### 8.1 改完教材後的發布流程

改動 `agentic-workshop/**`、`docs/**`、本文件、`scripts/README.md` 或 `.claude/skills/**` 後，執行：

```powershell
uv run --no-project --python 3.13 python -X utf8 scripts/release_materials.py
```

它依序做 Agent 工具同步檢查、知識點出處、台灣繁體中文、檢查點四區塊、簡報與 Runbook 對應檢查，再驗證、釘選、建置與驗證主課及 DLC 候選，重建兩版教材與 Speech，跑單元測試，最後印出 `RELEASE PIPELINE PASS`。各步驟見[工具說明](scripts/README.md)。通過後**不需詢問**：DLC 與主課分開 Commit，再 Push 到 `main`。失敗處理見 `release-materials` Skill。

### 8.2 Agent 工具（`.claude/` 為正本）

- Skills（`.claude/skills/`）：`course-authoring`（寫作標準，改教材前必讀）、`release-materials`（發布流程）、`curriculum-review`（內外迴圈審查）、`rehearsal`（以候選包實跑提示詞）、`fact-check`（對照權威文件查證說明）、`plain-language-review`（白話化與縮寫）。
- Workflows（`.claude/workflows/`）：`curriculum-review`、`rehearsal`、`wording-pass`，以 `scope`（main／dlc）整版平行執行。
- Hook `guard_generated.py`：擋下手改生成檔。
- Codex 鏡像：`.agents/skills/` 與 `.codex/hooks/` 由 `scripts/sync_harness.py` 從 `.claude/` 逐位元組複製；不要手改鏡像，改正本後重跑。

## 9. 寫作規則摘要（細節見 `course-authoring`）

- 一律台灣繁體中文（繁體字＋台灣詞彙，`scripts/check_zh_tw.py` 檢查）；技術識別字與 API 可用英文，重要術語首次出現時補白話說明。
- 絕對必要：每頁、每段、每句都要通過「少了它，學員會不會在某一步失敗或卡住？」否則刪除。
- 每個檢查點四區塊：① 為什麼做這一步、② 貼給 Agent、③ 確認結果（Agent 只回「成功」或「失敗：原因」，再附「失敗時」補救提示詞）、④ 補充（可省略）。含作業系統差異的提示詞用 ```prompt 區塊，分 Windows／macOS 分頁。
- 主持簡報投影只做兩件事：掌握節奏、告訴學員下一步；其餘放講者備註。每個 Runbook 檢查點對應一張簡報頁，`data-title` 必須等於「檢查點 N · 名稱」，由 `scripts/check_deck_runbook.py` 檢查。
- 保留每個檔案原有的換行格式；保留使用者既有變更，不做與授權任務無關的重構。
- 權限提示或封鎖出現時停下回報，不得繞過。

## 10. 決策與回報

規格衝突、核准結果與待處理差異維護在[決策與待協調事項](docs/planning/decisions-and-open-issues.md)；歷次驗證原始結果保留在對應 `evaluation/`，不得改寫舊證據。學員成果、標準實作驗收、治理表現與真人演練分開判定。

完成回報包含修改檔案、完成內容、實際驗證、規格一致性及已知限制。每次完成目標，先審視本文件是否需要更新，再依 §8.1 提交與推送。

## 完成條件

Agent 能說明本 Repo 的目標、規格來源、版本演化、可見性隔離、驗證責任與發布流程，並依使用者授權完成對應產出。
