---
type: Term
title: "剩餘座位數"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L13-13"
    excerpt_sha256: "sha256:773dd1daff8bda123494cbe7fd00986cd6061421c142fcd36b54b55ba8650760"
  - resource: "src/smart_ticket/domain/models.py#L28-28"
    excerpt_sha256: "sha256:a999176184982e57afaa8bd5a0b3271dda3023f2a204cb7fa49fb3ef3aba3929"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:59ade4ffa49a5c4da896eff0fed2578f3775219b5bfcd5513b321fd35e4d8efe"
  - resource: "src/smart_ticket/infrastructure/store.py#L27-27"
    excerpt_sha256: "sha256:b820570459bdae3e73657fd1167a07f30d4cbef0382cddeb01994c81c147ec53"
---
班次目前還能賣的座位數；訂票保留時減少、釋放時增加。程式中同時存在計數器、座位指派表與容量表三份資料。

# Relations
- Contexts: [inventory](/contexts/inventory)

# Synonyms
- available_seats
- 可售座位
