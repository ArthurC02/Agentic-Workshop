# ADR 003：同步記錄通知

> 讀者：參與者與Agent。時機：理解流程依賴。前置：閱讀架構。可見性：Participant。

## Context

付款、改票、退票需記錄通知，但本機情境不使用Email或簡訊服務。

## Decision

Status：Accepted。Application同步呼叫Notification Service，只新增In-Memory紀錄，不導入Queue或外部發送。

## Consequences

容易理解與驗證，但流程與通知有同步耦合；目前活動不要求解耦或訊息佇列。

## 完成條件

理解紀錄與真實發送的差別及歷史取捨，不擴增基礎設施。
