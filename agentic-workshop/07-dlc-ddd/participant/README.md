# DDD 延伸課程：Smart Ticket 領域建模

本延伸課程約 3 小時。你會先用 Domain-Memory plugin 為 Smart Ticket 建立 Domain Registry（Bounded Context、通用語言、Aggregate、商業規則），再用 DDD 實作三個新需求。

## 資料夾內容

| 路徑 | 內容 |
|---|---|
| `repository/smart-ticket-dlc-base/` | 起始程式庫：上線 12 個月的 Smart Ticket 訂票後端 |
| `scenarios/01-e-invoice.md` | 需求卡 01：接入外部電子發票服務 |
| `scenarios/02-points-redemption.md` | 需求卡 02：會員點數折抵 |
| `scenarios/03-group-partial-refund.md` | 需求卡 03：團體訂票部分取消退款 |

程式庫的產品規則文件在 `docs/requirements/`，架構決策在 `docs/adr/`。需求卡中的商業數字與驗收條件是唯一依據，不要自行補規則；卡片末尾的「待團隊決定的問題」由你和團隊決定，並記錄理由。

## 執行程式庫

需要 Python 3.13。本程式庫用 `pip install -r requirements.txt` 安裝，**不**使用 `pip install -e .`。

```bash
cd repository/smart-ticket-dlc-base
python -m venv .venv
source .venv/bin/activate          # Windows：.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q                           # 開始前應全部通過
uvicorn smart_ticket.main:app --app-dir src --reload
```

測試中可用 `clock` fixture 調整系統的「今天」（`clock.today = date(...)`），每個測試結束後自動重置。
