# Greenfield：從 Idea 到可開發的專案

> 讀者：學員。時機：45分鐘引導操作。前置：獨立練習目錄與可用的Coding Agent。

在新目錄進行；每步由人確認。程式與測試未執行時，標記未驗證。

## 1. 從 Idea 到可開發的專案

第一階段 · Greenfield（從空資料夾開始的新專案）／Tool（把 Agent 當工具使用） · 操作教學

- **今天要完成**：在自己的新資料夾，留下一套開發依據：需求、MVP（Minimum Viable Product，最小可行產品）、使用者故事、驗收條件、業務流程、Gherkin（用 Given／When／Then 寫測試情境的格式）與架構文件。

- **工作方式**：你確認問題與規則；Agent 協助整理與細化。每一步審查後才繼續。

**人工確認**：完成條件：一個核心訂票情境可從需求追到測試與模組責任。

## 2. 剛才的順利，哪些來自事先準備？

打開剛才的 G0（Greenfield 起始包）：先找到文件，再找到程式入口。

- **需求已明確**：四個 API、16 項商業規則、15 項驗收條件；限制了第一版範圍。

- **骨架已備妥**：型別、分層、固定資料、模擬付款、Health（健康檢查端點）與測試骨架；留下11個主要TODO（待完成的程式標記）。

### 交給 Agent 的指令

先不要修改檔案。閱讀目前G0的README、docs與tests，盤點哪些需求、規則、架構與驗證方式已準備好。列出檔案來源、這項準備消除了什麼不確定性，以及仍需要我決定的事項。

**人工確認**：指出一項對你有幫助的準備與檔案位置；未觀察到順利時，記錄真實卡點。

## 3. 把準備工作重新做一次

選用同一個案例：成人與學生一起訂票。

構想（Idea）／docs → MVP工作項目 → 使用者故事／使用案例 → 驗收條件（AC） → 業務流程（Business Flow） → Gherkin測試情境 → 分層架構

- **每次只往前一步**：先讀來源 → 提出草稿 → 人確認 → 保存文件 → 再細化。

- **文件可往回修**：流程暴露新問題時，回頭補使用者故事或驗收條件，保留調整理由。

**人工確認**：所有文件使用相同規則與識別碼；Agent補出的假設先標記，等你決定。

## 4. 建立自己的空專案

在自行選定的練習位置建立新資料夾，並用編輯器開啟。

- **連接 Agent**：讓你的 Coding Agent（能讀寫檔案、協助寫程式的 AI 助手）使用這個新資料夾；只在此處讀寫。

- **準備來源**：取得本教材的 practice/idea.md；複製到新專案的 docs/idea.md。

```text
# PowerShell
New-Item -ItemType Directory -Path smart-ticket-idea
Set-Location smart-ticket-idea
New-Item -ItemType Directory -Path docs

# bash（擇一執行）
mkdir smart-ticket-idea
cd smart-ticket-idea
mkdir docs
```

**人工確認**：確認位置正確且docs/idea.md可讀；若資料夾已存在，改用新名稱。

## 5. 先保存業務原意

開啟 docs/idea.md，讀完後用自己的話說明問題。

- **目標與流程**：旅客查詢班次、為1–4人訂票、模擬付款，成功後取得訂單。

- **規則與限制**：成人100%、學生75%、逐人加總；本機虛構資料、固定日期、In-Memory（資料只存在記憶體，重啟即清空）、無前端或真實付款。

### 交給 Agent 的指令

請閱讀docs/idea.md，先不要寫程式。整理問題、使用者、目標、核心情境、已明定規則與限制，寫入docs/01-project-brief.md。每項結論標示來源；來源未提到的內容列為待確認問題，不自行補成需求。完成後等我審查。

**人工確認**：產出01-project-brief.md；指出一個假設或缺口，決定保留待確認還是補充規則。

## 6. 把第一版切成可驗證的工作

