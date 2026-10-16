---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L11-12"
    excerpt_sha256: "sha256:e0d17d37a1fc6b3ba280b3fb5185fee50ed9a3cfbccbca8dd948a7b9858c3973"
  - resource: "src/smart_ticket/application/booking_service.py#L32-33"
    excerpt_sha256: "sha256:748fb2236325d5badb82b9144adbb179c7ca94734ecebda0529d50b866b435c8"
  - resource: "tests/integration/test_features.py#L53-56"
    excerpt_sha256: "sha256:40c2ae60ae58677653827dc2c4a905a3003f18095e3111472cee8ffe78ce869e"
---
一般訂票單筆 1 至 4 位旅客；5 位以上要走團體訂票。

# Relations
- Contexts: [booking](/contexts/booking)

# Examples
- 5 位：409 INVALID_PASSENGER_COUNT
- 4 位：建立成功
