---
type: Term
title: "最有利單一優惠"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L46-48"
    excerpt_sha256: "sha256:3228e1b59ca1744056b2b033f361d370476c257b68f8dc80e372cd2484ebc777"
  - resource: "docs/requirements/discount-overview.md#L3-3"
    excerpt_sha256: "sha256:fc5678df1c855e235ef5777cbb7204fccab27e7fccce5282e83a8688c78d77f1"
  - resource: "src/smart_ticket/domain/discounts.py#L27-34"
    excerpt_sha256: "sha256:c63f7dca019714e6017457c2a920d5da70b642dcb309d262f5b73635c6157c45"
---
每位旅客實際採用的唯一優惠：在所有符合的資格（含成人全額預設）中取 rate 最低者；多項優惠不疊加，也不依條件先後取第一個符合者。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Best Single Discount
- DiscountPolicy
