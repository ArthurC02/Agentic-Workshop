---
id: greenfield
title: Greenfield 任務：核心訂票 MVP
minute: 07-29
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 任務：核心訂票 MVP

```callout info
現在在做什麼
- **情境**：Smart Ticket 是全新的車票預訂服務（Greenfield：從頭開始的專案），22 分鐘內要交出第一版。
- **你的目標**：帶著 Agent 做出 MVP（最小可行產品）：查班次 → 訂票 → 模擬付款 → 查訂單。
- **今天的技巧**：**給 Agent 一份規則；先要計畫再動手；小步執行、每步驗收**。錯了只要退一小步。
- **完成的樣子**：你在 `/docs` 走完整流程；`notes/greenfield.md` 有計畫、每步的驗收對照表和交付摘要。
```

## 先貼給 Agent：工作規則

在檢查點 1 開啟 Agent 後，第一件事就是把下面整段貼給它；開了新對話也要重貼。這段是給 Agent 的，不需要看懂。

```callout tip
技巧：給 Agent 一份工作規則
規則先講好，之後每一步就不用重複叮嚀「先計畫」「做完停下」「附測試結果」。
📖 延伸閱讀：Claude Code 官方文件〈Best practices for Claude Code〉、OpenAI Codex 官方文件〈Custom instructions with AGENTS.md〉、GitHub 官方文件 Copilot〈Adding repository custom instructions for GitHub Copilot〉；你所用工具的官方文件通常有同名章節。
```

```text
以下是這次工作的規則，請在整段對話中遵守：
1. 你負責所有程式、測試與指令操作；我不會自己修改程式，也不會自己讀程式，請用白話向我說明。
2. 每次修改前先提出計畫，等我核准；只做核准的步驟，做完就停下來等我。
3. 商業規則放在 domain／application，Router 只做輸入輸出轉換；不新增套件、不改 Seed 資料、不動 /health。
4. 功能完成才移除對應的 skip；不得修改或刪除既有測試的斷言，不得用 skip／xfail 隱藏失敗。
5. 每次做完都執行 pytest -q，並用「驗收對照表」回報：每條驗收條件或規則一列，欄位固定為「編號、白話內容、結果（通過／失敗／未驗證）、依據的測試名稱」，最後一行寫通過／失敗／跳過的測試數。不要貼原始輸出，只給摘要。
6. 每次修改後，接在驗收對照表後面用白話回答四題審查問題，並附你實際執行的指令：(1) 改了哪些檔案、各改了什麼、為什麼，有沒有不在核准計畫裡的檔案（notes/ 不算）；(2) 測試總數有沒有比上一次少，有沒有新增 skip 或 xfail；(3) 有沒有刪除測試或修改既有測試的期待值（用 git diff 檢查 tests 資料夾）；(4) 這一步讓哪些原本跳過的測試變成通過。最後用一句話建議「可以放行」或「不建議放行（原因）」。
7. 你沒有實際執行的事情，一律標「未驗證」。
```

## 檢查點總覽

- **07–09 · 檢查點 1 交給 Agent 規則並備好環境**
- **09–11 · 檢查點 2 先要計畫，再核准**
- **11–24 · 檢查點 3 小步做、每步驗收**
- **24–29 · 檢查點 4 親自走一次流程並交付**

## 檢查點 1 · 交給 Agent 規則並備好環境（第 07–09 分鐘）

① 為什麼做這一步

規則先講好，再讓 Agent 建好環境、用 Git 記下起點，之後它才說得出「這次改了什麼」。

```download
id=g0 zip=participant-07-g0.zip label=下載 G0 Starter Repository
```

② 貼給 Agent

下載 `g0.zip`，解壓縮到短路徑（Windows：在檔案上按右鍵選「全部解壓縮」，例如 `C:\work\g0`；macOS：點兩下解壓縮，例如 `~/work/g0`）。在解壓後的 `agentic-workshop/01-greenfield/participant/starter-repository` 資料夾開啟你的 Agent（例如在編輯器用「開啟資料夾」選這個資料夾，再開 Agent 對話），先貼上方的「工作規則」，再貼這段（給 Agent 的，不需要看懂）：

