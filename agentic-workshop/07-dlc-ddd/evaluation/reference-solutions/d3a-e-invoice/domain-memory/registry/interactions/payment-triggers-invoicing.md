---
type: Interaction
status: draft
consistency: synchronous
delivery: "PaymentService 在付款鎖內呼叫 InvoicingService.open 傳入 Order（發票金額的唯一來源）建立 PENDING 發票，釋放鎖後呼叫 issue 一次；Invoicing 不回寫 Order 或 Booking。"
sources:
  - resource: "src/smart_ticket/application/payment_service.py#L22-27"
    excerpt_sha256: "sha256:b4cdd687efbb15a72e907b294b0ebfbef9da2176bfc95430de4e6c0eb085bd66"
  - resource: "src/smart_ticket/application/payment_service.py#L52-52"
    excerpt_sha256: "sha256:a017b59cfba92864503f6f24c63ebec8de49ea67088b7b128a5490f75d27e117"
  - resource: "src/smart_ticket/application/invoicing_service.py#L17-24"
    excerpt_sha256: "sha256:2637cf135178de0f1a65112076e9fb84c4d059b850624a303fbe07732e129e9e"
---
# Relations
- Producer context: [payment](/contexts/payment)
- Consumer context: [invoicing](/contexts/invoicing)
