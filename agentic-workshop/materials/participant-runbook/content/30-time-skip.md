---
id: time-skip
title: Time Skip：12 個月後
minute: 29-33
group: timeskip
section: Time Skip
---

# Time Skip：12 個月後

這是 Time Skip（時間快轉：專案假設已開發一段時間）：Smart Ticket 已上線 12 個月。請在 **4 分鐘**內停止自己的 Greenfield（從頭開始的新專案）開發，改為接手主持人統一提供的 **B0 - Brownfield Baseline**，請 Agent 建好環境、跑過測試。Brownfield 是已有程式碼的既有專案；B0 是它的起點版本，之後的 B1、B2、B3 是接在 B0 上的三段任務代號。Agent 的角色從 **Tool**（工具）轉為 **Teammate**（隊友）：先各自請 Agent 分析、比較判斷，再整合成小組的共同脈絡（Shared Context：小組整理出的共同事實）。

```callout warning
本段只接手，不修改
本段只做停手、下載、請 Agent 建環境與跑測試。**不要修改 B0 的程式**，也先不要叫 Agent 開始分析；個人分析從第 33 分鐘開始。全場使用同一份 B0，不要用自己的 Greenfield 成果代替。你不需要自己打終端機指令，也不需要讀程式：指令由 Agent 執行，你看它的白話回報做判斷。
```

```callout info
投影畫面和這份 Runbook 怎麼分工
投影畫面只顯示**時間**和**現在進行到第幾個檢查點**。要做什麼、要填的表單，全部在本頁。主持人換頁時，請跟著跳到本頁對應的檢查點。
```

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個檢查點。

| 檢查點 | 全場分鐘 | 段內時間 | 你要完成的事 |
|---|---:|---:|---|
| 1 · 停手 | 29–30 | 00–01 | 停止 Greenfield、保留現況，讀時間快轉公告 |
| 2 · 取得 B0 | 30–31 | 01–02 | 下載 B0、解壓到短路徑，開新的 Agent Session 並貼上工作規則 |
| 3 · 環境與版本 | 31–32 | 02–03 | 請 Agent 建環境、跑測試、啟動 B0，確認版本是 B0、Health 正常 |
| 4 · 測試與基準 | 32–33 | 03–04 | 請 Agent 建立 Git 基準、保留測試結果，讀交接說明 |

