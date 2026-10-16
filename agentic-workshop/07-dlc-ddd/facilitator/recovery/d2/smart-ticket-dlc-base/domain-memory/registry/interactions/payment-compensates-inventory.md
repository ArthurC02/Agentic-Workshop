---
type: Interaction
status: stable
consistency: synchronous
delivery: "團體付款失敗時 PaymentService 直接呼叫 SeatService.release 釋放全部座位"
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/adr/004-group-seat-atomicity.md#L10-10"
    excerpt_sha256: "sha256:21a97a6b2b9622339882afb743c8c3d525af18be24f2b36f615b1dba36700638"
  - resource: "src/smart_ticket/application/payment_service.py#L27-31"
    excerpt_sha256: "sha256:6d5c1ab25227ff4eb25b27e14b667c98e9f8cba90d6d1b7a4908e74a40ef4d94"
---
# Relations
- Producer context: [inventory](/contexts/inventory)
- Consumer context: [payment](/contexts/payment)
