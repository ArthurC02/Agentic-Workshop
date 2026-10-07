# D3a Recovery

內容：D2 的 reviewed Registry，加上 D3a 參考實作（程式、測試、文件）作為一個未簽章、未碰 Registry 的 commit「D3a：電子發票（Recovery 參考實作）」。Registry 沒有新增候選：D3a 的新事實請依 Runbook 以 `make_record.py --allow-unclassified --upsert` 自行登記為候選；`verify-evidence` 回報的 stale 引用是實作改動了已審查事實所引用的檔案，留到 D4 以 `upsert-candidate` 更新。

使用 Recovery 不算自己完成 D3a，請在 Runbook 表單如實記錄。

## 1. 還原（約 3 分鐘）

先保存自己的成果：關掉開在舊 Repo 的編輯器，終端機 `deactivate` 後離開舊 Repo。以下在 `participant/repository/`（舊 Repo 的上一層）執行，`<REC>` 換成本包解壓後 `recovery-dlc-d3a` 資料夾的完整路徑。

```powershell
$rec = "<REC>"
Rename-Item smart-ticket-dlc-base smart-ticket-dlc-base-mine-d3a
Copy-Item -Recurse "$rec\smart-ticket-dlc-base" .
Set-Location smart-ticket-dlc-base
git init -q -b main
git fetch -q "$rec\repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

```bash
REC="<REC>"
mv smart-ticket-dlc-base smart-ticket-dlc-base-mine-d3a
cp -r "$REC/smart-ticket-dlc-base" .
cd smart-ticket-dlc-base
git init -q -b main
git fetch -q "$REC/repo.bundle" main
git reset -q FETCH_HEAD
git config --local user.name "DLC Proposer"
git config --local user.email proposer@example.com
git status --short
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
source .venv/Scripts/activate
python -m pytest -q
```

**看到什麼算成功**：`git status --short` 沒有輸出；pytest 全部 passed。

## 2. 讓 Git 能驗證歷史簽章

Registry commit 由 Maintainer 金鑰簽章；本包只附**公鑰**（`keys/maintainer.allowed_signers`），沒有私鑰。

```powershell
New-Item -ItemType Directory -Force "$HOME\.dlc-keys" | Out-Null
Copy-Item "$rec\keys\maintainer.allowed_signers" "$HOME\.dlc-keys\"
git config --local gpg.format ssh
git config --local gpg.ssh.allowedSignersFile "$HOME\.dlc-keys\maintainer.allowed_signers"
git log --format='%h %G? %GS %s'
```

```bash
mkdir -p "$HOME/.dlc-keys" && cp "$REC/keys/maintainer.allowed_signers" "$HOME/.dlc-keys/"
git config --local gpg.format ssh
git config --local gpg.ssh.allowedSignersFile "$HOME/.dlc-keys/maintainer.allowed_signers"
git log --format='%h %G? %GS %s'
```

**看到什麼算成功**：三個 Registry commit 為 `G maintainer@example.com`；最上面的「D3a：電子發票（Recovery 參考實作）」為 `N`（未簽章，不碰 Registry，hook 允許）。

## 3. 檢查 Registry

```powershell
..\..\tools\dm.ps1 validate --require-reviewed
..\..\tools\dm.ps1 verify-evidence
..\..\tools\dm.ps1 verify-sources
..\..\tools\dm.ps1 verify-audit
..\..\tools\dm.ps1 verify-git-governance --commit 5538b6dbcba9e5c4468ceddec72b75b231f9688d
```

（Git Bash 改用 `../../tools/dm.sh`。）**看到什麼算成功**：`Registry is valid.`；verify-evidence 多數 `current`，實作改動過的檔案（如 `payment_service.py`、`store.py`）顯示 `stale`，exit 1 屬預期；verify-sources 同理回報 `stale`（來源快照已變），留到 D4 處理；verify-audit `valid`；`Git governance is valid.`。

## 4. 接續簽章與 push（之後要 commit Registry 時才需要）

歷史只授權 Maintainer 的 fingerprint `SHA256:Zgznp4qU2GZH6Vmr2/RHtQzVnE+CbK2meH71Cq9BAH0`，你們沒有那把私鑰。持鑰夥伴建立**本組自己的**金鑰並把它加入授權（金鑰放在 Repo 外的 `~/.dlc-keys/`；已經有 D2 金鑰的組也請另建一把，避免覆蓋）：

```powershell
..\..\tools\dm.ps1 init-signing-key --principal maintainer@example.com --key-file "$HOME\.dlc-keys\recovery-d3a\signing-key" --sign-every-commit --save "$HOME\.dlc-keys\recovery-d3a\signing.json"
Get-Content "$HOME\.dlc-keys\recovery-d3a\signing.json"     # 記下 fingerprint（SHA256:…）
..\..\tools\dm.ps1 amend-policy --field authorized_signers --value "SHA256:Zgznp4qU2GZH6Vmr2/RHtQzVnE+CbK2meH71Cq9BAH0,<新 fingerprint>" --reason "Recovery 後由本組接手簽章"
Get-Content "$HOME\.dlc-keys\maintainer.allowed_signers" | Add-Content (git config --local gpg.ssh.allowedSignersFile)
..\..\tools\dm.ps1 install-git-hitl-hook
..\..\tools\dm.ps1 governance-readiness
git add domain-memory
git commit -m "接手 Recovery：授權本組金鑰"
```

```bash
../../tools/dm.sh init-signing-key --principal maintainer@example.com --key-file "$HOME/.dlc-keys/recovery-d3a/signing-key" --sign-every-commit --save "$HOME/.dlc-keys/recovery-d3a/signing.json"
cat "$HOME/.dlc-keys/recovery-d3a/signing.json"
../../tools/dm.sh amend-policy --field authorized_signers --value "SHA256:Zgznp4qU2GZH6Vmr2/RHtQzVnE+CbK2meH71Cq9BAH0,<新 fingerprint>" --reason "Recovery 後由本組接手簽章"
cat "$HOME/.dlc-keys/maintainer.allowed_signers" >> "$(git config --local gpg.ssh.allowedSignersFile)"
../../tools/dm.sh install-git-hitl-hook
../../tools/dm.sh governance-readiness
git add domain-memory
git commit -m "接手 Recovery：授權本組金鑰"
```

- 第四行（把 Maintainer 公鑰附加到新的 allowed signers）不可省略：`init-signing-key` 會把 `gpg.ssh.allowedSignersFile` 改指向只含新金鑰的檔案，歷史上 Maintainer 簽的 commit 就驗不過，push 會被 hook 以「Git commit signature is invalid」拒絕。
- `governance-readiness` 應為 ready。要 push 時先啟用 `.venv`（hook 呼叫裸 `python`），再 `py -3.13 -X utf8 ../../tools/setup_remote.py` 與 `git push -u origin HEAD`。
- 私鑰永遠不要 commit、不要放進 ZIP 或截圖。
