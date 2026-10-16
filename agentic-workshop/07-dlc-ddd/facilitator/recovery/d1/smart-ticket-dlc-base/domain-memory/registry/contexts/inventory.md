---
type: Bounded Context
title: "座位庫存 Inventory"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: supporting
sources:
  - resource: "docs/requirements/business-rules.md#L42-43"
    excerpt_sha256: "sha256:e87da0d0ff624c96c28da423857890cf782ee6b83d8a33c64e80802c743c036f"
  - resource: "docs/requirements/business-rules.md#L62-62"
    excerpt_sha256: "sha256:19c1ea0de4babefb0a4f59b3153fcda4672af15284ed83cfefb2e60844426b43"
  - resource: "docs/adr/004-group-seat-atomicity.md#L10-10"
    excerpt_sha256: "sha256:21a97a6b2b9622339882afb743c8c3d525af18be24f2b36f615b1dba36700638"
  - resource: "src/smart_ticket/application/seat_service.py#L10-27"
    excerpt_sha256: "sha256:9d43de136361830756aa6b7f4b27f4da833f3a8ca41435b7b0fb39552ec37d02"
---
依班次容量配置與釋放座位：同班次座位不重複，團體需同車廂連續座位，訂票建立即保留、退票與團體付款失敗時釋放。
