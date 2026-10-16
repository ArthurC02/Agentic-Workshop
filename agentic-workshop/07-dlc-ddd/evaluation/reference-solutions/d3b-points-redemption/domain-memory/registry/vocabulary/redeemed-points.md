---
type: Term
title: "折抵點數"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L106-110"
    excerpt_sha256: "sha256:9d829be3a2166c08481ef4d65a1d011b61fcd9861d8161461cbf87442384eae0"
  - resource: "src/smart_ticket/domain/members.py#L5-10"
    excerpt_sha256: "sha256:d0a1f40361c994b9c8017897f759115b0b20a8a6e35e451aab5054d7066c3962"
  - resource: "src/smart_ticket/domain/models.py#L57-57"
    excerpt_sha256: "sha256:6467c574008d5c655544e82a90a031d692beacd3764be87824b54261c8a63af7"
---
訂票建立時以會員點數折抵票款的點數（1 點 = 1 元）：至少 100 點、為 100 的倍數、價值不超過優惠後總額 30%（向下取整）；建立成功即從餘額預留（扣除），記在 Booking 上作為歸還依據。折抵不是優惠。

# Relations
- Contexts: [membership](/contexts/membership)
- Contexts: [booking](/contexts/booking)

# Synonyms
- redeemed_points
- Points Redemption
