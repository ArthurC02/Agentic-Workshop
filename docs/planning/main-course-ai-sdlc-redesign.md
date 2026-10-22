# 主課程依 AI-native SDLC 改造設計（草案，2026-10-22）

> 狀態：設計提案，尚未改任何教材。依據：Anthropic〈The AI-native SDLC playbook〉（2026-08-21）與〈How Anthropic secures its AI-native software development lifecycle〉（2026-07-21）；引文與查核紀錄見 `docs/research/speech-agentic-sources.md`「2026-10-22 AI-native SDLC 查核」。Skilljar 沒有名為「AI SDLC」的課，最接近的官方內容是這份 playbook。

## 0. 一句話結論

主課程已經教了 playbook 最核心的兩件事：計畫核准（"Nothing is implemented without an accepted plan."）與完成前驗證（驗收對照表、「未驗證」）。缺口集中在三處：產物沒有排成一條「意圖 → 規格 → 計畫 → 驗證 → 審查」的鏈；寫程式的 Agent 自己回答變更審查，沒有獨立審查者；Maintain、指標與設定評估只停在講解。改造原則：不加分鐘、不加新檔，讓既有產物照 playbook 的鏈命名與串接，講不完的交給講解簡報與講義。

## 1. 對照表

### 1.1 各段落目前教到哪個階段

| 段落（分鐘） | 主要 SDLC 階段 | 產物 | 關卡 |
|---|---|---|---|
| 開場 00–07 | — | — | — |
| Greenfield CP1 07–11 | Build（規則檔） | 工作規則 7 條、`notes/greenfield.md`「起點」、Commit「G0 baseline」 | — |
| Greenfield CP2 11–15 | Plan＋Build（計畫） | 「計畫」4 步、「核准紀錄」 | **計畫核准**（人） |
| Greenfield CP3 15–25 | Build＋Test | 每步驗收對照表、四題變更審查、Commit | 每步放行（人） |
| Greenfield CP4 25–29 | Test＋交付 | 「最終驗收」「交付摘要」、`/docs` 人工驗證 | 交付決定表單 |
| Time Skip 29–33 | Maintain（接手） | `notes/time-skip.md` | 規則複述 |
| 個人分析 33–39 | Maintain → Plan | `notes/analysis.md`（事實／假設／缺口） | — |
| 共同脈絡 39–44 | Build（團隊設定） | `notes/shared-context.md`、`skills/team-rules.md`、角色「人員核准者」 | 小組確認表單 |
| B1 44–52 | Maintain（事故）→ Build → Test | `notes/b1.md`、`skills/fix-bug-with-test.md` | 修正計畫核准、三題審查、接受修正 |
| B2 52–63 | Design → Plan → Build → Test | `notes/b2.md` 方案比較／核准／變更審查／驗證與交付、ADR 狀態 | 方案核准、過時期待值核准、五題審查、接受交付 |
| B3 63–76 | Plan → Design → Build → Test | `b3-docs/`（任務卡、工作單、交付範本）、`skills/b3-work-order.md`、`notes/b3.md` | Gate 1 需求、Gate 2 設計與範圍＋「開始執行」、例外事件、Gate 3 交付 |
| 交付 76–80 | Deploy（放行決定） | `notes/delivery.md` 十二欄、Level | 交付核對表單 |
| 回顧 80–90 | Maintain（回寫）＋導入 | `notes/my-prompts.md`、自己的 Skill、帶回團隊的行動 | — |

### 1.2 Playbook 元素的覆蓋程度

