"""Check whether a domain-memory plugin build still fits the DDD DLC, before changing the pin.

    uv run --no-project --python 3.13 python -X utf8 scripts/check_dlc_plugin_compat.py [--source <plugin dir or ZIP>]

--source defaults to the vendored ZIP. Export a SkillHub commit first, never a working tree:
    git -C <SkillHub> archive <commit> .claude/skills/domain-memory | tar -x -C <scratch>
    ... --source <scratch>/.claude/skills/domain-memory

Everything runs in a temp sandbox; the repo, the reference bundle and the private key are never written or used.
Checks: (1) plugin commands/flags vs dmlib and the commands learners run, (2) participant tools self-test,
(3) D1 replay (make_recovery.build_d1) plus the D1/D3 read commands, (4) reference Registry from the bundle:
validate, verify-evidence/sources/audit, verify-git-governance, Change Packages, export (OKF records), push through
the pre-push hook (existing signed history, no key needed), (5) every plugin string the Runbook, Recovery or
the deck quotes to learners. Prints PASS/CHANGED per item; exit 1 when anything CHANGED.
Inventory and upgrade plan: docs/planning/domain-memory-touchpoints.md.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DLC = ROOT / "agentic-workshop/07-dlc-ddd"
TOOLS = DLC / "participant/tools"
VENDOR_ZIP = DLC / "participant/vendor/domain-memory-4.2.0.zip"
REFERENCE = DLC / "evaluation/reference-registry"
sys.path[:0] = [str(TOOLS), str(DLC / "facilitator/recovery")]
import dmlib  # noqa: E402
import make_recovery  # noqa: E402

# Commands and flags learners (Runbook, Recovery, tools README) and our tools pass to the plugin.
LEARNER_COMMANDS = {
    "readiness": [], "quality-gates": [], "validate": ["--require-reviewed"], "coverage": [],
    "discover-sources": [], "verify-sources": ["--source-map", "--policy"], "verify-evidence": [],
    "init-domain-memory": ["--output", "--source", "--exclude", "--storage-mode", "--data-classification",
                           "--review-mode", "--source-authority"],
    "confirm-sources": ["--confirmed-by"], "cite": ["--path", "--lines"],
    "upsert-candidate": ["--asset", "--record-file"], "resolve-terms": ["--query"], "get-context": ["--id"],
    "get-record": ["--asset", "--id", "--changes-root"], "analyze-boundary": ["--source-context", "--target-context"],
    "counterfactual": ["--file", "--find", "--replace", "--test-command", "--expect"],
    "init-change-package": ["--output"], "validate-change-package": ["--package-root"],
    "submit-proposal": ["--package-root"], "record-approval": ["--package-root", "--role", "--reviewer", "--scope"],
    "verify-proposal": ["--package-root"], "ship-package": ["--package-root", "--commit"],
    "init-signing-key": ["--principal", "--key-file", "--sign-every-commit"],
    "brief": ["--base", "--markdown"], "install-pre-commit-hook": [],
    "amend-policy": ["--set", "--reason", "--verifier"], "install-git-hitl-hook": [],
    "governance-readiness": [], "verify-git-governance": ["--commit"], "verify-audit": [], "scan-secrets": [],
    "export": ["--commit"], "compare-registry": ["--gold-root", "--gold-commit", "--candidate-root"],
    # D2 checkpoint 4 rescue when the proposal base went stale (facilitator guide FAQ 19/24)
    "retract-candidate": [], "rebase-proposal": ["--package-root"],
}
# Plugin output the learner-facing text quotes or a ③ check waits for (inventory section 3).
QUOTED = [
    "Registry is valid.", "Change package is valid.", "Proposal submitted for human review.",
    "Proposal test evidence verified.", "Git governance is valid for 1 commit.", "That is reach, not an error.",
    "the tests do not pass before anything is broken", "Git commit signature is invalid", "not reviewed",
    '"status": "ready"', '"blocks": []', '"status": "valid"', "verdict", "killed", "survived", "inconclusive", "failure_evidence",
    "restoration_result", "restored", "matching --expect", "match_kind", "mentioned", "no_registered_collaboration",
    "current", "shifted", "stale", "discovered_but_gone", "developer-confirmed", "content_changed",
    "changed_sources", "confirmed_absences", "source_kind", "unclassified", "authorized_signers",
    "review_governance", "review_mode", "scm-verified", "git-signed-commit", "git-push", "fingerprint",
    '"state": "brownfield"', '"tool": "pytest"', '"confidence": "high"', "not_applicable",
    "proven_by", "also_covers", "copied_evidence", "copied_matches", "overall_independent",
    "failing_tests", "rule_totals", "rules_by_context", "reviewed_rules", "contexts_without_reviewed_rules",
    '"proven"', '"unproven"', '"unknown"',
    # 1.0: analyze-boundary per direction, ship-package, brief (D3b/D3c), rule aggregate (D3c), pre-commit hook (D4)
    "source_depends_on_target", "target_depends_on_source", "completed", "applied", "Attention",
    "lies outside every Context", "belongs to context", "which the record does not name",
    "Installed Domain Memory pre-commit hook", "is renamed to", "relocate-evidence --from",
    # 1.2: re-run verify-proposal (D2 checkpoint 4 ③); stale base and its remedy (facilitator guide)
    "nothing was written", "proposal base revision is stale; rebase-proposal",
    "approvals_retired",
    # AGENTS.md: amend-policy note that is normal before any proposal exists
    "every captured base revision is now stale and needs fresh approval",
    # 1.2.3/1.2.4: ship-package stops before attesting on a stale base; a current-base rebase is a note
    "the proposal base is stale; rebase-proposal", "the proposal base is current; nothing was written",
    # 1.2.9/1.2.10: why a stale base cannot be compared, and the git deadline (facilitator guide FAQ 19 and 20)
    "does not hold the Registry at", "does not reproduce the recorded base digest",
    "nothing was written, so it is safe to run again",
    "DOMAIN_MEMORY_GIT_TIMEOUT", "to a larger number of seconds to wait longer", "must be a positive number of seconds",
]
ATTESTED = ["5538b6dbcba9e5c4468ceddec72b75b231f9688d", "38116f248f78befa51abac56405349301a5623c7"]
REGISTRY_COMMITS = 7  # six JSON-era commits + the signed OKF migration (0.33.0)

results: list[tuple[str, str, str]] = []
transcript: list[str] = []


def report(ok: bool, item: str, detail: str = "") -> None:
    results.append(("PASS" if ok else "CHANGED", item, detail))
    print(f"[{'PASS' if ok else 'CHANGED'}] {item}" + (f": {detail}" if detail else ""), flush=True)


def sh(cmd: list[str], cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env={**dmlib.env(), **(env or {})})
    transcript.append(done.stdout + done.stderr)
    return done


def dm(repo: Path, plugin: Path, *args: str) -> subprocess.CompletedProcess:
    return sh([sys.executable, "-X", "utf8", str(TOOLS / "dmlib.py"), "--plugin", str(plugin), *args], repo)


def unpack(source: Path, sandbox: Path) -> Path:
    if source.is_file():
        with zipfile.ZipFile(source) as archive:
            archive.extractall(sandbox / "plugin")
        return sandbox / "plugin/domain-memory"
    shutil.copytree(source, sandbox / "plugin/domain-memory", ignore=shutil.ignore_patterns("__pycache__"))
    return sandbox / "plugin/domain-memory"


def parser_surface(plugin: Path) -> dict[str, dict[str, bool]]:
    """{command: {--flag: required}} read from the plugin's own argparse parser (in a child process)."""
    code = ("import argparse,json,sys;sys.path.insert(0,sys.argv[1]);"
            "from domain_registry.cli_parser import build_parser;p=build_parser();"
            "s=next(a for a in p._actions if isinstance(a,argparse._SubParsersAction));"
            "print(json.dumps({n:{o:a.required for a in sp._actions for o in a.option_strings if o.startswith('--')}"
            " for n,sp in s.choices.items()}))")
    done = subprocess.run([sys.executable, "-I", "-c", code, str(plugin / "scripts")], capture_output=True,
                          text=True, encoding="utf-8")
    if done.returncode:
        raise SystemExit(f"cannot read the plugin parser:\n{done.stderr}")
    return json.loads(done.stdout)


