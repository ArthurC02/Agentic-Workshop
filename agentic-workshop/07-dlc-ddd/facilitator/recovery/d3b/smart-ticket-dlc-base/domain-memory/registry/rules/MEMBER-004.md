---
type: Business Rule
status: stable
owner: unknown
version: unknown
effective_from: unknown
effective_until: unknown
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/requirements/business-rules.md#L28-28"
    excerpt_sha256: "sha256:7dd7a93f7b101bd0ea0d835b5d245434d50dd7dbd5afd3572bc9ce5e19d2f83a"
  - resource: "src/smart_ticket/infrastructure/store.py#L20-22"
    excerpt_sha256: "sha256:c0cb77d95b42908a6ae7b3e474d1352e7c07b22e10b07597f26caf4106b06b6e"
  - resource: "tests/integration/test_seed.py#L17-20"
    excerpt_sha256: "sha256:bf776c80dcce873e6311ddfa006152a7239fd6979fd0452fed8cc130d1dd781b"
---
每位會員有非負整數點數餘額，可經會員查詢取得；目前沒有累積或使用點數的功能。

# Relations
- Contexts: [membership](/contexts/membership)

# Examples
- M001 1200、M002 5000、M003 0
