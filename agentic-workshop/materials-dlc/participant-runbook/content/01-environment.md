---
id: environment
title: 開場與環境
minute: 00-10
group: dlc-opening
section: 開始之前
---

# 開場與環境

10 分鐘內把環境備好：起始 Repo 測試全綠、Plugin 原樣解出並核對 SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同）、Plugin 認得這是 brownfield（已有程式碼的既有專案）、終端機用的是真正的 Python。每個檢查點都附「看到什麼算成功」，要看到才往下。

## 檢查點總覽

| 檢查點 | 全場分鐘 | 你要完成的事 |
|---|---:|---|
| 1 · 依賴安裝與測試 | 0–3 | 下載學員包、解壓到短路徑、建 venv（Python 虛擬環境）、安裝依賴、測試全綠 |
| 2 · 解出 Plugin 並核對 SHA256 | 3–5 | 解出 Plugin 0.2.2，每個檔案的 SHA256 與清單一致 |
| 3 · 專案就緒與品質關卡檢查 | 5–8 | Plugin 判定 brownfield，並找到 pytest |
| 4 · 確認真實 Python | 8–10 | 啟用 venv、建立起始 commit、`doctor.py` 全部通過 |

## 前置需求

- [ ] Windows 上的 Python **3.13**，而且有 `py` launcher（`py -3.13 --version` 有回應）。
- [ ] Git for Windows 2.34 以上（SSH 簽章需要）；bash 分頁使用 Git Bash。
- [ ] 一個可讀寫本機資料夾、能執行終端指令的 Coding Agent（主課用過的那一個即可）。
- [ ] 主課的經驗：知道怎麼要求 Agent 先提計畫、分段做、停下等你。

```download
id=participant-dlc-open zip=participant-dlc-open.zip label=下載學員包（起始 Repo、輔助工具、domain-memory Plugin）
```

學員包內容：`repository/smart-ticket-dlc-base/`（起始 Repo）、`tools/`（`dm.ps1`、`dm.sh` 與輔助腳本）、`vendor/`（Plugin ZIP 與 SHA256 清單）。之後所有 Plugin 指令都在 Repo 根目錄經 `tools/dm.ps1` 或 `tools/dm.sh` 執行；它們固定用 `py -3.13 -X utf8` 執行 Plugin，並自動補上 Registry 與 Repo 的路徑參數。

## 檢查點 1 · 依賴安裝與測試（第 0–3 分鐘）

- [ ] 按上方按鈕下載 `participant-dlc-open.zip`（存到「下載」資料夾）。
- [ ] 解壓到 `C:\dlc`，進入起始 Repo，建 venv 並安裝依賴（約 50 秒），再跑全部測試：

```cmd
# powershell
Expand-Archive -LiteralPath "$HOME\Downloads\participant-dlc-open.zip" -DestinationPath C:\dlc
Set-Location C:\dlc\agentic-workshop\07-dlc-ddd\participant\repository\smart-ticket-dlc-base
py -3.13 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pytest -q
# bash
unzip -q ~/Downloads/participant-dlc-open.zip -d /c/dlc
cd /c/dlc/agentic-workshop/07-dlc-ddd/participant/repository/smart-ticket-dlc-base
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
```

**看到什麼算成功**：最後一行是 `76 passed`（可能附帶 `1 warning`），沒有 `failed` 或 `error`。

```callout warning
一定要解壓到 C:\dlc 這種短路徑
Plugin 更新 Registry 時會在 `domain-memory/` 底下建立很長的暫存資料夾名稱。放在桌面、OneDrive 或深層資料夾，會在 D1 出現「檔名或副檔名太長」（WinError 206）。不要放在同步資料夾。
```

```callout tip
不需要 pip install -e .
本 Repo 只用 `pip install -r requirements.txt` 安裝；測試設定已包含 `src` 路徑。不要執行 `pip install -e .`。
```

