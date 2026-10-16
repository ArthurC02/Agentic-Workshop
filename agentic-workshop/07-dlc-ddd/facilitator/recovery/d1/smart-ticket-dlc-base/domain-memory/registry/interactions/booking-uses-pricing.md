---
type: Interaction
status: draft
consistency: synchronous
delivery: "同程序直接呼叫 DiscountPolicy.calculate（建立、團體建立、改票三處各自複製呼叫迴圈）"
sources:
  - resource: "docs/adr/002-introduce-discount-policy.md#L18-18"
    excerpt_sha256: "sha256:89a5ec6bb5df3e3e6065d0fb5282e873dadefc3822bbd8b5725560671a0e04a4"
  - resource: "src/smart_ticket/application/booking_service.py#L37-43"
    excerpt_sha256: "sha256:3ce6fd33b3b30605b27a03360d761e320c77422016c0ef33aeef8f42ea2b32c1"
  - resource: "src/smart_ticket/application/group_booking_service.py#L30-34"
    excerpt_sha256: "sha256:55aaae1d599e8bad154046016d7d79052bbc9c5b06cdb03166ae8c17fb79e898"
  - resource: "src/smart_ticket/application/change_booking_service.py#L35-41"
    excerpt_sha256: "sha256:f6f66bf2371fb9c4e0383330678f70f78a6df7ff40749627421ae5359bd3eb21"
---
# Relations
- Producer context: [pricing](/contexts/pricing)
- Consumer context: [booking](/contexts/booking)
