"""Check that course text uses Taiwan Traditional Chinese: traditional characters and Taiwan vocabulary.

- any CJK character that Big5 (cp950) cannot encode is reported (simplified or non-Taiwan form);
- any term in MAINLAND is reported with its Taiwan replacement.
Scans authored course sources, docs/ and the .claude harness only (not built HTML, code packages (smart-ticket-*), vendor or evaluation reference solutions).
Run: uv run --no-project --python 3.13 python -X utf8 scripts/check_zh_tw.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"repository", "vendor", "reference-solutions", "recovery", "dist", "node_modules", "starter-repository"}
SKIP_NAMES = {"runbook.html", "facilitator-deck.html"}
# Mainland term -> Taiwan term. Only terms with no common Taiwan meaning; left out on purpose because Taiwan uses
# them too or they hit inside other words: 代碼(錯誤代碼) 變量(不變量) 交互(交互作用) 登錄(登錄表) 攔截 數組 線程 實時.
MAINLAND = {
    "軟件": "軟體", "硬件": "硬體", "信息": "資訊", "默認": "預設", "源碼": "原始碼",
    "接口": "介面", "服務器": "伺服器", "網絡": "網路", "用戶": "使用者", "運行": "執行", "調用": "呼叫",
    "屏幕": "螢幕", "打印": "列印", "鏈接": "連結", "內存": "記憶體", "數據庫": "資料庫",
    "文檔": "文件", "菜單": "選單", "緩存": "快取", "函數": "函式",
    "字符串": "字串", "模塊": "模組", "視頻": "影片", "兼容": "相容", "反饋": "回饋",
    "優先級": "優先順序", "調試": "除錯", "文件夾": "資料夾", "創建": "建立", "刷新": "重新整理",
    "智能": "智慧", "獲取": "取得", "在線": "線上", "示例": "範例", "異步": "非同步",
    "質量": "品質", "賬號": "帳號", "高效": "有效率", "落地": "實施", "閉環": "結案", "賦能": "協助",
    "抓手": "切入點", "打通": "串接", "激活": "啟用", "項目組": "專案團隊",
    "缺省": "預設", "操作系統": "作業系統", "程序員": "程式設計師", "寬帶": "寬頻", "博客": "部落格",
}
CJK = re.compile(r"[一-鿿]")


def sources() -> list[Path]:
    files = [*(ROOT / "agentic-workshop").rglob("*.md"), *(ROOT / "agentic-workshop").rglob("*.html"),
             *(ROOT / "docs").rglob("*.md"), *(ROOT / ".claude").rglob("*.md"), ROOT / "Agent.md"]
    return sorted(p for p in files if not SKIP_PARTS & set(p.parts) and p.name not in SKIP_NAMES
                  and not any(part.startswith("smart-ticket") for part in p.parts))


def problems(text: str) -> list[str]:
    out = []
    for ch in sorted({c for c in CJK.findall(text)}):
        try:
            ch.encode("cp950")
        except UnicodeEncodeError:
            out.append(f"非台灣繁體字「{ch}」")
    out += [f"「{m}」→「{t}」" for m, t in MAINLAND.items() if m in text]
    return out


def main() -> None:
    found = []
    for path in sources():
        hits = problems(path.read_text(encoding="utf-8", errors="ignore"))
        if hits:
            found.append(f"{path.relative_to(ROOT).as_posix()}: {'、'.join(hits)}")
    print("\n".join(found) or "ZH-TW PASS")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
