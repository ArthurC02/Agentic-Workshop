---
id: greenfield
title: Greenfield 任務：核心訂票 MVP
minute: 07-30
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 任務：核心訂票 MVP

```callout info
現在在做什麼
- **情境**：Smart Ticket 是全新的車票預訂服務（Greenfield：從頭開始的專案），23 分鐘內要交出第一版。
- **你的目標**：帶著 Agent 做出 MVP（最小可行產品），能查班次、訂票、模擬付款、查訂單。
- **今天的技巧**：**給 Agent 一份規則；先要計畫再動手；小步執行、每步驗收**。規則寫進 `AGENTS.md`，錯了只要退一小步。
- **完成的樣子**：你在 `/docs` 親自試過訂票和付款；`notes/greenfield.md` 有計畫、每步的驗收對照表和交付摘要。
```

## 檢查點總覽

- **07–12 · 檢查點 1 交給 Agent 規則並備好環境**
- **12–17 · 檢查點 2 先要計畫，再核准**
- **17–24 · 檢查點 3 小步做、每步驗收**
- **24–30 · 檢查點 4 親自走一次流程並交付**

## 檢查點 1 · 交給 Agent 規則並備好環境（第 07–12 分鐘）

① 為什麼做這一步

規則寫進專案裡的 `AGENTS.md`，Agent 每次開工都會讀，提示詞就只要寫這次的事。再讓它建好環境、用 Git 存一版起點（Commit：專案在這一刻的存檔），之後才說得出「這次改了什麼」。

```download
id=g0 zip=participant-07-g0.zip label=下載 G0 Starter Repository
```

② 貼給 Agent

1. 按上方按鈕下載 `participant-07-g0.zip`，解壓縮到短路徑。Windows：在檔案上按右鍵選「全部解壓縮」，例如 `C:\work\g0`；macOS：把 ZIP 移到 `~/work` 再點兩下，會解到 `~/work/participant-07-g0`。
2. 在解壓後的 `agentic-workshop/01-greenfield/participant/starter-repository` 資料夾開啟 Agent。例如在編輯器用「開啟資料夾」選它，再開 Agent 對話。
3. 貼上：

```text
這是新專案 Smart Ticket，要在 23 分鐘內做出車票預訂服務的第一版。需求在上一層資料夾 01 到 05 開頭的五份 .md（讀不到就複製到 docs/ 再讀）。程式、測試和指令都交給你，我不讀程式。
這一步先把專案準備好，還不寫功能：
1. 照 04-agent-usage-guide.md，在專案根目錄寫 AGENTS.md（「怎麼跑」從 README 整理，「工作規則」照範本），再照範本建 check Skill：放在你這個工具會自動載入專案 Skill 的位置，並在 AGENTS.md 最後加一行它的位置（從專案根目錄算起的路徑）。
2. 照 AGENTS.md 建好環境、跑一次測試，用 Git 把現在的檔案存成「G0 baseline」，在 notes/greenfield.md 的「起點」記下測試數字。
做完告訴我 check Skill 的完整路徑，再用 check 檢查，最後一行寫成功或失敗。
```

