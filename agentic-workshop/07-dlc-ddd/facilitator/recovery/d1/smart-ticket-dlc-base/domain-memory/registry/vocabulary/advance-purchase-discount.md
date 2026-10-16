---
type: Term
title: "提前購票優惠"
status: draft
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L29-30"
    excerpt_sha256: "sha256:021b4fd4a4f7bd1bccc5426fa7cd23514c7598ae922537153134c195807b2716"
  - resource: "src/smart_ticket/domain/discounts.py#L30-31"
    excerpt_sha256: "sha256:ee4d4e5395e763c2b00eb1adeda46c7d8aec282304f7635b2ba0935424bb682f"
---
購票日（系統 Clock 的今天）至出發日相差至少 14 天時取得的 85% 資格；13 天不符合。

# Relations
- Not same as: [corporate-discount](/vocabulary/corporate-discount)
- Contexts: [pricing](/contexts/pricing)

# Synonyms
- Advance Purchase
- ADVANCE
