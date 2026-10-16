---
type: Term
title: "票價差額"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L34-34"
    excerpt_sha256: "sha256:6865782809dcaa9aae551744101ce8d776ee518cc6512134ad02c1e44becdbdd"
  - resource: "docs/requirements/change-booking-guide.md#L3-3"
    excerpt_sha256: "sha256:de0039e192166979de1622f2f309bcb0a762c71041d738e2120ef1f176f25b80"
  - resource: "src/smart_ticket/application/change_booking_service.py#L43-49"
    excerpt_sha256: "sha256:109531ebcc39c635e483861acf6267eb8ca4d1ab86864e4b83757a31e7e6a18b"
---
改票時新票價減原票價（new - old）；只記錄在 Booking 上，不執行補款或退款，Order 金額不變。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Fare Difference
- fare_difference
