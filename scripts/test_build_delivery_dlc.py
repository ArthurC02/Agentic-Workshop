"""DLC packaging: vendored plugin, candidate builder/verifier, and DLC recovery-download support."""
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_delivery  # noqa: E402
import build_delivery_dlc as dlc  # noqa: E402
import build_materials as bm  # noqa: E402
import vendor_dlc_plugin as vendor  # noqa: E402

P = "agentic-workshop/07-dlc-ddd/participant"
RELEASES = {"participant-dlc-open": ("participant", 0), "participant-dlc-d1": ("participant", 10),
            "recovery-dlc-d1": ("participant", 35), "evaluation-dlc-private": ("evaluation", -1)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


class VendorPluginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = Path(self.tmp.name) / "plugin"
        for name, body in {".claude-plugin/plugin.json": '{"version": "9.9.9"}', "SKILL.md": "skill",
                           "scripts/tool.py": "x = 1\r\n", "scripts/__pycache__/tool.cpython-313.pyc": "junk",
                           ".pytest_cache/v/x": "junk", ".ruff_cache/x": "junk", "scripts/stray.pyc": "junk",
                           "evals/case.json": "dev", "scripts/test_tool.py": "dev", "README.md": "dev",
                           "ruff.toml": "dev", "CHANGELOG.md": "log"}.items():
            (self.src / name).parent.mkdir(parents=True, exist_ok=True)
            (self.src / name).write_bytes(body.encode())

    def tearDown(self):
        self.tmp.cleanup()

    def test_deterministic_runtime_zip_without_dev_files_and_verifiable_sums(self):
        name, data, sums = vendor.build(self.src)
        self.assertEqual((name, data, sums), vendor.build(self.src))
        self.assertEqual(name, "domain-memory-9.9.9.zip")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(archive.namelist(), ["domain-memory/.claude-plugin/plugin.json",
                                                  "domain-memory/CHANGELOG.md", "domain-memory/SKILL.md",
                                                  "domain-memory/scripts/tool.py"])
            self.assertEqual(archive.read("domain-memory/scripts/tool.py"), b"x = 1\r\n")  # bytes untouched
            self.assertTrue(all(i.date_time == (2026, 1, 1, 0, 0, 0) for i in archive.infolist()))
        out = Path(self.tmp.name) / name
        out.write_bytes(data)
        out.with_name(name + ".SHA256SUMS").write_bytes(sums)
        self.assertEqual(vendor.verify(out), [])
        self.assertEqual(dlc.vendor_check({dlc.VENDOR_ZIP: data, dlc.VENDOR_ZIP + ".SHA256SUMS":
                                           sums.replace(name.encode(), b"domain-memory-0.10.15.zip")}), True)
        out.write_bytes(data + b"x")
        self.assertTrue(vendor.verify(out))

    def test_vendored_repo_copy_matches_its_sums(self):
        target = vendor.VENDOR / "domain-memory-0.10.15.zip"
        if not target.exists():
            self.skipTest("plugin not vendored yet")
        self.assertEqual(vendor.verify(target), [])


class DlcBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write(f"{P}/README.md", "# open\n[repo](repository/base/)\n")
        self.write(f"{P}/repository/base/app.py", "print(1)\n")
        self.write(f"{P}/repository/base/__pycache__/app.cpython-313.pyc", "junk")
        self.write(f"{P}/repository/base/.venv/x.py", "junk")
        self.write(f"{P}/worksheets/d1-sources.md", "# d1\n")
        self.write("agentic-workshop/07-dlc-ddd/facilitator/recovery/d1/repo/app.py", "print(2)\n")
        self.write("agentic-workshop/07-dlc-ddd/evaluation/answer.md", "# private\n")
        plugin = self.root / "plugin"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin/plugin.json").write_text('{"version": "0.10.15"}')
        _name, data, sums = vendor.build(plugin)
        (self.root / dlc.VENDOR_ZIP).parent.mkdir(parents=True)
        (self.root / dlc.VENDOR_ZIP).write_bytes(data)
        (self.root / (dlc.VENDOR_ZIP + ".SHA256SUMS")).write_bytes(sums)
        rec = "agentic-workshop/07-dlc-ddd/facilitator/recovery/d1"
        self.manifest = {"schema": 1, "packages": [
            self.pkg("participant-dlc-open", "participant", 0,
                     [f"{P}/README.md", f"{P}/repository/base/**/*", f"{P}/vendor/**/*"]),
            self.pkg("participant-dlc-d1", "participant", 10, [f"{P}/worksheets/d1-*.md"]),
            {**self.pkg("recovery-dlc-d1", "participant", 35, [rec + "/**/*"]),
             "destination_root": {"from": rec, "to": "recovery-dlc-d1"}},
            self.pkg("evaluation-dlc-private", "evaluation", -1, ["agentic-workshop/07-dlc-ddd/evaluation/**/*"])]}
        self.manifest_path = self.root / "scripts/package-manifest-dlc.json"
        self.save()
        self.patches = [mock.patch.object(dlc, "ROOT", self.root), mock.patch.object(build_delivery, "ROOT", self.root),
                        mock.patch.object(dlc, "MANIFEST", self.manifest_path),
                        mock.patch.object(dlc, "OUT_ROOT", self.root / "dist/dlc-candidate"),
                        mock.patch.object(dlc, "RELEASES", RELEASES)]
        for p in self.patches:
            p.start()
        dlc.pin()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def pkg(self, id_, role, minute, sources):
        return {"id": id_, "role": role, "release_minute": minute, "source_version": None, "source_commit": None,
                "sources": sources, "files": [], "generated": {}}

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

    def save(self):
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def build(self, **kw):
        with mock.patch("sys.stderr", io.StringIO()):
            return dlc.build(**kw)

    def test_build_records_versions_never_overwrites_and_verifies(self):
        evidence = self.build()
        self.assertEqual(evidence["missing_packages"], [])
        self.assertTrue(evidence["python"] and evidence["zlib"])
        run = self.root / evidence["output"]
        self.assertEqual(run.name, sha(self.manifest_path.read_bytes())[:16])
        open_files = next(p for p in evidence["packages"] if p["id"] == "participant-dlc-open")["files"]
        self.assertEqual(sorted(open_files)[:2], [f"{P}/README.md", f"{P}/repository/base/app.py"])
        self.assertEqual(len(open_files), 4)  # no cache/venv
        rec = next(p for p in evidence["packages"] if p["id"] == "recovery-dlc-d1")["files"]
        self.assertEqual(list(rec), ["recovery-dlc-d1/repo/app.py"])
        self.assertEqual(dlc.verify(run)["missing"], [])
        with self.assertRaises(FileExistsError):
            self.build()

    def test_missing_source_fails_clearly_unless_allowed(self):
        (self.root / f"{P}/worksheets/d1-sources.md").unlink()
        dlc.pin()
        with self.assertRaisesRegex(ValueError, "Missing sources for participant-dlc-d1"):
            self.build()
        evidence = self.build(allow_missing=True)
        self.assertEqual(evidence["missing_packages"], ["participant-dlc-d1"])
        self.assertTrue(evidence["allow_missing"])
        self.assertEqual(dlc.verify(self.root / evidence["output"])["missing"], ["participant-dlc-d1"])

    def test_allow_missing_build_without_vendored_plugin_still_verifies(self):
        for name in (dlc.VENDOR_ZIP, dlc.VENDOR_ZIP + ".SHA256SUMS"):
            (self.root / name).unlink()
        dlc.pin()
        with self.assertRaisesRegex(ValueError, "Missing sources"):
            self.build()
        evidence = self.build(allow_missing=True)
        self.assertEqual(dlc.verify(self.root / evidence["output"])["missing"], [])

    def test_unpinned_vanished_and_drifted_sources_fail(self):
        self.write(f"{P}/worksheets/d1-extra.md", "# new\n")
        with self.assertRaisesRegex(ValueError, "unpinned"):
            self.build()
        dlc.pin()
        self.write(f"{P}/worksheets/d1-extra.md", "# changed\n")
        with self.assertRaisesRegex(ValueError, "Source drift"):
            self.build()

    def test_participant_policies(self):
        cases = [(f"{P}/repository/base/key.txt", "-----BEGIN OPENSSH PRIVATE KEY-----\nabc\n", "Private key"),
                 (f"{P}/repository/base/observation-guide.md", "# x\n", "Role violation"),
                 (f"{P}/repository/base/docs/rubric.md", "# x\n", "Role violation")]
        for rel, body, error in cases:
            with self.subTest(rel=rel):
                self.write(rel, body)
                dlc.pin()
                with self.assertRaisesRegex(ValueError, error):
                    self.build()
                (self.root / rel).unlink()
                dlc.pin()

    def test_nested_zip_with_private_key_is_rejected(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as nested:
            nested.writestr("id_ed25519", "-----BEGIN OPENSSH PRIVATE KEY-----\n")
        with self.assertRaisesRegex(ValueError, "Private key"):
            dlc.content_policy({"role": "participant"}, {f"{P}/vendor/x.zip": stream.getvalue()})

    def test_participant_source_needs_participant_segment_and_recovery_its_folder(self):
        with self.assertRaisesRegex(ValueError, "Unapproved participant source"):
            dlc.source_policy({"id": "participant-dlc-d1", "role": "participant"}, "agentic-workshop/07-dlc-ddd/x.md")
        with self.assertRaisesRegex(ValueError, "Unapproved recovery source"):
            dlc.source_policy({"id": "recovery-dlc-d1", "role": "participant"},
                              "agentic-workshop/07-dlc-ddd/facilitator/recovery/d2/app.py")

    def test_verify_detects_tampered_zip(self):
        run = self.root / self.build()["output"]
        target = run / "participant-dlc-d1.zip"
        target.write_bytes(target.read_bytes() + b"x")
        with self.assertRaisesRegex(ValueError, "SHA256 differs"):
            dlc.verify(run)

    def test_shell_scripts_are_executable_for_unix_unzip(self):
        path = Path(self.tmp.name) / "t.zip"
        dlc.write_zip(path, {"tools/dm.sh": b"#!/bin/sh\n", "tools/README.md": b"x"})
        with zipfile.ZipFile(path) as archive:
            modes = {i.filename: (i.create_system, i.external_attr >> 16) for i in archive.infolist()}
        self.assertEqual(modes, {"tools/dm.sh": (3, 0o100755), "tools/README.md": (3, 0o100644)})


class RealDlcManifestTests(unittest.TestCase):
    def test_manifest_matches_release_plan_and_role_rules(self):
        manifest = json.loads(dlc.MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual({p["id"] for p in manifest["packages"]}, set(dlc.RELEASES))
        for package in manifest["packages"]:
            self.assertEqual((package["role"], package["release_minute"]), dlc.RELEASES[package["id"]])
            for entry in package["files"]:
                dlc.source_policy(package, entry["source"])
                self.assertEqual(entry["destination"], dlc.destination(package, entry["source"]))


class DlcRecoveryEditionTests(unittest.TestCase):
    def candidate(self, root, minute, version):
        data = b"PK-recovery"
        root.mkdir(parents=True, exist_ok=True)
        (root / "recovery-dlc-d1.zip").write_bytes(data)
        (root / "build-evidence.json").write_text(json.dumps({"packages": [
            {"id": "recovery-dlc-d1", "role": "participant", "release_minute": minute, "source_version": version,
             "zip_sha256": sha(data)}]}), encoding="utf-8")
        return data

    def test_edition_json_declares_recovery_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "edition.json").write_text(json.dumps({
                "candidate_id": "abc", "total_minutes": 180, "plan": [["dlc-opening", 0, 180, "x"]],
                "recovery_downloads": {"recovery-dlc-d1.zip": ["dlc-rec-d1", 35]}}), encoding="utf-8")
            with mock.patch.object(bm, "DLC_MATERIALS", folder):
                edition = bm.load_edition("dlc")
        self.assertEqual(edition.recovery_downloads, {"recovery-dlc-d1.zip": ("dlc-rec-d1", 35)})
        self.assertEqual(edition.recovery_groups, {"dlc-rec-d1": 35})

    def test_dlc_recovery_skips_main_version_check_but_keeps_minute_check(self):
        downloads = {"recovery-dlc-d1.zip": ("dlc-rec-d1", 35)}
        with tempfile.TemporaryDirectory() as tmp:
            data = self.candidate(Path(tmp) / "ok", 35, None)
            self.assertEqual(bm.Candidate(Path(tmp) / "ok", downloads).zip_bytes("recovery-dlc-d1.zip"), data)
            with self.assertRaises(bm.BuildError):
                bm.Candidate(Path(tmp) / "ok", downloads).read_member("recovery-dlc-d1.zip", "x")
            self.candidate(Path(tmp) / "late", 36, None)
            with self.assertRaisesRegex(bm.BuildError, "release minute"):
                bm.Candidate(Path(tmp) / "late", downloads).zip_bytes("recovery-dlc-d1.zip")

    def test_main_recovery_still_requires_its_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "recovery-52-b1.zip").write_bytes(b"x")
            (root / "build-evidence.json").write_text(json.dumps({"packages": [
                {"id": "recovery-52-b1", "role": "participant", "release_minute": 52, "source_version": "B2",
                 "zip_sha256": sha(b"x")}]}), encoding="utf-8")
            with self.assertRaisesRegex(bm.BuildError, "source version"):
                bm.Candidate(root).zip_bytes("recovery-52-b1.zip")


if __name__ == "__main__":
    unittest.main()
