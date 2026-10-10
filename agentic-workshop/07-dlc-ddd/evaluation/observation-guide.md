# DDD DLC 觀察指引

> 主持人／助教專用。不得放進學員包、Runbook 或投影；揭曉前不得讓學員看到。
> 用途：巡堂時知道該看什麼、何時介入，以及課後給每組一段具體回饋。**不排名、不比組與組**；Recovery 不作為小組成果評分。
> 搭配：`facilitator/facilitator-guide.md`（時程與釋放規則）、三份參考解答的 `SOLUTION-NOTES.md`（第 4 節反事實、第 5 節 Agent 常見錯誤）。

## 1. 三條觀察主軸

整場只看三件事，每段的觀察項都掛在其中一條下：

| 主軸 | 看什麼 | 好的樣子 |
|---|---|---|
| **A. DDD 決策** | owner Context、不變量、一致性邊界、Port／Adapter 位置，是不是**人**先決定、寫下理由 | 決策卡在 Agent 動手前就寫好，Agent 的計畫沿用它；有人問「這條規則的家在哪」 |
| **H. Human-in-the-loop** | 人有沒有在每個停點真的看過輸出、核准計畫、Review Diff；有沒有讓 Agent 自行宣稱完成 | 「先提計畫、停下等我」被遵守；人要 Agent 回報實際的 `pytest -q` 與指令結果，而不是只接受它的總結；Agent 停下時人真的回覆決定，Agent 沒有在人同意前寫入 |
| **E. 證據與反事實紀律** | reviewed 事實與候選分得清；每條新規則有 `killed`；只認 `killed` 字樣；survived 時補測試而不是換字串 | 紀錄檔寫「未證明」而不是假裝完成；候選不自稱 reviewed |

## 2. 各段觀察項與介入訊號

每段 3–5 個可觀察行為（規格 §2）。「介入訊號」出現時，用一句提問介入，不替學員做決定。

