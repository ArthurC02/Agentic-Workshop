---
type: Decision
status: stable
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/seat_service.py
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/domain/models.py#L28-28"
    excerpt_sha256: "sha256:70fe431755f712dd8c24770a1139f01b7ae3e69f87c9a9f059f5194650948e49"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:6db7bed85eefb641565312e70064a992e416e0c1b0394b62f89782b3b838cc41"
  - resource: "src/smart_ticket/infrastructure/store.py#L23-27"
    excerpt_sha256: "sha256:4e7390c84209ccafecf99baed2e681ad51115cc1399bcf821ccbdfbfa3e0931b"
---
現況觀察（非已核准決策）：座位庫存有三份資料——Trip.available_seats 計數器、seat_assignments、seat_capacity——沒有單一擁有者守住一致性，只靠服務層同步與全域 RLock。改動座位的變更必須同時處理三者。
