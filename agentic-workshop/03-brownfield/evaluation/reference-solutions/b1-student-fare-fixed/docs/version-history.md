# B0 → B1 Version History

> 讀者：主持人、驗收人員與教材產製 Agent。
> 使用時機：核對 B0→B1 的來源與最小修復。
> 前置條件：閱讀 README 及 B1 Validation Report。
> 可見性：Evaluation／Agent Production。

## B0 演化背景

最初版本提供班次、一般訂票、模擬付款及 Order。12 個月中陸續加入會員、提前購票優惠、改票、退票、通知、座位指派與 Audit，最後整合 Fare／Discount 計算。B0 保留原 API 與模型脈絡，以既有模組延伸；正式標記為 `b0-brownfield-baseline`。重置採本機 In-Memory，不引入外部平台。

## B1 - Student Fare Fixed

B1 從 `b0-brownfield-baseline` 真實歷史延續，只將 Fare Policy 唯一學生票率常數由 85 改為 75；不調整既有測試期待值，不加入最有利優惠或團體訂票。App 與專案版本 metadata、README 及本來源紀錄同步標示 B1。

Tag 為 `b1-student-fare-fixed`；實際 Commit 與 Bundle 查核見外層 `14-b1-case-history-and-delta.md`。完整測試預期全部通過，實際結果及 Warning 以 B1 Validation Report 為準。本版本仍維持 B0 兩份受控文件落差，不宣稱已修復其他任務。

## 完成條件

能追查 G1→B0→B1 真實祖先、唯一票率修改、原測試未弱化與既有能力保留；版本故事與 metadata 不代替實際驗證。
