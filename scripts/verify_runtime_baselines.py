"""Check all pinned distributions and six source trees before/after this check.

This supplements pytest evidence; it does not claim a new installation or compare
G0/G1 against a historical SHA manifest that does not exist.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

from validate_workshop import ROOT, VERSIONS, file_hash


def snapshot(path):
    return {p.relative_to(path).as_posix(): file_hash(p) for p in sorted(path.rglob('*'))
            if p.is_file() and not any(part in p.relative_to(path).parts
                for part in ('.git', '.pytest_cache', '__pycache__'))}


def main():
    output = ROOT / 'agentic-workshop/06-runbook/evaluation/p11-runtime-baseline-evidence.json'
    (output.parent / 'p11-validation-logs').mkdir(parents=True, exist_ok=True)
    evidence = {'executed_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'Pinned installed versions and source hashes before/after this dependency verification only',
                'installation': 'NOT RUN', 'versions': {}}
    for version, config in VERSIONS.items():
        repo = ROOT / 'agentic-workshop' / config[0]
        python = ROOT / '.codex-tmp' / f'{version.lower()}-env' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        before = snapshot(repo)
        code = ('import importlib.metadata,json,pathlib,sys; '
                'pins=[line.strip().split("==") for line in pathlib.Path("requirements.txt").read_text().splitlines() if line.strip() and not line.startswith("#")]; '
                'actual={name:importlib.metadata.version(name) for name,expected in pins}; '
                'print(json.dumps({"python":sys.version.split()[0],"installed":actual,"expected":dict(pins)})); '
                'assert all(actual[name]==expected for name,expected in pins); assert sys.version_info[:2]==(3,13)')
        result = subprocess.run([str(python), '-X', 'utf8', '-c', code], cwd=repo,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding='utf-8', timeout=20)
        after = snapshot(repo)
        logfile = output.parent / 'p11-validation-logs' / f'{version.lower()}-dependency-pins.log'
        logfile.write_text(result.stdout, encoding='utf-8')
        evidence['versions'][version] = {
            'status': 'PASS' if result.returncode == 0 and before == after else 'FAIL',
            'command': [str(python.relative_to(ROOT)), '-X', 'utf8', '-c', code],
            'cwd': str(repo.relative_to(ROOT)), 'returncode': result.returncode,
            'log': str(logfile.relative_to(ROOT)), 'log_sha256': file_hash(logfile),
            'source_sha256_before': before, 'source_sha256_after': after,
            'source_hashes_unchanged': before == after,
            'distribution_versions': json.loads(result.stdout.splitlines()[0]) if result.returncode == 0 else None}
    evidence['status'] = 'PASS' if all(v['status'] == 'PASS' for v in evidence['versions'].values()) else 'FAIL'
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(evidence['status'])
    return 0 if evidence['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
