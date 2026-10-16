---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L87-87"
    excerpt_sha256: "sha256:2be66d1c4e383e49ae17d3aeaab671bd5cc1285c05e19aa3a876d238a54806e6"
  - resource: "docs/requirements/business-rules.md#L92-92"
    excerpt_sha256: "sha256:b9d724a37ebf154abfacdcb703773ec695e6f23c773e563a67f58cbb810fc262"
  - resource: "src/smart_ticket/infrastructure/einvoice_provider.py#L31-34"
    excerpt_sha256: "sha256:fef7ad676bd8025a26021209ddf044fc4ca6f72889076ed07bfd41dbbe4da35c"
  - resource: "src/smart_ticket/infrastructure/einvoice_provider.py#L6-6"
    excerpt_sha256: "sha256:27b4842512158252e945336da2d8a43cb1d90d400f9133e92e500363d9c4e35b"
  - resource: "tests/integration/test_e_invoice.py#L148-156"
    excerpt_sha256: "sha256:ced6b4437d2ed72f235d3052c50e5a9e8eb077fcc9d133692ff8b83b813bb6f9"
  - resource: "tests/integration/test_e_invoice.py#L214-219"
    excerpt_sha256: "sha256:a240ebe8647bfae1c6df4c5d2e70a4be096a68f0f4ec7f9bf842647a12242d51"
---
一筆 Order 至多一張已開立發票：以 order_id 作為服務商的商家訂單編號，第一次開立、逾時後重試都用同一編號；服務商回覆已開立（2001）視為成功並沿用原號碼（EINV-010）。

# Relations
- Contexts: [invoicing](/contexts/invoicing)
