# G0 → G1 Version History

> 讀者：主持人、驗收人員與教材產製 Agent。
> 使用時機：版本來源核對與演化規劃。
> 前置條件：閱讀 [README](../README.md) 與 [案例歷史](case-history.md)。
> 可見性：Evaluation／Agent Production。

| 版本 | 定位 | 差異 |
|---|---|---|
| G0 - Starter Repository | 框架與固定資料 | Health 可用，四業務 API 501，11 主要 TODO，8 功能測試 Skip。 |
| G1 - Greenfield Reference MVP | 完整 MVP 標準快照 | 完成查詢、訂票、票價、付款、Order 及 Router 工作點，啟用原功能測試並新增邊界驗證。 |

G1 延續 G0 模型、Schema、Seed、Store 及分層。功能包括有座位班次精確篩選、1–4 人及容量限制、逐位成人／學生 75% 計價、座位保留、待付款狀態、付款唯一訂單與查詢錯誤。付款採既有獨立 PaymentService。

## 實際案例歷史

持久化來源為 `evaluation/reference-solution/g1-case-history.bundle`，包含真實案例 Repository 的完整歷史。這是產製時依既有成果依序組裝的實際 Commit，不聲稱重現原始開發時間或逐功能開發紀錄。

| Commit 識別 | 已提交內容 |
|---|---|
| `ee5c126`（`g0-starter`） | G0 初始可啟動骨架與固定資料。 |
| `57028ad` | G1 核心實作、Repository Protocol 與共用鎖。 |
| `43dc825` | 解除功能 Skip 並補足 API 驗收案例。 |
| `b9f1bd1` | G1 規則、API、架構、README 與歷史來源文件。 |
| `g1-greenfield-reference` | 最終驗證整合：補足 Unit Tests，同步來源紀錄與正式驗證證據；以 Tag 取得本次 Commit 的完整雜湊。 |

驗證整合前已在 G1 獨立環境正式執行 `pytest -q`：`28 passed, 1 warning in 0.21s`，無 Fail、Skip 或 XFail。已知 Warning 的詳細說明與其餘啟動／API／追溯證據，以外層 G1 Validation Report 為準。

Tag 指向、Bundle 可用性與快照同步由 Bundle 驗證、Clone 及全檔內容比對確認。後續 B0 必須由這份案例歷史的 G1 延續；不得另起沒有 G1 祖先的 Repository。Bundle 含完整 G1 答案，不供 Participant。

## 完成條件

版本與實際檔案一致，TODO 與原 Skip 的解除可核對，Commit／Tag 可由 Bundle 查證；測試、啟動及 Acceptance 結論以正式 Validation Report 為準。