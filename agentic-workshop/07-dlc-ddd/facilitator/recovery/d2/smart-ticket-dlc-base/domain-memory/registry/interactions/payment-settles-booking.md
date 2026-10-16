---
type: Interaction
status: stable
consistency: synchronous
delivery: "PaymentService 讀 total_fare 並直接改寫 Booking.status、seat_ids、assigned_seats（沒有 Booking 擁有的操作）"
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/application/payment_service.py#L25-37"
    excerpt_sha256: "sha256:1dbcab5aec72c20f5881eaa21de0a25f2cf49cb3d956bc29b27d34b84d4a2383"
---
# Relations
- Producer context: [booking](/contexts/booking)
- Consumer context: [payment](/contexts/payment)
