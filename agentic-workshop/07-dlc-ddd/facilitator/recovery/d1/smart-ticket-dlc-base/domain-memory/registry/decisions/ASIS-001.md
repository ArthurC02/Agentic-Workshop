---
type: Decision
status: draft
decision_status: observed-design-leak
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/seat_service.py
sources:
  - resource: "src/smart_ticket/domain/models.py#L28-28"
    excerpt_sha256: "sha256:a999176184982e57afaa8bd5a0b3271dda3023f2a204cb7fa49fb3ef3aba3929"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:59ade4ffa49a5c4da896eff0fed2578f3775219b5bfcd5513b321fd35e4d8efe"
  - resource: "src/smart_ticket/infrastructure/store.py#L23-27"
    excerpt_sha256: "sha256:4e7390c84209ccafecf99baed2e681ad51115cc1399bcf821ccbdfbfa3e0931b"
---
現況觀察（非已核准決策）：座位庫存有三份資料——Trip.available_seats 計數器、seat_assignments、seat_capacity——沒有單一擁有者守住一致性，只靠服務層同步與全域 RLock。改動座位的變更必須同時處理三者。
