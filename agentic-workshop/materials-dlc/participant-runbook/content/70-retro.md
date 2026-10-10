---
id: retro
title: 回顧：Domain Memory 改變了什麼
minute: 165-180
group: dlc-retro
section: 回顧
---

# 回顧：Domain Memory 改變了什麼

```callout info
現在在做什麼
- **情境**：今天留下了 `notes/`、交接單、Registry 與稽核紀錄。回到自己的專案時，你身邊沒有 Runbook。
- **你的目標**：請 Agent 從紀錄找出「Domain Memory 有沒有改變 Agent 的輸出」的證據，小組討論哪些核准步驟真的擋得住錯，最後帶走自己的提示詞清單和一項行動。
- **今天的技巧**：**請 Agent 從紀錄整理證據，人只判斷**；沒有證據就寫「未觀察」。
- **完成的樣子**：`notes/retro.md` 有附證據的回顧；每個人有一份 `notes/my-prompts-你的名字.md`；私鑰已刪除、表單已匯出。
```

除了檢查點 4 由夥伴貼到自己的 Agent 對話，其他提示詞貼給任一個 Agent 對話即可。

## 檢查點 1 · 請 Agent 從紀錄整理證據（第 165–169 分鐘）

① 為什麼做這一步

Agent 翻紀錄找證據，你們判斷證據站不站得住；記得的和紀錄不一樣時，以紀錄為準。

② 貼給 Agent

```prompt
# windows
我們要回顧今天的延伸課程。這一步只讀紀錄，不要修改程式或 domain-memory/。
請讀 notes/ 裡今天的所有紀錄、docs/handoffs/ 裡的交接單、git log，並在 Repo 根目錄執行 ..\..\tools\dm.ps1 verify-audit（Git Bash 用 ../../tools/dm.sh verify-audit）。
然後回答下面四題，每題一到三句，每句都附證據（哪個檔案的哪一段、哪個 commit 或哪個指令輸出）；找不到證據就寫「未觀察」，不要推測：
1. 哪一個已審查（reviewed）事實改變了 Agent 的輸出（任一個 Agent 對話都算）？原本會怎麼做、後來怎麼做？
2. 哪一個候選差點被當成事實？是誰（我們或你）、在哪一段發現的？
3. 哪一次反事實檢查（counterfactual）的結果出乎預期？學到什麼？
4. 哪個知識缺口（查不到的名詞或還沒決定的問題）影響最大？影響了哪個決定？
把回答寫進 notes/retro.md 的「檢查點 1 · 證據」小節（沒有這個檔就建立），在對話貼出四題的回答，然後停下等我回「同意」或「第 N 題改成…」。
# macos
我們要回顧今天的延伸課程。這一步只讀紀錄，不要修改程式或 domain-memory/。
請讀 notes/ 裡今天的所有紀錄、docs/handoffs/ 裡的交接單、git log，並在 Repo 根目錄執行 source .venv/bin/activate && ../../tools/dm.sh verify-audit。
然後回答下面四題，每題一到三句，每句都附證據（哪個檔案的哪一段、哪個 commit 或哪個指令輸出）；找不到證據就寫「未觀察」，不要推測：
1. 哪一個已審查（reviewed）事實改變了 Agent 的輸出（任一個 Agent 對話都算）？原本會怎麼做、後來怎麼做？
2. 哪一個候選差點被當成事實？是誰（我們或你）、在哪一段發現的？
3. 哪一次反事實檢查（counterfactual）的結果出乎預期？學到什麼？
4. 哪個知識缺口（查不到的名詞或還沒決定的問題）影響最大？影響了哪個決定？
把回答寫進 notes/retro.md 的「檢查點 1 · 證據」小節（沒有這個檔就建立），在對話貼出四題的回答，然後停下等我回「同意」或「第 N 題改成…」。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. notes/retro.md 有「檢查點 1 · 證據」，四題都有回答。
2. 每句回答都指得出檔案段落、commit 或指令輸出，找不到的寫「未觀察」。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
不要修改程式或 domain-memory/。請逐句重新核對 notes/retro.md「檢查點 1 · 證據」：指不出證據的句子改成「未觀察」，列出你改了哪些句子，然後停下。
```

## 檢查點 2 · 比較哪些核准步驟擋得住錯（第 169–174 分鐘）

① 為什麼做這一步

讓 Agent 把今天的核准流程一步一步攤開，再由人判斷哪一步真的擋住過錯誤、哪一步只是照流程做完。

