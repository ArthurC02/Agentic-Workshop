# B0 Regression Gate 修正提案

> 讀者：工作坊負責人、教材維護者與產製 Agent。時機：Time Skip／B0 產製前核准。前置：G1 PASS、O-04影響盤點。可見性：內部規劃，不提供學員。
> 日期：2026-10-05。**狀態：方案A已核准並套用。** 核准者：使用者；核准原文：「套用」。本次已同步B0／B1指令書、治理、Agent及規劃；B0程式與實際交付驗收仍待產製。

## 決策需求

已採用方案A：保留唯一主任務 Bug `BUG-B0-001`（學生票錯誤85%，正確75%），保留全部28項G1 Regression及其正確斷言，將B0驗收改為：**所有失敗須屬於已列明的Bug影響清單，零非預期失敗；B1修復後全部G1及B0測試通過。**

原B0規格同時要求學生85%、精確一項測試失敗、所有G1 Regression通過。G1已有多層學生與混合票價驗收，這三項不能按目前共用計價路徑同時成立。不能藉刪除／弱化／Skip／XFail／錯誤期望值湊一項失敗，也不應為保住測試數量另保留一條學員不使用的正確計價流程。

## 實際驗證證據

環境為G1獨立Python3.13.15 venv。2026-10-05在G1根目錄執行忽略目錄helper `.codex-tmp/probe_b0_regression.py`；helper以記憶體monkeypatch將 `FarePolicy.calculate` 學生分支75%換85%，其餘邏輯不變，再執行完整pytest（`-q -p no:cacheprovider`）。結束時恢復方法，未寫入G1 source、tests或案例Bundle。

```text
5 failed, 23 passed, 1 warning in 0.28s
FAILED=5 PASSED=23 EXIT=1
```

helper自身exit0只表示預期的5項失敗實驗吻合；pytest exit1表示套件確實失敗，不能記為28項通過。唯一Warning為既有Starlette／AnyIO相容警告。本實驗只證明G1原計價路徑的Bug影響，**不是B0已建立或已驗收的證據**。

實驗後另開新Python程序執行原G1 `python -m pytest -q -p no:cacheprovider`：`28 passed, 1 warning in 0.11s`，確認原正確行為仍可重現。

## 五項已證實的影響矩陣

路徑相對G1 `greenfield-reference-mvp/`。

| Test File | Test Name | Rule／AC | 正確斷言 | 注入85%後實際值 |
|---|---|---|---|---|
| tests/unit/test_fare_policy.py | test_student_fare_is_seventy_five_percent | FARE-002／AC-G-004 | 525 | 595 |
| tests/unit/test_fare_policy.py | test_mixed_passenger_fares_sum_as_integers | FARE-003／004／AC-G-005 | 1225 | 1295 |
| tests/unit/test_services.py | test_successful_mixed_booking_reserves_seats_and_starts_pending | FARE-003、BOOKING-004／005／AC-G-005／009 | 1225 | 1295 |
| tests/integration/test_features.py | test_student_booking | FARE-002／AC-G-004 | 525 | 595 |
| tests/integration/test_features.py | test_mixed_booking_reserves_seats | FARE-003／004、BOOKING-004／005／AC-G-005／009 | 1225 | 1295 |

同一Bug造成五項失敗，不是五個Bug。B0新增學生相關測試若也受影響，須在交付前以實際結果補入明確node ID清單；不把任意學生相關失敗自動接受為預期。

## 可選方案

| 方案 | 處理 | 影響與建議 |
|---|---|---|
| A：按Bug與完整影響清單驗收 | 一個Bug、多項明列失敗、零非預期；B1全恢復 | **已核准採用**；保留跨層Regression與真實影響分析 |
| B：維持精確一項失敗 | 重新設計G1／B0測試與計價分支以限制單一失敗 | 容易弱化覆蓋或引入兩套計價，不建議；未獲授權重寫已驗收G1 |
| C：取消刻意Bug | B0全部通過，另發故障練習版本 | 改動工作坊故事線與B1起點較大，不建議 |

