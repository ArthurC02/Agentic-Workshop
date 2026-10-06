# ADR 001：採用 In-Memory Repositories

> 讀者：參與者與Agent。時機：架構理解。前置：閱讀架構。可見性：Participant。

## Context

早期流程需快速重現、測試與重置，活動不依賴外部服務。

## Decision

Status：Accepted。採本機In-Memory Adapter與Repository Protocol，固定Seed與共用RLock；重啟資料清除。

## Consequences

部署與理解簡單，測試可隔離；無持久化、跨程序一致性或正式資料庫交易保障。

## 完成條件

能說明此取捨與限制，不自行加外部資料庫。
