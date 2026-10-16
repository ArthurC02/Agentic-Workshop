---
type: Bounded Context
title: "付款 Payment"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: supporting
sources:
  - resource: "docs/requirements/business-rules.md#L20-24"
    excerpt_sha256: "sha256:00607467ff05dd112e44eb9cd6ef487b489abe8bbe57a303d7204785ad1a16d3"
  - resource: "docs/requirements/business-rules.md#L66-70"
    excerpt_sha256: "sha256:e6e702c86865526cfdfbb5500bd668f987b070477b3875d7562d58dcd5e632da"
  - resource: "src/smart_ticket/application/payment_service.py#L18-41"
    excerpt_sha256: "sha256:c04783891cd3791d82c80613182ee0a086ad1b25a66d8bf2d1dda57046bb17f2"
---
向付款閘道扣款；成功時建立唯一 Order 作為付款當時的金額快照，團體付款失敗時執行補償。
