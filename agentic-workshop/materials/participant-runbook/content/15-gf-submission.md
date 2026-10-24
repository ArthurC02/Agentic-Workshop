---
id: gf-submission
title: Greenfield 回顧與交付決定
minute: 25-30
group: greenfield
section: Greenfield｜Tool
---

# Greenfield 回顧與交付決定

## Greenfield 交付決定

Agent 在做檢查點 4 時就先填，不用等它做完。理由與證據 Agent 會寫進 `notes/greenfield.md`；`/docs` 那一題，試完再改也可以。

```form
{"id": "greenfield-delivery", "title": "Greenfield 交付決定","fields":[
{"id": "accept", "label": "我接受這份交付嗎？", "type": "select", "options": ["接受：完整 MVP", "接受：部分完成，未完成已寫進 notes", "不接受，已請 Agent 修正"]},
{"id": "docs-flow", "label": "我在 /docs 親自試過訂票和付款，結果符合需求嗎？", "type": "select", "options": ["是", "部分符合", "否／沒走到"]},
{"id": "unsure", "label": "還有什麼不確定、要再問 Agent 的？（選填）", "type": "text", "suggestions": ["沒有"]}
]}
```

## 完成後想一想

等 Agent 的空檔先自己想一想，主持人揭曉時會問第 2 題。

1. **觀察**：哪一步的 Agent 回報讓你意外，或差點讓你放行了不該放行的東西？你是靠驗收對照表、審查答案還是 `/docs` 發現的？
2. **技巧**：如果一開始不要計畫、直接叫 Agent「把 MVP 做完」，你要怎麼確認它沒做錯？回到你的工作，哪一種任務最值得先要計畫、再小步放行？
3. **延伸**：如果交給你的是別人寫了一年、文件和程式不一定對得上的專案，你會先要 Agent 做什麼？

```callout sync
⏸ 看投影：第 30 分鐘請先停手，一起看 Greenfield 揭曉
```
