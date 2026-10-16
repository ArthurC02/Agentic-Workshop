---
type: Decision
status: draft
decision_status: observed-design-leak
effective_from: unknown
supersedes: []
source: src/smart_ticket/application/booking_service.py
sources:
  - resource: "src/smart_ticket/application/booking_service.py#L37-43"
    excerpt_sha256: "sha256:3ce6fd33b3b30605b27a03360d761e320c77422016c0ef33aeef8f42ea2b32c1"
  - resource: "src/smart_ticket/application/group_booking_service.py#L30-34"
    excerpt_sha256: "sha256:55aaae1d599e8bad154046016d7d79052bbc9c5b06cdb03166ae8c17fb79e898"
  - resource: "src/smart_ticket/application/change_booking_service.py#L35-41"
    excerpt_sha256: "sha256:f6f66bf2371fb9c4e0383330678f70f78a6df7ff40749627421ae5359bd3eb21"
  - resource: "src/smart_ticket/domain/fare_policy.py#L5-10"
    excerpt_sha256: "sha256:c3ea1b29b85b640f882740a4f4e696cbaed421e9c075157c5b73fd3feb5a3165"
  - resource: "src/smart_ticket/domain/discounts.py#L22-23"
    excerpt_sha256: "sha256:387a251a6e7b2b40e461fc5652817c591ef71bd5c9a43be7519b38afb939e19f"
---
現況觀察（非已核准決策）：計價迴圈在一般建立、團體建立、改票三處複製；新增計價規則必須三處一起改，否則路徑間不一致。文件說由 Fare Policy 協調，實際只走 DiscountPolicy，FarePolicy.calculate 只剩單元測試使用。