| Playbook 元素 | 程度 | 說明 |
|---|---|---|
| 計畫核准才動手 | **強** | Greenfield、B1、B2、B3 Gate 2 都有，核准人與時間由 Agent 記錄 |
| 完成前驗證（"Run the tests before reporting a task complete, and show the output."） | **強** | 驗收對照表、測試數不減、不加 skip，沒跑的標「未驗證」 |
| 團隊設定（CLAUDE.md、Skills） | **強** | `skills/team-rules.md`、三個 Skill；講解 03 第 8–11 頁 |
| 稽核軌跡（"the intent, the spec, the plan, the diff and the review findings are the audit trail"） | 強 | `notes/` 加上 Commit；講解 04 第 18 頁 |
| 意圖產物（intent.md） | **弱** | 需求由課程提供，學員沒有確認「要什麼、為什麼、限制」這一步；B3 Gate 1 其實就在做這件事，只是沒有這樣命名 |
| 規格產物（spec.md） | 弱 | B3 Gate 2 把規格和計畫混在一起；講解 01 第 8 頁只有示範 |
| 寫的人不能核准（"the agent that wrote the code has no way to approve it"） | **弱** | 講解 04 第 10、16、18 頁有教；實作中變更審查與「自我檢查：成功」都由寫程式的 Agent 自己回答 |
| 審查準則檔（REVIEW.md） | **缺** | 審查題目散在工作規則第 6 條、B2 五題、工作單 §7 |
| 上線放行關卡（"may act up to the production gate and cannot pass it"） | 弱 | Gate 3 加上交付 Level 是唯一的放行；講解 04 第 7、14、19 頁 |
| Agent 設定的評估（evals） | **缺** | 學員寫了 Skill，但從沒試跑過 |
| Maintain 觸發（control bands → 新 intent） | **缺** | B1 由客服回報開始，但沒有把「未完成」接回下一輪 |
| 領先／落後指標 | 缺（只有講解） | 講解 05 第 8 頁列了指標，沒分領先與落後；回顧的行動只寫「用什麼證據確認」 |
| 角色分工 | 弱 | 只有一位「人員核准者」；playbook 把核准分給產品負責人、工程師、技術負責人、上線負責人 |
| 依賴圖、先唯讀再寫（"starts with read-only judgment steps"） | 隱含 | Tool → Teammate → Digital Worker 已經是逐步放權；講解沒有點出來 |

## 2. 改造提案（依每分鐘的學習價值排序）

每項都寫出換掉什麼。除非特別註明，都不動分鐘、解鎖碼、表單 id、四段式結構，也不出現工具專屬名稱。

**P1　交付加入「獨立審查對話」：寫的人不核准自己**
- **改什麼**：交付檢查點 1 的 ③，改成在同一台電腦**開一個新對話**當審查者。它只讀 `notes/b3.md`、工作單 §4 與 §7，用 `git diff` 對照「B3 起點」。它把發現分成「重要／小問題」，寫進 `notes/b3.md` 的「審查紀錄」，最後一句是「建議放行／不建議放行」，不改任何檔案。主要 Agent 寫摘要時，審查對話同時跑。人看兩份結論後再選 Level。
- **為什麼**：「Separation of duties is preserved, because the agent that wrote the code has no way to approve it.」講解 04 第 16 頁已經教了「另開乾淨對話審」，實作卻沒練到。
- **換掉什麼**：交付提示詞結尾的寫作者自我檢查，以及 ③ 的成功／失敗提示詞。審查對話的回覆就是 ③。「三句話抽查」保留。
- **風險**：76–78 分鐘很緊；有些工具一次只能開一個對話，這時改成「主要 Agent 寫完後開新對話審」，要多約 1 分鐘。審查對話可能自己動手修，提示詞要寫明「只讀、不修改」。
- **檔案**：`70-delivery.md`、`b3-work-order.md` §10、`05-delivery-template.md`（Recommended Decision 要引用審查紀錄）、`facilitator-deck/src/slides/70-delivery.html`、詞彙表。

**P2　B3 三道 Gate 改名為「意圖 → 規格 → 計畫」的鏈**
- **改什麼**：任務卡就是意圖。Gate 1 改成「確認意圖：要什麼、為什麼、限制」。Gate 2 卡分兩節：「規格（行為與驗收條件）」和「計畫（改哪些檔、步驟、測試）」。「開始執行」明確叫做計畫核准。`notes/b3.md` 段落仍叫「Gate N」，標題後面加上階段名。
- **為什麼**：「Every stage commits an artifact the next stage can read.」B3 已經有三道關卡，只差把產物的名字對上。
- **換掉什麼**：Gate 1／2 卡的標題列和兩行 ①，不增加題目數。Gate 2 現有 5 題改歸兩節。
- **風險**：Gate 2 卡多了小標，讀卡時間可能增加約 15 秒。`check_deck_runbook.py` 會比對 Gate 名稱和分鐘，Gate 名稱和 66／69／75 都不能動。
- **檔案**：`b3-work-order.md` §5、`60-b3-overview.md` CP2–3 的 ①、`03-b3-group-booking.md` 引言、B3 投影片、`88-glossary.md`（新增「意圖」「規格」）。

