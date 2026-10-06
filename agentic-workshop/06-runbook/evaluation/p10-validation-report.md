# P10 主持、回顧與評估整合驗證報告

> 讀者：主持人、Evaluation與素材維護者。時機：P10驗收、P11規劃前。
> 前置：P0–P9已驗收，依[07產製指令](../../../docs/instructions/07_主持Runbook與回顧整合產製指令書.md)。可見性：Evaluation限定。

## 產出與驗收範圍

本輪補齊主持整合指令，產製總控要求的四份回顧材料與四份Runbook，增加評估索引、本報告及[JSON證據](p10-validation-evidence.json)，共11份輸出。靜態驗證已通過，**P10文件基線PASS**；實際Preflight、Recovery包生成／演練及90分鐘工作坊仍待P11。

| 類型 | 文件 |
|---|---|
| 學員回顧 | [Reflection](../../05-retrospective/participant/reflection-sheet.md)、[Maturity Comparison](../../05-retrospective/participant/maturity-comparison.md) |
| 主持回顧 | [Debrief](../../05-retrospective/facilitator/debrief-guide.md)、[組織導入](../../05-retrospective/facilitator/organization-adoption-prompts.md) |
| 評估整合 | [十段Evaluation Index](../../05-retrospective/evaluation/workshop-evaluation-index.md) |
| 主持準備與執行 | [主Runbook](../workshop-runbook.md)、[Environment](../environment-setup.md)、[Preflight](../preflight-checklist.md)、[Recovery](../recovery-plan.md) |

## 時程與人機責任

主流程00–07／07–29／29–33／33–39／39–44／44–52／52–63／63–76／76–80／80–90，連續無重疊共90分鐘；Time Skip、Brownfield及交付收斂為51分鐘，B3包含13分鐘、回顧10分鐘。

Greenfield個人、人主導與Agent協助；Time Skip統一B0，先個人Agent分析再小組Shared Context；B1／B2人Agent共同決策，B3人只Challenge／Review／Approve／Reject，Agent受核准範圍主導。唯一SQLite事件在69–70分鐘，含在13分鐘中，不另增時。

## 發放、提示與復原

依Shared Context→B1→B2→Operating Rules／Work Order與B3順序分批發放。每段有Cue、觀察、提示條件、停止及降級；時間到保留原成果與缺項，不要求人員補程式。

52分鐘接續B2的Recovery來源為B1，63分鐘接續B3來源為B2。主持保留成果、錯誤、來源版本、時間與新Session／Context確認。G1只供必要受控主持示範，B3答案不在63分鐘供學員作起點。

Recovery採白名單程式／測試／設定與精選業務文件，生成角色安全說明；排除Evaluation報告／完整目錄、答案索引、Bundle、版本歷史、未來版本與隱藏Git／cache／環境。包尚未產生，P11必須核對相對連結與內容／歷史；若受控起點未備妥或驗證不齊，採分析／Review降級，不直接發Evaluation。

## 環境、Preflight與版本Gate

文件提供Python3.13、獨立venv／pip、固定依賴、`src` Import Path、Uvicorn及pytest步驟，保持無必要前端、外部DB／API、真實金流。本機案例與Agent服務可用性分別準備，無新增產品專屬必要操作。

| 版本 | Preflight必須核對的既有基線 |
|---|---|
| G0 | 1 passed／8受控Skip，11主要TODO；Health可用，未實作不得冒稱完成 |
| G1 | 28全部通過、無Skip／XFail |
| B0 | 一個BUG-B0-001，五Manifest失敗／其餘39通過，node ID集合精確一致、零未知；不當一般全綠 |
| B1 | 44全部通過，五受控失敗恢復 |
| B2 | 55全部通過，政策遷移有記錄 |
| B3 | 75全部通過，團體原子性與付款補償 |

每版既有Warning已識別；未知失敗或Warning先核實，不用刪弱測試／Skip／XFail避開。上述是先前已驗收結果及本次文件中的核對標準，本次沒有重跑各版程式測試，也沒有執行Preflight清單。

## 回顧、評估與差異對齊

80–82個人、82–86小組、86–89收斂、89–90行動共10分鐘。記錄有效實務、問題根因、Context／Rule／Skill／流程／平台／治理改善、責任人與後續驗證。沒有活動量測記未觀察，不用pytest秒數代替人員時間。

評估索引對十段列目的、Input、Artifact、AC、提示、內部答案或接受範圍及驗證來源。完整Reference DoD與學員Level1–3分開，P9五維治理Rubric不以程式量或競賽排名取代；Recovery不記為小組自行完成。

O-01在新素材以90分鐘與個人→混合小組對齊，不強制contents中的一日／半日與跨角色輪轉；O-02區分Reference完整驗收、有限時間學員成果與治理證據。兩項完成文件對齊，實際演練驗證條件保留到P11，原參考文件與決策歷史不覆寫。

## 靜態檢查與限制

實際核對11份輸出（10 Markdown＋1 JSON），131個相對連結有效，UTF-8無BOM／Markdown區塊平衡、Participant內容與連結隔離通過；90分鐘連續區間、唯一事件、B3的59來源檔及P9的17文件雜湊全部核對一致。具體數字見JSON證據；獨立子代理Review檢查時程、Recovery、版本Gate、環境操作與評估定位。

正式Participant／Facilitator／Evaluation包、Recovery輸出、實際環境Preflight、2分鐘閱讀、60秒事件、13分鐘B3與90分鐘真人演練皆未執行。文件計畫與內容隔離不等同正式包或實際活動通過。

完成條件：11份整合輸出、來源與時程／責任／隔離／評估一致，**P10文件基線PASS**。P11尚未啟動，不宣稱整套工作坊已完成演練交付。
