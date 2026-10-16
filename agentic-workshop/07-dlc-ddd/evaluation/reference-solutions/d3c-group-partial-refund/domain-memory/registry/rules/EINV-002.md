---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L84-84"
    excerpt_sha256: "sha256:b940613e1612c2d73b664ca7500fb0736ab569065e835f7cc8bceea0b8d5ad1c"
  - resource: "src/smart_ticket/application/payment_service.py#L22-27"
    excerpt_sha256: "sha256:b4cdd687efbb15a72e907b294b0ebfbef9da2176bfc95430de4e6c0eb085bd66"
  - resource: "src/smart_ticket/application/invoicing_service.py#L26-39"
    excerpt_sha256: "sha256:5eb131d82aab9bfb39ca227cfb97c54213667153d87682f6c71e42a0c85885cb"
  - resource: "tests/integration/test_e_invoice.py#L77-94"
    excerpt_sha256: "sha256:f1f516dde062f65116b379605b864624a277f49d68950c52310061574ba5908f"
  - resource: "tests/integration/test_e_invoice.py#L116-121"
    excerpt_sha256: "sha256:770396632d21140a086a623b419b39a2c8a37db382375f6e1d013aa6f97ffbaf"
---
發票開立的任何結果都不影響付款：Order 與 PAID 先在付款鎖內成立，釋放全域鎖後才呼叫服務商（一般與團體路徑皆然），失敗只改 Invoice 狀態，付款 API 照樣成功、Order 金額不變。

# Relations
- Contexts: [invoicing](/contexts/invoicing)
- Contexts: [payment](/contexts/payment)
