# D3a 電子發票：主持人參考解答說明

本目錄是 DDD DLC 情境 D3a（需求卡 01：接入外部電子發票服務）的參考解答，也是 D3b（點數折抵）的 Recovery 起點。起點為 `participant/repository/smart-ticket-dlc-base`，只加入發票功能，其餘刻意保留的邊界洩漏（付款閘道無 Port、Service 依賴具體 Store、字串事件名等）原樣不動。

## 驗證方式

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 -m pytest -q          # 118 passed（原 76 + 新 42）
.\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\integration\test_e_invoice.py   # 42 passed
# 反事實檢查（需 domain-memory 外掛），結果寫入 evidence\counterfactual\*.json
py -3.13 -X utf8 evidence\run_counterfactuals.py .venv\Scripts\python.exe <SkillHub>\.claude\skills\domain-memory\scripts\registry_tools.py
```

## 1. 設計摘要

| 檔案 | 角色 | 行數 |
|---|---|---|
| `src/smart_ticket/domain/invoicing.py` | Invoicing Domain：稅額拆分、購票人發票資訊驗證、`InvoiceRequest`、Port `InvoiceIssuer`、`Invoice` 狀態機、商業數字 `VAT_RATE_PERCENT`／`MAX_ISSUE_ATTEMPTS` | 130 |
| `src/smart_ticket/application/invoicing_service.py` | 建立 PENDING 發票、開立／重試（鎖外呼叫 Port）、查詢、Audit／通知 | 54 |
| `src/smart_ticket/infrastructure/einvoice_provider.py` | Adapter：服務商欄位名、回應代碼、3 秒逾時、連線例外 → 三種 Domain 結果；`SimulatedEInvoiceProvider` 為不連網的 transport | 88 |
| `application/payment_service.py` | `pay` 拆成鎖內 `_charge`（扣款、Order、PAID、開 PENDING 發票）＋鎖外 `invoicing.issue`；`pay_group` 先釋放鎖再呼叫 `pay` | +17／−4 |
| `api/routes.py`、`schemas/contracts.py`、`api/dependencies.py`、`infrastructure/store.py` | 付款 body 選填 `invoice`、`GET /orders/{id}/invoice`、`POST /orders/{id}/invoice/retry`、組裝點、`store.invoices` | 小幅 |
| `tests/integration/test_e_invoice.py` | 每個 AC 至少一個 `test_einv_0xx_*`，共 20 個函式／42 個案例 | 306 |
| `tests/unit/test_services.py` | `PaymentService` 建構子多一個參數，改用 helper 建立（行為斷言不變） | ±15 |
| `docs/adr/005-issue-e-invoices-through-a-port.md`、`docs/requirements/business-rules.md`（新增 EINV 規則表）、`docs/architecture.md`、`docs/api-examples.md`、`README.md`、`docs/version-history.md`（1.5.0） | 團隊文件 | |

流程：

1. 付款請求先在 Domain 建立 `InvoiceBuyer`；格式錯誤即 422 `INVALID_INVOICE_INFO`，此時尚未扣款（EINV-013）。
2. `_charge` 在全域鎖內：扣款 → 建立 Order → PAID → Audit／通知（原行為）→ 建立 `PENDING` Invoice（金額取 **Order.amount**）。
3. 釋放鎖後 `InvoicingService.issue(order_id)` 呼叫 Port 一次；結果只改 Invoice 狀態，付款照常回 200。
4. 之後由 `POST /orders/{order_id}/invoice/retry`（排程或維運）以同一 order_id 重試，直到 ISSUED，或第 5 次呼叫失敗／永久失敗轉 FAILED。

Port 的詞彙只有三種結果：`ISSUED`（含 2001 重複開立）、`REJECTED`（1001／1002）、`UNAVAILABLE`（9001、逾時、連線失敗、未知代碼）。`grep -rn "merchant_order_no\|buyer_ban\|9001\|2001\|CALL_TIMEOUT" src` 只命中 Adapter 檔，可當作「供應商細節沒外洩」的證據。

## 2. Context 劃分與理由

| Context | 本次持有 | 理由 |
|---|---|---|
| **Invoicing（新）** | Invoice（order_id 為識別）、購票人發票資訊、稅額拆分、品項規則、重試上限、狀態機、Port | 發票有自己的生命週期（PENDING→ISSUED／FAILED）、自己的法規語言（統編、載具、銷售額／稅額）和自己的失敗模式；放進 Payment 會讓「付款成功」的一致性邊界被外部服務拖住。 |
| Payment／Order | Order.amount、付款狀態；觸發「要開發票」 | Order 是發票金額的唯一來源。Payment 只呼叫 `InvoicingService.open/issue`，不知道服務商。 |
| Booking／Trip Catalog | 起迄站、旅客數 | 只提供翻譯所需資料；Invoice 不回寫 Booking。 |
| Audit／Notification（Generic） | `INVOICE_ISSUED`、`INVOICE_FAILED` | 沿用 ADR 003 同步記錄，以 booking_id 為鍵，可用既有 `/audit-log`、`/notifications` 查。 |

需求卡待決問題的參考答案：

1. **歸屬**：Invoicing 是獨立 Context。兩段翻譯：Invoicing Application 把 Order／Booking／Trip 翻成 `InvoiceRequest`（自己的語言）；Adapter 再把 `InvoiceRequest` 翻成服務商欄位。
2. **時機與鎖**：同一次付款呼叫內「先記帳、後開立」：鎖內只建 PENDING，鎖外呼叫一次服務商，重試不在付款請求內。付款回應最多多 3 秒，但不持有全域鎖。
3. **發票資訊存放**：存在 Invoice（`InvoiceRequest.buyer`），不寫入 Booking 或 Order。
4. **Port**：要。`InvoiceIssuer` 宣告在 `domain/invoicing.py`。付款閘道**不**一併 Port 化：本需求沒有給它新的失敗語意，一起改只會擴大變更（ADR 005 第 6 點）。
5. **重試觸發**：本期只提供可呼叫的操作，排程留給維運。
6. **PENDING 過久**：未規定，列為 Unknown，不實作。

## 3. Implementation handoff

**Domain facts**
- Invoicing 擁有 Invoice；一筆 Order 至多一張已開立發票，識別鍵＝order_id＝`merchant_order_no`。
- 發票總額＝Order.amount（D3b 之後是「應付金額」，不是 `booking.total_fare`）。
- 銷售額＝round(總額 ÷ 1.05) 四捨五入、稅額＝總額 − 銷售額，皆為整數。
- 狀態：PENDING（可重試）／ISSUED（號碼不可變）／FAILED（永久或達上限，需人工）。
- 付款成功的事實（PAID、Order、金額）不受發票任何結果影響。

**Forces**
- 外部服務可能慢（3 秒）、停機、忙碌，或「做了但沒回」（逾時＝結果未知）。
- 全域 `store.lock` 是 RLock；`pay_group` 原本在持有鎖時呼叫 `pay`，任何在 `pay` 內「釋放鎖再呼叫」的寫法都會被外層鎖抵銷。
- ADR 003：同步、不引入 Queue。
- 無效發票資訊必須在扣款前被擋下（422）。
- D3b 會改變 Order.amount，D3c 不碰發票（折讓不在範圍）。

**Decision**
- Invoice 為小型 Entity＋狀態機（`Invoice.record`），不是大型 Aggregate；稅額拆分與品項是純函式。
- 一個 Port（`InvoiceIssuer.issue`），三種結果，不拋例外；Adapter 負責代碼與例外翻譯。
- 被否決的較簡單方案：在 `PaymentService.pay` 內直接呼叫服務商並 `try/except` 吞錯。它無法保證：重試能力（沒有 PENDING 紀錄）、逾時後不重複開立、鎖外呼叫，也讓供應商代碼進入付款流程。

**External systems**
- 發票服務商：「為這筆 Order 開立這張發票」。Domain 必須分辨：已取得號碼／永久不可能／暫時或未知。

**Unknowns（本解答的假設）**
- PENDING 逾時升級：未實作。
- 對 FAILED 執行重試：假設不呼叫服務商，直接回傳（卡片未明說，見第 6 節缺陷 D2）。
- 重試時的 `issue_date`：沿用付款當日（卡片未定義，D5）。
- 已退票但發票仍 PENDING：仍可重試開立（卡片未定義，D6）。
- 同時兩個重試：都可能呼叫服務商；服務商冪等保證只有一張，`attempts` 可能多算一次（單程序可接受，ADR 005）。
- 真實服務商的 `merchant_order_no` 長度限制未知（order_id 是 36 字元 UUID）。
- Adapter 從未對真實服務商執行過契約測試：**未驗證**，只驗證了模擬 transport。

**Proof obligations → 測試**

| 義務 | 測試 |
|---|---|
| 一般／團體各一張，團體整團一張 | `test_einv_001_*` |
| 任何發票失敗付款仍 200／PAID／Order 金額不變 | `test_einv_002_invoice_failure_never_affects_payment`（9001／1001／1002／DOWN）、`test_einv_002_provider_timeout_*` |
| 呼叫服務商時不持有全域鎖（一般與團體路徑） | `test_einv_002_provider_is_called_outside_the_store_lock[False/True]` |
| 稅額拆分三個試算值、皆為 int | `test_einv_003_*` |
| 品項一行、單價向下取整 | `test_einv_004_*`（1,225／2 → 612；1,925／3 → 641） |
| 逾時後重試不產生第二張 | `test_einv_005_*` |
| 狀態可查、404 | `test_einv_006_*` |
| 暫時失敗累計次數與最後錯誤；3 秒邊界 | `test_einv_007_*`（兩個） |
| 第 5 次失敗轉 FAILED、之後不再呼叫 | `test_einv_008_*` |
| 1001／1002 直接 FAILED | `test_einv_009_*` |
| 2001 以原號碼 ISSUED | `test_einv_010_*` |
| ISSUED 不重送、遲到結果不改號 | `test_einv_011_*` |
| 統編／載具／皆無對應的服務商欄位 | `test_einv_012_*` |
| 7 種無效輸入 422、未扣款、無 Order、未呼叫服務商 | `test_einv_013_*` |
| Audit／通知僅在 ISSUED／FAILED 轉換時產生 | `test_einv_014_*` |
| 每種代碼、逾時、停機都可模擬並正確映射；應用程式只接模擬服務商 | `test_einv_015_*`（三個） |

## 4. 反事實檢查（counterfactual）

每條新規則各破壞一次、跑聚焦測試、還原。25／25 killed，`failing_evidence` 皆為測試失敗而非建置錯誤：兩個「失敗隔離」mutant 是付款 API 因 `TimeoutError`／`RuntimeError` 穿透而失敗（正是要防止的行為），其餘為斷言失敗。另有一個等價 mutant 的 survived 紀錄，見下方說明。JSON 在 `evidence/counterfactual/`。

| AC | 規則 | 破壞方式 | 結果 |
|---|---|---|---|
| EINV-001 | 付款成功即開立 | `pay` 中 `self.invoicing.issue(order.order_id)` → `pass` | killed |
| EINV-001 | 團體整團一張 | 品項數量 `passenger_count` → `1` | killed |
| EINV-006 | 狀態值可查 | `PENDING = "PENDING"` → `"WAITING"` | killed |
| EINV-006 | 查無發票 404 | `INVOICE_NOT_FOUND` 的 `404` → `400` | killed |
| EINV-003 | 稅率 5% | `VAT_RATE_PERCENT = 5` → `6` | killed |
| EINV-003 | 四捨五入 | `remainder * 2 >= gross_percent` → `remainder >= gross_percent`（變成無條件捨去） | killed |
| EINV-004 | 單價向下取整 | `//` → 無條件進位 | killed |
| EINV-004 | 單價向下取整（對四捨五入） | `//` → `round(a / q)` | 先 survived，補 3 人案例後 killed |
| EINV-008 | 上限 5 次 | `MAX_ISSUE_ATTEMPTS = 5` → `6` | killed |
| EINV-008 | 上限比較 | `>=` → `>` | killed |
| EINV-009 | 永久失敗不重試 | 移除 `REJECTED or` | killed |
| EINV-007 | 3 秒逾時 | `CALL_TIMEOUT_SECONDS = 3` → `4` | killed |
| EINV-005 | 冪等鍵＝order_id | `merchant_order_no` 改為每次隨機 | killed |
| EINV-010 | 2001 視為成功 | `ISSUED_CODES` 移除 `2001` | killed |
| EINV-011 | ISSUED 不重送 | Service 守門 → `if False:` | killed |
| EINV-011 | 號碼不可變 | `Invoice.record` 守門 → `if False:` | killed |
| EINV-002 | 逾時不外洩成例外 | `except (TimeoutError, ConnectionError)` → 只接 `ConnectionError` | killed |
| EINV-002 | 忙碌是結果不是例外 | `return UNAVAILABLE` → `raise RuntimeError` | killed |
| EINV-002 | 鎖外呼叫 | `result = self.issuer.issue(...)` → 包進 `with self.store.lock:` | killed |
| EINV-013 | 統編 8 位數字 | `[0-9]{8}` → `[0-9]{7,8}` | killed |
| EINV-013 | 手機條碼格式 | 允許小寫與 6 碼 | killed |
| EINV-013 | 二者擇一 | 檢查 → `if False:` | killed |
| EINV-013 | 統編須附公司名稱 | 檢查 → `if False:` | killed |
| EINV-014 | FAILED Audit 含錯誤代碼 | detail 移除 `error=` | killed |
| EINV-014 | ISSUED 通知 | 移除通知 | killed |

