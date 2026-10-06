---
id: individual-analysis
title: 個人 Agent 分析
minute: 33-39
group: timeskip
section: Brownfield｜Teammate
---

# 個人 Agent 分析

這是 **6 分鐘的個人**任務。請各自使用自己的 Agent 理解同一份 B0，把結果記錄成可比較的成果，供第 39 分鐘的小組比較使用。Agent 在此階段是 **Teammate**：協助你分析 Repository、影響、風險與缺口，判斷仍由你負責。

```callout danger
此階段不修改程式
個人分析階段不得修改程式。不要讓 Agent 修改、刪除或弱化任何程式與測試；只閱讀、執行測試與記錄。
```

## 步驟

- [ ] 閱讀 [B0 系統 Context 與已知限制](#b0-context)，以及 Repository 的 `README.md`、`docs/architecture.md` 與 ADR。
- [ ] 在 B0 資料夾開啟新的 Agent Session，把下方通用要求交給你的 Agent。
- [ ] 執行 `pytest -q` 並保留實際輸出；記錄規則來源與推論依據。
- [ ] 填寫下方個人 Agent 分析表，區分事實與推論。
- [ ] 匯出或複製 Markdown，準備在 [Shared Context](#shared-context) 與小組比較。

通用要求：

```text
先不要修改程式，理解Repository與測試。列出有證據的結論、假設、資訊缺口與調查順序，說明各項依據。
```

```cmd
# powershell
& '.\.venv\Scripts\python.exe' -m pytest -q
# bash
.venv/bin/python -m pytest -q
```

```callout tip
不要只列檔名
說明模組責任、依賴與可能影響，並為每個關鍵結論附上來源（程式、測試或文件）。Agent 的結論若沒有證據，請標示為假設。
```

## 個人 Agent 分析表

```include
zip=participant-33-analysis.zip path=agentic-workshop/03-brownfield/participant/03-individual-analysis-sheet.md
```

### 線上填寫

```form
{
  "id": "individual-analysis",
  "title": "個人 Agent 分析表",
  "fields": [
    {"id": "modules", "label": "系統模組摘要／依賴", "type": "textarea"},
    {"id": "failing-tests", "label": "失敗測試及實際輸出", "type": "textarea"},
    {"id": "root-cause-hypotheses", "label": "可能根因／替代假設", "type": "textarea", "hint": "區分事實與推論"},
    {"id": "affected-files", "label": "受影響檔案與理由", "type": "textarea"},
    {"id": "rule-ids", "label": "相關Rule ID與來源", "type": "textarea"},
    {"id": "cross-evidence", "label": "程式／測試／文件的交叉證據", "type": "textarea"},
    {"id": "gaps", "label": "資訊缺口／待問問題", "type": "textarea"},
    {"id": "investigation-order", "label": "建議調查順序", "type": "textarea"},
    {"id": "risks", "label": "風險／不宜修改區域", "type": "textarea"}
  ]
}
```

## 完成檢核

- [ ] 已保留可追查的分析成果供小組比較。
- [ ] 沒有把未執行的測試或未驗證的根因描述為已證實。
- [ ] 尚未修改任何程式或測試。
