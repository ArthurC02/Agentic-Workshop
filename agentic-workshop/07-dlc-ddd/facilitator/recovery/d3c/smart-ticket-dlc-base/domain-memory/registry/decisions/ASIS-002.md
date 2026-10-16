---
type: Decision
status: stable
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/booking_service.py
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "src/smart_ticket/application/booking_service.py#L37-43"
    excerpt_sha256: "sha256:5afbdd645d50c0fbb72016112294f3ba1ef0f7287e3593090d9b70b01c2d0d19"
  - resource: "src/smart_ticket/application/group_booking_service.py#L30-34"
    excerpt_sha256: "sha256:433d2b3beb08d55525ea6f9589280faeaf2708ab4fa3d0ffc2987cbc6e8eaf6d"
  - resource: "src/smart_ticket/application/change_booking_service.py#L35-41"
    excerpt_sha256: "sha256:4f4f7438ae8b32f7ef59330582f66519ab596264cb7b2afddd39bc782e9a9b45"
  - resource: "src/smart_ticket/domain/fare_policy.py#L5-10"
    excerpt_sha256: "sha256:c3ea1b29b85b640f882740a4f4e696cbaed421e9c075157c5b73fd3feb5a3165"
  - resource: "src/smart_ticket/domain/discounts.py#L22-23"
    excerpt_sha256: "sha256:387a251a6e7b2b40e461fc5652817c591ef71bd5c9a43be7519b38afb939e19f"
---
現況觀察（非已核准決策）：計價迴圈在一般建立、團體建立、改票三處複製；新增計價規則必須三處一起改，否則路徑間不一致。文件說由 Fare Policy 協調，實際只走 DiscountPolicy，FarePolicy.calculate 只剩單元測試使用。
