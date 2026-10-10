# DDD 延伸課程：Smart Ticket 領域建模

本延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課）約 3 小時，主題是 DDD（Domain-Driven Design，領域驅動設計）。你會先用 domain-memory Plugin（課程提供的命令列工具）為 Smart Ticket 建立 Domain Registry（`domain-memory/` 裡記錄領域知識的 JSON 檔）。Registry 記四種知識：Bounded Context（名詞與規則意思一致的範圍）／通用語言（在同一個 Context 內共用的名詞與定義；不同 Context 可以用同一個詞指不同的東西）／Aggregate（聚合：必須一起保持一致的一組資料，只能從 Aggregate root 這個入口修改）／商業規則。接著再用 DDD 的方式實作三個新需求。

名詞不熟請看 Runbook（課堂操作手冊）的〈詞彙表〉頁。

## 今天的四段

D1–D4 是今天四段的代號；D3 再分 a、b、c 三張需求。

| 段落 | 內容 | 用到的檔案 |
|---|---|---|
| D1 | Agent 找證據、提草稿，你決定來源、詞彙、Context 與規則，Agent 登記為候選（有證據、但還沒審查的紀錄） | Runbook『D1 來源選擇原則』與『D1 候選紀錄格式』兩頁（不在 `worksheets/`）；紀錄由 Agent 寫進 `notes/d1.md` 與 `d1-records.json` |
| D2 | 兩人一組：一人提案、一人審查核准並簽章，把候選升為已審查（reviewed）事實 | `worksheets/d2-role-cards.md`、`worksheets/d2-signing-checklist.md` |
| D3a | 實作需求卡 01：電子發票 | `scenarios/01-e-invoice.md`、`worksheets/d3-decision-card.md` |
| D3b | 實作需求卡 02：點數折抵 | `scenarios/02-points-redemption.md`、`worksheets/d3-decision-card.md` |
| D3c | 實作需求卡 03：團體部分退款 | `scenarios/03-group-partial-refund.md`、`worksheets/d3-decision-card.md` |
| D4 | 把今天累積的 Domain Memory（`domain-memory/` 資料夾的全部內容：Registry、來源清單與稽核紀錄）交接給下一個 Agent 或同事 | `worksheets/d4-handoff-template.md` |

每段的「檢查點」（段內的小關卡）都在 Runbook 對應的頁面。做法都一樣：

1. 複製檢查點裡的提示詞，貼給你的 Coding Agent。Plugin 指令、輔助腳本、Git 與測試指令都寫在提示詞裡，由 Agent 執行並用白話回報；你不需要自己打指令。
2. 需要決定時，Agent 會先列出選項或草稿並停下；你只要回「同意」「選 B」「第 3 項不要」這類短回覆。
3. 紀錄由 Agent 寫進 Repo 的 `notes/` 與 `docs/handoffs/`。Runbook 的表單只記你的決定，以下拉與勾選為主。

D2 的核准要特別注意：兩人共用一台機器，但夥伴另開一個終端機、用自己的 Agent 對話。建立金鑰、核准、簽章 commit 與 push 只在夥伴的對話裡進行，由夥伴讀過變更審查包（Change Package）後下指令。你的 Agent 不 commit、不 push、不碰夥伴的金鑰，也不能代替夥伴核准。D3、D4 的 commit 也由夥伴的對話執行。

## 資料夾內容

| 路徑 | 內容 |
|---|---|
| `repository/smart-ticket-dlc-base/` | 起始程式庫：上線 12 個月的 Smart Ticket 訂票後端 |
| `scenarios/01-e-invoice.md` | 需求卡 01：串接外部電子發票服務 |
| `scenarios/02-points-redemption.md` | 需求卡 02：會員點數折抵 |
| `scenarios/03-group-partial-refund.md` | 需求卡 03：團體訂票部分取消退款 |
| `worksheets/` | 各段紀錄的格式範本，由 Agent 照格式寫進紀錄檔（見上方段落表） |
| `tools/` | 輔助腳本：代打 Plugin 長指令、產生 JSON、檢查環境；由 Agent 依提示詞執行（說明見 `tools/README.md`） |

開場學員包裡還沒有 `worksheets/` 與 `scenarios/`：D1 的兩份格式說明直接放在 Runbook 的 D1 頁面，其餘範本與需求卡隨後面各段的學員包提供（該段解鎖後在 Runbook 下載）。

程式庫的產品規則文件在 `docs/requirements/`，ADR（Architecture Decision Record，架構決策紀錄）在 `docs/adr/`。需求卡中的商業數字與驗收條件是唯一依據，不要自行補規則；卡片末尾的「待團隊決定的問題」由你們決定，Agent 把決定與理由記進紀錄檔。

## 執行程式庫

開場時 Agent 會依 Runbook 的提示詞代你完成下面的安裝與測試；這裡列出步驟，供 Agent 與課後參考。

需要 Python 3.13。本程式庫用 `pip install -r requirements.txt` 安裝相依套件即可，不需要 `pip install -e .`。

Windows PowerShell（主要方式）：

```powershell
cd repository/smart-ticket-dlc-base
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q                           # 開始前應全部通過
uvicorn smart_ticket.main:app --app-dir src --reload
```

若 PowerShell 顯示「已停用指令碼」，先執行 `Set-ExecutionPolicy -Scope Process Bypass` 再啟用。

Git Bash／macOS／Linux：

```bash
cd repository/smart-ticket-dlc-base
py -3.13 -m venv .venv            # macOS／Linux：python3.13 -m venv .venv
source .venv/bin/activate          # Git Bash on Windows：source .venv/Scripts/activate
python -m pip install -r requirements.txt
pytest -q
uvicorn smart_ticket.main:app --app-dir src --reload
```

寫測試時可用 pytest 提供的 `clock` 測試工具（fixture）調整系統的「今天」（`clock.today = date(...)`），每個測試結束後自動重置。
