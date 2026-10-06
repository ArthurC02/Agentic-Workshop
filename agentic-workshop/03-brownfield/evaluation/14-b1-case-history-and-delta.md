# B1 案例歷史與最小修改證據

> 讀者：主持人、驗收人員與教材產製 Agent。
> 使用時機：核對 B1 來源、最小修復、Regression 保留與恢復版本。
> 前置條件：Git 已安裝；閱讀 B1 Validation Report。
> 可見性：Evaluation／Agent Production，不供 Participant。

## 權威版本

持久化來源為 [b1-case-history.bundle](b1-case-history.bundle)，從 B0 Bundle Clone 後建立一次真實修復提交，完整延續 G0→G1→B0 的 10 個 Commit。

| 版本 | Tag | 完整 Commit |
|---|---|---|
| G1 | g1-greenfield-reference | `361bf00b43799dcf4117779f87e0679a5021c54e` |
| B0 | b0-brownfield-baseline | `392d920ce4510e5c2dd5df5ae2db25e9ab3b87e6` |
| B1 | b1-student-fare-fixed | `a1c1d45a26875feb2635f211059db5e8980035f7` |

本 Bundle 共 11 個實際 Commit，大小 **53,105 bytes**。案例 Commit 與作者 Repo Commit 分開管理；本次 Commit 對應已完成內容，不虛構原始開發順序。

## B0→B1 實際 Delta

`git diff --name-only b0-brownfield-baseline b1-student-fare-fixed` 僅列出五檔：

- `src/smart_ticket/domain/fare_policy.py`：唯一商業行為修改，`STUDENT_FARE_RATE` 由 85 改為 75。
- `src/smart_ticket/main.py`：App 版本由 B0 改為 B1。
- `pyproject.toml`：專案版本由 0.1.0 改為 0.2.1。
- `README.md`：標示 B1、Evaluation 用途及完整測試預期。
- `docs/version-history.md`：增加最小修復、來源與版本識別紀錄。

已實際執行針對 `tests/`、`docs/business-rules.md`、`docs/change-booking-guide.md`、`docs/discount-overview.md` 的跨 Tag Diff，exit code 0、無差異。測試期待值與案例均未弱化；既有優惠順序、改退票、座位、通知、Audit 及兩項受控文件落差保持原版本內容。B1 未加入最有利單一優惠或團體訂票。

## 實際來源驗證

從作者 Repo 根目錄操作：

```bash
git clone agentic-workshop/03-brownfield/evaluation/b1-case-history.bundle .codex-tmp/b1-history-review
git -C .codex-tmp/b1-history-review bundle verify ../../agentic-workshop/03-brownfield/evaluation/b1-case-history.bundle
git -C .codex-tmp/b1-history-review merge-base --is-ancestor b0-brownfield-baseline b1-student-fare-fixed
git -C .codex-tmp/b1-history-review diff b0-brownfield-baseline b1-student-fare-fixed -- src tests
git -C .codex-tmp/b1-history-review log --all --oneline --decorate
git -C .codex-tmp/b1-history-review for-each-ref
```

已實際完成 Bundle verify、重新 Clone 與 B0 祖先檢查，均成功；52 個追蹤來源檔與 `reference-solutions/b1-student-fare-fixed/` 的雙向檔案清單及全內容比對為 **0 差異**。比對排除 `.git`、虛擬環境及 caches，正規化 Git checkout 的 LF／CRLF。

完整可達歷史與 refs 已查核，僅包含 G0、G1、B0、B1；無 B2／B3 或隔離診斷 Commit。Bundle 與完整 Reference Solution 僅供 Evaluation；不得放入學員包。

## 完成條件

B1 真實延續 B0；商業行為變更只有唯一學生票率；測試未改、快照與 Tag 完整一致；App／專案 metadata 與文件明確識別 B1。測試是否全通過及 Runtime／API 結論由 B1 Validation Report 提供，不以 Git 或來源比對取代執行證據。
