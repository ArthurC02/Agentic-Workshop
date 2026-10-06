# B3 Validation Report

> 讀者：Evaluation、主持人與素材維護者。時機：P8驗收、進入P9前。
> 前置：已驗收B2、[B3影響分析](07-b3-expected-impact-analysis.md)與[AC Map](10-b3-acceptance-test-map.md)。可見性：Evaluation限定。

2026-10-05，正式[B3快照](reference-solutions/b3-group-booking/)實測通過。B1–B3產製指令範圍的Final Decision為 **PASS FOR WORKSHOP USE**；P9治理套件、正式交付包與實際13／90分鐘演練仍未完成。

## 環境、命令與實際結果

獨立`.codex-tmp/b3-env`，Python3.13.15；依本版requirements.txt成功安裝FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1，間接依賴Starlette0.46.2／AnyIO4.15.1。

從B3根目錄設定`PYTHONPATH=src`後，獨立Python執行完整pytest並收集逐案例證據：**75 passed、0 failed、0 skipped、0 XFail，exit0，0.58秒**。原55項B2測試檔逐檔字節保留，新增20項團體測試。首次74項通過後，審查補充「第一車廂滿仍可搜尋第二車廂」測試，最終75項全部通過。

唯一Warning是Starlette引用`anyio.abc.BlockingPortal`的已知DeprecationWarning，與B1／B2相同；未過濾或隱藏。完整node IDs、結果、來源雜湊與規則集合見[JSON證據](19-b3-validation-evidence.json)。

| 實際檢查 | 結果 |
|---|---|
| App Import／TestClient Health／OpenAPI | App版本B3；Health200且status=ok；13個API路徑，新增兩個group端點 |
| 真正啟動 | Uvicorn子程序正常啟動，HTTP Health通過，2.17秒；完成後停止程序 |
| 人數邊界 | 4／21拒絕、5／20成功；T001容量20支持20人，T006容量18拒絕20人 |
| 座位與Atomicity | 同車廂連續；可跨排、不可跨車廂；零散座位整筆拒絕；第一廂滿仍搜尋第二廂；建立失敗Booking／座位／Order及其他Ledger不變 |
| 團體優惠Smoke | 注入提前14天、企業會員，1學生＋4成人；75／85／85／85／85%，總額2905，逐旅客明細正確 |
| 成功付款Smoke | 整筆PAID，唯一Order2905，重複付款409；已付款團體可退票並全釋放 |
| 失敗付款Smoke | Mock Gateway FAILED後HTTP409；Booking CANCELLED、seat_ids及assigned_seats清空、容量恢復20、無Order／座位保留；Audit2筆、取消Notification1筆 |
| 入口及重試 | 一般付款入口不能繞過團體補償；group付款入口拒絕一般訂票；取消團體不得重試或重複釋放 |
| 既有能力 | 原G1、B0新增、B1修復及B2政策測試全通過；一般付款失敗仍pending並保留座位；一般改退票與記錄能力保留 |
| Reset | Booking／Order／Seat／Refund／Audit／Notification清除，Clock／Gateway及種子容量恢復 |

## 範圍與文件審查

57個唯一Rule ID等於治理Registry，19AC有程式、真實測試與文件定位。API公開booking_type與assigned_seats幾何欄位，保留原passengers與B2 applied_discounts；政策不放在Router。

連續位置以每車廂20位置、每排4座映射原Seat IDs；未將既有種子容量強改成40。測試才注入42位置驗證第二車廂與跨廂拒絕，Reset還原。一般訂票不保證相鄰；團體必須完整連續區段。

團體改票未列入新增功能，明確409拒絕；既有一般改票保持。已付款團體沿用既有退票能力，釋放全部座位。金流仍模擬，沒有部分成功、分次付款、候補、跨Trip、外部資料庫或通用Transaction Framework。

README、57業務規則、API、架構／ADR與歷史已同步；B3優惠範例更正繼承文件中的FULL_FARE文字為實際enum ADULT，B2快照保持凍結。改票指南同步Fare Difference記錄，但不執行補款／退款；保留同步Notification設計。

## 隔離、Timebox與Final Decision

Task卡只列業務、人員Gate及最低欄位需求，不含座位演算法、完整Response或解答路徑。Facilitator提供63–76分鐘提示／停止／Recovery與Level1–3；人員只Challenge／Review／Approve／Reject，Agent主導交付。B1–B3標準解答及Bundle保留Evaluation層。

分層與任務卡掃描支持本階段素材隔離；最終包尚未產生，不聲稱已完成交付包檢查。自動測試時間不等於真實學員13分鐘或90分鐘演練。三個Human Gates是學員操作要求，沒有虛構實際學員核准紀錄。

完成條件：B3完整AC與Regression、獨立環境、API、文件及案例歷史一致；B1–B3已分版驗收。Final Decision：**PASS FOR WORKSHOP USE**，適用本產製指令範圍。
