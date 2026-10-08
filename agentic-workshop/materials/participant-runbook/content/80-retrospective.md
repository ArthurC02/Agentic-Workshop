---
id: retrospective
title: 工作坊回顧
minute: 80-90
group: retro
section: 回顧
---

# 回顧：用實際證據看責任的變化

用 **10 分鐘**回看今天的三個階段：人和 Agent 各做了什麼、哪些做法有效、問題的根因，最後留下一項有責任人的改善行動。先個人、再小組。本段**沒有 Agent 操作**；每個檢查點的「確認」就是你自己寫下的紀錄。

```callout warning
用證據回顧，不排名、不編數據
- 每一格寫本次的具體例子；沒觀察到就填「未觀察」。未觀察或未完成如實保留，不強填每格。
- 不排名、不比程式碼量。成熟度指工作安排與責任配置，不是人員排名或工具產品能力榜。
- 沒有活動計時，不以 pytest 執行秒數代替人員工作時間；沒有可比較基準，不編造效率或 Agent 自主完成的比例。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**；要寫什麼全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 個人記錄 | 80–82 | 00–02 | 自己填「工作坊回顧紀錄」第 1 部分：三個階段人和 Agent 各做什麼、B3 Level |
| 2 · 小組比較 | 82–86 | 02–06 | 對照成熟度比較，填「你的比較證據」與回顧紀錄第 2 部分 |
| 3 · 收斂改善 | 86–89 | 06–09 | 收斂有證據的 1–3 項改善，填回顧紀錄第 3 部分 |
| 4 · 行動與匯出 | 89–90 | 09–10 | 至少一項改善寫明責任人與驗證；匯出所有表單 |

## 檢查點 1 · 個人記錄（第 80–82 分鐘）

先自己寫，不討論。

- [ ] 翻出今天留下的紀錄：Greenfield 各檢查點確認與交付摘要、個人分析與 Shared Context、B3 的 Gate 紀錄與 Delivery Summary。
- [ ] 在下方「工作坊回顧紀錄」填**第 1 部分**：Tool／從零開發、Teammate／分析與共用背景資料、Digital Worker／依核准範圍執行三個階段，人和 Agent 各做了什麼，以及具體證據或未完成。
- [ ] 填小組、B3 實際完成程度與治理證據。Level 與治理表現分開寫；若切換過接續版本（Recovery），寫原成果／缺項、版本來源與切換時間，使用接續版本不代表小組自行完成。
- [ ] 第 82 分鐘前，至少寫下一個真實例子或缺口。

第 2、3 部分先留空，在檢查點 2、3 回來填。

```include
zip=participant-80-retrospective.zip path=agentic-workshop/05-retrospective/participant/reflection-sheet.md
```

### 填寫：工作坊回顧紀錄

```form
{"id": "reflection", "title": "工作坊回顧紀錄","fields":[
{"id": "s1-tool-human", "label": "1. 本次成果與責任｜工具角色／從零開發｜人的主要工作", "type": "textarea", "hint": "請用實際證據回顧，不排名、不比程式碼量；沒觀察到就填「未觀察」。", "suggestions": [{"label": "人做的事", "text": "〈下指令／審查／測試／決策〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-tool-agent", "label": "1. 本次成果與責任｜工具角色／從零開發｜Agent 的主要工作", "type": "textarea", "suggestions": [{"label": "Agent 做的事", "text": "〈產生程式／測試／文件〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-tool-evidence", "label": "1. 本次成果與責任｜工具角色／從零開發｜具體證據／未完成", "type": "textarea", "suggestions": [{"label": "證據", "text": "證據：〈檔案／測試輸出／表單紀錄〉"}, {"label": "未完成", "text": "未完成：〈項目〉，原因：〈原因〉"}]},
{"id": "s1-teammate-human", "label": "1. 本次成果與責任｜隊友角色／分析與共用背景資料｜人的主要工作", "type": "textarea", "suggestions": [{"label": "人做的事", "text": "〈比對分析／整理共識／核准〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-teammate-agent", "label": "1. 本次成果與責任｜隊友角色／分析與共用背景資料｜Agent 的主要工作", "type": "textarea", "suggestions": [{"label": "Agent 做的事", "text": "〈讀程式／整理規則／提出假設〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-teammate-evidence", "label": "1. 本次成果與責任｜隊友角色／分析與共用背景資料｜具體證據／未完成", "type": "textarea", "suggestions": [{"label": "證據", "text": "證據：〈Shared Context／分析紀錄／測試輸出〉"}, {"label": "未完成", "text": "未完成：〈項目〉，原因：〈原因〉"}]},
{"id": "s1-dw-human", "label": "1. 本次成果與責任｜數位員工角色／依核准範圍執行｜人的主要工作", "type": "textarea", "suggestions": [{"label": "人做的事", "text": "〈Gate 核准／審查 Diff／處理例外〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-dw-agent", "label": "1. 本次成果與責任｜數位員工角色／依核准範圍執行｜Agent 的主要工作", "type": "textarea", "suggestions": [{"label": "Agent 做的事", "text": "〈依 Work Order 執行／測試／交付摘要〉：〈具體例子〉"}, "未觀察"]},
{"id": "s1-dw-evidence", "label": "1. 本次成果與責任｜數位員工角色／依核准範圍執行｜具體證據／未完成", "type": "textarea", "suggestions": [{"label": "證據", "text": "證據：〈Gate 紀錄／Delivery Summary／測試輸出〉"}, {"label": "未完成", "text": "未完成：〈項目〉，原因：〈原因〉"}]},
{"id": "s1-team", "label": "1. 本次成果與責任｜小組", "type": "text"},
{"id": "s1-b3-level", "label": "1. 本次成果與責任｜B3 實際完成程度", "type": "text", "hint": "Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付與治理表現分開記錄。若切換接續版本（Recovery），寫原成果／缺項、版本來源與切換時間；使用接續版本不代表小組自行完成任務。", "suggestions": [{"label": "Level", "text": "Level 〈1／2／3〉"}, {"label": "有切換接續", "text": "Level 〈1／2／3〉；原成果／缺項：〈…〉；接續版本來源：〈…〉，第〈分〉分切換"}]},
{"id": "s1-governance-evidence", "label": "1. 本次成果與責任｜治理證據", "type": "textarea", "suggestions": [{"label": "Gate 紀錄", "text": "Gate 〈1／2／3〉：〈決策〉，核准人〈姓名〉"}, {"label": "例外處理", "text": "例外：〈情況〉→ 升級給〈誰〉，決策：〈…〉"}, "未觀察"]},
{"id": "s2-practice-what", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜實務／問題與發生階段", "type": "textarea", "suggestions": [{"label": "實務與階段", "text": "〈實務〉（發生於〈Greenfield／分析／B1／B2／B3〉）"}]},
{"id": "s2-practice-evidence", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜證據／影響", "type": "textarea", "hint": "沒有活動計時，不以 pytest 執行秒數代替人員工作時間；沒有可比較基準，不編造效率或自主率。", "suggestions": [{"label": "證據與影響", "text": "證據：〈紀錄／輸出〉；影響：〈…〉"}, "未觀察"]},
{"id": "s2-practice-why", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜為何有效或可能根因", "type": "textarea", "suggestions": [{"label": "為何有效", "text": "有效原因：〈…〉"}, {"label": "假設", "text": "假設（未驗證）：〈…〉"}]},
{"id": "s2-practice-pending", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜有效實務｜尚待驗證", "type": "textarea", "suggestions": [{"label": "待驗證", "text": "待驗證：〈…〉，驗證方式：〈…〉"}, "無"]},
{"id": "s2-issue-what", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜實務／問題與發生階段", "type": "textarea", "suggestions": [{"label": "問題與階段", "text": "〈問題〉（發生於〈Greenfield／分析／B1／B2／B3〉）"}]},
{"id": "s2-issue-evidence", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜證據／影響", "type": "textarea", "suggestions": [{"label": "證據與影響", "text": "證據：〈紀錄／輸出〉；影響：〈…〉"}, "未觀察"]},
{"id": "s2-issue-why", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜為何有效或可能根因", "type": "textarea", "hint": "根因可分為需求、提示、背景資料、規則或技能缺口、Agent 錯誤、人員審查缺口、工具或環境問題；假設未驗證要標清楚。", "suggestions": [{"label": "根因分類", "text": "可能根因：〈需求／提示／背景資料／規則或技能缺口／Agent 錯誤／人員審查缺口／工具或環境〉；依據：〈…〉"}, {"label": "假設", "text": "假設（未驗證）：〈…〉"}]},
{"id": "s2-issue-pending", "label": "2. 有效實務與問題根因（各選有證據的 1–3 項）｜問題與根因｜尚待驗證", "type": "textarea", "suggestions": [{"label": "待驗證", "text": "待驗證：〈…〉，驗證方式：〈…〉"}, "無"]},
{"id": "s3-context-what", "label": "3. 改善與後續驗證｜背景資料｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, "待研究"]},
{"id": "s3-context-owner", "label": "3. 改善與後續驗證｜背景資料｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-context-next", "label": "3. 改善與後續驗證｜背景資料｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]},
{"id": "s3-rule-what", "label": "3. 改善與後續驗證｜規則｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, "待研究"]},
{"id": "s3-rule-owner", "label": "3. 改善與後續驗證｜規則｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-rule-next", "label": "3. 改善與後續驗證｜規則｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]},
{"id": "s3-skill-what", "label": "3. 改善與後續驗證｜技能（含不宜自動化的工作）｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, {"label": "不宜自動化", "text": "不宜自動化：〈工作〉，原因：〈需人判斷的部分〉"}, "待研究"]},
{"id": "s3-skill-owner", "label": "3. 改善與後續驗證｜技能（含不宜自動化的工作）｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-skill-next", "label": "3. 改善與後續驗證｜技能（含不宜自動化的工作）｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]},
{"id": "s3-process-what", "label": "3. 改善與後續驗證｜流程／檢查點｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, "待研究"]},
{"id": "s3-process-owner", "label": "3. 改善與後續驗證｜流程／檢查點｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-process-next", "label": "3. 改善與後續驗證｜流程／檢查點｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]},
{"id": "s3-platform-what", "label": "3. 改善與後續驗證｜平台｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, "待研究"]},
{"id": "s3-platform-owner", "label": "3. 改善與後續驗證｜平台｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-platform-next", "label": "3. 改善與後續驗證｜平台｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]},
{"id": "s3-governance-what", "label": "3. 改善與後續驗證｜治理／人員責任｜要改善什麼／保留何種證據", "type": "textarea", "suggestions": [{"label": "改善與證據", "text": "改善：〈…〉；連回：〈Gate／例外／檢查點紀錄〉"}, "待研究"]},
{"id": "s3-governance-owner", "label": "3. 改善與後續驗證｜治理／人員責任｜責任人", "type": "text", "suggestions": [{"label": "責任人", "text": "〈姓名〉"}, "待研究"]},
{"id": "s3-governance-next", "label": "3. 改善與後續驗證｜治理／人員責任｜下一步與驗證方式／期限", "type": "textarea", "suggestions": [{"label": "下一步", "text": "下一步：〈…〉；驗證：〈用什麼證據確認〉；期限：〈日期〉"}, "待研究"]}
]}
```

## 檢查點 2 · 小組比較（第 82–86 分鐘）

下方比較表原文以 Tool、Teammate、Digital Worker 表示工具、隊友、數位員工三種角色（Agent 從工具、隊友到能獨立執行任務的數位員工）；比較的是工作安排與責任配置。

- [ ] 小組對照比較表，比較三個階段的責任、有效做法與問題。意見不同時，分清事實、假設、證據與根因；不要把程式碼量當成果。
- [ ] 填下方「你的比較證據」五題，每題寫本次的具體例子；沒觀察到就填「未觀察」。
- [ ] 回到檢查點 1 的「工作坊回顧紀錄」，填**第 2 部分**：有效實務與問題根因，各選有證據的 1–3 項。根因可分為需求、提示、背景資料、規則或技能缺口、Agent 錯誤、人員審查缺口、工具或環境問題；假設未驗證要標清楚。
- [ ] 第 86 分鐘收斂成有證據的 1–3 項，不強填滿。

```include
zip=participant-80-retrospective.zip path=agentic-workshop/05-retrospective/participant/maturity-comparison.md
```

### 填寫：你的比較證據

```form
{"id": "maturity", "title": "Tool → Teammate → Digital Worker比較：你的比較證據","fields":[
{"id": "useful-context", "label": "哪些背景資料實際幫上忙？", "type": "textarea", "hint": "填本次具體例子；沒觀察到就填「未觀察」。", "suggestions": [{"label": "有用背景", "text": "〈背景資料〉：在〈階段〉幫助〈…〉（證據：〈紀錄〉）"}, "未觀察"]},
{"id": "rule-gate-decision", "label": "哪條規則或哪個核准關卡改變了決策？", "type": "textarea", "suggestions": [{"label": "改變決策", "text": "〈Rule ID／Gate〉：原本〈…〉，因此改為〈…〉（證據：〈紀錄〉）"}, "未觀察"]},
{"id": "skill-vs-human", "label": "哪類工作適合交給技能處理，哪類仍需人判斷？", "type": "textarea", "suggestions": [{"label": "分工範本", "text": "適合技能處理：〈…〉\n仍需人判斷：〈…〉，原因：〈…〉"}, "未觀察"]},
{"id": "review-rework", "label": "哪些審查或重工增加／減少？是否有計時證據？", "type": "textarea", "hint": "未觀察不推測數據。", "suggestions": [{"label": "增減與證據", "text": "〈增加／減少〉：〈審查或重工項目〉；計時證據：〈有／無〉"}, "未觀察，無計時證據"]},
{"id": "platform-retain", "label": "平台應保存哪些背景資料、對話工作階段、權限與測試資訊？", "type": "textarea", "suggestions": [{"label": "應保存項", "text": "背景資料：〈…〉\n對話工作階段：〈…〉\n權限：〈…〉\n測試資訊：〈…〉"}, "未觀察"]}
]}
```

## 檢查點 3 · 收斂改善（第 86–89 分鐘）

- [ ] 把小組的改善想法分到六類：背景資料（Context）、規則（Rule）、技能（Skill，含不宜自動化的工作）、流程／檢查點、平台、治理／人員責任。
- [ ] 選有證據的 1–3 項，在檢查點 1 的「工作坊回顧紀錄」**第 3 部分**填「要改善什麼／保留何種證據」。每一項都連回今天實際的 Gate、例外或檢查點紀錄。
- [ ] 只想到「Agent 更聰明」時，改問自己：可以改哪份背景資料、哪個 Gate，或哪個可驗證的控制？
- [ ] 第 89 分鐘停止新議題。沒討論到的、還待驗證的，寫進第 2 部分的「尚待驗證」。

```callout tip
怎麼選
有證據時，盡量涵蓋一項背景資料或規則的改善、一項技能或流程的需求、一項平台需求。沒有證據的類別留白即可。
```

## 檢查點 4 · 行動與匯出（第 89–90 分鐘）

- [ ] 從第 3 部分選**至少一項**寫完整：「責任人」與「下一步與驗證方式／期限」。要具體到說得出誰、何時、用什麼證據確認。
- [ ] 其他項目可以標「待研究」，不編造未觀察結果。
- [ ] 匯出所有表單（見下方「最後提醒」）。

### 最後提醒：匯出所有表單

```callout warning
離開前請匯出所有表單
表單只暫存在這個瀏覽器中。更換瀏覽器、使用私密視窗或清除瀏覽資料可能讓內容消失。按下方按鈕一次下載整場所有已填寫的表單（ZIP，每份表單一個 `.md` 檔），再依主持人指定方式交付或保存。
```

```exportall
```

下載後打開 ZIP 內的 `README.md`，確認下列內容都在（未填寫的表單會列在最後）：

- [ ] Greenfield：[各檢查點確認](#greenfield)、[交付摘要](#gf-submission)
- [ ] Time Skip：[各檢查點確認](#time-skip)
- [ ] Brownfield 分析：[個人 Agent 分析](#individual-analysis)、[Shared Context](#shared-context)
- [ ] [B1](#b1)、[B2](#b2) 各段頁面中的表單（有填寫時）
- [ ] B3：[各檢查點確認](#b3)、[Work Order](#b3-work-order)、[Gate 1／2／3 決策紀錄](#b3-approval-gates)、[Review Checklist](#b3-review-checklist)、[Exception Response 與 Escalation](#b3-exception-card)（有使用時）
- [ ] Delivery：[Delivery Summary 與檢查點 2 確認](#delivery)
- [ ] 回顧：本頁的工作坊回顧紀錄與你的比較證據

更自主仍須範圍、品質與可追溯；責任重新分配，不消失。
