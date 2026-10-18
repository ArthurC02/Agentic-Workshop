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
- **情境**：你接手 Smart Ticket 的訂票後端，今天要和 Agent 一起替它建立團隊共用的領域模型。
- **你的目標**：10 分鐘內讓 Agent 備好環境：測試全過、模型工具可信，並找出哪些錯只能靠人審查。
- **今天的技巧**：先講好「看到什麼算成功」，Agent 的回報對得上才往下。
- **完成的樣子**：`notes/opening.md` 有四個檢查點的結果；起始版本（起始 commit）已建立。
```

## 前置需求

- Python **3.13**：Windows 要有 `py` 啟動器；macOS 要有 `python3.13`。
- Git 2.34 以上（Windows 是 Git for Windows）。
- macOS 用 Safari 下載的人：到 Safari › 設定 › 一般，取消「下載後打開『安全』的檔案」，或改用 Chrome。
- 一個能讀寫本機資料夾、執行終端機指令的 Coding Agent（主課用過的即可）。

## 檢查點 1 · 確認起點：測試全部通過（第 0–3 分鐘）

① 為什麼做這一步

今天每個設計決定最後都要用測試證明，所以先確認起點：起始 Repo 的測試全部通過。開始前先做這三件事：

```download
id=participant-dlc-open zip=participant-dlc-open.zip label=下載學員包（起始 Repo、輔助工具、domain-memory Plugin）
```

- [ ] 按上方按鈕下載 `participant-dlc-open.zip`，解壓縮到你習慣的位置（例如下載資料夾）：Windows 在檔案上按右鍵選「全部解壓縮」；macOS 按兩下 zip
- [ ] 用 Agent 開啟解出來的 `participant-dlc-open` › `repository` › `smart-ticket-dlc-base` 資料夾（Repo 根目錄）
- [ ] 把下方兩段提示詞接在一起，一次貼給 Agent

② 貼給 Agent

先複製工作規則，再把本檢查點的提示詞接在後面，一起送出（中間不用等 Agent 回覆）。工作規則整場只貼一次，開新的 Agent 對話時才再貼。這段是給 Agent 的，不需要看懂：

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
請回覆「了解」；這段後面如果接著有指示，就直接開始做，否則等我的下一個指示。
# macos
以下是今天這堂延伸課程的工作規則，請在整段對話中遵守：
1. 你負責所有指令操作與檔案編輯；我不自己打指令、不讀程式。每次做完用白話告訴我結果，並引用關鍵的實際輸出字樣（例如「76 passed」「Registry is valid.」），不要只貼原始輸出。
2. 每一步做完就停下等我。需要我決定的地方，先列出選項或草稿，每項附證據（路徑:起-迄，行號要實際打開檔案核對），然後等我回覆「同意」或「改成…」。
3. 除非我另外說明，所有指令都在目前的 Repo 根目錄（你開啟 Agent 的資料夾，例如 smart-ticket-dlc-base；改用 Recovery 時是 resume- 開頭的資料夾）執行。不要直接執行 registry_tools.py，也不要手動修改 domain-memory/ 底下的檔案。
4. 這台是 macOS：Plugin 一律經 ../../tools/dm.sh（它會自己找 python3.13）。若出現 permission denied，先在 Repo 根目錄執行一次 chmod +x ../../tools/dm.sh 再重跑。
5. 你的每個指令可能在新的終端機程序執行，啟用過的 venv 不會延續：需要 python 時直接用 .venv/bin/python，或在同一個指令裡先 source .venv/bin/activate。
6. 你或我新增到 Domain Memory 的內容一律是候選（candidate），不要寫成「已確認」，也不要當成限制。
7. 沒有我的指示，不要 git commit 或 git push；不要讀取、複製或顯示任何私鑰檔。
8. 你沒有實際執行的事情，一律標「未驗證」。
請回覆「了解」；這段後面如果接著有指示，就直接開始做，否則等我的下一個指示。
```

接在後面的本檢查點提示詞：

