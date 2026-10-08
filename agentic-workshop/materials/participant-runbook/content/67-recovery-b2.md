---
id: recovery-b2
title: B2 Recovery 切換
minute: 63-76
group: recovery-b2
section: Brownfield｜Digital Worker
---

# B2 Recovery：63 分鐘按需切換

本頁是 Recovery（復原包：進度落後時改用的接續基線）。B2（導入不可疊加的最有利優惠政策）沒做完、但要接著做 B3 的小組，經主持人確認後，才會個別拿到本頁解鎖碼；一般 B3 解鎖碼打不開本頁。復原包只含 B2 該完成的修改，不含 B3 的完整實作；使用復原包不代表本組自己完成了 B2。

```callout info
現在在做什麼
- **情境**：B2 還沒做完，但時間到了，要換到已完成 B2 的版本接著做 B3。
- **你的目標**：保存原成果、換到復原包，確認版本正確後接續 B3。
- **今天的技巧**：開新對話先給規則與脈絡。換資料夾就開新的 Agent 對話，第一件事貼規則、把 `notes` 交給它讀，Agent 才知道之前發生什麼。
- **完成的樣子**：雜湊值相符、測試 55 passed、`/health` 正常；`notes/recovery-b2.md` 記下切換紀錄。
```

```download
id=recovery-63-b2 zip=recovery-63-b2.zip label=下載受控 B2 Recovery
```

- [ ] 先保存原本的成果，不要覆蓋：請原本的 Agent 把目前狀態 Commit，並把目前的變更內容（Diff）、最後一次測試結果與退出碼（exit code）、未完成事項寫進 `notes/b2.md`。
- [ ] 在原本的 Agent 對話貼上下方提示詞，請它停止舊版本的伺服器（不要停止別人的服務）：

```text
我們要切換到 B2 復原基線。請停止你在背景啟動的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 已經連不上，然後用白話告訴我結果。不要修改任何檔案，也不要停止不是你啟動的服務。
```

- [ ] 用檔案總管（右鍵「全部解壓縮」）或 Finder，把 `recovery-63-b2.zip` 解壓縮到新的資料夾（例如 `resume-b2-63`，不要覆蓋原成果），找到裡面的 `recovery-b2` 資料夾。
- [ ] 在 `recovery-b2` 開一個新的 Agent 對話（Session），先貼上 [B3](#b3) 檢查點 1 的工作規則，再依序貼上下方三段提示詞：

```text
請計算 recovery-63-b2.zip（位置：〈ZIP 所在資料夾〉）的 SHA256 雜湊並貼出來；再閱讀這個資料夾的 README 與 docs/context.md，用白話告訴我這是不是 B2 完成後的版本。不要修改任何檔案。
```

```text
請幫我準備這個專案的執行環境：確認 Python 版本是 3.13，在專案資料夾建立 .venv 虛擬環境並安裝 requirements.txt，接著執行 pytest -q。用白話告訴我：環境是否建好、測試有幾個通過／失敗／跳過，以及下一步要做什麼。遇到錯誤時先說明原因，不要自行修改程式。
```

```text
請在背景啟動這個專案的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 回傳 status=ok，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
```

- [ ] 核對：Agent 貼的 SHA256 與下載卡上的值相同（雜湊是檔案的指紋；一個位元組被改，值就不同）；測試預期 55 passed；`/health` 回傳 status=ok。任何一項不符就停止切換，請主持人確認。
- [ ] 版本要用包內說明文件（README、docs/context.md）、B2 的修改是否存在與測試結果一起確認，不能只看 Health 檢查。

- [ ] 把原成果的紀錄交給新對話，並請 Agent 記下切換經過。`〈 〉` 的內容由你們填寫：

```text
我們原本的成果在〈原成果資料夾〉。請把那裡的 notes 資料夾複製到這個資料夾（只複製 notes，不要動程式），讀 notes/shared-context.md 與 notes/b2.md，用白話告訴我原成果還有哪些未完成。再把下列內容寫進 notes/recovery-b2.md：切換原因與時間、原成果保存位置、SHA256／測試數／health 的實際結果與退出碼，以及「B2 的政策由 Recovery 提供，不是本組自己完成」。不要修改程式。
```

完成後接續 [B3](#b3)，仍須通過三個核准關卡（Gate）。

```form
{"id": "recovery-b2-record", "title": "B2 Recovery 紀錄","fields":[
{"id": "approver", "label": "1. 核准切換的主持人與分鐘", "type": "text", "suggestions": [{"label": "格式", "text": "〈姓名〉，第〈 〉分鐘"}]},
{"id": "verified", "label": "2. 雜湊值、55 passed、/health 三項都相符嗎？", "type": "select", "options": ["都相符", "有不符，已停止並請主持人確認"]},
{"id": "preserved", "label": "3. 原成果保存在哪個資料夾？", "type": "text", "suggestions": [{"label": "格式", "text": "〈資料夾路徑〉（已請 Agent Commit）"}]}
]}
```

```callout tip
這段學到的技巧
換資料夾或換版本就開新對話：先貼規則，再把 notes 交給 Agent 讀，它才接得上之前的脈絡。
```
