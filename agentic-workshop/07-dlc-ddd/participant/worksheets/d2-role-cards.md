# D2 角色卡：提案者與夥伴

> 讀者：DDD（Domain-Driven Design，領域驅動設計）延伸課程學員。使用時機：D2（今天第二段）開始時，兩人決定角色後各自讀自己的卡。

D2 兩人一組，共用一台機器（提案者的機器與 Repo），但**各自用自己的 Agent 對話**：夥伴在同一台機器另開一個終端機，啟動自己的 Agent 對話，並一直開到課程結束（D3a–D3c 的檢查點 5 與 D4 的 commit 都在這個對話執行）。輪到誰的步驟，就由誰坐到鍵盤前，把 Runbook 上標著自己角色的提示詞貼給**自己的** Agent，讀回報、做決定。三人一組時，第三人當 Observer。

## 提案者（Proposer）

- **身分**：`proposer@example.com`（開場時設定的 Git 使用者）。
- **你的 Agent 負責**：反事實檢查（counterfactual：故意改壞一處程式，確認測試會失敗；抓到就顯示 killed）、把 D1 的候選整理成變更審查包（Change Package）並驗證、送出提案、夥伴核准後定案、套用與驗證。
- **你決定**：用哪一條規則做反事實檢查；審查包看起來完整了才回「送出」。
- **你的 Agent 不可以**：執行 `record-approval`、碰夥伴的金鑰、commit 或 push（本 Repo 的 commit 會用夥伴的金鑰簽章）。Plugin（課程提供的 domain-memory 命令列工具）只比對身分字串，**它擋不住冒用夥伴的名字**，所以這條界線靠你們兩人遵守。

## 夥伴（Maintainer，持鑰人）

- **身分**：`maintainer@example.com`。
- **你的 Agent 負責**：建立你的簽章金鑰（放在 Repo 外的 `%USERPROFILE%\.dlc-keys\maintainer\`）、設定審查政策與 push 檢查、把審查包讀給你聽、在你回「核准」之後執行 `record-approval` 與簽章 commit、寫出核准證明並驗證、最後 push；D3、D4 的簽章 commit 也由你的 Agent 執行。
- **你決定**：讀過 Agent 貼出的證據原文與測試結果後，回「核准」或「退回：原因」。只有你的回覆能讓簽章發生。
- **你要追問的**：每條規則的測試真的有跑嗎？反事實是 `killed`，還是指令只是沒報錯？證據那幾行真的在講這條規則嗎？
- **你可以拒絕**：證據不足就不核准。退回比蓋章有價值。

## Observer（三人組才有）

- 看每一步是不是在對的人的 Agent 對話裡執行：核准、簽章、push 只能出現在夥伴的對話；最後一起看 `verify-audit` 的結果與事件數。

## 金鑰規則（兩人都要遵守）

1. 私鑰只放在 `%USERPROFILE%\.dlc-keys\maintainer\`（Git Bash：`~/.dlc-keys/maintainer/`），不放進 Repo（即使是已忽略的資料夾也會被祕密掃描檢查 `scan-secrets` 掃到）、不放 `.ssh`、不貼給任何 Agent、不截圖、不貼到聊天或表單。
2. 金鑰只為今天的練習產生。課程結束後刪除整個 `%USERPROFILE%\.dlc-keys\maintainer\` 資料夾。
3. 同一組從頭到尾用同一種終端機（PowerShell 或 Git Bash），因為兩者的 `ssh-keygen` 不同。

## 誠實的提醒

今天兩個身分在同一台機器上，誰都能打出對方的名字。分開兩個 Agent 對話，是讓你看見「提案」與「核准」必須由不同的人決定；真正的安全來自不同的人、不同的機器與伺服器端的保護。回顧時會討論這一點。
