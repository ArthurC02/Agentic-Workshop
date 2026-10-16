---
type: Term
title: "旅客部分取消"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L126-126"
    excerpt_sha256: "sha256:8314d3271072303b4b967d30e80f059c081b0f7c91caec6e60246e8c6cd2526c"
  - resource: "src/smart_ticket/domain/cancellation.py#L4-20"
    excerpt_sha256: "sha256:3f9ca6d206136d8f9e66c0706c06991db6adc2450da582bf4751592604809657"
---
已付款團體只取消部分旅客：依出發前天數 D（出發日台灣日期 − 今天）收手續費，D ≥ 14 為 10%、7–13 為 20%、1–6 為 30%、D ≤ 0 拒絕；手續費逐位以該旅客票價計算並向下取整，退款＝被取消旅客票價合計 − 手續費。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Partial Cancellation
- cancel_passengers
- 取消手續費
