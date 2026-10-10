# B1 Validation Report

> 讀者：Evaluation、主持人與產製Agent。時機：B1驗收／B2前置。前置：B0為PASS AS BROWNFIELD BASELINE。可見性：Evaluation，不供Participant。
> 日期：2026-10-05。版本：**B1 - Student Fare Fixed**。

## 來源與最小修復

正式版本位於 `reference-solutions/b1-student-fare-fixed/`，從正式B0複製，不把P5診斷副本改名當成完成。案例歷史延續B0 `392d920`，B1 Tag `b1-student-fare-fixed`＝`a1c1d45a26875feb2635f211059db5e8980035f7`。Bundle驗證、Clone、B0祖先與52檔快照比對通過，11個真實案例Commit，無B2／B3。詳見[來源／Delta](14-b1-case-history-and-delta.md)。

與B0來源清單相同，僅五檔不同：FarePolicy學生率85→75一行商業邏輯、main App版本B1、pyproject版本0.2.1、README與version-history版本識別／狀態。全部13個Test Python檔逐位元相同、DiscountPolicy與其餘Source不變；主要Business Rules本來正確，無無意義改寫。兩項B0受控文件落差保留，不在此階段修成額外工作。

## Environment／Dependency Installation

Windows／Python **3.13.15**。獨立工作區 `.codex-tmp/b1-env/`，實際建立venv並從B1 `requirements.txt`安裝成功；按已知ensurepip／網路沙箱限制核准執行。`python -m pip check`：`No broken requirements found.`

直接依賴FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1；Starlette0.46.2／AnyIO4.15.1。未改依賴或技術基線。

## Application Import／Health／OpenAPI

在B1根目錄設定`PYTHONPATH=src`，載入App輸出：`3.13.15 Smart Ticket Platform B1`。Health200、OpenAPI11條原有路徑通過，未改API Contract。

## Test Result與Regression

在正式B1根目錄使用其專用Python執行pytest collector（工作區忽略helper `.codex-tmp/run_b0_tests.py`；名稱沿用P5，實際載入B1 Source）。呼叫`pytest.main(['-q','-p','no:cacheprovider'])`取消快取寫入、無測試或Warning過濾：

```text
44 passed, 1 warning in 1.00s
exit code 0
```

原28項G1與16項B0新增測試均通過、無Skip／XFail、零失敗。完整node結果核對B0 Manifest五項均為passed，不只比較總數。唯一已知Warning為Starlette TestClient使用AnyIO BlockingPortal棄用別名，保留紀錄、不影響執行，無未知Warning。未重寫／弱化／刪除測試。

## API Smoke與優惠範圍

正式B1 TestClient實測T001單學生525、成人＋學生1225、成功付款Order1225與查詢一致。企業學生仍665，符合原企業firstmatch；距出發14天的非會員學生仍595，符合原advancefirstmatch，不提前加入B2最有利政策。

另驗證B0完整流程：會員→成人訂票665→付款→改T005712／差額47→退票REFUNDED→通知三事件／Audit四事件→原Order665快照保留。可售Trip、Clock提前價與全部Reset通過。輸出：`B1 STUDENT 525 MIXED 1225 ORDER AND UNCHANGED FIRST-MATCH: PASS`及完整API流程PASS。

## Acceptance Criteria／影響分析

AC-B1-001–007全部有實測或檔案比對證據，見[AC Map](08-b1-acceptance-test-map.md)、[Impact Analysis](05-b1-expected-impact-analysis.md)。原五失敗的Policy→Application→API路徑全部恢復，成人／優惠／改退票／座位／紀錄保持原能力。機器摘要、五恢復node及52檔SHA256見[13-b1-validation-evidence.json](13-b1-validation-evidence.json)。

## 原始B0與隔離

使用P5保存的52檔SHA256逐項比對，正式B0內容未變；B0仍85%，clean-copy與P5診斷副本未修改。B1解答／Bundle只在Evaluation。Participant只新增分批任務卡，不含實作檔位置、完整影響分析或答案連結；三級提示與時程／停止／行為觀察在Facilitator。最終打包仍須允許清單。

## 時間與限制

B1活動44–52分鐘，共8分鐘；Shared Context後才揭露。主持文件具核准、最小Diff Review、三級提示、停工及Recovery界線。測試1秒支持短回饋，但尚未做真實普通工程師8分鐘演練，不能將產製或自動執行時間當作學員完成時間。

In-Memory、Mock付款、單程序鎖與固定Clock邊界保留；B0兩項受控文件落差不變，後續任務不能把它們當成本次新Bug。B2／B3未產製或驗證，沒有宣稱B1–B3整套 `PASS FOR WORKSHOP USE`。

## Final Decision

**B1 個別 Gate：PASS**。學生率最小修復、44全通過／五失敗恢復、優惠順序不變、API Smoke、完整追溯、獨立環境、歷史與隔離均通過。B2可從本正式B1基線啟動，須另授權新目標；B1–B3整體Final Decision留待後續完整驗收。
