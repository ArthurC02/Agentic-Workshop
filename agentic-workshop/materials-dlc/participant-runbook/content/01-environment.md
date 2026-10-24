---
id: environment
title: 開場與環境
minute: 00-14
group: dlc-opening
section: 開始之前
---

# 開場與環境

```callout info
現在在做什麼
- **情境**：你接手 Smart Ticket 的訂票後端，今天要和 Agent 一起替它建立團隊共用的領域模型。專案裡有團隊留下的 `AGENTS.md`。
- **你的目標**：14 分鐘內讓 Agent 照 `AGENTS.md` 備好環境、裝好 Skill：測試全過、模型工具可信，並找出哪些錯只能靠人審查。
- **今天的技巧**：做法寫在 `AGENTS.md` 和 Skill，提示詞只交代這次的事；每一步用 `check` 對照實際結果。
- **完成的樣子**：`notes/opening.md` 有四個檢查點的結果；起始版本（起始 commit）已建立，裡面有 `AGENTS.md` 和 Skill。
```

## 前置需求

- Python **3.13**：Windows 要有 `py` 啟動器；macOS 要有 `python3.13`。
- Git 2.34 以上（Windows 是 Git for Windows）。
- macOS 用 Safari 下載的人：到 Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」，或改用 Chrome。
- 一個能讀寫本機資料夾、執行終端機指令的 Coding Agent（主課用過的即可）。

## 檢查點 1 · 確認起點：測試全部通過（第 0–6 分鐘）

① 為什麼做這一步

今天每個設計決定最後都要用測試證明，所以先確認起點：起始 Repo 的測試全部通過。專案的做法已寫在 `AGENTS.md`，學員包另附 5 個 Skill；Agent 先把它們放到會自動載入的位置，之後的提示詞就只要寫這次的事。

```download
id=participant-dlc-open zip=participant-dlc-open.zip label=下載學員包（起始 Repo、Skill、輔助工具、domain-memory Plugin）
```

② 貼給 Agent

1. 按上方按鈕下載 `participant-dlc-open.zip`，解壓縮到你習慣的位置（例如下載資料夾）：Windows 在檔案上按右鍵選「全部解壓縮」；macOS 按兩下 zip。主持人說明時已做好就跳過。
2. 用 Agent 開啟解出來的 `participant-dlc-open` › `repository` › `smart-ticket-dlc-base` 資料夾（Repo 根目錄），開新的 Agent 對話。
3. 貼上：

```text
這是 Smart Ticket 的訂票後端，今天要和你一起替它建立團隊共用的領域模型。專案的做法寫在 AGENTS.md；學員包的 skills 資料夾（在上兩層）有 5 個 Skill。這一步先把環境準備好，不改程式：
1. 把那 5 個 Skill 原樣放到你這個工具會自動載入專案 Skill 的位置，在 AGENTS.md「Skill」一節最後加一行它們的位置（從 Repo 根目錄算起的路徑）。
2. 照 AGENTS.md 建好 venv、裝好套件、跑一次全部測試，結果記在 notes/opening.md。
做完告訴我 Skill 的完整路徑，再用 check 檢查，最後一行寫成功或失敗。
```

