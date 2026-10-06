---
id: retrospective
title: 工作坊回顧
minute: 80-90
group: retro
section: 回顧
---

# 回顧：用實際證據看責任的變化

請用實際證據回顧，不排名、不比程式碼量；沒觀察到就填「未觀察」。成熟度指工作安排與責任配置，不是人員排名或工具產品能力榜。

| 全場第幾分鐘 | 做什麼 |
|---|---|
| 80–82 | 個人記錄 |
| 82–86 | 小組比較 |
| 86–89 | 收斂有證據的改善 |
| 89–90 | 確認至少一項可執行行動與責任人 |

- [ ] 80–82：個人記錄，用實際證據填寫下方「工作坊回顧紀錄」；沒觀察到就填「未觀察」。
- [ ] 82–86：小組比較，參考本頁下方的成熟度比較，用實際證據說明至少一項責任或協作方式的變化，填寫「你的比較證據」。
- [ ] 86–89：收斂有證據的改善。
- [ ] 89–90：確認至少一項可執行行動與責任人。
- [ ] 匯出所有表單（見頁尾「最後提醒」）。

未觀察或未完成如實保留，不強填每格。

## 工作坊回顧紀錄

```include
zip=participant-80-retrospective.zip path=agentic-workshop/05-retrospective/participant/reflection-sheet.md
```

### 填寫：工作坊回顧紀錄

```form
{"id":"reflection","title":"工作坊回顧紀錄","fields":[
{"id":"s1-tool-human","label":"1. 本次成果與責任｜工具角色／從零開發｜人的主要工作","type":"textarea","hint":"請用實際證據回顧，不排名、不比程式碼量；沒觀察到就填「未觀察」。"},
{"id":"s1-tool-agent","label":"1. 本次成果與責任｜工具角色／從零開發｜Agent 的主要工作","type":"textarea"},
{"id":"s1-tool-evidence","label":"1. 本次成果與責任｜工具角色／從零開發｜具體證據／未完成","type":"textarea"},
{"id":"s1-teammate-human","label":"1. 本次成果與責任｜協作夥伴角色／分析與共用背景資料｜人的主要工作","type":"textarea"},
{"id":"s1-teammate-agent","label":"1. 本次成果與責任｜協作夥伴角色／分析與共用背景資料｜Agent 的主要工作","type":"textarea"},
{"id":"s1-teammate-evidence","label":"1. 本次成果與責任｜協作夥伴角色／分析與共用背景資料｜具體證據／未完成","type":"textarea"},
{"id":"s1-dw-human","label":"1. 本次成果與責任｜數位工作者角色／依核准範圍執行｜人的主要工作","type":"textarea"},
{"id":"s1-dw-agent","label":"1. 本次成果與責任｜數位工作者角色／依核准範圍執行｜Agent 的主要工作","type":"textarea"},
{"id":"s1-dw-evidence","label":"1. 本次成果與責任｜數位工作者角色／依核准範圍執行｜具體證據／未完成","type":"textarea"},
{"id":"s1-team","label":"1. 本次成果與責任｜小組","type":"text"},
{"id":"s1-b3-level","label":"1. 本次成果與責任｜B3 實際完成程度","type":"text","hint":"Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付與治理表現分開記錄。若切換接續版本（Recovery），寫原成果／缺項、版本來源與切換時間；使用接續版本不代表小組自行完成任務。"},
{"id":"s1-governance-evidence","label":"1. 本次成果與責任｜治理證據","type":"textarea"},
{"id":"s2-practice-what","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜實務／問題與發生階段","type":"textarea"},
{"id":"s2-practice-evidence","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜證據／影響","type":"textarea","hint":"沒有活動計時，不以 pytest 執行秒數代替人員工作時間；沒有可比較基準，不編造效率或自主率。"},
{"id":"s2-practice-why","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜為何有效或可能根因","type":"textarea"},
{"id":"s2-practice-pending","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜尚待驗證","type":"textarea"},
{"id":"s2-issue-what","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜實務／問題與發生階段","type":"textarea"},
{"id":"s2-issue-evidence","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜證據／影響","type":"textarea"},
{"id":"s2-issue-why","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜為何有效或可能根因","type":"textarea","hint":"根因可分為需求、提示、背景資料、規則或技能缺口、Agent 錯誤、人員審查缺口、工具或環境問題；假設未驗證要標清楚。"},
{"id":"s2-issue-pending","label":"2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜尚待驗證","type":"textarea"},
{"id":"s3-context-what","label":"3. 改善與後續驗證｜背景資料｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-context-owner","label":"3. 改善與後續驗證｜背景資料｜責任人","type":"text"},
{"id":"s3-context-next","label":"3. 改善與後續驗證｜背景資料｜下一步與驗證方式／期限","type":"textarea"},
{"id":"s3-rule-what","label":"3. 改善與後續驗證｜規則｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-rule-owner","label":"3. 改善與後續驗證｜規則｜責任人","type":"text"},
{"id":"s3-rule-next","label":"3. 改善與後續驗證｜規則｜下一步與驗證方式／期限","type":"textarea"},
{"id":"s3-skill-what","label":"3. 改善與後續驗證｜技能（含不宜自動化的工作）｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-skill-owner","label":"3. 改善與後續驗證｜技能（含不宜自動化的工作）｜責任人","type":"text"},
{"id":"s3-skill-next","label":"3. 改善與後續驗證｜技能（含不宜自動化的工作）｜下一步與驗證方式／期限","type":"textarea"},
{"id":"s3-process-what","label":"3. 改善與後續驗證｜流程／檢查點｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-process-owner","label":"3. 改善與後續驗證｜流程／檢查點｜責任人","type":"text"},
{"id":"s3-process-next","label":"3. 改善與後續驗證｜流程／檢查點｜下一步與驗證方式／期限","type":"textarea"},
{"id":"s3-platform-what","label":"3. 改善與後續驗證｜平台｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-platform-owner","label":"3. 改善與後續驗證｜平台｜責任人","type":"text"},
{"id":"s3-platform-next","label":"3. 改善與後續驗證｜平台｜下一步與驗證方式／期限","type":"textarea"},
{"id":"s3-governance-what","label":"3. 改善與後續驗證｜治理／人員責任｜要改善什麼／保留何種證據","type":"textarea"},
{"id":"s3-governance-owner","label":"3. 改善與後續驗證｜治理／人員責任｜責任人","type":"text"},
{"id":"s3-governance-next","label":"3. 改善與後續驗證｜治理／人員責任｜下一步與驗證方式／期限","type":"textarea"}
]}
```

