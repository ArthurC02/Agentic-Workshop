---
name: signed-commit
description: 夥伴（Maintainer）在自己的對話裡，把這一段的成果做成簽章 commit，必要時 push。夥伴要「commit」「提交」「簽章提交」這段成果時使用；提案者的對話不能用。
---

# signed-commit：夥伴審過後做簽章 commit

1. 確認這是夥伴的對話；是提案者的對話就停下，說明 commit 要由夥伴在自己的對話做。
2. 執行 `git status --short` 和經 dm 腳本的 `validate`。用白話列出這次要 commit 的檔案（`records/` 不算），加上 validate 結果，以及使用者指定的那份紀錄（`notes/<段落>.md` 的某一節或交接單）的摘要。停下等夥伴回「同意」。
3. 夥伴同意後執行（commit 訊息照提示詞給的）：
   - `git add -A -- . ':!records'`
   - `git -c "user.name=DLC Maintainer" -c "user.email=maintainer@example.com" commit -S -m "訊息"`
   - `git log --show-signature -1`
4. 回報 commit 編號和簽章那一行（應有 `Good "git" signature for maintainer@example.com`）。不顯示金鑰內容。
5. 提示詞要 push 時才 push：同一次執行裡先啟用 `.venv`、設 `PYTHONUTF8=1`，再 `git push`（第一次加 `-u origin HEAD`）。回報 hook 印出的 `Git governance is valid for N commits.`。

簽章錯誤或被 hook 擋下時：不改 Git 設定、不重做 commit、不用 `--no-verify`，貼出錯誤訊息、用白話解釋原因，停下。
