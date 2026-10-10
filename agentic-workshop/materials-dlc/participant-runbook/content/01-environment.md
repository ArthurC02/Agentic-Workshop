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
- **情境**：你接手 Smart Ticket 的訂票後端，今天要替它建立 Agent 用得上的 Domain Memory。
- **你的目標**：10 分鐘內讓 Agent 跑過全部測試、核對 Plugin、確認專案狀態與真實 Python。
- **今天的技巧**：先講好「看到什麼算成功」，Agent 的回報對得上才往下；你不用看懂指令。
- **完成的樣子**：`notes/opening.md` 有四個檢查點的結果；起始 commit 已建立。
```

## 前置需求

- Python **3.13**：Windows 要有 `py` 啟動器；macOS 要有 `python3.13`。
- Git 2.34 以上（Windows 是 Git for Windows）。
- 一個能讀寫本機資料夾、執行終端機指令的 Coding Agent（主課用過的即可）。

## 檢查點 1 · 安裝相依套件與測試（第 0–3 分鐘）

① 為什麼做這一步

今天每一步都以測試結果為準，所以先讓 Agent 建好環境，確認起始 Repo 的測試全部通過。先做完這三件事：

```download
id=participant-dlc-open zip=participant-dlc-open.zip label=下載學員包（起始 Repo、輔助工具、domain-memory Plugin）
```

- [ ] 按上方按鈕下載 `participant-dlc-open.zip`，再解壓縮：
  - Windows：在檔案上按右鍵選「全部解壓縮」，目的地輸入 `C:\dlc`。
  - macOS：在家目錄建立 `dlc` 資料夾，把 zip 移進去後按兩下解壓縮，得到 `~/dlc/agentic-workshop`。
- [ ] 在 Repo 根目錄開啟你的 Agent：
  - Windows：`C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository\smart-ticket-dlc-base`
  - macOS：`~/dlc/agentic-workshop/07-dlc-ddd/participant/repository/smart-ticket-dlc-base`
- [ ] 依序貼下方兩段。

② 貼給 Agent

先貼工作規則（整場只貼一次；之後開新的 Agent 對話時再貼一次）。這段是給 Agent 的，不需要看懂：

```prompt
# windows
以下是今天這堂延伸課程的工作規則，請在整段對話中遵守：
1. 你負責所有指令操作與檔案編輯；我不自己打指令、不讀程式。每次做完用白話告訴我結果，並引用關鍵的實際輸出字樣（例如「76 passed」「Registry is valid.」），不要只貼原始輸出。
2. 每一步做完就停下等我。需要我決定的地方，先列出選項或草稿，每項附證據（路徑:起-迄，行號要實際打開檔案核對），然後等我回覆「同意」或「改成…」。
3. 除非我另外說明，所有指令都在目前的 Repo 根目錄（你開啟 Agent 的資料夾，例如 smart-ticket-dlc-base；改用 Recovery 時是 resume- 開頭的資料夾）執行。不要直接執行 registry_tools.py，也不要手動修改 domain-memory/ 底下的檔案。
4. 這台是 Windows，提示詞寫的是 PowerShell 寫法：Plugin 一律經 ..\..\tools\dm.ps1，每個新的 PowerShell 程序先執行 Set-ExecutionPolicy -Scope Process Bypass -Force。如果你的終端機是 bash（例如 Git Bash），反斜線換成斜線、參數不變：..\..\tools\dm.ps1 換成 ../../tools/dm.sh，.venv\Scripts\python.exe 換成 .venv/Scripts/python.exe；提示詞另外寫了 Git Bash 寫法時就用那一組。
5. 你的每個指令可能在新的終端機程序執行，啟用過的 venv 不會延續：需要 python 時直接用 .venv\Scripts\python.exe，或在同一個指令裡先啟用 .venv（PowerShell：.\.venv\Scripts\Activate.ps1；Git Bash：source .venv/Scripts/activate）。
6. 你或我新增到 Domain Memory 的內容一律是候選（candidate），不要寫成「已確認」，也不要當成限制。
7. 沒有我的指示，不要 git commit 或 git push；不要讀取、複製或顯示任何私鑰檔。
8. 你沒有實際執行的事情，一律標「未驗證」。
請回覆「了解」，然後等我的下一個指示。
# macos
以下是今天這堂延伸課程的工作規則，請在整段對話中遵守：
1. 你負責所有指令操作與檔案編輯；我不自己打指令、不讀程式。每次做完用白話告訴我結果，並引用關鍵的實際輸出字樣（例如「76 passed」「Registry is valid.」），不要只貼原始輸出。
2. 每一步做完就停下等我。需要我決定的地方，先列出選項或草稿，每項附證據（路徑:起-迄，行號要實際打開檔案核對），然後等我回覆「同意」或「改成…」。
3. 除非我另外說明，所有指令都在目前的 Repo 根目錄（你開啟 Agent 的資料夾，例如 smart-ticket-dlc-base；改用 Recovery 時是 resume- 開頭的資料夾）執行。不要直接執行 registry_tools.py，也不要手動修改 domain-memory/ 底下的檔案。
4. 這台是 macOS：Plugin 一律經 ../../tools/dm.sh。dm.sh 會用 PATH 上的 python3，所以每個 dm.sh 指令都在同一個指令裡先啟用 .venv，例如 source .venv/bin/activate && ../../tools/dm.sh validate。zip 解開後 dm.sh 沒有執行權限，出現 permission denied 時先在 Repo 根目錄執行一次 chmod +x ../../tools/dm.sh。
5. 你的每個指令可能在新的終端機程序執行，啟用過的 venv 不會延續：需要 python 時直接用 .venv/bin/python，或在同一個指令裡先 source .venv/bin/activate。
6. 你或我新增到 Domain Memory 的內容一律是候選（candidate），不要寫成「已確認」，也不要當成限制。
7. 沒有我的指示，不要 git commit 或 git push；不要讀取、複製或顯示任何私鑰檔。
8. 你沒有實際執行的事情，一律標「未驗證」。
請回覆「了解」，然後等我的下一個指示。
```

再貼本檢查點的提示詞：

```prompt
# windows
請準備起始 Repo 的執行環境，不要修改任何程式：
1. 在 Repo 根目錄建立 venv、安裝相依套件、執行全部測試。只用 pip install -r requirements.txt，不要執行 pip install -e .（測試設定已包含 src 路徑）：
   py -3.13 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   .venv\Scripts\python.exe -m pytest -q
