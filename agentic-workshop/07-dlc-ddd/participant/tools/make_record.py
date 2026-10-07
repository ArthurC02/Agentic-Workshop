"""以 cite 證據組出一筆完整的 Domain Registry record JSON，可直接交給 upsert-candidate。

單筆（在 Repo 根目錄執行）：
  py -3.13 -X utf8 ../tools/make_record.py --asset vocabulary --id advance-purchase-discount \\
      --name "提前購票優惠" --definition "購票日至出發日至少 14 天時的 85% 票價資格" \\
      --context pricing --evidence docs/requirements/business-rules.md:29-30 \\
      --evidence src/smart_ticket/domain/discounts.py:30-31 --upsert

批次（一個 JSON 陣列，每個物件用同樣的鍵；evidence 為 "路徑:起-迄" 字串陣列）：
  py -3.13 -X utf8 ../tools/make_record.py --batch d1-records.json --upsert

主要文字欄位：contexts 用 --responsibility，vocabulary 用 --definition，rules/decisions 用 --statement；
其他欄位用 --set 欄位=值（值若是 JSON 會被解析，例如 --set 'invariants=["..."]'）。
輸出預設寫到 records/<asset>-<id>.json；加 --upsert 會接著呼叫 upsert-candidate（一律寫成 candidate）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402

ASSETS = ["contexts", "vocabulary", "aggregates", "rules", "contracts", "interactions", "decisions",
          "events", "capabilities", "value-objects", "dependency-policies"]
# Plugin 對 reviewed record 的必要欄位（registry-schema.md），review 由 apply-approved-updates 產生。
REQUIRED = {
    "contexts": ("name", "responsibility"),
    "vocabulary": ("name", "definition", "contexts"),
    "aggregates": ("context", "root", "invariants"),
    "rules": ("contexts", "statement"),
    "contracts": ("kind", "producer_context", "consumer_contexts", "version", "compatibility_policy",
                  "data_classification"),
    "interactions": ("producer_context", "consumer_context", "consistency", "delivery"),
    "decisions": ("statement", "source"),
    "events": ("owner_context", "meaning", "schema"),
    "capabilities": ("context", "meaning"),
    "value-objects": ("context", "meaning", "fields"),
    "dependency-policies": ("from_context", "to_context", "mode", "policy"),
}
# 未知的負責人或日期記為 unknown，不得省略（registry-schema.md）。
DEFAULTS = {
    "contexts": {"business_owner": "unknown", "version": "unknown", "effective_from": "unknown"},
    "vocabulary": {"synonyms": [], "not_same_as": [], "required_qualifiers": [], "owner": "unknown"},
    "rules": {"owner": "unknown", "version": "unknown", "effective_from": "unknown",
              "effective_until": "unknown", "examples": []},
    "aggregates": {"entities": [], "value_objects": [], "domain_services": [], "policies": [], "commands": [],
                   "allowed_dependencies": [], "prohibited_dependencies": []},
    "decisions": {"effective_from": "unknown", "supersedes": []},
}
MULTI_CONTEXT = {"vocabulary", "rules"}
SINGLE_CONTEXT = {"aggregates": "context", "capabilities": "context", "value-objects": "context",
                  "events": "owner_context"}
CLASSIFIED_HINT = "docs/requirements/、docs/adr/、src/ 與 tests/ 下的 test_*.py"


def parse_evidence(spec: str) -> tuple[str, int, int]:
    """'path:12-18' 或 'path:12' → (path, 12, 18)。"""
    path, sep, lines = spec.rpartition(":")
    if not sep or not path:
        raise ValueError(f"證據格式應為 路徑:起-迄，例如 src/a.py:10-12，收到：{spec}")
    start, _, end = lines.partition("-")
    try:
        first, last = int(start), int(end or start)
    except ValueError:
        raise ValueError(f"行號不是數字：{spec}") from None
    if first < 1 or last < first:
        raise ValueError(f"行號範圍不合理：{spec}")
    return path.replace("\\", "/"), first, last


def cite(spec: str, allow_unclassified: bool, plugin: str | None) -> dict:
    path, start, end = parse_evidence(spec)
    citation = dmlib.run_json(["cite", "--path", path, "--start", str(start), "--end", str(end)], plugin)
    if citation.get("source_kind") == "unclassified" and not allow_unclassified:
        raise SystemExit(
            f"{spec} 不在已確認來源（{CLASSIFIED_HINT}）內：這種證據之後無法升為 reviewed。"
            "請改引用已確認來源；確定只要候選時才加 --allow-unclassified。"
        )
    return citation


def parse_value(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def build(spec: dict, allow_unclassified: bool = False, plugin: str | None = None) -> dict:
    """spec：asset、id、evidence（字串陣列）、context（字串或陣列）與任意欄位。"""
    spec = dict(spec)
    asset = spec.pop("asset", None)
    if asset not in ASSETS:
        raise SystemExit(f"asset 必須是 {', '.join(ASSETS)} 之一，收到：{asset}")
    evidence = spec.pop("evidence", [])
    if isinstance(evidence, str):
        evidence = [evidence]
    if not evidence:
        raise SystemExit(f"{asset}:{spec.get('id')} 至少需要一個 --evidence 路徑:起-迄")
    context = spec.pop("context", None)
    record = {"id": spec.pop("id", None), **DEFAULTS.get(asset, {}), **spec}
    if context:
        contexts = [context] if isinstance(context, str) else list(context)
        if asset in MULTI_CONTEXT:
            record["contexts"] = contexts
        elif asset in SINGLE_CONTEXT:
            record[SINGLE_CONTEXT[asset]] = contexts[0]
    if not record["id"]:
        raise SystemExit("需要 --id")
    missing = [field for field in REQUIRED[asset] if not record.get(field)]
    if missing:
        raise SystemExit(f"{asset}:{record['id']} 缺少必要欄位：{', '.join(missing)}（用對應旗標或 --set 欄位=值）")
    record.pop("review_status" if asset == "decisions" else "status", None)  # decisions 的 status 是決策狀態
    record.pop("review", None)
    record["evidence"] = [cite(item, allow_unclassified, plugin) for item in evidence]
    return record


def save_and_upsert(asset: str, record: dict, out: Path, upsert: bool, plugin: str | None) -> None:
    dmlib.write_json(out, record)
    print(f"已寫出 {out}（{len(record['evidence'])} 個證據）")
    if upsert:
        done = dmlib.run(["upsert-candidate", "--asset", asset, "--record-file", str(out)], plugin)
        print(f"  upsert-candidate {asset}:{record['id']} → {done.stdout.strip() or 'OK'}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="以 cite 證據產生 Domain Registry record JSON（候選）。",
                                     epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--asset", choices=ASSETS, help="資產種類")
    parser.add_argument("--id", help="穩定 id，例如 pricing、FARE-005")
    parser.add_argument("--name", help="名稱")
    parser.add_argument("--definition", help="vocabulary 的定義")
    parser.add_argument("--statement", help="rules／decisions 的可否證敘述")
    parser.add_argument("--responsibility", help="contexts 的職責")
    parser.add_argument("--context", action="append", help="所屬 Context id，可重複")
    parser.add_argument("--evidence", action="append", default=[], help="路徑:起-迄，可重複，至少一個")
    parser.add_argument("--set", action="append", default=[], metavar="欄位=值", help="其他欄位，值可為 JSON")
    parser.add_argument("--batch", help="JSON 陣列檔，一次產生多筆")
    parser.add_argument("--out", help="輸出檔（單筆）；預設 records/<asset>-<id>.json")
    parser.add_argument("--out-dir", default="records", help="批次輸出資料夾（預設 records）")
    parser.add_argument("--upsert", action="store_true", help="寫檔後立即 upsert-candidate")
    parser.add_argument("--allow-unclassified", action="store_true", help="允許引用未分類來源（只能當候選）")
    parser.add_argument("--plugin", help="Plugin 資料夾（預設 DOMAIN_MEMORY_PLUGIN 或 vendor/domain-memory）")
    args = parser.parse_args(argv)
    if args.batch:
        specs = dmlib.read_json(args.batch)
    elif args.asset:
        spec = {"asset": args.asset, "id": args.id, "evidence": args.evidence, "context": args.context}
        for field in ("name", "definition", "statement", "responsibility"):
            if getattr(args, field):
                spec[field] = getattr(args, field)
        for item in args.set:
            key, sep, value = item.partition("=")
            if not sep:
                parser.error(f"--set 需要 欄位=值：{item}")
            spec[key] = parse_value(value)
        specs = [spec]
    else:
        parser.error("需要 --asset ... 或 --batch 檔案")
    for spec in specs:
        record = build(spec, args.allow_unclassified, args.plugin)
        out = Path(args.out) if args.out and not args.batch else Path(args.out_dir) / f"{spec['asset']}-{record['id']}.json"
        save_and_upsert(spec["asset"], record, out, args.upsert, args.plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
