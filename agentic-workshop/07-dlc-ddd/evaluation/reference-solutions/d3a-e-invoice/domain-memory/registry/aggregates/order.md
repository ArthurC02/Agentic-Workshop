---
type: Aggregate
status: stable
entities: []
value_objects: []
domain_services: []
policies: []
allowed_dependencies: []
prohibited_dependencies: []
root: Order
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/domain/models.py#L57-62"
    excerpt_sha256: "sha256:67a736b874d8eac9a3da2dc7293d573c2fd22ca3771856425bfb0465300a2840"
  - resource: "docs/requirements/business-rules.md#L23-24"
    excerpt_sha256: "sha256:695856482638ebd79238c851e25f8897dfcd12ec5ae88fdf1f6c69081ed94c07"
  - resource: "src/smart_ticket/application/payment_service.py#L35-36"
    excerpt_sha256: "sha256:f6e3e5ddd73e5d39a2383fab2c4a1480977ee6fb84eb3b1eb576f3edea986a02"
---
# Relations
- Context: [payment](/contexts/payment)

# Commands
- pay

# Invariants
- 一筆付款成功只建立一筆 Order
- amount 為付款當時的訂票總票價，建立後不因改票而改變
