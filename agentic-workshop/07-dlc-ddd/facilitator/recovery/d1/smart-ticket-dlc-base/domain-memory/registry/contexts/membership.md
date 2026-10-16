---
type: Bounded Context
title: "會員 Membership"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: supporting
sources:
  - resource: "docs/requirements/business-rules.md#L25-28"
    excerpt_sha256: "sha256:e822e1a70d250df62c3ad9be896a422b092cfde24ea0f8798957093c4e459fd4"
  - resource: "src/smart_ticket/domain/members.py#L4-12"
    excerpt_sha256: "sha256:bb0c05aa56856c0bc84f12f67c4e4138211ff7eb33ce7c8ca9f4ae9baca8842f"
---
提供會員身分、會員類型（STANDARD／CORPORATE）與點數餘額查詢；訂票可不綁定會員。
