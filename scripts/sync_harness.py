"""Mirror the canonical Claude Code harness to the Codex harness, byte for byte.

.claude/skills/**                 -> .agents/skills/**   (extra files in the mirror are deleted)
.claude/hooks/guard_generated.py  -> .codex/hooks/guard_generated.py
A mirror whose top folder (.agents/ or .codex/) does not exist in this clone is skipped.
Run: python -X utf8 scripts/sync_harness.py [--check]   (--check: report drift, exit 1, change nothing)
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [(".claude/skills", ".agents/skills"),
         (".claude/hooks/guard_generated.py", ".codex/hooks/guard_generated.py")]


def drift(root: Path = ROOT) -> list[tuple[str, Path, Path | None]]:
    """(action, target, source) for every file that differs: copy (missing or different) or delete (extra)."""
    out = []
    for src, dst in PAIRS:
        s, d = root / src, root / dst
        if not (root / dst.split("/")[0]).is_dir():
            continue
        want = {f.relative_to(s): f for f in s.rglob("*") if f.is_file()} if s.is_dir() else {Path(): s}
        have = {f.relative_to(d) for f in d.rglob("*") if f.is_file()} if d.is_dir() else set()
        for rel, f in sorted(want.items()):
            t = d / rel
            if not t.is_file() or t.read_bytes() != f.read_bytes():
                out.append(("copy", t, f))
        out += [("delete", d / rel, None) for rel in sorted(have - want.keys())]
    return out


def main(argv: list[str], root: Path = ROOT) -> int:
    actions = drift(root)
    for action, target, source in actions:
        print(f"{'DRIFT ' if '--check' in argv else ''}{action} {target.relative_to(root).as_posix()}")
        if "--check" in argv:
            continue
        if source:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        else:
            target.unlink()
    if "--check" in argv and actions:
        print("harness mirror drifted: run scripts/sync_harness.py")
        return 1
    print("HARNESS IN SYNC" if "--check" in argv or not actions else "HARNESS SYNCED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
