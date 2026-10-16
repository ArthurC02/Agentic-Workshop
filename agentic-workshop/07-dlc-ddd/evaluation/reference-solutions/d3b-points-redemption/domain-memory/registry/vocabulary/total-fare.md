---
type: Term
title: "訂票總票價"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L18-19"
    excerpt_sha256: "sha256:d96485f0ad72afd6f80f201c8958744c5f571a758d350f503de5c18f4b8b2992"
  - resource: "docs/requirements/business-rules.md#L72-72"
    excerpt_sha256: "sha256:d0bd0888aec7d2d8574e2bd1f7937e81829c58f271bb51b6489a399298376994"
  - resource: "src/smart_ticket/application/booking_service.py#L40-40"
    excerpt_sha256: "sha256:60b3d63cdf05da3538c01cc868d047043a53fee4c591e9ef8b8d333ecbbd13d6"
---
每位旅客個別計價後的整數金額加總；團體同樣是個別票價加總。

# Relations
- Contexts: [pricing](/contexts/pricing)
- Contexts: [booking](/contexts/booking)

# Synonyms
- Total Fare
- total_fare
