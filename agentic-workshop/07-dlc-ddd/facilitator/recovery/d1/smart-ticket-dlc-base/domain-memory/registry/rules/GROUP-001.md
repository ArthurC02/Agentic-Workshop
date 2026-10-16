---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L59-60"
    excerpt_sha256: "sha256:08acbdabeef0904d355530b12a89cfcf6fdef3c081bca6c644c53c974c16fd6b"
  - resource: "src/smart_ticket/application/group_booking_service.py#L25-26"
    excerpt_sha256: "sha256:966cc373e31df909392de38d74bc590dda17190db5d0468d3e1ea9e2c0210a27"
  - resource: "tests/integration/test_group_creation.py#L5-23"
    excerpt_sha256: "sha256:0ff318082f6bc19213eea336526072b08fe39c9f398f01986d07a0f5ebf1765d"
---
團體訂票旅客數為 5 至 20 人（GROUP-001 最少 5、GROUP-002 最多 20）。

# Relations
- Contexts: [booking](/contexts/booking)

# Examples
- 4 人：409
- 5 人、20 人：201
- 21 人：409
