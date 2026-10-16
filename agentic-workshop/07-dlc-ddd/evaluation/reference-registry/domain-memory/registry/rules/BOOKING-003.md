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
  - resource: "docs/requirements/business-rules.md#L13-13"
    excerpt_sha256: "sha256:773dd1daff8bda123494cbe7fd00986cd6061421c142fcd36b54b55ba8650760"
  - resource: "src/smart_ticket/application/booking_service.py#L34-35"
    excerpt_sha256: "sha256:60164a1014aae5312421998623953ca7c46f922eb0ad23a49a17d7656039d18e"
  - resource: "tests/integration/test_features.py#L58-65"
    excerpt_sha256: "sha256:fefe3e49d387e20854a47ee6dc7363c4ee13ce426fabcce8136ec7ae8d0e2e9e"
---
旅客數不得超過班次剩餘座位數，失敗時不留下任何訂票或座位。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)
