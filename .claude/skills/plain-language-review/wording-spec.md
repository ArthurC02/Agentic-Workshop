# 白話化用語規範（主課與 DLC 共用）

讀者：銀行內部開發人員，第一次參加。原則：縮寫與英文工作用語在每檔／每頁第一次出現時就地附中文；之後照舊用。開發人員普遍懂的（API、JSON、HTTP、Git、commit、Repo、pytest、Diff、venv）不必展開。只改需要改的句子，維持全形標點與語氣。

## 統一展開寫法

| 詞 | 第一次出現寫法 |
|---|---|
| SDLC | Agentic SDLC（Software Development Life Cycle，軟體開發生命週期；這裡指 Agent 參與整個開發流程） |
| Tool → Teammate → Digital Worker | Agent 從工具、隊友到能獨立執行任務的數位員工；不要只寫 DW |
| MVP | MVP（Minimum Viable Product，最小可行產品） |
| AC | AC（Acceptance Criteria，驗收條件）；統一用「驗收條件」 |
| ADR | ADR（Architecture Decision Record，架構決策紀錄） |
| DDD | DDD（Domain-Driven Design，領域驅動設計） |
| DLC | 延伸課程（DLC，原指遊戲的追加內容；這裡指主課之後的加課） |
| SHA256 | SHA256 雜湊（檔案的指紋；一個位元組被改，值就不同） |
| Gate | 核准關卡（Gate） |
| Greenfield／Brownfield | Greenfield（從頭開始的新專案；主課由 G0 骨架起步）／Brownfield（已有程式碼的既有專案） |
| G0／B0–B3 | G0＝Greenfield 起始程式包；B0＝已上線的既有程式；B1–B3 各為一段任務 |
| D1–D4 | DLC 四段的代號；D3 再分 a、b、c 三張需求卡 |
| Time Skip | Time Skip（時間快轉：專案假設已開發一段時間） |
| Shared Context | 共同脈絡（Shared Context）；不用「共同背景」 |
| Teammate／Digital Worker（表單用語） | 隊友／數位員工 |
| Recovery | Recovery（復原包：進度落後時改用的接續基線） |
| Seed Data | Seed Data（系統預設的測試資料） |
| Rule ID | 規則編號（Rule ID） |
| Review／Delivery | 檢視（Review）／交付（Delivery） |
| Gherkin | Gherkin（用 Given／When／Then 寫測試情境的格式） |
| reviewed | 已審查（reviewed） |
| counterfactual | 反事實檢查（counterfactual：故意改壞一處程式，確認測試會失敗；抓到就顯示 killed） |
| Change Package | 變更審查包（Change Package） |
| CP／REQ／AC／OB／INV | CP＝Change Package、REQ＝需求、AC＝驗收條件、OB＝obligation（要通過的檢查）、INV＝不變量 |
| HITL | HITL（Human-in-the-loop，人工把關） |
| SCM | SCM（Source Control Management，版本控制，這裡指 Git） |
| ACL | 防腐層（ACL，Anti-Corruption Layer；不是存取控制清單） |
| Port／Adapter | Port（領域程式需要的對外能力介面）／Adapter（接真實外部系統的實作） |
| Aggregate | Aggregate（聚合：必須一起保持一致的一組資料，只能從 Aggregate root 這個入口修改） |
| fingerprint | 金鑰指紋（fingerprint，辨識是哪一把金鑰，可公開） |
| pre-push hook | pre-push hook（push 前 Git 自動執行的檢查腳本） |
| attestation | 核准證明（attestation） |
| stale／missing／invalid | 過期（stale）／不存在（missing）／格式錯誤（invalid） |

## 也要修
- 機關式說法（「受治理的變更」「從套件外部驗證」「儀式感」）改成白話。
- 投影頁上的整行指令與參數改為講目的，指令留在 Runbook。
- 標題只寫指令名的，改成講目的的中文（並同步所有出現處）。
- 前後矛盾的說法（例如成功判準）統一。

## 不可動
程式碼區塊、`include`／`download` 指令與被引入內容、表單 id／type／選項值／檢核項目、規則編號、數字、時間、解鎖時點；不可新增禁用字串或外部網址；Runbook 不放主持提示或解答。