2. 用白話告訴我：測試最後一行是什麼（成功應為 76 passed，沒有 warning）、有沒有 failed 或 error。
3. 建立 notes/opening.md，寫入標題「檢查點 1 · 安裝相依套件與測試」、Repo 的完整路徑、pytest 最後一行原文、遇到的問題與處理（沒有就寫「沒有」）。
做完停下等我。
# macos
請準備起始 Repo 的執行環境，不要修改任何程式：
1. 在 Repo 根目錄建立 venv、安裝相依套件、執行全部測試。只用 pip install -r requirements.txt，不要執行 pip install -e .（測試設定已包含 src 路徑）：
   python3.13 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python -m pytest -q
2. 用白話告訴我：測試最後一行是什麼（成功應為 76 passed，沒有 warning）、有沒有 failed 或 error。
3. 建立 notes/opening.md，寫入標題「檢查點 1 · 安裝相依套件與測試」、Repo 的完整路徑、pytest 最後一行原文、遇到的問題與處理（沒有就寫「沒有」）。
做完停下等我。
```

③ 確認結果

```prompt
# windows
請只檢查，不要修改任何檔案：
1. 用 .venv 裡的 python 執行 pytest -q，最後一行是 76 passed，沒有 warning、failed 或 error。
2. Repo 的完整路徑在 C:\dlc\ 底下。
3. notes/opening.md 有「檢查點 1 · 安裝相依套件與測試」。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
# macos
請只檢查，不要修改任何檔案：
1. 用 .venv 裡的 python 執行 pytest -q，最後一行是 76 passed，沒有 warning、failed 或 error。
2. Repo 的完整路徑在 ~/dlc/ 底下。
3. notes/opening.md 有「檢查點 1 · 安裝相依套件與測試」。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請先不要修改任何檔案。用白話解釋剛才的錯誤訊息：是 Python 版本、網路／pip 來源，還是資料夾位置的問題？列出你建議的處理方式，等我同意再做。
```

④ 補充

```callout warning
Windows 一定要解壓到 C:\dlc
放在桌面、OneDrive 或深層資料夾，D1 會出現「檔名或副檔名太長」（WinError 206）。
```

## 檢查點 2 · 解出 Plugin 並核對 SHA256（第 3–5 分鐘）

① 為什麼做這一步

今天的各種檢查都由 domain-memory Plugin 判定，所以 Plugin 必須原樣使用：檔案被改過，結果就不可信。

② 貼給 Agent

```prompt
# windows
請解出 domain-memory Plugin 並逐檔核對 SHA256，不要修改 Plugin 的任何檔案：
1. 到學員包的 vendor 資料夾解出 Plugin、逐檔核對清單、顯示版本，再回到 Repo 根目錄：
PowerShell：
  Set-Location ..\..\vendor
  Expand-Archive -LiteralPath .\domain-memory-0.10.15.zip -DestinationPath .
  py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.10.15.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  Select-String '"version"' .\domain-memory\.claude-plugin\plugin.json
  Set-Location ..\repository\smart-ticket-dlc-base
