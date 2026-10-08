---
id: b0-context
title: B0 系統 Context 與已知限制
minute: 33-39
group: timeskip
section: Brownfield｜Teammate
---

# B0 系統 Context 與已知限制

個人分析前，請先閱讀本頁兩份文件；B0 Repository 內的 README、架構文件與 ADR 可以自己讀，也可以請 Agent 用白話摘要。這些內容也可以交給你的 Agent 作為 Context。你不需要讀程式。

ADR（Architecture Decision Record，架構決策紀錄）說明當時的選擇與取捨；Context 指分析所需的背景資料。

```callout info
文件是線索，不是結論
文件可作 Context，但不保證全部敘述與程式完全同步。重要結論請 Agent 用白話說明程式、規則、測試三者是否一致，再由你判斷哪些是事實、哪些是假設；不把文件或單一 Agent 的推論視為已確認事實。
```

## B0 系統 Context

```include
zip=participant-33-analysis.zip path=agentic-workshop/03-brownfield/participant/01-system-context.md
```

## B0 已知限制

```include
zip=participant-33-analysis.zip path=agentic-workshop/03-brownfield/participant/02-known-constraints.md
```

## B0 Repository 內的文件

下列文件位於 B0 ZIP 的 `smart-ticket-b0` 資料夾內，可以直接在你解壓縮的 Repository 中開啟，或請你的 Agent 閱讀後用白話摘要。

| 檔案 | 內容 |
|---|---|
| `README.md` | 安裝、測試、啟動方式與文件索引 |
| `docs/business-rules.md` | 商業規則 |
| `docs/architecture.md` | 架構 |
| `docs/api-summary.md` | API 摘要 |
| `docs/context.md` | B0 Context |
| `docs/change-booking-guide.md` | 改票指南 |
| `docs/discount-overview.md` | 優惠概覽 |
| `docs/adr/001-use-in-memory-repositories.md` | ADR 001 |
| `docs/adr/002-introduce-discount-policy.md` | ADR 002 |
| `docs/adr/003-record-notifications-synchronously.md` | ADR 003 |

- [ ] 已閱讀 B0 系統 Context 與已知限制。
- [ ] 已閱讀（或請 Agent 用白話摘要）`README.md`、`docs/architecture.md` 與 ADR，理解歷史取捨。
- [ ] 知道哪些結論需要請 Agent 對照程式、規則與測試是否一致。

下一步：[個人 Agent 分析](#individual-analysis)。