```form
{"id": "env-cp1", "title": "檢查點 1 確認：依賴與測試","fields":[
{"id": "repo-path", "label": "起始 Repo 的完整路徑", "type": "text", "suggestions": ["C:\\dlc\\agentic-workshop\\07-dlc-ddd\\participant\\repository\\smart-ticket-dlc-base", {"label": "其他路徑", "text": "〈路徑〉（原因：〈 〉）"}]},
{"id": "pytest", "label": "pytest -q 最後一行（實際輸出）", "type": "text", "suggestions": [{"label": "實際輸出", "text": "〈 〉 passed，〈 〉 failed"}]},
{"id": "issues", "label": "遇到的問題與處理", "type": "textarea", "hint": "沒有就寫「沒有」。", "suggestions": ["沒有", {"label": "問題範本", "text": "問題：〈錯誤訊息〉\n處理：〈做了什麼〉\n結果：〈 〉"}]}
]}
```

## 檢查點 2 · 解出 Plugin 並核對 SHA256（第 3–5 分鐘）

Plugin 必須**原樣**使用：今天的 Registry 規則、簽章驗證與 counterfactual 都由它判定，任何一個位元組被改過，結果就不可信。

- [ ] 在 `vendor/` 解出 Plugin，逐檔核對 SHA256 清單，並確認版本，再回到 Repo 根目錄：

```cmd
# powershell
Set-Location ..\..\vendor
Expand-Archive -LiteralPath .\domain-memory-0.2.2.zip -DestinationPath .
py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.2.2.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
Select-String '"version"' .\domain-memory\.claude-plugin\plugin.json
Set-Location ..\repository\smart-ticket-dlc-base
# bash
cd ../../vendor
unzip -q domain-memory-0.2.2.zip
py -3.13 -c "import hashlib,pathlib;s=[l.split('  ',1) for l in pathlib.Path('domain-memory-0.2.2.zip.SHA256SUMS').read_text(encoding='utf-8').splitlines() if l.strip()];bad=[p for h,p in s if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h];print('SHA OK', len(s), 'files') if not bad else print('SHA MISMATCH', bad)"
grep '"version"' domain-memory/.claude-plugin/plugin.json
cd ../repository/smart-ticket-dlc-base
```

**看到什麼算成功**：`SHA OK 130 files`（129 個 Plugin 檔案加 ZIP 本身），以及 `"version": "0.2.2"`。出現 `SHA MISMATCH` 就停下，不要使用這份 Plugin，請主持人協助。

```form
{"id": "env-cp2", "title": "檢查點 2 確認：Plugin 完整性","fields":[
{"id": "sha", "label": "SHA 核對輸出", "type": "text", "suggestions": ["SHA OK 130 files", {"label": "不一致", "text": "SHA MISMATCH：〈檔案〉"}]},
{"id": "version", "label": "plugin.json 版本", "type": "text", "suggestions": ["0.2.2"]}
]}
```

## 檢查點 3 · 專案就緒與品質關卡檢查（第 5–8 分鐘）

`readiness` 只觀察檔案系統，告訴你這個 Repo 處於什麼狀態；`quality-gates` 列出 Repo 自己已有的檢查。兩者都是唯讀。

- [ ] 在 Repo 根目錄執行（PowerShell 每開一個新視窗，都要先執行第一行，允許本視窗執行 `dm.ps1`）：

```cmd
# powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
..\..\tools\dm.ps1 readiness
..\..\tools\dm.ps1 quality-gates
# bash
../../tools/dm.sh readiness
../../tools/dm.sh quality-gates
```

**看到什麼算成功**：`readiness` 輸出 `"state": "brownfield"`、`"confidence": "high"`；`quality-gates` 的 `gates` 只有一項 `"tool": "pytest"`，`"standard": "none"`（沒有 lint、型別或架構檢查，這是事實，不是錯誤）。每次執行前，`dm` 會先印一行 `[dm] registry_tools.py ...`，讓你看到實際送給 Plugin 的完整指令。

```callout info
為什麼一定要經過 dm.ps1／dm.sh
繁體中文 Windows 的預設編碼是 cp950（不是 UTF-8）。Plugin 讀寫的 JSON 與文件含中文，少了 `-X utf8` 會出現 `UnicodeDecodeError`。`dm` 已固定 `py -3.13 -X utf8`；不要直接用 `python registry_tools.py` 執行 Plugin。
```

