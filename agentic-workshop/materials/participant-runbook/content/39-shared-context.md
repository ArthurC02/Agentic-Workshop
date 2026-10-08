---
id: shared-context
title: Shared Context：小組比較分析
minute: 39-44
group: timeskip
section: Brownfield｜Teammate
---

# Shared Context：把共識寫成檔案給 Agent

```callout info
現在在做什麼
- **情境**：每個人的 Agent 都讀過 B0，但看法不完全一樣；接下來小組要一起改同一份系統。
- **你的目標**：5 分鐘內比較大家的分析，選出主要 Agent，讓它把小組共識寫成 `notes/shared-context.md`（Shared Context：小組共同脈絡）。
- **今天的技巧**：**把共識寫成檔案給 Agent**。口頭講過的 Agent 下次就忘了；寫成檔案，之後每一段開始先請它讀，Agent 就從同一份共識出發。
- **完成的樣子**：主要 Agent 的專案裡有 `notes/shared-context.md`，它複述的共識沒有把假設說成事實，也沒有自己加修改計畫。
```

```callout warning
B1 尚未揭露
B1（Brownfield 第一段任務）第 44 分鐘才發放。這段只整理共識：不提出或核准修改計畫，不修改程式。本段內容已在第 29 分鐘解鎖。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 比較各自的分析，選出主要 Agent | 39–42 | 00–03 | 每人請自己的 Agent 把分析濃縮成 5 行；小組比較，選主要 Agent 與核准者 |
| 2 · 請主要 Agent 寫成共同脈絡檔 | 42–44 | 03–05 | 把各人摘要交給主要 Agent，寫成 `notes/shared-context.md` 並複述後停下 |

## 檢查點 1 · 比較各自的分析，選出主要 Agent（第 39–42 分鐘）

每個人對自己的 Agent 貼：

```text
請把 notes/analysis.md 濃縮成 5 行，給小組比較用：系統地圖一句、規則在哪一句、測試現況一句、最重要的文件與程式不一致處一句、最大的不確定一句。每行標事實（來源）、假設或缺口。不要修改任何檔案。
```

小組把每個人的 5 行放在一起比較：多人一致且附得出來源的，是共同事實；說法不同或沒有證據的，是分歧。不需要讀程式。最後選定**主要 Agent**（之後由它執行任務）與**人員核准者**。

**看什麼證據**：每條「共同事實」至少有一個來源（文件位置、測試名稱或實際執行結果）；分歧有寫下怎麼驗證。

## 檢查點 2 · 請主要 Agent 寫成共同脈絡檔（第 42–44 分鐘）

把各人的 5 行摘要（不是整段對話）一起貼給主要 Agent：

```text
先不要修改程式，也不要提出修改計畫。以下是我們小組每個人的分析摘要：
〈貼上各人的 5 行摘要〉
我們的共識是：〈一兩句話，例如哪些事實大家都同意、哪裡還有分歧〉
請寫成 notes/shared-context.md，分五節：共同事實（附來源）、仍有分歧（附驗證方式）、已知限制、待決事項、分工（主要 Agent：〈誰的電腦〉；核准者：〈姓名〉）。證據不足的寫成假設，不要寫成事實。寫完用白話複述重點，指出你認為證據不足或互相矛盾的地方，然後停下等我們確認。
```

**看什麼證據**：複述裡沒有把分歧或假設說成事實，也沒有自己加修改計畫；有就請它修正檔案。

之後每一段開始（B1、B2、B3，或開了新的 Agent 對話），第一句先貼：

```text
開始前請先讀 notes/shared-context.md，用三句話告訴我你理解的小組共識，再等我交代任務。
```

```include
zip=participant-39-shared-context.zip path=agentic-workshop/03-brownfield/participant/04-shared-context-template.md
```

```form
{"id": "shared-context", "title": "Shared Context 確認","fields":[
{"id": "main-agent", "label": "主要 Agent（誰的電腦）與人員核准者", "type": "text", "suggestions": [{"label": "分工範本", "text": "主要 Agent：〈誰〉的電腦；核准者：〈姓名〉"}]},
{"id": "restate-ok", "label": "主要 Agent 已寫好 notes/shared-context.md，複述沒有把假設說成事實、沒有自己加修改計畫", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "open-issue", "label": "小組最大的分歧或待決事項（一句話）", "type": "text", "suggestions": ["目前沒有分歧", {"label": "分歧", "text": "〈判斷〉：還要請 Agent 〈重跑哪個測試／對照哪條規則〉"}]}
]}
```

第 44 分鐘停止。B1 揭露後，任務範圍、計畫與核准由 Agent 寫進 `notes/b1.md`，不再填在本頁。

這段學到的技巧：**把共識寫成檔案給 Agent，之後每段都先請它讀，而不是靠口頭重講。**
