"""PreToolUse hook (Claude Code Edit|Write, Codex apply_patch): block hand edits to generated files.

Exit 2 + stderr blocks the edit and tells the agent which source or script to use instead.
Canonical copy: .claude/hooks/; scripts/sync_harness.py mirrors it to .codex/hooks/.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = "agentic-workshop/06-runbook/evaluation/"
GENERATED = [  # (regex on the repo-relative path, what to do instead)
    (r"agentic-workshop/materials(-dlc)?/participant-runbook/runbook\.html",
     "edit participant-runbook/content/*.md or template/, then run release-materials"),
    (r"agentic-workshop/materials(-dlc)?/facilitator-deck/facilitator-deck\.html",
     "edit facilitator-deck/src/, then run release-materials"),
    (r"agentic-workshop/materials/speech/01-greenfield/greenfield-(deck\.html|handout\.md)",
     "edit speech/01-greenfield/src/slides.json, then run release-materials"),
    (r"dist/.*", "dist/ is build output; run release-materials"),
    (re.escape(EVAL) + r"(p11-(validation|static-validation|package-validation|runtime-baseline)-evidence\.json"
     r"|p11-validation-logs/.*|consistency-(correction|package-validation)-evidence\.json)",
     "validation evidence is written by scripts/ (validate_workshop, verify_delivery, verify_runtime_baselines, "
     "validate_consistency_corrections); fix the source and rerun"),
]
PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.M)


def targets(tool_input: dict) -> list[str]:
    paths = [tool_input.get("file_path") or tool_input.get("path") or ""]
    for value in tool_input.values():  # Codex apply_patch carries the patch text instead of a path
        if isinstance(value, str):
            paths += PATCH_FILE.findall(value)
    return [p.strip() for p in paths if p.strip()]


def relative(path: str) -> str:
    p = Path(path)
    p = (p if p.is_absolute() else ROOT / p).resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return path.replace("\\", "/")


def blocked(tool_input: dict) -> list[str]:
    return [f"{rel} is generated: {why}." for rel in map(relative, targets(tool_input))
            for pattern, why in GENERATED if re.fullmatch(pattern, rel)]


if __name__ == "__main__":
    hits = blocked(json.loads(sys.stdin.buffer.read().decode("utf-8-sig")).get("tool_input") or {})  # BOM: PowerShell pipes
    if hits:
        print("\n".join(hits), file=sys.stderr)
        sys.exit(2)
