---
type: Bounded Context
title: "計價 Pricing"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: core
confirmed_absences:
  - asset: aggregates
    reason: "計價是無狀態的政策（DiscountPolicy），只根據輸入計算結果，不持有需要一致性保護的狀態。"
sources:
  - resource: "docs/requirements/discount-overview.md#L3-3"
    excerpt_sha256: "sha256:fc5678df1c855e235ef5777cbb7204fccab27e7fccce5282e83a8688c78d77f1"
  - resource: "docs/adr/002-introduce-discount-policy.md#L18-18"
    excerpt_sha256: "sha256:89a5ec6bb5df3e3e6065d0fb5282e873dadefc3822bbd8b5725560671a0e04a4"
  - resource: "src/smart_ticket/domain/discounts.py#L20-35"
    excerpt_sha256: "sha256:81ecc217bf62dc9872316323df7a5f8c2b85d888231c300054f5c58b2dd17638"
---
逐位旅客評估所有優惠資格，採 rate 最低的單一優惠（不疊加），產生每位旅客的整數票價與 Applied Discount。
