# Smart Ticket G0 Starter Repository

> 讀者：Greenfield 參與者與 Coding Agent。
> 使用時機：22 分鐘個人 MVP 任務。
> 前置條件：Python 3.13；先閱讀上一層需求與驗收條件。

此版本提供框架、固定資料與 Health；四個業務 API 回應 501，核心 Use Case 尚未實作。人員主導需求與拆解，Agent 協助完成 MVP。

在本目錄操作，建議使用 Python 3.13。先建立並啟用虛擬環境（venv）：

- macOS／Linux：`python3.13 -m venv .venv`，再 `source .venv/bin/activate`。
- Windows：建議用 `py -3.13 -m venv .venv` 建立。Git Bash 用 `source .venv/Scripts/activate` 啟用；PowerShell 用 `.venv\Scripts\Activate.ps1` 啟用。

啟用後執行：

```bash
python --version
python -m pip install -r requirements.txt
python -m uvicorn smart_ticket.main:app --app-dir src --reload
python -m pytest -q
```

也可以跳過啟用，直接呼叫虛擬環境裡的 Python（PowerShell 執行原則擋下啟用時也這樣做）：Windows 用 `.venv\Scripts\python.exe -m pytest -q`（Git Bash 寫 `.venv/Scripts/python.exe`），macOS／Linux 用 `.venv/bin/python -m pytest -q`；安裝與啟動指令同理，把開頭的 `python` 換掉即可。

初始預期為 `1 passed, 8 skipped`，實際結果以執行輸出為準。功能 Skip 原因對應 Rule ID；完成功能後移除對應 Skip，補足 Unit／Integration 邊界測試。搜尋 `TODO(GREENFIELD` 找出 11 個主要實作點；初始 Skip 不代表完成 MVP。

文件入口：[架構](docs/architecture.md)、[規則待填表](docs/business-rules.md)、[API 範例待填表](docs/api-examples.md)。框架錯誤格式為 `{"error":{"code":"...","message":"..."}}`，Request Validation 可保留 FastAPI 422。

## 完成條件

完成查詢、訂票、付款與訂單流程，移除功能 Skip，補足測試，更新規則與 API 範例，提供實際測試結果與交付摘要。