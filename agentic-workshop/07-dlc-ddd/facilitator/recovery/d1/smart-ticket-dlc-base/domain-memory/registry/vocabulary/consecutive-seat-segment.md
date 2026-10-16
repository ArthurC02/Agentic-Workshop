---
type: Term
title: "連續座位區段"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L62-62"
    excerpt_sha256: "sha256:19c1ea0de4babefb0a4f59b3153fcda4672af15284ed83cfefb2e60844426b43"
  - resource: "docs/adr/004-group-seat-atomicity.md#L10-10"
    excerpt_sha256: "sha256:21a97a6b2b9622339882afb743c8c3d525af18be24f2b36f615b1dba36700638"
  - resource: "src/smart_ticket/application/seat_service.py#L37-51"
    excerpt_sha256: "sha256:e42174d062731ccc7fa85620cc1c0833bd98288a27ffdb3e0553c5510044af9b"
---
同一車廂（每車廂 20 個位置）內連號且完全空著的一段座位；團體訂票只能配置在這樣的一段內，不可跨車廂。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- Consecutive Seats
