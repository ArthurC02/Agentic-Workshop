---
type: Term
title: "開立呼叫次數"
status: draft
not_same_as: []
required_qualifiers: []
owner: unknown
sources:
  - resource: "docs/requirements/business-rules.md#L89-90"
    excerpt_sha256: "sha256:24ef17d747db314a257f006bbaaadbc049a73926179ef851d8cd6cc5387aa916"
  - resource: "src/smart_ticket/domain/invoicing.py#L15-15"
    excerpt_sha256: "sha256:4aa9a81e7afb34594e6789ed0e4f0e31f69618d6d21977bfa4032b9bf9584dfb"
  - resource: "src/smart_ticket/domain/invoicing.py#L119-130"
    excerpt_sha256: "sha256:21f2715cd841b8f6faa3ce34766f746754d12b7d9538317096d9e932c8114f20"
---
Invoicing 為同一張發票呼叫服務商的累計次數（含第一次），每次都用同一 order_id；暫時失敗記錄最後錯誤並維持 PENDING，第 5 次仍未成功轉 FAILED。

# Relations
- Contexts: [invoicing](/contexts/invoicing)

# Synonyms
- attempts
- Issue Attempt
