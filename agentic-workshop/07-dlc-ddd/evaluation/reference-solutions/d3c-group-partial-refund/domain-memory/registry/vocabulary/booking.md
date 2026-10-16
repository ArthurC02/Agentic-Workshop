---
type: Term
title: "訂票"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L11-15"
    excerpt_sha256: "sha256:4ad7d7efab7c15ab9fc7f02f521f49f4c4c03793e780266d8fad358856d3b8ff"
  - resource: "src/smart_ticket/domain/models.py#L43-55"
    excerpt_sha256: "sha256:79b4ac99efb2e12eeb455c9a1d9b71ecbe8748c36417d8b93c6917709a655965"
---
一位或多位旅客對同一班次的一次訂位，持有旅客、狀態、總票價、採用優惠明細、座位與可選的會員 id。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Booking
