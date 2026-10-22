---
id: recovery-b2
title: B2 Recovery 切換
minute: 63-76
group: recovery-b2
section: Brownfield｜Digital Worker
---

# B2 Recovery：第 63 分鐘，必要時才切換

```callout info
現在在做什麼
- **情境**：B2 還沒做完，但時間到了，要換到已完成 B2 的版本接著做 B3。
- **你的目標**：保存原成果、換到復原包，確認版本正確後接續 B3。
- **今天的技巧**：開新對話先給規則與脈絡（加深一層）：把原成果的 `notes/`、`AGENTS.md` 和 Skill 帶過來。
- **完成的樣子**：雜湊值相符、測試 55 passed、`/health` 正常；`notes/recovery-b2.md` 記下切換紀錄。
```

先按下方按鈕下載復原包，存在瀏覽器預設的下載資料夾即可。記下按鈕旁的 SHA256 雜湊：它是檔案的指紋，用來確認檔案沒被改過。

```download
id=recovery-63-b2 zip=recovery-63-b2.zip label=下載受控 B2 Recovery
```

## 步驟 1 · 保存原成果並解開復原包

① 為什麼做這一步

先把原成果 Commit、停掉伺服器，換版本時才不會弄丟成果或搶埠號。你判斷 Agent 算出的 SHA256 前 12 碼，和下載按鈕旁的值相同（大小寫不算）。不同就停止切換，請主持人確認。

② 貼給 Agent

在**原本的** Agent 對話貼上：

```text
我們要切換到 B2 復原包。先把目前狀態 Commit，把變更、最後一次測試結果和沒做完的事寫進 notes/b2.md，再停掉你啟動的伺服器。
接著到下載資料夾找 recovery-63-b2.zip（檔名可能多了 (1)；找不到就問我；只有同名資料夾、沒有 ZIP，就提醒我 Safari 可能已自動解開，要到 Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」再重新下載），算出 SHA256 貼給我，解壓到原成果旁邊的新資料夾 resume-b2-63，告訴我裡面 recovery-b2 和原成果資料夾的完整路徑。
```

③ 確認結果

```text
用 check 檢查剛才這一段：原成果已 Commit，你啟動的伺服器已停止，resume-b2-63 裡有 recovery-b2。
```

失敗時：

```text
先停。哪一項不符？只補做那一項，不要改程式，也不要停不是你啟動的程式。
```

## 步驟 2 · 在復原包開新對話，接上脈絡

① 為什麼做這一步

新對話帶著原成果的 `notes/`、`AGENTS.md` 和 Skill，就接得上脈絡，不用重講。你判斷 Agent 依包內文件和測試結果，確認這是 B2 完成後的版本；只看 `/health` 不算。不符就停止，請主持人確認。

② 貼給 Agent

在 `recovery-b2` 資料夾開一個**新的** Agent 對話，貼上：

```text
這是 B2 的復原包，我們從這裡接著做。先一次問我兩件事：原成果資料夾的路徑，以及 SHA256 前 12 碼和按鈕旁的是否相符。
再把原成果的 notes/、AGENTS.md 和你放 Skill 的資料夾複製過來（覆蓋這裡的 AGENTS.md，不動程式），然後重讀 AGENTS.md：裡面還指向原成果資料夾的路徑改成這裡的；沒有「審查準則」一節就直接告訴我。
接著照 AGENTS.md 建好環境、跑測試、啟動伺服器，給我 /docs 網址；讀 README 和 docs/context.md，告訴我這是不是 B2 完成後的版本；讀 notes/b2.md，告訴我原成果還有哪些沒做完。
最後把切換紀錄寫進 notes/recovery-b2.md：原因與時間、原成果位置、SHA256 比對、測試數、health 結果，以及「B2 的政策由 Recovery 提供，不是本組自己完成」。做完用 check 檢查。
```

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：測試是 55 passed，/health 正常。
```

失敗時：

```text
先停，不要再改。哪一項不符？你建議怎麼做？
```

④ 補充

Agent 說 `AGENTS.md` 沒有「審查準則」時（原成果沒做完共同脈絡），才貼這段：

```text
請在 AGENTS.md 加一節「審查準則」，照下面原文抄，不改寫：
寫程式的 Agent 自己審、另開對話審查，都照這一節。先用 git status 與 git diff 對照這段的起點 Commit（提示詞沒指定就用最近一次 Commit），列出改了哪些檔案、各改什麼、為什麼（notes/、AGENTS.md、Skill 資料夾、b3-docs/ 不列）。再回答三題「是／否／不確定」，各附實際指令與結果：(1) 改的檔案都在核准的計畫或範圍裡；(2) 測試總數沒有比這段開始時少，也沒有新增 skip 或 xfail；(3) 沒有刪除測試，除了經人核准的過時期待值，沒有修改既有測試的期待值（用 git diff 檢查 tests 資料夾；有改的逐一列出測試名稱、Rule ID 與核准紀錄位置）。分級：任一題是「否」或「不確定」，或宣稱通過卻沒有實際執行的指令與結果，是「重要」；文件措辭、命名不清楚是「小問題」，小問題最多報 5 條，其餘只寫條數；排版與寫法偏好不用報。
```

完成後回到 [B3](#b3)，從檢查點 1 開始，走「用 Recovery 的組：走縮短版」，目標 Level 1。

```form
{"id": "recovery-b2-record", "title": "B2 Recovery 紀錄","fields":[
{"id": "verified", "label": "1. 雜湊值、55 passed、/health 三項都相符嗎？", "type": "select", "options": ["都相符", "有不符，已停止並請主持人確認"]},
{"id": "preserved", "label": "2. 原成果已 Commit 並保留在原資料夾", "type": "checkbox"}
]}
```
