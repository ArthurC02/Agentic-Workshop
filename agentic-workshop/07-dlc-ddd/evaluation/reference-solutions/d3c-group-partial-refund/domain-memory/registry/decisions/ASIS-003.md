---
type: Decision
status: stable
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/payment_service.py
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/application/payment_service.py#L5-16"
    excerpt_sha256: "sha256:75ccfdf8da512cd3ab9ca0f8f5439c8e123716261da6be77527a16fc5027b85f"
  - resource: "src/smart_ticket/infrastructure/payment_gateway.py#L3-12"
    excerpt_sha256: "sha256:5965bafa9f1220f7b71501b95509dc1f050a4ac270f343f74a912cd3431f3480"
---
現況觀察（非已核准決策）：PaymentService 直接依賴具體 MockPaymentGateway（無 Port），閘道只有 charge；團體補償、Booking 狀態改寫都寫在 PaymentService 內。
