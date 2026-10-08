---
id: time-skip
title: Time Skip：12 個月後
minute: 29-33
group: timeskip
section: Time Skip
---

# Time Skip：12 個月後

```callout info
現在在做什麼
- **情境**：Smart Ticket 已上線 12 個月（Time Skip：時間快轉）。你被調去接手同事維護的既有系統 B0（Brownfield Baseline：既有專案的起點版本，之後的 B1、B2、B3 都接在它上面）。
- **你的目標**：4 分鐘內停下 Greenfield，在 B0 開一個新的 Agent 對話，讓 Agent 把環境跑起來並記下起點。
- **今天的技巧**：**開新對話先給規則與脈絡**。換專案就開新對話，第一件事貼規則、說明背景；Agent 不記得上一個專案，沒給規則它就照自己的習慣做。這也是 Token 節費：不把舊對話帶過來。
- **完成的樣子**：Agent 複述得出規則與背景；它回報版本是 B0、健康檢查正常，並把測試結果與 Git 起點寫進 `notes/time-skip.md`。
```

```callout warning
本段只接手，不修改
全場使用主持人提供的同一份 B0，不要用自己的 Greenfield 成果代替。**不要修改 B0 的程式**，也先不要叫 Agent 分析；分析從第 33 分鐘開始。指令由 Agent 執行，你看它的白話回報做判斷。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。投影畫面只顯示時間與目前檢查點，要做什麼都在本頁。

- **29–31 · 檢查點 1 停手並取得 B0**：請 Greenfield 的 Agent 停掉 App，下載 B0 並解壓到短路徑。
- **31–32 · 檢查點 2 開新對話先貼規則與背景**：在 B0 開新的 Agent 對話，貼一段規則與背景，請它複述。
- **32–33 · 檢查點 3 請 Agent 建好環境並記下起點**：Agent 建環境、跑測試、確認版本與健康檢查、建立 Git 起點，寫進 `notes/time-skip.md`。

## 檢查點 1 · 停手並取得 B0（第 29–31 分鐘）

先把舊專案收好：保留 Greenfield 現況（不刪除、不覆寫），讓原本的 Agent 停掉它啟動的 App，避免之後兩個版本搶同一個埠號。在原本 Greenfield 的 Agent 對話貼上：

```text
請停止你在背景啟動的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 已經連不上，然後用白話告訴我結果。不要修改任何檔案。
```

接著下載 B0，用檔案總管（右鍵「全部解壓縮」）或 Finder 解壓縮到短路徑，例如 `C:\work\b0`，找到 `smart-ticket-b0` 資料夾（路徑是 `agentic-workshop\03-brownfield\participant\repository\smart-ticket-b0`，裡面有 `README.md`）。

```download
id=b0 zip=participant-29-b0.zip label=下載 B0 Repository
```

**看到什麼算過關**：Greenfield 的 Agent 回報 /health 已連不上；`smart-ticket-b0` 資料夾裡看得到 `README.md`。

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請不要放在深層的同步資料夾或桌面子資料夾，避免 Windows 路徑長度限制導致檔案不完整。
```

### 時間快轉公告

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md
```

### 公司與系統成長摘要

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/02-company-growth-summary.md
```

## 檢查點 2 · 開新對話先貼規則與背景（第 31–32 分鐘）

在 `smart-ticket-b0` 資料夾開啟**新的** Agent 對話（不要沿用 Greenfield 的對話：B0 是另一個專案，舊對話裡的規則和背景都不適用）。第一件事貼下面整段：前半是 Agent 工作規則（給 Agent 的，不需要看懂），後半是專案背景。最後請它複述，是為了確認它真的讀進去了。

```callout tip
技巧：Token 節費
Token（詞元）是 Agent 讀寫文字的計費與記憶單位：對話越長、貼越多，越貴，也越容易忘記前面講過的事。Greenfield 的對話已經很長，帶過來的每一句 Agent 都要重讀，還會把 G0 的規則混進 B0。需要的舊資訊已經寫在 notes 檔裡，所以開新對話，只給規則、背景與要讀的檔案。節費的基本做法：一個任務一個新對話；指定要讀的檔，不說「讀整個專案」；要摘要，不貼完整輸出；把共識寫成檔案，下次直接讀。接下來幾段會一個一個用到。
📖 延伸閱讀：Anthropic 官方文件〈Context windows〉與〈Token counting〉、Anthropic Engineering 文章〈Effective context engineering for AI agents〉；你所用工具的官方文件通常有同名章節。
```

