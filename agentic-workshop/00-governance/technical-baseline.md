# 技術基線與適用紀錄

> 目標讀者：素材產製 Agent、維護者與評估者。
> 使用時機：建立 G0 或演化任一程式版本之前。
> 前置條件：閱讀[技術標準](../../docs/instructions/01_技術棧與Repository標準指令書.md)與[Manifest](workshop-manifest.md)。
> 版本：P2 文件基線，2026-10-05。
> 可見性：Facilitator／Evaluation／Agent Production；不整份發給學員。

## 1. 固定技術與適用範圍

| 項目 | 基線與責任 |
|---|---|
| 執行環境 | Python 3.13；每版獨立 `venv`／`pip` 環境 |
| Web／Schema | FastAPI、原生 OpenAPI、Pydantic 2；Request／Response 與 Domain 分離 |
| Server／Test | Uvicorn、pytest、FastAPI TestClient 或相容 httpx |
| Persistence | In-Memory Repository 集中管理狀態、測試間 Reset；不加入資料庫 |
| 依賴宣告 | `requirements.txt`，只使用必要的 fastapi／uvicorn／pydantic／pytest／httpx；G0 產製時固定相容版本範圍並實際驗證 |
| Import／設定 | `src/smart_ticket/` layout；`pyproject.toml` 設 pytest test path、pythonpath 與必要 options |
| 文件／版本 | Markdown 與版本識別；G1 案例 History／Tag 與 Bundle 已建立，B0 須延續並驗證隔離，不等同作者 Repo 的文件 Commit |

本次確認文件要求，未安裝依賴、未決定未驗證的套件精確版本，也未宣稱 Python／API／pytest 相容性已實測。核心流程不依賴外部 API、付費服務或雲端帳號；禁止必要前端、微服務、Kubernetes、Message Broker、真實付款與外部資料庫。Docker 只能選用，不能成為活動前置。

## 2. 分層與依賴

| 層 | 責任 | 邊界 |
|---|---|---|
| API／Schemas | HTTP、Pydantic、Status Code、錯誤轉換 | 不算票價、不配置座位、不控制商業狀態 |
| Application | Use Case 編排、Policy／Repository 呼叫、失敗補償邊界 | 不耦合 FastAPI；不建立通用 Transaction Framework |
| Domain | Trip／Passenger／Booking／Order、Enum、Fare／Discount／Seat 規則 | 不依賴 HTTP、FastAPI 或測試框架 |
| Infrastructure | In-Memory Store、Seed、Mock Payment、可替換 Clock／ID | 不呼叫外部服務；結果可控制、資料可重置 |

依賴採 Router→Service→Model／Policy 與 Repository 抽象→In-Memory 實作；由應用初始化組裝。G1 結構應可自然擴充會員、優惠、改退票、通知、座位與Audit。各版完整快照，不跨版 Import，共通環境在各版 README 明確說明。

## 3. API 與錯誤 Contract

G1 必要入口為 `GET /health`、`GET /trips`、`POST /bookings`、`POST /bookings/{booking_id}/pay`、`GET /orders/{order_id}`；`GET /bookings/{booking_id}` 可選。B0／B3 新 API 依其專屬指令，不在 G0 預先實作。

健康檢查回 200 與 `{"status":"ok"}`。Domain／Application 錯誤統一採以下格式（BOOKING_NOT_FOUND 僅為範例，各錯誤使用相應 code／message）： `{"error":{"code":"BOOKING_NOT_FOUND","message":"Booking not found"}}`；找不到資源回404、不回Stack Trace。商業規則可選409或422，但每版固定一致；Pydantic標準422可保留。付款失敗409或502需由G1文件明定且測試，不在P2擅選成正式API變更。

Trip／Passenger／Booking／Order 最小欄位依[技術標準 §9](../../docs/instructions/01_技術棧與Repository標準指令書.md)，名詞依[Glossary](glossary.md)。所有日期與種子固定、抵達晚於出發、付款成功／失敗可注入，測試不依賴真實日期或執行順序。

## 4. 規則編號對齊

本次 P2 依 G0／G1 的詳細規格統一識別，保留既有兩項商業限制，不改變數值或測試門檻：

| 舊技術標準編號與語意 | 統一編號 | 適用 |
|---|---|---|
| `BOOKING-002`：旅客數不得超過剩餘座位 | `BOOKING-003` | 一般訂票容量限制；B3 另追溯 `GROUP-*` 的整團座位要求 |
| 技術標準未列、G0／G1 已定義：一般單筆最多4人 | `BOOKING-002` | G0需求／G1及後續一般訂票；不限制 B3 團體端點5–20人 |

同時對齊技術標準的 Trip／Fare／Payment／Order 基線與 G0／G1 固定ID，詳細映射見[Rule Traceability Baseline](rule-traceability-baseline.md)。O-03 僅識別與文件對齊；不作原總控的例外變更，不推論使用者核准其他政策調整。O-04–O-07仍按各自條件處理。

## 5. 版本驗證與後續入口

各版須獨立安裝／Import／啟動、Health、OpenAPI、pytest、API Smoke與Rule追溯。命令、輸出紀錄與版本例外見[版本驗證要求](version-validation-requirements.md)與[Acceptance Gates](acceptance-gates.md)。G0可明確Feature Skip；G1與B1–B3無Skip／XFail；B0 僅一個 `BUG-B0-001`，保留全部 28 項 G1 正確斷言，實測失敗 node ID 集合須與已核實 Intentional Failure Manifest 完全一致、零非預期失敗，其餘全通過且無 Skip／XFail／未知 Warning。B1 全部 G1 及 B0 新增測試恢復通過。

2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)，O-04 規格衝突解除，B0 實測仍待驗收；G1 已 PASS 滿足前置。Fixture／組裝可適配原 Seed、固定非提前優惠 Clock 與可選 Member，但不改原測試 body／assert、不繞過正式學生 Bug；B0 完整 Seed 與新功能另行驗證。Manifest 以 node ID、Diff／呼叫路徑及修復驗證核實因果。

P2完成只表示技術與規則文件基線可用。下一階段G0仍須真正建立需求、骨架、Fixture、TODO、測試與驗證報告，並實際驗證安裝／啟動，不由本文件代替。

## 完成條件

技術棧、分層、Import、依賴、API、資料邊界與規則編號對齊已文件化，相關來源與驗證要求可追溯。未建立程式、未安裝依賴、未宣稱Runtime驗證通過；後續問題仍保留對應階段的條件。
