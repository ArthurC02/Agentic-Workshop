# D4 Handoff 範本：交給下一個 Agent

> 讀者：DDD 延伸課程學員。使用時機：D4 檢查點 3；把今天的 Domain Memory 交給下一個接手的 Agent 或同事。

依 Plugin 的 implementation handoff 七段撰寫，存成 `docs/handoffs/d4-next-agent.md`。**只引用 Registry 中查得到的 id**（用 `get-record` 或 `get-context` 確認過）；查不到的寫進 Unknowns，不要編 id。每一項標明是 reviewed 還是候選。

```text
# Handoff：Smart Ticket Domain Memory（〈日期〉）

## Domain facts
- reviewed Contexts：〈context id〉、〈context id〉
- reviewed 詞彙與規則：〈asset:id〉、〈asset:id〉
- D3 新增的候選（尚未審查，不可當成限制）：〈asset:id〉、〈asset:id〉
- D3 之後已不成立、需要新提案取代的 reviewed 事實：〈asset:id → 新候選 id〉

## Forces
- 一致性：〈哪些資料必須同時成立〉
- 失敗與重試：〈外部系統、冪等鍵〉
- 生命週期：〈預留／歸還、部分取消〉

## Decision
- 〈今天做出的設計決定，各一句，附需求卡 AC 或規則 id〉

## External systems
- 〈系統〉：domain 要它做什麼；必須分辨的結果；目前用什麼替身測試

## Unknowns
- 〈需求卡待決問題中仍未決定的項目〉
- 〈verify-sources 的 stale 項目：哪些新檔案還沒經過來源確認〉

## Proof obligations
- 〈規則或 AC id〉 → 〈測試〉（最後一次完整 pytest：〈 〉 passed，〈 〉 failed）

## Counterfactual check
| 規則 id | 改壞的保護（檔案:行 原字串 → 改後） | 測試 | 結果 |
|---|---|---|---|
| 〈 〉 | 〈 〉 | 〈 〉 | killed |
```

交出前自我檢查：

- [ ] 七段都在，沒有空段（沒有就寫「無」並說明）。
- [ ] 每個 id 都在 Registry 查得到；候選與 reviewed 分清楚。
- [ ] 沒有把未決問題寫成已決定。
- [ ] counterfactual 表格每一列都有實際看到的 `killed`。
