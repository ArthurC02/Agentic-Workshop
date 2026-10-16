---
type: Bounded Context
title: "訂票 Booking"
status: draft
business_owner: unknown
version: unknown
effective_from: unknown
subdomain: core
sources:
  - resource: "docs/requirements/business-rules.md#L11-15"
    excerpt_sha256: "sha256:4ad7d7efab7c15ab9fc7f02f521f49f4c4c03793e780266d8fad358856d3b8ff"
  - resource: "docs/requirements/business-rules.md#L59-61"
    excerpt_sha256: "sha256:bfaceff15c23a3781bfcc9d01871a443a40fb31e96ff01411383e40395369dde"
  - resource: "src/smart_ticket/domain/models.py#L43-55"
    excerpt_sha256: "sha256:d274efe92e7e8610be2e01376d32b519c006bd33e4691a3a68938484c5a36f88"
---
管理一筆訂票從建立、付款前待付、付款後、改票到退票的生命週期；一般訂票 1–4 人，團體訂票 5–20 人同一班次。
