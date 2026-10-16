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
  - resource: "docs/requirements/business-rules.md#L34-34"
    excerpt_sha256: "sha256:6865782809dcaa9aae551744101ce8d776ee518cc6512134ad02c1e44becdbdd"
  - resource: "src/smart_ticket/application/change_booking_service.py#L43-49"
    excerpt_sha256: "sha256:f8ab1f7072bf9309d08d6ccec652ab5f6d8eb7c21abf56f779bdc6ff6c7f3efd"
  - resource: "tests/integration/test_changes.py#L1-10"
    excerpt_sha256: "sha256:5efdd715f9dada3b7ea0919b2c2a57acaf0cb30645884458c38a4006797fc7b2"
---
改票只記錄票價差額（new - old），不執行補價或退款。

# Relations
- Contexts: [booking](/contexts/booking)

# Examples
- T001 700 改 T005 750：fare_difference 50，Order 仍 700
