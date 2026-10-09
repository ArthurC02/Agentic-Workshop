# 主持 Runbook、回顧與評估整合產製指令書

> 讀者：P10素材產製Agent與Repo維護者。時機：P0–P9已驗收後。
> 前置：總控00、技術01、任務05、治理06及各版真實驗證報告。本指令整合既有要求，不改商業規則或90分鐘配置。

## 授權範圍與來源

本輪使用者「下一個新目標」依既定路線啟動P10。以總控及05／06為準；contents/07評估與08主持指南的一日／半日、跨角色交接只作參考，改用90分鐘、個人Greenfield→Time Skip→個人分析→小組Shared Context及主要Agent執行。（2026-10-09：contents/07、08 已改寫為現行 90 分鐘設計，一日／半日版本已刪除。）

## 輸出與責任

- `agentic-workshop/05-retrospective/participant/reflection-sheet.md`、`maturity-comparison.md`：以真實證據比較Tool／Teammate／Digital Worker，記錄有效實務、根因、改善與未完成，無標準解答。
- `05-retrospective/facilitator/debrief-guide.md`、`organization-adoption-prompts.md`：80–90分鐘回顧、組織方法與控制點／平台需求，含時間、提示／停止與產出。
- `05-retrospective/evaluation/workshop-evaluation-index.md`：各階段目的、學員輸入、成果、AC、提示、答案／接受範圍及驗證連結；區分功能完成度與治理Rubric，不排名、不編造結果。
- `06-runbook/workshop-runbook.md`、`environment-setup.md`、`preflight-checklist.md`、`recovery-plan.md`：主持完整流程、準備、版本專屬Gate及受控復原。
- `06-runbook/evaluation/p10-validation-report.md`與`p10-validation-evidence.json`：靜態檢查、時程、隔離、來源雜湊及獨立審查證據。素材驗收不等於演練或正式交付。

## 必需檢查

1. 主流程十段為00–07、07–29、29–33、33–39、39–44、44–52、52–63、63–76、76–80、80–90，無缺口或重疊，加總90分鐘。
2. Greenfield個人；Brownfield先個人Agent分析再小組整合；Time Skip統一B0，不以個人G1作小組起點。
3. B1／B2／B3分批揭露；B3先宣布人不Coding，再發Work Order與三Gate。唯一SQLite事件包含在69–70分鐘，不另加時，不真安裝。
4. 每段列Cue、觀察、提示條件與停止／降級；時間不足保留理解／設計Gate及最低交付Review，不以人補程式救場。
5. 環境Python3.13／venv／pip／固定依賴，PowerShell與一般shell啟動方式可操作；`src` Import Path正確，無必要前端、DB、外部服務／真實金流。Agent服務可用性與本機案例不需外部API分開說明。
6. Preflight明列G0受控Skip、G1全通過、B0核實Manifest失敗集合且零未知、B1／B2／B3全通過；既知Warning可識別，未知失敗不得放行。空勾選表不當已執行證據。
7. Recovery明列切換觸發、已驗收版本來源、保留原成果／失敗／切換時間、新Session與Context確認，以及按發放時點只提供必要前版能力。
8. B1 Recovery供52分鐘進B2，B2 Recovery供63分鐘進B3；G1僅必要主持示範，B3答案不在63分鐘供學員作起點。不得發完整Evaluation、Bundle、作者Repo、未來解答或歷史。
9. 確定Recovery允許內容及排除清單，隔離套用於文件／連結／程式／隱藏檔／Git；若受控包或驗證不齊，採分析／Review降級，不能直接分享Evaluation目錄。
10. 80–90分鐘收斂成熟度、有效實務／根因、Context／Rule／Skill／流程／平台／治理改善與責任人／後續驗證。無時間數據記未觀察，不用測試執行秒數代替人員活動時間。
11. O-01時程／角色與O-02完整Reference DoD／學員Level1–3在新素材中對齊；真實演練解除證據保留到P11，不刪原決策歷史。
12. 相對連結有效、Markdown區塊平衡；Participant不能連向主持／答案／產製指令。G0–B3及P9來源凍結，不在本階段改程式、打包或宣稱演練完成。

## 完成條件

上述11份輸出完成，靜態一致性、來源、時程及內容隔離檢查通過，可判P10文件基線PASS；實際Preflight、受控包生成、Recovery演練與90分鐘真人活動為P11待執行事項。收尾審視Agent.md並提交本機Commit，下一目標P11需使用者授權啟動。
