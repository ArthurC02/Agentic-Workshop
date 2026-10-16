---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L35-38"
    excerpt_sha256: "sha256:e94f9078ca55a3df93f04cd0a70b391c3b21ec8c6922503c29baafbbec40456c"
  - resource: "src/smart_ticket/application/refund_service.py#L22-29"
    excerpt_sha256: "sha256:9a8e3026e2da7c72675f40b5c6c42bd619abcda7829a17e6d9decc0794b92865"
  - resource: "tests/integration/test_refunds.py#L4-17"
    excerpt_sha256: "sha256:dddaee8b1e0176d41d96afdfb67468d418a19aba84cd3e0c90a63565a9c953fe"
---
只有已付款訂票可退票，退票建立唯一退款紀錄並釋放座位；同一訂票不可再退。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)
