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
- **你的目標**：請 Agent 依實際證據寫交付摘要，你抽查證據後交件。
- **今天的技巧**：**請 Agent 整理交付摘要，人核對**。每一句都要指得出證據，沒驗證的如實標「未驗證」。
- **完成的樣子**：`notes/delivery.md` 有附證據來源的交付摘要與完成等級（Level）；你選了 Level、勾了交件。
```

## 檢查點總覽

- **76–78 · 檢查點 1 請 Agent 寫交付摘要，你來核對**
- **78–79 · 檢查點 2 匯出與交件**

## 檢查點 1 · 請 Agent 寫交付摘要，你來核對（第 76–78 分鐘）

第 76 分停止一切修改。複製下方提示詞，再按下方 Delivery Summary 範本的「複製 Markdown」，接在後面一起貼給主要 Agent。

```text
停止新增功能與測試，不要再修改任何程式。請讀 notes/b3.md（只讀這個檔與範本，不要回頭翻對話或讀整個專案），依附在這段後面的 Delivery Summary 範本十二欄，標題與順序照範本不變，把交付摘要寫進 notes/delivery.md：
- 每一欄都附證據來源：notes/b3.md 的哪一段、哪個實際執行的指令、哪份文件。找不到證據的寫「未驗證」及原因，未驗證不能寫 PASS。
- Completion Level 擇一並說明證據，不自動選 Level 3。
- 修改檔案欄用白話寫每個檔案改了什麼、為什麼，附上 Gate 3 前的變更審查答案；沒有修改時寫「無修改」及原因，不虛構變更。
- 驗收結果用驗收對照表呈現；測試只寫實際執行過的命令與結果，沒執行的寫「未執行」及原因。
- Gate 決策照 notes/b3.md 的原文抄錄；寫出與 Gate 2 核准計畫的偏差，沒有偏差也要明寫。
寫完在對話給我核對用的三句話：你建議的 Level、測試結果、修改範圍。每句後面直接引用它的證據原文與位置（notes/b3.md 的段落或實際指令）；引用不出證據的，在摘要裡改成「未驗證」。最後列出未驗證項目清單，然後停下等我們核對。不要自行修正或補做任何項目。
```

```include
zip=participant-63-b3-governance.zip path=agentic-workshop/04-digital-worker/participant/05-delivery-template.md
```

```callout tip
技巧：Structured Output（結構化輸出，加深一層）
這次多加一層：每一句都要附證據位置。交付摘要固定十二個標題，你只要一欄一欄問「證據在哪？」。
📖 延伸閱讀：Anthropic 官方文件〈Structured outputs〉、OpenAI 官方文件〈Structured model outputs〉；你所用工具的官方文件通常有同名章節。
```

**看到什麼算過關**

- 三句話都引用得出證據原文；引用不出的已改成「未驗證」。
- Level 有證據支持，Gate 決策和 `notes/b3.md` 一致。
- Agent 沒有在這段修改程式。

**如果卡住**（看不懂某句，或覺得證據對不上）

```text
不要修改程式。摘要裡這幾句我看不懂或覺得證據對不上：請用白話重新解釋，並引用 notes/b3.md 的原文。對不上的，在 notes/delivery.md 改成「未驗證」並寫原因。
```

## 檢查點 2 · 匯出與交件（第 78–79 分鐘）

小組先花 1 分鐘聊：Agent 建議的 Level 你們同意嗎？只看驗收對照表會選哪一級，加上 Gate 紀錄與缺項後還一樣嗎？如果主管只看一欄，你們希望他看哪一欄？

說好後，把結論記在下方表單，再按按鈕一次下載所有已填寫的表單；要匯出才算交件。

```form
{"id": "delivery-check", "title": "交付核對（任務 ID：TASK-B3-001）","fields":[
{"id": "level", "label": "核對後的完成等級", "type": "select", "options": ["Level 1：分析完成（Analysis Complete）", "Level 2：核心流程完成（Core Flow Complete）", "Level 3：完整交付（Delivery Complete）"], "hint": "依 notes/delivery.md 的證據擇一，不自動選 Level 3。"},
{"id": "evidence-cited", "label": "抽查的三句都指得出證據嗎？", "type": "select", "options": ["是", "否，已請 Agent 改成未驗證", "不確定"]},
{"id": "handed-in", "label": "已匯出表單並連同 notes 資料夾交件", "type": "checkbox"}
]}
```

```exportall
```

依主持人指定方式交件：匯出的表單 ZIP，加上主要 Agent 電腦上的 `notes/` 資料夾。

```callout warning
交件後停止修改
交件後不再修改交付摘要、Level 或任何表單。第 80 分鐘進入回顧。
```

## 完成後想一想

先自己想 30 秒，再和旁邊的人聊；主持人會請 1–2 位分享第 2 題。

1. **觀察**：你抽查的三句裡，有沒有哪一句引用不出證據、被改成「未驗證」？Agent 一開始建議的 Level 跟你們最後選的一樣嗎？
2. **技巧**：如果交付摘要讓 Agent 自由發揮、不要求每句附證據，你要怎麼分辨哪些是真的做到、哪些只是它「覺得」做到？你工作上的週報或交接文件，哪幾欄值得固定下來？
3. **延伸**：今天的交付只看證據、不看程式。回到公司，誰應該替這份交付簽名負責？他還需要看到什麼？
