---
id: recovery-b2
title: B2 Recovery 切換
minute: 63-76
group: recovery-b2
section: Brownfield｜Digital Worker
---

# B2 Recovery：63 分鐘按需切換

本頁是 Recovery（復原包：進度落後時改用的接續基線）。B2（導入不可疊加的最有利優惠政策）沒做完、但要接著做 B3 的小組，經主持人確認後，才會個別拿到本頁解鎖碼；一般 B3 解鎖碼打不開本頁。復原包只含 B2 該完成的修改，不含 B3 的完整實作；使用復原包不代表本組自己完成了 B2。

```download
id=recovery-63-b2 zip=recovery-63-b2.zip label=下載受控 B2 Recovery
```

- [ ] 先保存原本的成果，不要覆蓋：請原本的 Agent 把目前狀態 Commit，並用白話列出目前的變更內容（Diff）、最後一次測試結果與退出碼（exit code）；你保存核准關卡（Gate）紀錄與未完成事項。
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

在新對話中明確告訴 Agent：現在接手的是哪個版本、原成果還有哪些未完成、已確認的規則，以及 B3 已核准的範圍；更新共同脈絡（Shared Context）後，接續 [B3](#b3)，仍須通過三個核准關卡（Gate）。

```form
{"id": "recovery-b2-record", "title": "B2 Recovery 紀錄","fields":[
{"id": "decision", "label": "切換原因／核准的主持人／時間／復原包來源", "type": "textarea", "suggestions": [{"label": "觸發範本", "text": "觸發：〈B2 未完成的原因〉\n主持核准人：〈姓名〉；時間：第〈 〉分鐘\n提供來源：recovery-63-b2.zip"}]},
{"id": "preserved", "label": "原成果保存路徑／變更內容（Diff）／Gate 狀態／未完成事項", "type": "textarea", "suggestions": [{"label": "保存範本", "text": "原成果路徑：〈路徑〉\n變更內容：〈Agent 已 Commit／摘要〉\nGate：〈狀態〉\n未完成：〈…〉"}]},
{"id": "verification", "label": "新目錄／確認是 B2 版本的證據／安裝、55 項測試與 Health 的實際結果及退出碼", "type": "textarea", "suggestions": [{"label": "驗證範本", "text": "新目錄：〈路徑〉\nB2 版本證據：〈SHA256／README／docs/context.md〉\n安裝：〈結果〉，退出碼〈 〉\npytest -q：〈 〉 passed，退出碼〈 〉\nHealth：〈實際回應〉"}]},
{"id": "context", "label": "新對話（Session）或重新提供的背景／接續的核准範圍／哪些不是本組自己完成的", "type": "textarea", "suggestions": [{"label": "接續範本", "text": "〈新 Session／重新輸入 Context〉\n接續核准範圍：〈B3 範圍〉\n非自行完成：B2 能力由 Recovery 提供"}]}
]}
```
