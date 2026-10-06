# B0 Validation Report

> 讀者：主持人、Evaluation與產製Agent。時機：B0驗收／後續B1前置。前置：G1 PASS、方案A已核准。可見性：Evaluation，禁止發入Participant。
> 日期：2026-10-05。以下為實際執行結果；不是全套一般pytest PASS。

## Version

**B0 - Brownfield Baseline**。來源G1 Tag `361bf00`，B0 Tag `b0-brownfield-baseline`＝`392d920ce4510e5c2dd5df5ae2db25e9ab3b87e6`，獨立案例歷史10個真實Commit。Bundle與52檔快照比對見[來源證據](05-case-history-and-copy-evidence.md)。Time Skip設定G1上線後12個月，不偽稱真實營運資料。

## Environment

Windows、Python **3.13.15**，使用工作區獨立 `.codex-tmp/b0-env/`。正式B0、clean-copy与診斷均是同一B0來源的獨立目錄；G0／G1檔案未改。

## File Count

正式B0 52個來源檔；**25個Production Python＋13個Tests Python＝38實質檔**，排除package init、Markdown與設定，符合35–45。Tests含具fixture/reset內容的conftest。AST核對44個有效test functions：原28＋新增16，不用參數化膨脹數量。

## Dependency Installation

實際 `python -X utf8 -m venv .codex-tmp/b0-env`、該環境 `python -m pip install -r requirements.txt` 成功；建立環境／安裝按已知沙箱限制核准執行。`python -m pip check`：`No broken requirements found.`

直接依賴FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1，主要傳遞依賴Starlette0.46.2／AnyIO4.15.1。Python3.13為已核准技術基線。

## Application Import

在正式B0根目錄以`PYTHONPATH=src`載入App：`3.13.15 Smart Ticket Platform B0`。Health200、OpenAPI11條路徑。另啟Uvicorn綁`127.0.0.1:18764`，HTTP Health實測成功，從啟動helper至回應2.23秒，驗證後停止該process。

## Test Summary

正式B0與隔離診斷均在各自根目錄執行同一pytest套件。helper `.codex-tmp/run_b0_tests.py`使用 `pytest.main(['-q','-p','no:cacheprovider'])`，取消快取以避免沙箱快取權限副作用，**沒有過濾測試或Warning**。記錄全部node ID／outcome／traceback／exit。

| 版本 | 最終實際結果 | pytest exit | 判定 |
|---|---|---|---|
| 正式B0 | **5 failed, 39 passed, 1 warning in 0.44s** | 1 | 五项受控影響与manifest完全一致；零非預期 |
| 隔離只修學生率 | **44 passed, 1 warning in 0.32s** | 0 | 全部28原G1与16新增恢復 |

原始首次結果正式1.57秒、診斷0.68秒；補足新增測試的付款／改票通知与改票Audit斷言後，以上為最終重驗。全部低於8秒，無Skip／XFail。唯一已知Warning來自Starlette TestClient的 `anyio.abc.BlockingPortal`棄用別名；已記錄，不影響執行，不過濾，無未知Warning。

## Intentional Failure Verification

唯一 `BUG-B0-001`＝FarePolicy單一學生率常數85%，公開規則仍75%。學生525變595，混合1225變1295；五個失敗是同一Bug跨Policy／Application／API影響，不是五個Bug。正式Source不含提示Bug答案的註解。

## Intentional Failure Manifest and Set Equality

[Manifest](06-intentional-failure-manifest.md)與[JSON node清單](06-intentional-failure-manifest.json)列完整五項node ID、Rule／AC、expected／actual、Diff／呼叫路徑因果。以實測 failed集合與manifest雙向相等核對，不只比較失敗數量；結果 **PASS**。機器驗證摘要与52檔SHA256見[validation-evidence.json](validation-evidence.json)。

## Isolated Diagnostic Repair Verification

