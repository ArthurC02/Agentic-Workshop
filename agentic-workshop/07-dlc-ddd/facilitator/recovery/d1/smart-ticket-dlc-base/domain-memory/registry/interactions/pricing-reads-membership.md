---
type: Interaction
status: draft
consistency: synchronous
delivery: "Booking 先以 MemberService 取得 Member 物件再傳給 DiscountPolicy；Pricing 直接判斷 Membership 的 MemberType（共用 entity，無 ACL）"
sources:
  - resource: "src/smart_ticket/domain/discounts.py#L5-5"
    excerpt_sha256: "sha256:e143a36f05afeead0036f8d34ecf26ed6aa39dcadbb3e6f7d581bb0063c25f07"
  - resource: "src/smart_ticket/domain/discounts.py#L32-33"
    excerpt_sha256: "sha256:67eff644f630d233a69dae193ed3a268cf2b0faf36f14ace1bea7429d0acab95"
  - resource: "src/smart_ticket/application/booking_service.py#L36-36"
    excerpt_sha256: "sha256:021c91384f09d13901290e95915df465d0f25f2bb185d9e1bcd02d018c2076cb"
---
# Relations
- Producer context: [membership](/contexts/membership)
- Consumer context: [pricing](/contexts/pricing)
