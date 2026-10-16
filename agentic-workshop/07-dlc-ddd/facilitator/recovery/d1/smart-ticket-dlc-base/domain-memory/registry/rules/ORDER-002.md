---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L24-24"
    excerpt_sha256: "sha256:15d857afef33219d6e091009674cfffc04d7450cf59b27d1ac9938038e947901"
  - resource: "src/smart_ticket/application/payment_service.py#L35-35"
    excerpt_sha256: "sha256:20557359ecc59ab85d40a0a116ed405d1d80e2b726eafaf393a8f4e693eb4b7c"
  - resource: "tests/integration/test_best_discount_api.py#L38-56"
    excerpt_sha256: "sha256:befa63bd2224aa5f3851812eee88d4ff929c5ace369e23d2af9eb304683ee40c"
---
Order 建立時 amount 等於付款當時的訂票總票價；改票後 Order 保留原付款快照，不執行差額金流。

# Relations
- Contexts: [payment](/contexts/payment)
- Contexts: [booking](/contexts/booking)