def check_commands(plugin: Path) -> None:
    cli = parser_surface(plugin)
    sets = {"REGISTRY_REQUIRED": ({c for c, o in cli.items() if o.get("--registry-root") is True},
                                  dmlib.REGISTRY_REQUIRED),
            "REGISTRY_OPTIONAL": ({c for c, o in cli.items() if o.get("--registry-root") is False},
                                  dmlib.REGISTRY_OPTIONAL),
            "REPO_ROOT": ({c for c, o in cli.items() if "--repo-root" in o}, dmlib.REPO_ROOT)}
    for name, (plugin_set, ours) in sets.items():
        extra, missing = sorted(plugin_set - ours), sorted(ours - plugin_set)
        report(not extra and not missing, f"dmlib.{name} vs cli_parser",
               f"plugin adds {extra}, plugin drops {missing}" if extra or missing else f"{len(ours)} commands")
    gone = [f"{c} {f}".strip() for c, flags in LEARNER_COMMANDS.items() for f in ([""] + flags)
            if c not in cli or (f and f not in cli[c])]
    report(not gone, "learner commands and flags exist", ", ".join(gone) or f"{len(LEARNER_COMMANDS)} commands")
    new = sorted(set(cli) - set(LEARNER_COMMANDS) - dmlib.REGISTRY_REQUIRED - dmlib.REGISTRY_OPTIONAL
                 - dmlib.REPO_ROOT - {"init", "redraft-proposal", "supersede-proposal", "validate-policy",
                                      "validate-contract", "verify-scm-attestation"})
    if new:
        print(f"[INFO] commands new to the DLC: {', '.join(new)}")


