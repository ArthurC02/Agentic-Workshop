---
type: Decision
status: draft
decision_status: observed-design-leak
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/refund_service.py
sources:
  - resource: "src/smart_ticket/application/refund_service.py#L22-29"
    excerpt_sha256: "sha256:9a8e3026e2da7c72675f40b5c6c42bd619abcda7829a17e6d9decc0794b92865"
  - resource: "src/smart_ticket/infrastructure/store.py#L24-24"
    excerpt_sha256: "sha256:8aeaa023bf3a657baa00485f7e49f83443ffe2f6092c6a5bd43966a6331f2f17"
---
現況觀察（非已核准決策）：退款紀錄以 booking_id 為鍵且金額固定為總票價，結構上一筆訂票只能有一筆全額退款；部分退款需要先改變這個結構。
