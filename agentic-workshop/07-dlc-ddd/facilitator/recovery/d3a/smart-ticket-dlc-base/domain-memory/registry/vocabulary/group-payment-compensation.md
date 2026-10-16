---
type: Term
title: "團體付款失敗補償"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L67-69"
    excerpt_sha256: "sha256:92390da918c7cab69c51fa1feb8d36736c9e6603b6536a18c88f44f788b7ab03"
  - resource: "docs/adr/004-group-seat-atomicity.md#L10-10"
    excerpt_sha256: "sha256:21a97a6b2b9622339882afb743c8c3d525af18be24f2b36f615b1dba36700638"
  - resource: "src/smart_ticket/application/payment_service.py#L26-34"
    excerpt_sha256: "sha256:24dded47e154bec4bb19496fcf9b80671569b6e591e3aabbaba0602434a2f3b6"
---
團體付款失敗時的整套處置：訂票轉 CANCELLED、釋放全部座位、不建立 Order、留下 Audit 與取消通知。文件稱補償，程式沒有對應名稱，只是 PaymentService.pay 內的一個分支。

# Relations
- Contexts: [payment](/contexts/payment)
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- Compensation
- 補償
