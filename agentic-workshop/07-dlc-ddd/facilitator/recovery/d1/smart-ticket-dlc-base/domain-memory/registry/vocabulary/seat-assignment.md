---
type: Term
title: "座位指派"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L42-42"
    excerpt_sha256: "sha256:1aa2b89deab537aacd215ed1d2daf91ec953a39264abe35d4502a03476a00f4c"
  - resource: "src/smart_ticket/domain/records.py#L4-13"
    excerpt_sha256: "sha256:af9d9f40fe0be7b462fed466c99f5ec5582f272d00116f907cac685489338811"
  - resource: "src/smart_ticket/application/seat_service.py#L29-35"
    excerpt_sha256: "sha256:64dec2f8fcd3950e5a2a98b66251ec566b16757f86ea5d5c911ceee4a631fdb8"
---
一位旅客在某班次的座位：Seat ID（S001 起）、車廂、排、位置；同班次 Seat ID 不重複。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- Seat Assignment
- SeatAssignment
- Seat ID
