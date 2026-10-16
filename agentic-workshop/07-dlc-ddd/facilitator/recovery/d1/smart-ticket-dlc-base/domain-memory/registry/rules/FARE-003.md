---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L18-18"
    excerpt_sha256: "sha256:81ffe065ca270936c9856dbbf291c42104514e49a706e76a36eac3441c254875"
  - resource: "src/smart_ticket/application/booking_service.py#L37-40"
    excerpt_sha256: "sha256:64f5bd5558ac439b9868e9615fb51c7e3a8363c286ed886ed3da6958e6395d4e"
  - resource: "tests/integration/test_best_discount_api.py#L14-25"
    excerpt_sha256: "sha256:bc9f618bf55561885e9076edd8c7ef29a9a9d65e56677152f661a749d56c2797"
---
每位旅客個別計價，個別整數金額加總為訂票總票價。

# Relations
- Contexts: [pricing](/contexts/pricing)
- Contexts: [booking](/contexts/booking)

# Examples
- 成人提前 595 + 學生 525 = 1120
