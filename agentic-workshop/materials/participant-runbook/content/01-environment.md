---
id: environment
title: 環境準備
minute: 00-07
group: open
section: 開始之前
---

# 環境準備

開場時確認下列項目，有問題立即告知主持人。

- [ ] 電腦已安裝 Python **3.13**（版本由 Agent 幫你確認）。
- [ ] 一個可用的 Coding Agent，能讀本機資料夾、修改檔案並執行終端機指令。
- [ ] 已安裝 Git（Agent 用它記下起點、回報改了什麼）。
- [ ] 已用瀏覽器開啟這份 `runbook.html`。

現在不用做任何準備：建環境的提示詞在 Greenfield 檢查點 1。這頁只放出錯時用的疑難排解。

## 疑難排解

遇到任何錯誤，先把錯誤交給 Agent，請它用白話說明，不要自己動手修：

```text
剛才的步驟出錯了。請先不要修改任何檔案，用白話告訴我：錯誤訊息是什麼意思、可能的原因、你建議怎麼處理（列 1–2 個做法），然後停下等我決定。
```

```callout tip
Agent 說 Python 不是 3.13
提示詞會要 Agent 停下來，不要改用其他版本；請告知主持人。
```

```callout tip
/docs 頁面一片空白
**/docs 的畫面要從網路載入，沒有網路就是空白頁。**
- 請 Agent 改用 Python 的 httpx 實際呼叫同一組 API
- 每一步的狀態碼和回應重點列給你看
- 在 notes 註明「/docs 無法載入，改由 Agent 呼叫 API」
```

```callout tip
Git 回報檔名太長（Filename too long）
**多半是解壓縮的路徑太深。**
- 把 ZIP 重新解壓縮到短路徑，例如 `C:\work\g0`
- 或請 Agent 只在這個專案設定 `core.longpaths` 為 true（不要用 --global）
```

```callout tip
Port 8000 已被佔用
**請 Agent 改用其他未使用的埠號（Port），例如 8001。**
- 它要告訴你新的 `/docs` 網址
- 在 notes 寫下實際使用的 Port
```

```callout danger
套件無法安裝時
網路不可用或 Agent 回報套件安裝失敗，請立即告知主持人，不要臨時更換 Python 版本或改用其他技術。
```
