---
type: Term
title: "座位指派"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L42-42"
    excerpt_sha256: "sha256:1aa2b89deab537aacd215ed1d2daf91ec953a39264abe35d4502a03476a00f4c"
  - resource: "src/smart_ticket/domain/records.py#L4-13"
    excerpt_sha256: "sha256:0be683ff1acefd36341a7550d1948e6a9302c5fcd21601889aec4260dd053b18"
  - resource: "src/smart_ticket/application/seat_service.py#L29-35"
    excerpt_sha256: "sha256:8e2b44f85b53cf46d4f7dabc71fe1b9493e11cb50dcdc1477006905343adbfaa"
---
一位旅客在某班次的座位：Seat ID（S001 起）、車廂、排、位置；同班次 Seat ID 不重複。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- Seat Assignment
- SeatAssignment
- Seat ID
