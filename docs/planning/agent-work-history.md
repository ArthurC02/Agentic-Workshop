# 決策與驗證參考索引

> 目標讀者：素材維護者與接手者。
> 使用時機：確認規格依據、查找驗證證據及判斷驗收範圍。
> 前置條件：閱讀 [Agent 工作指引](../../Agent.md)。

本文件依主題整理原先散落在 Agent.md 的參考資料。工作規範由 Agent.md 維護；決策狀態與測試結果請查閱下列來源，避免多處摘要失去同步。

## 規格與決策

| 要確認的事項 | 判讀重點 | 參考來源 |
|---|---|---|
| 時程與角色安排 | 工作坊採 90 分鐘演化式活動；其他時長的概念素材需另行安排 | [總控規格](../instructions/00_Agentic工作坊素材產製總控指令書.md)、[決策與待協調事項](decisions-and-open-issues.md) |
| Python 與案例技術基線 | 各案例使用統一技術基線；安裝與執行依各版本 README | [Agent 技術基線](../../Agent.md#6-技術與資料基線) |
| B0 的刻意錯誤與失敗判定 | 一個受控 Bug 可影響多項測試；失敗集合須符合 Manifest，其餘通過，B1 須全部恢復 | [B0 Gate 提案](b0-regression-gate-proposal.md)、[B0 驗證報告](../../agentic-workshop/03-brownfield/evaluation/01-b0-validation-report.md) |
| Rule ID 與版本來源 | 沿用規則 Registry；來源副本、案例歷史與版本差異以正式證據核對 | [決策與待協調事項](decisions-and-open-issues.md)、[B0 歷史與副本證據](../../agentic-workshop/03-brownfield/evaluation/05-case-history-and-copy-evidence.md) |
| 學員交付與答案隔離 | 依時段揭露任務；Recovery 須主持人核准；學員只收允許的成品 | [教材一致性規格](../instructions/09_教材一致性修正與交付重驗指令書.md)、[Materials 操作說明](../../agentic-workshop/materials/README.md) |
| 獨立操作教學 | Speech 的用途、操作步驟與驗證另有文件；與主議程的整合需使用者安排 | [Speech 說明](../../agentic-workshop/materials/speech/README.md)、[Greenfield 教學驗證](../../agentic-workshop/materials/speech/01-greenfield/validation-report.md) |

## 案例驗證

| 案例 | 查閱內容 | 報告與證據 |
|---|---|---|
| G0／G1 | 骨架的受控 TODO、MVP 功能與測試基線 | [G0 報告](../../agentic-workshop/01-greenfield/evaluation/03-g0-validation-report.md)、[G1 報告](../../agentic-workshop/01-greenfield/evaluation/04-g1-validation-report.md) |
| B0 | 受控失敗、API 行為與來源副本一致性 | [驗證報告](../../agentic-workshop/03-brownfield/evaluation/01-b0-validation-report.md)、[來源證據](../../agentic-workshop/03-brownfield/evaluation/05-case-history-and-copy-evidence.md) |
| B1 | 學生票修復與既有行為保留 | [驗證報告](../../agentic-workshop/03-brownfield/evaluation/12-b1-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/13-b1-validation-evidence.json)、[版本差異](../../agentic-workshop/03-brownfield/evaluation/14-b1-case-history-and-delta.md) |
| B2 | 逐位旅客選最有利單一優惠、不疊加優惠 | [驗證報告](../../agentic-workshop/03-brownfield/evaluation/15-b2-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/16-b2-validation-evidence.json)、[版本差異](../../agentic-workshop/03-brownfield/evaluation/17-b2-case-history-and-delta.md) |
| B3 | 團體訂票、連續座位與付款失敗補償 | [驗證報告](../../agentic-workshop/03-brownfield/evaluation/18-b3-validation-report.md)、[實測證據](../../agentic-workshop/03-brownfield/evaluation/19-b3-validation-evidence.json)、[版本差異](../../agentic-workshop/03-brownfield/evaluation/20-b3-case-history-and-delta.md) |

標準實作的整體判定見 [B1–B3 素材驗收](../../agentic-workshop/03-brownfield/evaluation/21-b1-b3-production-result.md)。測試數字、耗時、Commit、Tag 與檔案雜湊直接查原始證據，不在本索引重複摘錄。

## 治理、教材與交付驗證

| 查閱目的 | 文件入口 |
|---|---|
| Work Order、Operating Rules、人員 Gate 與例外事件的一致性 | [治理驗證報告](../../agentic-workshop/04-digital-worker/evaluation/06-governance-validation-report.md) |
| 主持流程、回顧與時間配置 | [Runbook 文件驗證](../../agentic-workshop/06-runbook/evaluation/p10-validation-report.md) |
| 全域技術驗證、受控打包與 Recovery | [全域驗證報告](../../agentic-workshop/06-runbook/evaluation/p11-validation-report.md)、[工具說明](../../scripts/README.md) |
| 答案隔離、任務揭露與教學語意修正 | [一致性修正報告](../../agentic-workshop/06-runbook/evaluation/consistency-correction-report.md) |
| 主持簡報與單檔學員 Runbook | [Materials 驗證報告](../../agentic-workshop/materials/validation-report.md)、[教材交叉審查](../../agentic-workshop/materials/cross-review-2026-10-06.md) |

## 驗收結果的解讀

案例測試通過、文件一致性、學員活動成果、治理 Gate 核准及真人演練是不同的驗收項目。標準實作通過不代表學員已交付，候選包生成成功也不代表正式發布已獲核准。

判讀報告時，先確認其驗證對象、來源版本、候選包與實際執行範圍。報告中的未執行項目描述該次驗證；後續是否完成，須查核對應的新證據，不改寫舊報告，也不以階段編號推定目前狀態或授權。

## 完成條件

維護者能按問題找到規格、決策與驗證來源，並區分素材驗收、學員成果與正式放行的依據。
