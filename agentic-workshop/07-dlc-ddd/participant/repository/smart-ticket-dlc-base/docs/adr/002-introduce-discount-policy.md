# ADR 002：引入 Discount Policy


## Context

票價從旅客類型擴充至會員與提前購票，條件逐步增加。

## Decision

Status：Accepted。以Domain Discount Policy處理資格與採用結果，由Fare Policy／Application協調；保留既有條件分支順序，未因擴充全面重寫計價。

## Consequences

計價集中且可測試，但條件順序形成歷史耦合；政策變更需追查所有計價使用端、測試與文件。

## 後續決策：最有利單一優惠

Status：Accepted。優惠政策從歷史首個符合改為全部資格候選最低rate，逐Passenger評估且不疊加；局部改善Policy並保留原呼叫邊界，建立與改票共用，結果明細可追溯。原Context與過去Decision保留作歷史，不代表目前仍以順序選首個符合。
