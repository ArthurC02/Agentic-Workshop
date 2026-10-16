---
type: Term
title: "退款紀錄"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L38-38"
    excerpt_sha256: "sha256:1089369560938252a2769a446548ee401da7524769827ec26ceea685a9cef352"
  - resource: "src/smart_ticket/domain/records.py#L15-19"
    excerpt_sha256: "sha256:cb21e5b34b19e971bf12ded045c65474780c88b696584995d6b1e9c17fe312ab"
  - resource: "src/smart_ticket/application/refund_service.py#L22-29"
    excerpt_sha256: "sha256:33b78b1face67df0d1447198fdb46d4ac8d08b5d059711d796298193d3cc7d8d"
---
已付款訂票退票時建立的唯一本機紀錄，金額為訂票總票價；目前以 booking_id 為鍵，結構上一筆訂票只能退一次。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Refund Record
- RefundRecord
