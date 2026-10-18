# 延伸課程輔助工具

本資料夾是延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課）的輔助腳本，讓時間花在領域決策，而不是手打 JSON。腳本只用 Python 標準函式庫，代你呼叫 domain-memory Plugin（課程提供的命令列工具），不修改 Plugin。

**所有指令都在 Repo 根目錄（`smart-ticket-dlc-base/`）執行。** 下面以 `../../tools/` 表示本資料夾。

| 檔案 | 用途 |
|---|---|
| `dm.ps1`、`dm.sh` | 代打 Plugin 長指令：自動用 Python 3.13、UTF-8 編碼執行（Windows `py -3.13 -X utf8`，macOS `python3.13 -X utf8`），並補上 `--registry-root domain-memory` 與 `--repo-root .`；`--save 檔案` 以 UTF-8 存輸出 |
| `make_record.py` | 由 id、名稱、定義與 `路徑:起-迄` 呼叫 Plugin 的 `cite` 指令，寫出完整的紀錄 JSON；`--upsert` 直接登記為候選；`--batch` 一次多筆（同一種資產一起登記：全部成功或全部不登記） |
| `fill_package.py` | 由一份精簡描述 JSON 建立並填寫 Change Package；測試**實際執行**，記錄真實 exit code 與輸出的 SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同） |
| `setup_remote.py` | 在本機建立一個模擬的遠端儲存庫（bare remote）並設為 `origin`，讓 pre-push hook（push 前 Git 自動執行的檢查腳本）有地方 push |
| `doctor.py` | 檢查 Windows／macOS 常見的環境問題（Python 版本、編碼、Git、ssh-keygen 等），依作業系統列出修正方式 |
| `dmlib.py` | `dm.ps1`、`dm.sh` 共用的 Python 程式 |
| `test_tools.py` | 自檢：`py -3.13 -X utf8 -m unittest discover -s ../../tools -p "test_*.py"`（macOS 把 `py -3.13` 換成 `python3.13`） |

每支腳本都有 `--help`（繁體中文）。

## Plugin 位置

依序尋找：`--plugin <資料夾>` → 環境變數 `DOMAIN_MEMORY_PLUGIN` → `tools/` 旁的 `vendor/domain-memory/`（從 Repo 根目錄看是 `../../vendor/domain-memory/`；把 `vendor/domain-memory-1.2.8.zip` 解壓到這裡）。

## 常用指令

```powershell
# PowerShell（若顯示已停用指令碼：Set-ExecutionPolicy -Scope Process Bypass）
py -3.13 -X utf8 ..\..\tools\doctor.py
..\..\tools\dm.ps1 readiness
..\..\tools\dm.ps1 validate
py -3.13 -X utf8 ..\..\tools\make_record.py --asset rules --id FARE-005 --context pricing `
  --statement "購票日至出發日至少 14 天才有 85% 提前購票資格" `
  --evidence docs/requirements/business-rules.md:29-30 --evidence src/smart_ticket/domain/discounts.py:30-31 --upsert
..\..\tools\dm.ps1 counterfactual --file src/smart_ticket/domain/discounts.py --find ".days >= 14" --replace ".days > 14" `
  --expect "700 == 595" --test-command "./.venv/Scripts/python.exe -m pytest -q tests/integration/test_advance.py" --save cf.json
py -3.13 -X utf8 ..\..\tools\fill_package.py package-spec.json
..\..\tools\dm.ps1 ship-package --package-root domain-memory/changes/CP-D2-001 --commit HEAD
```

```bash
# Git Bash
../../tools/dm.sh readiness
../../tools/dm.sh get-context --id pricing
```

macOS（zsh 預設不把 `#` 當註解，所以這段不放註解）：

```bash
python3.13 -X utf8 ../../tools/doctor.py
../../tools/dm.sh readiness
../../tools/dm.sh validate
../../tools/dm.sh counterfactual --file src/smart_ticket/domain/discounts.py --find ".days >= 14" --replace ".days > 14" --expect "700 == 595" --test-command '.venv/bin/python -m pytest -q tests/integration/test_advance.py' --save cf.json
python3.13 -X utf8 ../../tools/fill_package.py package-spec.json
```

## 注意

- 反事實檢查 `counterfactual`（故意改壞一處程式，確認測試會失敗；抓到就顯示 killed）的 `--test-command` 不經 shell，由 Plugin 拆字後直接執行：Windows 寫 `./.venv/Scripts/python.exe`（斜線、`./` 開頭；反斜線會被吃掉，沒有 `./` 找不到程式），macOS 寫 `.venv/bin/python`。指令拒絕執行時（例如路徑寫錯、`--find` 找不到或不只一處、改壞前測試就沒通過），輸出仍是 JSON，`verdict` 是 `error`，原因在 `reason`（例如 `… could not start`）。`--expect` 是失敗輸出必須符合的斷言片段（正規表示式），不符時 verdict 是 `inconclusive`；改壞後程式無法載入也是 `inconclusive`。**要看到 `"verdict": "killed"` 才算數**，失敗輸出在 `failure_evidence`。
- PowerShell 5.1 的 `>` 會存成 UTF-16；請用 `--save 檔案`。Plugin 的 `ERROR:` 與 `NOTE:` 一律印在畫面上（stderr），不會寫進存檔。
- `init-signing-key` 沒給 `--key-file` 時，`dm` 會補成 `~/.dlc-keys/<身分代號>/signing-key`；`--key-file` 落在 Repo 內（例如 PowerShell 裡寫了不會展開的 `%USERPROFILE%`）會被拒絕。
- 證據預設只能引用 D1 確認過的來源（docs/requirements、docs/adr、src，以及 source map 列出的測試檔）；D3 新增的檔案要加 `--allow-unclassified`，只能當候選，之後無法直接升為 reviewed。
- `analyze-boundary` 一次回報兩個方向：`source_depends_on_target`（`--source-context` 依賴 `--target-context`）與 `target_depends_on_source`（反過來）。兩邊都空、`status` 是 `no_registered_collaboration`，才是沒有登記協作。
- `resolve-terms` 依名稱、id 或別名（synonyms）找詞彙，每筆附 `match_kind`：`name` 是用了正式名稱，`synonym` 是用了別名，`definition` 只是定義裡提到。查不到詞彙時回 `[]`，或列出以完整單字提到這句話的已審查紀錄（`match_kind: "mentioned"`）：那只是被提到，不是定義。
- pre-push hook 在 PATH 上找 Python 3.10 以上（先 `python3`、再 `python`）。Windows 常只有 `py` 啟動器或 Store 捷徑，macOS 的 `python3` 可能是內建的 3.9，所以 push 前在同一次執行先啟用 `.venv`（macOS：`source .venv/bin/activate`）。
- 金鑰放在 Repo **外**的 `%USERPROFILE%\.dlc-keys\<身分代號>\`（Git Bash／macOS：`~/.dlc-keys/<身分代號>/`；程式內為 `dmlib.key_dir()`），不要放在 Repo 內、不要放 `~/.ssh`。祕密掃描檢查 `scan-secrets` 會掃到工作目錄內（含已忽略）的私鑰；在已 `git init` 的 Repo 執行 `doctor.py` 時也會檢查。回顧檢查點 4 只刪除私鑰 `signing-key`，保留 `signing-key.allowed_signers`；公用電腦課後再由主持人刪除整個 `.dlc-keys` 資料夾。