教學提示：有兩個 mutant 曾經 **survived**，值得拿來討論「測試證明的是什麼」：
- **單價 `round(amount / quantity)`**：原本只有 1,225 ÷ 2 ＝ 612.5 一個案例，Python 的銀行家捨入剛好得到 612，與向下取整相同，mutant 存活。補上 3 人案例（1,925 ÷ 3 → 641，四捨五入會得 642）後 killed（`unit-price-floor-vs-round.json`）。這正是外掛規則「survived 代表沒有測試保護這條規則，補測試再跑一次」。
- **四捨五入邊界 `>=` → `>`**：仍然 survived，而且**無法**被殺死，是等價 mutant（`vat-half-boundary-EQUIVALENT-survived.json`）。5% 稅率下整數總額永遠不會剛好落在 .5：若 總額 × 100 ÷ 105 ＝ n + ½，則 總額 × 200 ＝ 105 × (2n + 1)，左邊是偶數、右邊是奇數，不可能。所以「四捨五入」與「五捨六入」對所有合法輸入結果相同；同理，Agent 寫 `round(total / 1.05)` 也會通過所有試算，「不使用浮點數」只能靠 Code Review。

## 5. Agent 常見錯誤（巡堂檢查清單）

1. **在鎖內呼叫服務商**。最隱蔽的版本：在 `pay` 裡把呼叫移到 `with self.store.lock` 外面，卻沒發現 `pay_group` 原本在持有 RLock 時呼叫 `pay`，團體路徑仍在鎖內。看 `pay_group`。
2. **發票失敗拋 `DomainError`**：Order 已建立、Booking 已 PAID，但 API 回 409／500，客戶被扣款卻看到失敗。
3. **`except Exception: pass`**：付款回 200，但沒有 PENDING 紀錄、無法重試、沒有人知道失敗。
4. **在付款請求內同步重試 5 次**：最壞 15 秒，且常常在鎖內。
5. **逾時當作「沒開出來」**：重試時換新的 `merchant_order_no`，或把逾時直接判 FAILED。
6. **2001 當作錯誤**，或重試時沒有使用回傳的原號碼。
7. **用 `booking.total_fare` 當發票金額**：今天碰巧等於 Order.amount，D3b 之後就錯了。
8. **供應商代碼進入 Domain／Service**（`if code == "9001"`），或 Port 以供應商命名（`EzPayClient`、`HttpInvoiceClient`），或 Port 宣告在 infrastructure 檔案。
9. **把發票欄位塞進 Order／Booking**（`Order.invoice_number`），改動 `OrderResponse` 合約。
10. **驗證放在扣款之後**：回 422 但 Order 已建立；或只在 Pydantic 驗證，規則散在 schema（可接受，但要問「規則的家在哪」）。
11. **重試次數算錯**：「重試 5 次」實作成 1 + 5 = 6 次呼叫。
12. **FAILED／ISSUED 仍呼叫服務商**。
13. **浮點稅額**：`round(total / 1.05)` 通過所有測試（見上一節），只能靠 Review。
14. **順手把付款閘道也 Port 化、或導入 Queue／背景執行緒**：超出範圍，且違反 ADR 003 卻沒寫新 ADR。
15. **測試只有 happy path**，或 import `requests`／`httpx` 真的打網路。
16. **PENDING 每次失敗都發通知**（EINV-014 明確不需要）。

