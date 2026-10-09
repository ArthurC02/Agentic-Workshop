---
id: environment
title: 開場與環境
minute: 00-10
group: dlc-opening
section: 開始之前
---

# 開場與環境

```callout info
現在在做什麼
- **情境**：你接手 Smart Ticket 的訂票後端，今天要替它建立 Agent 用得上的 Domain Memory。先把環境備好。
- **你的目標**：10 分鐘內讓 Agent 把起始 Repo 測試跑綠、原樣解出 Plugin 並核對雜湊、確認專案狀態與真正的 Python。
- **今天的技巧**：先講好「看到什麼算成功」，再讓 Agent 執行並回報。每個提示詞都寫明成功的樣子（例如 `76 passed`、`SHA OK 130 files`），Agent 的回報對得上才往下；你不用看懂指令，只看結果。
- **完成的樣子**：`notes/opening.md` 有 Agent 寫的四個檢查點結果；起始 commit 已建立，還沒有 `domain-memory/`。
```

本段沒有需要你決定的事，所以沒有表單。四個檢查點的指令都已寫進提示詞，由 Agent 執行。

## 檢查點總覽

時間是**最晚**完成的時間；提早完成就直接進入下一個。

- **檢查點 1 · 依賴安裝與測試（0–3）**：下載、解壓到短路徑；Agent 建 venv（Python 虛擬環境）、安裝依賴、測試全綠。
- **檢查點 2 · 解出 Plugin 並核對 SHA256（3–5）**：Agent 解出 Plugin 0.2.2，逐檔核對 SHA256。
- **檢查點 3 · 專案就緒與品質關卡檢查（5–8）**：Agent 確認 Plugin 判定 brownfield（已有程式碼的既有專案），並找到 pytest。
- **檢查點 4 · 確認真實 Python（8–10）**：Agent 確認 `python` 是 venv 裡的真實直譯器、建立起始 commit、環境健檢全部通過。

## 前置需求

- Windows 上的 Python **3.13**，而且有 `py` launcher（Python 啟動器）。
- Git for Windows 2.34 以上（D2 的 SSH 簽章需要）。
- 一個可讀寫本機資料夾、能執行終端機指令的 Coding Agent（主課用過的那一個即可）。

## 檢查點 1 · 依賴安裝與測試（第 0–3 分鐘）

```download
id=participant-dlc-open zip=participant-dlc-open.zip label=下載學員包（起始 Repo、輔助工具、domain-memory Plugin）
```

- [ ] 按上方按鈕下載 `participant-dlc-open.zip`，在檔案上按右鍵選「全部解壓縮」，目的地輸入 `C:\dlc`。
- [ ] 在 `C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository\smart-ticket-dlc-base` 這個資料夾開啟你的 Agent（這裡稱為 Repo 根目錄）。
- [ ] 先貼下方的「工作規則」，再貼本檢查點的提示詞。

```callout warning
一定要解壓到 C:\dlc 這種短路徑
Plugin 更新 Registry 時會在 `domain-memory/` 底下建立很長的暫存資料夾名稱。放在桌面、OneDrive 或深層資料夾，會在 D1 出現「檔名或副檔名太長」（WinError 206）。不要放在同步資料夾。
```

**工作規則**（整場只貼一次；之後開新的 Agent 對話時再貼一次）。規則先講好，之後每個提示詞就不用重複「用哪個終端機」「做完停下」。這段是給 Agent 的，不需要看懂：

