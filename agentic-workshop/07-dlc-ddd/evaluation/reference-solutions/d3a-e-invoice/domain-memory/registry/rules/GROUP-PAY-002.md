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
  - resource: "docs/requirements/business-rules.md#L67-69"
    excerpt_sha256: "sha256:92390da918c7cab69c51fa1feb8d36736c9e6603b6536a18c88f44f788b7ab03"
  - resource: "src/smart_ticket/application/payment_service.py#L26-34"
    excerpt_sha256: "sha256:24dded47e154bec4bb19496fcf9b80671569b6e591e3aabbaba0602434a2f3b6"
  - resource: "tests/integration/test_group_payment.py#L21-32"
    excerpt_sha256: "sha256:0c23ab49ad1168d6128d97d381b7cbc4489eaf9120c36c6f1439c1a6ccebf95e"
---
團體付款失敗時訂票轉 CANCELLED、釋放全部團體座位且不建立 Order（GROUP-PAY-002 至 004）。

# Relations
- Contexts: [payment](/contexts/payment)
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)