## 方案A的已核准替換文字

**B0測試／驗收門檻：**

> 保留全部G1 Regression Tests與其正確商業斷言。B0僅注入BUG-B0-001；完整套件中所有失敗必須逐項列入Intentional Failure Manifest，並以實際Diff、呼叫路徑及修復驗證證明皆由此Bug造成。其餘測試全部通過，無Skip／XFail／未知Warning；不得有非預期失敗。失敗總數以manifest為準，不要求精確一項。G1 Regression報告逐項揭露學生票相關失敗，其餘全部通過。

**B0 PASS判定：**

> Final Decision仍為PASS AS BROWNFIELD BASELINE或FAIL。只有Bug數為一、實測失敗node ID集合與已核實manifest完全一致、零非預期失敗且其餘Gate符合，才能PASS。不得以pytest非零exit直接當作一般通過；Evaluation須另判定預期失敗集合。

**B1恢復條件：**

> 修復85%至75%後，全部28項原G1 Regression及全部B0新增測試均通過，manifest所有失敗均已恢復；無Skip／XFail。28是G1 Regression數，不是B1全套測試數。

**學員交接文字：**

> 目前有若干測試失敗，需要小組分析是否具有共同原因；先完成個人Agent分析與Shared Context，再開始修改。

學員文字不揭露Bug根因、位置、已知失敗數或完整影響矩陣。主持人仍按8分鐘B1活動安排，實際可行性留待演練。

## Regression上下文適配邊界

除Bug外，B0新增Seed／優惠／座位會影響原測試背景，需在產製時清楚分離上下文：

- 原28項G1測試body／assert保留；其fixture使用T001–T004原Seed、非提前優惠固定Clock（例如出發2030-01-15前1天）、member預設None。學生仍走正式B0計價，不得繞過Bug或注入正確學生分支。
- 另以完整B0 Seed（至少8班）、會員、13／14／15天優惠邊界驗證B0新增能力，不得讓正式B0只有4班或停用提前優惠。原Trip精確集合斷言不改成subset。
- B0 Seat ledger須與可售容量相容；原測試直接設容量1時，仍應以容量限制拒絕2人，不能讓空座位清單繞過容量。Reset清除Booking／Order／Seat／Refund／Notification／Audit及可控Clock／Gateway狀態。
- API與原Service呼叫相容，member可選，原Passenger欄位與enum保持。404／409／422策略與付款失敗pending／保留座位行為保留；B3團體補償不提前加入。

可修改fixture與組裝適配，但須記錄Diff及理由，不修改原業務期待值。這些是B0實作方案，仍需實測，不在本提案宣稱已成立。

## 已套用同步清單與P5範圍

| 文件 | 同步區域 |
|---|---|
| docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md | §13／14／19／20.3／25／26／29的單項失敗、全G1通過與交接描述 |
| docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md | §6／8／31的唯一失敗與B1恢復；保留B1全套通過要求 |
| Agent.md | 版本表、驗證、O-04狀態 |
| agentic-workshop/00-governance/acceptance-gates.md、consistency-rules.md、technical-baseline.md、version-validation-requirements.md、rule-traceability-baseline.md、workshop-manifest.md | B0預期失敗集合／B1恢复／O-04狀態 |
| docs/planning/decisions-and-open-issues.md、production-roadmap.md、repository-structure.md | 核准紀錄、P5Gate與來源；歷史證據保留為當時事實 |

已完成上述規格同步；後續P5為Time Skip學員3／主持2文件、B0完整程式与接手學員4／主持3／評估4文件，及要求的clean-copy。B0需35–45實質Python與測試檔、約30–45測試、三項債／兩項文件落差；延續G1 Tag歷史，clean-copy從同一固定B0來源產生並比對。不得提前建立B1–B3答案。

## 完成與核准條件

本次提案與核准套用已完成。**O-04規格衝突已解除**，核准日期2026-10-05、原文「套用」；B0仍須實際產製及驗證manifest、Regression與其餘Gate，不以規格同步代替程式驗收。
