---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L89-91"
    excerpt_sha256: "sha256:65237a239071e8917703960991a2cc1303e9003641f53ef49c341ecaa7cd1279"
  - resource: "src/smart_ticket/domain/invoicing.py#L119-130"
    excerpt_sha256: "sha256:21f2715cd841b8f6faa3ce34766f746754d12b7d9538317096d9e932c8114f20"
  - resource: "tests/integration/test_e_invoice.py#L191-211"
    excerpt_sha256: "sha256:9cee2602b524a3c1421b19d79d3b7cb8aaabc2d86bd734de98838847f4770fdd"
---
暫時失敗（忙碌、逾時、連線失敗）維持 PENDING 並可重試；累計呼叫 5 次（含第一次）仍未成功轉 FAILED，永久失敗（1001／1002）第一次就轉 FAILED；FAILED 之後不再呼叫服務商（EINV-007／008／009）。

# Relations
- Contexts: [invoicing](/contexts/invoicing)
