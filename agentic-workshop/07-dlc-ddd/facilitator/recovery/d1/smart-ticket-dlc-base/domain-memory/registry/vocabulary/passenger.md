---
type: Term
title: "旅客"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L48-48"
    excerpt_sha256: "sha256:5b57403b736c195257536a63ff55df84be6bed39563ff72bc23d1605e0cc9155"
  - resource: "src/smart_ticket/domain/models.py#L6-8"
    excerpt_sha256: "sha256:29eb0ea851eb4e39f36fe2784cc20780fd3d4c644815f686e57f0c9801349b7c"
  - resource: "src/smart_ticket/domain/models.py#L30-34"
    excerpt_sha256: "sha256:45a073abeb379f70bc2dd64c9d733d17d00a3fc83cb1e83643b34faba1d211bf"
---
訂票中的一位乘客，帶 passenger_id、姓名與旅客類型（ADULT 或 STUDENT）；每位旅客獨立決定優惠。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Passenger
- PassengerType
- ADULT
- STUDENT