MVP：用最少功能完整走完核心流程的第一版；今天就是查詢→訂票→付款→訂單。每一階段都寫出能驗證的成果。

- **M1 查詢**：班次資料、只列可售班次、精確篩選。

- **M2 訂票**：人數與容量驗證、逐人計價、保留座位。

- **M3 付款與訂單**：成功付款、唯一訂單、重複與失敗處理。

- **M4 完整交付**：串起四個API、測試、文件與交付摘要。

### 交給 Agent 的指令

依已確認的docs/idea.md與01-project-brief.md，產生docs/02-mvp-plan.md。將本次MVP拆為M1查詢、M2訂票、M3付款與訂單、M4整合交付；每階段列目標、工作ID、依賴、可驗證產出及不處理項目。每個工作應可獨立審查；不要引入新功能。等我確認優先順序。

**人工確認**：M1–M4是同一版MVP的工作階段；只有查詢完成時，仍是部分成果。

## 7. 練習：讓工作項目能被接手

選M2，補上工作ID、規則與驗證方式。

```text
TASK-GF-02：建立核心訂票
輸入：Trip ID、1–4位旅客與旅客類型
依據：BOOKING-001～005、FARE-001～004
工作：驗證 → 逐人計價 → 建立待付款訂票 → 保留座位
產出：用例、票價Policy、API與測試
驗證：T001成人＋學生＝1225，座位20→18
失敗：0／5人、班次不存在、容量不足；無部分寫入
```

**人工確認**：說出這項工作依賴什麼，以及完成後如何驗證；無法回答時先補文件。

## 8. 從工作項目，回到使用者情境

使用者故事說明「誰、想做什麼、為了什麼價值」；使用案例寫出使用者與系統一步步的互動與例外。先說清楚使用者要什麼，再安排實作。

- **使用者故事（User Story）**：身為旅客，我希望為同行成人與學生一次訂票，以取得各自正確票價並保留座位。

- **使用案例（Use Case）**：前置：班次可售。主流程：選班次→填旅客→確認總價→建立訂票。例外：人數不合法、班次不存在、容量不足。

### 交給 Agent 的指令

依02-mvp-plan.md，將每個工作項目對應到User Story或Use Case，寫入docs/03-stories.md。先完整細化TASK-GF-02：列角色、目的、前置、主流程、例外、後置狀態與規則編號（Rule ID，例如FARE-002）。技術工作可列為支援任務，不硬寫成使用者需求。未知內容標待確認，等我審查。

**人工確認**：使用者故事描述價值；使用案例描述互動。檢查每個工作都有情境或支援任務的依據。

## 9. 把「正確」寫成可判定的結果

驗收條件（AC）：事先寫好、能明確判定符合或不符合的完成標準。先手算：700＋700×75%＝1225。

- **AC-G-005／009**：成人＋學生訂票：總額1225、整數、PENDING_PAYMENT（待付款）、座位20→18。

- **AC-G-006～008**：0人／5人拒絕；4人容量足夠可接受；僅剩1座卻訂2人拒絕且座位不變。

### 交給 Agent 的指令

依idea.md與03-stories.md，產生docs/04-acceptance.md。沿用來源AC-G識別碼與Rule ID；每列寫前置、操作、可觀察結果。先完整寫訂票正常、人數邊界、容量不足與班次不存在；再列付款與查詢條件。不要新增未明定錯誤碼，缺口列待確認。等我審查。

**人工確認**：每個條件能判斷符合／不符合；避免只寫「正常運作」「錯誤處理完善」。

## 10. 把功能串成狀態與資料變化

業務流程（Business Flow）：串起查詢、訂票、付款與訂單；成功和失敗都要有出口。

查詢可售班次（Trip） → 驗證旅客與容量 → 逐人計價 → 訂票（Booking）待付款＋保留座位 → 模擬付款成功 → Booking已付款＋唯一訂單（Order）