## 6. 需求卡檢查結果

**數字與範例全部一致**：700 → 667／33、3,500 → 3,333／167、665 → 633／32 均正確；665 可由 M002 企業會員成人 1 位重現、3,500 為 T001 成人 5 位團體；手機條碼、發票號碼格式、5 次（含第一次）在「商業數字」與 EINV-008 一致；「團體整團一張」與 EINV-004 的「quantity 為旅客數」一致；EINV-013 的「不扣款」與 EINV-002 不衝突。

**缺陷與建議修正**（依影響排序）：

| # | 問題 | 影響 | 建議修正文字 |
|---|---|---|---|
| D1 | 沒有定義 API：付款 body 怎麼帶發票資訊、查詢與重試的路徑、422 錯誤碼。 | 各組做出不同介面，主持人無法用同一份驗收測試；Agent 會自己發明。 | 新增「API」小節：`POST /bookings/{id}/pay` 與 `POST /group-bookings/{id}/pay` 可選 body `{"invoice":{"business_id","company_name","mobile_barcode"}}`；`GET /orders/{order_id}/invoice` 回 `status`、`invoice_number`、`attempts`、`last_error`；`POST /orders/{order_id}/invoice/retry` 回同格式；EINV-013 錯誤碼 `INVALID_INVOICE_INFO`。（若刻意留給學員設計，至少規定錯誤碼與查詢路徑。） |
| D2 | 對 `FAILED` 執行「重試開立」的行為未定義。EINV-008 只說「不再**自動**重試」，而 EINV-007 的重試可由維運人員觸發。 | 有人會讓人工重試再次呼叫服務商，與「需人工處理」矛盾。 | EINV-011 改為：「`ISSUED` 或 `FAILED` 的發票執行重試時不呼叫服務商，直接回傳原結果；`FAILED` 的人工處理不在本期範圍。」 |
| D3 | EINV-007「記錄失敗次數」與 EINV-008「累計呼叫 5 次」計數單位不同。 | 實作者分不清 attempts 從 0 還是 1 起算、是否含成功那次。 | EINV-007 改為「記錄呼叫次數（含第一次）與最後錯誤」。 |
| D4 | EINV-004 沒有「單價需要取整」的試算；所有範例都整除。 | 規則存在但沒有可對照的數字。 | 試算加一行：「T001 成人 1＋學生 1：amount 1,225、quantity 2、unit_price 612」。 |
| D5 | 重試時的 `issue_date` 未定義（付款日或重試日）。 | 跨日重試時結果不同。 | 加一句：「`issue_date` 為付款當日（系統 Clock），重試沿用同一日期。」 |
| D6 | 整筆退票時發票仍是 `PENDING`，之後的重試是否還要開立，未定義。 | 可能對已退票訂單開出新發票；作廢又不在本期。 | 「不在本期範圍」加一句：「退票不改變發票狀態；PENDING 發票仍可重試開立，作廢與折讓於下一期處理。」 |
| D7 | 「四捨五入」與「不使用浮點數」無法用範例驗證：5% 下整數總額不會剛好 .5（見第 4 節），`round(總額/1.05)` 也會得到相同結果。 | 規則只能靠 Review 檢查（不算錯，但主持人要知道）。 | 可選：在商業數字加「整數算法：銷售額 = ⌊(含稅總額 × 200 + 105) ÷ 210⌋」，或僅在主持人筆記說明。 |
| D8 | 「單次呼叫逾時 3 秒」列在「商業數字」，但它是整合設定，不是法規或商業規則。 | 不是錯誤；是好的討論點（它應該住在 Adapter）。 | 不改，或移到「發票服務商 API」段。 |

