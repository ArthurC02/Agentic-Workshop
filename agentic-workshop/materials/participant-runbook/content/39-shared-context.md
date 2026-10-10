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
- **你的目標**：5 分鐘內比較大家的分析，選出主要 Agent，讓它把小組共識寫成 `notes/shared-context.md`（Shared Context：小組共同脈絡），並把小組規則寫成一個 Skill 檔 `skills/team-rules.md`。
- **今天的技巧**：**把共識寫成檔案給 Agent**。口頭講過的 Agent 下次就忘了；寫成檔案，之後每段先請它讀。
- **完成的樣子**：主要 Agent 的專案裡有 `notes/shared-context.md` 與 `skills/team-rules.md`，它複述的共識沒有把假設說成事實，也沒有自己加修改計畫。
```

```callout warning
B1 尚未揭露
B1 第 44 分鐘才發放。這段只整理共識：不提出或核准修改計畫，不修改程式。
```

## 檢查點總覽

- **39–42 · 檢查點 1 比較各自的分析，選出主要 Agent**
- **42–44 · 檢查點 2 請主要 Agent 寫成共同脈絡檔**

## 檢查點 1 · 比較各自的分析，選出主要 Agent（第 39–42 分鐘）

先請自己的 Agent 把分析濃縮成 5 行，小組才比得起來。

```callout tip
技巧：Token 節費（加深一層）
要摘要、不要全文：5 行摘要貼給主要 Agent，比整段對話省下大量 Token，主要 Agent 也不會被細節淹沒。
📖 延伸閱讀：Anthropic Engineering 文章〈Effective context engineering for AI agents〉、Anthropic 官方文件〈Context windows〉；你所用工具的官方文件通常有同名章節。
```

每個人對自己的 Agent 貼：

```text
請把 notes/analysis.md 濃縮成 5 行，給小組比較用：系統地圖一句、規則在哪一句、測試現況一句、最重要的文件與程式不一致處一句、最大的不確定一句。每行標事實（來源）、假設或缺口。只回覆這 5 行，不要修改任何檔案。
```

```callout tip
💬 討論一下
1. 把每個人的 5 行放在一起（念出來或傳到小組聊天室）：哪幾行大家說的一樣、而且都附得出來源？那就是共同事實。說法不同或沒證據的，是分歧——要重跑哪個測試或對照哪條規則才分得出對錯？
2. 誰的電腦當**主要 Agent**（之後由它執行任務）？誰當**人員核准者**？
口頭講就好，不用寫下來；下一步由主要 Agent 記錄。
```

**看到什麼算過關**：小組說得出至少一條附來源的共同事實、一個分歧，並選定主要 Agent 與核准者。

## 檢查點 2 · 請主要 Agent 寫成共同脈絡檔（第 42–44 分鐘）

在**主要 Agent** 的對話裡**一次貼完**以下三樣再送出：① 下面這段提示詞；② 一兩句小組分工與共識（主要 Agent 在誰的電腦、核准者是誰、口頭討論的共識與分歧）；③ 其他成員的 5 行摘要（從聊天室複製即可）。

```callout tip
技巧：Skill（可重複使用的工作說明）
Skill 是把一套反覆要用的做法寫成 Markdown 檔，放在專案的 `skills/` 資料夾，由 Agent 建立（工具內建的 Skill 功能另有固定格式，今天不需要）。之後只要說「請先讀 skills/… 並照做」，不必重貼：B1 起每段提示詞第一句都是「請先讀 skills/team-rules.md」。
📖 延伸閱讀：Anthropic 官方文件〈Agent Skills〉、OpenAI Codex 官方文件〈Custom instructions with AGENTS.md〉、GitHub 官方文件 Copilot〈Adding repository custom instructions for GitHub Copilot〉；你所用工具的官方文件通常有同名章節。
```

```text
先不要修改程式，也不要提出修改計畫。我們要把小組共識寫成 notes/shared-context.md，再把小組的工作規則寫成 skills/team-rules.md。這段後面我附上了兩樣東西：小組的分工與口頭共識（主要 Agent 在誰的電腦、人員核准者是誰、共識與分歧），以及其他成員的 5 行分析摘要。少了哪一樣，只問那一樣。請依序做：
1. 讀我附上的分工、共識與摘要；你自己的 notes/analysis.md 也濃縮成 5 行一起比較。
2. 寫成 notes/shared-context.md，分五節：共同事實（多人一致、附來源：文件位置、測試名稱或實際執行結果）、仍有分歧（附驗證方式：重跑哪個測試、對照哪條規則）、已知限制（只記限制，不預先核准修改）、待決事項（要等任務揭露才能決定的事）、分工（主要 Agent 與核准者）。證據不足的寫成假設，不要寫成事實。
3. 建立 skills/team-rules.md（給 Agent 的工作說明，之後每段開工都會先讀），固定三節：開工先讀（notes/shared-context.md）；工作規則（把這個對話一開始我貼給你的 7 條工作規則原文抄進來，第 4 條要包含「因規則改變而過時的期待值，須列出測試名稱與規則編號（Rule ID），經人核准後才更新」；對話裡找不到就先問我）；回報格式（驗收對照表欄位：編號、白話內容、結果（通過／失敗／未驗證）、依據的測試名稱；改了哪些檔案與原因；只給摘要不貼完整輸出；做完停下等我）。
4. 寫完用白話複述重點，指出你認為證據不足或互相矛盾的地方，然後停下等我們確認。
```

**看到什麼算過關**：

- 主要 Agent 的專案裡有 `notes/shared-context.md`，五節都有內容；`skills/team-rules.md` 有開工先讀、工作規則、回報格式三節。
- 複述沒有把分歧或假設說成事實，也沒有自己加修改計畫；有就請它修正檔案。

小組確認過主要 Agent 的複述後，把你們的結論記下來：

```form
{"id": "shared-context", "title": "Shared Context 確認","fields":[
{"id": "my-role", "label": "我在小組的角色", "type": "select", "options": ["主要 Agent 在我的電腦", "人員核准者", "主要 Agent ＋ 核准者", "其他成員"]},
{"id": "restate-ok", "label": "主要 Agent 已寫好 notes/shared-context.md 與 skills/team-rules.md，複述沒有把假設說成事實、沒有自己加修改計畫", "type": "select", "options": ["是", "否", "不確定"]}
]}
```

第 44 分鐘停止。

## 完成後想一想

先自己想 30 秒，再和旁邊的人聊；主持人會請 1–2 位分享第 2 題。

1. **觀察**：比較 5 行摘要時，哪一條大家說法不一樣？最後是靠什麼證據（文件位置、測試名稱或實際執行結果）決定寫成事實還是分歧？
2. **技巧**：如果不寫 `notes/shared-context.md` 和 `skills/team-rules.md`，只靠口頭講好，下一段換人或開新對話時會發生什麼？你的團隊有哪些「每次都要重講一次」的規則，值得寫成 Skill？
3. **延伸**：主要 Agent 只有一個，但小組有好幾個人。接下來要真的改程式時，誰說了算、怎麼避免大家各自叫 Agent 改？
