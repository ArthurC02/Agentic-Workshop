# 環境準備

> 讀者：主持人與環境準備人員。時機：活動前。前置：取得本次受控來源與可用的通用Coding Agent。可見性：Facilitator；需另產學員版，不直接分享含內部定位的本檔。

統一Python3.13（已驗收3.13.15）、venv／pip、FastAPI0.115.12、Uvicorn0.34.2、Pydantic2.11.4、pytest8.3.5、httpx0.28.1、Starlette0.46.2、AnyIO4.9.0；以各版requirements.txt為準。不需要前端、外部DB、真實金流／交通API。本機案例不依賴外部API；Agent服務或本機工具的可用性須另確認，不以案例Health代替Agent可用。

## 學員電腦：由Agent代為準備

全程人不碰程式：學員不自己打下列指令。學員在Agent對話貼上Greenfield 檢查點 1 的提示詞（寫專案根目錄的`AGENTS.md`與`check` Skill，照它建.venv、安裝requirements.txt、跑pytest -q並白話回報）與檢查點 4 的啟動提示詞（背景啟動8000埠伺服器、確認/health、給出/docs網址），由Agent代做；學員只在瀏覽器開/docs試API。主持事前要在每台學員電腦實測這條路徑可行（見[Preflight](preflight-checklist.md)），包括Agent有權限執行指令、能在背景啟動伺服器、瀏覽器能連到127.0.0.1。下列手動指令只供主持／環境準備人員驗證與排錯用。

## AGENTS.md與Skill自動載入

課程把規則放在專案根目錄的`AGENTS.md`、固定做法放在標準Skill（`<工具的專案Skill資料夾>/<名稱>/SKILL.md`，開頭有name與description）；B0與兩份Recovery包附前任同事的`AGENTS.md`。學員頁不寫工具名稱，下列以常見工具為例，供主持事前確認與現場排錯（2026-10-22查核）：

- Claude Code：v2.1.277起由內建外掛`cc-plugin-agents-md@builtin`讀`AGENTS.md`，預設只在工作資料夾及其上層都沒有`CLAUDE.md`／`CLAUDE.local.md`時才讀。版本較舊、停用該外掛，或剛從2.1.276以前升級後的第一個工作階段，有時讀不到；v2.1.281以前，經Bedrock或關閉遙測的工作階段只讀`CLAUDE.md`。補救二擇一：建一個只有一行`@AGENTS.md`的`CLAUDE.md`；或在`/config`把Project instructions設為`claude-md-and-agents-md`。專案Skill在`.claude/skills/<名稱>/SKILL.md`。
- Codex：從Git根目錄往下到目前資料夾逐層讀`AGENTS.md`，合計預設上限32 KiB；專案Skill在`.agents/skills/<名稱>/SKILL.md`。
- 現場讀不到時，學員照Runbook Time Skip檢查點2貼「請先讀AGENTS.md。再把你的工具設定成之後開新對話會自動讀它」，Agent會自己用上面的補救；不要發`CLAUDE.md`給學員。
- Preflight時在每台學員電腦開新對話問「這個專案的工作規則是什麼？只引用AGENTS.md原文」，確認讀得到。

## 每版獨立準備

在已核對來源的版本根目錄操作，不共用可變Store或跨版本Import。下列是待執行步驟，不代表本輪已安裝或Preflight。

PowerShell：

```powershell
py -3.13 --version
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\python.exe' -m pytest -q
& '.\.venv\Scripts\python.exe' -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

一般shell（macOS 用 python3.13）：

```bash
python3.13 --version
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn smart_ticket.main:app --app-dir src --host 127.0.0.1 --port 8000
```

pyproject的pytest設定包含src Import Path；啟動用`--app-dir src`。單獨Import或TestClient明確使用本版venv及src路徑。

PowerShell：

```powershell
$env:PYTHONPATH='src'
& '.\.venv\Scripts\python.exe' -c 'from smart_ticket.main import app; print(app.title, app.version)'
```

一般shell：

```bash
PYTHONPATH=src .venv/bin/python -c 'from smart_ticket.main import app; print(app.title, app.version)'
```

另一終端以`curl.exe http://127.0.0.1:8000/health`（PowerShell）或`curl`檢查200及status=ok，並檢查`/openapi.json`與App版本。切版先以Ctrl+C停止自己啟動的Server（學員電腦則請Agent停止它啟動的伺服器），確認新版本正常啟動，避免讀到舊程序；不終止其他人的程序。Port佔用時改未使用Port並記錄。

## 主持來源與學員發放

G0為`01-greenfield/participant/starter-repository/`，B0為`03-brownfield/participant/repository/smart-ticket-b0/`（學員實際內容以 participant-29-b0.zip 為準）。G1與B1–B3位於Evaluation，只供主持驗證；學員只取得按[Recovery](recovery-plan.md)整理的受控版本，不能取得作者Repo或Bundle。

事前完成依賴下載／安裝與Agent操作確認；若網路不可用且依賴未備妥，改用事先已驗證環境或分析降級，不在120分鐘中臨時更換Python版本或改用其他技術。各版venv不進交付包。資料固定種子、可控Clock／Gateway與In-Memory，重啟會重置；先保存學員成果再復原。

完成條件：逐版Python／依賴／Import／Health／OpenAPI及版本Gate真實證據完整、學員受控來源與Agent可用，且每台學員電腦的Agent能代為建環境、啟動伺服器，瀏覽器能開/docs；填[Preflight](preflight-checklist.md)，未執行項不勾選。