## 7. 25 分鐘可行性與建議切片

參考解答規模：新增正式程式約 270 行、修改約 60 行、測試約 300 行；完整 15 條 AC 加上 25 個反事實檢查。

| 時段 | 活動 |
|---|---|
| 0–4 分 | 讀卡、回答待決問題 1–4（Context、Port、鎖、資料存放） |
| 4–7 分 | 寫 handoff／指示 Agent（facts、forces、proof obligations） |
| 7–17 分 | Agent 實作與測試（核心切片） |
| 17–23 分 | Review：鎖、失敗隔離、冪等；跑 2–3 個 counterfactual |
| 23–25 分 | 緩衝 |

**判定：完整 15 條 AC 在 25 分鐘內不可行**（多數組只能完成實作，沒有時間 Review 與反事實檢查，而這兩者才是本段教學重點）。**核心切片可行**。

建議切片：

- **必做**：EINV-001、002、003、005、006、007、008、009、010、011、015（Port＋Adapter＋模擬服務商、狀態機、鎖外呼叫、冪等、上限）。
- **砍掉或改成加分**：EINV-012／013（發票資訊與驗證，約占程式與測試的 25%，且與 DDD 主題關聯低）、EINV-014（Audit／通知，機械性工作）、EINV-004 的描述字串細節（保留「一行、總額＝Order.amount」即可）。
- **反事實檢查只做 3 個**：重試上限（`MAX_ISSUE_ATTEMPTS`）、鎖外呼叫、冪等鍵。
- 主持人應先公布 D1 的 API 形狀，省下 Agent 發明介面與學員爭論的時間。
- 段落結束時發放本目錄作為 Recovery 起點。

