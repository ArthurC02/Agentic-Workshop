---
type: Business Rule
status: stable
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L62-63"
    excerpt_sha256: "sha256:3f827c2e0a36b984b1654d5894d0dd894bd4dcd0fb6663ef768d76d7dfcf6139"
  - resource: "src/smart_ticket/application/seat_service.py#L43-51"
    excerpt_sha256: "sha256:4755e4803f673661d0cd599c1fd9c64a578ab1c425c81d350c4eea9c346b38e8"
  - resource: "tests/integration/test_group_creation.py#L58-64"
    excerpt_sha256: "sha256:f7e2029468d4a33ef85c05bf2cefb6e8d6087e8daf232609fef8d5ec8764d5fe"
---
團體訂票必須配置同一車廂內的連續座位；找不到完整區段就不建立訂票（GROUP-005）。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Examples
- 位置 19–23 跨車廂：409 CONSECUTIVE_SEATS_UNAVAILABLE
