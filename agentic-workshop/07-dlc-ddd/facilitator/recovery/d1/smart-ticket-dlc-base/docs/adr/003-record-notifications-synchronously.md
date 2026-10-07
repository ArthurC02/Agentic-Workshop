# ADR 003：同步記錄通知


## Context

付款、改票、退票需記錄通知，但本機情境不使用Email或簡訊服務。

## Decision

Status：Accepted。Application同步呼叫Notification Service，只新增In-Memory紀錄，不導入Queue或外部發送。

## Consequences

容易理解與驗證，但流程與通知有同步耦合；當時規模不需要解耦或訊息佇列。