## 8. 對 D3b／D3c 的影響（Recovery 注意事項）

- D3b 會讓 Order.amount 變成「應付金額」。本解答的發票金額取 `order.amount`，因此自動正確；請學員不要改成 `booking.total_fare`。可以加一個 D3b 測試：M001 成人 1 位折 200 點 → 發票總額 500、銷售額 476、稅額 24。
- D3b 需要修改扣款金額，位置在 `PaymentService._charge`（原 `pay` 的內容）。`pay` 現在只是「扣款＋鎖外開立」兩行，`PaymentService` 建構子多了 `invoicing` 參數（`tests/unit/test_services.py` 的 `payment_service()` helper 示範如何建立）。
- D3c（部分取消退款）不碰發票；折讓明確不在範圍。若學員問「部分退款後發票怎麼辦」，答案是下一期的作廢／折讓需求。
- `store.invoices` 以 order_id 為鍵，`reset_state()` 會一併重置模擬服務商。

## 9. Registry 參考狀態

`domain-memory/` 是表現良好的一組在 D3a 檢查點 5 結束時的 Registry：D2 的 reviewed Registry（`reference-registry` bundle，tag `dlc-d2-reviewed`，CP-CORE-001）原樣保留，加上 10 筆**候選**。輸入檔是 `evidence/registry-candidates.json`，在 Repo 根目錄以一行登記（約 20 秒）：

