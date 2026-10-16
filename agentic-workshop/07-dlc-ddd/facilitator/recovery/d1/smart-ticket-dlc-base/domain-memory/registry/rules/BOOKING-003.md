---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L13-13"
    excerpt_sha256: "sha256:773dd1daff8bda123494cbe7fd00986cd6061421c142fcd36b54b55ba8650760"
  - resource: "src/smart_ticket/application/booking_service.py#L34-35"
    excerpt_sha256: "sha256:2f93bfdde6ee157382f08479dc9c6b8be56f9a5cb2bd934f23f0081ed3ca4340"
  - resource: "tests/integration/test_features.py#L58-65"
    excerpt_sha256: "sha256:fefe3e49d387e20854a47ee6dc7363c4ee13ce426fabcce8136ec7ae8d0e2e9e"
---
旅客數不得超過班次剩餘座位數，失敗時不留下任何訂票或座位。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)
