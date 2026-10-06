# G1 Validation Report

> 讀者：主持人、驗收人員與產製 Agent。時機：G1 驗收／B0 前置檢核。前置：G0 已驗證，使用 G1 獨立環境。可見性：Evaluation，禁止發入 Participant。

版本：**G1 - Greenfield Reference MVP**。驗證日期：2026-10-05。目錄：`reference-solution/greenfield-reference-mvp/`。

## 驗證環境

Windows、Python **3.13.15**，全新 `.codex-tmp/g1-env/`，獨立於 G0 環境。下列測試與 Smoke 在 G1 根目錄執行。Python 3.13 為使用者已核准變更。

## Dependency Installation

實際執行 `python -X utf8 -m venv .codex-tmp/g1-env`，及該環境 `python -m pip install -r requirements.txt`，成功。沙箱初次 ensurepip／套件索引與暫存權限失敗，核准後重試成功。

直接依賴：FastAPI 0.115.12、Uvicorn 0.34.2、Pydantic 2.11.4、pytest 8.3.5、httpx 0.28.1；主要傳遞依賴 Starlette 0.46.2、AnyIO 4.15.1。`python -m pip check`：`No broken requirements found.`

## Application Import

設定 `PYTHONPATH=src`，實際載入 `smart_ticket.main.app`：`Smart Ticket Platform`／`G1`。Health 200，OpenAPI 含全部五個 endpoint。驗證 helper：工作區忽略目錄 `.codex-tmp/validate_g1.py`，不是交付必要依賴。

## Test Result

在 G1 執行其獨立環境 `python -X utf8 -m pytest -q`：

```text
28 passed, 1 warning in 0.21s
```

13 Unit（3 Fare、10 Service）、14 Integration、1 Health。包含人數 0／4／5、容量不足／售罄、失敗無部分座位消耗、75% 學生及混合整數金額、付款失敗與可重試、重複付款、404／409／422與端到端流程。

## API Smoke Test

TestClient 實際完成：Health 200 → Trip 查詢三班 → T001 學生訂票 201／525 → 付款 200／SUCCESS → Order 查詢 200 與付款回應一致。OpenAPI 五 endpoint 通過。Reset 後 T001 回復20座、Booking／Order清空。輸出：`IMPORT HEALTH OPENAPI E2E RESET: PASS`。

## Rule Traceability

全部16項 Greenfield Rule ID 與15項 AC 有 Requirement／Code／Test／Document 對應，見 [Acceptance Test Map](06-acceptance-test-map.md)。來源語意、Seed ID／票價／初始容量未改；新能力、完成TODO與移除Skip见 [Delta](05-g0-to-g1-delta.md)。

## Skip / XFail / Warning

無 Skip、XFail、未知測試失敗。唯一已知相容 Warning：Starlette TestClient 使用 `anyio.abc.BlockingPortal` 已棄用別名，AnyIO 建議改用 `anyio.from_thread.BlockingPortal`。來自第三方依賴，不影響本次所有測試；未過濾或隱藏。

初次沙箱執行另產生 pytest cache 權限警告；正式核准重跑後不存在。首次缺失 Unit 同步已修正，再跑完整28項。相容 Warning 為 G1 規格允許且已記錄的非阻擋項，不降低測試門檻。

## Known Limitations

In-Memory／單程序教學案例，重啟即重置；非生產持久化或真實付款。鎖只保障本程序內座位與付款提交，不提供跨程序交易。資料讀取不是交易快照；未宣稱生產級隔離。以上是固定案例邊界，不是未完成 MVP 功能。尚未進行22分鐘真實學員演練與最終打包隔離驗證。

## G0 Consistency Check

作者 Repo `git diff -- agentic-workshop/01-greenfield/participant` 無變更。G0保留受控TODO／Skip，不覆蓋標準答案。Participant Markdown 無 Reference Solution 連結，無內嵌案例Git歷史；檢核輸出 `PARTICIPANT LINKS/HISTORY: PASS`。G1與案例Bundle只放 Evaluation。資料夾分層不構成權限，最終交付仍須允許清單打包。

## Brownfield Readiness Check

FarePolicy、Application Service、輕量 Repository Protocol／Store、可控Gateway與Booking→Order關係可供演化；未加入會員、優惠、改退票、通知、具名座位、Audit或團體功能。

真實案例歷史、G0／G1 Tag與可還原Bundle見 [Case History](reference-solution/greenfield-reference-mvp/docs/case-history.md)。後續B0必須從案例G1 Tag延續，而非作者Repo全部教材歷史。

**O-04仍阻擋B0 Bug注入**：同一政策改75%→85%會破壞五個既有G1測試（Fare學生／混合、Service混合、API學生／混合），金額525→595、1225→1295。不能同時聲稱全部G1 Regression通過與精確一項失敗。須先建立合理且可驗證的演化方案，或取得規格調整核准；不刪除／弱化／Skip測試。

## Final Decision

**PASS** — G1 全部 MVP 功能、規則、測試、Smoke、追溯與當前目錄隔離通過。已知第三方Warning符合本版允許條件。此結論不宣稱B0規格衝突已解除，亦不代表整套工作坊已完成演練與打包。

完成條件：保留本次實測結果、對照與限制；G1可作穩定演化起點，B0仍須獨立完成其前置衝突處理及驗收。
