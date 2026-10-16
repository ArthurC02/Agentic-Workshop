---
type: Interaction
status: draft
consistency: synchronous
delivery: "團體付款失敗時 PaymentService 直接呼叫 SeatService.release 釋放全部座位"
sources:
  - resource: "docs/adr/004-group-seat-atomicity.md#L10-10"
    excerpt_sha256: "sha256:21a97a6b2b9622339882afb743c8c3d525af18be24f2b36f615b1dba36700638"
  - resource: "src/smart_ticket/application/payment_service.py#L27-31"
    excerpt_sha256: "sha256:a046f41bf8941115055b5dd5d7703d84ec54d58bf70b13e90961f3d3d85a1b0c"
---
# Relations
- Producer context: [inventory](/contexts/inventory)
- Consumer context: [payment](/contexts/payment)
