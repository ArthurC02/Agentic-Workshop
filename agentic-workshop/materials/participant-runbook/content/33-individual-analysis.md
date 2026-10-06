---
id: individual-analysis
title: 個人 Agent 分析
minute: 33-39
group: timeskip
section: Brownfield｜Teammate
---

# 個人 Agent 分析

這是 **6 分鐘的個人**任務。請各自使用自己的 Agent 理解同一份 B0，把結果記錄成可比較的成果，供第 39 分鐘的小組比較使用。Agent 在此階段是 **Teammate**：協助你分析 Repository、影響、風險與缺口，判斷仍由你負責。

```callout warning
此階段不修改程式
個人分析階段不得修改程式。不要讓 Agent 修改、刪除或弱化任何程式與測試；只閱讀、執行測試與記錄。Agent 說的每個結論，你要分清楚是**事實**（有程式、測試或文件可查）還是**推論**，並記下證據。本段分成 2 個檢查點，每個檢查點結束時 Agent 必須停下，等你核對。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要貼給 Agent 的提示詞、要填的欄位，全部在本頁。本段內容已在第 29 分鐘解鎖，不需要另外輸入解鎖碼。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 理解 B0 與測試 | 33–36 | 00–03 | 讀 Context、開新 Session；Agent 說明模組後停下；你自己跑 `pytest -q` |
| 2 · 證據與推論 | 36–39 | 03–06 | Agent 列結論、假設、缺口與調查順序後停下；你核對來源，填完分析表 |

兩個檢查點都填同一張個人 Agent 分析表（在本頁下方）。

## 檢查點 1 · 理解 B0 與測試（第 33–36 分鐘）

- [ ] 閱讀 [B0 系統 Context 與已知限制](#b0-context)，以及 Repository 的 `README.md`、`docs/architecture.md` 與 ADR。
- [ ] 在 B0 資料夾開啟**新的** Agent Session，把下方提示詞貼給你的 Agent。

```text
先不要修改程式，理解Repository與測試。請閱讀 README.md、docs/architecture.md 與 ADR，說明各模組的責任與依賴（不要只列檔名），然後執行 pytest -q 並貼出實際輸出。先不要推論失敗原因，做完停下等我確認。
```

- [ ] 自己執行 `pytest -q`，保留實際輸出。

```cmd
# powershell
& '.\.venv\Scripts\python.exe' -m pytest -q
# bash
.venv/bin/python -m pytest -q
```

- [ ] Agent 停下後核對：它貼的測試輸出和你自己跑的一致嗎？模組摘要有沒有說出責任與依賴，而不是只列檔名？
- [ ] Agent 若已經開始修改檔案，請它立刻停下並還原，回到只讀狀態。

**確認**：填下方分析表第 1 欄「系統模組摘要／依賴」、第 2 欄「失敗測試及實際輸出」。第 2 欄貼**你自己執行**的輸出。

## 檢查點 2 · 證據與推論（第 36–39 分鐘）

- [ ] 把下方提示詞貼給 Agent：

```text
先不要修改程式，理解Repository與測試。列出有證據的結論、假設、資訊缺口與調查順序，說明各項依據。
每一項標示是「事實」（附程式、測試或文件的位置）還是「推論」（說明推論依據）；另外列出可能受影響的檔案與理由、相關 Rule ID 與來源、風險與不宜修改的區域。不要修改任何檔案，列完停下等我確認。
```

- [ ] 從 Agent 的結論中挑一個關鍵的，自己打開它引用的程式、測試或文件核對；對不上或找不到來源，就改標為推論。
- [ ] 未執行的測試、未驗證的根因，不寫成已證實；查不清楚的寫進「資訊缺口／待問問題」。
- [ ] 填完分析表第 3–9 欄。
- [ ] 第 39 分鐘停止。匯出或複製 Markdown，準備在 [Shared Context](#shared-context) 與小組比較。

```callout tip
不要只列檔名
說明模組責任、依賴與可能影響，並為每個關鍵結論附上來源（程式、測試或文件）。Agent 的結論若沒有證據，請標示為假設。
```

**確認**：分析表第 3 欄「可能根因／替代假設」、第 4 欄「受影響檔案與理由」、第 5 欄「相關 Rule ID 與來源」、第 6 欄「程式／測試／文件的交叉證據」、第 7 欄「資訊缺口／待問問題」、第 8 欄「建議調查順序」、第 9 欄「風險／不宜修改區域」。

## 個人 Agent 分析表

檢查點 1 填第 1–2 欄，檢查點 2 填第 3–9 欄。

```include
zip=participant-33-analysis.zip path=agentic-workshop/03-brownfield/participant/03-individual-analysis-sheet.md
```

### 線上填寫

```form
{"id": "individual-analysis", "title": "個人 Agent 分析表","fields":[
{"id": "modules", "label": "系統模組摘要／依賴", "type": "textarea", "suggestions": [{"label": "模組責任", "text": "〈模組〉：負責〈責任〉，依賴〈模組〉（來源：〈檔案〉）"}]},
{"id": "failing-tests", "label": "失敗測試及實際輸出", "type": "textarea", "suggestions": [{"label": "輸出摘要", "text": "pytest -q：〈數字〉 passed、〈數字〉 failed（我自己執行）"}, {"label": "失敗測試", "text": "〈測試名稱〉：期待〈值〉，實際〈值〉"}, {"label": "與 Agent 不同", "text": "Agent 貼的輸出與我執行的不一致：〈差異〉"}]},
{"id": "root-cause-hypotheses", "label": "可能根因／替代假設", "type": "textarea", "hint": "區分事實與推論", "suggestions": [{"label": "事實", "text": "事實：〈結論〉（來源：〈檔案／測試／文件位置〉）"}, {"label": "推論", "text": "推論：〈假設〉（依據：〈…〉，未驗證）"}, {"label": "替代假設", "text": "替代假設：〈另一種可能〉，排除方式：〈…〉"}]},
{"id": "affected-files", "label": "受影響檔案與理由", "type": "textarea", "suggestions": [{"label": "檔案與理由", "text": "〈檔案〉：〈理由〉"}]},
{"id": "rule-ids", "label": "相關Rule ID與來源", "type": "textarea", "suggestions": [{"label": "Rule 與來源", "text": "Rule 〈Rule ID〉：〈規則內容〉（來源：〈文件路徑〉）"}, {"label": "找不到來源", "text": "〈規則〉：找不到 Rule ID 來源，標為推論"}]},
{"id": "cross-evidence", "label": "程式／測試／文件的交叉證據", "type": "textarea", "suggestions": [{"label": "三方對照", "text": "程式：〈檔案第幾行〉〈…〉\n測試：〈測試名稱〉〈…〉\n文件：〈路徑〉〈…〉\n是否一致：〈是／否〉"}, {"label": "我親自核對", "text": "我打開〈檔案〉核對 Agent 的結論〈…〉：〈對得上／對不上〉"}]},
{"id": "gaps", "label": "資訊缺口／待問問題", "type": "textarea", "suggestions": [{"label": "待問問題", "text": "〈問題〉：〈為什麼查不清楚〉，可問〈誰〉或查〈哪裡〉"}, {"label": "未驗證", "text": "未驗證：〈項目〉（原因：〈…〉）"}]},
{"id": "investigation-order", "label": "建議調查順序", "type": "textarea", "suggestions": [{"label": "順序範本", "text": "1. 〈先查什麼〉，理由：〈…〉\n2. 〈再查什麼〉\n3. 〈…〉"}]},
{"id": "risks", "label": "風險／不宜修改區域", "type": "textarea", "suggestions": [{"label": "不宜修改", "text": "〈模組／檔案〉：不宜修改，理由：〈…〉"}, {"label": "風險範本", "text": "〈風險〉：〈可能影響〉"}, {"label": "保留既有測試", "text": "既有通過的 Regression 測試不可刪除或放寬斷言"}]}
]}
```

## 完成檢核

- [ ] 已保留可追查的分析成果供小組比較。
- [ ] 沒有把未執行的測試或未驗證的根因描述為已證實。
- [ ] 尚未修改任何程式或測試。
