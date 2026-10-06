# B0 案例歷史與乾淨副本證據

> 讀者：教材產製 Agent、維護者與 Evaluation 驗收人員。
> 使用時機：核對 B0 來源、恢復基線或交付歷史前。
> 前置條件：Git 可用；閱讀 B0 Validation Report 與本機實際來源。
> 可見性：Evaluation／Agent Production，不提供 Participant。

## 權威來源

本目錄的 [b0-case-history.bundle](b0-case-history.bundle) 是案例 Repository 持久化來源。作者 Repo 的 Commit 與案例 Commit 分開識別。B0 從 G1 Bundle Clone 後實際提交增量，沒有另起歷史或加入診斷修復版本。

| 來源／版本 | 實際 Commit |
|---|---|
| G0 `g0-starter` | `ee5c126d54f5a8510ae745d7c98b95f9acc8eea1` |
| G1 `g1-greenfield-reference` | `361bf00b43799dcf4117779f87e0679a5021c54e` |
| B0 核心演化 | `0364721` |
| B0 測試擴充 | `3f354f9` |
| B0 文件與 ADR | `06f9954` |
| B0 最終 `b0-brownfield-baseline` | `392d920ce4510e5c2dd5df5ae2db25e9ab3b87e6`，最終文件編碼與換行正規化。 |

這些是本次產製依已存在成果組裝的真實 Git Commit，可核對 Diff，不聲稱重現原始開發時間或逐功能修改順序。歷史文件會包含已發生的 G0、G1 行為與紀錄；G1 是 B0 的前身，並非未來修復答案。G1 的 `docs/case-history.md` 已在 B0 文件 Commit 移除，B0 `docs/version-history.md` 由本版本文件取代。

最終 Bundle 大小為 **50,809 bytes**。前次通知與 Audit 驗證 Commit `3e0fa1e` 保留，最終純文件格式 Commit `392d920` 追加其後，未重寫演化歷史。`392d920` 的最終 Bundle 已再驗證與重新 Clone，52 個來源檔全內容比對仍為 0 差異。

## 還原與祖先核對

從作者 Repo 根目錄操作：

```bash
git clone agentic-workshop/03-brownfield/evaluation/b0-case-history.bundle .codex-tmp/b0-history-review
git -C .codex-tmp/b0-history-review bundle verify ../../agentic-workshop/03-brownfield/evaluation/b0-case-history.bundle
git -C .codex-tmp/b0-history-review merge-base --is-ancestor g1-greenfield-reference b0-brownfield-baseline
git -C .codex-tmp/b0-history-review log --oneline --decorate
git -C .codex-tmp/b0-history-review for-each-ref
```

G1 祖先檢查應回傳 exit code 0。最終 Bundle 檢查須確認 Branch、Tag、所有可達 Commit 只截止 B0；不得包括 B1–B3 答案或把學生率改為 75 的隔離診斷 Commit。

## 快照與 clean-copy

Participant 原始快照為 `../participant/repository/smart-ticket-b0/`；乾淨副本依原規格放在 `reference-baseline/smart-ticket-b0-clean-copy/`。clean-copy 是未修復的 B0，同樣保留原始測試預期，不能改成 B1。

比對來源檔時只包含版本允許的程式、測試、設定與文件，排除 `.git`、`__pycache__`、`.pytest_cache`、虛擬環境。Clone 的 checkout 可能依 Git 設定轉換 LF／CRLF；歷史內容比對應正規化換行並檢查兩向檔案清單，不能只核對部分檔案。

已實際執行最終 Bundle verify（exit code 0）、重新 Clone、G1 祖先檢查（exit code 0）、52 個追蹤來源檔雙向清單與全部內容比對：0 差異（LF／CRLF 正規化）。`for-each-ref` 與 `log --all` 查核全部可達歷史只包含 G0、G1 與 B0 的 10 個實際 Commit；無 B1–B3 Tag／Commit，也未包含隔離診斷的修復版本。clean-copy已實際建立，與正式B0雙向52檔清單、內容及SHA256一致，保留85%學生Bug及全部正確測試；逐檔雜湊見validation-evidence.json。診斷副本僅一行rate不同，正式套件5failed／39passed與診斷44passed結果詳見Validation Report。clean-copy沒有獨立再跑套件，以完全一致檔案與正式執行證據核對。

## 完成條件

真實 G1 祖先、B0 Tag 與 Bundle 可核對；最終快照完整一致；無未來答案可達；clean-copy 實際存在並保持同一 B0 內容與測試預期。驗證限制需如實列明。
