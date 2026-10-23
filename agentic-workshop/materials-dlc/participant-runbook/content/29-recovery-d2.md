---
id: recovery-d2
title: D2 Recovery 切換
minute: 45-70
group: dlc-rec-d2
section: D2｜審查與核准
---

# D2 Recovery：視需要接續

D2 Recovery（復原包）的內容：起始 Repo，加上已審查、簽章並套用的 Registry，裡面全是已審查事實。原 Repo 保留不動；Agent 會在紀錄寫明這段由 Recovery 提供。

```download
id=recovery-dlc-d2 zip=recovery-dlc-d2.zip label=下載 D2 Recovery
```

## 步驟 1 · 【提案者】保存原成果並解出 Recovery

① 為什麼做這一步

先記下原 Repo 做到哪裡，再把 Recovery 解成和原 Repo 同一層的 `resume-d2`；原 Repo 不動。
- 按上方按鈕下載 `recovery-dlc-d2.zip`，存到「下載」資料夾
- 把下方提示詞貼到**原本**的提案者 Agent 對話

② 貼給 Agent

```text
我們要改用 D2 Recovery 接續，recovery-dlc-d2.zip 在下載資料夾。照 dlc-recovery 做步驟 1：先問我們做到哪、為什麼沒完成，原 Repo 不動。做完用 check 檢查。
```

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：resume-d2 已建立，原 Repo 沒有被改動。
```

失敗時（中途失敗、要重跑）：

```text
先停，原 Repo 不要動。哪一步失敗？照 dlc-recovery 的「中途失敗要重跑」告訴我要刪哪兩個資料夾，等我同意再刪掉重跑。
```

## 步驟 2 · 【夥伴】在 resume-d2 開新的 Agent 對話，接手簽章

① 為什麼做這一步

Recovery 的簽章歷史來自另一把金鑰。夥伴還原歷史後，改用自己的金鑰簽章，之後的 commit 才通得過推送檢查。
- 夥伴結束原 Repo 裡自己的 Agent 對話，在 `resume-d2` 另開一個終端機，啟動自己的**新**對話
- Agent 列出要 commit 的檔案時，確認裡面沒有私鑰檔 `signing-key`、沒有 `records/`，再回「同意」；`domain-memory/` 的政策檔和稽核紀錄（接手金鑰時改的）在清單裡是預期的

② 貼給 Agent

```text
我是夥伴。我們改用 D2 Recovery，照 ../../recovery-d2/recovery-dlc-d2/RECOVERY.md 第 2 節接手簽章，commit 前先列檔案等我同意。做完用 check 檢查。
```

③ 確認結果（貼到夥伴的對話）

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：簽章 commit 有 Good "git" signature for maintainer@example.com，也有 Git governance is valid for 1 commit.。
```

失敗時：

```text
先停，不要自己改設定、不要重做 commit、不要繞過 hook。錯誤訊息是什麼意思？是哪一個前提沒做到（例如金鑰、政策、HEAD 指向哪個 commit）？你建議怎麼做？
```

④ 補充

**這個夥伴對話開到課程結束**：D3a–D3c 檢查點 5 與 D4 的簽章 commit 都在這裡執行。

## 步驟 3 · 【提案者】在 resume-d2 開新的 Agent 對話，建環境並驗證

① 為什麼做這一步

提案者在 `resume-d2` 建好環境，確認測試、Registry 與稽核紀錄都可用，才接續下一段。
- 結束提案者原本的對話，到 `resume-d2` 開一個**新的** Agent 對話
- 看 Agent 是否在紀錄寫明「D2 的成果由 Recovery 提供，不是我們自己完成」

② 貼給 Agent

```text
我是提案者。我們改用 D2 Recovery，夥伴已接手簽章。照 ../../recovery-d2/recovery-dlc-d2/RECOVERY.md 第 3 節建環境並驗證。做完用 check 檢查。
```

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：測試全部 passed（多 1 個 warning 是預期的），Registry is valid.，verify-audit 是 "status": "valid"。
```

失敗時（測試結果不符就停止切換，請主持人確認）：

```text
先停，不要改程式或 domain-memory/，也不要 commit。哪一行指令失敗？錯誤訊息是什麼意思？列出建議的處理方式，等我們和主持人決定。
```

完成後回到 [D3a](#d3a)：切換已用掉 8–10 分鐘，直接照頁首「時間不夠時的最低完成線」做。
