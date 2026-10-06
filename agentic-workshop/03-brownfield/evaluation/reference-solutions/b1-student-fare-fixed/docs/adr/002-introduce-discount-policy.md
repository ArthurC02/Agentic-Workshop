# ADR 002：引入 Discount Policy

> 讀者：參與者與Agent。時機：理解計價成長。前置：閱讀主要規則及架構。可見性：Participant。

## Context

票價從旅客類型擴充至會員與提前購票，條件逐步增加。

## Decision

Status：Accepted。以Domain Discount Policy處理資格與採用結果，由Fare Policy／Application協調；保留既有條件分支順序，未因擴充全面重寫計價。

## Consequences

計價集中且可測試，但條件順序形成歷史耦合；政策變更需追查所有計價使用端、測試與文件。

## 完成條件

能辨識集中政策與呼叫端，不把ADR當作後續政策變更答案。
