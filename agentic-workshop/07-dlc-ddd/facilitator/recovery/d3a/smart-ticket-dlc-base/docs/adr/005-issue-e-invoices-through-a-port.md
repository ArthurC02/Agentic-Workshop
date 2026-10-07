# ADR 005：電子發票經由 Port 開立，失敗不回滾付款


## Context

財務要求每筆付款成功的 Order 開立電子發票，由外部發票服務商代開。這是系統第一個真正在程序外、會變慢、逾時、停機、甚至「做了但沒回覆」的協作者。現有付款閘道 `MockPaymentGateway` 沒有 Port，`PaymentService` 直接依賴具體類別，且所有 Use Case 都在全域 `store.lock`（RLock）內執行。

需求卡 01 的限制：付款結果不得因發票失敗改變（EINV-002）；一筆 Order 至多一張發票，以 order_id 為服務商的商家訂單編號（EINV-005）；暫時失敗可重試，累計 5 次呼叫後轉 FAILED（EINV-007／008）；逾時代表結果未知。

## Decision

Status：Accepted。

1. **新增 Invoicing Context**（`domain/invoicing.py`、`application/invoicing_service.py`）。Invoice 以 order_id 為識別，狀態 PENDING／ISSUED／FAILED，自己持有購票人發票資訊（統編、公司名稱、手機條碼），不寫進 Booking 或 Order。稅額拆分、品項、重試上限、狀態轉移都在 Invoicing 的 Domain。
2. **Port `InvoiceIssuer`** 宣告在 `domain/invoicing.py`，用 Invoicing 的語言：輸入 `InvoiceRequest`，輸出三種結果 `ISSUED`（含原號碼的重複開立）、`REJECTED`（永久失敗）、`UNAVAILABLE`（暫時或未知）。Port 不拋例外。
3. **Adapter `EInvoiceProviderAdapter`**（`infrastructure/einvoice_provider.py`）是唯一知道服務商欄位名稱（`merchant_order_no`、`buyer_ban`…）、回應代碼（0000／2001／1001／1002／9001）、3 秒逾時與連線例外的地方，把它們翻譯成上述三種結果。本期 transport 為 `SimulatedEInvoiceProvider`（無網路，測試可排入任意代碼與延遲）；接正式環境只替換 transport。組裝在 `api/dependencies.py`。
4. **失敗隔離**：付款在鎖內完成扣款、建立 Order、PAID，並同時建立 PENDING Invoice（「要開發票」這件事與付款一起成立）；釋放鎖之後才呼叫服務商做第一次開立。任何發票結果只改 Invoice 狀態，付款 API 照樣回 200。
5. **重試**：提供 `POST /orders/{order_id}/invoice/retry`，供排程或維運觸發；本期不自動排程。每次使用相同 order_id，ISSUED／FAILED 不再呼叫服務商。
6. 付款閘道的 Port 化不在本次範圍：它沒有新的失敗語意需要處理，一起改只會擴大變更。

## Consequences

- 付款回應最多多等一次呼叫（3 秒），但不會持有全域鎖，其他請求不受影響；重試不在付款請求內進行。
- 逾時後服務商可能已開立；因為以 order_id 冪等、服務商回 2001 視為成功，重試不會開出第二張。
- 兩個重試請求若同時進行，兩者都可能呼叫服務商；服務商的冪等鍵保證只有一張發票，Invoice 只接受第一個結果，但 attempts 可能多算一次。若改為多程序部署，需要以 Invoice 為單位的鎖或樂觀版本。
- 仍為同步呼叫，沿用 ADR 003 不引入 Queue；若付款延遲不可接受，下一步是把第一次開立也交給重試排程（只需移除 `PaymentService.pay` 中的一行）。
- PENDING 超過多久升級人工處理（需求卡待決問題 6）尚未定義。
