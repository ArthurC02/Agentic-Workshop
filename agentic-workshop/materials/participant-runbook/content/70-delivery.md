---
id: delivery
title: Delivery Summary 與交付
minute: 76-80
group: b3
section: Delivery
---

# 交付：請 Agent 整理交付摘要，人核對

```callout info
現在在做什麼
- **情境**：B3 時間到了。主管要一份「做了什麼、證據在哪、還缺什麼」的交付摘要，才能決定能不能收。
- **你的目標**：請 Agent 依實際證據寫交付摘要，你逐項核對後交件。
- **今天的技巧**：**請 Agent 整理交付摘要，人核對**。整理很花時間，交給 Agent；但摘要每一句都要指得出證據，沒驗證的如實標「未驗證」，人只需核對，不必自己寫。
- **完成的樣子**：`notes/delivery.md` 有附證據來源的交付摘要與完成等級（Level）；你填完 4 欄的交付核對表並交件。
```

全場第 76 分鐘停止擴充，接下來 **3 分鐘**定稿交付摘要（Delivery Summary）並交件。Agent 的建議不等於人員決策，人員最後決策以 B3 的 Gate 3 為準。

```callout warning
如實交付，交件後不再修改
- 完成等級（Completion Level：Level 1 分析完成、Level 2 核心流程完成、Level 3 完整交付）擇一並說明證據，不自動選 Level 3。
- 未驗證不能寫 PASS（通過）；Gate 核准也不能代替驗收或測試 PASS。
- 已完成分析時，可交付 Level 1；無程式修改或未執行測試也可交付，但須列明原因、未驗證範圍與後續工作。
- 交件後，交付摘要與 Level 保持交件時的樣子；人不補寫程式或測試。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 請 Agent 寫交付摘要，你來核對 | 76–78 | 00–02 | Agent 寫 `notes/delivery.md` 後停下；你核對證據並填交付核對表 |
| 2 · 匯出與交件 | 78–79 | 02–03 | 匯出表單，連同 `notes/` 資料夾依主持人指定方式交件 |
| 看投影 | 79–80 | 03–04 | 交件後不再修改；第 80 分鐘進入回顧 |

## 檢查點 1 · 請 Agent 寫交付摘要，你來核對（第 76–78 分鐘）

- [ ] 76 分鐘到，停止擴充。把下方提示詞貼給主要 Agent，並附上本頁下方的 Delivery Summary 範本全文：

```text
停止新增功能與測試，不要再修改任何程式。請讀 notes/b3.md，依附上的 Delivery Summary 範本十二欄，把交付摘要寫進 notes/delivery.md：
- 每一欄都附證據來源：notes/b3.md 的哪一段、哪個實際執行的指令、哪份文件。找不到證據的寫「未驗證」及原因，未驗證不能寫 PASS。
- Completion Level 擇一並說明證據，不自動選 Level 3。
- 修改檔案欄用白話寫每個檔案改了什麼、為什麼，附上 Gate 3 前的變更審查答案；沒有修改時寫「無修改」及原因，不虛構變更。
- 驗收結果用驗收對照表呈現；測試只寫實際執行過的命令與結果，沒執行的寫「未執行」及原因。
- Gate 決策照 notes/b3.md 的原文抄錄；寫出與 Gate 2 核准計畫的偏差，沒有偏差也要明寫。
寫完在對話列出：建議的 Level、未驗證項目清單，然後停下等我們核對。不要自行修正或補做任何項目。
```

- [ ] 核對摘要（不看程式）：抽三句話問 Agent「這句的證據在哪？」，它應該指得出 `notes/b3.md` 的段落或實際指令；Level 有證據；未驗證項目如實列出；Gate 決策與 `notes/b3.md` 一致。指不出證據的句子，請 Agent 改成「未驗證」。必要時請 Agent 依 [交付審查清單](#b3-review-checklist) 自評。
- [ ] 填下方「交付核對」表單第 1–3 欄。

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/05-delivery-template.md
```

**看什麼證據**：`notes/delivery.md` 每一欄都有證據來源或「未驗證」；Agent 沒有在這段修改程式。

## 檢查點 2 · 匯出與交件（第 78–79 分鐘）

表單會自動暫存在瀏覽器中，但要匯出才算交件。按下方按鈕（或右上角下載圖示）一次下載所有已填寫的表單。

```exportall
```

- [ ] 依主持人指定方式交件：匯出的表單 ZIP，加上主要 Agent 電腦上的 `notes/` 資料夾（`b3.md`、`delivery.md`）。Gate 紀錄、條件與未完成事項本身就是交付的一部分。
- [ ] 勾選下方表單第 4 欄。

### 填寫：交付核對

```form
{"id": "delivery-check", "title": "交付核對（任務 ID：TASK-B3-001）","fields":[
{"id": "level", "label": "核對後的完成等級", "type": "select", "options": ["Level 1：分析完成（Analysis Complete）", "Level 2：核心流程完成（Core Flow Complete）", "Level 3：交付完成（Delivery Complete）"], "hint": "依 notes/delivery.md 的證據擇一，不自動選 Level 3。"},
{"id": "evidence-cited", "label": "摘要每一句都指得出證據嗎？", "type": "select", "options": ["是", "否，已請 Agent 改成未驗證", "不確定"]},
{"id": "unverified-honest", "label": "未驗證的項目有如實標示嗎？還缺什麼？", "type": "text", "suggestions": [{"label": "有缺項", "text": "有如實標示；缺：〈一句話〉"}, "有如實標示；無缺項"]},
{"id": "handed-in", "label": "已匯出表單並連同 notes 資料夾交件", "type": "checkbox"}
]}
```

```callout warning
交件後停止修改
交件後不再修改交付摘要、Level 或任何表單，接下來看投影。未完成如實列為缺項，不把部分完成描述為完整交付。第 80 分鐘進入回顧。
```

> 這段學到的技巧：**讓 Agent 寫摘要，但要求每一句附證據**；人用「證據在哪？」核對，比自己寫更快也更可靠。
