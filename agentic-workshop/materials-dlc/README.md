# DDD DLC 素材（materials-dlc）

本資料夾是 DDD DLC 的學員 Runbook（`participant-runbook/content/`）、主持簡報（`facilitator-deck/src/slides/`）、檢查點對照（`CHECKPOINTS.md`）與解鎖碼（`unlock-codes.json`）。下面記錄 Runbook 的寫法、打包與 edition 設定。

## Runbook 的寫法（複製提示詞即可通關）

- 每段頁首一張「現在在做什麼」卡（情境、目標、今天的技巧、完成的樣子），段落結尾用「完成後想一想」（3 題）收尾；檢查點總覽用條列（分鐘＋要做什麼），不用表格。
- 每個檢查點分四塊：① 為什麼做這一步（人要判斷的事寫在這裡）→ ② 貼給 Agent（指令依系統不同時用 Windows／macOS 分頁）→ ③ 確認結果（Agent 只回「成功」或「失敗：原因」，下方接一段「失敗時」補救提示詞）→ ④ 補充（技巧／新概念小卡、「💬 討論一下」，有才出現）。
- Plugin、`make_record.py`、Git 與 pytest 指令原樣寫進提示詞，由學員的 Coding Agent 執行並白話回報；需要人決定時，Agent 先列選項或草稿並停下，學員只回「同意」「選 B」「第 3 項不要」這類短回覆。學員頁面不放要學員自己打的指令區塊。
- 紀錄由 Agent 寫進學員 Repo：各段 `notes/<段落>.md`、決策卡與交接單在 `docs/handoffs/`。表單每段最多一張，只留人的決定，以下拉與勾選為主（最多 3 欄＋1 個短文字欄）。
- D2 起兩人共用一台機器：夥伴另開終端機與自己的 Agent 對話，金鑰、`record-approval`、簽章 commit 與 push 只在那個對話裡、由夥伴讀過審查包後下指令（D3a–c 檢查點 5 與 D4 的 commit 也沿用它）；提案者的 Agent 不 commit、不 push、不讀 `.dlc-keys`，也不代替核准。
- 檢查點名稱改動時，Runbook 標題、`CHECKPOINTS.md` 與簡報 `data-title`／時間軸要一起改。

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
py -3.13 -X utf8 scripts/vendor_dlc_plugin.py            # 重建 vendor/domain-memory-0.10.15.zip 與 .SHA256SUMS（--check 只比對）
py -3.13 -X utf8 scripts/build_delivery_dlc.py --pin     # 依 manifest 的 sources 重新列舉 files[]；審查 diff
py -3.13 -X utf8 scripts/build_delivery_dlc.py           # 建 dist/dlc-candidate/<sha16>/，缺來源即失敗
py -3.13 -X utf8 scripts/build_delivery_dlc.py --verify dist/dlc-candidate/<sha16>
```

- `--allow-missing` 僅供開發：缺少的來源以警告略過，沒有任何檔案的包不產出，並列於 `build-evidence.json` 的 `missing_packages`。正式候選不得使用。
- 包別固定：`participant-dlc-open`、`participant-dlc-d1`、`-d2`、`-d3a`（情境卡 01＋`worksheets/d3-*.md`）、`-d3b`、`-d3c`、`-d4`、`recovery-dlc-d1/d2/d3a/d3b/d3c`（來源 `07-dlc-ddd/facilitator/recovery/<段>/`，ZIP 內根目錄 `recovery-dlc-<段>/`）、`facilitator-dlc-before-session`、`evaluation-dlc-private`。
- 學員包內路徑即 Repo 相對路徑，Runbook `include` 寫法例：`zip=participant-dlc-d3a.zip path=agentic-workshop/07-dlc-ddd/participant/scenarios/01-e-invoice.md`。
- 建置後在 `edition.json` 更新 `candidate_id`，再跑 `build_materials.py --edition dlc` 與 `package_materials.py dlc`（輸出 `dist/materials-dlc/participant-materials-dlc.zip`）。
- 注意：builder 不允許在 `open` 頁放 `download`；`participant-dlc-open.zip` 的下載需放在第一個解鎖群組的頁面，或由主持人另行發放。