```text
以下是今天這堂延伸課程的工作規則，請在整段對話中遵守：
1. 你負責所有指令操作與檔案編輯；我不自己打指令、不讀程式。每次做完用白話告訴我結果，並引用關鍵的實際輸出字樣（例如「76 passed」「Registry is valid.」），不要只貼原始輸出。
2. 每一步做完就停下等我。需要我決定的地方，先列出選項或草稿，每項附證據（路徑:起-迄，行號要實際打開檔案核對），然後等我回覆「同意」或「改成…」。
3. 除非我另外說明，所有指令都在目前的 Repo 根目錄（smart-ticket-dlc-base）執行。先判斷你執行指令用的是哪一種終端機：PowerShell 就用提示詞裡的 PowerShell 寫法（Plugin 一律經 ..\..\tools\dm.ps1，每個新的 PowerShell 程序先執行 Set-ExecutionPolicy -Scope Process Bypass -Force）；bash（例如 Git Bash）就用 bash 寫法（Plugin 一律經 ../../tools/dm.sh）。不要直接執行 registry_tools.py，也不要手動修改 domain-memory/ 底下的檔案。
4. 你的每個指令可能在新的終端機程序執行，啟用過的 venv 不會延續：需要 python 時，在同一個指令裡先啟用 .venv（PowerShell：.\.venv\Scripts\Activate.ps1；bash：source .venv/Scripts/activate），或直接用 .venv 裡的 python.exe。
5. 你或我新增到 Domain Memory 的內容一律是候選（candidate），不要寫成「已確認」，也不要當成限制。
6. 沒有我的指示，不要 git commit 或 git push；不要讀取、複製或顯示任何私鑰檔。
7. 你沒有實際執行的事情，一律標「未驗證」。
請回覆「了解」，然後等我的下一個指示。
```

本檢查點的提示詞：

```text
請準備起始 Repo 的執行環境，不要修改任何程式：
1. 在 Repo 根目錄建立 venv、安裝依賴、執行全部測試。
   PowerShell：
     py -3.13 -m venv .venv
     & '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
     & '.\.venv\Scripts\python.exe' -m pytest -q
   bash：
     py -3.13 -m venv .venv
     .venv/Scripts/python.exe -m pip install -r requirements.txt
     .venv/Scripts/python.exe -m pytest -q
   本 Repo 只用 pip install -r requirements.txt，不要執行 pip install -e .（測試設定已包含 src 路徑）。
2. 用白話告訴我：測試最後一行是什麼（成功應為 76 passed，可能附帶 1 warning）、有沒有 failed 或 error。
3. 建立 notes/opening.md，寫入標題「檢查點 1 · 依賴安裝與測試」、Repo 的完整路徑、pytest 最後一行原文、遇到的問題與處理（沒有就寫「沒有」）。
做完停下等我。
```

**看到什麼算過關**

- Agent 回報測試最後一行是 `76 passed`（可能附帶 `1 warning`），沒有 `failed` 或 `error`。
- Repo 路徑在 `C:\dlc\` 底下。

**如果卡住**（安裝失敗或測試不是全過）：

```text
請先不要修改任何檔案。用白話解釋剛才的錯誤訊息：是 Python 版本、網路／pip 來源，還是資料夾位置的問題？列出你建議的處理方式，等我同意再做。
```

## 檢查點 2 · 解出 Plugin 並核對 SHA256（第 3–5 分鐘）

Plugin 必須**原樣**使用：今天的 Registry 規則與各種檢查都由它判定，任何一個位元組被改過，結果就不可信。這一步讓 Agent 逐檔比對雜湊，你只看它回報的一行結論。

```callout info
新概念：SHA256 雜湊
雜湊是由檔案內容算出的一串固定長度的字，像檔案的指紋：內容改了一個位元組，雜湊就完全不同。SHA256 是常用的一種。學員包附了每個 Plugin 檔案的「正確指紋」清單，Agent 重算一次、逐檔比對，全部相同才印 `SHA OK`。D1 起 Plugin 也用同樣的方法記住你引用的證據內容。
📖 延伸閱讀：NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉。
```

```text
請解出 domain-memory Plugin 並逐檔核對 SHA256，不要修改 Plugin 的任何檔案：
1. 到 ..\..\vendor（bash：../../vendor）資料夾，解出 Plugin、逐檔核對清單、顯示版本，再回到 Repo 根目錄。
   PowerShell：
     Set-Location ..\..\vendor
     Expand-Archive -LiteralPath .\domain-memory-0.2.2.zip -DestinationPath .
     py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.2.2.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
     Select-String '"version"' .\domain-memory\.claude-plugin\plugin.json
     Set-Location ..\repository\smart-ticket-dlc-base
   bash：
     cd ../../vendor
     unzip -q domain-memory-0.2.2.zip
     py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.2.2.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
     grep '"version"' domain-memory/.claude-plugin/plugin.json
     cd ../repository/smart-ticket-dlc-base
