---
type: Interaction
status: draft
consistency: synchronous
delivery: "PaymentService 讀 total_fare 並直接改寫 Booking.status、seat_ids、assigned_seats（沒有 Booking 擁有的操作）"
sources:
  - resource: "src/smart_ticket/application/payment_service.py#L25-37"
    excerpt_sha256: "sha256:17da3e858e75ef4915195073d2be6352d8c77141c6d8d912b22ae5324c43a764"
---
# Relations
- Producer context: [booking](/contexts/booking)
- Consumer context: [payment](/contexts/payment)
