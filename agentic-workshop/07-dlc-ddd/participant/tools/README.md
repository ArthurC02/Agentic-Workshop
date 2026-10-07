# DLC 輔助工具

讓時間花在領域決策，而不是手打 JSON。只用 Python 標準函式庫，以 subprocess 呼叫 domain-memory Plugin，不修改 Plugin。

**所有指令都在 Repo 根目錄（`smart-ticket-dlc-base/`）執行。** 下面以 `../tools/` 表示本資料夾。

| 檔案 | 用途 |
|---|---|
| `dm.ps1`、`dm.sh` | Plugin 命令前綴：固定 `py -3.13 -X utf8`，自動補 `--registry-root domain-memory` 與 `--repo-root .`；`--save 檔案` 以 UTF-8 存輸出 |
| `make_record.py` | 由 id、名稱、定義與 `路徑:起-迄` 呼叫 `cite`，寫出完整 record JSON；`--upsert` 直接登記為候選；`--batch` 一次多筆 |
| `fill_package.py` | 由一份精簡描述 JSON 建立並填寫 Change Package；測試**實際執行**，記錄真實 exit code 與輸出 sha256 |
| `write_scm_attestation.py` | 把夥伴的已簽章 commit 寫成 `git-signed-commit` attestation |
| `setup_remote.py` | 建本機 bare remote 並設為 `origin`，讓 pre-push hook 有地方 push |
| `doctor.py` | 健檢 Windows 陷阱並列出修正方式 |
| `dmlib.py` | 共用模組（dm 前綴本體） |
| `test_tools.py` | 自檢：`py -3.13 -X utf8 -m unittest discover -s ../tools -p "test_*.py"` |

每支腳本都有 `--help`（繁體中文）。

## Plugin 位置

依序尋找：`--plugin <資料夾>` → 環境變數 `DOMAIN_MEMORY_PLUGIN` → `../vendor/domain-memory/`（把 `vendor/domain-memory-0.2.2.zip` 解壓到這裡）。

## 常用指令

```powershell
# PowerShell（若顯示已停用指令碼：Set-ExecutionPolicy -Scope Process Bypass）
py -3.13 -X utf8 ..\tools\doctor.py
..\tools\dm.ps1 readiness
..\tools\dm.ps1 validate
py -3.13 -X utf8 ..\tools\make_record.py --asset rules --id FARE-005 --context pricing `
  --statement "購票日至出發日至少 14 天才有 85% 提前購票資格" `
  --evidence docs/requirements/business-rules.md:29-30 --evidence src/smart_ticket/domain/discounts.py:30-31 --upsert
..\tools\dm.ps1 counterfactual --file src/smart_ticket/domain/discounts.py --find ".days >= 14" --replace ".days > 14" `
  --test-command ".venv\Scripts\python.exe -m pytest -q tests/integration/test_advance.py" --save cf.json
py -3.13 -X utf8 ..\tools\fill_package.py package-spec.json
py -3.13 -X utf8 ..\tools\write_scm_attestation.py --package domain-memory/changes/CP-001 --commit HEAD
```

```bash
# Git Bash
../tools/dm.sh readiness
../tools/dm.sh get-context --id pricing
```

## 注意

- `counterfactual` 的 `--test-command` 由 cmd.exe 執行：用 `.venv\Scripts\python.exe` 這種反斜線路徑。路徑錯時會以 `ERROR: the tests do not pass before anything is broken` 加一行亂碼（cmd.exe 的 cp950 錯誤訊息）結束、exit 1；**看到 `"verdict": "killed"` 才算數**。
- PowerShell 5.1 的 `>` 會存成 UTF-16；請用 `--save 檔案`（指令失敗時錯誤訊息仍會印在畫面上）。
- `init-signing-key` 沒給 `--key-file` 時，`dm` 會補成 `~/.dlc-keys/<principal>/signing-key`；`--key-file` 落在 Repo 內（例如 PowerShell 裡寫了不會展開的 `%USERPROFILE%`）會被拒絕。
- 證據只能引用已確認來源：`docs/requirements/`、`docs/adr/`、`src/`、`tests/` 下的 `test_*.py`；其他位置 `make_record.py` 會拒絕（那種證據之後無法升為 reviewed）。
- `analyze-boundary` 有方向：`--source-context` 是提供方（producer），反過來查會得到 `no_registered_collaboration`。
- `resolve-terms` 比對的是詞的名稱、id 或定義，不比對 synonyms；查詢句要包含詞的完整名稱。
- pre-push hook 會呼叫裸 `python`：push 前先啟用 `.venv`。
- 金鑰放在 Repo **外**的 `%USERPROFILE%\.dlc-keys\<代號>\`（Git Bash：`~/.dlc-keys/<代號>/`；程式內為 `dmlib.key_dir()`），不要放在 Repo 內、不要放 `~/.ssh`；`scan-secrets` 會掃到工作目錄內（含已忽略）的私鑰，`doctor.py` 會檢查。課後請刪除該資料夾。
