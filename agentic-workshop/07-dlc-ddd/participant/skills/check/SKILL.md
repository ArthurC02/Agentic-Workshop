---
name: check
description: 檢查剛完成的一段工作是不是真的完成。使用者說「用 check 檢查」「確認結果」，或要驗收一個檢查點時使用。只讀不改。
---

# check：檢查一段工作

只讀：不建立、修改或刪除任何檔案，不 commit，不修程式，不執行會寫入 `domain-memory/` 的指令，不讀私鑰檔 `signing-key`。

1. 找出這一段該完成什麼：這個檢查點的提示詞、使用者回覆的決定、已核准的計畫或交接單、需求卡的驗收條件，以及使用者這次另外指定的條件。
2. 自己執行指令取得實際結果，不憑記憶、不只看 notes：完整測試、`git status --short`、`git log`（看簽章加 `--show-signature -1`）、經 dm 腳本的唯讀 Plugin 指令（例如 `validate`、`verify-evidence`、`verify-sources`、`verify-audit`、`governance-readiness`、`get-record`、`get-context`），以及檔案和段落是否存在。測試例外：提示詞說「不用重跑」或「沿用」，或 notes 記下最近一次完整測試後程式和測試都沒改過（用 `git status --short` 確認），就不重跑，引用 notes 裡的數字和時間。紀錄是候選還是已審查，以指令輸出為準。`records/`（make_record.py 的暫存）不 commit，`git status` 列出它不算未提交的變更；push 之後才補寫的 notes（例如 D2 檢查點 6 push 後的 `notes/d2.md`）還沒 commit 也是預期的。
3. 對照三樣：notes 裡寫的、實際結果、該完成的事（決定、計畫、驗收條件）。
4. 列出對不上的地方，每條附證據（檔案位置或指令結果）；都對得上就不用列。
5. 這段有跑測試時，倒數第二行寫通過、失敗、跳過各幾個；最後一行只寫「成功」，或「失敗：」加一句原因。
