---
type: Term
title: "折扣率"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:maintainer@example.com"
    at: "2026-10-14T16:51:15.653837Z"
sources:
  - resource: "docs/requirements/business-rules.md#L5-5"
    excerpt_sha256: "sha256:aa62b0eb17e954655f6c72c581d8e837e602b75b0e3366ee28e9dc2028935ab4"
  - resource: "src/smart_ticket/domain/discounts.py#L27-35"
    excerpt_sha256: "sha256:5b21670b385a034ebf8c1c9d8104297c86204c0703751a5e34a07e15b9080200"
---
以百分比整數表示的票價比例（100、95、85、75）；旅客票價 = 基本票價 × rate // 100。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Rate