```powershell
py -3.13 -X utf8 ..\..\tools\make_record.py --batch registry-candidates.json --allow-unclassified --upsert
```

`--allow-unclassified` 是因為 `tests/integration/test_e_invoice.py` 不在 D1 確認過的 source map 內（新的 `src/` 與 `docs/` 檔案在已確認的資料夾下，不需要）。本段**不做**治理升級：沒有 Change Package、沒有簽章 commit。

| 候選 | 內容 | 證據 |
|---|---|---|
| `contexts:invoicing` | 新 Context（supporting），持有 Invoice、購票人發票資訊、稅額拆分、重試上限、Port | ADR 005、`domain/invoicing.py` |
| `vocabulary:invoice`、`invoice-buyer-info`、`issue-attempt` | 電子發票、購票人發票資訊、開立呼叫次數 | business-rules EINV 表、`domain/invoicing.py` |
| `rules:EINV-003` | 稅額拆分（總額＝Order.amount、四捨五入、整數） | 規則表、`split_vat`、`test_einv_003_*` |
| `rules:EINV-008` | 重試上限 5 次（含 EINV-007／009） | 規則表、`Invoice.record`、`test_einv_008/009_*` |
| `rules:EINV-005` | 冪等：order_id＝商家訂單編號，2001 視為成功（含 EINV-010） | 規則表、Adapter、`test_einv_005/010_*` |
| `rules:EINV-002` | 失敗隔離：鎖內記帳、鎖外呼叫，失敗不回滾付款 | 規則表、`PaymentService.pay`、`InvoicingService.issue`、`test_einv_002_*` |
| `interactions:payment-triggers-invoicing` | payment（producer，Order 是金額唯一來源）→ invoicing | `payment_service.py`、`invoicing_service.py` |
| `decisions:ADR-005` | 發票經由 Port 開立，失敗不回滾付款 | ADR 005 Decision 1–6 |