`diagnostic-repair/smart-ticket-b0-student-rate-check/`為Evaluation限定副本。與正式B0雙向52檔清單一致，只差 `src/smart_ticket/domain/fare_policy.py`一行 `STUDENT_FARE_RATE = 85`→`75`；其他Code／Test／Document完全一致，44全通過。正式B0与clean-copy仍85且五項受控失敗。此副本不供Participant、不進案例History、不代表B1正式版本已製作。

## API Smoke Tests

在正式B0使用TestClient實測：Health／七班可售Trip／企業M002→成人訂票665与唯一Seat→付款Order665→改T005總712、差47、原T001回20座／T005剩5→退票REFUNDED／T005回6座→三通知与四Audit事件查詢。Order仍保留原付款665。

另將Clock設2030-01-01，距出發14天，非會員成人提前價595；Reset恢復固定Seed与全部ledger。輸出 `IMPORT HEALTH OPENAPI MEMBER BOOK PAY CHANGE REFUND NOTIFY AUDIT ADVANCE RESET: PASS`。新端點missing404、格式422与業務409亦由Integration測試覆蓋。

## G1 Regression

原Health／Fare／Service／Feature四檔文字比對一致，全部28測試body／assert未改；仅conftest限定原T001–T004＋非提前Clock背景。學生仍走正式B0Policy。正式結果23passed／5受控failed，隔離修復28passed。完整B0 Seed／優惠／會員另由新增16案例驗證，沒有使用fixture避開學生Bug。

## Rule Traceability

原16＋新增20＝**36項規則**，Requirement→Code→Test→Document→State見[追溯表](04-b0-rule-traceability.md)，新增資料與流程見[Delta](02-g1-to-b0-delta.md)與[Module Map](03-b0-module-map.md)。SEAT-002是不保證相鄰的能力邊界，不要求刻意安排不相鄰；未加入B2最有利或B3團體。

## Controlled Technical Debt

精確三項：DEBT-001優惠firstmatch分支、DEBT-002通知同步耦合、DEBT-003改票指南略落後。完整位置／歷史理由／Learning Purpose／Must Fix Now見[Controlled Debt Map](../facilitator/03-controlled-debt-map.md)。

## Controlled Documentation Gaps

精確兩項：`docs/change-booking-guide.md`未記差額、`docs/discount-overview.md`未清楚定義優先序。公開主規則、API與啟動指令正確；其他文件不加入故意錯誤。學員只被提醒交叉驗證，不預告落差位置。

## Participant Leakage Check

Participant Markdown／Python掃描未含Evaluation解答連結、診斷路徑、BUG／DEBT地圖或學生率修復常數；沒有內嵌`.git`。Time Skip交接不揭根因位置／失敗數；三級提示只在Facilitator。Bundle仅供Evaluation，10個可達Commit截至G0／G1／B0，無未來解答或診斷Commit。最终學員打包仍須允許清單，目錄分層不等於權限。

原要求 `reference-baseline/smart-ticket-b0-clean-copy/`已實際建立；52檔清單与內容／SHA256完全相同，仍含85%Bug。O-06來源與防漂移方案已落實。

## 難度與時間校正

本機啟動2.23秒、測試0.44秒，程式38實質檔，資料／API／ADR与三級提示足以提供調查入口；不需外部網路服务才能運行。依規模與單一計價來源評估3分鐘啟動、5分鐘初析／候選、8分鐘B1具有可行性。**未完成普通工程師實際演練**，不把Agent產製與自動測試時間當作學員時間；真實3／5／8分鐘與90分鐘校正留待Runbook／最終演練驗收。

## Final Decision

**PASS AS BROWNFIELD BASELINE**。符合已核准方案A：一個受控Bug、完整實測manifest集合一致、零非預期失敗、隔離只修該Bug後全通過、其餘素材Gate與來源／副本核對完成。正式B0 pytest exit為1，不能稱一般全套通過；此決策不宣稱B1–B3或最終活動演練／交付包完成。
