---
type: Term
title: "旅客"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L48-48"
    excerpt_sha256: "sha256:5b57403b736c195257536a63ff55df84be6bed39563ff72bc23d1605e0cc9155"
  - resource: "src/smart_ticket/domain/models.py#L6-8"
    excerpt_sha256: "sha256:f5b24aff9d835654d9d20062200d27e99a9fe6f7197d3445e8e9c54c93fcf0ed"
  - resource: "src/smart_ticket/domain/models.py#L30-34"
    excerpt_sha256: "sha256:a27a5c4ef9283e5f5ffcea03ca4159cfa55dad6262931c17ffeabf39ebbdefa2"
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