```prompt
# windows
請準備起始 Repo 的執行環境，不要修改任何程式：
1. 在 Repo 根目錄建立 venv、安裝相依套件、執行全部測試。只用 pip install -r requirements.txt，不要執行 pip install -e .（測試設定已包含 src 路徑）：
   py -3.13 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   .venv\Scripts\python.exe -m pytest -q
2. 用白話告訴我：測試最後一行是什麼（成功應為 76 passed，沒有 warning）、有沒有 failed 或 error。
3. 建立 notes/opening.md，寫入標題「檢查點 1 · 安裝相依套件與測試」、pytest 最後一行原文、遇到的問題與處理（沒有就寫「沒有」）。
4. 最後只檢查、不修改：pytest 最後一行是 76 passed，沒有 warning、failed 或 error；notes/opening.md 有「檢查點 1 · 安裝相依套件與測試」。全部符合在最後一行只寫「成功」，否則寫「失敗：」加一句原因。
做完停下等我。
# macos
請準備起始 Repo 的執行環境，不要修改任何程式：
1. 在 Repo 根目錄建立 venv、安裝相依套件、執行全部測試。只用 pip install -r requirements.txt，不要執行 pip install -e .（測試設定已包含 src 路徑）：
   python3.13 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python -m pytest -q
2. 用白話告訴我：測試最後一行是什麼（成功應為 76 passed，沒有 warning）、有沒有 failed 或 error。
3. 建立 notes/opening.md，寫入標題「檢查點 1 · 安裝相依套件與測試」、pytest 最後一行原文、遇到的問題與處理（沒有就寫「沒有」）。
4. 最後只檢查、不修改：pytest 最後一行是 76 passed，沒有 warning、failed 或 error；notes/opening.md 有「檢查點 1 · 安裝相依套件與測試」。全部符合在最後一行只寫「成功」，否則寫「失敗：」加一句原因。
做完停下等我。
```

Agent 安裝套件約要一分鐘，趁這時先讀檢查點 2 的 ①。

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
請只檢查，不要修改任何檔案：
1. 用 .venv 裡的 python 執行 pytest -q，最後一行是 76 passed，沒有 warning、failed 或 error。
2. notes/opening.md 有「檢查點 1 · 安裝相依套件與測試」。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時：

```text
請先不要修改任何檔案。用白話解釋剛才的錯誤訊息：是 Python 版本，還是網路／pip 來源的問題？列出你建議的處理方式，等我同意再做。
```

## 檢查點 2 · 備好可信的共用模型工具（第 3–5 分鐘）

① 為什麼做這一步

今天的共用模型由 domain-memory 工具保存，之後每個 Agent 都照它做事，所以工具本身要可信。Agent 逐檔核對工具的指紋，全部相符才使用；你只看 ③ 是否成功。

② 貼給 Agent

```prompt
# windows
請解出 domain-memory Plugin 並逐檔核對 SHA256，不要修改 Plugin 的任何檔案：
1. 到學員包的 vendor 資料夾解出 Plugin、逐檔核對清單、顯示版本，再回到 Repo 根目錄：
PowerShell：
  Set-Location ..\..\vendor
  Expand-Archive -LiteralPath .\domain-memory-1.2.8.zip -DestinationPath .
  py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-1.2.8.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  Select-String '"version"' .\domain-memory\.claude-plugin\plugin.json
  Set-Location ..\repository\smart-ticket-dlc-base
Git Bash：
  cd ../../vendor
  unzip -qo domain-memory-1.2.8.zip
  py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-1.2.8.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  grep '"version"' domain-memory/.claude-plugin/plugin.json
  cd ../repository/smart-ticket-dlc-base
2. 用白話告訴我核對結果與版本。如果出現 SHA MISMATCH，立刻停下，不要使用這份 Plugin，也不要嘗試修正。
3. 在 notes/opening.md 加上標題「檢查點 2 · Plugin 完整性」，寫入核對輸出與版本原文。
做完停下等我。
# macos
請解出 domain-memory Plugin 並逐檔核對 SHA256，不要修改 Plugin 的任何檔案：
1. 到學員包的 vendor 資料夾解出 Plugin、逐檔核對清單、顯示版本，再回到 Repo 根目錄：
  cd ../../vendor
  unzip -qo domain-memory-1.2.8.zip
  python3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-1.2.8.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
  grep '"version"' domain-memory/.claude-plugin/plugin.json
  cd ../repository/smart-ticket-dlc-base
2. 用白話告訴我核對結果與版本。如果出現 SHA MISMATCH，立刻停下，不要使用這份 Plugin，也不要嘗試修正。
3. 在 notes/opening.md 加上標題「檢查點 2 · Plugin 完整性」，寫入核對輸出與版本原文。
做完停下等我。
```

③ 確認結果

```text
請只檢查，不要修改任何檔案：
1. notes/opening.md 的「檢查點 2 · Plugin 完整性」記著 SHA OK 95 files，沒有 SHA MISMATCH。
2. 學員包 vendor/domain-memory/.claude-plugin/plugin.json 的版本是 "version": "1.2.8"。
全部符合只回「成功」，否則只回「失敗：」加一句原因。
```

失敗時（出現 SHA MISMATCH 就停下，請主持人協助）：

```text
請不要修改 Plugin 的任何檔案。用白話說明是哪一步沒有成功：找不到 zip、解壓縮失敗、核對不符，還是版本不對？列出不符的檔案，等我和主持人決定。
```

## 檢查點 3 · 找出只能靠人審查的錯（第 5–8 分鐘）

① 為什麼做這一步

