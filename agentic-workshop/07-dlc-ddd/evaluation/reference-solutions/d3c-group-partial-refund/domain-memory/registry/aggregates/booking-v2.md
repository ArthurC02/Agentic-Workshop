---
type: Aggregate
status: draft
domain_services: []
policies: []
prohibited_dependencies: []
root: Booking
sources:
  - resource: "src/smart_ticket/domain/models.py#L74-114"
    excerpt_sha256: "sha256:fcfc6aca589ba9e8c6ac2fd9a71e9d5870812ae115e5b5ef07c7e6630116c780"
  - resource: "src/smart_ticket/domain/models.py#L9-9"
    excerpt_sha256: "sha256:ef11c5bb8560846e43e7fbcdd0b7a17d6804b35a1c2a90def5ed753764370658"
  - resource: "docs/adr/007-group-booking-owns-passenger-cancellation.md#L18-20"
    excerpt_sha256: "sha256:16dc0399d63f2569c952c1e784aa852421a043c766c7d9f8acdd0d6a2fc8b3ed"
---
# Relations
- Context: [booking](/contexts/booking)

# Entities
- Passenger

# Value objects
- AppliedDiscount
- PassengerCancellation

# Commands
- create
- create_group
- pay
- change
- refund_in_full
- cancel_passengers

# Allowed dependencies
- pricing
- inventory
- membership

# Invariants
- 狀態 PENDING_PAYMENT → PAID →（部分取消 n 次仍 PAID）→ REFUNDED，或團體 PENDING_PAYMENT → CANCELLED
- 一般訂票 1–4 人；團體建立時 5–20 人，部分取消後有效旅客 ≥ 5 或 0
- Σ退款 + Σ手續費 + Σ有效旅客票價 = Order.amount；total_fare 與 applied_discounts 不因取消改變
- 每位旅客只能被取消一次；部分取消過的訂票不可整筆退票（取代 reviewed aggregates:booking 的「已付款訂票只能退一次」）
