---
id: retro
title: 回顧：Domain Memory 改變了什麼
minute: 165-180
group: dlc-retro
section: 回顧
---

# 回顧：Domain Memory 改變了什麼

15 分鐘，用今天實際留下的紀錄回答：檔案化、經審查的領域知識，到底有沒有改變 Agent 的輸出？哪裡只是儀式？沒觀察到的就寫「未觀察」，不要推測。

## 檢查點總覽

| 檢查點 | 全場分鐘 | 你要完成的事 |
|---|---:|---|
| 1 · 個人反思 | 165–169 | 每人先獨立填反思表 |
| 2 · 小組比較 | 169–174 | 兩人對照答案，分清事實與推測 |
| 3 · 收斂與行動 | 174–178 | 選 1–3 個有證據的改善，寫出負責人與驗證方式 |
| 4 · 匯出與結束 | 178–180 | 匯出全部表單；刪除簽章私鑰 |

## 檢查點 1 · 個人反思（第 165–169 分鐘）

- [ ] 先自己填，不要先討論。每題寫一個今天的具體例子，附 id、表單或指令輸出作為證據。

```form
{"id": "retro-reflection", "title": "DLC 反思表","fields":[
{"id": "fact-changed-output", "label": "哪一個 reviewed 事實改變了 Agent 的輸出？", "type": "textarea", "hint": "寫出 asset:id、Agent 原本會怎麼做、後來怎麼做。", "suggestions": [{"label": "例子範本", "text": "〈asset:id〉：Agent 原本〈 〉，查到這個事實後改為〈 〉（證據：〈表單／提示詞回覆〉）"}, "未觀察"]},
{"id": "candidate-near-fact", "label": "哪一個候選差點被當成事實？", "type": "textarea", "hint": "誰差點這樣做（你、夥伴或 Agent），在哪個檢查點發現。", "suggestions": [{"label": "例子範本", "text": "〈asset:id〉（候選）：〈誰〉差點把它當成〈限制／已確認〉，在〈檢查點〉發現，因為〈 〉"}, "未觀察"]},
{"id": "ritual-vs-governance", "label": "自我核准的「儀式感」和真實治理差在哪裡？", "type": "textarea", "hint": "今天兩個身分在同一台機器上，誰都能打出對方的名字。", "suggestions": [{"label": "比較範本", "text": "像儀式的步驟：〈 〉，因為〈 〉\n真的擋住錯誤的步驟：〈 〉，證據〈 〉\n真實團隊還需要：〈 〉"}]},
{"id": "counterfactual-lesson", "label": "哪一次 counterfactual 結果讓你意外？", "type": "textarea", "suggestions": [{"label": "例子範本", "text": "〈規則 id〉：預期〈killed／survived〉，實際〈 〉；學到〈 〉"}, "未觀察"]},
{"id": "gap", "label": "哪個知識缺口（查不到的名詞或未決問題）影響最大？", "type": "textarea", "suggestions": [{"label": "缺口範本", "text": "〈名詞／問題〉：影響〈哪一段的哪個決定〉"}, "未觀察"]}
]}
```

```callout warning
說清楚：今天的成對簽章是教學示範，不是安全保證
今天 Proposer 與 Maintainer 在同一台機器上操作，`record-approval` 只比對身分字串，私鑰也在同一個使用者資料夾裡；任何一人都能冒用另一人的名字，pre-push hook 也能用 `--no-verify` 跳過。它讓你看見治理的每一步留下什麼證據，但**不能**證明真的有兩個不同的人審查過。真實團隊需要不同的人、不同的機器與金鑰，以及伺服器端（例如受保護分支與必要審查）的強制檢查。
```

## 檢查點 2 · 小組比較（第 169–174 分鐘）

- [ ] 兩人（或三人）對照反思表。意見不同時，回到證據：表單紀錄、`verify-audit` 事件數、counterfactual 的 JSON、Handoff。
- [ ] 一起回答下面三題。