Agent 建立 Skill 資料夾時，工具若跳出允許視窗，按允許。安裝套件、跑測試約要一到三分鐘，趁這時先讀下方 ④ 的小卡。

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：測試全部通過、沒有 warning，5 個 Skill 都在。
```

失敗時：

```text
先停，不要再改。發生什麼事？是 Python 版本、網路還是套件來源的問題？你建議怎麼做？
```

④ 補充

```callout tip
技巧：團隊的 AGENTS.md 和 Skill（加深一層）
**主課你寫過 AGENTS.md；今天的 Repo 已經有團隊寫好的一份，連 Plugin 怎麼呼叫、金鑰放哪裡都寫在裡面。**
- 每次都要的事（怎麼跑、工作規則、審查準則）放 `AGENTS.md`；一步步的做法（檢查、登記候選、反事實檢查、簽章 commit）放 Skill
- 新對話的 Agent 答不出 `AGENTS.md` 的規則，就說「請先讀 AGENTS.md」
- 回到工作：把團隊每次都要重講的一件事寫進 `AGENTS.md`，重複三次以上的做法寫成 Skill
📖 延伸閱讀：OpenAI〈AGENTS.md〉、Claude Code 官方文件〈How Claude remembers your project〉、agentskills.io〈Agent Skills Overview〉；你所用工具的官方文件通常有同名章節。
```

## 檢查點 2 · 備好可信的共用模型工具（第 6–8 分鐘）

① 為什麼做這一步

今天的共用模型由 domain-memory 工具保存，之後每個 Agent 都照它做事，所以工具本身要可信。Agent 逐檔核對工具的指紋，全部相符才使用；你只看 ③ 是否成功。

② 貼給 Agent

```text
照 AGENTS.md 解出 domain-memory Plugin、逐檔核對指紋，告訴我核對結果和版本，記在 notes/opening.md。核對不符就停下，不要用它。做完用 check 檢查，最後一行寫成功或失敗。
```

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：核對結果是 SHA OK，版本是 4.2.0。
```

失敗時（出現 SHA MISMATCH 就停下，請主持人協助）：

```text
先停，不要動 Plugin 的任何檔案。是哪一步沒成功：找不到 zip、解壓縮失敗、核對不符，還是版本不對？列出不符的檔案，等我和主持人決定。
```

## 檢查點 3 · 找出只能靠人審查的錯（第 8–11 分鐘）

① 為什麼做這一步

Agent 用兩個只讀不改的檢查看這個 Repo：它是已有程式的既有專案，自動檢查只有測試，沒有架構檢查。所以程式有沒有越界，例如計價程式直接改會員資料，只能靠人審查；D3 每次變更都會回來問這一題，`AGENTS.md` 的審查準則也寫了這一題。

② 貼給 Agent

```text
用 Plugin 看看這個 Repo：跑 dm readiness 和 dm quality-gates（都是唯讀）。用白話告訴我：它判斷這是新專案還是既有專案、有多少把握；有哪些自動檢查（測試、lint 程式風格檢查、型別、架構）；所以你之後改程式時，哪些問題只能靠測試和人的審查才抓得到。記在 notes/opening.md，附關鍵輸出原文。做完用 check 檢查，最後一行寫成功或失敗。
```

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：notes/opening.md 照實記下 readiness 和 quality-gates 的結果。
```

失敗時：

```text
先停，不要改任何檔案。readiness 或 quality-gates 的輸出哪裡和你預期不同？可能的原因是什麼？你建議怎麼做？
```

## 檢查點 4 · 確認環境並建立起始版本（第 11–14 分鐘）

① 為什麼做這一步

Agent 確認用的是真正的 Python 3.13，並建立起始版本（起始 commit），之後每次變更都能和它比對。D2 起，共用模型每次推送前都會自動檢查有沒有核准，這項檢查要用到正確的 Python。

② 貼給 Agent

```text
最後把起點存起來：照 AGENTS.md 建立 Git Repo（身分只設在這個 Repo），做一次環境健檢，把結果記進 notes/opening.md，再把現在全部的檔案 commit 成「起始 Repo」。這時還沒有 domain-memory/，不用簽章。
告訴我 venv 的 Python 版本和路徑、健檢最後一行和有沒有 [!!]、commit 後工作區是不是乾淨的。做完用 check 檢查，最後一行寫成功或失敗。
```

等 Agent 時，還沒有 D2 夥伴的先找好（見本頁最後的「⏸ 看投影」）。

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：Python 是 3.13，健檢沒有 [!!]，起始 commit 裡有 AGENTS.md 和 Skill、沒有 domain-memory/，工作區是乾淨的。
```

失敗時：

```text
先停，不要改程式。每一個 [!!] 或 Python 路徑不對的原因是什麼？健檢建議怎麼修？只列出來，等我同意再做。
```

④ 補充

```callout danger
第 14 分鐘仍未通過
不要在活動中更換 Python 版本或工具。告知主持人，從 D1 起先和夥伴共用一台已通過的機器。
```

```callout sync
⏸ 看投影：第 11 分鐘找好 D2 夥伴，D2 起兩人一組
```
