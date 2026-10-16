---
type: Term
title: "訂票總票價"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L18-19"
    excerpt_sha256: "sha256:d96485f0ad72afd6f80f201c8958744c5f571a758d350f503de5c18f4b8b2992"
  - resource: "docs/requirements/business-rules.md#L72-72"
    excerpt_sha256: "sha256:d0bd0888aec7d2d8574e2bd1f7937e81829c58f271bb51b6489a399298376994"
  - resource: "src/smart_ticket/application/booking_service.py#L40-40"
    excerpt_sha256: "sha256:f2ca0aa9e3f74beb5d2d48d882b84fa4d1488127f34c342b13ee57a200bc4872"
---
每位旅客個別計價後的整數金額加總；團體同樣是個別票價加總。

# Relations
- Contexts: [pricing](/contexts/pricing)
- Contexts: [booking](/contexts/booking)

# Synonyms
- Total Fare
- total_fare