**P3　工作單 §7 變更審查改寫成「審查準則」，各段共用**
- **改什麼**：把工作規則第 6 條、B2 五題、工作單 §7 三題整理成同一份「審查準則」：哪些算「重要」（超出核准範圍、測試變少、改了期待值、宣稱通過卻沒證據）、哪些不用報、一定要查什麼。這份準則放在 `skills/team-rules.md` 的新一節，由共同脈絡 CP2 建立。B2 和 B3 改為「依審查準則」。
- **為什麼**：「`REVIEW.md`: instructions for reviews alone. Use it to say what your team wants flagged, at what severity, and what to skip.」準則由人定，寫的人和審的人讀同一份，P1 的審查對話也有依據。
- **換掉什麼**：B2 CP2 ② 和工作單 §7 重複列出的審查題目，提示詞因此變短。不加新檔。
- **風險**：team-rules.md 變長，共同脈絡 CP2 的提示詞與 ③ 要改；Recovery 包裡的 `skills/team-rules.md` 也要重建。
- **檔案**：`39-shared-context.md`、`52-b2.md`、`b3-work-order.md`、`04-shared-context-template.md`、`make_recovery.py` 產出、Recovery 頁。

**P4　交付的「未完成」接成下一輪的意圖（Maintain 回到 Plan）**
- **改什麼**：交付範本的 Not Implemented 欄，「下一步」改成三行下一輪意圖：要什麼、為什麼、限制。回顧 CP3 的行動格式加兩欄：「兩週內看得到的領先指標」「一季後看的落後指標」。
- **為什麼**：「Any breached control band is diagnosed and written back into the loop.」playbook 每個 play 都有 "Leading indicator"／"Lagging indicator"。
- **換掉什麼**：範本裡的「下一步：____」，以及行動格式的「用什麼證據確認」（後者併入兩個指標）。表單 `action` 仍是 text，id 不變。
- **風險**：學員可能分不清領先和落後指標，所以 Agent 提候選時要各附一個例子（例如「每週退回次數」和「上線後才發現的問題數」）。
- **檔案**：`05-delivery-template.md`、`80-retrospective.md` CP3、`reflection-sheet.md`、回顧投影片。

**P5　回顧 CP2：新 Skill 試跑一次才收（最小的 eval）**
- **改什麼**：Agent 寫好 Skill 檔後，用今天 notes 裡的一個例子，在新對話照 Skill 走一遍（只讀、不改檔），回報「照做了／哪一步沒照做」，必要時改一句再收。
- **為什麼**：「Evals are the AI-native equivalent of stage-gate QA.」「Gate configuration changes on the results.」Skill 就是 Agent 的設定，改了要先試。
- **換掉什麼**：CP2 ④ 的「快速模型 vs 強模型」討論。這個主題在 B2 和講解 03 第 5–6 頁已經教過。
- **風險**：82–86 分鐘只有 4 分鐘，試跑可能超時，所以要設成「可選、時間不夠就跳過」。
- **檔案**：`80-retrospective.md`、回顧投影片、`reflection-sheet.md`。

**P6　Greenfield CP2 的計畫開頭加三行「意圖」（零分鐘）**
- **改什麼**：計畫提示詞的輸出格式，在開頭加一行：先用三行寫出意圖（要什麼、為什麼、限制）。① 的核准條件加「意圖和需求文件一致」。
- **為什麼**：intent 是 "what is wanted, why, and under which constraints"，在最早的段落就讓學員看到這個鏈。
- **換掉什麼**：計畫開頭原本的「TODO 數量」那一句改放到第二行，不刪除。
- **風險**：③ 的檢查要多驗一項；需要重新演練 CP2。
- **檔案**：`10-greenfield.md`、`20-greenfield.html`。

