---
type: Term
title: "團體訂票"
status: draft
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L59-62"
    excerpt_sha256: "sha256:e5ff7c45ca994a8d577477a62b74eede557d013ffe6f2301525180e39827015b"
  - resource: "src/smart_ticket/application/group_booking_service.py#L25-26"
    excerpt_sha256: "sha256:966cc373e31df909392de38d74bc590dda17190db5d0468d3e1ea9e2c0210a27"
  - resource: "src/smart_ticket/domain/models.py#L54-54"
    excerpt_sha256: "sha256:626b195cb6e99431e18a55b510cadef882ede9d116b8f8ef797cc7ef29bb3f7e"
---
5–20 位旅客搭乘同一班次、配置同車廂連續座位的訂票；以 booking_type 字串 "GROUP" 區分，沒有獨立型別。

# Relations
- Not same as: [booking](/vocabulary/booking)
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- Group Booking
- GROUP
- booking_type
