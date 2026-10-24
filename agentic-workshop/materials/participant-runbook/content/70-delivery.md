---
id: delivery
title: Delivery Summary 與交付
minute: 99-105
group: b3
section: Delivery
---

# 交付：請 Agent 整理交付摘要，人核對

```callout info
現在在做什麼
- **情境**：B3 時間到了。主管要一份交付摘要，寫清楚做了什麼、證據在哪、還缺什麼，才能決定收不收。
- **你的目標**：請 Agent 依實際證據寫交付摘要，你抽查證據後交件。
- **今天的技巧**：**請 Agent 整理交付摘要，人核對**。每一句都要指得出證據，沒驗證的如實標「未驗證」。
- **完成的樣子**：`notes/delivery.md` 有附證據來源的交付摘要和完成等級，`notes/b3.md` 有另一個對話寫的審查紀錄；你選了 Level、勾了交件。
```

## 檢查點總覽

- **99–104 · 檢查點 1 請 Agent 寫交付摘要，你來核對**
- **104–105 · 檢查點 2 匯出與交件（約 30 秒）**

## 檢查點 1 · 請 Agent 寫交付摘要，你來核對（第 99–104 分鐘）

① 為什麼做這一步

第 99 分鐘停止一切修改。寫程式的 Agent 不核准自己的成果，所以另開一個只讀的審查對話，照審查準則把結論寫進 `notes/b3.md` 的「審查紀錄」。你核對：

- Agent 給的三句話（Level、測試結果、修改範圍）都引用得出證據原文，引用不出的已改成「未驗證」
- 審查紀錄有沒有「重要」問題；有的話，Level 照證據選，Gate 3 的「核准」紀錄不改，不同意見寫進 Risks and Limitations
- Gate 決策和 `notes/b3.md` 一致

② 貼給 Agent

1. 複製下方提示詞貼給主要 Agent；交付摘要範本（Delivery Summary）已在 B3 文件包裡，Agent 會自己讀。它會先核對 B3 的 Gate 3 紀錄：有 Gate 3 卡但缺你的決定就問你，回「核准」「附條件：…」或「退回：…」即可；還沒有 Gate 3 卡（Recovery 組時間到）就記「未進行」，不問你。
2. 主要 Agent 開始寫摘要後，在同一台電腦、同一個專案資料夾**開一個新對話**，貼 ③ 的審查提示詞，兩邊同時跑。工具一次只能開一個對話時，等主要 Agent 回完三句話再開新對話貼。

```text
B3 時間到，不再改程式，請寫交付摘要給主管：照 b3-docs/delivery-template.md 寫進 notes/delivery.md，素材只用 notes/b3.md。每一欄附證據位置，找不到證據的寫「未驗證」；Level 依證據選，不自動選 Level 3。notes/b3.md 有 Gate 3 卡但缺我的決定，就附卡上的建議先問我一句；還沒有 Gate 3 卡，就在「Gate 3」寫「未進行（時間到）」，不要補問。另一個對話會同時審查這次的修改、寫進 notes/b3.md 的「審查紀錄」，那一節你不要動，也不用等它。
寫完給我三句話：建議的 Level、測試結果、修改範圍，每句後面引用證據原文和位置；再告訴我 notes 資料夾的完整路徑。
```

等 Agent 寫摘要時，和小組聊 30 秒：Agent 建議的 Level 你們同意嗎？加上 Gate 紀錄、審查紀錄和缺項後，還會選同一級嗎？

③ 確認結果

在新對話貼這段審查提示詞。它的回覆就是這一步的確認結果：最後一行回「成功」就往下；回「失敗」就貼下方「失敗時」。新對話會自己讀 `AGENTS.md` 的審查準則。

```text
你是這次交付的審查者，不是寫程式的人，只讀不改。照 AGENTS.md 的審查準則審 B3 的修改：起點是「B3 起點」Commit（含 git status 列出、還沒 Commit 的新檔），核准範圍看 b3-docs/b3-work-order.md 第 4 節和 notes/b3.md 裡 Gate 2 核准的計畫；不要讀 notes/delivery.md。自己執行指令，比對 notes/b3.md 寫的和你看到的是否一致。
結論寫進 notes/b3.md 最後的「審查紀錄」，最後一行寫「結論：建議放行」或「結論：不建議放行（一句原因）」。最後用 check 檢查：這個對話除了 notes/b3.md 沒有改任何檔案（對照你開始時的 git status）。對話只回四行：重要幾條、小問題幾條、結論，最後一行是 check 的結果。
```

失敗時（在審查對話貼）：

```text
先停。剛才哪一步沒做到？改到 notes/b3.md「審查紀錄」以外的檔案就用 Git 還原，再照審查準則重寫「審查紀錄」。
```