```prompt
# windows
請幫我把這個專案準備好，做完用白話回報，不要修改任何程式：
1. 用 py -3.13 -m venv .venv 建立虛擬環境。不必啟用 venv，之後一律直接呼叫 .venv\Scripts\python.exe（Git Bash 寫 .venv/Scripts/python.exe），例如 .venv\Scripts\python.exe -m pip install -r requirements.txt、.venv\Scripts\python.exe -m pytest -q。版本不是 3.13 或找不到 3.13 就停下告訴我，不要改用其他版本。安裝完執行 pytest -q，告訴我測試有幾個通過／失敗／跳過。
2. 確認你讀得到上一層資料夾的 01 到 05 開頭的五份 .md 文件；讀不到就把這五份都複製到 docs\ 資料夾，之後提到上一層的文件都改讀 docs\ 裡的副本。
3. 建立 Git 基準：初始化 Git，把目前所有檔案 Commit 成「G0 baseline」。如果 Git 要求姓名或 Email，只在本資料夾設定（不要用 --global），名字用「workshop」、Email 用「you@example.com」。電腦沒有 Git 就告訴我你改用什麼方式記錄起始狀態。
4. 建立 notes/greenfield.md，第一段「起點」寫下測試數字與 Git 基準是否建立。
遇到錯誤時先說明原因，不要自行修改程式。做完停下等我。
# macos
請幫我把這個專案準備好，做完用白話回報，不要修改任何程式：
1. 用 python3.13 -m venv .venv 建立虛擬環境。不必啟用 venv，之後一律直接呼叫 .venv/bin/python，例如 .venv/bin/python -m pip install -r requirements.txt、.venv/bin/python -m pytest -q。版本不是 3.13 或找不到 3.13 就停下告訴我，不要改用其他版本。安裝完執行 pytest -q，告訴我測試有幾個通過／失敗／跳過。
2. 確認你讀得到上一層資料夾的 01 到 05 開頭的五份 .md 文件；讀不到就把這五份都複製到 docs/ 資料夾，之後提到上一層的文件都改讀 docs/ 裡的副本。
3. 建立 Git 基準：初始化 Git，把目前所有檔案 Commit 成「G0 baseline」。如果 Git 要求姓名或 Email，只在本資料夾設定（不要用 --global），名字用「workshop」、Email 用「you@example.com」。電腦沒有 Git 就告訴我你改用什麼方式記錄起始狀態。
4. 建立 notes/greenfield.md，第一段「起點」寫下測試數字與 Git 基準是否建立。
遇到錯誤時先說明原因，不要自行修改程式。做完停下等我。
```

③ 確認結果

```text
請檢查下列三件事，不要修改任何檔案：1. .venv 裡的 Python 是 3.13，requirements.txt 已安裝；2. 有「G0 baseline」這個 Git Commit；3. notes/greenfield.md 有「起點」段落，寫著測試數字（沒有失敗）與 Git 基準已建立。全部符合只回「成功」；有任何一項不符，只回「失敗：」加一句原因。
```

