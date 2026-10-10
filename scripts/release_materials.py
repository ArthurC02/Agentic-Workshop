"""Rebuild candidates and materials in the order docs/instructions/08 (2026-10-08 adjustment) requires.

Run with Python 3.13 from anywhere:  uv run --no-project --python 3.13 python -X utf8 scripts/release_materials.py
Only validates/repins when manifest sources drifted, so an unchanged repo keeps its candidate IDs.
Exits non-zero at the first failing step; nothing is committed.
"""
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = [sys.executable, "-X", "utf8"]
MANIFEST = ROOT / "scripts/package-manifest.json"
from validate_workshop import VERSIONS  # noqa: E402  (scripts/ is on sys.path when run as a script)
VERSION_ROOTS = tuple("agentic-workshop/" + v[0] + "/" for v in VERSIONS.values())
DELIVERY_EVIDENCE = "agentic-workshop/06-runbook/evaluation/consistency-package-validation-evidence.json"


def run(*args, capture=False):
    print("$", " ".join(str(a) for a in args), flush=True)
    result = subprocess.run([*PY, *args], cwd=ROOT, text=True, encoding="utf-8",
                            capture_output=capture)
    if result.returncode:
        if capture:
            print(result.stdout[-3000:], result.stderr[-3000:])
        sys.exit(f"FAILED: {' '.join(str(a) for a in args)}")
    return result.stdout if capture else ""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def drifted() -> list[str]:
    manifest = json.loads(MANIFEST.read_bytes())
    return [e["source"] for p in manifest["packages"] for e in p["files"]
            if sha((ROOT / e["source"]).read_bytes()) != e["sha256"]]


def set_candidate_id(new: str) -> None:
    for name in ("scripts/build_materials.py", "scripts/test_materials_md.py"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r'(CANDIDATE_ID = "|"p11-candidate" / ")[0-9a-f]{16}"', rf'\g<1>{new}"', text),
                        encoding="utf-8")


def main_candidate() -> str:
    changed = drifted()
    if changed:
        full = any(s.startswith(VERSION_ROOTS) for s in changed)
        print(f"{len(changed)} manifest sources drifted; {'full' if full else 'static'} validation first")
        run("scripts/validate_workshop.py", *([] if full else ["--static-only"]))
        run("scripts/build_delivery.py", "--repin-reviewed-sources",
            "--expect-manifest-sha256", sha(MANIFEST.read_bytes()), capture=True)
    new_id = sha(MANIFEST.read_bytes())[:16]
    out = ROOT / "dist/p11-candidate" / new_id
    if not out.exists():
        run("scripts/build_delivery.py")
        try:  # verify snapshots scripts/ into the candidate, so it only runs on a fresh build
            run("scripts/verify_delivery.py", f"dist/p11-candidate/{new_id}", "--evidence", DELIVERY_EVIDENCE)
        except SystemExit:
            remove_tree(out)  # an unverified candidate must not be reused by the next run
            raise
    set_candidate_id(new_id)
    print("main candidate", new_id)
    return new_id


def dlc_candidate() -> str:
    run("scripts/build_delivery_dlc.py", "--pin", capture=True)
    new_id = sha((ROOT / "scripts/package-manifest-dlc.json").read_bytes())[:16]
    if not (ROOT / "dist/dlc-candidate" / new_id).exists():
        run("scripts/build_delivery_dlc.py", capture=True)
    run("scripts/build_delivery_dlc.py", "--verify", f"dist/dlc-candidate/{new_id}", capture=True)
    edition = ROOT / "agentic-workshop/materials-dlc/edition.json"
    text = edition.read_text(encoding="utf-8")
    edition.write_text(re.sub(r'("candidate_id": ")[0-9a-f]{16}"', rf'\g<1>{new_id}"', text), encoding="utf-8")
    print("dlc candidate", new_id)
    return new_id


def remove_tree(path: Path) -> None:
    # Packaged files are read-only on Windows; clear the bit and retry.
    shutil.rmtree(path, onexc=lambda fn, p, _: (os.chmod(p, stat.S_IWRITE), fn(p)))


def prune(kind: str, keep: str) -> None:
    """Delete superseded candidate directories under dist/ (gitignored build output)."""
    for old in (ROOT / "dist" / kind).iterdir():
        if old.is_dir() and old.name != keep:
            remove_tree(old)
            print("pruned", f"dist/{kind}/{old.name}")


def main() -> None:
    run("scripts/check_references.py")  # every knowledge point cites a verified source
    run("scripts/check_zh_tw.py")  # Taiwan Traditional Chinese characters and vocabulary
    run("scripts/check_blocks.py")  # every checkpoint uses the four blocks ①②③(④)
    main_id = main_candidate()
    dlc_id = dlc_candidate()
    for edition in ("main", "dlc"):
        run("scripts/build_materials.py", "--edition", edition)
        run("scripts/build_materials.py", "--edition", edition, "--check")
        run("scripts/package_materials.py", *([] if edition == "main" else ["dlc"]))
    speech = "agentic-workshop/materials/speech/"
    run(speech + "build_decks.py")
    run(speech + "build_decks.py", "--check")
    run(speech + "verify_browser.py", capture=True)
    run("-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py")
    left = drifted()
    if left:
        sys.exit(f"FAILED: manifest still drifts after rebuild: {left[:5]}")
    prune("p11-candidate", main_id)
    prune("dlc-candidate", dlc_id)
    print("RELEASE PIPELINE PASS")


if __name__ == "__main__":
    main()
