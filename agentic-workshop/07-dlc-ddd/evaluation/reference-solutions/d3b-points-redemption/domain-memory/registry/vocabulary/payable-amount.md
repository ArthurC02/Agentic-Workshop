---
type: Term
title: "應付金額"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L112-112"
    excerpt_sha256: "sha256:57ce2cd058588b329fdbf45bb7ce5ba6ec432abb41ac7b1b4503e8c1d92bf813"
  - resource: "docs/requirements/business-rules.md#L114-114"
    excerpt_sha256: "sha256:1adc4ed17d37fa33106215c4edfa65491c4d9a5b92f13728f46fa80a39866639"
  - resource: "src/smart_ticket/domain/models.py#L59-62"
    excerpt_sha256: "sha256:ecd26d49bb4aa4034cff62d6124b9289adf24d5c2470428cd93c53efa28e985f"
---
優惠後總額（total_fare）減去折抵點數價值；付款向閘道扣的就是它，Order.amount 等於它，電子發票與退款再從 Order.amount 取。total_fare 與 applied_discounts 不因折抵改變。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [payment](/contexts/payment)

# Synonyms
- payable_amount
