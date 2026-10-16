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
  - resource: "docs/requirements/business-rules.md#L20-22"
    excerpt_sha256: "sha256:e701fa8bd3e6b5b0f9f523eab96a9d90dca18f89f412a8d1bcef4d0a0ae36c67"
  - resource: "src/smart_ticket/application/payment_service.py#L23-24"
    excerpt_sha256: "sha256:9281061c4a1b574e8bba100456dd0bea317d35b00f0b5626b8c827db82544b04"
  - resource: "tests/integration/test_features.py#L90-94"
    excerpt_sha256: "sha256:b104171b98af388ed2f1538926b2988f12155b5bf136c4fba86e5806ed7a9eef"
---
只有 PENDING_PAYMENT 的訂票可以付款；同一訂票不得重複付款（PAYMENT-003）。

# Relations
- Contexts: [payment](/contexts/payment)
- Contexts: [booking](/contexts/booking)
