---
type: Bounded Context
title: "付款 Payment"
status: stable
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: supporting
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L20-24"
    excerpt_sha256: "sha256:00607467ff05dd112e44eb9cd6ef487b489abe8bbe57a303d7204785ad1a16d3"
  - resource: "docs/requirements/business-rules.md#L66-70"
    excerpt_sha256: "sha256:e6e702c86865526cfdfbb5500bd668f987b070477b3875d7562d58dcd5e632da"
  - resource: "src/smart_ticket/application/payment_service.py#L18-41"
    excerpt_sha256: "sha256:c606635e9245ba8f23aa6046cd3458ab9d66539e88b51f24101f17a230297b63"
---
向付款閘道扣款；成功時建立唯一 Order 作為付款當時的金額快照，團體付款失敗時執行補償。
