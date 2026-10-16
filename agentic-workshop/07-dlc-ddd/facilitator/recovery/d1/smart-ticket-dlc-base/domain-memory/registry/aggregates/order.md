---
type: Aggregate
status: draft
entities: []
value_objects: []
domain_services: []
policies: []
allowed_dependencies: []
prohibited_dependencies: []
root: Order
sources:
  - resource: "src/smart_ticket/domain/models.py#L57-62"
    excerpt_sha256: "sha256:be479dae1b5f8b1022f80c5d06fcbf87eb8d5e79e2b1bb075615d67f96b2bce7"
  - resource: "docs/requirements/business-rules.md#L23-24"
    excerpt_sha256: "sha256:695856482638ebd79238c851e25f8897dfcd12ec5ae88fdf1f6c69081ed94c07"
  - resource: "src/smart_ticket/application/payment_service.py#L35-36"
    excerpt_sha256: "sha256:754f53692ac1825e87ad61e74efd75d7d99b457cb6dbf46b252b53f99545a89a"
---
# Relations
- Context: [payment](/contexts/payment)

# Commands
- pay

# Invariants
- 一筆付款成功只建立一筆 Order
- amount 為付款當時的訂票總票價，建立後不因改票而改變
