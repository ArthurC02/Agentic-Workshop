---
name: counterfactual
description: 反事實檢查：故意改壞一處程式、跑指定的測試，確認測試抓得到（killed），再自動還原。要證明某條規則有測試守著，或使用者說「反事實檢查」「改壞看看」時使用。
---

# counterfactual：證明測試守得住規則

## 1. 先提方案，不執行

每條規則各列一個方案：

- FILE：守住這條規則的程式檔；改的要是守住規則的那一行。
- FIND：這個檔案裡只出現一次的一段原字串；REPLACE：改壞後的字串。
- TEST：預期會失敗的測試檔。
- EXPECT（可省略）：改壞後應該出現的斷言片段，給 `--expect` 用，例如 `700 == 595`。

寫進這段的 notes，停下等使用者同意或選擇。

## 2. 同意後，每條執行一次

存檔名照提示詞給的（例如 `cf-d2.json`、`cf-d3a-1.json`、`cf-d3a-2.json`）。有 EXPECT 才加 `--expect "EXPECT"`。

- Windows PowerShell：`..\..\tools\dm.ps1 counterfactual --file FILE --find "FIND" --replace "REPLACE" --expect "EXPECT" --test-command './.venv/Scripts/python.exe -m pytest -q -W ignore::DeprecationWarning TEST' --save cf-….json`
- Windows Git Bash：`../../tools/dm.sh counterfactual`，其餘參數相同（`--test-command` 一樣是 `./.venv/Scripts/python.exe`）。
- macOS：`../../tools/dm.sh counterfactual …`，`--test-command '.venv/bin/python -m pytest -q -W ignore::DeprecationWarning TEST'`。

`--test-command` 不經 shell，由 Plugin 直接執行：Windows 一定寫 `./.venv/Scripts/python.exe`（斜線、`./` 開頭），整段用單引號包住。`-W ignore::DeprecationWarning` 讓套件過時警告不混進失敗輸出。

## 3. 讀結果

讀存下的 JSON，回報：`verdict`、`reason`、`failure_evidence` 裡的斷言那一行、`failing_tests`、`restoration_result.restored`。

- **killed** 才算有測試守著，而且 `failure_evidence` 要是測試本身失敗：AssertionError，被測程式自己丟出的例外（例如 ConnectionError），或測試替身注入、被測程式本該攔下卻漏出來的例外。ImportError、語法錯誤、收集測試時的錯誤（collection error）、只有亂碼，都不算。
- **inconclusive**：失敗了，但不是 `--expect` 寫的那個斷言，或改壞後程式根本無法載入；不算證明。測試逾時就縮小 TEST 範圍、用同一組字串重跑；程式無法載入就換一種程式仍能執行的改法。
- **error**：指令拒絕執行，原因在 `reason`（例如找不到字串、字串不只一處、`the tests do not pass before anything is broken`：改壞前測試就沒通過）。換一段更精確的字串並告訴使用者；error 的 cf 檔先刪掉再重跑。
- **survived**：沒有測試守著。`reason` 提到改跑整套時，可以用同一組字串、TEST 換成 `tests`、存成下一個編號再跑一次。仍是 survived，不要換一個比較容易 killed 的字串：提出要補的測試，停下等同意，補完用同一組字串重跑。
  - 判斷沒有任何輸入分辨得出改壞前後（例如另一段程式也擋住；這叫等價）：不要硬補測試，指出原因所在的 `檔案路徑:行號`，停下等確認，記為「等價、未證明」。只是現有測試資料剛好碰不到（例如測試的時鐘固定在某個時刻）不算等價，要補測試。
- 來不及補的，在紀錄中標「未證明」；survived 的規則不能當成已受保護。

## 4. 收尾

- `restoration_result.restored` 必須是 true；不是就停下告訴使用者。
- killed、survived、inconclusive 的 cf 檔都保留，會一起 commit。
- 全部跑完再執行一次完整測試，回報每條規則是不是都有 killed。
