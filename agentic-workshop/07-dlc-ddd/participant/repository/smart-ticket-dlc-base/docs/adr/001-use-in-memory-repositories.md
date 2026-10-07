# ADR 001：採用 In-Memory Repositories


## Context

早期產品需快速重現、測試與重置，不依賴外部資料庫。

## Decision

Status：Accepted。採本機In-Memory Adapter與Repository Protocol，固定Seed與共用RLock；重啟資料清除。

## Consequences

部署與理解簡單，測試可隔離；無持久化、跨程序一致性或正式資料庫交易保障。
