"""從一份精簡描述 JSON 建立並填寫 Change Package（requirement／proposal／obligations／evidence）。

  py -3.13 -X utf8 ../../tools/fill_package.py package-spec.json

- 套件不存在時先執行 init-change-package；只會改寫 status 為 draft 的套件。
- 每條驗收條件（acceptance_criteria）與規則（rules）各產生一個 obligation（OB-<id>），
  並「實際執行」它的 test，記錄真實 exit code 與輸出 sha256；失敗就記 failed，絕不預填 passed。
- promote 列出要升為 reviewed 的既有候選（由 get-record 取出 Registry 裡的現行內容）。
- counterfactual.result_file 是 `dm counterfactual ... --save cf.json` 的輸出；verdict 必須是 killed 才算通過。
- 最後執行 validate-change-package 並印出結果。

描述檔鍵（* 為必填）：
  package*, requirement_id*, proposal_id*, proposer*, intent*, actor, observable_outcome,
  acceptance_criteria*: [{id, statement, test, expected, level}], rules: [{id, test, expected, level}],
  promote: {asset: [id...]}, owner_context*, invariant*, owner_evidence: ["路徑:起-迄"],
  interaction, consistency, prohibited_dependencies, boundary_evidence: ["路徑:起-迄"],
  design: {domain_forces, decision, invariants_preserved, rejected_alternatives, counterfactual_check},
  counterfactual: {obligation_id, result_file}, risk_flags, approval_roles, candidate_terms,
  open_questions, sources, residual_risks, affected_contexts
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402
from make_record import cite  # noqa: E402

FILES = ("requirement-normalization.json", "domain-change-proposal.json", "test-obligations.json",
         "evidence-bundle.json")
REQUIRED = ("package", "requirement_id", "proposal_id", "proposer", "intent", "acceptance_criteria", "owner_context",
            "invariant")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def default_test_command() -> str:
    venv = Path(".venv/Scripts/python.exe") if os.name == "nt" else Path(".venv/bin/python")
    if not venv.exists():
        raise SystemExit("找不到 .venv 的 Python；請先建立 .venv 並安裝依賴，或用 --test-command 指定。")
    return f"{venv} -m pytest -q"


def run_test(test_command: str, target: str) -> dict:
    """真的執行測試；回傳 exit code、輸出 sha256 與完成時間。"""
    command = f"{test_command} {target}" if os.name == "nt" else shlex.split(test_command) + shlex.split(target)
    try:
        done = subprocess.run(command, capture_output=True, env=dmlib.env())
    except OSError as error:
        raise SystemExit(f"無法執行測試指令「{test_command}」：{error}。請確認 .venv 已建立，或用 --test-command 指定。") from None
    return {"exit_code": done.returncode, "output_sha256": "sha256:" + hashlib.sha256(done.stdout).hexdigest(),
            "finished_at": now(), "evidence": f"{test_command} {target}",
            "tail": done.stdout.decode("utf-8", "replace")[-300:]}


def obligations_from(spec: dict) -> list[dict]:
    items = [("acceptance-criterion", item) for item in spec["acceptance_criteria"]]
    items += [("rule", item) for item in spec.get("rules", [])]
    obligations = []
    for source_type, item in items:
        if not item.get("test"):
            raise SystemExit(f"{item['id']} 缺少 test（要執行的測試路徑或 node id）")
        obligations.append({"id": f"OB-{item['id']}", "source_type": source_type, "source_id": item["id"],
                            "expected_outcome": item.get("expected") or item.get("statement") or item["id"],
                            "level": item.get("level", "integration"), "status": "executed",
                            "check": item["test"]})
    return obligations


def promoted_updates(spec: dict, plugin: str | None) -> list[dict]:
    updates = []
    for asset, ids in spec.get("promote", {}).items():
        for record_id in ids:
            record = dmlib.run_json(["get-record", "--asset", asset, "--id", record_id], plugin)
            record.pop("status", None)
            record.pop("review", None)
            record.pop("review_status", None)
            updates.append({"asset": asset, "operation": "upsert", "record": record})
    return updates


def counterfactual_evidence(spec: dict) -> dict | None:
    config = spec.get("counterfactual")
    if not config:
        return None
    result = dmlib.read_json(config["result_file"])
    mutated = result.get("mutated_protection", {})
    killed = result.get("verdict") == "killed"
    if not killed:
        print(f"注意：counterfactual verdict 是 {result.get('verdict')}，不是 killed，記為 failed。")
    elif not result.get("failing_evidence"):
        print("注意：counterfactual 沒有失敗輸出（failing_evidence 空白），verify-proposal 會拒絕；請讓測試印出斷言失敗。")
    return {"status": "passed" if killed else "failed", "obligation_id": config["obligation_id"],
            "mutated_protection": f"{result.get('file')}:{result.get('line')} "
                                  f"{mutated.get('from')} -> {mutated.get('to')}",
            "failure_evidence": (result.get("failing_evidence") or "")[-600:],
            "restored": bool((result.get("restoration_result") or {}).get("restored"))}


def fill(spec: dict, test_command: str, plugin: str | None = None, run_tests: bool = True) -> list[dict]:
    missing = [key for key in REQUIRED if not spec.get(key)]
    if missing:
        raise SystemExit(f"描述檔缺少必填鍵：{', '.join(missing)}（見 --help）")
    package = Path(spec["package"])
    if not package.exists():
        dmlib.run(["init-change-package", "--output", str(package)], plugin)
        print(f"已建立 {package}")
    proposal_file = package / "domain-change-proposal.json"
    current = dmlib.read_json(proposal_file)
    if current.get("status") != "draft":
        raise SystemExit(f"{proposal_file} 狀態是 {current.get('status')}，只有 draft 能重新填寫。")
    docs = {name: dmlib.read_json(package / name) for name in FILES}
    req_id, prop_id = spec["requirement_id"], spec["proposal_id"]
    flags = spec.get("risk_flags", [])
    sources = spec.get("sources", [])
    obligations = obligations_from(spec)
    updates = promoted_updates(spec, plugin)
    rule_ids = [item["id"] for item in spec.get("rules", [])]
    contexts = spec.get("affected_contexts") or sorted(
        {spec["owner_context"]} | {u["record"]["id"] for u in updates if u["asset"] == "contexts"})
    owner_evidence = [cite(item, False, plugin) for item in spec.get("owner_evidence", [])]
    boundary_evidence = [cite(item, False, plugin) for item in spec.get("boundary_evidence", [])]
    design = spec.get("design", {})
    docs["requirement-normalization.json"].update({
        "requirement_id": req_id, "intent": spec["intent"], "actor": spec.get("actor", "unknown"),
        "observable_outcome": spec.get("observable_outcome", spec["intent"]),
        "acceptance_criteria": [{"id": a["id"], "statement": a["statement"]} for a in spec["acceptance_criteria"]],
        "candidate_terms": spec.get("candidate_terms", []), "open_questions": spec.get("open_questions", []),
        "risk_flags": flags, "required_approval_roles": spec.get("approval_roles", ["domain-owner"]),
        "sources": sources})
    docs["domain-change-proposal.json"].update({
        "proposal_id": prop_id, "proposer": spec["proposer"], "requirement_id": req_id,
        "affected_contexts": contexts, "rule_ids": rule_ids, "contract_ids": spec.get("contract_ids", []),
        "ownership_decision": {"owner_context": spec["owner_context"], "invariant": spec["invariant"],
                               "evidence": owner_evidence},
        "boundary_decision": {"interaction": spec.get("interaction", "none"),
                              "consistency": spec.get("consistency", "synchronous"),
                              "prohibited_dependencies": spec.get("prohibited_dependencies", []),
                              "evidence": boundary_evidence},
        "implementation_design": {
            "domain_forces": design.get("domain_forces", []), "decision": design.get("decision", ""),
            "invariants_preserved": design.get("invariants_preserved", []),
            "rejected_alternatives": design.get("rejected_alternatives", []),
            "proof_obligations": [o["id"] for o in obligations],
            "counterfactual_check": design.get("counterfactual_check", "")},
        "registry_updates": updates, "risk_flags": flags, "open_questions": spec.get("open_questions", []),
        "approvals": []})
    docs["test-obligations.json"].update({"requirement_id": req_id, "proposal_id": prop_id,
                                          "obligations": obligations})
    results = []
    if run_tests:
        for obligation in obligations:
            outcome = run_test(test_command, obligation["check"])
            status = "passed" if outcome["exit_code"] == 0 else "failed"
            print(f"  {obligation['id']}: {status}（exit {outcome['exit_code']}）{obligation['check']}")
            if status == "failed":
                print("    " + outcome["tail"].strip().replace("\n", "\n    "))
            results.append({"obligation_id": obligation["id"], "status": status, "evidence": outcome["evidence"],
                            "command_profile": "pytest-local", "exit_code": outcome["exit_code"],
                            "output_sha256": outcome["output_sha256"], "finished_at": outcome["finished_at"]})
    docs["evidence-bundle.json"].update({
        "requirement_id": req_id, "proposal_id": prop_id, "approvals": [], "scm_attestation": None,
        "counterfactual_check": counterfactual_evidence(spec), "sources": sources, "test_results": results,
        "residual_risks": spec.get("residual_risks", [])})
    for name, data in docs.items():
        dmlib.write_json(package / name, data)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="建立並填寫 Change Package，測試結果來自實際執行。",
                                     epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec", help="精簡描述 JSON 檔")
    parser.add_argument("--test-command", help=r"測試指令前綴；預設 .venv\Scripts\python.exe -m pytest -q")
    parser.add_argument("--no-run", action="store_true", help="只填文件、不執行測試（test_results 留空）")
    parser.add_argument("--plugin", help="Plugin 資料夾（預設 DOMAIN_MEMORY_PLUGIN 或 vendor/domain-memory）")
    args = parser.parse_args(argv)
    spec = dmlib.read_json(args.spec)
    test_command = args.test_command or ("" if args.no_run else default_test_command())
    results = fill(spec, test_command, args.plugin, not args.no_run)
    check = dmlib.run(["validate-change-package", "--package-root", spec["package"]], args.plugin, check=False)
    print(check.stdout.strip(), check.stderr.strip())
    failed = [r["obligation_id"] for r in results if r["status"] != "passed"]
    if failed:
        print(f"有 obligation 未通過：{', '.join(failed)}。修正後重跑本指令。")
    return 1 if failed or check.returncode else 0


if __name__ == "__main__":
    raise SystemExit(main())
