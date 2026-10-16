---
type: Term
title: "點數餘額"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L28-28"
    excerpt_sha256: "sha256:7dd7a93f7b101bd0ea0d835b5d245434d50dd7dbd5afd3572bc9ce5e19d2f83a"
  - resource: "src/smart_ticket/domain/members.py#L12-12"
    excerpt_sha256: "sha256:89966f34a24ddb9a7558ebb029c27995641c123d46aa71d307a5462b247d700b"
---
每位會員的非負整數點數，可經會員查詢取得；目前沒有任何累積或使用點數的功能。

# Relations
- Contexts: [membership](/contexts/membership)

# Synonyms
- points_balance
