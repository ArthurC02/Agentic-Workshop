---
type: Interaction
status: stable
consistency: synchronous
delivery: "同程序直接呼叫 DiscountPolicy.calculate（建立、團體建立、改票三處各自複製呼叫迴圈）"
verified:
  - by: "human:Maintainer <maintainer@example.com>"
    at: "2026-10-07T03:06:45.386842Z"
sources:
  - resource: "docs/adr/002-introduce-discount-policy.md#L18-18"
    excerpt_sha256: "sha256:89a5ec6bb5df3e3e6065d0fb5282e873dadefc3822bbd8b5725560671a0e04a4"
  - resource: "src/smart_ticket/application/booking_service.py#L37-43"
    excerpt_sha256: "sha256:5afbdd645d50c0fbb72016112294f3ba1ef0f7287e3593090d9b70b01c2d0d19"
  - resource: "src/smart_ticket/application/group_booking_service.py#L30-34"
    excerpt_sha256: "sha256:433d2b3beb08d55525ea6f9589280faeaf2708ab4fa3d0ffc2987cbc6e8eaf6d"
  - resource: "src/smart_ticket/application/change_booking_service.py#L35-41"
    excerpt_sha256: "sha256:4f4f7438ae8b32f7ef59330582f66519ab596264cb7b2afddd39bc782e9a9b45"
---
# Relations
- Producer context: [pricing](/contexts/pricing)
- Consumer context: [booking](/contexts/booking)
