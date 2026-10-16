---
type: Interaction
status: draft
consistency: synchronous
delivery: "同一把 store RLock 內呼叫 SeatService.plan／reserve／release"
sources:
  - resource: "src/smart_ticket/application/booking_service.py#L47-50"
    excerpt_sha256: "sha256:ba6a5b00684a09b18e5f1b3fef032a5f5f3e98a9dc8e963540759a8940c700d2"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:59ade4ffa49a5c4da896eff0fed2578f3775219b5bfcd5513b321fd35e4d8efe"
  - resource: "docs/adr/001-use-in-memory-repositories.md#L10-10"
    excerpt_sha256: "sha256:724cfcb099da6caa5e27e1cbde51828e3f95a7e9b1ff229032d7bc30d693790d"
---
# Relations
- Producer context: [inventory](/contexts/inventory)
- Consumer context: [booking](/contexts/booking)
