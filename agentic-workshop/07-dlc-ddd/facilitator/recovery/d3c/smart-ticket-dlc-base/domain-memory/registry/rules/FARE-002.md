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
  - resource: "docs/requirements/business-rules.md#L17-17"
    excerpt_sha256: "sha256:5053fd35676ab3c319a54a13f535b951134e7e38bb5591caf3d1e706c0da86c8"
  - resource: "src/smart_ticket/domain/discounts.py#L28-29"
    excerpt_sha256: "sha256:159904de6ab72ab01cc76e078fe4222b62ef50e7f5af8153d4263b311526fabe"
  - resource: "tests/unit/test_best_discount_policy.py#L9-25"
    excerpt_sha256: "sha256:34e62a07435a82fbe6350137ca00df9ff5d8cfb889d9395dc3a526b973b3d6de"
---
學生旅客具備基本票價 75% 的資格，實際結果仍由最有利單一優惠決定。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Examples
- 基本票價 700 的學生，無其他資格：525
