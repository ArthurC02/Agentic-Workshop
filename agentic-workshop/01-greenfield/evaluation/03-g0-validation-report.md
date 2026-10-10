# G0 Validation Report

> 目標讀者：主持人、評估者與產製 Agent。
> 使用時機：G0交付、環境準備及G1產製前。
> 前置條件：固定G0檔案與獨立驗證環境。
> 可見性：Evaluation，不提供Participant。

## 環境與依賴

2026-10-05於Windows實際驗證。使用者明確允許Python3.13／3.14，統一採Python **3.13.15**；技術標準已標記「已核准變更」。獨立venv位於Repo忽略的`.codex-tmp/g0-env`，非學員包內容。

實際執行venv建立與`python -m pip install -r requirements.txt`成功；固定FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1。`pip check`回報`No broken requirements found`。直接依賴固定，傳遞依賴由本次安裝解析，尚非完整lockfile。

## 啟動與Smoke

實際Import成功：App title為`Smart Ticket Platform`。TestClient：Health回200與`{"status":"ok"}`、OpenAPI成功且含業務API路徑。Uvicorn實際啟動於127.0.0.1:18763，HTTP Health成功，檢查後停止程序。

Seed T001–T004票價／座位與固定路線正確，Arrival晚於Departure。變更座位後Reset還原；Mock付款由失敗狀態Reset回預設成功。未實作查詢／訂單入口回501與統一error格式，沒有偽裝成完整MVP。

## pytest實際結果

在starter-repository根目錄執行venv Python的`-m pytest -q`：

```text
1 passed, 8 skipped, 1 warning in 0.07s
```

8項Skip：班次查詢、訂票保留座位、一般人數上限、剩餘容量、付款與重複付款、Order查詢、成人計價、學生計價。每項原因引用Rule ID；無Fail／XFail／未知錯誤。完成MVP必須移除相應Skip並補測試。

已知Warning：Starlette0.46.2使用anyio.abc.BlockingPortal別名，anyio4.15.1標記deprecated；不影響本次Health、OpenAPI或啟動。未過濾Warning。首次沙箱執行另有pytest快取權限Warning，允許寫入後重跑已消除，以上為重跑實際結果。2026-10-09 起 requirements 釘選 AnyIO 4.9.0，這個 Warning 已不再出現。

## 規格與隔離

Starter共26個來源檔（包含.gitignore，不計快取／venv），11個主要`TODO(GREENFIELD, ...)`，符合10–16範圍。學員需求含16項Rule、15項AC；Evaluation矩陣獨立保存。Domain與Service使用型別方法骨架；計價、訂票、付款與Order核心仍未實作。

Participant、Facilitator、Evaluation分目錄，學員素材不連向標準答案或評估目錄、不預告受控Bug。未建立G1或後續功能。26檔採適度合併schemas／router／enum，不靠空init虛增數量。

## 限制與完成條件

22分鐘活動採2＋2＋13＋5配置，11主要實作點作範圍校正；尚未進行真實學員時間演練，不宣稱已測得完成時間。本次完成G0環境、框架、初始測試與文件驗證；不代表MVP業務功能已完成。已知相容Warning如上留存（2026-10-09 釘選 AnyIO 4.9.0 後已消除），學員仍須補上實作、完整單元／整合測試及規則／API文件。
