---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L46-47"
    excerpt_sha256: "sha256:0124050434f167fba7b1618dd14b1db328ad2c27a92f1c9dce63b25c1b55f9e2"
  - resource: "docs/requirements/discount-overview.md#L5-5"
    excerpt_sha256: "sha256:1db0f853587bae8c022bc3b91a2d92ecc4d43f873b25d7cf57d75e6c40c9439d"
  - resource: "src/smart_ticket/domain/discounts.py#L34-35"
    excerpt_sha256: "sha256:89c6543da87b8bece69aed4df28652edd74fe9ed0496a745a12cf8dea1934d26"
  - resource: "tests/unit/test_best_discount_policy.py#L9-25"
    excerpt_sha256: "sha256:34e62a07435a82fbe6350137ca00df9ff5d8cfb889d9395dc3a526b973b3d6de"
---
同時符合多項優惠時只採 rate 最低的單一優惠，多項優惠不疊加（FARE-007）。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Examples
- 學生加提前：75
- 企業加提前：85
- 學生、企業、提前同時符合：75
