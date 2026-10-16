---
type: Term
title: "購票人發票資訊"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L94-95"
    excerpt_sha256: "sha256:d200cc169d1d92b72d4b3630d43481dbba54970168a105dbfb371a98414d70ec"
  - resource: "src/smart_ticket/domain/invoicing.py#L30-45"
    excerpt_sha256: "sha256:ad365f7d34df07d4bd1f9d841e8f456293bbeb433d9d3954d5eaadabab16f10f"
---
付款時選填的統編（8 位數字，須附公司名稱）或手機條碼載具（/ 加 7 碼），二者擇一；皆未提供時開立一般個人發票。格式錯誤在扣款前以 422 拒絕；資訊存在 Invoice，不寫入 Booking 或 Order。

# Relations
- Contexts: [invoicing](/contexts/invoicing)

# Synonyms
- InvoiceBuyer
- Buyer Info
