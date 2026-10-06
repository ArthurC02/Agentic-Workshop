---
id: shared-context
title: Shared Context：小組比較分析
minute: 39-44
group: timeskip
section: Brownfield｜Teammate
---

# Shared Context：整理小組共同背景

這是 **5 分鐘的小組**任務。請比較每位成員的個人分析，整理出共同事實、證據與分歧，選定主要 Agent 與人員核准者，再把整理後的共同 Context 交給主要 Agent。

```callout warning
B1 尚未揭露
這時尚未揭露 B1，不要求提出或核准任務修改計畫，也不修改程式。共同背景記錄已確認的事實與待決事項；不代表已取得修改程式的授權。
```

## 步驟

- [ ] 比較每位成員的 [個人 Agent 分析表](#individual-analysis)：共同事實、證據與分歧。
- [ ] 對仍有分歧的判斷，寫下驗證方式；未確認的推論清楚標示。
- [ ] 選定主要 Agent 與人員核准者。
- [ ] 把整理後的共同 Context 交給主要 Agent；不要把所有人的 Session 原封不動拼接。
- [ ] 只填寫下方表單的共同欄位；「任務揭露後補填」欄位留到第 44 分鐘取得 B1 後再填。

## Shared Context 範本

```include
zip=participant-39-shared-context.zip path=agentic-workshop/03-brownfield/participant/04-shared-context-template.md
```

### 在本頁填寫（不需連線）

前六個欄位在第 39–44 分鐘填寫。標示「任務揭露後補填」的欄位，請在第 44 分鐘取得 B1 任務後再填；沒有核准或證據仍不足時先補缺口，不修改程式。

```form
{
  "id": "shared-context",
  "title": "Shared Context",
  "fields": [
    {"id": "common-facts", "label": "共同事實與規則來源", "type": "textarea"},
    {"id": "verified-evidence", "label": "已驗證證據（檔案／測試／輸出）", "type": "textarea"},
    {"id": "disagreements", "label": "仍有分歧的判斷及驗證方式", "type": "textarea"},
    {"id": "constraints", "label": "已知限制／不宜修改區域", "type": "textarea", "hint": "記錄系統限制，不預先核准修改"},
    {"id": "main-agent-approver", "label": "主要Agent與人員核准者", "type": "textarea"},
    {"id": "pending-decisions", "label": "尚待任務揭露後決定的事項", "type": "textarea"},
    {"id": "b1-task-source", "label": "【任務揭露後補填】任務ID／起點版本／規則來源", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-scope", "label": "【任務揭露後補填】任務範圍／不處理項目", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-change-areas", "label": "【任務揭露後補填】建議修改區域、理由及不應修改區域", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-test-plan", "label": "【任務揭露後補填】測試計畫／Regression保留", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-plan", "label": "【任務揭露後補填】主要Agent的5–8步執行計畫", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-approver", "label": "【任務揭露後補填】人員核准紀錄：核准人", "type": "text", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-approved-at", "label": "【任務揭露後補填】人員核准紀錄：時間", "type": "text", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-decision", "label": "【任務揭露後補填】人員核准紀錄：結論", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"},
    {"id": "b1-conditions", "label": "【任務揭露後補填】人員核准紀錄：條件", "type": "textarea", "hint": "第44分鐘取得B1任務後填寫"}
  ]
}
```

## 完成檢核

- [ ] 已留下共同事實、來源、分歧、限制、主要 Agent 及待決事項。
- [ ] 未確認的推論已清楚標示。
- [ ] 在第39–44分鐘尚未提出或核准任務修改計畫，也未修改程式；第44分鐘任務揭露後，另補範圍、計畫與核准，不以共同背景代替授權。
