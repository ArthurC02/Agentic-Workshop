---
type: Term
title: "團體訂票"
status: stable
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L59-62"
    excerpt_sha256: "sha256:e5ff7c45ca994a8d577477a62b74eede557d013ffe6f2301525180e39827015b"
  - resource: "src/smart_ticket/application/group_booking_service.py#L25-26"
    excerpt_sha256: "sha256:07e876b08bc12bd077ef7509bb20e65f776d1c6a6f8029f657ac8cd7df9f2ada"
  - resource: "src/smart_ticket/domain/models.py#L54-54"
    excerpt_sha256: "sha256:88a8d525126ec50aced4cfebbc34973fb6263344290c4272443aa1533299d607"
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
