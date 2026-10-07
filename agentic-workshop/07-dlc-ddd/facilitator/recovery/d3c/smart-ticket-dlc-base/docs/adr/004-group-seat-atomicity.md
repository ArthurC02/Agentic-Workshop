# ADR 004：團體連續座位與本機補償


## Context

5–20人團體需同車廂完整連續空位，不可部分成立；付款失敗不得留下座位與Order。固定Seed容量及既有一般流程必須延續。

## Decision

Status：Accepted。既有Seat IDs映射carriage/row/seat/position，每車廂20位置，採可理解連續區段查找與一次保留。Group付款失敗以取消／全釋放／無Order及紀錄補償，共用付款也識別Type；不引入資料庫或通用交易Framework。Group Change拒絕，Paid Group Refund保留。

## Consequences

規則與失敗邊界清楚可測，標準布局不處理真實走道偏好；幾何支援多廂但容量不增加，仍是單程序本機模型。
