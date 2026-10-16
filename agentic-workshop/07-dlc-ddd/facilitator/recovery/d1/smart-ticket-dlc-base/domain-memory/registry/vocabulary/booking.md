---
type: Term
title: "訂票"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L11-15"
    excerpt_sha256: "sha256:4ad7d7efab7c15ab9fc7f02f521f49f4c4c03793e780266d8fad358856d3b8ff"
  - resource: "src/smart_ticket/domain/models.py#L43-55"
    excerpt_sha256: "sha256:d274efe92e7e8610be2e01376d32b519c006bd33e4691a3a68938484c5a36f88"
---
一位或多位旅客對同一班次的一次訂位，持有旅客、狀態、總票價、採用優惠明細、座位與可選的會員 id。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Booking