**P7　講解簡報與講義補上實作做不到的部分**（Phase C）
- **講解 04**：
  - 新增 1 頁「規則提醒 vs 機制把關」，引用 "A skill is an advisory control while a hook is the deterministic layer behind it."
  - 第 7 頁補上放行關卡：Agent 最多做到上線前，不能自己上線。
  - 第 18 頁補「先唯讀判斷、再開放寫入、再逐個環境放權」，對應今天 Tool → Teammate → Digital Worker 的順序。
- **講解 05**：
  - 第 8 頁拆成領先／落後指標。
  - 新增 1 頁「出事後回到下一輪意圖」（control bands 的工具中立版）。
  - 第 12 頁的 30 天計畫，改成依 playbook 依賴圖排序。
- **講解 01**：第 7–8 頁把 idea → spec 的示範改成「意圖 → 規格 → 計畫」三段式，和 B3 用同一組詞。
- 每頁都只新增或替換，總頁數上限是 +2，對應的講義與名詞解釋一併更新。

## 3. 分期計畫

| 期 | 內容 | 檔案 | 演練 |
|---|---|---|---|
| **A 措辭與命名** | P2（只改標題與 ①）、P4 的範本欄位、詞彙表新增「意圖」「規格」「審查準則」「領先／落後指標」、對應投影片標題 | `60-b3-overview.md`、`b3-work-order.md` §5 標題、`05-delivery-template.md`、`88-glossary.md`、`60-b3-digital-worker.html`、`70-delivery.html` | `check_deck_runbook.py`、`check_references.py`、`check_zh_tw.py`；B3 Gate 卡跑一次 rehearsal |
| **B 檢查點與提示詞** | P1、P3、P5、P6、P4 的回顧格式 | `10-greenfield.md`、`39-shared-context.md`、`52-b2.md`、`70-delivery.md`、`80-retrospective.md`、`b3-work-order.md`、`04-shared-context-template.md`、Recovery 包、投影片 | 完整 rehearsal 兩輪（Windows、macOS 各一）；要計時 76–80 與 82–86；用 Recovery 路徑跑一次 B3 → 交付；`curriculum-review` |
| **C 講解與講義** | P7 | `speech/01,04,05/src/slides.json`、`stage.json`、講義 | `fact-check`（新增引文）、`plain-language-review`、`release-materials` |

順序：A → C 可以先發布。B 要等演練確認 76–80 不超時才上。

## 4. 待使用者決定

1. **交付要不要開第二個對話當審查者（P1）？** 建議：要，這是投入產出比最高的一項。分鐘不變，審查和寫摘要並行；工具不能並行時，退回「寫完再審」，交付第 76–80 分可能要借用回顧的 1 分鐘（回顧變 80→81 開始）。
2. **要不要增加分鐘或新增一個「Maintain／上線」段落？** 建議：不要。90 分鐘已經排滿，Maintain、放行關卡和指標放在講解 04／05。實作只做 P4 的「接回下一輪意圖」。
3. **學員頁要不要直接使用 intent.md、spec.md、REVIEW.md 這些檔名？** 建議：不要。學員頁用「意圖」「規格」「計畫」「審查準則」，不新增檔案；playbook 標題只出現在 📖 延伸閱讀，並加上「你所用工具的官方文件通常有同名章節」。
4. **審查準則（P3）放在 `skills/team-rules.md` 還是 B3 文件包的新檔？** 建議：放在 team-rules.md 的新一節，從 B1 起就能用，也不違反「文件包只放流程用得到的檔」。
5. **核准角色要不要拆成三種（需求、計畫、交付）？** 建議：暫時不拆。小組通常只有 3–4 人，表單選項值也不能改；只在講解 04 說明 playbook 的角色分工，Gate 卡維持一位核准者。
6. **回顧的 Skill 試跑（P5）要必做還是選做？** 建議：選做。先演練量時間，穩定在 4 分鐘內再改成必做。
