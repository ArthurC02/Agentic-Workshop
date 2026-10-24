# DLC Speech：DDD 延伸課的概念與技巧講解

> 讀者：講者與教材維護者。時機：DDD 延伸課各段之後，講解該段背後的概念與 Agentic 開發技巧。前置：讀過 DLC Runbook 與 `CHECKPOINTS.md`。

本資料夾存放四場獨立講解的投影片原稿、講者備註與學員講義，教學方式與主課 [Speech](../../materials/speech/README.md) 相同：學員不寫程式、不讀程式、不打指令；頁面上的提示詞是示範，沒有實際執行的結果一律視為未驗證。每個概念只在第一次需要時講一次，之後的場次只加深。

## 四場講解

| 存放位置 | 對應段落 | 長度 | 頁數 | 第一次講的概念與技巧 |
|---|---|---|---|---|
| `01-language-boundary/` | 開場、D1 | 30 分鐘 | 17 | DDD 三句話、Agent 沒有走廊記憶（模型放 domain-memory、團隊決定寫進 AGENTS.md）、要證據不要形容詞、通用語言、候選、用 AI 讀舊系統（案例）、Agent 編出的名字、Bounded Context 與同字異義、先語言再邊界的擷取順序、多個訊號才劃邊界、從版本紀錄看一起變更、Context 畫布、Context Map、邊界洩漏 |
| `02-review-approval/` | D2 | 25 分鐘 | 13 | 決策紀錄（ADR）與已審查事實、做與核准分開（加深 Gate）、規則寫成檢查（AGENTS.md、Skill、hook 各放什麼）、Replit 與 AWS Kiro 警示案例、紀錄只放模型、審查表與審查方法、測試被改、反事實檢查（變異測試）、核准紀錄（誰、何時） |
| `03-domain-design/` | D3a–D3c | 40 分鐘 | 19 | 不變量、Aggregate、領域事件、定義寫「是什麼／不是什麼」、Port／Adapter 與防腐層、冪等、交給 Agent 列不變量與邊界選項、用反事實檢查守不變量、依領域模型讓 Agent 改舊系統（案例）、重構不等於模型變更 |
| `04-handoff-retro/` | D4、回顧 | 25 分鐘 | 13 | 交接要寫理由、用編號句子講領域、共用模型是外部記憶、人和 Agent 讀同一份模型、只准引用查得到的 id、模型漂移定期回收、提交前檢查擋下新漂移、用人審過的模型評估 Agent、團隊共用指示（AGENTS.md）與指示過長（多步驟流程移成 Skill）、成對簽章的限制、從一個 Context 導入 |

每場最後一頁銜接下一場；時間不足時，優先保留各場的概念頁，先砍示範提示詞頁。實際時間需現場確認，與 255 分鐘 DLC 流程的整合另行安排。

## 內容依據與邊界

- DLC Runbook：`../participant-runbook/content/`（開場、D1–D4、回顧與詞彙表）
- 檢查點對照：[CHECKPOINTS.md](../CHECKPOINTS.md)
- 引用來源只用 `.claude/skills/course-authoring/references.md` 列出的標題。

不公布 D3 三張需求卡的參考設計與負責 Context，不引用 `07-dlc-ddd/evaluation/` 的任何內容；簡報範例的 id 與行號僅示意。簡報不把效率數字當成本課程的結果；外部案例數字一律註明是對方自稱。

## 建置與檢查

與主課共用 `materials/speech/` 的建置腳本與版型，從 Repo 根目錄執行；不帶資料夾名稱時處理主課與 DLC 全部場次：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py [01-language-boundary …]
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py [01-language-boundary …]
```

每場的來源是 `src/stage.json` 與 `src/slides.json`；`*-deck.html` 與 `*-handout.md` 由建置產生，不要手改。溢出時刪減文字，不縮小版型。發布時由 `release-materials` 一併執行。
