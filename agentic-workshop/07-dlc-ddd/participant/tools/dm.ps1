# domain-memory 命令前綴（PowerShell）。在 Repo 根目錄執行：
#   ..\..\tools\dm.ps1 readiness
#   ..\..\tools\dm.ps1 validate          # 自動補 --registry-root domain-memory --repo-root .
# 固定以 Python 3.13 加 -X utf8 執行，避免 cp950 UnicodeDecodeError。
# 若出現「已停用指令碼執行」，先執行：Set-ExecutionPolicy -Scope Process Bypass
# PowerShell 7.3 之前傳給原生程式會丟掉空字串（--replace ''）、吃掉引號；先自行跳脫。
$argv = $args
if ($PSVersionTable.PSVersion -lt [version]'7.3') {
  $argv = @($args | ForEach-Object {
    if ($_ -eq '') { '""' }
    else { $s = $_ -replace '(\\*)"', '$1$1\"'; if ($s -match '\s') { $s -replace '(\\+)$', '$1$1' } else { $s } }
  })
}
& py -3.13 -X utf8 (Join-Path $PSScriptRoot 'dmlib.py') @argv
exit $LASTEXITCODE