### 2.1 開場與環境（0–10）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| O1 | E | Agent 回報裡出現 `76 passed`、`SHA OK 71 files`、`"version": "0.10.15"`，學員對照過關字樣才往下 |
| O2 | H | 學員先貼工作規則、再貼提示詞，自己不打指令；Agent 的 Plugin 指令經 `tools/dm.*`，沒有直接呼叫 `registry_tools.py` |
| O3 | E | `notes/opening.md` 記有 `python` 路徑在 `.venv\Scripts\`、`doctor.py` 全 `[OK]` |

介入訊號：解壓在桌面／OneDrive（之後會 WinError 206）→「這個路徑多長？」；`SHA MISMATCH` 卻想繼續 →「這份 Plugin 的判定還可信嗎？」；學員自己在終端機打指令或改指令 →「把 Runbook 的提示詞貼給 Agent，卡住就貼『如果卡住』那一段」。

### 2.2 D1 共同語言與邊界（10–35）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| O1 | H | 來源、詞彙、Context 與規則是**人**看過 Agent 的建議與證據後回覆決定的；`notes/d1.md` 記得到採用與不採用的理由，學員能說出為什麼排除某些來源 |
| O2 | E | 每個候選至少一個 `cite` 證據，且證據在已確認來源內（Agent 回報 `validate` 通過、`verify-evidence` 全部 current） |
| O3 | A | 發現名稱矛盾（Fare Policy／Discount Policy）或沒有對應程式的詞（Compensation），選擇記錄矛盾或「未建模」，而不是挑一個當答案 |
| O4 | A | `analyze-boundary` 用兩個不同 Context，學員能依 Agent 附的證據說出一個邊界洩漏 |

評估看 `notes/d1.md` 的證據與學員的決定（「D1 決定」只有三個選擇＋一個短文字），不因少填表扣分。

介入訊號：Agent 憑空補 Compensation 實作或定義 →「證據在哪一行？」；學員對 Agent 的草稿一律回「同意」、沒看證據 →「挑一個，請 Agent 把它的 cite 原文念給你聽，你同意這個定義嗎？」

### 2.3 D2 審查與核准（35–60）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| O1 | H | 兩個 Agent 對話分清：`record-approval`、簽章 commit、push 只出現在 Maintainer 自己的 Agent 對話；proposer 的 Agent 沒碰 `.dlc-keys`、沒 commit（三人組由 Observer 看） |
| O2 | H | Maintainer 回「核准」前讀過 Agent 貼出的證據原文與測試結果，說得出一行證據支持哪條規則；不是 Agent 一停就回核准 |
| O3 | E | counterfactual 方案由 proposer 選定，結果只認 `killed`；Change Package 的測試結果來自實際執行（`fill_package.py`），沒有預填 PASS |
| O4 | E | `notes/d2.md` 有 Agent 寫下的 readiness `ready`、obligation 結果、審查摘要與核准決定、簽章行；私鑰不在 Repo、不在截圖、不貼給 Agent |
| O5 | H | 能說出「`record-approval` 只比字串，真正擋得住的是簽章；Agent 不能替自己的提案核准」 |

證據看 `notes/d2.md` 與學員有沒有在 Agent 停下時做決定，不看表單填了多少。介入訊號：核准或 commit 出現在 proposer 的對話 →「這個核准是誰決定的？」；Maintainer 直接回核准 →「哪一行證據支持這條規則？」；金鑰放在 Repo 內或 `.ssh` → 立刻請 Agent 移到 `%USERPROFILE%\.dlc-keys\` 並確認 `git status`；卡 5 分鐘 → 依手冊提供 `dlc-rec-d2`。

### 2.4 D3 共同（每段都看）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| C1 | E | 學員貼提示詞後，Agent 實際執行 `resolve-terms`／`get-context`，`notes/d3*.md` 把 reviewed 事實與知識缺口分開 |
| C2 | A | Agent 每題提兩個選項＋證據，**學員自己選**（不是回「你決定」）；決策卡（`docs/handoffs/d3*.md`）在 Agent 改檔前完成，寫的是學員選的選項 |
| C3 | H | Agent 先提計畫、學員回「同意」才動手；分段停下，學員看實際測試結果才回「繼續」；核心 AC 排在延伸之前、介面照卡上 API |
| C4 | E | 學員看過 Agent 列的改壞方式才同意執行；每條登記的新規則有 `killed`；survived 時補測試用同一組字串重跑；未證明的在紀錄檔照實寫 |
| C5 | E | 學員看過審查答案才同意登記；Agent 用 `make_record.py` 登記，措辭仍是候選；沒有執行 `record-approval`、`amend-policy` |

共同介入訊號：跳過選項直接叫 Agent 實作，或回「你決定」→「決策卡呢？owner 是誰選的？」；Agent 改既有測試期待值讓測試過 →「規格 R8 允許改寫哪些？理由寫在哪？」；只看 exit code →「`killed` 在哪？」

### 2.5 D3a 電子發票（70–95）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| A1 | A | 發票有自己的 Context（或至少自己的模組與狀態機），不塞進 Order／Booking |
| A2 | A | Port 宣告在 domain／application 邊界、以領域語言命名，Adapter 在 infrastructure；供應商代碼不出現在 Service |
| A3 | A | 付款與發票的一致性邊界分開：鎖內只建 PENDING，鎖外呼叫；**團體路徑也是** |
| A4 | E | 逾時被當成「結果未知」：重試用同一個 order_id |

介入訊號：`except Exception: pass` →「失敗之後誰知道？還能重試嗎？」；只改 `pay` →「`pay_group` 呼叫 `pay` 時手上有沒有鎖？」

### 2.6 D3b 點數折抵（95–125）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| B1 | A | owner Context 有理由（不是「放哪都行」）；30% 上限的歸屬有說明 |
| B2 | A | 計價（`DiscountPolicy`、三條計價迴圈）沒被改；點數不是優惠 |
| B3 | A | 預留在建立時、寫入之前、鎖內；歸還的時機分清（團體付款失敗、整筆退票歸還；一般付款失敗、改票不動） |
| B4 | E | 有 M002 665（上限 199）的測試，或在 counterfactual 中發現需要它 |

介入訊號：點數放進 `DiscountPolicy` →「`applied_discounts` 現在變成什麼？」；在 route 先查餘額 →「兩個請求同時來會怎樣？」

### 2.7 D3c 團體部分退款（125–155）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| C1 | A | 有一個唯一入口決定「誰被取消、每人 fee＋refund」，恆等式在那裡成立 |
| C2 | A | 先檢查全部條件再寫入；不在迴圈中邊驗證邊修改 |
| C3 | A | 手續費的商業數字只有一個家；以每位旅客自己的票價逐位計算 |
| C4 | A | 整筆退票路徑也被處理（部分取消過就不能整筆退） |
| C5 | E | 測試含成人＋學生混合團（或在 counterfactual 中發現需要它） |

介入訊號：改 `total_fare` →「恆等式右邊還是 Order.amount 嗎？」；整筆 release 再 reserve →「中間失敗會怎樣？會不會換座位？」；第 148 分還在寫延伸 → 停手進 Review。

### 2.8 D4 交接（155–165）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| D1 | E | `notes/d4.md` 有三個驗證結果；`stale` 被記下並分清候選或 reviewed，沒有跳過，也沒讓 Agent 當場修 |
| D2 | H | Agent 先列更新清單，學員回覆後才登記；只更新真的改變的事實，而且是候選（reviewed 以新 id 候選取代） |
| D3 | E | 交接單七段齊全，Agent 回報的 id 核對清單全部查得到；commit 由 Maintainer 自己的 Agent 對話執行；Unknowns 誠實（例：D3c 低於 5 人是否降級、整筆退票是否收手續費、閘道退款失敗） |

介入訊號：想直接標 reviewed →「核准簽章在哪？」；Agent 沒等回覆就登記 → 請學員貼「先停下，列出你要寫入的內容等我同意」；交接單引用不存在的 id →「下一個 Agent 查得到它嗎？」

### 2.9 回顧（165–180）

| # | 主軸 | 可觀察行為 |
|---|---|---|
| R1 | E | `notes/retro.md` 有「reviewed 事實改變了 Agent 輸出」的具體例子與證據，或誠實寫「未觀察」；學員有抽問 Agent「證據在哪？」 |
| R2 | E | 能指出一個差點被當成事實的候選 |
| R3 | H | 口頭討論時能區分 `record-approval`（字串比對）與簽章（持鑰）的治理強度 |

介入訊號：Agent 的回顧寫了紀錄裡沒有的事 →「這句的證據在哪？沒有就請它改成未觀察」；討論停在「很有用」→「哪一個 commit 或哪一段紀錄看得出來？」

## 3. 輕量評分表（不排名）

每組每條主軸給一個等級，附一句**觀察到的具體證據**（Agent 回報的指令輸出、`notes/` 或 `docs/handoffs/` 的紀錄、Diff 片段）。依「紀錄檔裡的證據＋學員有沒有做決定」判斷，不因表單少填扣分。沒有總分、不跨組比較；用途是課後回饋與改進教材。使用 Recovery 的段落標「Recovery」，不評該段產出，只評之後的行為。

| 等級 | A. DDD 決策 | H. Human-in-the-loop | E. 證據與反事實紀律 |
|---|---|---|---|
| **看得到** | 決策卡先於實作，owner／不變量／邊界有理由，Agent 照做 | 每個停點都有人看實際輸出、核准計畫、Review Diff | reviewed／候選分清；每條新規則 `killed` 或如實標未證明；survived 會補測試 |
| **部分** | 有決策但事後補寫，或理由只有名稱 | 有停點但常直接接受 Agent 總結 | 有 counterfactual 但只看 exit code，或未證明的沒標 |
| **還沒看到** | 需求卡直接丟給 Agent | Agent 自行跑到底 | 候選自稱 reviewed；沒有 counterfactual |

回饋句型：「在〈段落〉，我看到〈具體行為〉，所以〈主軸〉是〈等級〉；下一次可以〈一個動作〉。」

## 4. 各情境 Agent 常見錯誤（巡堂清單）

摘自三份 SOLUTION-NOTES 第 5 節，依「最常見且最傷」排序。完整清單與理由見原文。

### 4.1 D3a 電子發票

1. **在鎖內呼叫服務商**。最隱蔽：在 `pay` 內把呼叫移出 `with self.store.lock`，卻沒發現 `pay_group` 持有 RLock 時呼叫 `pay`，團體路徑仍在鎖內。
2. **發票失敗拋 `DomainError`**：已扣款、Booking 已 PAID，API 卻回 409／500。
3. **`except Exception: pass`**：付款 200，但沒有 PENDING 紀錄、無法重試。
4. **在付款請求內同步重試 5 次**：最壞 15 秒，常常還在鎖內。
5. **逾時當成「沒開出來」**：重試換新的 `merchant_order_no`，或直接判 FAILED。
6. **2001 當錯誤**，或重試沒用回傳的原號碼。
7. **發票金額用 `booking.total_fare`**：今天碰巧等於 Order.amount，D3b 之後就錯。
8. **供應商代碼進 Domain／Service**（`if code == "9001"`）、Port 以供應商命名或宣告在 infrastructure。
9. **發票欄位塞進 Order／Booking**，改動既有回應合約。
10. **重試次數算錯**：「5 次」實作成 1 + 5 = 6 次呼叫；FAILED／ISSUED 仍呼叫服務商。
11. **浮點稅額** `round(total / 1.05)`：通過所有測試（見 §5.1），只能靠 Review。
12. **順手把付款閘道 Port 化或導入 Queue**：超出範圍，違反 ADR 003 卻沒寫新 ADR。

### 4.2 D3b 點數折抵

1. **點數放進 `DiscountPolicy`**：破壞 PTS-006，`applied_discounts` 被改。
2. **從 `total_fare` 直接扣點數**：之後改票差額、退款、上限（以扣後金額算 30%）全錯。
3. **在三條計價迴圈各加一份折抵**，或漏了團體；或改票路徑也重算點數。
4. **付款時才扣點**：違反 PTS-008，同一會員兩筆 PENDING 可超扣。
5. **驗證在寫入之後**，或**扣點在座位規劃之前**（團體無連續座位時點數已扣）。
6. **上限用原價或 `round()`**：通過 700 試算、在 M002 665 失敗。
7. **用 Pydantic `Field(ge=100, multiple_of=100)`**：回 422 而不是 409，規則有兩個家。
8. **退款退 `total_fare`**（現金＋點數重複退）或 `total_fare − 點數`（改票後錯）。
9. **一般付款失敗也歸還**（違反 PTS-011），或團體付款失敗忘了歸還。
10. **檢查在鎖外**：check-then-act 競態。
11. **過度設計**：新 Loyalty Context＋Domain Event＋Reservation Repository＋Saga。
12. **順手收斂三份計價迴圈**：方向對，但不是這張卡的範圍。

### 4.3 D3c 團體部分退款

1. **改 `total_fare` 或 Order.amount**：恆等式「永遠成立」但失去意義。
2. **手續費以 `total_fare` 平均，或在加總後取整一次**：通過全成人範例，混合團失敗。
3. **整筆 release 再重新 reserve**：重新配位、兩步之間失敗遺失座位。
4. **四份座位資料只改一兩份**（`Trip.available_seats`、`store.seat_assignments`、Booking 的 `seat_ids`／`assigned_seats`）。
5. **邊驗證邊修改**：第三位才 404，前兩位已被取消（PCR-011）。
6. **`store.refunds[booking_id] = record` 原樣沿用**：第二次覆寫第一次。
7. **人數下限寫成 `remaining < 5`**：不能一次取消全部；或拿請求人數比。
8. **忘了整筆退票路徑**：部分取消後整筆退仍退全額（重複退款）。
9. **只靠 Pydantic 擋重複 id**：Service 層呼叫時手續費算兩次。
10. **在 `Passenger` 上加 `status`**：破壞既有 `passengers` 合約。
11. **有點數的團體沒排除**：恆等式兩邊不同基準。
12. **呼叫付款閘道退款**：違反 PCR-014。
13. **過度設計**：Refund Aggregate＋Domain Event＋Saga；或順手合併四份座位資料成 TripInventory。

## 5. 教學 mutant（揭曉或 Review 時拿出來討論「測試證明的是什麼」）

### 5.1 D3a

- **單價 `round(amount / quantity)`**：只有 1,225 ÷ 2 ＝ 612.5 一個案例時，Python 的銀行家捨入剛好得 612，與向下取整相同 → survived。補 3 人案例（1,925 ÷ 3：向下取整 641、四捨五入 642）後 killed。這就是「survived 代表沒有測試保護這條規則，補測試再跑」。
- **稅額四捨五入邊界 `>=` → `>`：等價 mutant，殺不死**。5% 稅率下整數總額永遠不會剛好落在 .5：若 總額 × 100 ÷ 105 ＝ n + ½，則 總額 × 200 ＝ 105 × (2n + 1)，左偶右奇，不可能。所以「四捨五入」與「五捨六入」對所有合法輸入相同；Agent 寫 `round(total / 1.05)` 也全過。「不使用浮點數」只能靠 Code Review。
- 討論題：「這個 survived 是測試漏洞，還是規則本來就觀察不到？」

### 5.2 D3b

- **最低點數 100 → 1：等價 mutant**。「至少 100」與「100 的倍數」重疊：正的 100 倍數必然 ≥ 100，最低值只多擋了負數（−100 在 Python 中 `% 100 == 0`）。所以 100 → 1 對所有輸入相同；但**整個拿掉最低檢查**會被 −100 殺死。卡上兩個數字其實是同一條規則。
- **只有 M002 665 對上限敏感**：700／3,500／1,225 的上限是 210／1,050／367，而折抵是 100 的倍數，所以 30% → 31%、`//` → `round`、以原價算上限三個 mutant 在只測前三個試算時都存活。665 × 30% ＝ 199.5 是唯一能區分的數字。
- **上限等號**只有上限剛好是 100 倍數時可觀察（T002 成人 2 位 3,000 → 900）。
- **退款讀 `payable_amount`** 只有「改票後退票」抓得到（750 − 200 ＝ 550 ≠ 實付 500）。