def check_tools(plugin: Path) -> None:
    done = sh([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(TOOLS), "-p", "test_*.py"],
              TOOLS, {"DOMAIN_MEMORY_PLUGIN": str(plugin), "PYTHONDONTWRITEBYTECODE": "1"})
    tail = (done.stdout + done.stderr).strip().splitlines()
    report(done.returncode == 0, "participant tools self-test", tail[-1] if tail else "")


def check_d1(plugin: Path, sandbox: Path) -> None:
    work, tmp = sandbox / "d1/smart-ticket-dlc-base", sandbox / "d1-tmp"
    tmp.mkdir(parents=True)
    try:
        make_recovery.build_d1(work, str(plugin), tmp)
    except SystemExit as error:
        report(False, "D1 replay (make_recovery.build_d1)", str(error)[-600:])
        return
    expected = len(dmlib.read_json(REFERENCE / "inputs/d1-records.json"))
    found = sum(len(doc.get(key, [])) for doc in run_in(work, dmlib.registry_documents, "domain-memory", str(plugin))
                .values() for key in doc if isinstance(doc.get(key), list))
    report(found == expected, "D1 replay (make_recovery.build_d1)", f"{found}/{expected} candidates via registry_documents")
    for args in (["validate"], ["verify-evidence"], ["verify-sources"], ["coverage"], ["readiness"],
                 ["quality-gates"], ["resolve-terms", "--query", "提前購票優惠"], ["get-context", "--id", "pricing"],
                 ["get-record", "--asset", "rules", "--id", "FARE-005"],
                 ["analyze-boundary", "--source-context", "pricing", "--target-context", "booking"]):
        done = dm(work, plugin, *args)
        report(done.returncode == 0, f"D1 {' '.join(args)}", "" if done.returncode == 0 else
               (done.stdout + done.stderr).strip()[-300:])


def run_in(cwd: Path, func, *args):
    old = Path.cwd()
    os.chdir(cwd)
    try:
        return func(*args)
    finally:
        os.chdir(old)


