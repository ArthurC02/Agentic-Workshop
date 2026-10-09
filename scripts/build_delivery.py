"""Build role/time isolated workshop candidates from an explicit, hash-pinned manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts/package-manifest.json"
FORBIDDEN = {".git", ".venv", "__pycache__", ".pytest_cache"}
RELEASES = {"participant-07-g0": ("participant", 7), "participant-29-time-skip": ("participant", 29),
            "participant-29-b0": ("participant", 29), "participant-33-analysis": ("participant", 33),
            "participant-39-shared-context": ("participant", 39), "participant-44-b1": ("participant", 44),
            "participant-52-b2": ("participant", 52), "participant-63-b3-governance": ("participant", 63),
            "participant-80-retrospective": ("participant", 80), "recovery-52-b1": ("participant", 52),
            "recovery-63-b2": ("participant", 63), "facilitator-before-session": ("facilitator", -1),
            "evaluation-private": ("evaluation", -1)}
B0_ROOT = "agentic-workshop/03-brownfield/participant/repository/smart-ticket-b0"
B0_CONTEXT_FILES = ("docs/change-booking-guide.md", "docs/discount-overview.md",
                    "docs/adr/001-use-in-memory-repositories.md", "docs/adr/002-introduce-discount-policy.md",
                    "docs/adr/003-record-notifications-synchronously.md")
B0_ADR_DESTINATIONS = {B0_ROOT + "/" + name for name in B0_CONTEXT_FILES if "/adr/" in name}
# Recovery packages carry the same context docs a normal group has, taken from the reference solution itself.
RECOVERY = {"recovery-52-b1": ("b1-student-fare-fixed", "recovery-b1", B0_CONTEXT_FILES),
            "recovery-63-b2": ("b2-best-discount-policy", "recovery-b2", B0_CONTEXT_FILES + ("docs/api-examples.md",))}


def package_schema(package: dict) -> None:
    if package.get("id") not in RELEASES or (package.get("role"), package.get("release_minute")) != RELEASES[package["id"]]:
        raise ValueError("Unknown package identity, role or release minute")
    expected = {"recovery-52-b1": "B1", "recovery-63-b2": "B2", "participant-29-b0": "B0", "participant-07-g0": "G0"}.get(package["id"])
    if expected and package.get("source_version") != expected:
        raise ValueError("Source version does not match package identity")


def destination_check(package: dict, name: str) -> str:
    name = safe_path(name).as_posix()
    safe_b0_adr = package["id"] == "participant-29-b0" and name in B0_ADR_DESTINATIONS
    if package["id"] in RECOVERY:
        _, root, context = RECOVERY[package["id"]]
        safe_b0_adr = name in {root + "/" + n for n in context if "/adr/" in n}
    denied = {"evaluation", "facilitator", "instructions"}
    if not safe_b0_adr:
        denied.add("adr")
    if package["role"] == "participant" and any(x in name.split("/") for x in denied):
        raise ValueError(f"Role violation: {name}")
    return name


def content_policy(package: dict, contents: dict[str, bytes]) -> None:
    """Apply pedagogical policy to both prepared files and actual ZIP bytes."""
    if package["id"] == "recovery-52-b1":
        for name, body in contents.items():
            if name.endswith(".md") and re.search(r"FARE-0(?:0[7-9]|10)|applied_discounts|最低rate", body.decode("utf-8"), re.I):
                raise ValueError("B1 recovery material discloses B2 rules: " + name)
    if package["id"] != "participant-29-b0":
        return
    for relative in B0_CONTEXT_FILES:
        name = B0_ROOT + "/" + relative
        if name not in contents:
            raise ValueError("Missing controlled B0 context: " + relative)
        if contents[name] != (ROOT / name).read_bytes():
            raise ValueError("Controlled B0 context must retain original bytes: " + relative)
    for name, body in contents.items():
        if not name.endswith(".md"):
            continue
        data = body.decode("utf-8")
        if re.search(r"受控.{0,12}(?:學生|student).{0,12}(?:Bug|錯|缺陷)|(?:學生|student).{0,12}(?:Bug|85%|錯誤率)|BUG-B0-001", data, re.I):
            raise ValueError("B0 generated material discloses diagnosis")
        if re.search(r"企業.{0,20}提前.{0,20}學生|CORP(?:ORATE)?.{0,20}ADV(?:ANCE)?.{0,20}STUDENT", data, re.I):
            raise ValueError("B0 generated material discloses discount priority")
    architecture = contents[B0_ROOT + "/docs/architecture.md"].decode("utf-8")
    for name in B0_ADR_DESTINATIONS:
        if Path(name).name not in architecture:
            raise ValueError("B0 architecture must link each allowed ADR")


def repin_reviewed_sources(expected_sha256: str) -> dict:
    """Update only already enumerated sources after an explicit review anchor."""
    raw = MANIFEST.read_bytes()
    if digest(raw) != expected_sha256:
        raise ValueError("Manifest review anchor differs; inspect the current manifest first")
    manifest = json.loads(raw)
    changes = []
    for package in manifest["packages"]:
        package_schema(package)
        for entry in package["files"]:
            new_hash = digest((ROOT / safe_path(entry["source"])).read_bytes())
            if new_hash != entry["sha256"]:
                changes.append({"package": package["id"], "source": entry["source"], "old": entry["sha256"], "new": new_hash})
                entry["sha256"] = new_hash
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"reviewed_manifest_sha256": expected_sha256, "changed_sources": changes, "new_manifest_sha256": digest(MANIFEST.read_bytes())}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(value: str) -> Path:
    path = Path(value)
    if path.anchor or ":" in value or ".." in path.parts or any(p in FORBIDDEN for p in path.parts):
        raise ValueError(f"Unsafe path: {value}")
    return path


def link_check(files: dict[str, bytes]) -> int:
    count = 0
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", data.decode("utf-8")):
            target = target.split("#", 1)[0].strip("<>")
            if not target or re.match(r"[a-z]+:", target):
                continue
            resolved = (ROOT / name).parent.joinpath(unquote(target)).resolve()
            key = resolved.relative_to(ROOT).as_posix()
            if key not in files:
                raise ValueError(f"Missing packaged link: {name} -> {target}")
            count += 1
    return count


def build() -> dict:
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    run = ROOT / "dist/p11-candidate" / digest(raw)[:16]
    prepared = []
    if len(manifest["packages"]) != len(RELEASES) or {p["id"] for p in manifest["packages"]} != set(RELEASES):
        raise ValueError("Package set differs from reviewed release plan")
    for package in manifest["packages"]:
        package_schema(package)
        contents = {}
        for entry in package["files"]:
            source = ROOT / safe_path(entry["source"])
            if package["role"] == "participant":
                source_parts = safe_path(entry["source"]).parts
                is_recovery = package["id"] in RECOVERY
                if "participant" not in source_parts and not is_recovery:
                    raise ValueError(f"Unapproved participant source: {entry['source']}")
                if is_recovery:
                    expected, _, context = RECOVERY[package["id"]]
                    if expected not in source_parts or source.name == "README.md":
                        raise ValueError(f"Unapproved recovery source: {entry['source']}")
                    index = source_parts.index(expected)
                    relative = "/".join(source_parts[index+1:])
                    if not (relative.startswith("src/smart_ticket/") or relative.startswith("tests/") or relative in {"requirements.txt", "pyproject.toml", *context}):
                        raise ValueError(f"Unapproved recovery file: {relative}")
                if package["id"] == "participant-29-b0":
                    relative = source.relative_to(ROOT / B0_ROOT).as_posix()
                    if not (relative.startswith("src/smart_ticket/") or relative.startswith("tests/") or relative in {"requirements.txt", "pyproject.toml", *B0_CONTEXT_FILES}):
                        raise ValueError("Unapproved B0 source: " + relative)
                if source.name.startswith("03-b3-") and package["release_minute"] < 63:
                    raise ValueError("Premature B3 release")
                if source.name.startswith("02-b2-") and package["release_minute"] < 52:
                    raise ValueError("Premature B2 release")
            data = source.read_bytes()
            if digest(data) != entry["sha256"]:
                raise ValueError(f"Source drift: {entry['source']}")
            dest = destination_check(package, entry["destination"])
            if dest in contents:
                raise ValueError(f"Duplicate destination: {dest}")
            contents[dest] = data
        for name, body in package.get("generated", {}).items():
            name = destination_check(package, name)
            if name in contents:
                raise ValueError(f"Generated destination collision: {name}")
            contents[name] = body.encode("utf-8")
        content_policy(package, contents)
        links = link_check(contents) if package["role"] == "participant" else None
        inventory = {name: digest(data) for name, data in sorted(contents.items())}
        metadata = {"id": package["id"], "role": package["role"], "release_minute": package["release_minute"],
                    "source_version": package.get("source_version"), "source_commit": package.get("source_commit"),
                    "files": inventory, "participant_relative_links": links,
                    "status": "CANDIDATE; human rehearsal and release approval pending"}
        contents["PACKAGE-MANIFEST.json"] = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        prepared.append((package, contents, metadata))
    # Validate all inputs before creating output. Never overwrite an existing directory.
    run.mkdir(parents=True, exist_ok=False)
    results = []
    for package, contents, metadata in prepared:
        destination = run / (package["id"] + ".zip")
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(contents.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        results.append({**metadata, "zip": destination.relative_to(ROOT).as_posix(),
                        "zip_sha256": digest(destination.read_bytes()), "zip_bytes": destination.stat().st_size})
    evidence = {"manifest_sha256": digest(raw), "output": run.relative_to(ROOT).as_posix(), "packages": results}
    (run / "build-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repin-reviewed-sources", action="store_true")
    parser.add_argument("--expect-manifest-sha256")
    args = parser.parse_args()
    if args.repin_reviewed_sources:
        if not args.expect_manifest_sha256:
            parser.error("Repinning requires --expect-manifest-sha256 from the reviewed explicit manifest")
        print(json.dumps(repin_reviewed_sources(args.expect_manifest_sha256), ensure_ascii=False))
    else:
        result = build()
        print(json.dumps({"output": result["output"], "packages": len(result["packages"])}, ensure_ascii=False))