### 5.3 D3c

- **總額取整一次（floor-on-sum）**：只有「兩位學生一起取消」抓得到（157.5 × 2：逐位 314，總額取整 315）。
- **以 `total_fare` 平均分攤（average）**：只有**成人＋學生混合團**抓得到。卡上範例全是成人（6 × 700 × 30% 整除、平均票價＝每人票價），只測卡片範例時兩個錯誤都存活。
- **D 用 datetime 相減**：現有 FixedClock 時刻固定 09:00、只能設日期，所以現有測試分辨不出；但測試把 clock.now 換成出發時刻之後（例如 09:01）就分辨得出，所以不是等價 mutant，而是測試不足（依 D3 工作規則第 11 條）。來不及補測試就標「未證明」。
- **只列本訂票的退款紀錄**：只有一個團體有退款時會存活，測試要讓另一筆訂票也有退款。

## 6. 參考數字（核對學員結果用）

| 情境 | 參考解答 pytest | 新規則 counterfactual |
|---|---|---|
| D3a | 118 passed（76 ＋ 42） | 25／25 killed；另 1 個等價 mutant 存活紀錄 |
| D3b | 156 passed（118 ＋ 38） | 23／24 killed；1 個等價 mutant |
| D3c | 179 passed（156 ＋ 23） | 37／38 killed；1 個存活（datetime 相減，測試不足） |

學員的數字不需要相同；看的是「每條登記的規則有沒有 killed」與「survived 有沒有被如實處理」。
