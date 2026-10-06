"""Offline, reproducible workshop preflight; never claims human rehearsal.

Run with Python 3.13: python scripts/validate_workshop.py
Existing independent environments default to .codex-tmp/<version>-env.
Use --env-root to select a prepared directory containing those environments.
No installation, network, snapshot modification, or human timing is performed.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    'G0': ('01-greenfield/participant/starter-repository', 1, 8, 0),
    'G1': ('01-greenfield/evaluation/reference-solution/greenfield-reference-mvp', 28, 0, 0),
    'B0': ('03-brownfield/participant/repository/smart-ticket-b0', 39, 0, 5),
    'B1': ('03-brownfield/evaluation/reference-solutions/b1-student-fare-fixed', 44, 0, 0),
    'B2': ('03-brownfield/evaluation/reference-solutions/b2-best-discount-policy', 55, 0, 0),
    'B3': ('03-brownfield/evaluation/reference-solutions/b3-group-booking', 75, 0, 0),
}
G0_SKIP_NAMES = {'test_sellable_trips', 'test_booking_reserves_seat',
                 'test_more_than_four_rejected', 'test_insufficient_seats_rejected',
                 'test_payment_then_duplicate_rejected', 'test_paid_order_query',
                 'test_adult_fare', 'test_student_fare'}
KNOWN_WARNING = ('DeprecationWarning', 'The anyio.abc.BlockingPortal alias is deprecated, '
                 'use anyio.from_thread.BlockingPortal instead.')


def warning_gate(text):
    warnings = re.findall(r'((?:[A-Za-z_][A-Za-z0-9_]*\.)*(?:[A-Za-z_][A-Za-z0-9_]*)?Warning): ([^\n\r]+)', text)
    return warnings, all(tuple(warning) == KNOWN_WARNING for warning in warnings)


def test_gate(count, failed_ids, skip_reasons, version, config, manifest):
    _, passes, skips, fails = config
    return (count == {'passed': passes, 'skipped': skips, 'failed': fails}
            and (failed_ids == sorted(manifest) if version == 'B0' else not failed_ids)
            and all(reason.get('type') == 'pytest.skip' for reason in skip_reasons))


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def documents():
    files = [ROOT / 'Agent.md', *sorted((ROOT / 'docs').rglob('*.md')),
             *sorted((ROOT / 'agentic-workshop').rglob('*.md')),
             *sorted((ROOT / 'scripts').rglob('*.md'))]
    errors, bom_files, links = [], [], 0
    for path in files:
        raw = path.read_bytes()
        if raw.startswith(b'\xef\xbb\xbf'):
            bom_files.append(path.relative_to(ROOT).as_posix())
        try:
            content = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            errors.append(f'Invalid UTF-8: {path.relative_to(ROOT)}')
            continue
        if sum(line.lstrip().startswith('```') for line in content.splitlines()) % 2:
            errors.append(f'Unbalanced fences: {path.relative_to(ROOT)}')
        participant = 'participant' in path.relative_to(ROOT).parts
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            target = target.strip().strip('<>')
            if '://' in target or target.startswith('#'):
                continue
            target = unquote(target.split('#')[0])
            if not target:
                continue
            links += 1
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f'Broken link: {path.relative_to(ROOT)} -> {target}')
            if participant and any(part in resolved.parts for part in
                                   ('facilitator', 'evaluation', 'instructions')):
                errors.append(f'Participant internal link: {path.relative_to(ROOT)} -> {target}')
        if participant and any(token in content for token in ('reference-solutions/', 'reference-solution/')):
            errors.append(f'Participant answer reference: {path.relative_to(ROOT)}')
    return {'status': 'PASS' if not errors else 'FAIL', 'markdown_files': len(files),
            'relative_links': links, 'errors': errors,
            'existing_utf8_bom_files': bom_files,
            'scope': 'Agent.md + docs/**/*.md + agentic-workshop/**/*.md + scripts/**/*.md',
            'limits': 'Static links/encoding/fences/participant internal references only; not semantic review'}


def traceability():
    registry = (ROOT / 'agentic-workshop/00-governance/rule-traceability-baseline.md').read_text(encoding='utf-8')
    rules = set(re.findall(r'^\| `([A-Z]+(?:-[A-Z]+)*-\d{3})` \|', registry, re.M))
    errors, results = [], {}
    maps = {
        'G1': ['01-greenfield/evaluation/06-acceptance-test-map.md'],
        'B0': ['03-brownfield/evaluation/04-b0-rule-traceability.md'],
        'B1': ['03-brownfield/evaluation/04-b0-rule-traceability.md', '03-brownfield/evaluation/08-b1-acceptance-test-map.md'],
        'B2': ['03-brownfield/evaluation/04-b0-rule-traceability.md', '03-brownfield/evaluation/09-b2-acceptance-test-map.md'],
        'B3': ['03-brownfield/evaluation/04-b0-rule-traceability.md', '03-brownfield/evaluation/09-b2-acceptance-test-map.md', '03-brownfield/evaluation/10-b3-acceptance-test-map.md'],
    }
    for version, paths in maps.items():
        repo = ROOT / 'agentic-workshop' / VERSIONS[version][0]
        business = (repo / 'docs/business-rules.md').read_text(encoding='utf-8-sig')
        actual = set(re.findall(r'^\| `?([A-Z]+(?:-[A-Z]+)*-\d{3})`? \|', business, re.M))
        mapping = '\n'.join((ROOT / 'agentic-workshop' / p).read_text(encoding='utf-8-sig') for p in paths)
        missing_registry = sorted(actual - rules)
        missing_mapping = sorted(rule for rule in actual if rule not in mapping)
        functions = {node.name for p in (repo / 'tests').rglob('*.py')
                     for node in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig')))
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        modules = {p.stem for p in (repo / 'tests').rglob('*.py')}
        cited = set(re.findall(r'\btest_[A-Za-z0-9_]+', mapping)) - modules
        missing_functions = sorted(cited - functions)
        expected_rule_count = {'G1': 16, 'B0': 36, 'B1': 36, 'B2': 40, 'B3': 57}[version]
        if len(actual) != expected_rule_count:
            errors.append({'version': version, 'expected_rule_count': expected_rule_count, 'actual': len(actual)})
        if missing_registry or missing_mapping or missing_functions:
            errors.append({'version': version, 'missing_registry': missing_registry,
                           'missing_mapping': missing_mapping, 'missing_test_functions': missing_functions})
        results[version] = {'business_rules': len(actual), 'cited_test_functions': len(cited),
                            'maps': paths, 'missing_registry': missing_registry,
                            'missing_mapping': missing_mapping, 'missing_test_functions': missing_functions}
    ac_maps = {}
    for name, filename, prefix, expected_count in [
        ('G1', '01-greenfield/evaluation/06-acceptance-test-map.md', 'AC-G-', 15),
        ('B1', '03-brownfield/evaluation/08-b1-acceptance-test-map.md', 'AC-B1-', 7),
        ('B2', '03-brownfield/evaluation/09-b2-acceptance-test-map.md', 'AC-B2-', 13),
        ('B3', '03-brownfield/evaluation/10-b3-acceptance-test-map.md', 'AC-B3-', 19)]:
        content = (ROOT / 'agentic-workshop' / filename).read_text(encoding='utf-8')
        ids = sorted(set(re.findall(re.escape(prefix) + r'\d{3}', content)))
        ac_maps[name] = {'map': filename, 'ac_ids': ids, 'count': len(ids)}
        if len(ids) != expected_count:
            errors.append({'ac_map': name, 'expected': expected_count, 'actual': len(ids)})
    if len(rules) != 57 or results['B3']['business_rules'] != 57:
        errors.append({'registry_or_b3_rule_count': 'must be 57'})
    return {'status': 'PASS' if not errors else 'FAIL', 'registry_rule_count': len(rules), 'acceptance_maps': ac_maps,
            'versions': results, 'errors': errors,
            'limits': 'Rule ID coverage and named test symbol presence; not proof of complete assertion semantics'}


def frozen_sources():
    errors, results = [], {}
    for version, filename in [('B0', 'validation-evidence.json'), ('B1', '13-b1-validation-evidence.json'),
                              ('B2', '16-b2-validation-evidence.json'), ('B3', '19-b3-validation-evidence.json')]:
        baseline = ROOT / 'agentic-workshop/03-brownfield/evaluation' / filename
        expected = json.loads(baseline.read_text(encoding='utf-8-sig'))['source_sha256']
        repo = ROOT / 'agentic-workshop' / VERSIONS[version][0]
        changed = [name for name, digest in expected.items()
                   if not (repo / name).is_file() or file_hash(repo / name) != digest]
        results[version] = {'baseline': baseline.relative_to(ROOT).as_posix(),
                            'source_file_count': len(expected), 'changed_files': changed}
        if changed:
            errors.append({'version': version, 'changed_files': changed})
    return {'status': 'PASS' if not errors else 'FAIL', 'versions': results, 'errors': errors,
            'limits': 'Compare B0/B1/B2/B3 source bytes against previously accepted evidence'}


def command(python, args, cwd, env, logfile, timeout=120):
    started = time.monotonic()
    result = subprocess.run([str(python), '-X', 'utf8', *args], cwd=cwd, env=env,
                            text=True, encoding='utf-8', errors='replace',
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    logfile.write_text(result.stdout, encoding='utf-8')
    return {'command': [str(python.relative_to(ROOT)) if python.is_relative_to(ROOT) else str(python),
                        '-X', 'utf8', *args],
            'cwd': str(cwd.relative_to(ROOT)), 'returncode': result.returncode,
            'elapsed_seconds': round(time.monotonic() - started, 3),
            'log': str(logfile.relative_to(ROOT)) if logfile.is_relative_to(ROOT) else str(logfile),
            'log_sha256': file_hash(logfile)}


def validate_version(version, config, args, logs):
    relative, passes, skips, fails = config
    cwd = ROOT / 'agentic-workshop' / relative
    environment = args.env_root / f'{version.lower()}-env'
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    env = os.environ.copy()
    env['PYTHONPATH'] = str(cwd / 'src')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTEST_ADDOPTS'] = ''
    env.pop('PYTHONWARNINGS', None)
    checks = {}
    for name, command_args in [
        ('python', ['--version']), ('pip_check', ['-m', 'pip', 'check']),
        ('core_smoke', [str(ROOT / 'scripts/smoke' / f'smoke_{version.lower()}.py')]),
        ('uvicorn_health_openapi', [str(ROOT / 'scripts/smoke/server_probe.py')])]:
        checks[name] = command(python, command_args, cwd, env, logs / f'{version.lower()}-{name}.log')
    xmlpath = logs / f'{version.lower()}-pytest.xml'
    checks['pytest'] = command(python,
        ['-m', 'pytest', '-q', '-W', 'default', '-p', 'no:cacheprovider', f'--junitxml={xmlpath}'],
        cwd, env, logs / f'{version.lower()}-pytest.log')
    xml = ET.parse(xmlpath)
    testcases = xml.findall('.//testcase')
    actual_skips = [c for c in testcases if c.find('skipped') is not None]
    actual_failed = [c for c in testcases if c.find('failure') is not None or c.find('error') is not None]
    failed_ids = sorted(f"{c.attrib['classname'].replace('.', '/')}::{c.attrib['name']}"
                        for c in actual_failed)
    # pytest classname contains the module without .py; restore the manifest format.
    failed_ids = [node.replace('::', '.py::', 1) for node in failed_ids]
    skip_reasons = [c.find('skipped').attrib for c in actual_skips]
    count = {'passed': len(testcases) - len(actual_skips) - len(actual_failed),
             'skipped': len(actual_skips), 'failed': len(actual_failed)}
    manifest = json.loads((ROOT / 'agentic-workshop/03-brownfield/evaluation/06-intentional-failure-manifest.json').read_text(encoding='utf-8-sig'))
    gate = test_gate(count, failed_ids, skip_reasons, version, config, manifest)
    if version == 'G0':
        gate = gate and {c.attrib['name'] for c in actual_skips} == G0_SKIP_NAMES
    gate = gate and checks['pytest']['returncode'] == (1 if version == 'B0' else 0)
    pytest_text = (logs / f'{version.lower()}-pytest.log').read_text(encoding='utf-8')
    warnings, warnings_valid = warning_gate(pytest_text)
    unknown_warning = not warnings_valid
    gate = gate and not unknown_warning
    gate = gate and not re.search(r'\b\d+ xpassed\b', pytest_text)
    gate = gate and all(checks[name]['returncode'] == 0 for name in checks if name != 'pytest')
    gate = gate and (logs / f'{version.lower()}-python.log').read_text(encoding='utf-8').startswith('Python 3.13.')
    return {'status': 'PASS' if gate else 'FAIL', 'source': relative, 'checks': checks,
            'test_counts': count, 'failed_node_ids': failed_ids, 'skip_reasons': skip_reasons,
            'test_node_ids': [f"{c.attrib['classname'].replace('.', '/')}.py::{c.attrib['name']}" for c in testcases],
            'b0_manifest_exact_match': failed_ids == sorted(manifest) if version == 'B0' else None,
            'known_warning': 'Starlette BlockingPortal DeprecationWarning' if warnings and not unknown_warning else None,
            'warnings': warnings,
            'unknown_warning': unknown_warning,
            'source_sha256': {p.relative_to(cwd).as_posix(): file_hash(p) for p in sorted(cwd.rglob('*'))
                              if p.is_file() and not any(part in p.relative_to(cwd).parts
                                for part in ('.pytest_cache', '__pycache__', '.git'))}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-root', type=Path, default=ROOT / '.codex-tmp')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--logs', type=Path, default=ROOT / 'agentic-workshop/06-runbook/evaluation/p11-validation-logs')
    parser.add_argument('--static-only', action='store_true')
    parser.add_argument('--refresh-static', action='store_true', help='Refresh static sections in existing full evidence, retaining technical run timestamps/logs')
    args = parser.parse_args()
    if args.output is None:
        name = 'p11-static-validation-evidence.json' if args.static_only else 'p11-validation-evidence.json'
        args.output = ROOT / 'agentic-workshop/06-runbook/evaluation' / name
    args.env_root, args.output, args.logs = args.env_root.resolve(), args.output.resolve(), args.logs.resolve()
    args.logs.mkdir(parents=True, exist_ok=True)
    evidence = {'executed_utc': datetime.now(timezone.utc).isoformat(),
                'installation': ('NOT RUN: static checks only' if args.static_only else
                                 'NOT RUN: existing independent environments; pip check executed'),
                'human_rehearsal': 'NOT RUN', 'agent_service_availability': 'NOT RUN',
                'coverage': 'STATIC_ONLY' if args.static_only else 'SIX_VERSION_TECHNICAL',
                'documents': documents(), 'traceability': traceability(), 'frozen_sources': frozen_sources(), 'versions': {}}
    if args.refresh_static:
        previous = json.loads(args.output.read_text(encoding='utf-8'))
        evidence['executed_utc'] = previous['executed_utc']
        evidence['static_refreshed_utc'] = datetime.now(timezone.utc).isoformat()
        evidence['versions'] = previous['versions']
        if set(evidence['versions']) != set(VERSIONS):
            raise ValueError('Cannot refresh full evidence lacking six version results')
        for version, result in evidence['versions'].items():
            repo = ROOT / 'agentic-workshop' / VERSIONS[version][0]
            current_sources = {p.relative_to(repo).as_posix(): file_hash(p)
                               for p in sorted(repo.rglob('*')) if p.is_file()
                               and not any(part in p.relative_to(repo).parts
                                           for part in ('.pytest_cache', '__pycache__', '.git'))}
            if current_sources != result.get('source_sha256'):
                raise ValueError(f'{version} source changed since technical validation; rerun full validation')
            for check in result.get('checks', {}).values():
                logfile = ROOT / check['log']
                if file_hash(logfile) != check['log_sha256']:
                    raise ValueError(f'Technical log changed: {logfile}')
    elif not args.static_only:
        for version, config in VERSIONS.items():
            print(f'Validating {version}', flush=True)
            try:
                evidence['versions'][version] = validate_version(version, config, args, args.logs)
            except Exception as error:
                evidence['versions'][version] = {'status': 'FAIL', 'error': str(error)}
            print(f"{version}: {evidence['versions'][version]['status']}", flush=True)
    # Documents can be added concurrently during the technical run; scan final state.
    evidence['documents'] = documents()
    success = (evidence['documents']['status'] == 'PASS' and evidence['traceability']['status'] == 'PASS'
               and evidence['frozen_sources']['status'] == 'PASS' and all(
        result['status'] == 'PASS' for result in evidence['versions'].values()))
    evidence['status'] = ('STATIC_PASS' if args.static_only else 'PASS') if success else 'FAIL'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': evidence['status'], 'documents': evidence['documents'],
                      'output': str(args.output)}, ensure_ascii=False))
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
