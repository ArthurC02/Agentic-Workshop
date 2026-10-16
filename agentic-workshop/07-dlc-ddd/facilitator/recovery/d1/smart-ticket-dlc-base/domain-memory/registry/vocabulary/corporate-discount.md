---
type: Term
title: "企業會員優惠"
status: draft
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L27-27"
    excerpt_sha256: "sha256:bd508437b67a7f6e2c2006663d0ba265a0763c7f68e597306310f77974d1d95e"
  - resource: "src/smart_ticket/domain/discounts.py#L32-33"
    excerpt_sha256: "sha256:67eff644f630d233a69dae193ed3a268cf2b0faf36f14ace1bea7429d0acab95"
---
訂票綁定的會員類型為 CORPORATE 時取得的 95% 資格；資格判斷目前寫在 Pricing，直接讀取 Membership 的 Member 型別。

# Relations
- Not same as: [advance-purchase-discount](/vocabulary/advance-purchase-discount)
- Contexts: [pricing](/contexts/pricing)
- Contexts: [membership](/contexts/membership)

# Synonyms
- CORPORATE
