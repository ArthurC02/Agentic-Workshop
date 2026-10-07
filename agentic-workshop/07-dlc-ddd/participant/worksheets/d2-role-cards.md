# D2 角色卡：Proposer 與 Maintainer

> 讀者：DDD 延伸課程學員。使用時機：D2 開始時，兩人決定角色後各自讀自己的卡。

D2 兩人一組，**只用一台機器**（Proposer 的機器與 Repo）。兩人輪流坐到鍵盤前：輪到誰的步驟，就由誰親手輸入。三人一組時，第三人當 Observer。

## Proposer（提案人）

- **身分**：`proposer@example.com`（開場時設定的 Git 使用者）。
- **你負責**：把 D1 的候選整理成 Change Package、執行 counterfactual、填寫並驗證套件、送出提案（`submit-proposal`）、最後套用（`apply-approved-updates`）與驗證。
- **你不可以**：執行 `record-approval`；碰 Maintainer 的私鑰；替 Maintainer 執行簽章 commit。Plugin 只比對身分字串，**它擋不住你冒用夥伴的名字**，所以這條規則靠你們兩人遵守。
- **你要準備給夥伴看的**：要升級哪些候選、每一條規則對應哪個測試、counterfactual 的 `killed` 輸出。

## Maintainer（維護者，持鑰人）

- **身分**：`maintainer@example.com`。
- **你負責**：建立自己的簽章金鑰（放在 Repo 外的 `%USERPROFILE%\.dlc-keys\maintainer\`）、決定授權誰簽章、審查提案並 `record-approval`、親手做簽章 commit、確認 `verify-git-governance`。
- **你要問 Proposer 的**：這些候選的證據你看過了嗎？每條規則的測試真的有跑嗎？counterfactual 是 `killed` 還是只是 exit 0？
- **你可以拒絕**：證據不足就不核准。退回比蓋章有價值。

## Observer（三人組才有）

- 對照「D2 簽章流程清單」，每一步確認是**對的人**在操作，並在最後核對 `verify-audit` 的輸出與事件數。

## 金鑰規則（兩人都要遵守）

1. 私鑰只放在 `%USERPROFILE%\.dlc-keys\maintainer\`（Git Bash：`~/.dlc-keys/maintainer/`），不放進 Repo（即使是已忽略的資料夾也會被 `scan-secrets` 掃到）、不放 `.ssh`、不截圖、不貼到聊天或表單。
2. 金鑰只為今天的練習產生。課程結束後刪除整個 `%USERPROFILE%\.dlc-keys\maintainer\` 資料夾。
3. 同一組從頭到尾用同一種終端機（PowerShell 或 Git Bash），因為兩者的 `ssh-keygen` 不同。

## 誠實的提醒

今天兩個身分在同一台機器上，誰都能打出對方的名字。這是**教學示範**，讓你看見治理的每一步留下什麼證據；真正的安全來自不同的人、不同的機器與伺服器端的保護。回顧時會討論這一點。
