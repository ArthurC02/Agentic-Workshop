---
type: Interaction
status: stable
consistency: synchronous
delivery: "同一把 store RLock 內呼叫 SeatService.plan／reserve／release"
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/application/booking_service.py#L47-50"
    excerpt_sha256: "sha256:c3064259d015cc3e6864dc9d3c0f49e24ed69d9a6f53a5e1e1f1b87a56de9db6"
  - resource: "src/smart_ticket/application/seat_service.py#L20-27"
    excerpt_sha256: "sha256:6db7bed85eefb641565312e70064a992e416e0c1b0394b62f89782b3b838cc41"
  - resource: "docs/adr/001-use-in-memory-repositories.md#L10-10"
    excerpt_sha256: "sha256:724cfcb099da6caa5e27e1cbde51828e3f95a7e9b1ff229032d7bc30d693790d"
---
# Relations
- Producer context: [inventory](/contexts/inventory)
- Consumer context: [booking](/contexts/booking)