審查紀錄有「重要」問題時，對主要 Agent 貼（不用自己挑句子）：

```text
審查紀錄列了重要問題：照抄進 notes/delivery.md 的 Risks and Limitations。摘要裡和審查紀錄對不上的句子改成「未驗證」並寫原因；Level 照證據選。Gate 3 的紀錄保留原樣，審查和 Gate 3 說法不同的地方也寫進 Risks and Limitations。用白話告訴我改了哪幾句。
```

摘要有句子你看不懂、覺得證據對不上時，對主要 Agent 貼，再接上那幾句：

```text
摘要裡這幾句我看不懂或覺得證據對不上：請用白話重講，引用 notes/b3.md 的原文。對不上的在 notes/delivery.md 改成「未驗證」並寫原因。
```

④ 補充

```callout tip
技巧：另開對話審查
**寫程式的 Agent 不核准自己的成果；另開一個只讀的對話，照同一份審查準則審。**
- 新對話沒看過寫程式的過程，只看檔案和指令結果，不替自己辯護
- 審查準則由人定，寫的人和審的人讀同一份
- 回到工作：審查的對話只報告、不修改，要不要放行由人決定
📖 延伸閱讀：Anthropic〈The AI-native SDLC playbook〉、Claude Code 官方文件〈Best practices for Claude Code〉；你所用工具的官方文件通常有同名章節。
```

```callout tip
技巧：Structured Output（結構化輸出，加深一層）
**這次多一層：每一句都要附證據位置。**
- 交付摘要固定十二個標題，你只要一欄一欄問「證據在哪？」
📖 延伸閱讀：Anthropic 官方文件〈Structured outputs〉、OpenAI 官方文件〈Structured model outputs〉；你所用工具的官方文件通常有同名章節。
```

## 檢查點 2 · 匯出與交件（第 104–105 分鐘）

① 為什麼做這一步

要匯出才算交件，約 30 秒。把檢查點 1 聊好的 Level 與抽查結果記進表單，再匯出。

② 貼給 Agent

Agent 在檢查點 1 已告訴你 `notes/` 的完整路徑，就跳過 ② ③，直接填下方表單。沒給才貼：

```text
告訴我這個專案 notes 資料夾的完整路徑，列出裡面的檔案。
```

③ 確認結果

只有貼了 ② 才需要：

```text
用 check 檢查剛才這一段：notes 裡有 b3.md 和 delivery.md，delivery.md 寫了 Completion Level。
```

失敗時：

```text
先停。notes/b3.md 和 notes/delivery.md 實際在哪個資料夾？delivery.md 缺了什麼？
```

把結論記在下方表單，再按下方「下載全部填寫內容（ZIP）」：ZIP 裡每份表單一個 Markdown（.md）檔；瀏覽器擋下載時，改按各表單的「匯出 Markdown」。

```form
{"id": "delivery-check", "title": "交付核對（任務 ID：TASK-B3-001）","fields":[
{"id": "level", "label": "核對後的完成等級", "type": "select", "options": ["Level 1：分析完成（Analysis Complete）", "Level 2：核心流程完成（Core Flow Complete）", "Level 3：完整交付（Delivery Complete）"], "hint": "依 notes/delivery.md 的證據擇一，不自動選 Level 3。"},
{"id": "evidence-cited", "label": "抽查的三句都指得出證據嗎？", "type": "select", "options": ["是", "否，已請 Agent 改成未驗證", "不確定"]},
{"id": "handed-in", "label": "我會匯出表單，連同 notes 資料夾交件", "type": "checkbox"}
]}
```

```exportall
```

依主持人指定方式交件：匯出的表單 ZIP，加上主要 Agent 電腦上的 `notes/` 資料夾。主要 Agent 那位同時把 `notes/`、`AGENTS.md` 和 Skill 資料夾傳給組員，回顧要用。

```callout sync
⏸ 看投影：交件後請先停手，一起看 B3 揭曉
交件後不再修改交付摘要、Level 或任何表單；第 105 分鐘進入回顧。
```

## 完成後想一想

先自己想 30 秒，再和旁邊的人聊；趁等 Agent 回報時聊，這段不另開全場分享。

1. **觀察**：你抽查的三句裡，有沒有哪一句引用不出證據、被改成「未驗證」？審查對話找到的問題，寫程式的 Agent 自己有提到嗎？
2. **技巧**：如果交付摘要讓 Agent 自由發揮、不要求每句附證據，你要怎麼分辨哪些是真的做到、哪些只是它「覺得」做到？你工作上的週報或交接文件，哪幾欄值得固定下來？
3. **延伸**：今天的交付只看證據、不看程式。回到公司，誰應該替這份交付簽名負責？他還需要看到什麼？