② 貼給 Agent

```text
請依 notes/ 與 git log 裡 D2 的紀錄，以及 D3、D4 碰到 domain-memory/ 的 commit，把今天的核准流程列成清單，每一步一行：步驟、留下了什麼證據（檔案、簽章或指令輸出）、同一個人在同一台機器上能不能自己完成這一步。最後補一句：要證明「真的有另一個人審查過」，還缺什麼。不要修改任何檔案，列完停下。
```

③ 確認結果

```text
請只檢查你剛才列的清單，不要修改任何檔案：每一步都有證據，也都有「一個人能不能自己完成」的判斷，最後有一句還缺什麼。全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請把清單裡缺證據或缺判斷的步驟補齊；查不到證據的寫「紀錄中沒有」。不要修改任何檔案，列完停下。
```

④ 補充

```callout warning
說清楚：今天的成對簽章是教學示範，不是安全保證
兩人在同一台機器上：任何一人都能打出另一人的 email、拿到私鑰，push 前的檢查也能用 `--no-verify` 跳過。它讓你看見每一步留下什麼證據，但**不能**證明真的有兩個人審查過。真實團隊需要不同的人、機器與金鑰，以及伺服器端的強制檢查（例如受保護分支）。
```

```callout tip
💬 討論一下
- 回想各段結尾的討論：清單裡哪一步真的擋住過今天的錯誤？哪一步只是照流程做完？
- 同一個需求，沒有 Domain Memory 時 Agent 會怎麼做？花在 D1、D2 建立記憶的時間值得嗎？說得出證據的才算數。
```

## 檢查點 3 · 挑選提示詞與一項行動（第 174–178 分鐘）

① 為什麼做這一步

讓 Agent 從紀錄挑出有效的提示詞、改寫成能用在任何專案的版本，你只要挑；每個人輪流貼一次。最後小組選一項帶回團隊的行動；不知道選什麼時，再貼第二段。

② 貼給 Agent

```text
請先問我的名字，等我回答後再往下做。依 notes/ 與 docs/handoffs/ 裡今天的紀錄，以及 notes/retro.md，起草 5 段我回到自己的專案可以直接貼給 Agent 的提示詞，例如：交接前先驗證記憶、只引用查得到的 id、先列清單等人同意才寫入、故意改壞一處確認測試會抓到。
每段寫：什麼時候用、提示詞本身、做完要看什麼證據、今天的例子（只寫紀錄裡真的發生的事，沒有就寫「未觀察」）。不要綁定今天的 Smart Ticket 專案；會因專案而變的部分用一句話說明要換成什麼。
在對話列出 5 段的標題與一句說明，停下等我回「留第幾段」或「第 N 段改成…」。我選定後，只把我留下的寫進 notes/my-prompts-<我回答的名字>.md，寫完貼給我看。
```

```text
請依 notes/retro.md，提出 3 個有證據佐證的改善行動，類別從這幾種選：Domain Memory 內容、來源選擇、審查流程、工具、Agent 提示詞、人員責任。每個寫一句做什麼、一句證據（今天的哪個紀錄）、一句怎麼確認有效。不要修改任何檔案，列完停下等我們選。我們選定後，把它寫進 notes/retro.md 的「檢查點 3 · 行動」小節。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. notes/ 底下有用我的名字命名的 my-prompts 檔，裡面是我留下的提示詞，每段都有「做完要看什麼證據」。
2. notes/retro.md 有「檢查點 3 · 行動」，寫著我們選的行動。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請用白話說明缺了哪一個檔案或哪一段，再問我要留哪幾段或選哪一項行動，等我回覆後補上，然後停下。
```

## 檢查點 4 · 匯出與結束（第 178–180 分鐘）

① 為什麼做這一步

離開前刪掉今天練習用的簽章私鑰，並關掉「每個 commit 都要簽章」的設定，否則之後的 commit 都會失敗。由**夥伴**在自己的 Agent 對話貼下方提示詞；最後每個人填完下方回顧表並按「匯出」。

② 貼給 Agent

