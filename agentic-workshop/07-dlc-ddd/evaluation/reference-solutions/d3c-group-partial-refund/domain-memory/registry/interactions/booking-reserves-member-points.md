---
type: Interaction
status: draft
consistency: synchronous
delivery: "BookingService 與 GroupBookingService 在全域鎖內、寫入前呼叫 MemberService.reserve_points(booking)；團體付款失敗（PaymentService）與退票（RefundService）呼叫 restore_points。同步直接呼叫，不用事件。"
sources:
  - resource: "src/smart_ticket/application/booking_service.py#L49-49"
    excerpt_sha256: "sha256:4d545a4401f476ba89dc0b0bc52c6def124306f74cc9065a891ea5e882f0a412"
  - resource: "src/smart_ticket/application/member_service.py#L17-31"
    excerpt_sha256: "sha256:a94643a565714bb0dc718d9404b3ea0ab6fb2efbc060f2df0b67ccd1dbdb691c"
  - resource: "src/smart_ticket/application/payment_service.py#L46-46"
    excerpt_sha256: "sha256:1af66ccac467679d4c59b6271976701f840ee7fd5e522e6b8bb4e4bdb1cf49c7"
  - resource: "src/smart_ticket/application/refund_service.py#L28-28"
    excerpt_sha256: "sha256:34329cc71e71640d522c4e366bab5a39c3de65d2b9e629d83ad52e39c4d74a4f"
---
# Relations
- Producer context: [membership](/contexts/membership)
- Consumer context: [booking](/contexts/booking)
