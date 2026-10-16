---
type: Decision
status: stable
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/refund_service.py
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/application/refund_service.py#L22-29"
    excerpt_sha256: "sha256:33b78b1face67df0d1447198fdb46d4ac8d08b5d059711d796298193d3cc7d8d"
  - resource: "src/smart_ticket/infrastructure/store.py#L24-24"
    excerpt_sha256: "sha256:8aeaa023bf3a657baa00485f7e49f83443ffe2f6092c6a5bd43966a6331f2f17"
---
現況觀察（非已核准決策）：退款紀錄以 booking_id 為鍵且金額固定為總票價，結構上一筆訂票只能有一筆全額退款；部分退款需要先改變這個結構。
