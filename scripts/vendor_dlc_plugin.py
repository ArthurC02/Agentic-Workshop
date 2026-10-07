"""Vendor the domain-memory plugin into the DLC participant tree as a deterministic ZIP.

Usage:
    py -3.13 -X utf8 scripts/vendor_dlc_plugin.py [--source <plugin dir>] [--check]

Writes agentic-workshop/07-dlc-ddd/participant/vendor/domain-memory-<version>.zip (top folder
domain-memory/, caches excluded, sorted members, fixed timestamps) and <zip>.SHA256SUMS with one
line per member file plus a final line for the ZIP itself (sha256sum format).
--check rebuilds in memory and exits 1 when the vendored files differ.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("C:/Users/a8022/Desktop/SkillHub/.claude/skills/domain-memory")
VENDOR = ROOT / "agentic-workshop/07-dlc-ddd/participant/vendor"
EXCLUDED_DIRS = {".pytest_cache", ".ruff_cache", "__pycache__", ".git", ".venv"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
TOP = "domain-memory"


def plugin_files(source: Path) -> list[tuple[str, bytes]]:
    files = []
    for path in source.rglob("*"):
        rel = path.relative_to(source)
        if path.is_dir() or EXCLUDED_DIRS & set(rel.parts) or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink not allowed in vendored plugin: {rel.as_posix()}")
        files.append((f"{TOP}/{rel.as_posix()}", path.read_bytes()))
    return sorted(files)


def build(source: Path) -> tuple[str, bytes, bytes]:
    """Return (zip name, zip bytes, SHA256SUMS bytes)."""
    version = json.loads((source / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    files = plugin_files(source)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    data = buffer.getvalue()
    name = f"domain-memory-{version}.zip"
    lines = [f"{hashlib.sha256(body).hexdigest()}  {member}" for member, body in files]
    lines.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
    return name, data, ("\n".join(lines) + "\n").encode("utf-8")


def verify(zip_path: Path) -> list[str]:
    """Check a vendored ZIP against its SHA256SUMS (whole ZIP and every member, no extras)."""
    sums_path = zip_path.with_name(zip_path.name + ".SHA256SUMS")
    expected = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        sha, name = line.split("  ", 1)
        expected[name] = sha
    data = zip_path.read_bytes()
    problems = []
    if expected.pop(zip_path.name, None) != hashlib.sha256(data).hexdigest():
        problems.append(f"{zip_path.name}: whole-ZIP SHA256 mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        actual = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
    for name in sorted(set(expected) | set(actual)):
        if expected.get(name) != actual.get(name):
            problems.append(f"{name}: member SHA256 mismatch or missing")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    name, data, sums = build(args.source)
    zip_path, sums_path = VENDOR / name, VENDOR / (name + ".SHA256SUMS")
    if args.check:
        same = zip_path.exists() and zip_path.read_bytes() == data and sums_path.read_bytes() == sums
        print(("UP-TO-DATE " if same else "STALE ") + zip_path.relative_to(ROOT).as_posix())
        return 0 if same else 1
    VENDOR.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(data)
    sums_path.write_bytes(sums)
    print(json.dumps({"zip": zip_path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
                      "members": sums.count(b"\n") - 1}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