2. 用白話告訴我核對結果與版本。如果出現 SHA MISMATCH，立刻停下，不要使用這份 Plugin，也不要嘗試修正。
3. 在 notes/opening.md 加上標題「檢查點 2 · Plugin 完整性」，寫入核對輸出與版本原文。
做完停下等我。
```

**看到什麼算過關**：Agent 回報 `SHA OK 130 files`（129 個 Plugin 檔案加 ZIP 本身），以及 `"version": "0.2.2"`。出現 `SHA MISMATCH` 就停下，請主持人協助。

## 檢查點 3 · 專案就緒與品質關卡檢查（第 5–8 分鐘）

`readiness` 只觀察檔案系統，告訴你這個 Repo 處於什麼狀態（`state`：例如 brownfield，已有程式碼的既有專案）以及判斷有多確定（`confidence`）；`quality-gates` 列出 Repo 自己已有的檢查。兩者都是唯讀。這一步也讓 Agent 第一次經過 `dm` 腳本呼叫 Plugin，之後所有 Plugin 指令都走同一條路。

📖 延伸閱讀：學員包 `vendor/domain-memory/references/readiness.md`（Plugin 自帶，列出每一種 state 的意思）。

```text
請用 dm 腳本執行兩個唯讀檢查，不要修改任何檔案：
PowerShell：
  Set-ExecutionPolicy -Scope Process Bypass -Force
  ..\..\tools\dm.ps1 readiness
  ..\..\tools\dm.ps1 quality-gates
bash：
  ../../tools/dm.sh readiness
  ../../tools/dm.sh quality-gates
然後用白話告訴我：
1. readiness 的 state 與 confidence 是什麼？
2. quality-gates 找到哪些檢查？有沒有 lint（程式風格檢查）、型別或架構檢查？
3. 這代表你之後改程式時，哪些問題只能靠測試和人的審查才抓得到？
在 notes/opening.md 加上標題「檢查點 3 · 專案就緒與品質關卡」，寫入上面三題的答案與關鍵輸出原文。做完停下等我。
```

**看到什麼算過關**

- `readiness` 為 `"state": "brownfield"`、`"confidence": "high"`。
- `quality-gates` 只有一項 `"tool": "pytest"`，`"standard": "none"`（沒有 lint、型別或架構檢查，這是事實，不是錯誤）。
- 每次執行前 `dm` 會先印一行 `[dm] registry_tools.py ...`，顯示實際送給 Plugin 的完整指令；Agent 可以引用它。

```callout info
為什麼一定要經過 dm.ps1／dm.sh
繁體中文 Windows 的預設編碼是 cp950（不是 UTF-8）。Plugin 讀寫的 JSON 與文件含中文，少了 `-X utf8` 會出現 `UnicodeDecodeError`。`dm` 固定用 `py -3.13 -X utf8` 執行 Plugin，並自動補上 Registry 與 Repo 的路徑參數。工作規則第 3 條已要求 Agent 一律經過它。
```

```callout tip
💬 討論一下
這個 Repo 沒有任何程式風格、型別或架構檢查。Agent 之後改程式時，哪一類錯誤最可能溜過去？
```

## 檢查點 4 · 確認真實 Python（第 8–10 分鐘）

D2 推送（push）時，pre-push hook（push 前 Git 自動執行的檢查腳本）會直接呼叫 `python`。教室電腦上的 `python` 常常是 Microsoft Store 的別名（路徑含 `WindowsApps`），會讓 push 失敗。啟用 Repo 的 venv 後，`python` 才是 venv 裡的真實直譯器。這一步也建立起始 commit，之後 Agent 才說得清楚改了什麼。

```text
請確認真實 Python、建立起始 commit，並執行環境健檢：
1. 在同一個指令裡啟用 venv 並確認 python 的版本與路徑：
   PowerShell：.\.venv\Scripts\Activate.ps1; python --version; (Get-Command python).Source
   bash：source .venv/Scripts/activate && python --version && command -v python