Agent 用兩個只讀不改的檢查看這個 Repo：它是已有程式的既有專案，自動檢查只有測試，沒有架構檢查。所以程式有沒有越界，例如計價程式直接改會員資料，只能靠人審查；D3 每次變更都會回來問這一題。

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
  ../../tools/dm.sh readiness && ../../tools/dm.sh quality-gates
若出現 permission denied，先執行 chmod +x ../../tools/dm.sh（只開執行權限，不改內容）再重跑。
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

## 檢查點 4 · 確認環境並建立起始版本（第 8–10 分鐘）

① 為什麼做這一步

Agent 確認用的是真正的 Python 3.13，並建立起始版本（起始 commit），之後每次變更都能和它比對。D2 起，共用模型每次推送前都會自動檢查有沒有核准，這項檢查要用到正確的 Python。

② 貼給 Agent

```prompt
# windows
請確認真實 Python、建立 Git Repo、執行環境健檢，再建立起始 commit：
1. 在同一個指令裡啟用 venv 並確認 python 的版本與路徑：
   PowerShell：.\.venv\Scripts\Activate.ps1; python --version; (Get-Command python).Source
   Git Bash：source .venv/Scripts/activate && python --version && command -v python
2. 建立 Git Repo，Git 使用者只設在本 Repo，不要用 --global；這時先不要 commit：
   git init -b main
   git config --local user.name "DLC Proposer"
   git config --local user.email proposer@example.com
3. 執行環境健檢（它會檢查 PATH 上的 python 與本 Repo 的 Git 設定，所以在 git init 之後執行，同一個指令裡先啟用 venv）：
   PowerShell：.\.venv\Scripts\Activate.ps1; py -3.13 -X utf8 ..\..\tools\doctor.py
   Git Bash：source .venv/Scripts/activate && py -3.13 -X utf8 ../../tools/doctor.py
4. 在 notes/opening.md 加上標題「檢查點 4 · 真實 Python 與環境健檢」，寫入 python 版本與路徑原文、doctor.py 的最後一行，以及有沒有 [!!]（[--] 只是提醒）。這份紀錄要在下一步 commit 之前寫完。
5. 建立起始 commit（這時還沒有 domain-memory/，所以不需要簽章）：
   git add -A
   git commit -m "起始 Repo"
6. 用白話告訴我：python 是不是 3.13.x、路徑是否在 smart-ticket-dlc-base 的 .venv\Scripts 底下且不含 WindowsApps；doctor.py 的最後一行、有沒有 [!!]；起始 commit 是否建立、裡面有沒有 domain-memory/；commit 後 git status --short 是不是空的。不要再改 notes/opening.md。
最後一行只寫「成功」（python 是 3.13.x 且路徑正確、doctor.py 最後一行是「全部必要項目通過。」且沒有 [!!]、起始 commit 已建立且沒有 domain-memory/、git status --short 是空的），否則寫「失敗：」加一句原因。
做完停下等我。
# macos
請確認真實 Python、建立 Git Repo、執行環境健檢，再建立起始 commit：
1. 在同一個指令裡啟用 venv 並確認 python 的版本與路徑：
   source .venv/bin/activate && python --version && command -v python
2. 建立 Git Repo，Git 使用者只設在本 Repo，不要用 --global；這時先不要 commit：
   git init -b main
   git config --local user.name "DLC Proposer"
   git config --local user.email proposer@example.com
3. 執行環境健檢（它會檢查 PATH 上的 python 與本 Repo 的 Git 設定，所以在 git init 之後執行，同一個指令裡先啟用 venv）：
   source .venv/bin/activate && python -X utf8 ../../tools/doctor.py
4. 在 notes/opening.md 加上標題「檢查點 4 · 真實 Python 與環境健檢」，寫入 python 版本與路徑原文、doctor.py 的最後一行，以及有沒有 [!!]（[--] 只是提醒）。這份紀錄要在下一步 commit 之前寫完。
5. 建立起始 commit（這時還沒有 domain-memory/，所以不需要簽章）：
   git add -A
   git commit -m "起始 Repo"
6. 用白話告訴我：python 是不是 3.13.x、路徑是否在 smart-ticket-dlc-base 的 .venv/bin 底下；doctor.py 的最後一行、有沒有 [!!]；起始 commit 是否建立、裡面有沒有 domain-memory/；commit 後 git status --short 是不是空的。不要再改 notes/opening.md。
最後一行只寫「成功」（python 是 3.13.x 且路徑正確、doctor.py 最後一行是「全部必要項目通過。」且沒有 [!!]、起始 commit 已建立且沒有 domain-memory/、git status --short 是空的），否則寫「失敗：」加一句原因。
做完停下等我。
```

等 Agent 時，還沒有 D2 夥伴的先找好（見本頁最後的「⏸ 看投影」）。

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

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

```callout sync
⏸ 看投影：第 8 分鐘找好 D2 夥伴，D2 起兩人一組
```