- **訂票拒絕**：不建立Booking，不扣座位；回傳明確錯誤。

- **付款失敗**：不建立Order、不標PAID；Greenfield仍待付款且保留座位。

### 交給 Agent 的指令

依03-stories.md與04-acceptance.md，建立docs/05-business-flow.md。用文字流程或Mermaid（用文字描述流程圖的語法）呈現查詢→訂票→付款→訂單，標示驗證點、狀態與資料變化；補上訂票失敗、付款失敗、重複付款。逐一核對Rule／AC，不確定的分支先列問題，不改規則。

**人工確認**：付款前不能已有Order；付款成功只有一筆Order；失敗不誤標已付款。

## 11. 停下來：用流程反查驗收條件

一位同學說明流程，另一位只追問狀態與證據。

- **追問一**：付款成功後又收到一次付款請求，會新增第二筆Order嗎？

- **追問二**：票價已算出但容量不足，系統是否留下半筆Booking或扣掉座位？

- **追問三**：付款失敗時，Booking、Order、座位各是什麼狀態？

- **保存決策**：將缺漏補回04-acceptance.md，再同步05-business-flow.md；記錄來源與理由。

**人工確認**：流程與驗收條件不能各說各話；無法決定的分支保留待確認。

## 12. 讓測試情境讀起來像業務範例

Gherkin：用接近口語的步驟寫測試情境，業務與開發都讀得懂。Given：前置狀態 · When：一次操作 · Then：可觀察結果

```text
@AC-G-005 @AC-G-009
Feature: 核心訂票
  Scenario: 成人與學生一起訂票
    Given 狀態已重置，T001基本票價700且剩餘20座
    When 為T001建立一位成人與一位學生的訂票
    Then 訂票總額為1225且為整數
    And 訂票狀態為PENDING_PAYMENT
    And T001剩餘18座
```

### 交給 Agent 的指令

將04-acceptance.md與05-business-flow.md轉為docs/06-booking.feature，使用英文Gherkin關鍵字與中文敘述。用AC標籤追溯；涵蓋混合訂票、人數0／4／5、容量不足、班次不存在、付款成功／失敗與重複付款。每個情境重置資料；驗證結果由來源規則推導，未知內容列待確認。

**人工確認**：預期金額先由人核對；同一情境的When只描述本次要驗證的操作。

## 13. 操作：補上人數邊界

用Scenario Outline（情境範本：同一組步驟，依Examples表格逐列代入不同輸入）把相同操作的不同輸入放在一起。

```text
@AC-G-006 @AC-G-007
Scenario Outline: 驗證旅客人數
  Given 狀態已重置，T001剩餘20座
  When 為T001建立<count>位成人的訂票
  Then 建立結果為<result>
  And 剩餘座位為<seats>
  Examples:
    | count | result | seats |
    | 0     | 拒絕   | 20    |
    | 4     | 成功   | 16    |
    | 5     | 拒絕   | 20    |
```

**人工確認**：每一列從乾淨狀態開始；拒絕案例還要確認沒有新增Booking。

## 14. 從情境，接到可執行測試

本案例用pytest；將Given／When／Then分別落到準備、操作與斷言。

```text
# pytest示意：需要client與memory_store fixture
def test_mixed_booking(client, memory_store):
    response = client.post('/bookings', json={
        'trip_id': 'T001', 'passengers': [
            {'passenger_id': 'P1', 'name': 'Adult', 'passenger_type': 'ADULT'},
            {'passenger_id': 'P2', 'name': 'Student', 'passenger_type': 'STUDENT'}]})
    assert response.status_code == 201
    body = response.json()
    assert body['total_fare'] == 1225 and type(body['total_fare']) is int
    assert body['status'] == 'PENDING_PAYMENT'
    assert memory_store.trips['T001'].available_seats == 18
```

