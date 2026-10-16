---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L27-27"
    excerpt_sha256: "sha256:bd508437b67a7f6e2c2006663d0ba265a0763c7f68e597306310f77974d1d95e"
  - resource: "src/smart_ticket/domain/discounts.py#L32-33"
    excerpt_sha256: "sha256:67eff644f630d233a69dae193ed3a268cf2b0faf36f14ace1bea7429d0acab95"
  - resource: "tests/integration/test_members.py#L10-12"
    excerpt_sha256: "sha256:1336e65317f1317a11247e722b5f89b5120334af8c47d3487aa0d088fe78a364"
---
綁定 CORPORATE 會員的訂票，旅客具備 95% 企業優惠資格。

# Relations
- Contexts: [membership](/contexts/membership)
- Contexts: [pricing](/contexts/pricing)

# Examples
- M002 成人無提前：665