接下來：第 33–39 分鐘用自己的 Agent [個人分析](#individual-analysis)（先讀 [B0 系統 Context](#b0-context)）→ 第 39–44 分鐘小組整理 [Shared Context](#shared-context) → 第 44–52 分鐘依發放的任務與核准計畫工作。

## 檢查點 1 · 停手（第 29–30 分鐘）

- [ ] 停止修改自己的 Greenfield Repository，保留現況，不要刪除或覆寫。
- [ ] 在原本 Greenfield 的 Agent 對話貼上下方提示詞，請它停止 G0（Greenfield 起始包）的 App：

```text
請停止你在背景啟動的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 已經連不上，然後用白話告訴我結果。不要修改任何檔案。
```

- [ ] 讀下方時間快轉公告與公司成長摘要。

### 時間快轉公告

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/01-time-skip-announcement.md
```

### 公司與系統成長摘要

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/02-company-growth-summary.md
```

```form
{"id":"ts-cp1","title":"檢查點 1 確認","fields":[
{"id":"stopped","label":"已停止修改 Greenfield、保留現況，G0 的 App 已停止","type":"checkbox"}
]}
```

## 檢查點 2 · 取得 B0（第 30–31 分鐘）

```download
id=b0 zip=participant-29-b0.zip label=下載 B0 Repository
```

- [ ] 下載 `b0.zip`，用檔案總管（右鍵「全部解壓縮」）或 Finder 解壓縮到短路徑，例如 `C:\work\b0`。
- [ ] 找到 `smart-ticket-b0` 資料夾（路徑是 `agentic-workshop\03-brownfield\participant\repository\smart-ticket-b0`，裡面有 `README.md` 與 `requirements.txt`）。
- [ ] 在 `smart-ticket-b0` 開啟**新的** Agent Session（與 Agent 的對話工作階段），先把下方「Agent 工作規則」整段貼給它。這段是給 Agent 的，不需要看懂；除此之外先不要交代任何工作。

```text
以下是這次工作的規則，請在整段對話中遵守：
1. 你負責所有程式、測試與指令操作；我不會自己修改程式，也不會自己讀程式，請用白話向我說明。
2. 每次修改前先提出計畫，等我核准；只做核准的步驟，做完就停下來等我。
3. 只處理任務卡範圍，做最小修改；不全面重寫，不改不相關的 API，不新增套件、服務或優惠政策。
4. 不刪除、弱化或隱藏任何測試，不用 skip／xfail，不把正確的期待值改成符合錯誤的輸出。
5. 每次做完都執行 pytest -q，並用「驗收對照表」回報：每條驗收條件或規則一列，寫通過／失敗／未驗證，以及依據的測試名稱。不要只貼原始輸出。
6. 每次修改後用白話說明：改了哪些檔案、各改了什麼、為什麼，以及有沒有超出我核准的範圍。
7. 你沒有實際執行的事情，一律標「未驗證」。
```

```callout warning
解壓縮到短路徑
ZIP 內的資料夾層級較深。請解壓縮到 `C:\work\b0` 這類短路徑，不要放在深層的同步資料夾或桌面子資料夾，避免 Windows 路徑長度限制導致檔案不完整。
```

```callout info
B0 是一份新的 Repository
B0 不是你的 Greenfield 成果延伸。請在新的資料夾開啟 B0，並為它重新建立 Agent Session 與 Context，不要沿用 Greenfield 的 Session。
```

```form
{"id": "ts-cp2", "title": "檢查點 2 確認","fields":[
{"id": "path", "label": "B0 的資料夾路徑", "type": "text", "hint": "例如：C:\\work\\b0\\…\\smart-ticket-b0", "suggestions": [{"label": "路徑範本", "text": "C:\\work\\b0\\〈…〉\\smart-ticket-b0"}]},
{"id": "session", "label": "已在 B0 資料夾開啟新的 Agent Session（沒有沿用 Greenfield 的 Session）", "type": "checkbox"}
]}
```

## 檢查點 3 · 環境與版本（第 31–32 分鐘）

B0 要在 `smart-ticket-b0` 資料夾內**獨立**建立環境，不要沿用 G0 的環境。以下指令都由 Agent 執行。

- [ ] 把下方提示詞貼給 Agent，請它建環境並跑測試：

```text
請幫我準備這個專案的執行環境：確認 Python 版本是 3.13，在專案資料夾建立 .venv 虛擬環境並安裝 requirements.txt，接著執行 pytest -q。用白話告訴我：環境是否建好、測試有幾個通過／失敗／跳過，以及下一步要做什麼。遇到錯誤時先說明原因，不要自行修改程式。
```

- [ ] 請 Agent 確認版本：

```text
請告訴我這個 App 的名稱與版本號（app.title 與 app.version 的實際值），並用白話確認它是不是 B0 - Brownfield Baseline。不要修改任何檔案。
```

- [ ] 請 Agent 啟動 App 並確認 Health（健康檢查端點，用來確認服務有正常啟動）：

```text
請在背景啟動這個專案的伺服器（埠號 8000），確認 http://127.0.0.1:8000/health 回傳 status=ok，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
```

- [ ] 用瀏覽器打開 Agent 給的 `/docs` 網址，看得到 API 清單就表示服務正常。

```callout tip
環境問題
Agent 回報埠號 8000 被佔用、虛擬環境建不起來或套件裝不起來時，請它先用白話說明原因與建議做法，你決定後再讓它處理；可參考 [環境準備](#environment)。環境無法啟動時請立即告知主持人；請使用主持人提供的同一份 B0，不要改用其他版本。
```

```form
{"id": "ts-cp3", "title": "檢查點 3 確認","fields":[
{"id": "version", "label": "版本輸出", "type": "text", "hint": "貼上 Agent 回報的 App 名稱與版本號", "suggestions": [{"label": "輸出範本", "text": "〈app.title〉 〈app.version〉"}]},
{"id": "health", "label": "GET /health 回傳 {\"status\":\"ok\"}", "type": "checkbox"},
{"id": "env-issue", "label": "環境問題與耗時", "type": "text", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "問題與耗時", "text": "〈問題〉：〈處理方式〉，耗時約 〈分鐘〉 分鐘"}]}
]}
```

## 檢查點 4 · 測試與基準（第 32–33 分鐘）

- [ ] 保留 Agent 在檢查點 3 回報的**實際測試結果**（通過／失敗／跳過各幾個），個人分析時要用。
- [ ] 請 Agent 建立 Git 基準。B0 不是 Git Repository；先記下起始狀態，之後 Agent 才能說清楚它實際改了什麼。
- [ ] 讀下方 Brownfield 接手說明。

```text
請在這個資料夾建立 Git 基準：先 git init，再把目前所有檔案 Commit 成「B0 baseline」，不要修改任何檔案。完成後用白話告訴我 Commit 是否成功，並再貼一次 pytest -q 的最後一行摘要。如果 Git 要求設定姓名或 Email，先問我要填什麼，只設定在這個資料夾。
```

```callout warning
目前有若干測試失敗
目前有若干測試失敗，需要小組分析是否具有共同原因。**請先不要修改程式**，各自使用自己的 Agent 完成分析；保留測試結果、規則來源與推論依據。文件是線索，重要結論要請 Agent 用白話說明程式、規則、測試三者是否一致，再由你判斷。
```

```callout tip
常見狀況
- 電腦沒有 Git 時，請 Agent 說明它改用什麼方式記錄起始狀態，並在表單註明。
- `.venv`、`__pycache__`、`.pytest_cache` 已列在 B0 的 `.gitignore`，不會進入基準。
```

### Brownfield 接手說明

```include
zip=participant-29-time-skip.zip path=agentic-workshop/02-time-skip/participant/03-brownfield-handover.md
```

```form
{"id": "ts-cp4", "title": "檢查點 4 確認","fields":[
{"id": "pytest", "label": "B0 的 pytest -q 結果", "type": "text", "hint": "貼上 Agent 回報的最後一行摘要，以實際輸出為準。", "suggestions": [{"label": "結果範本", "text": "〈數字〉 failed, 〈數字〉 passed"}, {"label": "未執行", "text": "未執行：〈原因〉"}]},
{"id": "done", "label": "完成檢核", "type": "checklist", "items": ["已切換到同一份 B0，版本為 B0 - Brownfield Baseline", "已保留 pytest -q 的實際輸出", "已建立 Git 基準（或已註明改用其他變更檢視）", "尚未直接修改程式"], "hint": "只勾實際完成的項目。"}
]}
```

下一步（第 33 分鐘）：[B0 系統 Context](#b0-context)，接著 [個人 Agent 分析](#individual-analysis)。
