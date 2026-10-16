---
type: Term
title: "退款紀錄"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L38-38"
    excerpt_sha256: "sha256:1089369560938252a2769a446548ee401da7524769827ec26ceea685a9cef352"
  - resource: "src/smart_ticket/domain/records.py#L15-19"
    excerpt_sha256: "sha256:3a2f0808e688b7ea08262a83e32a5972d134030bb3b592bb283cee607168adc4"
  - resource: "src/smart_ticket/application/refund_service.py#L22-29"
    excerpt_sha256: "sha256:9a8e3026e2da7c72675f40b5c6c42bd619abcda7829a17e6d9decc0794b92865"
---
已付款訂票退票時建立的唯一本機紀錄，金額為訂票總票價；目前以 booking_id 為鍵，結構上一筆訂票只能退一次。

# Relations
- Contexts: [booking](/contexts/booking)

# Synonyms
- Refund Record
- RefundRecord