## 工具 → 協作夥伴 → 數位工作者的比較

原文以 Tool、Teammate、Digital Worker 表示這三種角色；比較的是工作安排與責任配置。

```include
zip=participant-80-retrospective.zip path=agentic-workshop/05-retrospective/participant/maturity-comparison.md
```

### 填寫：你的比較證據

```form
{"id":"maturity","title":"Tool → Teammate → Digital Worker比較：你的比較證據","fields":[
{"id":"useful-context","label":"哪些背景資料實際幫上忙？","type":"textarea","hint":"填本次具體例子；沒觀察到就填「未觀察」。"},
{"id":"rule-gate-decision","label":"哪條規則或哪個核准關卡改變了決策？","type":"textarea"},
{"id":"skill-vs-human","label":"哪類工作適合交給技能處理，哪類仍需人判斷？","type":"textarea"},
{"id":"review-rework","label":"哪些審查或重工增加／減少？是否有計時證據？","type":"textarea","hint":"未觀察不推測數據。"},
{"id":"platform-retain","label":"平台應保存哪些背景資料、對話工作階段、權限與測試資訊？","type":"textarea"}
]}
```

## 最後提醒：匯出所有表單

```callout warning
離開前請匯出所有表單
表單只暫存在這個瀏覽器中。更換瀏覽器、使用私密視窗或清除瀏覽資料可能讓內容消失。請在每份表單按「匯出 Markdown」下載 `.md` 檔，或按「複製 Markdown」，再依主持人指定方式交付或保存。
```

請逐一確認已匯出：

- [ ] Greenfield：[交付摘要](#gf-submission)
- [ ] Brownfield 分析：[個人 Agent 分析](#individual-analysis)、[Shared Context](#shared-context)
- [ ] [B1](#b1)、[B2](#b2) 各段頁面中的表單（有填寫時）
- [ ] B3：[Work Order](#b3-work-order)、[Gate 1／2／3 決策紀錄](#b3-approval-gates)、[Review Checklist](#b3-review-checklist)、[Exception Response 與 Escalation](#b3-exception-card)（有使用時）
- [ ] Delivery：[Delivery Summary](#delivery)
- [ ] 回顧：本頁的工作坊回顧紀錄與你的比較證據

更自主仍須範圍、品質與可追溯；責任重新分配，不消失。