def check_reference(plugin: Path, sandbox: Path) -> None:
    repo = sandbox / "reference"
    sh(["git", "clone", "-q", "--no-checkout", str(REFERENCE / "smart-ticket-dlc-reference.bundle"), str(repo)],
       sandbox)
    for args in (["-c", "core.autocrlf=false", "checkout", "-q", "-B", "main", make_recovery.REVIEWED_TAG],
                 ["remote", "remove", "origin"], ["config", "--local", "gpg.format", "ssh"],
                 ["config", "--local", "gpg.ssh.allowedSignersFile",
                  str(REFERENCE / "keys/maintainer.allowed_signers")]):
        sh(["git", *args], repo)
    checks = [["validate", "--require-reviewed"], ["verify-evidence"], ["verify-sources"], ["verify-audit"],
              *(["verify-git-governance", "--commit", sha] for sha in ATTESTED),
              *(["validate-change-package", "--package-root", f"domain-memory/changes/CP-CORE-00{n}"] for n in (1, 2)),
              # 1.2.2: verify-proposal on an applied package is a harmless re-run (1.1.x packages unchanged).
              *(["verify-proposal", "--package-root", f"domain-memory/changes/CP-CORE-00{n}"] for n in (1, 2)),
              ["install-git-hitl-hook"], ["governance-readiness"]]
    for args in checks:
        done = dm(repo, plugin, *args)
        report(done.returncode == 0, f"reference {' '.join(args)}", "" if done.returncode == 0 else
               (done.stdout + done.stderr).strip()[-300:])
    # OKF bundle (0.29+ layout, 0.31 record shape): export lists every asset; reviewed records carry `verified`.
    exported = run_in(repo, dmlib.registry_documents, "domain-memory", str(plugin))
    records = [r for doc in exported.values() for v in doc.values() if isinstance(v, list) for r in v
               if isinstance(r, dict) and "id" in r]
    odd = [r["id"] for r in records if "review" in r or not r.get("verified")]
    report(sorted(exported) == sorted(dmlib.ASSETS) and records and not odd, "reference export (OKF records)",
           f"{len(exported)} assets, {len(records)} records" + (f"; review block or no verified: {odd}" if odd else ""))
    sh(["git", "init", "-q", "--bare", str(sandbox / "remote.git")], sandbox)
    path = os.pathsep.join([str(Path(sys.executable).parent), os.environ.get("PATH", "")])
    done = sh(["git", "push", "-u", str(sandbox / "remote.git"), "HEAD:main"], repo, {"PATH": path})
    # 0.58+: the hook verifies a push's Registry commits in one call and prints one line for them all.
    output = done.stdout + done.stderr
    expected = f"Git governance is valid for {REGISTRY_COMMITS} commits."
    lines = output.count("Git governance is valid")
    report(done.returncode == 0 and expected in output and lines == 1, "reference push through pre-push hook",
           f"{lines} governance line(s); expect one '{expected}'")
    # 1.0 (D4 checkpoint 3): the pre-commit hook refuses a commit that renames a cited file, then is undone.
    dm(repo, plugin, "install-pre-commit-hook")
    cited, moved = "src/smart_ticket/domain/discounts.py", "src/smart_ticket/domain/discount_rules.py"
    sh(["git", "mv", cited, moved], repo)
    done = sh(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-m", "rename"], repo,
              {"PATH": path})
    sh(["git", "mv", moved, cited], repo)
    output = done.stdout + done.stderr
    report(done.returncode != 0 and "relocate-evidence --from" in output, "reference pre-commit hook refuses a rename",
           "refused with the relocate-evidence hint" if done.returncode else "commit went through")


def check_quoted(plugin: Path) -> None:
    source = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (plugin / "scripts").rglob("*.py")
                       if not p.name.startswith("test_"))
    seen = "\n".join(transcript)
    missing = [q for q in QUOTED if q not in seen and q not in source]
    report(not missing, "learner-quoted plugin strings", f"missing: {missing}" if missing else
           f"{len(QUOTED)} strings ({sum(q in seen for q in QUOTED)} seen in this run's output)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=VENDOR_ZIP, help="plugin folder or ZIP (default: vendored)")
    parser.add_argument("--keep", action="store_true", help="keep the sandbox folder for inspection")
    args = parser.parse_args(argv)
    sandbox = Path(tempfile.mkdtemp(prefix="dlc-compat-"))
    try:
        plugin = unpack(args.source.resolve(), sandbox)
        version = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
        print(f"domain-memory {version} from {args.source}\nsandbox {sandbox}", flush=True)
        check_commands(plugin)
        check_tools(plugin)
        check_d1(plugin, sandbox)
        check_reference(plugin, sandbox)
        check_quoted(plugin)
    finally:
        if not args.keep:
            shutil.rmtree(sandbox, onexc=make_recovery._writable_retry)
    changed = [item for status, item, _ in results if status != "PASS"]
    print(f"\ndomain-memory {version}: {len(results) - len(changed)} PASS, {len(changed)} CHANGED"
          + (f" ({'; '.join(changed)})" if changed else ""))
    return 1 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
