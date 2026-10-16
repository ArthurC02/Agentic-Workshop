---
type: Term
title: "訂票狀態"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L15-15"
    excerpt_sha256: "sha256:5b6e93663bbb50a77b5ad7e3eb90cdfa951b8d37f44998ccec99b3dd0b08d92d"
  - resource: "docs/requirements/business-rules.md#L21-21"
    excerpt_sha256: "sha256:42ded7967f3dee77693a28ae91bb01972efbc1531674d3b0aa38907890e69d4f"
  - resource: "docs/requirements/business-rules.md#L36-36"
    excerpt_sha256: "sha256:241ecfef191bedfde9a5a28862502cb147e7fcb0d1a6122529e2ebe86236fa8f"
  - resource: "docs/requirements/business-rules.md#L67-67"
    excerpt_sha256: "sha256:1f6ea53b7baca0e4a56185661be48b36b49ad4fa7f5db482ac1ec312aeac2be1"
  - resource: "src/smart_ticket/domain/models.py#L10-14"
    excerpt_sha256: "sha256:f1dc0212ab95c341ca9638f229aa36c8c794409dd8ee6cf95f99b13b80424ac1"
---
建立後為 PENDING_PAYMENT；付款成功轉 PAID；已付款退票轉 REFUNDED；團體付款失敗轉 CANCELLED。一般付款失敗維持 PENDING_PAYMENT。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- BookingStatus
- PENDING_PAYMENT
- PAID
- CANCELLED
- REFUNDED
