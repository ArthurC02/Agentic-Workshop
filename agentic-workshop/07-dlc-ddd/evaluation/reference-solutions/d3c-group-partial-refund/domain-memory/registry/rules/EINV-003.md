---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L85-85"
    excerpt_sha256: "sha256:5267aced6e21a1f46442507980c961b1afa2cfa162a1f241e1381524cc92d43c"
  - resource: "src/smart_ticket/domain/invoicing.py#L21-27"
    excerpt_sha256: "sha256:5864027378c397995ac707f3071f28fd4a93feef333163e5d883a962f0ff59da"
  - resource: "tests/integration/test_e_invoice.py#L124-134"
    excerpt_sha256: "sha256:683655885a9c2a0b959d32bcb4a92d3b7cb81bdd6c9f8930329051ff465046a1"
---
發票總額等於 Order.amount；銷售額 = 總額 ÷ 1.05 四捨五入、稅額 = 總額 − 銷售額，全部以整數計算。

# Relations
- Contexts: [invoicing](/contexts/invoicing)

# Examples
- 700 → 銷售額 667、稅額 33
- 3,500 → 3,333／167
- 665 → 633／32
