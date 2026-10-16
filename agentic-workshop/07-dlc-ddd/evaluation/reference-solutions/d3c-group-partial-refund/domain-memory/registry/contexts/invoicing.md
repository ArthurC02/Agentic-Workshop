---
type: Bounded Context
title: "電子發票 Invoicing"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: supporting
sources:
  - resource: "docs/adr/005-issue-e-invoices-through-a-port.md#L14-15"
    excerpt_sha256: "sha256:99cd932696ce96ce6d8528e2738759e9077e62bc40f2b14f135b4ddcecce6311"
  - resource: "src/smart_ticket/domain/invoicing.py#L1-5"
    excerpt_sha256: "sha256:ed0b9954adf46be38263af421d06de745cfa95016d5292c9223f0876e09d7e5f"
---
為每筆付款成功的 Order 開立一張電子發票：持有 Invoice（以 order_id 識別）、購票人發票資訊、稅額拆分、品項、重試上限與狀態機；只經 Port InvoiceIssuer 與外部發票服務商溝通，發票失敗不回滾付款。