```form
{"id": "retro-group", "title": "小組比較","fields":[
{"id": "with-without", "label": "同一個需求，沒有 Domain Memory 時 Agent 會怎麼做？差別有證據嗎？", "type": "textarea", "suggestions": [{"label": "比較範本", "text": "需求卡〈 〉：沒有時〈推測／主課經驗〉；有時〈實際觀察〉；證據〈 〉"}, "未觀察，無法比較"]},
{"id": "cost", "label": "建立與維護 Domain Memory 花了多少時間？值得嗎？", "type": "textarea", "hint": "用今天各段的實際分鐘數，不要估計。", "suggestions": [{"label": "成本範本", "text": "D1〈 〉分、D2〈 〉分、D3 登記〈 〉分；換到〈 〉；結論〈 〉"}]},
{"id": "disagreement", "label": "我們意見不同的地方", "type": "textarea", "suggestions": ["沒有", {"label": "分歧範本", "text": "〈議題〉：A 認為〈 〉，B 認為〈 〉；證據〈 〉；待驗證〈 〉"}]}
]}
```

## 檢查點 3 · 收斂與行動（第 174–178 分鐘）

- [ ] 選 1–3 個**有證據**的改善，各自歸類：Domain Memory 內容、來源選擇、審查流程、工具、Agent 提示詞，或人員責任。
- [ ] 至少一項寫完整：誰負責、下一步、用什麼證據確認、期限。

```form
{"id": "retro-actions", "title": "改善行動","fields":[
{"id": "action-1", "label": "行動 1", "type": "textarea", "suggestions": [{"label": "行動範本", "text": "類別：〈 〉\n改善：〈 〉\n證據（今天的哪個紀錄）：〈 〉\n負責人：〈 〉\n驗證方式與期限：〈 〉"}]},
{"id": "action-2", "label": "行動 2（可留白）", "type": "textarea", "suggestions": [{"label": "行動範本", "text": "類別：〈 〉\n改善：〈 〉\n證據：〈 〉\n負責人：〈 〉\n驗證方式與期限：〈 〉"}, "待研究"]},
{"id": "keep", "label": "回到自己的專案，第一個想放進 Domain Memory 的事實", "type": "textarea", "suggestions": [{"label": "事實範本", "text": "〈事實〉：目前散在〈文件／程式／口頭〉，證據會是〈 〉"}]}
]}
```

## 檢查點 4 · 匯出與結束（第 178–180 分鐘）

- [ ] 刪除今天產生的簽章私鑰（持鑰的 Maintainer 在自己操作的那台機器執行）：

```cmd
# powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.dlc-keys\maintainer"
# bash
rm -rf "$HOME/.dlc-keys/maintainer"
```

- [ ] 匯出全部表單：

```callout warning
離開前請匯出所有表單
表單只暫存在這個瀏覽器中。按下方按鈕一次下載整場所有已填寫的表單（ZIP，每份表單一個 `.md` 檔），再依主持人指定方式保存。
```

```exportall
```

下載後打開 ZIP 內的 `README.md`，確認下列內容都在（未填寫的表單會列在最後）：

- [ ] [開場與環境](#environment) 四個檢查點確認
- [ ] [D1](#d1) 六個檢查點確認
- [ ] [D2](#d2) 六個檢查點確認
- [ ] [D3a](#d3a)、[D3b](#d3b)、[D3c](#d3c) 的決策卡、各檢查點確認與揭曉對照
- [ ] [D4](#d4) 的 Domain Memory 現況、已變動事實與 Handoff 摘要
- [ ] 本頁的反思表、小組比較與改善行動
- [ ] 有使用 Recovery 時，對應的 Recovery 紀錄

Agent 會忘記，但檔案不會；只有經過人審查、有證據、能被測試推翻的知識，才值得讓 Agent 當成事實。
