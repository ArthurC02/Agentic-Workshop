---
id: time-skip
title: Time Skip：12 個月後
minute: 30-39
group: timeskip
section: Time Skip
---

# Time Skip：12 個月後

```callout info
現在在做什麼
- **情境**：Smart Ticket 已上線 12 個月（Time Skip：時間快轉），你接手同事維護的既有系統 B0；專案裡有同事留下的 `AGENTS.md`。
- **你的目標**：第 39 分前停下 Greenfield，在 B0 開新的 Agent 對話，確認它讀到規則，再建好環境、記下起點。
- **今天的技巧**：**開新對話，確認 Agent 讀到規則檔**。換專案就開新對話，先確認 Agent 讀到 `AGENTS.md`，再說背景。
- **完成的樣子**：Agent 引用得出 `AGENTS.md` 的規則；版本、測試結果和 Git 起點已寫進 `notes/time-skip.md`。
```

```callout warning
本段只接手，不修改
**全場用同一份 B0，這段只接手、不修改。**
- 不要用自己的 Greenfield 成果代替 B0
- 先不要叫 Agent 分析，分析從第 39 分鐘開始
```

## 檢查點總覽

- **30–32 · 檢查點 1 停手並取得 B0**
- **32–37 · 檢查點 2 開新對話，確認 Agent 讀到 AGENTS.md**
- **37–39 · 檢查點 3 請 Agent 建好環境並記下起點**

## 檢查點 1 · 停手並取得 B0（第 30–32 分鐘）

① 為什麼做這一步

Greenfield 成果保留不動。只請原本的 Agent 停掉它啟動的伺服器，免得兩個版本搶同一個埠號。

② 貼給 Agent

在原本 Greenfield 的 Agent 對話貼上：

```text
Greenfield 先做到這裡。請停掉你啟動的伺服器，確認都停了再告訴我；不是你啟動的程式不要動。
```

貼完不用等它回覆，馬上按下方按鈕下載 B0，解壓縮到短路徑。Windows：右鍵選「全部解壓縮」，例如 `C:\work\b0`；macOS：把 ZIP 移到 `~/work` 再點兩下，會解到 `~/work/participant-29-b0`。

解壓後找到 `smart-ticket-b0` 資料夾，路徑是 `agentic-workshop/03-brownfield/participant/repository/smart-ticket-b0`，裡面有 `README.md` 和 `AGENTS.md`。

```download
id=b0 zip=participant-29-b0.zip label=下載 B0 Repository
```

③ 確認結果

Agent 回覆已說清楚它啟動的伺服器都停了，就直接往下。沒說清楚時，回到 Greenfield 對話貼：

```text
用 check 檢查剛才這一段：你啟動的伺服器都已停止。
```

失敗時：

```text
先停，別動其他程式。還有哪個伺服器在跑、是誰啟動的？是你啟動的就停掉，不是的告訴我它的名稱和 PID（程序編號）。
```

## 檢查點 2 · 開新對話，確認 Agent 讀到 AGENTS.md（第 32–37 分鐘）

① 為什麼做這一步

換專案就開新對話，第一件事確認 Agent 讀到這個專案的規則，再說背景。你判斷它引用的是 `AGENTS.md` 原文，而且有這三點：程式由 Agent 做、改程式前先計畫等核准、沒執行過的標「未驗證」。

② 貼給 Agent

在 `smart-ticket-b0` 資料夾開**新的** Agent 對話，不要沿用 Greenfield 的對話。貼上：

```text
我剛接手這個已上線 12 個月的訂票系統 B0，還不熟。這段只接手：建好環境、記下起點，先不分析、不改程式。
先告訴我：這個專案的工作規則是什麼？只引用 AGENTS.md 原文，不要自己補；你沒有自動讀到它就直接說。接著照 AGENTS.md 建好環境、跑一次測試（有失敗先別修），再用 Git 把現在的檔案存成「B0 baseline」，只建這一個 Commit，紀錄等我下一步再說。
```

Agent 說沒有自動讀到 `AGENTS.md`，貼：

```text
請先讀 AGENTS.md。再把你的工具設定成之後開新對話會自動讀它，告訴我你改了什麼。
```

Agent 引用完會接著裝環境。趁它安裝，對照 ① 的三點：都有就直接貼檢查點 3 ②，不用等安裝完。

③ 確認結果

不用等安裝：Agent 會在檢查點 3 一起回報環境。只有它在檢查點 3 沒提到環境時，才貼：

```text
用 check 檢查剛才這一段：.venv 是 Python 3.13，套件都裝好了。
```

失敗時：

```text
先停，不要再改。發生什麼事？你建議怎麼做？
```

④ 補充

```callout tip
技巧：Token 節費
**換專案就開新對話，只給規則、背景和要讀的檔案，不帶舊對話。**
- Token（詞元）是模型讀寫文字的單位：計費和一次對話能裝多少內容，都用它計算
- 對話越長、貼得越多，就越貴，也越容易忘了前面講過的事
- 規則已在 AGENTS.md，新對話會自己讀，不用從舊對話帶過來
📖 延伸閱讀：Anthropic 官方文件〈Context windows〉與〈Token counting〉、Anthropic Engineering 文章〈Effective context engineering for AI agents〉；你所用工具的官方文件通常有同名章節。
```

Agent 引用的不是原文、或漏了重點，貼：「請重新打開 AGENTS.md，逐字引用工作規則那一節。」

## 檢查點 3 · 請 Agent 建好環境並記下起點（第 37–39 分鐘）

① 為什麼做這一步

測試和 Git 起點檢查點 2 已經在做；這步只補確認版本是 B0，把起點寫進紀錄。之後每段改了什麼，才說得清楚。

② 貼給 Agent

同一個對話繼續貼，Agent 還在安裝也可以先貼：

```text
上一步做完後，確認 App 的版本（app.version）是 B0。版本、剛才的測試數字和 Commit 結果寫進 notes/time-skip.md，不用重跑測試、也不用再 Commit。做完用 check 檢查。
```

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段。
```

失敗時：

```text
先停。哪一項不符？只補做那一項，不要改程式。
```

④ 補充

有幾個測試失敗是正常的，**先不要修改**。

```callout tip
時間不夠時
**第 39 分鐘不論做到哪裡，都翻到「個人 Agent 分析」頁，不等安裝。**
- 還沒貼檢查點 3 ② 的，在同一個對話先貼它，再接著貼分析的檢查點 1 ②；Agent 會依序做完
- 檢查點 3 的「成功」或「失敗」等 Agent 回報再看；回「失敗」就先貼「失敗時」，再做分析的檢查點 1 ③
- 安裝沒好就讓它繼續，不要開新對話
```

## 完成後想一想

先自己想 30 秒，再和旁邊的人聊；趁等 Agent 回報時聊，這段不另開全場分享。

1. **觀察**：新對話的 Agent 一開始就引用得出 `AGENTS.md` 的規則嗎？如果它沒讀到、你也沒問，會在什麼時候才發現？
2. **技巧**：如果直接在 Greenfield 的舊對話裡處理 B0，可能出什麼事？你工作上哪些時候該開新對話，而不是一直聊下去？
3. **延伸**：B0 有幾個測試沒過，文件也寫了很多。接手陌生專案時，你會先問 Agent 哪三個問題，才敢讓它動手？

下一步（第 39 分鐘）：[個人 Agent 分析](#individual-analysis)。
