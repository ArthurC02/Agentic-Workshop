---
id: glossary
title: 詞彙表
minute: 00-180
group: open
section: 參考
---

# 詞彙表

本表整理這堂延伸課常用詞彙的意思。DDD 概念不另開理論課，這裡只寫到「今天操作時夠用」的程度；各需求的業務名詞，以該段解鎖後的需求卡為準。

## DDD 概念

| 詞彙 | 今天的用法 |
|---|---|
| 通用語言（Ubiquitous Language） | 團隊、文件、程式與測試對同一件事使用同一個名字與定義。今天以 Registry 的 vocabulary（詞彙）記錄；同一件事兩個名字、或文件有而程式沒有，都是要記下的發現。 |
| Bounded Context（Context） | 一個名詞或規則「在這個範圍內有一致意義」的邊界，通常對應一群負責同一類決定的程式。今天以 Registry 的 contexts 記錄，每個 Context 寫「它決定什麼」。 |
| Context Map／邊界協作 | Context 之間誰提供、誰使用、交換什麼。`analyze-boundary` 列出已登記的協作；回 `no_registered_collaboration` 表示沒有登記，不代表程式裡沒有互相讀寫。 |
| Aggregate | 一組必須**一起**保持一致的資料，外界只能透過一個入口（Aggregate root）修改它。用來回答「哪些資料要在同一次操作中同時成立」。 |
| 不變量（Invariant） | 任何時刻都必須成立的條件，例如某個數量不得為負。好的不變量可以寫成一個會失敗的測試。 |
| 一致性邊界 | 不變量必須立即成立的範圍。邊界內同步、全有或全無；邊界外可以事後處理。 |
| Port／Adapter | Port 是 domain 對外需要的能力（用領域語言描述的介面）；Adapter 是接上真實外部系統的實作。測試時用替身（Fake）實作同一個 Port。 |
| 防腐層（ACL, Anti-Corruption Layer） | 把外部系統的資料格式與錯誤碼翻譯成自己領域語言的那一層，讓外部的命名與規則不滲進 domain。 |
| 冪等（Idempotency） | 同一個請求重送多次，結果和送一次相同。通常靠一個穩定的鍵（例如訂單編號）判斷是否已處理過。 |

## domain-memory Plugin

| 詞彙 | 今天的用法 |
|---|---|
| Domain Memory／Registry | 存在 Repo 的 `domain-memory/` 資料夾中、以 JSON 檔保存的領域知識：policy、source map、registry（各類 record）與 audit（稽核鏈）。 |
| record | Registry 裡的一筆資料，例如一個 Context、一個詞彙、一條規則或一個 Aggregate。每筆都有 `id` 與 `evidence`。 |
| 來源（source）／source map | 人確認過、可以當證據的路徑清單與它們的快照。之後新增、刪除或改名檔案，`verify-sources` 會回報 `stale`。 |
| 證據（evidence）／`cite` | 指向某個檔案第幾行到第幾行、並帶內容雜湊的引用。引用的行被改過，`verify-evidence` 會回報 `stale`。 |
| 候選（candidate） | 有證據、但還沒經過核准的主張。Agent 或任何人登記的新內容都是候選，不可當成限制或事實。 |
| reviewed | 經 Change Package、他人核准、簽章 commit 與 `apply-approved-updates` 升級後的 record。不能直接覆寫，只能由下一個核准的提案取代。 |
| local-draft-only／scm-verified | Registry 的審查模式。前者只能存候選；後者要求從套件外部驗證的核准證據（今天是簽章 commit）。 |
| Change Package | 一次變更的審查包，放在 `domain-memory/changes/<id>/`：需求正規化、提案、測試 obligation 與證據包四個 JSON。 |
| obligation | 一個驗收條件或規則對應的可觀察檢查。證據包記錄它實際執行的 exit code 與輸出雜湊。 |
| attestation | 寫進證據包、指向簽章 commit 的外部核准證據。 |
| counterfactual | 故意把守住某條規則的一段程式改壞，跑指定測試，再原樣還原。`killed`：測試抓到了；`survived`：沒有測試守住它；`inconclusive`：逾時。 |
| Handoff | 交給 Coding Agent 的決策紀錄：Domain facts、Forces、Decision、External systems、Unknowns、Proof obligations、Counterfactual check 七段。 |
| audit／`verify-audit` | 每次 Registry 變動都附加一筆、以雜湊串起的稽核事件。能看出被竄改，但不是外部不可變的紀錄。 |

## 角色與工具

| 詞彙 | 今天的用法 |
|---|---|
| Proposer | D2 的提案人：整理 Change Package、送出提案、套用。不得核准自己的提案。 |
| Maintainer | D2 的持鑰人：建立簽章金鑰、決定授權誰簽章、核准並做簽章 commit。 |
| `dm.ps1`／`dm.sh` | 學員包 `tools/` 中的 Plugin 命令前綴，固定 `py -3.13 -X utf8`，並自動補 `--registry-root domain-memory` 與 `--repo-root .`；`--save 檔案` 以 UTF-8 存輸出。 |
| `make_record.py` | 由 id、名稱、定義與「路徑:起-迄」產生帶 `cite` 證據的 record；`--upsert` 直接登記為候選，`--batch` 一次多筆。 |
| `fill_package.py` | 由一份精簡描述 JSON 填寫 Change Package，並實際執行每個測試。 |
| `write_scm_attestation.py` | 把已簽章的 commit 寫成 attestation。 |
| `doctor.py` | 檢查 Python、UTF-8、PATH 上的 python、Git、ssh-keygen 與 Plugin 版本等環境問題。 |
| Recovery | 落後時由主持人個別提供的接續起點。使用 Recovery 不算自己完成前一段。 |