```prompt
# windows
請刪除今天練習用的簽章私鑰 signing-key（只刪這一個檔案，同一個資料夾裡的其他檔案不要動），再關掉這個 Repo 的「每個 commit 都要簽章」設定。
PowerShell 執行：Remove-Item -Force "$env:USERPROFILE\.dlc-keys\maintainer\signing-key"
Git Bash 執行：rm -f "$HOME/.dlc-keys/maintainer/signing-key"
同一個資料夾的 signing-key.allowed_signers 要留著：它只有公鑰，Git 驗證今天的簽章 commit 時要讀它；刪了，git log 會把今天的簽章都顯示成無法驗證。signing-key.pub 與 signing.json 也只有可公開的內容，可以留著。
再到 Repo 根目錄執行 git config --local --unset commit.gpgsign：金鑰刪掉後，這個 Repo 若仍要求每個 commit 都簽章，之後的 commit 都會失敗。repository 資料夾裡的 smart-ticket-dlc-base 與其他 resume- 開頭的 Repo（用過 Recovery 才有）也要做：到每一個的根目錄執行同一行；名稱以 -remote.git 結尾的是 push 用的遠端，跳過。這一行沒有任何輸出、結束碼是 5，代表那個 Repo 本來就沒開這個設定，不算失敗。
執行後確認 signing-key 已經不存在、signing-key.allowed_signers 還在，並逐一列出每個 Repo 是「已關閉」還是「本來就沒開（結束碼 5）」，用一兩句話回報。
# macos
請刪除今天練習用的簽章私鑰 signing-key（只刪這一個檔案，同一個資料夾裡的其他檔案不要動），再關掉這個 Repo 的「每個 commit 都要簽章」設定。
執行：rm -f "$HOME/.dlc-keys/maintainer/signing-key"
同一個資料夾的 signing-key.allowed_signers 要留著：它只有公鑰，Git 驗證今天的簽章 commit 時要讀它；刪了，git log 會把今天的簽章都顯示成無法驗證。signing-key.pub 與 signing.json 也只有可公開的內容，可以留著。
再到 Repo 根目錄執行 git config --local --unset commit.gpgsign：金鑰刪掉後，這個 Repo 若仍要求每個 commit 都簽章，之後的 commit 都會失敗。repository 資料夾裡的 smart-ticket-dlc-base 與其他 resume- 開頭的 Repo（用過 Recovery 才有）也要做：到每一個的根目錄執行同一行；名稱以 -remote.git 結尾的是 push 用的遠端，跳過。這一行沒有任何輸出、結束碼是 5，代表那個 Repo 本來就沒開這個設定，不算失敗。
執行後確認 signing-key 已經不存在、signing-key.allowed_signers 還在，並逐一列出每個 Repo 是「已關閉」還是「本來就沒開（結束碼 5）」，用一兩句話回報。
```

③ 確認結果（貼到夥伴的對話）

```text
請只檢查，不要修改任何檔案，也不要讀取金鑰內容：
1. 使用者資料夾 .dlc-keys/maintainer/ 底下的 signing-key 已不存在，signing-key.allowed_signers 還在。
2. repository 資料夾裡每個 Repo（-remote.git 結尾的除外）執行 git config --local --get commit.gpgsign 都沒有輸出。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請用白話說明哪個檔案或哪個 Repo 的設定不符。只刪 signing-key 這一個檔案，signing-key.allowed_signers 不要動；列出你要執行的指令，等我同意再做。
```

### 小組收尾

填表前，小組用兩分鐘對齊：已審查的事實真的改變了 Agent 的輸出嗎？證據是哪一條？你們帶回團隊的行動是什麼、誰負責、怎麼知道有效？把你們討論出的結論記下來：

```form
{"id": "retro-review", "title": "DLC 回顧","fields":[
{"id": "memory-changed-output", "label": "已審查的事實有沒有改變 Agent 的輸出？", "type": "select", "options": ["有，notes/retro.md 有證據", "沒有觀察到", "不確定，證據不足"]},
{"id": "action-category", "label": "我們帶回團隊的行動屬於哪一類？", "type": "select", "options": ["Domain Memory 內容", "來源選擇", "審查流程", "工具", "Agent 提示詞", "人員責任", "待研究"]},
{"id": "action", "label": "這項行動：誰、何時、用什麼證據確認", "type": "text", "hint": "一句話；細節已由 Agent 寫進 notes/retro.md。", "suggestions": ["待研究"]},
{"id": "done", "label": "離開前", "type": "checklist", "items": ["notes/my-prompts 已寫好，我會帶走", "簽章私鑰 signing-key 已刪除", "已匯出所有表單"]}
]}
```

```callout warning
離開前請匯出所有表單
表單只暫存在這個瀏覽器中。按下方按鈕下載整場的表單（ZIP），依主持人指定方式保存；Repo 的 `notes/` 與 `docs/handoffs/` 也一併保存。
```

```exportall
```
