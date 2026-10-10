# 各版本驗證要求

> 目標讀者：Facilitator、Evaluation、Agent Production。
> 使用時機：P2 定義驗證基線；G0／G1／B0–B3 交付前逐版執行並留存證據。
> 前置條件：已閱讀 [Acceptance Gates](acceptance-gates.md)、[技術基線](technical-baseline.md)與[Rule 追溯基線](rule-traceability-baseline.md)；確認本版來源及上一版 Gate。
> 可見性：內部；含故意失敗與驗收條件，不整份放入 Participant Package。
> 文件完成條件：命令、證據、版本預期及來源可核對；本文件為 P2 純文件交付，未執行安裝、程式或測試，不代表任何版本已通過。

## 每版必備實際證據

每版從自己的 Repository 根目錄開始，建立獨立、乾淨 `.venv`；不得沿用上一版環境或拿上一版報告代替。報告記錄版本／來源 Commit 或內容識別、工作目錄、日期、執行者、完整命令、退出碼與輸出附件。

| Gate | 留存內容 |
|---|---|
| A 環境／Import | Python 3.13 版本、直譯器路徑、requirements 安裝完整結果、pip freeze／pip check；必要檔案清單；`src` Import 成功與載入來源路徑；不依賴外部憑證 |
| B 啟動／API | 實際 uvicorn 啟動紀錄；TestClient 載入 App，`/health` HTTP 200 且 body 為 `{"status":"ok"}`；`/openapi.json` HTTP 200、有效 OpenAPI schema／paths；保留 smoke 輸出 |
| C pytest | 全套命令與完整 summary：passed／failed／skipped／xfailed／xpassed／warnings、耗時；失敗 node ID 與 traceback；另列 Regression 範圍、結果及 Warning 原因 |
| D 追溯 | Requirement／AC → Rule ID → 實作檔案／符號 → test node ID → 文件 → Evaluation；確認每個引用存在、同 ID 同義，標記本版適用及未實作項 |
| E 可操作／隔離 | README 命令可重現、Seed／Reset 可重置；Participant／Facilitator／Evaluation 隔離檢查；限制、未完成及 Recovery 說明 |

## 可執行命令選項

以下採標準入口 `src/smart_ticket/main.py` 的 `smart_ticket.main:app`；若實際入口不同，須先以本版 README 的入口更新命令並記錄。新環境安裝依本版 requirements；相容性須由實測證明。

Windows PowerShell（不需啟用環境）：

```powershell
py -3.13 -m venv .venv
$venvPython = '.\.venv\Scripts\python.exe'
& $venvPython --version
& $venvPython -m pip install -r requirements.txt
& $venvPython -m pip freeze
& $venvPython -m pip check
$env:PYTHONPATH = 'src'
& $venvPython -c "import sys,smart_ticket.main as m; print(sys.executable); print(m.__file__); print(m.app)"
& $venvPython -m pytest -q -ra
& $venvPython -c "from fastapi.testclient import TestClient; from smart_ticket.main import app; c=TestClient(app); h=c.get('/health'); print(h.status_code,h.json()); assert h.status_code==200 and h.json()=={'status':'ok'}; o=c.get('/openapi.json'); print(o.status_code,o.json().get('openapi')); assert o.status_code==200 and o.json().get('openapi') and '/health' in o.json()['paths']"
& $venvPython -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

POSIX shell：

```sh
python3.13 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip freeze
.venv/bin/python -m pip check
PYTHONPATH=src .venv/bin/python -c 'import sys,smart_ticket.main as m; print(sys.executable); print(m.__file__); print(m.app)'
PYTHONPATH=src .venv/bin/python -m pytest -q -ra
PYTHONPATH=src .venv/bin/python -c 'from fastapi.testclient import TestClient; from smart_ticket.main import app; c=TestClient(app); h=c.get("/health"); print(h.status_code,h.json()); assert h.status_code==200 and h.json()=={"status":"ok"}; o=c.get("/openapi.json"); print(o.status_code,o.json().get("openapi")); assert o.status_code==200 and o.json().get("openapi") and "/health" in o.json()["paths"]'
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

uvicorn 為前景程序，確認啟動後以 Ctrl+C 停止並留存紀錄。逐步執行並核對退出碼（PowerShell `$LASTEXITCODE`／POSIX `$?`）；安裝或 Import 失敗不得繼續判定通過。B0 的 pytest 非零退出碼必須核對指定故意失敗，不能直接視為正常。TestClient smoke 只驗證基本載入與協定，不能代替商業流程與完整測試。

## 版本預期與 Final Decision

