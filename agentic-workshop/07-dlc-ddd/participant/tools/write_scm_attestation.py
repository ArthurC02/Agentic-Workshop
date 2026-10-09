"""把已簽章 commit 寫成 git-signed-commit SCM attestation，放進 Change Package 的 evidence-bundle.json。

  py -3.13 -X utf8 ../../tools/write_scm_attestation.py --package domain-memory/changes/CP-CORE-001 --commit HEAD

前提：夥伴（maintainer）已 record-approval、verify-proposal，並以自己的金鑰 `git commit -S` 提交了這個套件。
本工具只寫 attestation；簽章是否被授權由 `dm verify-git-governance --commit <sha>` 與 finalize-proposal 判定。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402


def git(*args: str) -> str:
    done = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if done.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失敗：{done.stderr.strip()}")
    return done.stdout.strip()


def write(package: Path, commit: str) -> dict:
    sha = git("rev-parse", "--verify", f"{commit}^{{commit}}")
    signature = git("log", "-1", "--format=%G?", sha)
    if signature == "E":
        raise SystemExit(f"commit {sha[:12]} 有簽章但無法驗證（%G?=E）：本 Repo 的 gpg.format 須為 ssh，"
                         "且 gpg.ssh.allowedSignersFile 須指向含夥伴公鑰的檔案（git config --local 設定）。")
    if signature not in ("G", "U"):
        raise SystemExit(f"commit {sha[:12]} 沒有有效簽章（%G?={signature}）。請由持鑰夥伴以 git commit -S 提交。")
    proposal = dmlib.read_json(package / "domain-change-proposal.json")
    if not proposal.get("approvals"):
        raise SystemExit("proposal 還沒有任何核准；請夥伴先執行 record-approval。")
    path = package / "evidence-bundle.json"
    evidence = dmlib.read_json(path)
    evidence["scm_attestation"] = {
        "provider": "git-signed-commit", "commit": sha, "status": "approved",
        "proposal_revision": proposal["proposal_revision"],
        "base_registry_revision": proposal["base_registry_revision"],
        "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")}
    evidence["approvals"] = proposal["approvals"]
    dmlib.write_json(path, evidence)
    return evidence["scm_attestation"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="寫入 git-signed-commit SCM attestation。",
                                     epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--package", required=True, help="Change Package 資料夾")
    parser.add_argument("--commit", default="HEAD", help="已簽章的 commit（預設 HEAD）")
    args = parser.parse_args(argv)
    attestation = write(Path(args.package), args.commit)
    print(f"已寫入 attestation：commit {attestation['commit']}")
    print(f"下一步（夥伴）：dm verify-git-governance --commit {attestation['commit']}；finalize-proposal 由提案者執行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
