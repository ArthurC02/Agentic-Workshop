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
- **今天的技巧**：**把共識寫成檔案給 Agent**。口頭講過的 Agent 下次就忘了；寫成檔案，之後每一段開始先請它讀，Agent 就從同一份共識出發。提示詞示範兩個 Agent 技巧：Skill（可重複使用的工作說明）與 Token 節費。
- **完成的樣子**：主要 Agent 的專案裡有 `notes/shared-context.md` 與 `skills/team-rules.md`，它複述的共識沒有把假設說成事實，也沒有自己加修改計畫。
```

```callout warning
B1 尚未揭露
B1（Brownfield 第一段任務）第 44 分鐘才發放。這段只整理共識：不提出或核准修改計畫，不修改程式。本段內容已在第 29 分鐘解鎖。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

- **39–42 · 檢查點 1 比較各自的分析，選出主要 Agent**：每人請自己的 Agent 把分析濃縮成 5 行；小組口頭比較，選主要 Agent 與核准者。
- **42–44 · 檢查點 2 請主要 Agent 寫成共同脈絡檔**：主要 Agent 收齊大家的摘要，寫成 `notes/shared-context.md` 與 `skills/team-rules.md`，複述後停下。

## 檢查點 1 · 比較各自的分析，選出主要 Agent（第 39–42 分鐘）

每個人的 Agent 只看過自己那份分析。先請它濃縮成 5 行，小組才比得起來；比的是摘要，不是整段對話。

```callout tip
技巧：Token 節費（加深一層）
Time Skip 學過 Token 節費的「要摘要、不要全文」，這次用在小組之間：5 行摘要貼給主要 Agent，比整段對話或整份分析省下大量 Token，主要 Agent 也不會被細節淹沒。
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

口頭共識 Agent 下次就忘了，寫成檔案才會留下來。在**主要 Agent** 的對話**一次貼完**：先複製下面這段，接著在後面用一兩句話打上小組的分工與共識（主要 Agent 在誰的電腦、核准者是誰、口頭討論的共識與分歧），最後貼上其他成員的 5 行摘要（從聊天室複製即可），一起送出。

```callout tip
技巧：Skill（可重複使用的工作說明）
Skill 是把一套反覆要用的做法寫成一個 Markdown 檔，放在專案的 `skills/` 資料夾；之後只要說「請先讀 skills/… 並照做」，不必重教。檔案由 Agent 建立，你不用手寫。這裡的 `skills/team-rules.md` 寫的是：開工先讀什麼、要守的規則（就是你在 Greenfield 和 Time Skip 貼過的工作規則）、回報用什麼格式。寫好之後，B1、B2、B3 的提示詞只要一句「請先讀 skills/team-rules.md」，不用每段重貼整段規則，省時間也省 Token。這裡的 Skill 是一般 Markdown 檔，靠你在提示詞說「先讀它」才會用到；工具內建的 Skill 功能（例如 Agent Skills）有固定的資料夾、檔名與開頭欄位，放對位置後 Agent 會在相關時自動讀取。
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

之後每一段開始（B1、B2、B3，或開了新的 Agent 對話），不用再貼整段規則，第一句改成：

```text
請先讀 skills/team-rules.md 並照做，用三句話告訴我你理解的小組共識與規則，再等我交代任務。
```

```include
zip=participant-39-shared-context.zip path=agentic-workshop/03-brownfield/participant/04-shared-context-template.md
```

```form
{"id": "shared-context", "title": "Shared Context 確認","fields":[
{"id": "my-role", "label": "我在小組的角色", "type": "select", "options": ["主要 Agent 在我的電腦", "人員核准者", "主要 Agent ＋ 核准者", "其他成員"]},
{"id": "restate-ok", "label": "主要 Agent 已寫好 notes/shared-context.md 與 skills/team-rules.md，複述沒有把假設說成事實、沒有自己加修改計畫", "type": "select", "options": ["是", "否", "不確定"]}
]}
```

第 44 分鐘停止。B1 揭露後，任務範圍、計畫與核准由 Agent 寫進 `notes/b1.md`，不再填在本頁。

## 完成後想一想

不用填表、不用寫下來，自己想一想就好：

1. **觀察**：比較 5 行摘要時，哪一條大家說法不一樣？最後是靠什麼證據（文件位置、測試名稱或實際執行結果）決定寫成事實還是分歧？
2. **技巧**：如果不寫 `notes/shared-context.md` 和 `skills/team-rules.md`，只靠口頭講好，下一段換人或開新對話時會發生什麼？你的團隊有哪些「每次都要重講一次」的規則，值得寫成 Skill？
3. **延伸**：主要 Agent 只有一個，但小組有好幾個人。接下來要真的改程式時，誰說了算、怎麼避免大家各自叫 Agent 改？

```callout tip
💬 討論一下
先自己想 30 秒，再跟旁邊的人各說一個答案：你們的「仍有分歧」裡，哪一條最可能影響接下來的任務？
```

```callout tip
這段學到的技巧
把共識寫成檔案給 Agent，之後每段都先請它讀，而不是靠口頭重講。把反覆要用的規則寫成 Skill 檔，是從 Teammate 走向 Digital Worker 的準備：到 B3，整份工作單就是交給 Agent 的 Skill。
```
