# G1 → B0 Delta

> 讀者：主持人、驗收與後續產製Agent。時機：B0來源核對／後續任務規劃。前置：G1 PASS與方案A已核准。可見性：Evaluation，禁止發給學員。

## 新增與保留能力

G1四個核心API與Health、原T001–T004、75%公開規則及全部28項原測試保留。B0新增會員、提前優惠、改票、退票、通知、座位與Audit，仍使用In-Memory與Mock付款，不加入登入、外部服務、團體或最有利優惠政策。

| 區域 | 新增／變更檔 | 主要變更 |
|---|---|---|
| Domain | members.py、discounts.py、records.py、models.py | MemberType／Member、DiscountType／Result、SeatAssignment／RefundRecord／NotificationRecord／AuditEntry；Booking member／seats／difference與REFUNDED |
| Application | 六新增Service及Booking／Payment | Member、ChangeBooking、Refund、Seat、Notification、Audit；計價、座位与成功事件串接 |
| Infrastructure | clock.py、store.py、seed_data.py | 可注入固定Clock、8Trip／3Member、全部ledger与完整Reset |
| API／Schema | routes.py、dependencies.py、contracts.py | 原API相容、會員可選，新增會員／改退票／通知／Audit與Booking查詢六API |
| Tests | conftest.py、新增8 integration檔 | 原28 body／assert不改；G1限定Seed背景與完整B0背景分別驗證，新增16項，合計44 |
| Documents | README、架構／規則／API／歷史、兩guide／overview与3ADR | 公開36項規則、API、合理決策、兩受控文件落差 |
| Workshop | Time Skip5文件、Brownfield學員4／主持3文件 | 12個月快轉、停止個人Repo、統一B0、獨立分析與Shared Context |

## 商業規則與付款快照

新增20項規則：MEMBER-001–003、FARE-005–006、CHANGE-001–004、REFUND-001–004、NOTIFY-001–003、SEAT-001–002、AUDIT-001–002；連同原16項共36項。對照見[追溯表](04-b0-rule-traceability.md)。

現況DiscountPolicy依CORPORATE→ADVANCE→STUDENT→ADULT第一個符合項目選擇，未取最有利；企業成人95%、提前至少14天85%。學生公開規則仍75%。金額整數。改票重新計價並記錄new-old差額、不做差額金流；Order保留建立時原付款金額，Refund只是本機紀錄。

## 唯一Bug、三項債與兩項落差

`BUG-B0-001`只在FarePolicy學生率常數設定85%，Domain／Application／API共用同一來源。不是合法政策變更。正式B0五項學生相關失敗与manifest相等；只修該常數至75%的隔離副本全部44通過。詳見[Manifest](06-intentional-failure-manifest.md)與[驗證報告](01-b0-validation-report.md)。

- DEBT-001：discount順序分支，是政策演化痕跡；不強制全面重寫。
- DEBT-002：Payment／Change／Refund同步呼叫Notification；本機規模可接受，不導入Queue。
- DEBT-003：change-booking-guide未更新差額記錄；主要規則/API正確。

僅兩項文件落差：change-booking-guide未載Fare Difference、discount-overview未明確列優惠優先序。主持完整地圖在facilitator，學員不預告位置。Bug是功能問題，不與債或文件落差混計。

## G1 Regression與來源

原四測試檔（Health、Fare、Service、Feature）的body／assert保持一致；唯一測試背景適配在conftest，使用原四Trip及固定距出發1天Clock，不改學生計價分支。新增16案例使用完整8Trip，驗證13／14／15天優惠、會員、改退票與記錄。

原G1 Regression結果為23通過／5受控失敗；隔離診斷為28全通過。B0全套39通過／5受控失敗；診斷44全通過。無Skip／XFail，已知第三方Warning不過濾。新增通知／Audit斷言已納入正式重驗，最終結果以報告為準。

真實G1祖先、B0 Tag／Bundle、快照及clean-copy比對見[來源證據](05-case-history-and-copy-evidence.md)。診斷副本不進案例Git歷史或學員包，沒有把本階段診斷稱為B1正式版本。

## 後續演化邊界

B1只修學生率並全套恢復；B2才決定最有利單一优惠；B3才加入5–20團體、連續完整座位與失敗補償。本版未加入這些功能。只以當前副本與驗證作基線，後續版本仍須各自來源、Delta及實測。

完成條件：G1保留與B0變更可追溯，Bug／債／落差明確，驗證與來源證據完整且不洩漏學員答案。
