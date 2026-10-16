# Bounded Contexts

- [訂票 Booking](/contexts/booking) — 管理一筆訂票從建立、付款前待付、付款後、改票到退票的生命週期；一般訂票 1–4 人，團體訂票 5–20 人同一班次。.
- [座位庫存 Inventory](/contexts/inventory) — 依班次容量配置與釋放座位：同班次座位不重複，團體需同車廂連續座位，訂票建立即保留、退票與團體付款失敗時釋放。.
- [會員 Membership](/contexts/membership) — 提供會員身分、會員類型（STANDARD／CORPORATE）與點數餘額查詢；訂票可不綁定會員。.
- [付款 Payment](/contexts/payment) — 向付款閘道扣款；成功時建立唯一 Order 作為付款當時的金額快照，團體付款失敗時執行補償。.
- [計價 Pricing](/contexts/pricing) — 逐位旅客評估所有優惠資格，採 rate 最低的單一優惠（不疊加），產生每位旅客的整數票價與 Applied Discount。.
