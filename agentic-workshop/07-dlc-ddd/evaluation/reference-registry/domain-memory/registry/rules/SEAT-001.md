---
type: Business Rule
status: stable
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L42-42"
    excerpt_sha256: "sha256:1aa2b89deab537aacd215ed1d2daf91ec953a39264abe35d4502a03476a00f4c"
  - resource: "src/smart_ticket/application/seat_service.py#L10-18"
    excerpt_sha256: "sha256:8847e4da24867d69551027f85bed2b955ddbd692a9fdbdcdb2d7673bec0ace32"
  - resource: "tests/integration/test_seats.py#L6-13"
    excerpt_sha256: "sha256:af5da76ce1f53add547eaf2cafe3715208b93c2d9add85ce6d0189c316ea43ef"
---
同一班次內 Seat ID 不可重複配置。

# Relations
- Contexts: [inventory](/contexts/inventory)