失敗時（其他狀況見 [環境準備](#environment) 頁「疑難排解」）：

```text
剛才的步驟出錯了。請先不要修改任何檔案，用白話告訴我：錯誤訊息是什麼意思、可能的原因、你建議怎麼處理（列 1–2 個做法），然後停下等我決定。
```

④ 補充

起始測試是 `1 passed, 8 skipped`（以實際輸出為準）。跳過（Skip）的測試代表功能還沒做。

## 檢查點 2 · 先要計畫，再核准（第 09–11 分鐘）

① 為什麼做這一步

先看計畫，你才能在動手前抓出範圍外的項目，所以這一步 Agent 只提計畫、不改程式。你判斷三件事，都成立就核准：

- 每一步都標了規則與驗收條件的編號（例如 `FARE-002`、`AC-G-005`）和預計修改的檔案
- 沒有範圍外項目
- 每個問題都附了建議答案；拿不準的舉手問主持人，不要讓 Agent 自行假設

② 貼給 Agent

先貼這段要計畫：

```text
【目標】先不要修改程式。提出 5 至 8 步的實作計畫。先仔細想過再回答，列出你考慮過的拆法。
【背景／要讀的檔】只讀這些：上一層資料夾（或 docs\ 副本）的商業需求（02-business-requirements.md）與驗收條件（03-acceptance-criteria.md）、這個專案的 README 與 docs/，以及程式碼（.py）中標示 TODO(GREENFIELD 的地方。
【限制】
- 建議依序拆成小步：票價 → 班次查詢 → 建立訂票 → 付款 → 查詢訂單。
- 每一步都要替這一步對應的驗收條件補上測試（例如建立訂票那步要有 1225 的測試，付款那步要有付款失敗不建立 Order 的測試），不能只靠移除 skip。
- 不要放進前端、登入、會員、優惠、改退票或新套件等範圍外項目。
- 下列事項需求文件沒有逐字寫明，請照這樣處理並寫進計畫：付款失敗時 Booking 維持 PENDING_PAYMENT、座位不釋放、不建立 Order、之後仍可再付款；找不到 Trip／Booking／Order 回 404；人數不符（0 人、超過 4 人）回 409，要在 domain／application 檢查，不要寫成輸入格式限制；座位不足、重複付款、付款失敗回 409；輸入格式錯誤沿用 422（回應內容用 FastAPI 預設，不另外包裝）；其他錯誤內容沿用 {"error":{"code":"...","message":"..."}}；測試要能指定付款失敗，不用隨機結果（把 MockPaymentGateway.next_result 設為 PaymentStatus.FAILED）。
【輸出格式】寫進 notes/greenfield.md 的「計畫」段落。開頭寫你在 .py 檔找到幾個 TODO(GREENFIELD 標記。每一步固定四項：第幾步、完成後使用者能做什麼（白話）、對應的規則編號（Rule ID）與驗收條件（AC）、預計修改的檔案。最後列出還需要我決定的問題，每題附上你建議的答案。
【停止條件】寫完就停下等我，不要開始修改。
```

看完計畫再貼這段。不同意某個建議答案，就在第一行後面加上「第 N 題改成…」：

```text
計畫核准，問題照你建議的答案處理（我有改的寫在這一行後面）。
請把我的決定和核准時間（用你電腦的目前時間）寫進 notes/greenfield.md 的「核准紀錄」。這一次做計畫的第 1、2 步（兩步都很小，一起做，驗收對照表照步驟分開列），並依實際結果更新 README 與 docs/ 裡相關的段落。做完依工作規則回報，然後停下等我，不要繼續下一步。
```

③ 確認結果

```text
請檢查下列三件事，不要修改任何檔案：1. notes/greenfield.md 的「計畫」有 5 至 8 步，每步都有規則編號、驗收條件與預計修改的檔案，開頭寫的 TODO(GREENFIELD 數量和 .py 檔裡實際的數量一致；2. 「核准紀錄」寫了我的決定與核准時間；3. 這次只改了計畫第 1、2 步預計修改的檔案（notes/、README 與 docs/ 不算）。全部符合只回「成功」；有任何一項不符，只回「失敗：」加一句原因。
```

失敗時：

```text
請停下，不要再修改。用白話說明哪一項不符、為什麼；改到計畫外的檔案就用 Git 還原那幾個檔案，缺的紀錄補進 notes/greenfield.md，然後停下等我。
```

④ 補充

```callout tip
技巧：Prompt 結構
**好的提示詞有五個部分，缺任何一塊，Agent 就會自己猜。**
- 【目標】【背景／要讀的檔】【限制】【輸出格式】【停止條件】
- 這一步的計畫提示詞就照五個部分寫
📖 延伸閱讀：Anthropic 官方文件〈Prompt engineering overview〉與〈Prompting best practices〉、OpenAI 官方文件〈Prompt engineering〉；你所用工具的官方文件通常有同名章節。
```

Agent 回報找到 11 個 `TODO(GREENFIELD` 標記（「這裡還沒做」的註記）才對。

核准前它就開始改檔案，貼：「請立刻停下，不要再修改。用白話告訴我你剛才改了哪些檔案，然後用 Git 還原到 G0 baseline（notes 資料夾保留），再重新只提計畫，停下等我。」

## 檢查點 3 · 小步做、每步驗收（第 11–24 分鐘）

① 為什麼做這一步

每次只放行一小步，錯了只要退一小步。Agent 每做完一步，看它附的審查答案，判斷三件事：

- 改的檔案都在計畫裡（notes/ 不算）
- 測試數沒有變少，也沒有新增跳過
- 沒有刪除測試，也沒有改既有期待值

做到建立訂票時，自己手算 T001 成人 700 ＋ 學生 525 ＝ **1225**，跟驗收對照表中 AC-G-005 的結果對照。

② 貼給 Agent

三件都成立，就貼放行提示詞（每一步都貼同一段）：

```text
這一步我核准了。請把這一步的驗收對照表、審查答案和核准時間（用你電腦的目前時間）寫進 notes/greenfield.md，段落標題用「第 N 步」（N 由你依計畫編號），依這一步的實際結果更新 README 與 docs/ 裡相關的段落，再把變更 Commit 成同樣的名稱。接著只做計畫中的下一步，做完依工作規則回報，然後停下等我。如果計畫已經沒有下一步，就停下告訴我『計畫已全部完成』，不要自己加新功能。
```

任何一件不成立或不確定，改貼這段：

```text
這一步我先不核准。請用白話解釋審查答案裡有問題或我看不懂的地方，提出修正做法，等我同意後再修正並重跑 pytest -q。
```

③ 確認結果

每放行一步後貼：

```text
請檢查剛核准的那一步，不要修改任何檔案：1. notes/greenfield.md 有這一步的「第 N 步」段落，含驗收對照表、審查答案與核准時間，而且已 Commit；2. 最近一次 pytest -q 失敗數為 0，跳過數沒有增加，且這一步計畫要解除的 skip 已變成通過，沒有新增 skip 或 xfail；3. 如果這一步是建立訂票，AC-G-005 的結果是 1225；如果是付款，只有待付款能付款、成功後建立唯一 Order、重複付款與付款失敗都不建立 Order。全部符合只回「成功」；有任何一項不符，只回「失敗：」加一句原因。
```

失敗時：

```text
請用白話說明哪一項不符、為什麼。缺的紀錄或 Commit 直接補上；需要改程式就先提修正做法，等我同意後再改，並重跑 pytest -q。
```

④ 補充

```callout tip
技巧：Structured Output（結構化輸出）
**要求 Agent 用固定格式回報，人才看得快、能前後比對。**
- **驗收對照表**（每步都附）：編號、白話內容、結果、依據的測試名稱
- **變更審查**：你不讀程式的修改內容，改看 Agent 用白話回答四題固定問題
- 審查答案裡的 skip（略過測試）、xfail（把測試標成預期會失敗）都會把問題藏起來
- Agent 仍可能漏欄，要檢查
📖 延伸閱讀：Anthropic 官方文件〈Structured outputs〉、OpenAI 官方文件〈Structured model outputs〉、Google Engineering Practices〈Google's Code Review Guidelines〉；你所用工具的官方文件通常有同名章節。
```

- Agent 的回報沒有審查答案：貼「請依工作規則第 6 條補上四題審查答案，然後停下等我。」
- 建立訂票那步 Agent 回報「把訂票結果轉成回應時出錯」（旅客資料無法轉換）：這是起始程式的已知小問題，貼「請用最小的修改讓回應能讀取旅客資料，不要改測試，並在審查答案說明改了哪個檔案。」

```callout tip
時間不夠時
第 24 分鐘還沒做到付款，就停在已核准的那一步，直接進入檢查點 4 驗證已做的功能。未完成的請 Agent 寫進交付摘要，不要硬趕。
```

## 檢查點 4 · 親自走一次流程並交付（第 24–29 分鐘）

① 為什麼做這一步

不再加新功能，最後一步驗收由你親自在 `/docs` 操作。你判斷的是：交付摘要裡的人工驗證結果和你在 `/docs` 看到的一致；不一致時以你的實際操作為準，請 Agent 改正 notes。

② 貼給 Agent

先貼這段，讓 Agent 替還沒有測試的驗收條件補測試、整理最終驗收對照表並啟動 App：

```text
不要再加新功能。對照驗收條件 AC-G-001 到 AC-G-015，凡是還沒有測試的（常漏的是 AC-G-001、002、009、013），用測試用的 TestClient 補上最少的測試並執行 pytest -q；需要實際呼叫 API 時用 Python 的 httpx，不要用 curl（Windows 的 curl 會弄亂中文）。
再把最終驗收對照表寫進 notes/greenfield.md 的「最終驗收」段落：涵蓋所有驗收條件，欄位與每一步相同，最後一行寫測試總數，附上你實際執行的指令。
最後在背景啟動這個專案的伺服器（埠號 8000；啟動前先確認 8000 沒有其他程式在用，有的話就停下告訴我是哪個程式，不要停它），確認 http://127.0.0.1:8000/health 回傳 status=ok，把 /health 的結果與實際使用的埠號也寫進「最終驗收」，然後告訴我 /docs 的網址。之後要換版本或結束時，先停止你啟動的伺服器。
```

自己走一次完整流程。在瀏覽器開 `http://127.0.0.1:8000/docs` → 點開要試的 API → 按「Try it out」→ 填入參數或在 Request body 貼上下方範例 → 按「Execute」→ 看 Response 的狀態碼（例如 201 成功、404 找不到、409 狀態衝突）和內容。依序試：

1. `GET /trips`：確認沒有 T003。
2. `POST /bookings`：把下方範例貼到 Request body，確認 `total_fare` 為 1225、`status` 為 `PENDING_PAYMENT`，記下 `booking_id`。
3. `POST /bookings/{booking_id}/pay`：填入 `booking_id`，確認回傳 Order，記下 `order_id`。
4. `GET /orders/{order_id}`：確認 `amount` 為 1225、`payment_status` 為 `SUCCESS`、`booking_id` 正確。
5. 再付款一次同一個 `booking_id`，確認被拒絕。

```text
{
  "trip_id": "T001",
  "passengers": [
    {"passenger_id": "P1", "name": "測試旅客一", "passenger_type": "ADULT"},
    {"passenger_id": "P2", "name": "測試旅客二", "passenger_type": "STUDENT"}
  ]
}
```

App 重啟後資料會重置，這是設計行為。走完再貼這段，請 Agent 寫交付摘要：

```text
請把交付摘要寫進 notes/greenfield.md 的「交付摘要」段落，下列每一項用一個固定小標題：完成的功能與對應的 Rule ID、AC；修改了哪些檔案；最後一次 pytest -q 的指令與測試總數；文件更新；未完成項目、仍被跳過的測試與風險；人和 Agent 各做了什麼（依 notes 裡的「核准紀錄」與各「第 N 步」段落整理）。沒有實際執行過的項目標為「未驗證」。
我剛在 /docs 依序試了：查班次（應該沒有 T003）、成人加學生訂票（應為 1225、待付款）、付款、查訂單（金額 1225、付款成功）、同一筆再付款（應被拒）。請把這五項當成「人工驗證」寫進摘要；先問我結果，我會回「五項都一致」或「第 N 項不一致：我看到…」，照我的回覆寫入。寫完把所有變更 Commit 成「Greenfield 交付」，告訴我，不要再修改程式。
```

③ 確認結果

```text
請檢查下列三件事，不要修改任何檔案：1. notes/greenfield.md 的「最終驗收」涵蓋 AC-G-001 到 AC-G-015，最後一行的測試總數沒有失敗，並記了 /health 結果與埠號；2. 「交付摘要」六個小標題都有內容，「人工驗證」照我的回覆寫入；3. 變更都已 Commit。全部符合只回「成功」；有任何一項不符，只回「失敗：」加一句原因。
```

失敗時（第 29 分鐘就停止修改，如實交付）：

```text
不要再修改程式。請把缺的部分補進 notes/greenfield.md；做不完的，記下目前完成到哪裡、還有哪些沒做完、哪些未驗證，再 Commit，然後告訴我。
```

④ 補充

做完到 [Greenfield 回顧與交付決定](#gf-submission) 和旁邊的人聊一下，再選交付決定。
