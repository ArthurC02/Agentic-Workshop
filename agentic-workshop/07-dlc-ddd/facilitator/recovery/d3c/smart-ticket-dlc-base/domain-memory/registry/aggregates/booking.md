---
type: Aggregate
status: stable
domain_services: []
policies: []
prohibited_dependencies: []
root: Booking
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/domain/models.py#L43-55"
    excerpt_sha256: "sha256:79b4ac99efb2e12eeb455c9a1d9b71ecbe8748c36417d8b93c6917709a655965"
  - resource: "docs/requirements/business-rules.md#L11-15"
    excerpt_sha256: "sha256:4ad7d7efab7c15ab9fc7f02f521f49f4c4c03793e780266d8fad358856d3b8ff"
  - resource: "src/smart_ticket/application/payment_service.py#L23-24"
    excerpt_sha256: "sha256:9281061c4a1b574e8bba100456dd0bea317d35b00f0b5626b8c827db82544b04"
  - resource: "src/smart_ticket/application/refund_service.py#L22-23"
    excerpt_sha256: "sha256:a3da4b76e6ccf50d999b03d698256085a1406d618764236dad008763a711e8fb"
---
# Relations
- Context: [booking](/contexts/booking)

# Entities
- Passenger

# Value objects
- AppliedDiscount

# Commands
- create
- create_group
- pay
- change
- refund

# Allowed dependencies
- pricing
- inventory
- membership

# Invariants
- 狀態只能 PENDING_PAYMENT → PAID → REFUNDED，或團體 PENDING_PAYMENT → CANCELLED
- 一般訂票 1–4 人、團體 5–20 人
- 總票價 = 採用優惠明細 amount 加總
- 已付款訂票只能退一次
