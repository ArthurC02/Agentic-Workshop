---
type: Business Rule
status: draft
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L29-30"
    excerpt_sha256: "sha256:021b4fd4a4f7bd1bccc5426fa7cd23514c7598ae922537153134c195807b2716"
  - resource: "src/smart_ticket/domain/discounts.py#L30-31"
    excerpt_sha256: "sha256:ee4d4e5395e763c2b00eb1adeda46c7d8aec282304f7635b2ba0935424bb682f"
  - resource: "tests/integration/test_advance.py#L4-10"
    excerpt_sha256: "sha256:32a05044cf694fbd69abc830f3861451c4ef97d6fc755f2f8354e0d36160f6fe"
---
購票日至出發日相差至少 14 天才具備 85% 提前購票資格；未滿 14 天不具備（FARE-006）。

# Relations
- Contexts: [pricing](/contexts/pricing)

# Examples
- 相差 13 天：700
- 相差 14 天：595
- 相差 15 天：595
