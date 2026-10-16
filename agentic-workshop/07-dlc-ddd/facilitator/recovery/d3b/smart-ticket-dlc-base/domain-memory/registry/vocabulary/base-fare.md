---
type: Term
title: "基本票價"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L16-16"
    excerpt_sha256: "sha256:27004ea6e03617fe9c9d75958d529792fc79dc64cce81fb2a4dd28f498ff89f5"
  - resource: "src/smart_ticket/domain/models.py#L27-27"
    excerpt_sha256: "sha256:d946aadb4e46c26dffe0954cd15053c8dff834d49902fbc2f65d0759c30a87f7"
---
班次的標準全額票價（整數）；成人無其他優惠時就付基本票價（rate 100）。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Base Fare
- base_fare