```form
{"id": "env-cp3", "title": "檢查點 3 確認：專案就緒與品質關卡檢查","fields":[
{"id": "readiness", "label": "readiness 的 state／confidence", "type": "text", "suggestions": ["brownfield／high", {"label": "其他", "text": "〈state〉／〈confidence〉"}]},
{"id": "gates", "label": "quality-gates 找到的檢查", "type": "text", "suggestions": ["只有 pytest（pyproject.toml），standard: none", {"label": "其他", "text": "〈 〉"}]},
{"id": "note", "label": "這代表 Agent 改程式時，哪些檢查只能靠我們自己？", "type": "textarea", "suggestions": [{"label": "回答範本", "text": "沒有〈lint／型別／架構〉檢查，所以〈 〉要靠人審查與測試"}]}
]}
```

## 檢查點 4 · 確認真實 Python（第 8–10 分鐘）

D2 推送（push）時，pre-push hook（push 前 Git 自動執行的檢查腳本）會直接呼叫 `python`。教室電腦上的 `python` 常常是 Microsoft Store 的別名（路徑含 `WindowsApps`），會讓 push 失敗。啟用 Repo 的 venv 後，`python` 就是 venv 裡的真實直譯器。

- [ ] 啟用 venv、確認 `python` 的路徑，建立起始 commit（這時還沒有 `domain-memory/`，所以這個 commit 不需要簽章），再執行環境健檢：

```cmd
# powershell
.\.venv\Scripts\Activate.ps1
python --version
(Get-Command python).Source
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git commit -m "起始 Repo"
py -3.13 -X utf8 ..\..\tools\doctor.py
# bash
source .venv/Scripts/activate
python --version
command -v python
git init
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git add -A
git commit -m "起始 Repo"
py -3.13 -X utf8 ../../tools/doctor.py
```

**看到什麼算成功**：`python --version` 為 `Python 3.13.x`；`python` 的路徑在 `smart-ticket-dlc-base\.venv\Scripts\` 底下，**不含** `WindowsApps`；`doctor.py` 每一項都是 `[OK]`（`[--]` 是提醒），最後一行為「全部必要項目通過。」。

```callout warning
每開一個新終端機都要重新啟用 venv
`Activate.ps1`／`activate` 只對目前這個視窗有效。之後開新視窗時，先 `Set-Location`／`cd` 到 Repo 根目錄，PowerShell 再執行 `Set-ExecutionPolicy -Scope Process Bypass -Force` 與 `.\.venv\Scripts\Activate.ps1`；Git Bash 執行 `source .venv/Scripts/activate`。
```

```callout tip
為什麼 Git 使用者都叫 DLC Proposer
DLC 指這堂延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課）。今天只在本機練習，每個人先以 `proposer@example.com` 身分工作；D2 時夥伴會以 `maintainer@example.com` 身分核准與簽章。這兩個字串會出現在稽核紀錄裡，讓你看清楚「誰做了什麼」。只改本 Repo 的設定（`--local`），不要改全域 Git 設定。
```

```form
{"id": "env-cp4", "title": "檢查點 4 確認：真實 Python 與環境健檢","fields":[
{"id": "python", "label": "python --version 與路徑", "type": "textarea", "suggestions": [{"label": "實際輸出", "text": "Python 3.13.〈 〉\n〈路徑〉"}]},
{"id": "doctor", "label": "doctor.py 結果", "type": "text", "suggestions": ["全部必要項目通過。", {"label": "有項目未過", "text": "[!!] 〈項目〉：〈處理方式〉"}]},
{"id": "check", "label": "已確認", "type": "checklist", "items": ["python 路徑在 .venv 內，不含 WindowsApps", "已建立起始 commit，且尚未有 domain-memory/", "Git 使用者為 DLC Proposer <proposer@example.com>（只設在本 Repo）", "我知道新開終端機要重新啟用 venv"], "hint": "只勾實際確認過的項目。"}
]}
```

```callout danger
第 10 分鐘仍未通過
不要在活動中更換 Python 版本或改用其他語言或工具。告知主持人，D1 起先和夥伴共用一台已通過的機器，同時記下卡在哪一步。
```