Git Bash：
  cd ../../vendor
  unzip -q domain-memory-0.10.15.zip
  py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.10.15.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  grep '"version"' domain-memory/.claude-plugin/plugin.json
  cd ../repository/smart-ticket-dlc-base
2. 用白話告訴我核對結果與版本。如果出現 SHA MISMATCH，立刻停下，不要使用這份 Plugin，也不要嘗試修正。
3. 在 notes/opening.md 加上標題「檢查點 2 · Plugin 完整性」，寫入核對輸出與版本原文。
做完停下等我。
# macos
請解出 domain-memory Plugin 並逐檔核對 SHA256，不要修改 Plugin 的任何檔案：
1. 到學員包的 vendor 資料夾解出 Plugin、逐檔核對清單、顯示版本，再回到 Repo 根目錄：
  cd ../../vendor
  unzip -q domain-memory-0.10.15.zip
  python3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.10.15.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  grep '"version"' domain-memory/.claude-plugin/plugin.json
  cd ../repository/smart-ticket-dlc-base
2. 用白話告訴我核對結果與版本。如果出現 SHA MISMATCH，立刻停下，不要使用這份 Plugin，也不要嘗試修正。
3. 在 notes/opening.md 加上標題「檢查點 2 · Plugin 完整性」，寫入核對輸出與版本原文。
做完停下等我。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. notes/opening.md 的「檢查點 2 · Plugin 完整性」記著 SHA OK 71 files，沒有 SHA MISMATCH。
2. 學員包 vendor/domain-memory/.claude-plugin/plugin.json 的版本是 "version": "0.10.15"。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時（出現 SHA MISMATCH 就停下，請主持人協助）：

```text
請不要修改 Plugin 的任何檔案。用白話說明是哪一步沒有成功：找不到 zip、解壓縮失敗、核對不符，還是版本不對？列出不符的檔案，等我和主持人決定。
```

④ 補充

```callout info
新概念：SHA256 雜湊
雜湊是由檔案內容算出的一串字，像檔案的指紋：內容改一個位元組就完全不同。Agent 逐檔重算並和清單比對，全部相同才印 `SHA OK`。
📖 延伸閱讀：NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉。
```

## 檢查點 3 · 專案就緒與品質關卡檢查（第 5–8 分鐘）

① 為什麼做這一步

兩個唯讀檢查：`readiness` 判斷 Repo 狀態，`quality-gates` 列出 Repo 已有哪些自動檢查。沒有的檢查，之後只能靠測試和人的審查補上。

② 貼給 Agent

```prompt
# windows
請用 dm 腳本執行兩個唯讀檢查，不要修改任何檔案：
  Set-ExecutionPolicy -Scope Process Bypass -Force
  ..\..\tools\dm.ps1 readiness
  ..\..\tools\dm.ps1 quality-gates
然後用白話告訴我：
1. readiness 的 state 與 confidence 是什麼？
2. quality-gates 找到哪些檢查？有沒有 lint（程式風格檢查）、型別或架構檢查？
3. 這代表你之後改程式時，哪些問題只能靠測試和人的審查才抓得到？
在 notes/opening.md 加上標題「檢查點 3 · 專案就緒與品質關卡」，寫入上面三題的答案與關鍵輸出原文。做完停下等我。
# macos
請用 dm 腳本執行兩個唯讀檢查，不要修改任何檔案：
  chmod +x ../../tools/dm.sh   # 解壓縮後沒有執行權限；只開權限，不改內容
  source .venv/bin/activate && ../../tools/dm.sh readiness && ../../tools/dm.sh quality-gates
然後用白話告訴我：
1. readiness 的 state 與 confidence 是什麼？
2. quality-gates 找到哪些檢查？有沒有 lint（程式風格檢查）、型別或架構檢查？
3. 這代表你之後改程式時，哪些問題只能靠測試和人的審查才抓得到？
在 notes/opening.md 加上標題「檢查點 3 · 專案就緒與品質關卡」，寫入上面三題的答案與關鍵輸出原文。做完停下等我。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. notes/opening.md 的「檢查點 3 · 專案就緒與品質關卡」記著 readiness 為 "state": "brownfield"、"confidence": "high"。
2. 同一段記著 quality-gates 只有一項 "tool": "pytest"、"standard": "none"。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請不要修改任何檔案。用白話解釋 readiness 或 quality-gates 的輸出和預期哪裡不同，可能的原因是什麼，列出建議的下一步，等我同意。
```

④ 補充

`readiness` 的 brownfield 指已有程式碼的既有專案。`quality-gates` 只有 pytest、沒有 lint、型別或架構檢查，這是事實，不是錯誤。

