# DDD DLC（Agent 的領域記憶）

主課（Tool → Teammate → Digital Worker）之後的 180 分鐘加課：把領域知識轉成經審查、以檔案保存的 Domain Memory（domain-memory Plugin 0.10.15），並用它驅動受治理的變更。九段：開場、D1 共同語言與邊界、D2 審查與核准（成對簽章）、休息、D3a 電子發票、D3b 點數折抵、D3c 團體部分退款、D4 交接、回顧。

學員操作方式：Runbook 每個檢查點給一段可直接複製的提示詞，學員的 Coding Agent 照提示詞執行 Plugin、輔助腳本與 Git 指令並白話回報；需要決定時 Agent 先列選項並停下，學員以短回覆決定。紀錄由 Agent 寫進學員 Repo 的 `notes/` 與 `docs/handoffs/`，表單只留人的決定。D2 起兩人共用一台機器：夥伴另開終端機與自己的 Agent 對話，金鑰、核准、簽章 commit 與 push 只在那個對話執行（D3、D4 的 commit 也是）；提案者的 Agent 不 commit、不 push、不碰金鑰、不代替核准。

## 資料夾

| 資料夾 | 內容 | 發給學員 |
|---|---|---|
| `participant/` | 起始 Repo `smart-ticket-dlc-base`、需求卡、`vendor/`（Plugin ZIP 與 SHA256）、`tools/`、`worksheets/`（Agent 寫紀錄用的格式範本） | 是（依段落分包） |
| `facilitator/` | 主持人指南、`recovery/`（各段 Recovery 來源與 `make_recovery.py`） | 否（Recovery 只按需公布其 ZIP） |
| `evaluation/` | reference Registry、三個參考解答、觀察指引、驗證報告與證據 | 否，永不給學員 |

`facilitator/` 與 `evaluation/` 不得出現在任何學員包或 Runbook。

## 建置與打包

於 Repo 根，Python 3.13：

```text
py -3.13 -X utf8 scripts/vendor_dlc_plugin.py --check
py -3.13 -X utf8 scripts/build_delivery_dlc.py --pin
py -3.13 -X utf8 scripts/build_delivery_dlc.py
py -3.13 -X utf8 scripts/build_materials.py --edition dlc [--check]
py -3.13 -X utf8 scripts/package_materials.py dlc
```

`build_delivery_dlc.py --verify dist/dlc-candidate/<id>` 驗證候選包。建置後須更新 `materials-dlc/edition.json` 的 `candidate_id`。主課 manifest 與凍結候選不得變更。

## 文件

- 規格：[`docs/instructions/11_DDD_DLC產製指令書.md`](../../docs/instructions/11_DDD_DLC產製指令書.md)
- 主持人指南：[`facilitator/facilitator-guide.md`](facilitator/facilitator-guide.md)
- 素材與建置細節：[`../materials-dlc/README.md`](../materials-dlc/README.md)
