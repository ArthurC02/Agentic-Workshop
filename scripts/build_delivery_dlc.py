"""Build and verify the DDD DLC candidate from scripts/package-manifest-dlc.json.

Usage:
    py -3.13 -X utf8 scripts/build_delivery_dlc.py --pin              # re-enumerate declared sources into files[]
    py -3.13 -X utf8 scripts/build_delivery_dlc.py [--allow-missing]  # build dist/dlc-candidate/<manifest sha16>/
    py -3.13 -X utf8 scripts/build_delivery_dlc.py --verify <dir>     # inspect an existing candidate

Same manifest schema as package-manifest.json plus one key per package: "sources" (glob patterns relative
to the repo root) and optional "destination_root" {"from", "to"} (recovery packages). The build fails when
a declared source matches nothing; --allow-missing (dev only) skips those sources with a warning, and a
package left without files is skipped and listed under "missing_packages" in build-evidence.json.
Pinned files must equal what the sources enumerate (no unpinned additions, no vanished files, no drift).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
import zlib
from pathlib import Path
from urllib.parse import unquote

from build_delivery import ROOT, digest, link_check, safe_path

MANIFEST = ROOT / "scripts/package-manifest-dlc.json"
OUT_ROOT = ROOT / "dist/dlc-candidate"
DLC = "agentic-workshop/07-dlc-ddd"
VENDOR_ZIP = f"{DLC}/participant/vendor/domain-memory-0.10.15.zip"
RECOVERY_ROOT = f"{DLC}/facilitator/recovery"
RELEASES = {
    "participant-dlc-open": ("participant", 0), "participant-dlc-d1": ("participant", 10),
    "participant-dlc-d2": ("participant", 35), "participant-dlc-d3a": ("participant", 70),
    "participant-dlc-d3b": ("participant", 95), "participant-dlc-d3c": ("participant", 125),
    "participant-dlc-d4": ("participant", 155),
    # Recovery packages are participant-role downloads (build_materials.Candidate requires it), released
    # only through their own dlc-rec-* unlock group at these minutes (spec 3.2).
    "recovery-dlc-d1": ("participant", 35), "recovery-dlc-d2": ("participant", 45),
    "recovery-dlc-d3a": ("participant", 95), "recovery-dlc-d3b": ("participant", 125),
    "recovery-dlc-d3c": ("participant", 155),
    "facilitator-dlc-before-session": ("facilitator", -1), "evaluation-dlc-private": ("evaluation", -1)}
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".dlc-keys"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
# Path segments (case-insensitive substring) that must never reach a participant or recovery package.
PRIVATE_SEGMENTS = ("facilitator", "evaluation", "instructions", "reference-registry", "reference-solution",
                    "rubric", "observation")
PRIVATE_KEY = re.compile(rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def is_recovery(package_id: str) -> bool:
    return package_id.startswith("recovery-dlc-")


def enumerate_sources(package: dict) -> tuple[list[str], list[str]]:
    """Return (sorted repo-relative files, patterns that matched nothing). Caches/venvs are never listed."""
    found, missing = set(), []
    for pattern in package["sources"]:
        hits = [p for p in ROOT.glob(pattern) if p.is_file()
                and not EXCLUDED_DIRS & set(p.relative_to(ROOT).parts) and p.suffix not in EXCLUDED_SUFFIXES]
        if not hits:
            missing.append(pattern)
        found.update(p.relative_to(ROOT).as_posix() for p in hits)
    return sorted(found), missing


def destination(package: dict, source: str) -> str:
    mapping = package.get("destination_root")
    if mapping:
        prefix = mapping["from"].rstrip("/") + "/"
        if not source.startswith(prefix):
            raise ValueError(f"Source outside destination_root: {source}")
        return mapping["to"].rstrip("/") + "/" + source[len(prefix):]
    return source


def pin() -> dict:
    """Rewrite files[] from the declared sources. Review the manifest diff before building."""
    manifest = json.loads(MANIFEST.read_bytes())
    report = {}
    for package in manifest["packages"]:
        files, missing = enumerate_sources(package)
        package["files"] = [{"source": s, "destination": destination(package, s),
                             "sha256": digest((ROOT / s).read_bytes())} for s in files]
        report[package["id"]] = {"files": len(files), "missing_sources": missing}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"manifest_sha256": digest(MANIFEST.read_bytes()), "packages": report}


def path_policy(package: dict, name: str) -> None:
    """Role/content rules on a packaged path (also applied to members of nested ZIPs)."""
    parts = safe_path(name).parts
    if EXCLUDED_DIRS & set(parts) or Path(name).suffix in EXCLUDED_SUFFIXES:
        raise ValueError(f"Cache/venv/key material in package: {name}")
    if package["role"] == "participant" and any(m in part.lower() for part in parts for m in PRIVATE_SEGMENTS):
        raise ValueError(f"Role violation: {name}")


def content_policy(package: dict, contents: dict[str, bytes]) -> None:
    for name, data in contents.items():
        path_policy(package, name)
        if PRIVATE_KEY.search(data):
            raise ValueError(f"Private key material: {name}")
        if name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as nested:
                content_policy(package, {f"{name}!/{n}": nested.read(n) for n in nested.namelist()})


def source_policy(package: dict, source: str) -> None:
    parts = safe_path(source).parts
    if package["role"] != "participant":
        return
    if is_recovery(package["id"]):
        segment = package["id"].removeprefix("recovery-dlc-")
        if not source.startswith(f"{RECOVERY_ROOT}/{segment}/"):
            raise ValueError(f"Unapproved recovery source: {source}")
    elif "participant" not in parts:
        raise ValueError(f"Unapproved participant source: {source}")


def vendor_check(contents: dict[str, bytes]) -> bool:
    """The vendored plugin ZIP must match its SHA256SUMS (whole ZIP and every member)."""
    if VENDOR_ZIP not in contents:
        return False
    sums = contents.get(VENDOR_ZIP + ".SHA256SUMS")
    if sums is None:
        raise ValueError("Vendored plugin ZIP without SHA256SUMS")
    expected = dict(reversed(line.split("  ", 1)) for line in sums.decode("utf-8").splitlines())
    data = contents[VENDOR_ZIP]
    if expected.pop(Path(VENDOR_ZIP).name, None) != digest(data):
        raise ValueError("Vendored plugin ZIP SHA256 mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        actual = {n: digest(archive.read(n)) for n in archive.namelist()}
    if actual != expected:
        raise ValueError("Vendored plugin members differ from SHA256SUMS")
    return True


def prepare(package: dict, allow_missing: bool) -> tuple[dict[str, bytes] | None, list[str]]:
    if RELEASES.get(package.get("id")) != (package.get("role"), package.get("release_minute")):
        raise ValueError(f"Unknown package identity, role or release minute: {package.get('id')}")
    files, missing = enumerate_sources(package)
    if missing and not allow_missing:
        raise ValueError(f"Missing sources for {package['id']}: {missing} (use --allow-missing for an interim build)")
    pinned = [e["source"] for e in package["files"]]
    if sorted(pinned) != files:
        extra, gone = sorted(set(files) - set(pinned)), sorted(set(pinned) - set(files))
        raise ValueError(f"{package['id']}: sources differ from pinned files[] (unpinned {extra}, vanished {gone}); "
                         "review and run --pin")
    contents = {}
    for entry in package["files"]:
        source_policy(package, entry["source"])
        data = (ROOT / safe_path(entry["source"])).read_bytes()
        if digest(data) != entry["sha256"]:
            raise ValueError(f"Source drift: {entry['source']}")
        dest = safe_path(entry["destination"]).as_posix()
        if dest != destination(package, entry["source"]) or dest in contents:
            raise ValueError(f"Bad or duplicate destination: {dest}")
        contents[dest] = data
    for name, body in package.get("generated", {}).items():
        name = safe_path(name).as_posix()  # normalize first so "./x" cannot overwrite a pinned file
        if name in contents:
            raise ValueError(f"Generated destination collision: {name}")
        contents[name] = body.encode("utf-8")
    if not contents:
        return None, missing
    content_policy(package, contents)
    if package["id"] == "participant-dlc-open" and not vendor_check(contents) and not allow_missing:
        raise ValueError("participant-dlc-open lacks the vendored plugin ZIP")
    return contents, missing


def dlc_link_check(contents: dict[str, bytes]) -> int:
    """build_delivery.link_check, but a link to a directory is fine when the package ships files under it."""
    files = dict(contents)
    for name, data in contents.items():
        if name.endswith(".md"):
            for target in re.findall(r"\]\(([^)]+)\)", data.decode("utf-8")):
                target = unquote(target.split("#", 1)[0].strip("<>"))
                if target.endswith("/") and not re.match(r"[a-z]+:", target):
                    folder = (ROOT / name).parent.joinpath(target).resolve().relative_to(ROOT).as_posix() + "/"
                    if any(n.startswith(folder) for n in contents):
                        files[folder.rstrip("/")] = b""  # resolved key of the directory link
    return link_check(files)


def write_zip(path: Path, contents: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            # Unix host + exec bit on .sh so macOS unzip keeps dm.sh runnable.
            info.create_system = 3
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, data)


def build(allow_missing: bool = False, out_root: Path | None = None) -> dict:
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    run = (out_root or OUT_ROOT) / digest(raw)[:16]
    if {p["id"] for p in manifest["packages"]} != set(RELEASES) or len(manifest["packages"]) != len(RELEASES):
        raise ValueError("Package set differs from the DLC release plan")
    prepared, skipped, warnings = [], [], []
    for package in manifest["packages"]:
        contents, missing = prepare(package, allow_missing)
        warnings += [f"WARNING {package['id']}: missing source {m}" for m in missing]
        if contents is None:
            skipped.append(package["id"])
            continue
        links = dlc_link_check(contents) if package["role"] == "participant" else None
        metadata = {"id": package["id"], "role": package["role"], "release_minute": package["release_minute"],
                    "source_version": package.get("source_version"), "source_commit": package.get("source_commit"),
                    "files": {n: digest(d) for n, d in sorted(contents.items())}, "participant_relative_links": links,
                    "status": "CANDIDATE; human rehearsal and release approval pending"}
        contents["PACKAGE-MANIFEST.json"] = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        prepared.append((package, contents, metadata))
    for line in warnings:
        print(line, file=sys.stderr)
    run.mkdir(parents=True, exist_ok=False)  # validate everything first; never overwrite a candidate
    results = []
    for package, contents, metadata in prepared:
        target = run / (package["id"] + ".zip")
        write_zip(target, contents)
        results.append({**metadata, "zip": target.relative_to(ROOT).as_posix() if target.is_relative_to(ROOT)
                        else target.as_posix(), "zip_sha256": digest(target.read_bytes()),
                        "zip_bytes": target.stat().st_size})
    evidence = {"manifest_sha256": digest(raw), "output": run.relative_to(ROOT).as_posix() if run.is_relative_to(ROOT)
                else run.as_posix(), "python": sys.version.split()[0], "zlib": zlib.ZLIB_VERSION,
                "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION, "allow_missing": allow_missing,
                "missing_packages": skipped, "warnings": warnings, "packages": results}
    (run / "build-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verify(run)
    return evidence


def verify(run: Path) -> dict:
    """Inspect actual ZIP bytes of a candidate against its evidence and the DLC policies."""
    raw = MANIFEST.read_bytes()
    evidence = json.loads((run / "build-evidence.json").read_text(encoding="utf-8"))
    if evidence["manifest_sha256"] != digest(raw) or run.name != digest(raw)[:16]:
        raise ValueError("Candidate was not built from the current DLC manifest")
    listed = {p["id"] for p in evidence["packages"]}
    if listed | set(evidence["missing_packages"]) != set(RELEASES) or listed & set(evidence["missing_packages"]):
        raise ValueError("Evidence package set differs from the DLC release plan")
    for package in evidence["packages"]:
        if RELEASES[package["id"]] != (package["role"], package["release_minute"]):
            raise ValueError(f"Role/minute mismatch: {package['id']}")
        data = (run / (package["id"] + ".zip")).read_bytes()
        if digest(data) != package["zip_sha256"]:
            raise ValueError(f"ZIP SHA256 differs from evidence: {package['id']}")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = archive.infolist()
            names = [i.filename for i in infos]
            if names != sorted(names) or len(names) != len(set(names)) or any(i.date_time != ZIP_TIME for i in infos):
                raise ValueError(f"Non-deterministic or duplicate ZIP members: {package['id']}")
            payload = {safe_path(n).as_posix(): archive.read(n) for n in names}
        meta = json.loads(payload.pop("PACKAGE-MANIFEST.json"))
        inventory = {n: digest(d) for n, d in payload.items()}
        if inventory != meta["files"] or inventory != package["files"]:
            raise ValueError(f"ZIP membership or hashes differ from evidence: {package['id']}")
        content_policy(package, payload)
        if package["id"] == "participant-dlc-open" and not vendor_check(payload) and not evidence["allow_missing"]:
            raise ValueError("participant-dlc-open lacks the vendored plugin ZIP")
    return {"output": run.as_posix(), "verified": sorted(listed), "missing": evidence["missing_packages"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pin", action="store_true", help="re-enumerate declared sources into files[]")
    parser.add_argument("--allow-missing", action="store_true", help="dev only: skip missing sources with a warning")
    parser.add_argument("--verify", type=Path, metavar="DIR", help="verify an existing candidate directory")
    args = parser.parse_args()
    try:
        if args.pin:
            result = pin()
        elif args.verify:
            result = verify(args.verify.resolve())
        else:
            evidence = build(args.allow_missing)
            result = {"output": evidence["output"], "packages": len(evidence["packages"]),
                      "missing_packages": evidence["missing_packages"]}
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
