---
name: record-candidates
description: 把使用者同意的詞彙、Context、規則等登記成 domain-memory 的候選（candidate）。使用者同意一份候選清單、要「登記」「寫回模型」時使用；也用來先試產生、不登記。
---

# record-candidates：把同意的項目登記為候選

只登記使用者同意的項目。每筆都要有證據 `路徑:起-迄`：行號實際打開檔案核對，段落越短越好，只框住佐證這句話的那幾行。下面的 `<py>` 是 Windows `py -3.13`、macOS `python3.13`；`<dm>` 是 AGENTS.md 寫的 dm 腳本。

## 多筆：寫成一個 JSON 檔再登記（D1）

1. 在 Repo 根目錄寫 `d1-records.json`（檔案編輯工具、UTF-8），內容是一個陣列，每筆一個物件，順序是 Context → 詞彙 → 規則（詞彙和規則會參照 Context）：
   - `{"asset": "contexts", "id": "context id", "name": "名稱", "responsibility": "它決定什麼", "evidence": ["路徑:起-迄"]}`
   - `{"asset": "vocabulary", "id": "詞彙 id", "name": "名稱", "definition": "定義", "context": "context id", "evidence": ["路徑:起-迄"]}`
   - `{"asset": "rules", "id": "規則 id", "statement": "一句能被測試推翻的敘述", "context": "context id", "evidence": ["規則文件的段落", "測試或程式的段落"]}`
   - id 用小寫英文加連字號；規則 id 沿用文件裡的規則編號。
   - 兩個 Context 確實共用同一個定義，才寫 `"context": ["id1", "id2"]`。同一個詞在兩個 Context 意思不同，各寫一筆（不同 id），互加 `"not_same_as": ["對方的 id"]`。使用者選了別名，加 `"synonyms": ["別名"]`；別名不可重複，也不可和任何詞彙的名稱相同。
   - Context id 改了，同步改詞彙和規則的 `context`。
2. 先試產生、不登記：`<py> -X utf8 ../../tools/make_record.py --batch d1-records.json`。只回報沒通過的那幾筆與原因（全部通過就說「全部通過」）。
3. 使用者要登記時，同一個指令加 `--upsert`（同一種資產一起登記：全部成功或全部不登記）。

## 單筆（D3、D4）

`<py> -X utf8 ../../tools/make_record.py --asset rules --id 規則id --statement "敘述" --context contextid --evidence 路徑:起-迄 --evidence 路徑:起-迄 --allow-unclassified --upsert`

- 詞彙改用 `--name` 和 `--definition`，Context 改用 `--name` 和 `--responsibility`；其他欄位看 `make_record.py --help`。
- 證據在 D3 新增的檔案時一定要 `--allow-unclassified`：新檔案不在 D1 確認過的來源清單裡，只能當候選。

## Aggregate 與規則（D3c）

- Aggregate：`{"asset": "aggregates", "id": "…", "context": "context id", "root": "唯一入口的實體", "invariants": ["…"], "evidence": ["路徑:起-迄"]}`；規則可加 `"aggregate": "Aggregate id"`（不屬於任何 Aggregate 就不寫）。寫成一個 JSON 檔，用 `<py> -X utf8 ../../tools/make_record.py --batch 檔案 --allow-unclassified --upsert`。
- 看到 `aggregate … belongs to context …, which the record does not name`：不要刪掉 aggregate 硬過，停下說明是規則的 Context 還是 Aggregate 放錯了，等使用者決定。

## 登記之後

1. 執行 `<dm> validate` 和 `<dm> verify-evidence`。
2. 回報：登記了哪些 asset:id、失敗的有哪些與原因、validate 的結果、verify-evidence 的 current、shifted、stale、missing、invalid 各幾個。
3. 不把任何紀錄寫成 reviewed。已審查的紀錄不能覆寫：行為變了，就用新 id 登記一條候選。

## 失敗時

- 證據不在已確認來源內：改引用 `docs/requirements/`、`docs/adr/`、`src/` 或 `tests/` 底下的 `test_*.py`；D3 的新檔案加 `--allow-unclassified`。
- 行號不對：重新打開檔案核對。
- 列出要改的地方，等使用者同意再重跑。不手動修改 `domain-memory/`。
