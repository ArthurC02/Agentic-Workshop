# B2 凍結文件勘誤

> 讀者：主持人、Evaluation與教材維護者。時機：使用B2標準來源及驗收文件時。
> 前置：已驗收B2 Tag／快照與本輪一致性審查。可見性：內部；學員Recovery只發角色安全摘要，不直接發本勘誤或完整Evaluation。

## 合約名稱

B2的實際DiscountType Enum及100%預設回應為`ADULT`，不是`FULL_FARE`。

| 凍結文件位置 | 舊文字 | 正確解讀與驗證 |
|---|---|---|
| [API範例](reference-solutions/b2-best-discount-policy/docs/api-examples.md)第55行 | discount_type為FULL_FARE | 應為ADULT；rate100、amount700不變 |
| [Architecture](reference-solutions/b2-best-discount-policy/docs/architecture.md)第15行 | 加入FULL_FARE | 應為ADULT全額預設候選 |
| [Discount Overview](reference-solutions/b2-best-discount-policy/docs/discount-overview.md)第5行 | FULL_FARE100% | 應為ADULT100% |

實際依據：[DiscountType／Policy](reference-solutions/b2-best-discount-policy/src/smart_ticket/domain/discounts.py)、[Unit測試](reference-solutions/b2-best-discount-policy/tests/unit/test_best_discount_policy.py)。B3文件已修正名稱，但B2凍結來源為保留原Tag／Hash與追溯而不改寫。

## 驗收說明

[B2 AC Map](09-b2-acceptance-test-map.md)的AC-B2-013原「文件與Code同步」判定漏掉名稱誤文，不能以該舊判定宣稱原B2文件完全一致。本勘誤補上已知缺口：功能／Enum／測試結果保持有效，使用說明以ADULT為準。B2 Recovery生成摘要不得再引入FULL_FARE。

改票指南的舊「不處理金額差異」則是刻意保留的DEBT-003：實際記錄new-old Fare Difference，不做補退款金流；與本次意外名稱錯誤分開。參考[受控債務地圖](../facilitator/03-controlled-debt-map.md)，不要為消除文字不一致破壞原教材。

完成條件：維護者能定位三處誤文、實際合約與測試；使用勘誤或正確摘要，不修改凍結案例來源；本勘誤不代替真人Review。
