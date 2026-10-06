import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import package_materials as pm


class ParticipantDistributionTests(unittest.TestCase):
    def test_only_reviewed_html_is_distributed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "runbook.html"
            source.write_bytes(b"reviewed HTML")
            (root / "unlock-codes.json").write_text("private code")
            (root / "answer.md").write_text("private answer")
            with mock.patch.object(pm.bm, "ROOT", root), mock.patch.object(pm.bm, "outputs", return_value={"runbook": source}), mock.patch.object(pm.bm, "build_runbook", return_value=(b"reviewed HTML", {})):
                target = pm.package()
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(archive.namelist(), ["runbook.html"])
                self.assertEqual(archive.read("runbook.html"), b"reviewed HTML")

    def test_stale_html_is_rejected_before_distribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "runbook.html"
            source.write_bytes(b"stale")
            with mock.patch.object(pm.bm, "ROOT", root), mock.patch.object(pm.bm, "outputs", return_value={"runbook": source}), mock.patch.object(pm.bm, "build_runbook", return_value=(b"reviewed", {})):
                with self.assertRaises(pm.bm.BuildError):
                    pm.package()
            self.assertFalse((root / "dist").exists())