Agent 建立 Skill 資料夾時，工具若跳出允許視窗，按允許。安裝約要 1 分鐘，等的時候先讀下方 ④ 的小卡。

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：AGENTS.md 和 check Skill 都在，有「G0 baseline」。
```

失敗時（其他狀況見 [環境準備](#environment) 頁「疑難排解」）：

```text
先停，不要再改。發生什麼事？你建議怎麼做？
```

④ 補充

```callout tip
技巧：規則寫進 AGENTS.md
**AGENTS.md 是放在專案根目錄、給 Agent 看的說明；多數 Coding Agent 開新對話會自動讀它。**
- 只放每次都要的事：怎麼跑、工作規則；一步步的固定做法另存成 Skill（例如 check），用得上時 Agent 才讀
- 它是提醒，不是強制：Agent 仍可能沒照做，所以每一步都要檢查
- 回到工作：先看你的專案有沒有 AGENTS.md；沒有就請 Agent 從 README 起草，你補上團隊規則
📖 延伸閱讀：OpenAI〈AGENTS.md〉、Claude Code 官方文件〈How Claude remembers your project〉、agentskills.io〈Agent Skills Overview〉；你所用工具的官方文件通常有同名章節。
```

起始測試應是 `1 passed, 8 skipped`（1 個通過、8 個跳過），以實際輸出為準。跳過（Skip）的測試代表功能還沒做。

## 檢查點 2 · 先要計畫，再核准（第 12–17 分鐘）

① 為什麼做這一步

先看計畫，動手前就抓得出範圍外的項目；這一步 Agent 只提計畫、不改程式。下面四件都成立就核准：

- 開頭三行（要什麼、為什麼、限制）和需求文件一致，沒有多加（不一致就回「開頭第 N 行不在需求文件裡，請刪掉重寫」）
- 每一步都標了規則編號和驗收條件編號（例如 `FARE-002`、`AC-G-005`），也寫了要改的檔案
- 沒有範圍外的項目
- 每個問題都附了建議答案；拿不準就舉手問主持人，不要讓 Agent 自己假設

② 貼給 Agent

先貼這段要計畫：

```text
先別改程式，給我一份 4 步的實作計畫，先仔細想過再回答。要做什麼看 01 到 03（任務說明、商業需求、驗收條件），程式裡標 TODO(GREENFIELD 的地方就是要補的；前端、登入、會員、優惠、改退票不在這次範圍。
固定拆成：1 票價、2 班次查詢、3 建立訂票、4 付款與查詢訂單；每一步都替它的驗收條件補上測試，不能只靠移除 skip。
寫進 notes/greenfield.md 的「計畫」：開頭三行寫要什麼、為什麼、限制（只照需求文件），下一行寫找到幾個 TODO(GREENFIELD；每一步寫完成後使用者能做什麼、對應的 Rule ID 和 AC、要改的檔案。需求文件沒寫清楚的列成問題，每題附建議答案。
```

看完計畫再貼這段「計畫核准」。不同意某個建議答案，就在第一行後面加上「第 N 題改成…」：

```text
計畫核准，問題照你建議的答案（我有改的寫在這一行後面）。
先做第 1、2 步，兩步很小、一起做，驗收對照表照步驟分開列。做完用 check 檢查，最後一行寫成功或失敗。
```

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：計畫寫的 TODO(GREENFIELD 數量，要和「G0 baseline」那一版的數量一致。
```

失敗時：

```text
先停，不要再改。哪一項不符、為什麼？你建議怎麼處理？
```

④ 補充

```callout tip
技巧：Prompt 結構
**交辦一件事，說清楚四樣：這次要什麼、為什麼、完成的樣子、素材在哪。**
- 規則和固定做法已在 AGENTS.md 與 Skill 裡，提示詞不用重寫
- 計畫開頭三行（要什麼、為什麼、限制）是請 Agent 先複述，你一眼就看出它有沒有理解錯
- 需求沒寫清楚的，讓 Agent 列成問題附建議答案，由你決定
📖 延伸閱讀：Anthropic 官方文件〈Prompt engineering overview〉與〈Prompting best practices〉、OpenAI 官方文件〈Prompt engineering〉；你所用工具的官方文件通常有同名章節。
```

Agent 應回報找到 11 個 `TODO(GREENFIELD` 標記（程式裡「這裡還沒做」的註記）。

Agent 在核准前就改檔案，貼：「先停。你改了哪些檔案？用 Git 還原到 G0 baseline（notes 資料夾保留），再重新只提計畫。」

## 檢查點 3 · 小步做、每步驗收（第 17–24 分鐘）

① 為什麼做這一步

每次只放行一小步，錯了只要退一小步。Agent 停下時，看它附的變更審查和驗收對照表（每條驗收條件一列的結果），判斷三件事：

- 改的檔案都在計畫裡（notes/ 不算）
- 測試數沒有變少，也沒有新增跳過
- 沒有刪除測試，也沒有改既有的期待值

第 3、4 步做完時，自己手算 T001 成人 700 ＋ 學生 525，再和驗收對照表 AC-G-005 的結果比對。

② 貼給 Agent

三件都成立，就貼這段「放行」。第 1、2 步放行後 Agent 會接著做第 3、4 步；第 3、4 步回報後三件也都成立，再貼同一段：

```text
這一段核准。把結果記進 notes/greenfield.md（段落用剛核准的步驟命名），再 Commit 成同樣的名稱。
剛核准的是第 1、2 步，就接著把第 3、4 步一起做；是第 3、4 步，就停下告訴我「計畫已全部完成」，不要自己加新功能。做完用 check 檢查，最後一行寫成功或失敗。
```

有一件不成立或不確定，改貼這段：

```text
這一步我先不核准。請用白話解釋審查裡有問題或我看不懂的地方，提出修正做法，等我同意再改。
```

③ 確認結果

Agent 說「計畫已全部完成」、最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼（時間不夠、只放行到第 1、2 步的，Agent 停下回報第 3、4 步時也貼這段）：

```text
用 check 檢查我最後放行的那一段。
```

失敗時：

```text
先停。哪一項不符、為什麼？已經開始的下一步先暫停；需要改程式就先提做法，等我同意再改。
```

④ 補充

```callout tip
技巧：Structured Output（結構化輸出）
**要求 Agent 用固定格式回報，人才看得快、能前後比對。**
- **驗收對照表**（每步都附）：編號、白話內容、結果、依據的測試名稱
- **變更審查**：你不讀程式，改看 Agent 用白話回答固定的幾題
- skip（略過測試）和 xfail（標成預期會失敗）都會把問題藏起來
- 格式寫在 AGENTS.md，Agent 仍可能漏欄，要檢查
📖 延伸閱讀：Anthropic 官方文件〈Structured outputs〉、OpenAI 官方文件〈Structured model outputs〉、Google Engineering Practices〈Google's Code Review Guidelines〉；你所用工具的官方文件通常有同名章節。
```

- 回報沒有變更審查：貼「照 AGENTS.md 工作規則第 6 條補上變更審查。」
- 建立訂票時 Agent 回報「把訂票結果轉成回應時出錯」（旅客資料無法轉換）：這是起始程式的已知小問題。貼「用最小的修改讓回應讀得到旅客資料，需要的話可以改 schemas/contracts.py（算在計畫內），不要改測試。」

```callout tip
時間不夠時
**第 24 分鐘還沒做完付款，就停在已核准的那一段。**
- 直接進入檢查點 4，驗證已做好的功能
- 沒做完的請 Agent 寫進交付摘要，不要硬趕
```

## 檢查點 4 · 親自走一次流程並交付（第 24–30 分鐘）

① 為什麼做這一步

不再加新功能。Agent 先啟動伺服器給你 `/docs` 網址，你親自試訂票和付款兩個 API；同時 Agent 補測試、寫交付摘要，其餘由它用測試驗證。你判斷 `/docs` 看到的是否和預期一致，照實回覆，以你看到的為準。

② 貼給 Agent

先貼這段。Agent 會先給你 `/docs` 網址，你邊試、它邊補測試和寫交付摘要：

```text
不再加新功能，準備交付：
1. 先啟動伺服器，啟動後馬上用一句話回我 /docs 網址（我會先去試訂票和付款），再接著做下面的事。
2. 我試的時候：AC-G-001～015 每條都要有測試，缺的補上，跑全套測試；最終驗收對照表寫進 notes/greenfield.md 的「最終驗收」。
3. 照 05-submission-checklist.md 的小標題寫「交付摘要」，README 和 docs/ 要改的地方照實際結果一起改；「人工驗證」先寫「待我確認」，然後停下。我會回你一行試用結果，你照寫，再 Commit 成「Greenfield 交付」，然後用 check 檢查，最後一行寫成功或失敗。
```

Agent 工作的時候，先到 [Greenfield 回顧與交付決定](#gf-submission) 填交付決定。

拿到網址後自己試訂票和付款。在瀏覽器開 Agent 告訴你的 `/docs` 網址（通常是 `http://127.0.0.1:8000/docs`；8000 被占用時 Agent 會改用 8001，以它給的為準），每個 API 都這樣試：

- 點開 API，按「Try it out」。
- 填參數，或在 Request body 貼上下方範例。
- 按「Execute」，看 Response 的狀態碼和內容。200 或 201 是成功，404 是找不到，409 是和目前狀態衝突。

依序試這兩個；查班次、查訂單和重複付款由 Agent 的測試驗證：

1. `POST /bookings`：把下方範例貼到 Request body，確認 `total_fare` 和你手算的一樣（1225）、`status` 為 `PENDING_PAYMENT`，記下 `booking_id`。
2. `POST /bookings/{booking_id}/pay`：填入 `booking_id`，確認回傳的 Order `amount` 也是 1225、`payment_status` 為 `SUCCESS`。

```text
{
  "trip_id": "T001",
  "passengers": [
    {"passenger_id": "P1", "name": "測試旅客一", "passenger_type": "ADULT"},
    {"passenger_id": "P2", "name": "測試旅客二", "passenger_type": "STUDENT"}
  ]
}
```

伺服器重啟後，資料會回到初始狀態，這是刻意的設計。試完回 Agent 一行，例如：

```text
兩項都一致
```

不一致就回「第 N 項不一致：我看到…」。

③ 確認結果

Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：

```text
用 check 檢查剛才這一段：「人工驗證」已照我的回覆寫入，沒有未 Commit 的變更。
```

失敗時（第 30 分鐘就停止修改，如實交付）：

```text
不要再改程式。缺的補進 notes/greenfield.md；做不完的照實寫完成到哪、哪些未驗證，Commit 成「Greenfield 交付」後告訴我。
```
