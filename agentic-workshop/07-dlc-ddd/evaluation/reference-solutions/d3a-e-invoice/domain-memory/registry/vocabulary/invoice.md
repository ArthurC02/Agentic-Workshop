---
type: Term
title: "電子發票"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L88-88"
    excerpt_sha256: "sha256:f8ec8b3d3984c02e4b58191e7287d27b23b44a98c59426ee30e6f27916f7dfa6"
  - resource: "src/smart_ticket/domain/invoicing.py#L106-113"
    excerpt_sha256: "sha256:0836337a9babac934777cbddef84269e82ea5d7c563494ff058b613b5e1be9a5"
---
為一筆 Order 開立的電子發票，以 order_id 識別、總額等於 Order.amount；狀態 PENDING（可重試）、ISSUED（含不可變更的發票號碼）、FAILED（永久失敗或達呼叫上限，需人工處理）。

# Relations
- Contexts: [invoicing](/contexts/invoicing)

# Synonyms
- Invoice
- e-invoice