驗證（產製時實測，Repo 根目錄）：

| 指令 | 結果 |
|---|---|
| `validate` | `Registry is valid.` |
| `validate --require-reviewed` | 失敗，列出新候選 not reviewed（預期，Runbook 已說明） |
| `verify-audit` | `valid`，72 events，head `sha256:d6b8f6bf…1a6e` |
| `coverage` | 6 Contexts、24 詞、20 規則、2 Aggregates；缺口 `without_aggregate`：inventory、membership、invoicing（Invoice 是小型 Entity＋狀態機，刻意不登記 Aggregate）；6 個 Context 都無 Contract |
| `verify-evidence` | 192 個引用：177 current、15 stale（exit 1，預期） |
| `verify-sources` | `stale`：`src`、`tests`、`docs/adr` 檔案變更，`docs/requirements` 內容變更 |

**stale 的 reviewed 事實**（引用行被 `payment_service.py`、`store.py` 的修改改變了；15 筆都是 reviewed，候選沒有 stale）：`contexts:payment`、`vocabulary:available-seats`、`vocabulary:order`、`vocabulary:group-payment-compensation`、`aggregates:booking`、`aggregates:order`、`rules:GROUP-PAY-002`、`rules:PAYMENT-001`、`rules:ORDER-002`、`rules:MEMBER-004`、`interactions:payment-settles-booking`、`interactions:payment-compensates-inventory`、`decisions:ASIS-001`、`decisions:ASIS-003`、`decisions:ASIS-004`。內容上仍成立（只是行號移動），沒有被 D3a 推翻的 reviewed 事實。

**D4 要做的事**：

- 以一個 Change Package 把 10 筆候選升為 reviewed（成對核准、簽章 commit）；`test_e_invoice.py` 要先 `confirm-sources` 納入來源，否則引用它的規則無法升級。
- 同一個 Change Package 以 `registry_updates` 重新引用上面 15 筆 stale 的 reviewed 事實（內容不變、更新行號）；改動 reviewed 紀錄必須在 proposal 的 `supersedes` 指名 CP-CORE-001。
- 交接 Unknowns：PENDING 逾時升級、真實服務商契約測試未做、`merchant_order_no` 長度限制（第 3 節）。
