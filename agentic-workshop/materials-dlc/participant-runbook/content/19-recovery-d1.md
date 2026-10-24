---
id: recovery-d1
title: D1 Recovery 切換
minute: 43-70
group: dlc-rec-d1
section: D1｜共同語言與邊界
---

# D1 Recovery：視需要接續

D1 Recovery（復原包）的內容：起始 Repo，加上已確認的來源和一組 D1 候選。原 Repo 保留不動；Agent 會在紀錄寫明這段由 Recovery 提供。

```download
id=recovery-dlc-d1 zip=recovery-dlc-d1.zip label=下載 D1 Recovery
```

## 步驟 1 · 保存原成果並解出 Recovery

① 為什麼做這一步

先記下原 Repo 做到哪裡，再把 Recovery 解成和原 Repo 同一層的 `resume-d1`；原 Repo 不動。
- 按上方按鈕下載 `recovery-dlc-d1.zip`，存到「下載」資料夾
- 把下方提示詞貼給**原本**的 Agent
- Agent 會先問做到哪、為什麼沒完成，最後一行是「等你們回答」：回一句就好，例如「做到檢查點 4，時間不夠」
- Agent 建立 Skill 資料夾時，工具若跳出允許視窗，按允許

② 貼給 Agent

```text
我要改用 D1 Recovery 接續，recovery-dlc-d1.zip 在下載資料夾。照 dlc-recovery 做步驟 1：先問我做到哪、為什麼沒完成，原 Repo 不動。做完用 check 檢查，最後一行寫成功或失敗。
```

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：resume-d1 已建立，原 Repo 沒有被改動。
```

失敗時（中途失敗、要重跑）：

```text
先停，原 Repo 不要動。哪一步失敗？照 dlc-recovery 的「中途失敗要重跑」告訴我要刪哪兩個資料夾，等我同意再刪掉重跑。
```

## 步驟 2 · 在 resume-d1 開新的 Agent 對話，還原並驗證

① 為什麼做這一步

在 `resume-d1` 還原 Git 歷史、建環境，確認 Recovery 的 Registry 可用。
- 結束目前的 Agent 對話，在 `resume-d1` 資料夾重新開啟 Agent
- 看 Agent 是否在紀錄開頭寫明「D1 的成果由 Recovery 提供」

② 貼給 Agent

```text
我要改用 D1 Recovery 接續。照 ../../recovery-d1/recovery-dlc-d1/RECOVERY.md 第 2 節還原並驗證，domain-memory/ 不要 commit。做完用 check 檢查，最後一行寫成功或失敗。
```

③ 確認結果

回報最後一行已是成功就不用再貼；沒有才貼：

```text
用 check 檢查剛才這一段：測試全部 passed，Registry is valid.，domain-memory/ 還是未追蹤。
```

失敗時：

```text
先停，不要改 domain-memory/，也不要 commit。哪一行指令失敗？錯誤訊息是什麼意思？列出建議的處理方式，等我和主持人決定。
```

完成後回到 [D2](#d2)：夥伴在 `resume-d1` 另開終端機與自己的 Agent 對話。
