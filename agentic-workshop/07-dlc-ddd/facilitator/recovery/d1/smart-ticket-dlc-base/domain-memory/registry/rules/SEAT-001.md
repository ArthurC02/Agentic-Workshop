---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L42-42"
    excerpt_sha256: "sha256:1aa2b89deab537aacd215ed1d2daf91ec953a39264abe35d4502a03476a00f4c"
  - resource: "src/smart_ticket/application/seat_service.py#L10-18"
    excerpt_sha256: "sha256:899c89f91b27542d7ed1c467d31ba272d650a7e50321e19d0cd7454fb137b478"
  - resource: "tests/integration/test_seats.py#L6-13"
    excerpt_sha256: "sha256:af5da76ce1f53add547eaf2cafe3715208b93c2d9add85ce6d0189c316ea43ef"
---
同一班次內 Seat ID 不可重複配置。

# Relations
- Contexts: [inventory](/contexts/inventory)