```text
以下是這次工作的規則，請在整段對話中遵守：
1. 你負責所有程式、測試與指令操作；我不會自己修改程式，也不會自己讀程式，請用白話向我說明。
2. 每次修改前先提出計畫，等我核准；只做核准的步驟，做完就停下來等我。
3. 只處理任務卡範圍，做最小修改；不全面重寫，不改不相關的 API，不新增套件、服務或優惠政策。
4. 不刪除、弱化或隱藏任何測試，不用 skip／xfail，不把正確的期待值改成符合錯誤的輸出。
5. 每次做完都執行 pytest -q，並用「驗收對照表」回報：每條驗收條件或規則一列，欄位固定為「編號、白話內容、結果（通過／失敗／未驗證）、依據的測試名稱」，最後一行寫通過／失敗／跳過的測試數。不要貼原始輸出，只給摘要。
6. 每次修改後用白話說明：改了哪些檔案、各改了什麼、為什麼，以及有沒有超出我核准的範圍。
7. 你沒有實際執行的事情，一律標「未驗證」。

以下是這個專案的背景，請記住：
- 這是已上線 12 個月的訂票系統 Smart Ticket，版本 B0。我剛接手，還不熟。
- 這一段只接手：建好環境、跑測試、記下起點；先不要分析，也不要修改任何程式。
- 之後的紀錄都寫在專案裡的 notes 資料夾；notes 只放紀錄，不算程式修改。
請用三句話複述你理解的規則與背景，然後停下等我。
```

**看到什麼算過關**：Agent 的複述有提到「不自己改程式、先計畫再核准、沒執行過的標未驗證」與「這段只接手、不修改」。

**如果卡住**：複述漏了重點，貼這段：

```text
你的複述漏了一些規則。請重新讀一次上面的規則與背景，逐條確認你會遵守，再用三句話複述。
```

## 檢查點 3 · 請 Agent 建好環境並記下起點（第 32–33 分鐘）

同一個對話繼續貼下面這段。先確認版本、記下 Git 起點，之後 Agent 才能證明「它改了什麼」，也避免拿錯版本分析。

```text
請幫我準備這個專案的執行環境：確認 Python 版本是 3.13，在專案資料夾建立 .venv 虛擬環境並安裝 requirements.txt，接著執行 pytest -q。用白話告訴我：環境是否建好、測試有幾個通過／失敗／跳過，以及下一步要做什麼。遇到錯誤時先說明原因，不要自行修改程式。
接著請：
1. 告訴我這個 App 的名稱與版本號（app.title 與 app.version 的實際值），確認是不是 B0 - Brownfield Baseline。
2. 在背景啟動這個專案的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 回傳 status=ok，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
3. 建立 Git 起點：git init，把目前所有檔案 Commit 成「B0 baseline」，不要修改任何檔案。如果 Git 要求設定姓名或 Email，只在這個資料夾設定（不要用 --global），名字用「workshop」、Email 用「you@example.com」；電腦沒有 Git 就告訴我你改用什麼方式記錄起始狀態。
4. 把版本、健康檢查結果、測試數字（通過／失敗／跳過）與 Commit 是否成功寫進 notes/time-skip.md。
做完停下等我。
```

**看到什麼算過關**：

- 版本是 B0；瀏覽器打開 Agent 給的 `/docs` 網址看得到 API 清單。
- `notes/time-skip.md` 裡有測試數字與 Commit 結果。目前有若干測試失敗是正常的，**先不要修改**，第 33 分鐘起由個人分析處理。

```callout tip
常見狀況
- 埠號 8000 被佔用：多半是 Greenfield 的 App 沒停，回檢查點 1 請舊對話的 Agent 停掉。
- 環境建不起來：貼 [環境準備](#environment) 頁「疑難排解」的提示詞，請 Agent 先用白話說明原因與建議做法，你決定後再讓它處理；仍無法啟動請立即告知主持人，不要改用其他版本。
```

### Brownfield 接手說明

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/03-brownfield-handover.md
```

```form
{"id": "time-skip-check", "title": "Time Skip 確認","fields":[
{"id": "rules-first", "label": "新對話的第一件事是貼規則與背景，Agent 複述正確", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "b0-ready", "label": "版本是 B0、健康檢查正常、Git 起點與測試數字已寫進 notes/time-skip.md", "type": "select", "options": ["是", "否", "不確定"]},
{"id": "blocker", "label": "卡住的地方（選填，一句話）", "type": "text", "suggestions": ["沒有"]}
]}
```

## 完成後想一想

不用填表、不用寫下來，自己想一想就好：

1. **觀察**：新對話的 Agent 複述規則時，有沒有漏掉或講錯哪一條？如果你沒請它複述，會在什麼時候才發現？
2. **技巧**：如果直接在 Greenfield 的舊對話裡處理 B0，可能出什麼事？你工作上哪些時候該開新對話，而不是一直聊下去？
3. **延伸**：B0 有幾個測試沒過，文件也寫了很多。接手一個陌生專案時，你會先問 Agent 哪三個問題，才敢讓它動手？

```callout tip
💬 討論一下
先自己想 30 秒，再跟旁邊的人各說一個答案：你們的 Agent 複述規則時，漏掉的是同一條嗎？
```

這段學到的技巧：**換專案就開新對話，第一件事貼規則與背景，並請 Agent 複述確認。** 進入 Teammate 階段，對話會越來越長，從這裡開始練 Token 節費：一個任務一個新對話，只給需要的規則與檔案。

下一步（第 33 分鐘）：[B0 系統 Context](#b0-context)，接著 [個人 Agent 分析](#individual-analysis)。
