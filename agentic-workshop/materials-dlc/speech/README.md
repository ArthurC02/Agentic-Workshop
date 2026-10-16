# DLC Speech：DDD 延伸課的概念與技巧講解

> 讀者：講者與教材維護者。時機：DDD 延伸課各段之後，講解該段背後的概念與 Agentic 開發技巧。前置：讀過 DLC Runbook 與 `CHECKPOINTS.md`。

本資料夾存放四場獨立講解的投影片原稿、講者備註與學員講義，教學方式與主課 [Speech](../../materials/speech/README.md) 相同：學員不寫程式、不讀程式、不打指令；頁面上的提示詞是示範，沒有實際執行的結果一律視為未驗證。每個概念只在第一次需要時講一次，之後的場次只加深。

## 四場講解

| 存放位置 | 對應段落 | 長度 | 頁數 | 第一次講的概念與技巧 |
|---|---|---|---|---|
| `01-language-boundary/` | 開場、D1 | 30 分鐘 | 12 | 先講好什麼算成功、只能靠人抓的錯、候選、通用語言、Bounded Context、邊界洩漏 |
| `02-review-approval/` | D2 | 25 分鐘 | 11 | 做與核准分開（加深 Gate）、變更審查包、反事實檢查、核准紀錄、已審查事實 |
| `03-domain-design/` | D3a–D3c | 40 分鐘 | 17 | 需求卡是唯一依據、負責的 Context、Port／Adapter 與防腐層、冪等、不變量、預留與歸還、Aggregate、交接單（加深工作單） |
| `04-handoff-retro/` | D4、回顧 | 25 分鐘 | 11 | 模型落後程式、交接單七段、只准引用查得到的 id、從紀錄整理證據、成對簽章的限制 |

每場最後一頁銜接下一場；時間不足時，優先保留各場的概念頁，先砍示範提示詞頁。實際時間需現場確認，與 180 分鐘 DLC 流程的整合另行安排。

## 內容依據與邊界

- DLC Runbook：`../participant-runbook/content/`（開場、D1–D4、回顧與詞彙表）
- 檢查點對照：[CHECKPOINTS.md](../CHECKPOINTS.md)
- 引用來源只用 `.claude/skills/course-authoring/references.md` 列出的標題。

不公布 D3 三張需求卡的參考設計與負責 Context，不引用 `07-dlc-ddd/evaluation/` 的任何內容；簡報範例的 id 與行號僅示意。本工作坊未量測效率，簡報不引用此類數字。

## 建置與檢查

與主課共用 `materials/speech/` 的建置腳本與版型，從 Repo 根目錄執行；不帶資料夾名稱時處理主課與 DLC 全部場次：

```powershell
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py [01-language-boundary …]
py -3.13 -X utf8 agentic-workshop/materials/speech/build_decks.py --check
py -3.13 -X utf8 agentic-workshop/materials/speech/verify_browser.py [01-language-boundary …]
```

每場的來源是 `src/stage.json` 與 `src/slides.json`；`*-deck.html` 與 `*-handout.md` 由建置產生，不要手改。溢出時刪減文字，不縮小版型。發布時由 `release-materials` 一併執行。