2. 執行環境健檢（它會檢查 PATH 上的 python，所以同一個指令裡要先啟用 venv）：
   PowerShell：.\.venv\Scripts\Activate.ps1; py -3.13 -X utf8 ..\..\tools\doctor.py
   bash：source .venv/Scripts/activate && py -3.13 -X utf8 ../../tools/doctor.py
3. 在 notes/opening.md 加上標題「檢查點 4 · 真實 Python 與環境健檢」，寫入 python 版本與路徑原文、doctor.py 的最後一行，以及有沒有 [!!]（[--] 只是提醒）。這份紀錄要在下一步 commit 之前寫完。
4. 建立起始 commit（這時還沒有 domain-memory/，所以不需要簽章）。Git 使用者只設在本 Repo，不要用 --global：
   git init
   git config --local user.name "DLC Proposer"
   git config --local user.email proposer@example.com
   git add -A
   git commit -m "起始 Repo"
5. 用白話告訴我：python 是不是 3.13.x、路徑是否在 smart-ticket-dlc-base 的 .venv\Scripts 底下且不含 WindowsApps；doctor.py 的最後一行、有沒有 [!!]；起始 commit 是否建立、裡面有沒有 domain-memory/；commit 後 git status --short 是不是空的。不要再改 notes/opening.md。
做完停下等我。
```

**看到什麼算過關**

- `python --version` 為 `Python 3.13.x`，路徑在 `smart-ticket-dlc-base\.venv\Scripts\` 底下，**不含** `WindowsApps`。
- `doctor.py` 最後一行為「全部必要項目通過。」（`[--]` 只是提醒，不算失敗；健檢時還沒 `git init`，所以會看到 `[--] git repo：目前目錄不是 git repo…`，這是預期，下一步就建立 commit）。
- 起始 commit 已建立，裡面沒有 `domain-memory/`；`git status --short` 是空的（`notes/opening.md` 已一起 commit）。

**如果卡住**（`python` 指向 `WindowsApps` 或 doctor 有 `[!!]`）：

```text
請不要修改程式。用白話解釋 doctor.py 每一個 [!!] 項目或 python 路徑不對的原因，以及它建議的修正方式；只列出來，等我同意再做。
```

```callout tip
為什麼 Git 使用者叫 DLC Proposer
今天只在本機練習，每個人先以 `proposer@example.com` 身分工作。第 7 分鐘主持人會請你找一位夥伴，D2 起兩人一組：夥伴（Maintainer，持鑰人）會以 `maintainer@example.com` 身分核准與簽章。這兩個字串會出現在稽核紀錄裡，讓你看清楚「誰做了什麼」。
```

```callout danger
第 10 分鐘仍未通過
不要在活動中更換 Python 版本或改用其他語言或工具。告知主持人，D1 起先和夥伴共用一台已通過的機器，並請 Agent 在 `notes/opening.md` 記下卡在哪一步。
```

```callout tip
這段學到的技巧
交給 Agent 執行之前，先寫好「看到什麼算成功」；Agent 的回報對得上這幾個字樣才往下。你不用看懂指令，也能判斷環境是不是真的好了。
```