## 檢查點 4 · 確認真實 Python（第 8–10 分鐘）

① 為什麼做這一步

D2 推送（push）時 Git 會直接呼叫 `python`。
- Windows 教室電腦上的 `python` 常是 Microsoft Store 的別名（路徑含 `WindowsApps`），會讓 push 失敗。
- 這一步也建立起始 commit。

② 貼給 Agent

```prompt
# windows
請確認真實 Python、建立起始 commit，並執行環境健檢：
1. 在同一個指令裡啟用 venv 並確認 python 的版本與路徑：
   PowerShell：.\.venv\Scripts\Activate.ps1; python --version; (Get-Command python).Source
   Git Bash：source .venv/Scripts/activate && python --version && command -v python
2. 執行環境健檢（它會檢查 PATH 上的 python，所以同一個指令裡要先啟用 venv）：
   PowerShell：.\.venv\Scripts\Activate.ps1; py -3.13 -X utf8 ..\..\tools\doctor.py
   Git Bash：source .venv/Scripts/activate && py -3.13 -X utf8 ../../tools/doctor.py
3. 在 notes/opening.md 加上標題「檢查點 4 · 真實 Python 與環境健檢」，寫入 python 版本與路徑原文、doctor.py 的最後一行，以及有沒有 [!!]（[--] 只是提醒）。這份紀錄要在下一步 commit 之前寫完。
4. 建立起始 commit（這時還沒有 domain-memory/，所以不需要簽章）。Git 使用者只設在本 Repo，不要用 --global：
   git init
   git config --local user.name "DLC Proposer"
   git config --local user.email proposer@example.com
   git add -A
   git commit -m "起始 Repo"
5. 用白話告訴我：python 是不是 3.13.x、路徑是否在 smart-ticket-dlc-base 的 .venv\Scripts 底下且不含 WindowsApps；doctor.py 的最後一行、有沒有 [!!]；起始 commit 是否建立、裡面有沒有 domain-memory/；commit 後 git status --short 是不是空的。不要再改 notes/opening.md。
做完停下等我。
# macos
請確認真實 Python、建立起始 commit，並執行環境健檢：
1. 在同一個指令裡啟用 venv 並確認 python 的版本與路徑：
   source .venv/bin/activate && python --version && command -v python
2. 執行環境健檢（它會檢查 PATH 上的 python，所以同一個指令裡要先啟用 venv）：
   source .venv/bin/activate && python -X utf8 ../../tools/doctor.py
3. 在 notes/opening.md 加上標題「檢查點 4 · 真實 Python 與環境健檢」，寫入 python 版本與路徑原文、doctor.py 的最後一行，以及有沒有 [!!]（[--] 只是提醒）。這份紀錄要在下一步 commit 之前寫完。
4. 建立起始 commit（這時還沒有 domain-memory/，所以不需要簽章）。Git 使用者只設在本 Repo，不要用 --global：
   git init
   git config --local user.name "DLC Proposer"
   git config --local user.email proposer@example.com
   git add -A
   git commit -m "起始 Repo"
5. 用白話告訴我：python 是不是 3.13.x、路徑是否在 smart-ticket-dlc-base 的 .venv/bin 底下；doctor.py 的最後一行、有沒有 [!!]；起始 commit 是否建立、裡面有沒有 domain-memory/；commit 後 git status --short 是不是空的。不要再改 notes/opening.md。
做完停下等我。
```

③ 確認結果

```prompt
# windows
請只檢查，不要修改任何檔案：
1. 啟用 .venv 後的 python 是 3.13.x，路徑在 smart-ticket-dlc-base 的 .venv\Scripts 底下，不含 WindowsApps。
2. notes/opening.md 記著 doctor.py 最後一行「全部必要項目通過。」，沒有 [!!]。
3. 起始 commit 已建立、裡面沒有 domain-memory/，git status --short 是空的。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
# macos
請只檢查，不要修改任何檔案：
1. 啟用 .venv 後的 python 是 3.13.x，路徑在 smart-ticket-dlc-base 的 .venv/bin 底下。
2. notes/opening.md 記著 doctor.py 最後一行「全部必要項目通過。」，沒有 [!!]。
3. 起始 commit 已建立、裡面沒有 domain-memory/，git status --short 是空的。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請不要修改程式。用白話解釋 doctor.py 每一個 [!!] 項目或 python 路徑不對的原因，以及它建議的修正方式；只列出來，等我同意再做。
```

④ 補充

```callout danger
第 10 分鐘仍未通過
不要在活動中更換 Python 版本或工具。告知主持人，從 D1 起先和夥伴共用一台已通過的機器。
```

第 7 分鐘主持人會請你找一位夥伴，D2 起兩人一組。
