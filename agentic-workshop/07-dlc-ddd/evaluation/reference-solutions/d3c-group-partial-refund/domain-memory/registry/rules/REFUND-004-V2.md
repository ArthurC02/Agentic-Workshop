---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
examples: []
sources:
  - resource: "docs/requirements/business-rules.md#L38-38"
    excerpt_sha256: "sha256:d6fdd4374f621f3c3c1bb6bcfaa5011564b0d791ae559870c836e2a20181ad47"
  - resource: "docs/requirements/business-rules.md#L141-141"
    excerpt_sha256: "sha256:bf19027240cae71959c1295c926de94b7411dd69f515428f2e51f01635f41669"
  - resource: "src/smart_ticket/domain/models.py#L106-109"
    excerpt_sha256: "sha256:de1710515078dd7a805706c8afca04acfb001949d0cf0adf4adb71e9a8e05978"
  - resource: "src/smart_ticket/infrastructure/store.py#L25-25"
    excerpt_sha256: "sha256:0c5ed671c3d2c982e099ca43b84625c5a5955f193054e92a24f16a9160c498d6"
  - resource: "tests/integration/test_partial_cancellation.py#L179-187"
    excerpt_sha256: "sha256:4efb76ed680fb9b491ceaad62e6d1a85ac8c65c1e61ac9e75a5f92d3a621dcaf"
  - resource: "tests/integration/test_partial_cancellation.py#L246-255"
    excerpt_sha256: "sha256:9e3638c0c237a8d39c12bd91c369bb0b7a1c87f0fc726b473e292c8e1f9392ee"
---
每次退款建立一筆新的退款紀錄（append-only，既有紀錄不被覆寫）：整筆退票一筆、團體部分取消每次一筆；整筆退票只能一次，且只限從未部分取消過的訂票（PCR-007、PCR-012）。取代 reviewed REFUND-004 的「同一訂票不可再退」。

# Relations
- Contexts: [booking](/contexts/booking)
- Contexts: [inventory](/contexts/inventory)
