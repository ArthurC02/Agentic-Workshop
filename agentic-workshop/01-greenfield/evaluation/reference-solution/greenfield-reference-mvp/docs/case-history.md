# 案例 Repository 真實版本歷史

> 讀者：教材產製 Agent、維護者與 Evaluation 驗收人員。
> 使用時機：檢查 G0→G1 來源、重新匯出版本或準備 B0 演化前。
> 前置條件：Git 已安裝；具備 Evaluation 存取權限。

## 權威來源與重現

持久化案例歷史為上一層的 `g1-case-history.bundle`，其 `main` 與 `g1-greenfield-reference` 指向 G1；`g0-starter` 指向 G0。作者 Repo 的 Commit 與此案例 Repo 分開管理，不能混用版本識別。

Bundle 位於 `agentic-workshop/01-greenfield/evaluation/reference-solution/g1-case-history.bundle`。從作者 Repo 根目錄操作：

```bash
git clone agentic-workshop/01-greenfield/evaluation/reference-solution/g1-case-history.bundle .codex-tmp/g1-case-review
git -C .codex-tmp/g1-case-review bundle verify ../../agentic-workshop/01-greenfield/evaluation/reference-solution/g1-case-history.bundle
git -C .codex-tmp/g1-case-review log --oneline --decorate
git -C .codex-tmp/g1-case-review show g0-starter:src/smart_ticket/main.py
git -C .codex-tmp/g1-case-review show g1-greenfield-reference:src/smart_ticket/main.py
```

## 歷史的形成與用途

這是本次產製時建立的真實 Git Repository，依已存在的版本成果組裝四次實際 Commit：G0 初始版本、G1 核心實作、G1 測試、G1 文件；再以第五次驗證整合 Commit 同步新增 Unit Tests、版本來源與正式驗證證據。每次提交具有實際 Diff；未虛構逐功能開發時間或原始開發順序。查核 Commit 日期與差異時，以 Bundle 的 Git 資料為準。

G0 初始 Commit：`ee5c126`（Tag `g0-starter`）。G1 實作 Commit：`57028ad`。G1 測試 Commit：`43dc825`。G1 文件 Commit：`b9f1bd1`。最終第五次驗證整合 Commit 由 Tag `g1-greenfield-reference` 唯一識別，以 `git rev-parse g1-greenfield-reference` 取得完整雜湊。

G1 測試保留 G0 可執行 Health 與 Fare acceptance，移除功能 Skip，增加實際驗收案例。此歷史不能取代 Validation Report 或測試證據。

## 快照同步及後續 B0

`greenfield-reference-mvp/` 為 Tag `g1-greenfield-reference` 的獨立可執行快照；工作目錄 `.codex-tmp/g1-case-history/` 是暫存，Bundle 才是持久保存載體。匯出時只包含 Tag 追蹤檔，排除 cache、虛擬環境及 `.git`；以逐檔內容比對驗證 Bundle 與快照一致。日後修改權威案例 Repo 時應建立實際 Commit、更新相應版本識別與 Bundle，再重新匯出快照；不能只改快照後聲稱歷史已同步。

B0 必須從此 Bundle 的 G1 歷史延續，不能另起無 G1 祖先的 Repository。B0 時間快轉的歷史決策與案例演化另依 B0 規格產製；此文件不聲稱 B0 已存在。需為新演化另存對應 Bundle 並核對 G1 祖先、Tag 與快照。

## 可見性

Bundle 包含 G1 完整答案，只供 Evaluation／Agent Production 使用，不得混入 Participant 包。未來 B0 學員包即使提供案例歷史，也須檢查 Branch、Tag 與所有可達 Commit，不得讓 B1–B3 未來答案可見。原始作者 Repo 的完整歷史同樣不得直接提供學員。

## 完成條件

Bundle 可驗證且可 Clone；兩個 Tag 與實際 Commit 可查；G1 Tag 快照內容一致；後續 B0 有可延續來源；歷史與答案隔離經驗證。此文件未宣稱尚未執行的 B0 或打包檢查完成。