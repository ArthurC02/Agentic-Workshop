# DDD DLC 素材（materials-dlc）

> 其他段落（使用方式、解鎖碼位置、Preflight）由簡報／Runbook 作者補齊；本節只記錄打包與 edition 設定。

## edition.json

`scripts/build_materials.py --edition dlc` 讀取本目錄的 `edition.json`：

| 鍵 | 內容 |
|---|---|
| `candidate_id` | `dist/dlc-candidate/<id>/` 的 16 碼 id（DLC manifest SHA256 前 16 碼） |
| `total_minutes` / `plan` | 180 分鐘；段落 id 採規格 §3.1 的 `dlc-` 前綴（`dlc-opening` … `dlc-retro`）。builder 對段落 id 無格式限制，只要求與投影片 `data-seg` 及 `facilitator-deck/src/js/10-deck-core.js` 的 JS PLAN（含標籤）完全一致，故不需去掉前綴。 |
| `recovery_downloads` | `{"recovery-dlc-<段>.zip": ["dlc-rec-<段>", 最早分鐘]}`：d1=35、d2=45、d3a=95、d3b=125、d3c=155（規格 §3.2）。分鐘必須等於候選包 `build-evidence.json` 的 `release_minute`；主課專用的 B1/B2 版本檢查不套用於 DLC。Recovery ZIP 只能在對應 `dlc-rec-*` 群組頁以 `download` 發放，不可 `include`。 |
| `forbidden_markers` | 規格 §5.1：`facilitator`、`evaluation`、`reference-solution`、`reference answer`、`標準答案`、`observation-guide`、`rubric`、`評分表`、`reference-registry`（`STUDENT_FARE_RATE` 不列入） |
| `marker_exemptions` | 只允許 `[頁 id, 精確片語]`，每條須在此說明理由（目前無）。 |

## 候選包（dist/dlc-candidate）

```text
py -3.13 -X utf8 scripts/vendor_dlc_plugin.py            # 重建 vendor/domain-memory-0.2.2.zip 與 .SHA256SUMS（--check 只比對）
py -3.13 -X utf8 scripts/build_delivery_dlc.py --pin     # 依 manifest 的 sources 重新列舉 files[]；審查 diff
py -3.13 -X utf8 scripts/build_delivery_dlc.py           # 建 dist/dlc-candidate/<sha16>/，缺來源即失敗
py -3.13 -X utf8 scripts/build_delivery_dlc.py --verify dist/dlc-candidate/<sha16>
```

- `--allow-missing` 僅供開發：缺少的來源以警告略過，沒有任何檔案的包不產出，並列於 `build-evidence.json` 的 `missing_packages`。正式候選不得使用。
- 包別固定：`participant-dlc-open`、`participant-dlc-d1`、`-d2`、`-d3a`（情境卡 01＋`worksheets/d3-*.md`）、`-d3b`、`-d3c`、`-d4`、`recovery-dlc-d1/d2/d3a/d3b/d3c`（來源 `07-dlc-ddd/facilitator/recovery/<段>/`，ZIP 內根目錄 `recovery-dlc-<段>/`）、`facilitator-dlc-before-session`、`evaluation-dlc-private`。
- 學員包內路徑即 Repo 相對路徑，Runbook `include` 寫法例：`zip=participant-dlc-d3a.zip path=agentic-workshop/07-dlc-ddd/participant/scenarios/01-e-invoice.md`。
- 建置後在 `edition.json` 更新 `candidate_id`，再跑 `build_materials.py --edition dlc` 與 `package_materials.py dlc`（輸出 `dist/materials-dlc/participant-materials-dlc.zip`）。
- 注意：builder 不允許在 `open` 頁放 `download`；`participant-dlc-open.zip` 的下載需放在第一個解鎖群組的頁面，或由主持人另行發放。
