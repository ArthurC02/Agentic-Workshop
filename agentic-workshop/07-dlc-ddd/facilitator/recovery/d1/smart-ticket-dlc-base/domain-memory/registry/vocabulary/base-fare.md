---
type: Term
title: "基本票價"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L16-16"
    excerpt_sha256: "sha256:27004ea6e03617fe9c9d75958d529792fc79dc64cce81fb2a4dd28f498ff89f5"
  - resource: "src/smart_ticket/domain/models.py#L27-27"
    excerpt_sha256: "sha256:02c5a5f888de69d6ba7761c2bbcab3c40973eee999f00f057a9fa1f75eea3893"
---
班次的標準全額票價（整數）；成人無其他優惠時就付基本票價（rate 100）。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Base Fare
- base_fare
