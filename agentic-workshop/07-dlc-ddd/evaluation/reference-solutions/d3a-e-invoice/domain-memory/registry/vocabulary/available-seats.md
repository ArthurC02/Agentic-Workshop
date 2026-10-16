---
type: Term
title: "剩餘座位數"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L13-13"
    excerpt_sha256: "sha256:773dd1daff8bda123494cbe7fd00986cd6061421c142fcd36b54b55ba8650760"
  - resource: "src/smart_ticket/domain/models.py#L28-28"
    excerpt_sha256: "sha256:70fe431755f712dd8c24770a1139f01b7ae3e69f87c9a9f059f5194650948e49"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:6db7bed85eefb641565312e70064a992e416e0c1b0394b62f89782b3b838cc41"
  - resource: "src/smart_ticket/infrastructure/store.py#L27-27"
    excerpt_sha256: "sha256:b820570459bdae3e73657fd1167a07f30d4cbef0382cddeb01994c81c147ec53"
---
班次目前還能賣的座位數；訂票保留時減少、釋放時增加。程式中同時存在計數器、座位指派表與容量表三份資料。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- available_seats
- 可售座位
