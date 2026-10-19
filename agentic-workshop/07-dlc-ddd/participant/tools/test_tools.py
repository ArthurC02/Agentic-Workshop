"""輔助腳本自檢：py -3.13 -X utf8 -m unittest discover -s tools -p "test_*.py" -v

整合測試在暫存 git repo 內走一次 D1＋D2（含 SSH 簽章）；找不到 Plugin、git 或 ssh-keygen 時略過。
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import dmlib  # noqa: E402
from make_record import parse_evidence  # noqa: E402


def plugin_available() -> bool:
    try:
        dmlib.plugin_root()
        return bool(shutil.which("git") and shutil.which("ssh-keygen"))
    except SystemExit:
        return False


class UnitTests(unittest.TestCase):
    def test_doctor_warns_when_key_inside_repo(self):
        import doctor
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as repo:
            saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
            os.environ["HOME"] = os.environ["USERPROFILE"] = home
            try:
                self.assertEqual(doctor.key_checks(Path(repo))[0][0], "OK")
                (Path(repo) / ".dlc-keys" / "m").mkdir(parents=True)
                (Path(repo) / ".dlc-keys" / "m" / "id_ed25519").write_text("x")
                self.assertEqual(doctor.key_checks(Path(repo))[0][0], "!!")
            finally:
                for k, v in saved.items():
                    os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def test_expand_adds_fixed_roots_only_where_accepted(self):
        self.assertEqual(dmlib.expand(["validate"], True),
                         ["validate", "--registry-root", "domain-memory", "--repo-root", "."])
        self.assertEqual(dmlib.expand(["cite", "--path", "a"], False), ["cite", "--path", "a", "--repo-root", "."])
        self.assertEqual(dmlib.expand(["record-approval", "--role", "r"], True), ["record-approval", "--role", "r"])
        self.assertEqual(dmlib.expand(["validate", "--registry-root", "x"], True),
                         ["validate", "--registry-root", "x", "--repo-root", "."])
        default = dmlib.expand(["init-signing-key", "--principal", "m@x.com"], False)
        self.assertEqual(default[-1], str(dmlib.key_dir() / "m@x.com" / "signing-key"))
        with self.assertRaises(SystemExit):  # PowerShell 不展開 %USERPROFILE% → 落在 Repo 內
            dmlib.expand(["init-signing-key", "--principal", "m", "--key-file", "%USERPROFILE%\\.dlc-keys\\k"], False)

    def test_parse_evidence(self):
        self.assertEqual(parse_evidence("src/a.py:3-7"), ("src/a.py", 3, 7))
        self.assertEqual(parse_evidence("src\\a.py:5"), ("src/a.py", 5, 5))
        for bad in ("src/a.py", "src/a.py:x-2", "src/a.py:9-3"):
            with self.assertRaises(ValueError):
                parse_evidence(bad)

    def test_dm_sh_has_lf_only(self):
        self.assertNotIn(b"\r", (TOOLS / "dm.sh").read_bytes())  # CRLF 會讓 macOS 的 sh 讀到 "python3\r"

    @unittest.skipUnless(shutil.which("sh"), "需要 sh（Git Bash／macOS／Linux）")
    def test_dm_sh_prefers_python313_without_py(self):
        # macOS／Linux：沒有 py 啟動器時，要用 python3.13，而不是 PATH 上較舊或較新的 python3。
        with tempfile.TemporaryDirectory() as shims:
            for name in ("python3.13", "python3"):
                shim = Path(shims) / name
                shim.write_bytes(f'#!/bin/sh\necho "{name} $*"\n'.encode())
                shim.chmod(0o755)
            sh = shutil.which("sh")
            path = os.pathsep.join([shims, str(Path(sh).parent)] if os.name == "nt" else [shims, "/usr/bin", "/bin"])
            done = subprocess.run([sh, str(TOOLS / "dm.sh"), "readiness"], capture_output=True, text=True,
                                  env={**os.environ, "PATH": path})
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertTrue(done.stdout.startswith("python3.13 -X utf8 "), done.stdout)
            self.assertTrue(done.stdout.strip().endswith("dmlib.py readiness"), done.stdout)

    def test_env_defaults_git_timeout_without_overriding(self):
        saved = os.environ.pop("DOMAIN_MEMORY_GIT_TIMEOUT", None)
        try:
            self.assertEqual(dmlib.env()["DOMAIN_MEMORY_GIT_TIMEOUT"], "60")
            os.environ["DOMAIN_MEMORY_GIT_TIMEOUT"] = "5"
            self.assertEqual(dmlib.env()["DOMAIN_MEMORY_GIT_TIMEOUT"], "5")
        finally:
            os.environ.pop("DOMAIN_MEMORY_GIT_TIMEOUT", None) if saved is None else os.environ.__setitem__("DOMAIN_MEMORY_GIT_TIMEOUT", saved)

    def test_save_skips_empty_output(self):
        # A refused command prints only to stderr; --save must not leave an empty file behind.
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.json"
            empty = subprocess.CompletedProcess([], 1, stdout="", stderr="ERROR: refused")
            with mock.patch.object(dmlib, "command_line", return_value=["py"] * 5):
                with mock.patch.object(dmlib.subprocess, "run", return_value=empty):
                    self.assertEqual(dmlib.main(["validate", "--save", str(out)]), 1)
            self.assertFalse(out.exists())

    def test_read_json_accepts_powershell_utf16(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cf.json"
            path.write_bytes('{"verdict": "killed"}'.encode("utf-16"))
            self.assertEqual(dmlib.read_json(path), {"verdict": "killed"})


@unittest.skipUnless(plugin_available(), "需要 domain-memory Plugin、git 與 ssh-keygen")
class GovernedLifecycleTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="dlc-tools-"))
        self.home = Path(tempfile.mkdtemp(prefix="dlc-home-"))  # 金鑰預設在 HOME/.dlc-keys，測試不碰真實家目錄
        self.saved_env = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
        os.environ["HOME"] = os.environ["USERPROFILE"] = str(self.home)
        files = {
            ".gitignore": "__pycache__/\n",
            ".gitattributes": "* -text\n",
            "docs/requirements/rules.md": "# Rules\n\n| `LIM-001` | 單筆上限為 14。 |\n",
            "src/app.py": "LIMIT = 14\n",
            "tests/test_check.py": "import sys\nsys.path.insert(0, 'src')\nimport app\nassert app.LIMIT == 14, 'LIMIT changed'\nprint('ok')\n",
            "README.md": "not a source\n",
        }
        for name, text in files.items():
            (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / name).write_text(text, encoding="utf-8", newline="\n")
        self.git("init", "-q", "-b", "main")
        self.git("config", "--local", "user.name", "Proposer")
        self.git("config", "--local", "user.email", "proposer@example.com")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")

    def tearDown(self):
        for k, v in self.saved_env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        shutil.rmtree(self.repo, ignore_errors=True)
        shutil.rmtree(self.home, ignore_errors=True)

    def git(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True).stdout.strip()

    def tool(self, script: str, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        done = subprocess.run([sys.executable, "-X", "utf8", str(TOOLS / script), *args], cwd=self.repo,
                              capture_output=True, text=True, encoding="utf-8", env=dmlib.env())
        if ok:
            self.assertEqual(done.returncode, 0, f"{script} {args}\n{done.stdout}\n{done.stderr}")
        return done

    def dm(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        return self.tool("dmlib.py", *args, ok=ok)

    def test_d1_and_d2_with_tools(self):
        quoted = f'"{sys.executable}"'
        self.dm("init-domain-memory", "--output", "domain-memory", "--source", "docs/requirements", "--source", "src",
                "--source", "tests", "--storage-mode", "tracked", "--data-classification", "internal",
                "--review-mode", "local-draft-only", "--source-authority", "Proposer <proposer@example.com>")
        self.dm("confirm-sources", "--confirmed-by", "Proposer <proposer@example.com>")
        # D1：未分類來源被拒，已確認來源可建出 record 並 upsert。
        refused = self.tool("make_record.py", "--asset", "contexts", "--id", "x", "--name", "X",
                            "--responsibility", "r", "--evidence", "README.md:1", ok=False)
        self.assertNotEqual(refused.returncode, 0)
        batch = [
            {"asset": "contexts", "id": "limits", "name": "上限", "responsibility": "決定單筆上限",
             "evidence": ["docs/requirements/rules.md:3"]},
            {"asset": "vocabulary", "id": "limit", "name": "上限", "definition": "單筆最多 14",
             "context": "limits", "not_same_as": ["quota"], "evidence": ["docs/requirements/rules.md:3", "src/app.py:1"]},
            {"asset": "vocabulary", "id": "quota", "name": "額度", "definition": "全部加總的上限",  # 互標 not_same_as
             "context": "limits", "not_same_as": ["limit"], "evidence": ["docs/requirements/rules.md:3"]},
            {"asset": "rules", "id": "LIM-001", "statement": "單筆上限為 14", "context": ["limits"],
             "evidence": ["docs/requirements/rules.md:3", "tests/test_check.py:4"]},
        ]
        (self.repo / "batch.json").write_text(json.dumps(batch, ensure_ascii=False), encoding="utf-8")
        self.tool("make_record.py", "--batch", "batch.json", "--upsert")
        record = dmlib.read_json(self.repo / "records" / "vocabulary-limit.json")
        self.assertEqual(record["contexts"], ["limits"])
        self.assertEqual(len(record["evidence"]), 2)
        documents = dmlib.registry_documents(self.repo / "domain-memory")  # 經 Plugin export
        self.assertEqual(sorted(documents), sorted(dmlib.ASSETS))
        self.assertEqual({t["id"] for t in documents["vocabulary"]["terms"]}, {"limit", "quota"})
        self.assertIn("valid", self.dm("validate").stdout)
        self.dm("counterfactual", "--file", "src/app.py", "--find", "LIMIT = 14", "--replace", "LIMIT = 15",
                "--test-command", f"{quoted} tests/test_check.py", "--save", "cf.json")
        self.assertEqual(dmlib.read_json(self.repo / "cf.json")["verdict"], "killed")
        # D2：簽章先於第一個 Registry commit。
        key = json.loads(self.dm("init-signing-key", "--principal", "maintainer@example.com", "--key-file",
                                 str(dmlib.key_dir() / "m" / "id_ed25519"), "--sign-every-commit").stdout)
        self.assertTrue(str(dmlib.key_dir()).startswith(str(self.home)))
        self.assertFalse((self.repo / ".dlc-keys").exists())
        self.dm("amend-policy", "--field", "authorized_signers", "--value", key["fingerprint"], "--reason", "t")
        self.dm("amend-policy", "--field", "review_trigger", "--value", "git-push", "--reason", "t")
        self.dm("amend-policy", "--field", "review_mode", "--value", "scm-verified", "--verifier",
                "git-signed-commit", "--reason", "t")
        package = "domain-memory/changes/CP-T-001"
        spec = {"package": package, "requirement_id": "REQ-T-001", "proposal_id": "CP-T-001",
                "proposer": "Proposer <proposer@example.com>", "intent": "升為 reviewed",
                "acceptance_criteria": [{"id": "AC-1", "statement": "上限 14", "test": "tests/test_check.py"}],
                "rules": [{"id": "LIM-001", "test": "tests/test_check.py"}],
                "promote": {"contexts": ["limits"], "vocabulary": ["limit", "quota"], "rules": ["LIM-001"]},
                "owner_context": "limits", "invariant": "單筆不超過 14",
                "owner_evidence": ["docs/requirements/rules.md:3"],
                "design": {"domain_forces": ["上限會調整"], "decision": "沿用常數",
                           "invariants_preserved": ["LIM-001"], "rejected_alternatives": ["寫死在呼叫端"],
                           "counterfactual_check": "LIMIT 改 15，tests/test_check.py 失敗"},
                "counterfactual": {"obligation_id": "OB-LIM-001", "result_file": "cf.json"}}
        (self.repo / "spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        self.tool("fill_package.py", "spec.json", "--test-command", quoted)
        bundle = dmlib.read_json(self.repo / package / "evidence-bundle.json")
        self.assertEqual({r["exit_code"] for r in bundle["test_results"]}, {0})
        self.assertEqual(bundle["counterfactual_check"]["status"], "passed")
        self.dm("submit-proposal", "--package-root", package)
        self.assertNotEqual(self.dm("record-approval", "--package-root", package, "--role", "domain-owner",
                                    "--reviewer", "Proposer <proposer@example.com>", "--scope", "all",
                                    ok=False).returncode, 0)
        self.dm("record-approval", "--package-root", package, "--role", "domain-owner",
                "--reviewer", "Maintainer <maintainer@example.com>", "--scope", "all")
        self.dm("verify-proposal", "--package-root", package)
        # 1.2.1 起重跑 verify-proposal 不再拒絕（D2 檢查點 4 的 ③ 會重跑）。
        self.assertIn("already verified at revision 1; nothing was written",
                      self.dm("verify-proposal", "--package-root", package).stdout)
        # 未簽章 commit 不得當成核准證明：ship-package 在 attest 這一步就拒絕，什麼都不寫。
        self.git("add", "-A")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "unsigned")
        self.assertNotEqual(self.dm("ship-package", "--package-root", package, "--commit", "HEAD",
                                    ok=False).returncode, 0)
        self.git("reset", "-q", "--soft", "HEAD~1")
        self.git("-c", "user.name=Maintainer", "-c", "user.email=maintainer@example.com", "commit", "-qm", "approve")
        self.dm("verify-git-governance", "--commit", self.git("rev-parse", "HEAD"))
        # D2 檢查點 6：一步寫入核准證明、定案並套用（Plugin 1.0 的 ship-package）。
        shipped = json.loads(self.dm("ship-package", "--package-root", package, "--commit", "HEAD").stdout)
        self.assertEqual(shipped["status"], "applied", shipped)
        self.dm("validate", "--require-reviewed")
        # 0.31 起 reviewed record 帶 verified（誰、何時核准），不再有 review 區塊；讀取一律經 export。
        rule = dmlib.registry_documents(self.repo / "domain-memory")["rules"]["rules"][0]
        self.assertEqual(rule["status"], "reviewed")
        self.assertNotIn("review", rule)
        self.assertTrue(rule["verified"] and all(v["by"].startswith("human:") for v in rule["verified"]), rule)
        self.assertIn('"valid"', self.dm("verify-audit").stdout)
        self.tool("setup_remote.py", "--path", "../" + self.repo.name + "-remote.git")
        self.assertTrue(self.git("remote", "get-url", "origin").endswith("-remote.git"))
        shutil.rmtree(self.repo.parent / f"{self.repo.name}-remote.git", ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