**人工確認**：現在先記錄對應；空專案還沒有App或fixture（pytest的測試前置準備）。Gherkin檔案本身不代表測試已執行。

## 15. 讓規則與流程有清楚的落點

每層只做一類事；Domain（業務核心）不依賴FastAPI。

API／Schemas（介面層）：HTTP與輸入輸出 → Application（應用層）：協調訂票用例 → Domain（領域層）：模型與票價規則

- **Infrastructure（基礎設施層）**：記憶體資料存取、預設測試資料（Seed）、模擬付款。

- **依賴方向**：API→Application→Domain；實作在程式入口組裝。

### 交給 Agent 的指令

依已確認的docs/01至06文件，建立docs/07-architecture.md。採API、Schemas、Application、Domain、Infrastructure輕量分層；列模組責任、依賴、入口組裝、Repository契約與測試方式。以訂票用例逐步說明在哪層驗證、計價、保存與轉HTTP回應。Domain不依賴FastAPI，不新增資料庫或外部服務；先不要寫業務程式。

**人工確認**：學生75%在Domain的票價Policy（規則物件）；HTTP轉換在API；訂票協調在Application。

## 16. 把架構轉成可開工的檔案規劃

先核准架構，再請Agent建立目錄與責任說明。

```text
docs/                         # 已確認的開發依據
src/smart_ticket/
  main.py                     # App與依賴組裝
  api/                        # Router、HTTP錯誤轉換
  schemas/                    # Request／Response
  application/                # 查詢、訂票、付款、訂單用例
  domain/                     # 模型、票價Policy、Repository契約
  infrastructure/             # In-Memory、Seed、Mock Payment
tests/unit/                   # Policy與用例
tests/integration/            # HTTP與完整流程
```

### 交給 Agent 的指令

依我已核准的07-architecture.md，列出預計建立的目錄與檔案及每個檔案的責任，寫入docs/08-file-plan.md。維持Python3.13、FastAPI、Pydantic2、pytest與In-Memory。提出骨架建立計畫，等我確認後才建立目錄與README；不實作業務邏輯，不安裝新套件。

**人工確認**：目錄與責任對得上；未核准時保留檔案計畫，不提前寫程式。

## 17. 用一條追溯鏈核對所有文件

追溯鏈：從工作項目一路連到規則、驗收條件、測試情境與程式模組，每一環都找得到依據。選混合訂票情境，親手走一遍。

TASK-GF-02 → 同行成人與學生的使用者故事 → FARE-002／003 → AC-G-005／009 → 混合訂票情境（Scenario） → FarePolicy＋Booking用例＋測試

### 交給 Agent 的指令

請交叉檢查docs/idea.md及01至08文件，產生docs/09-traceability.md。每列連結工作ID、Story／Use Case、Rule ID、AC、Gherkin情境、模組與預計測試。指出孤立需求、漏測條件、規則矛盾與未決問題，不自行改規則。最後列已完成、未完成與待我決定項目。

**人工確認**：至少一條完整鏈；付款失敗、重複付款與容量不足都有對應情境。

## 18. 保存現況，讓下一步可以開始

這次交付的是開發依據；完成實作後仍需測試與檢視（Review）。

- **交付資料夾**：docs/idea.md與01–09文件；附未決問題、版本與人的確認紀錄。

- **下一步指令**：請Agent依核准文件提出第一個實作計畫。人確認後，才執行、測試與審查變更差異（Diff）。

### 交給 Agent 的指令

請整理本次文件交付摘要，寫入docs/10-handover.md：列文件、已確認決策、尚未確認事項、下一個可執行工作與驗證方式。明確標記程式／測試尚未實作或執行；不要宣稱MVP完成。先提出下一步計畫，等我確認。

**人工確認**：離場前：能說明一項事先準備如何減少不確定性，並展示自己的文件與待辦。

## 完成條件
至少一條需求到情境與模組的追溯鏈，附已確認決策、缺項與下一步；實測需另有證據。
