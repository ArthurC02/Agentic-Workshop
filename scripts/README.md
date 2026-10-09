# P11 驗證與受控打包工具

> 讀者：維護者、主持與驗收人員。時機：事前技術驗證及候選包產製。前置：Python3.13、作者Repo與已驗收來源。可見性：內部，不發學員。

`package-manifest.json` 列出每個允許來源、目的地及SHA256，以及刻意改寫的角色安全文件。增加檔案或更新雜湊須先審查角色、時点及內容，不用遞迴目錄直接發學員。

來源修改後（依[08規範調整](../docs/instructions/08_全域驗證與受控打包產製指令書.md)）：完整驗證通過，再以`build_delivery.py --repin-reviewed-sources --expect-manifest-sha256 <目前Manifest SHA256>`更新雜湊並重建；新候選ID只寫在`build_materials.py`的`CANDIDATE_ID`。Manifest來源由根目錄`.gitattributes`設為`-text`，雜湊即Repo原始位元組。

```powershell
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/build_delivery.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/verify_delivery.py dist/p11-candidate/<manifest-hash-prefix> --evidence agentic-workshop/06-runbook/evaluation/p11-package-validation-evidence.json
```

Builder使用固定ZIP時間與排序，輸出於Manifest雜湊命名的新目錄；若同名目錄已存在會停止，不覆寫。重驗既有包使用Verifier；重建相同Manifest需由維護者另選乾淨工作區，不能刪除不明生成物。工具從程式位置定位Repo，命令中的相對參數仍以目前工作目錄解讀。

13包各自標記角色與發放分鐘：G0在7、Time Skip與B0在29、獨立分析33、Shared Context39、B1任務44、B2任務52、B3任務及治理63、回顧80。B1／B2 Recovery只在52／63分鐘由主持按需核准；保留原成果，在新目錄確認版本、Health及新Agent Context。B3答案沒有Recovery包。

Facilitator與Evaluation私有包分開；主持／驗收人員可在同一**私有**目錄解壓兩包及所有分時學員包以交叉核對相對連結，學員只取得當下已授權的一包。P11生成的打包證據不放進它所描述的ZIP，避免自我雜湊循環；其JSON及驗證報告以作者相對路徑作私有外置補充交付。完整私有資料樹不發學員，也不發`.git`或Bundle至學員。

B0／Recovery採過濾輸出與安全README、Context、API摘要；程式與測試保持來源字節一致，不能稱為52檔完整clean-copy。初始B0於29分鐘保留兩份受控文件落差及三份當時B0安全ADR精確白名單，供個人分析；生成文字不指出學生票Bug或直接給出優惠順序。Recovery仍排除ADR、歷史、原內部README及API範例，不發未來解答。既有凍結來源不改寫，B2名稱誤文以[勘誤](../agentic-workshop/03-brownfield/evaluation/22-b2-documentation-errata.md)及正確摘要查證。

Verifier檢查實際ZIP清單、來源／輸出雜湊與學員相對連結，並拒絕路徑穿越、隱藏Git、越界答案與損壞內容。B1／B2解壓副本使用既有獨立venv執行pip check、44／55項版本Gate及Health／OpenAPI／建立／付款／改退票Smoke；不宣稱重新安裝依賴或真人Recovery完成。Python `-O` 不支援驗證。

一次執行全部步驟（檢查知識點出處、偵測漂移、驗證、釘選、建置、驗證候選、重建教材與測試）：`scripts/release_materials.py`。

台灣繁體中文檢查：`scripts/check_zh_tw.py`。課程素材、docs/ 與 .claude 的文字必須是繁體字並使用台灣詞彙；發布流程會先執行。

知識點出處檢查：`scripts/check_references.py`。每個「技巧／新概念」說明框和詞彙表的每一列，都必須引用 `.claude/skills/course-authoring/references.md` 中已查證的出處；Plugin 章節與本課程文件標題也必須真的存在。

## 全域技術驗證

```powershell
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/validate_workshop.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/verify_runtime_baselines.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 -m unittest discover -s scripts -p 'test_*.py'
```

六個獨立環境預設`.codex-tmp/g0-env`至`b3-env`；全域驗證可用`--env-root`指定已準備環境。可用uv建立：`uv venv --seed --python 3.13 .codex-tmp/<版本>-env`，再`uv pip install --python .codex-tmp/<版本>-env/Scripts/python.exe -r <版本目錄>/requirements.txt`。執行JSON與原始log／JUnit XML保存於`agentic-workshop/06-runbook/evaluation/`；B0僅精確Manifest失敗集合可接受，G0受控skip與其他版本全通過分開。

`validate_workshop.py --static-only`另寫STATIC_PASS證據，不能當六版技術PASS；其凍結來源檢查只與最新一次完整執行的六版來源雜湊比對。完成技術執行後只改文件，可用`--refresh-static`核對六版來源與原始log雜湊後更新靜態部分，保留技術原執行時間。`verify_runtime_baselines.py`核對requirements固定版本及本次依賴核對前後來源Hash，未宣稱重新安裝。

真人90分鐘、B3 13分鐘、兩分鐘閱讀及60秒例外、現場Agent可用性與發布核准仍需人工證據。填[演練紀錄](../agentic-workshop/06-runbook/rehearsal-record.md)及[發布清單](../agentic-workshop/06-runbook/release-checklist.md)，未執行項保持NOT_RUN／PENDING。

完成條件：來源一致、實際包驗證通過且角色／時點審查完成；候選包通過技術驗證不等同正式發布。

## 本輪一致性修正

原`360cb551f76eeb73`候選未涵蓋教材語意問題，已停止用於本次演練。修正與最新候選定位見[修正報告](../agentic-workshop/06-runbook/evaluation/consistency-correction-report.md)。內容政策同時檢查準備內容與實際ZIP，拒絕重新注入答案、移除必要教材或擴大ADR例外。

```powershell
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/validate_consistency_corrections.py
& '.\.codex-tmp\b3-env\Scripts\python.exe' -X utf8 scripts/verify_delivery.py 'dist/p11-candidate/<本輪實際ID>' --evidence 'agentic-workshop/06-runbook/evaluation/consistency-package-validation-evidence.json'
```

新包與內容驗證JSON採私有外置補充，不放進描述自身ZIP的內容形成循環Hash。變更已列來源須先review，再以build_delivery.py的`--repin-reviewed-sources --expect-manifest-sha256 <已審查Manifest完整SHA256>`更新既有白名單Hash；此命令不自行加入新檔，新增檔需明列審查。舊P11證據保留歷史，不覆寫成新候選結果。