| 版本 | 必須核對的預期 | Final Decision |
|---|---|---|
| G0 | Health／框架測試通過；未實作 Feature 可明確 Skip，列 node ID、原因與待辦；不得有未知失敗 | 依 G0 報告記錄 Gate 結果，不套用後續版本通過名稱 |
| G1 | 全套通過、無 skip／xfail／xpass；至少 18 個有效測試，目標小於 5 秒；Warning 無或僅已記錄且不影響執行的相容性 Warning；AC／Rule 可追溯 | `PASS`／`PASS WITH DOCUMENTED LIMITATION`／`FAIL` |
| B0 | 僅一個 `BUG-B0-001`；全部 28 項 G1 Regression 與正確斷言保留；完整實測失敗 node ID 集合與已核實 Intentional Failure Manifest 完全一致，零非預期失敗、其餘全部通過；無 skip／xfail／xpass／未知 Warning | `PASS AS BROWNFIELD BASELINE`／`FAIL`；實測待驗收 |
| B1 | Manifest 全部失敗恢復，最小修復與規則一致；全部 28 項原 G1 及全部 B0 新增測試通過，無 skip／xfail／xpass；28 非 B1 全套數 | B1–B3 整體 `PASS FOR WORKSHOP USE`／`FAIL`；個別版本另列 Gate 結果 |
| B2 | 最有利單一優惠、逐人計價、改票與文件同步；全套及 Regression 通過，無 skip／xfail／xpass | 同 B1–B3 整體決策，保留本版獨立報告 |
| B3 | 團體邊界／連續座位／原子性／付款補償／單一 Order／B2 計價／Audit 與通知；全套及 Regression 通過，無 skip／xfail／xpass／未知失敗；完整套件建議 55–75 個、目標小於 10 秒 | 同 B1–B3 整體決策，保留本版獨立報告 |

O-04 規格衝突已解除：2026-10-05 使用者以「套用」核准[方案 A](../../docs/planning/b0-regression-gate-proposal.md)。B0已按方案A實測驗收；Manifest 須列完整 node ID、Rule／AC、Diff／呼叫路徑與修復驗證，證明每項失敗皆由唯一 Bug 造成。不得刪除、弱化、改預期、Skip／XFail 或隱藏 G1 測試；不得另設正確計價分支繞過 Bug。可記錄 fixture／組裝的原 Seed、固定非提前優惠 Clock／可選 Member 適配，原 28 項測試 body／assert 不改；完整 B0 Seed／新增功能另測。集合不一致或有非預期失敗即 FAIL；pytest 非零退出碼不得記一般通過。

O-07：G1 已取得 `PASS`，B0 前置滿足；`PASS WITH DOCUMENTED LIMITATION` 不等於前置 `PASS` 的一般門檻保留。G1 案例歷史／Tag 與 Bundle 已建立，B0 須延續來源與隔離。報告列 Known Limitations、未解除問題與實際證據；未執行項明記「未驗證」，不得推定通過。

## 來源

- [01 技術棧與 Repository 標準](../../docs/instructions/01_技術棧與Repository標準指令書.md)：環境、src、Gate A–E。
- [03 G1 Reference MVP](../../docs/instructions/03_G1_Greenfield_Reference_MVP產製指令書.md)：測試、Warning、限制及決策。
- [04 B0 Repository 演化](../../docs/instructions/04_B0_Brownfield_Repository演化產製指令書.md)：故意失敗、Regression、B0 決策。
- [05 Brownfield 任務卡與 B1–B3](../../docs/instructions/05_Brownfield任務卡與B1-B3產製指令書.md)：逐版 AC、Regression 與整體決策。
- [Acceptance Gates](acceptance-gates.md)：跨階段前置、O-04／O-07 與隔離要求。

## 完成條件

各版本的命令、證據、例外與進入條件可追溯；本 P2 文件交付不表示安裝、程式或測試已執行。實際商業流程 Smoke 與完整測試仍需於後續逐版取得證據。

2026-10-05 P5實測紀錄：B0為38實質Python／測試檔、44項測試；正式5failed／39passed符合完整manifest且零非預期，隔離一行學生率修復44passed。52檔clean-copy雜湊一致、B0 Tag392d920與Bundle續G1，已知相容Warning保留。詳見[B0 Validation Report](../03-brownfield/evaluation/01-b0-validation-report.md)。B1正式版本、真實學員與90分鐘演練仍未完成。

2026-10-05 P6正式B1驗收：獨立環境44passed／1已知Warning（1.00s），全部28G1與16B0新增通過、五Manifest失敗全部恢復，原測試／優惠順序不變。案例Tag a1c1d45與52檔來源核對通過，個別B1 Gate PASS；詳見[B1 Validation Report](../03-brownfield/evaluation/12-b1-validation-report.md)。B2／B3與B1–B3整體驗收、真實8分鐘／90分鐘演練仍待完成。
