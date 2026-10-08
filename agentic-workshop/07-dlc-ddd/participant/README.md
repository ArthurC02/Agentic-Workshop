# DDD 延伸課程：Smart Ticket 領域建模

本延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課）約 3 小時，主題是 DDD（Domain-Driven Design，領域驅動設計）。你會先用 domain-memory Plugin（課程提供的命令列工具）為 Smart Ticket 建立 Domain Registry：一組存在程式庫 `domain-memory/` 資料夾裡、記錄領域知識的 JSON 檔，內容包括 Bounded Context（名詞與規則意義一致的範圍）、通用語言（團隊共用的名詞定義）、Aggregate（聚合：必須一起保持一致的一組資料，只能從 Aggregate root 這個入口修改）與商業規則。接著再用 DDD 的方式實作三個新需求。

名詞不熟請看 Runbook（課堂操作手冊）的〈詞彙表〉頁。

## 今天的四段

D1–D4 是今天四段的代號；D3 再分 a、b、c 三張需求。

| 段落 | 內容 | 用到的檔案 |
|---|---|---|
| D1 | 選定證據來源，找出 Context、詞彙與規則，登記為候選 | `worksheets/d1-source-selection.md`、`worksheets/d1-model-canvas.md` |
| D2 | 兩人一組：一人提案、一人審查核准並簽章，把候選升為已審查（reviewed）事實 | `worksheets/d2-role-cards.md`、`worksheets/d2-signing-checklist.md` |
| D3a | 實作需求卡 01：電子發票 | `scenarios/01-e-invoice.md`、`worksheets/d3-decision-card.md` |
| D3b | 實作需求卡 02：點數折抵 | `scenarios/02-points-redemption.md`、`worksheets/d3-decision-card.md` |
| D3c | 實作需求卡 03：團體部分退款 | `scenarios/03-group-partial-refund.md`、`worksheets/d3-decision-card.md` |
| D4 | 把今天的 Domain Memory 交接給下一個 Agent 或同事 | `worksheets/d4-handoff-template.md` |

每段的操作步驟與「檢查點」（段內的小關卡）都在 Runbook 對應的頁面。

## 資料夾內容

| 路徑 | 內容 |
|---|---|
| `repository/smart-ticket-dlc-base/` | 起始程式庫：上線 12 個月的 Smart Ticket 訂票後端 |
| `scenarios/01-e-invoice.md` | 需求卡 01：接入外部電子發票服務 |
| `scenarios/02-points-redemption.md` | 需求卡 02：會員點數折抵 |
| `scenarios/03-group-partial-refund.md` | 需求卡 03：團體訂票部分取消退款 |
| `worksheets/` | 各段要填寫的工作表（見上方段落表） |
| `tools/` | 輔助腳本：代打 Plugin 長指令、產生 JSON、檢查環境（說明見 `tools/README.md`） |

程式庫的產品規則文件在 `docs/requirements/`，ADR（Architecture Decision Record，架構決策紀錄）在 `docs/adr/`。需求卡中的商業數字與驗收條件是唯一依據，不要自行補規則；卡片末尾的「待團隊決定的問題」由你和團隊決定，並記錄理由。

## 執行程式庫

需要 Python 3.13。本程式庫用 `pip install -r requirements.txt` 安裝依賴套件即可，不需要 `pip install -e .`。

Windows PowerShell（主要方式）：

```powershell
cd repository/smart-ticket-dlc-base
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q                           # 開始前應全部通過
uvicorn smart_ticket.main:app --app-dir src --reload
```

若 PowerShell 顯示「已停用指令碼」，先執行 `Set-ExecutionPolicy -Scope Process Bypass` 再啟用。

Git Bash／macOS／Linux：

```bash
cd repository/smart-ticket-dlc-base
python -m venv .venv
source .venv/bin/activate          # Git Bash on Windows：source .venv/Scripts/activate
python -m pip install -r requirements.txt
pytest -q
uvicorn smart_ticket.main:app --app-dir src --reload
```

寫測試時可用 pytest 提供的 `clock` 測試工具（fixture）調整系統的「今天」（`clock.today = date(...)`），每個測試結束後自動重置。
