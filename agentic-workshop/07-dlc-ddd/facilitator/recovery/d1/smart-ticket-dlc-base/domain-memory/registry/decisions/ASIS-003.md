---
type: Decision
status: draft
decision_status: observed-design-leak
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/payment_service.py
sources:
  - resource: "src/smart_ticket/application/payment_service.py#L5-16"
    excerpt_sha256: "sha256:8eb3485d79dfb182ec77637c6644f80a7ca453725edab891c9da42ffce1e0554"
  - resource: "src/smart_ticket/infrastructure/payment_gateway.py#L3-12"
    excerpt_sha256: "sha256:5d16161d8e875d8a41f84162b670b4371e207e44acdfe7f903662d7c50bd3166"
---
現況觀察（非已核准決策）：PaymentService 直接依賴具體 MockPaymentGateway（無 Port），閘道只有 charge；團體補償、Booking 狀態改寫都寫在 PaymentService 內。
