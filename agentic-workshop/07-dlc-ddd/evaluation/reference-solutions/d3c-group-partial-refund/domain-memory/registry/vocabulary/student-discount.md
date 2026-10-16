---
type: Term
title: "學生優惠"
status: stable
not_same_as: []
required_qualifiers: []
owner: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L17-17"
    excerpt_sha256: "sha256:5053fd35676ab3c319a54a13f535b951134e7e38bb5591caf3d1e706c0da86c8"
  - resource: "src/smart_ticket/domain/fare_policy.py#L3-3"
    excerpt_sha256: "sha256:8c54d88ec7aedbc4470bc05c7c4cab7ac42a4070060d791f8e48de03d70ee59b"
  - resource: "src/smart_ticket/domain/discounts.py#L28-29"
    excerpt_sha256: "sha256:159904de6ab72ab01cc76e078fe4222b62ef50e7f5af8153d4263b311526fabe"
---
旅客類型為學生時取得的 75% 資格；仍與其他資格一起比較，取最低 rate。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- STUDENT
