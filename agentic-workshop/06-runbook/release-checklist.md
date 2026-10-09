# 工作坊正式放行清單

> 讀者：Repo 維護者、主持人與正式放行責任人。
> 使用時機：核對 P11 自動化候選成果，以及本次真人演練後決定是否正式發放。
> 前置條件：已取得具版本與 Checksum 的交付候選，閱讀 [Preflight](preflight-checklist.md)、[Recovery](recovery-plan.md) 與 [真人紀錄](rehearsal-record.md)。
> 可見性：Facilitator／Evaluation，不整份提供學員。

**Automated Candidate Status: NOT_RUN**（本模板未填實際自動化證據）。**Human Rehearsal Status: NOT_RUN**。**Workshop Release Decision: PENDING**。使用者已選擇本次安排真人演練，排程與人員待確認。自動化檢查通過只能支持候選包，不能單獨宣稱 90 分鐘工作坊已正式驗收。

## 本次 Release 識別

| 欄位 | 實際結果 |
|---|---|
| Candidate／Release ID、建立時間 | 未記錄 |
| 作者來源 Commit／來源清單 | 未記錄 |
| G0／G1／B0／B1／B2／B3 Tag 與完整 SHA | 未記錄 |
| 包清單／各包角色與發放階段 | 未記錄 |
| manifest／Checksum 檔與逐包核對 | 未核對 |
| 自動化證據、命令、退出碼、操作者 | 未記錄 |
| 真人演練 ID／日期／參與者／記錄者 | 未記錄 |
| 放行責任人／決策時間 | 未記錄 |

## 自動化候選與內容隔離

每項須提供本次真實證據；空勾選不是已執行報告。

- [ ] 六版獨立環境、Python 3.13、固定依賴、Import、Health／OpenAPI、代表 API Smoke 與 Reset 驗證完成。
- [ ] G0 的 Health 通過／8 個受控 Skip 有對應，G1／B1／B2／B3 全通過且無 Skip／XFail／未知失敗。
- [ ] B0 實際失敗 node 集合精確等已核實 Manifest，零未知失敗；不只核對五個數量，不將 exit 1 偽稱一般 pytest PASS。
- [ ] 已知 Warning 有來源與影響判定；未知 Warning／失敗已處理，不過濾或弱化測試掩蓋。
- [ ] Requirement／Rule／Code／Test／Document／Evaluation 追溯與本次版本一致。
- [ ] Candidate 的來源、輸出檔清單及 Checksum 雙向核對，生成可重現；未混入暫存、venv／cache／憑證。
- [ ] Participant 只含當時發放材料；無主持／答案／產製指令、內部連結、Bundle／Git 歷史或未來解答。
- [ ] Facilitator 與 Evaluation 依角色隔離；任務與答案包不能混發。
- [ ] B1／B2 Recovery 包依允許清單生成角色安全 README／API 摘要，確認 ADULT 等實際 Contract，內部／失效連結已移除或改寫。
- [ ] 受控包在乾淨輸出目錄安裝、版本 Gate 與 Smoke 通過；若不齊，有可執行分析／Review 降級方案。

自動化判定：NOT_RUN | PASS | FAIL。實際選擇：NOT_RUN。命令／輸出／責任人／時間：未記錄。未完成與修正：未記錄。

## 本次真人演練

證據引用 [Rehearsal Record](rehearsal-record.md) 的實際時間與觀察，不以測試秒數、字數推估或 Agent 模擬代替。

- [ ] 排程、一般工程師真人參與者、主持／計時／記錄／放行責任人已確認。
- [ ] 十段完整執行，90 分鐘總限制有真實開始／結束與偏差紀錄。
- [ ] Greenfield 個人、Time Skip 統一 B0、Brownfield 個人分析後 Shared Context、主要 Agent 執行實際成立。
- [ ] B1／B2／B3 分批揭露，人員在 B3 不 Coding／不補測試；版本及 Context 不混用。
- [ ] B3 13 分鐘實測，Gate 1／2 核准後才前進，Gate 3 至少審查測試及未完成，條件未解除時保持停止。
- [ ] Operating Rules 真人閱讀目標 2 分鐘內有實測及理解核對。
- [ ] 只有 EXCEPTION-DW-001，69–70 分鐘內最多 60 秒完成決策；縮 30 秒情況有原因與真實證據，未真正加入超範圍依賴。
- [ ] Recovery 實際切換或另次受控試演有原成果、時間、包 Checksum、新 Session／Context、Health 與接續紀錄。
- [ ] B1 Recovery 僅 52 分鐘進 B2，B2 Recovery 僅 63 分鐘進 B3；不提供 B3 解答作起點，不拿 Recovery 當本組已完成。
- [ ] Level 1–3／未完成如實記錄；治理 Rubric 與完整標準實作驗收分開，不排名。
- [ ] 80–90 分鐘回顧收斂有效實務、根因、控制點／平台需求、改善責任人及後續驗證。

真人判定：NOT_RUN | PASS | FAIL | INCOMPLETE。實際選擇：NOT_RUN。演練紀錄／觀察／責任人：未記錄。時間偏差、風險與重驗：未記錄。

## 缺項與修正結案

| 未通過／未驗證項目 | 影響與停止／降級 | 修正責任人 | 預定完成／重驗 | 實際證據／結論 |
|---|---|---|---|---|
| 自動化候選本次證據 | 待填，不能只靠舊報告放行 | 未記錄 | 未記錄 | NOT_RUN |
| 本次真人排程與演練 | 待確認人員與時段，正式放行保持待定 | 未記錄 | 未記錄 | NOT_RUN |
| 其他風險／偏差 | 未記錄 | 未記錄 | 未記錄 | 未驗證 |

## 最終 Decision

Workshop Release Decision: PENDING | APPROVE | REJECT

本次選擇：PENDING。

審查 Candidate ID／Checksum：未記錄；自動化證據：未記錄；真人演練證據：未記錄；未解問題：未記錄；決策理由：未記錄；放行責任人與時間：未記錄。

缺少必要實測或真人結論時保持 PENDING，不把「工具／素材完成」等同「活動已演練並可正式放行」。若不符合則記 REJECT 與修正／重驗，完成後另有具名決策。不得預勾、代填真人簽核或宣稱未執行成果已通過。

## 完成條件

候選來源與包驗證、真人時間／治理／Recovery 實測、未解問題結案及具名決策均可核對，才可宣稱正式工作坊放行；本文件目前是未執行的檢核模板。
