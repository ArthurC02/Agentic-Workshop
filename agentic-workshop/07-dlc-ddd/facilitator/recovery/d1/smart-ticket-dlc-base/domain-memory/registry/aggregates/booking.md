---
type: Aggregate
status: draft
domain_services: []
policies: []
prohibited_dependencies: []
root: Booking
sources:
  - resource: "src/smart_ticket/domain/models.py#L43-55"
    excerpt_sha256: "sha256:d274efe92e7e8610be2e01376d32b519c006bd33e4691a3a68938484c5a36f88"
  - resource: "docs/requirements/business-rules.md#L11-15"
    excerpt_sha256: "sha256:4ad7d7efab7c15ab9fc7f02f521f49f4c4c03793e780266d8fad358856d3b8ff"
  - resource: "src/smart_ticket/application/payment_service.py#L23-24"
    excerpt_sha256: "sha256:6dba43d6280a7296fe04eb8908ec0348cd0440c81e649db199962d37fd0e17e7"
  - resource: "src/smart_ticket/application/refund_service.py#L22-23"
    excerpt_sha256: "sha256:967a8860f5f8820e02ebc89a10f342dbb87fa930c4be0eb5bbfc1c6dbc8abdb5"
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
