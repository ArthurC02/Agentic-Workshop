---
type: Term
title: "採用優惠明細"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L49-49"
    excerpt_sha256: "sha256:8fc03deca299452ab13b7a76cf273bd48841263635e66bf5e60df5a978cce0a4"
  - resource: "docs/requirements/discount-overview.md#L7-7"
    excerpt_sha256: "sha256:4250549ebb7c87077566d387bb4fd726a6252a08284155f1fa6f17c11e743af4"
  - resource: "src/smart_ticket/domain/models.py#L36-41"
    excerpt_sha256: "sha256:6ef1b2b7aa6cb53ae57888ec0c34f34bd3091ebc8939471530cd5968e7dc252d"
  - resource: "src/smart_ticket/domain/discounts.py#L14-18"
    excerpt_sha256: "sha256:af7b5a24af5eeee3f3bcd79dc6e57003ea12ceb85a6fa2374805d0a8b5130690"
---
每位旅客實際採用的優惠紀錄：passenger_id、discount_type、rate、amount；建立與改票都會重新產生。文件稱 Fare Result，程式在計價端叫 DiscountResult、在 Booking 上叫 AppliedDiscount。

# Relations
- Contexts: [pricing](/contexts/pricing)
- Contexts: [booking](/contexts/booking)

# Synonyms
- Applied Discount
- applied_discounts
- Fare Result
- DiscountResult
