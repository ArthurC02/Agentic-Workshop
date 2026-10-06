"""Read-only review of the nine documented consistency corrections.

Writes new current evidence, never edits historical P9/P10 JSON or app sources.
No app suite, package build, dependency installation, or human rehearsal runs.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import zipfile

import build_delivery
from validate_workshop import ROOT, VERSIONS, documents, file_hash, frozen_sources, traceability

WORKSHOP = ROOT / 'agentic-workshop'


def display(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def read(relative):
    return (WORKSHOP / relative).read_text(encoding='utf-8-sig')


def compact(text):
    return re.sub(r'\s+', '', text)


def check(result, identifier, criterion, passed, files, details=None):
    result.append({'id': identifier, 'criterion': criterion,
                   'status': 'PASS' if passed else 'FAIL', 'files': files,
                   'details': details})


def version_sources():
    previous = json.loads((WORKSHOP / '06-runbook/evaluation/p11-validation-evidence.json').read_text(encoding='utf-8'))
    results = {}
    for version, config in VERSIONS.items():
        repo = WORKSHOP / config[0]
        actual = {p.relative_to(repo).as_posix(): file_hash(p) for p in sorted(repo.rglob('*'))
                  if p.is_file() and not any(part in p.relative_to(repo).parts
                    for part in ('.git', '__pycache__', '.pytest_cache'))}
        expected = previous['versions'][version]['source_sha256']
        results[version] = {'status': 'PASS' if actual == expected else 'FAIL',
                            'files': len(actual), 'source_sha256': actual}
    return {'status': 'PASS' if all(r['status'] == 'PASS' for r in results.values()) else 'FAIL',
            'baseline': 'p11-validation-evidence.json technical source manifests', 'versions': results}


def historical_document_changes():
    """Report changes as current corrections, not a claim of historical immutability."""
    changed, unchanged, evidence_hashes = [], [], {}
    for relative, base in [
        ('04-digital-worker/evaluation/07-governance-validation-evidence.json', WORKSHOP / '04-digital-worker'),
        ('06-runbook/evaluation/p10-validation-evidence.json', ROOT)]:
        path = WORKSHOP / relative
        evidence_hashes[relative] = file_hash(path)
        previous = json.loads(path.read_text(encoding='utf-8'))['source_sha256']
        for name, digest in previous.items():
            current = base / name
            actual = file_hash(current) if current.is_file() else None
            record = {'file': current.relative_to(ROOT).as_posix(), 'historical_sha256': digest,
                      'current_sha256': actual}
            (unchanged if actual == digest else changed).append(record)
    return {'historical_evidence_sha256': evidence_hashes, 'changed_documents': changed,
            'unchanged_document_count': len(unchanged),
            'interpretation': 'Prior PASS describes prior files; changed documents have new current semantic evidence here. Historical JSON is not rewritten.'}


def corrections(package_output):
    checks, scoped = [], set()
    def record(identifier, criterion, passed, files, details=None):
        scoped.update(files)
        check(checks, identifier, criterion, passed, files, details)

    manifest = json.loads(build_delivery.MANIFEST.read_text(encoding='utf-8'))
    b0 = next(p for p in manifest['packages'] if p['id'] == 'participant-29-b0')
    package_file = package_output / 'participant-29-b0.zip'
    try:
        with zipfile.ZipFile(package_file) as archive:
            contents = {name: archive.read(name) for name in archive.namelist()}
        build_delivery.content_policy(b0, contents)
        record('C-01-02', 'Actual B0 ZIP hides generated bug/priority answers and preserves two controlled gap documents plus three safe ADRs',
               True, ['scripts/package-manifest.json', 'scripts/build_delivery.py'],
               {'zip': display(package_file), 'zip_sha256': file_hash(package_file),
                'controlled_files': list(build_delivery.B0_CONTEXT_FILES)})
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        record('C-01-02', 'Actual B0 ZIP content policy', False,
               ['scripts/package-manifest.json', 'scripts/build_delivery.py'], str(error))

    shared = '03-brownfield/participant/04-shared-context-template.md'
    text = compact(read(shared))
    early = text.split('##任務揭露後補填')[0]
    record('C-03', '39–44 Shared Context gathers common facts; task-specific scope/plan/approval follows B1 reveal at44',
           all(s in text for s in ['39–44', '44分鐘', '尚未揭露B1', '不修改程式', '任務揭露後補填'])
           and '|任務ID／起點版本／規則來源|' not in early,
           ['agentic-workshop/' + shared])

    level_files = ['03-brownfield/participant/task-cards/03-b3-group-booking.md',
                   '04-digital-worker/participant/05-delivery-template.md',
                   '05-retrospective/participant/maturity-comparison.md']
    level_results = {}
    for relative in level_files:
        rows = [compact(line) for line in read(relative).splitlines() if re.search(r'Level\s*1', line)]
        relevant = [line.split('Level2')[0] for line in rows]
        valid = any(('Gate1／2' in line or '理解／設計Gate' in line)
                    and ('合理Impact' in line or '合理影響分析' in line or re.search(r'影響分析.{0,15}合理', line))
                    and any(token in line for token in ('完整TestStrategy', '完整測試策略', '測試策略完整'))
                    and ('未完成' in line or '尚未完成' in line) for line in relevant)
        level_results[relative] = valid
    delivery = compact(read(level_files[1]))
    allowance = any(token in delivery for token in ('尚未修改', '未修改', '無程式修改', '沒有程式修改', '可無修改'))
    unrun = any(token in delivery for token in ('NOTRUN', '未執行', '無已執行測試'))
    review_file = '04-digital-worker/participant/04-review-checklist.md'
    review = compact(read(review_file))
    review_allows_analysis = 'Level1' in review and '未執行測試' in review and ('尚無修改' in review or '無修改' in review)
    gate_file = '04-digital-worker/participant/03-approval-gates.md'
    gates = compact(read(gate_file))
    gate_allows_analysis = 'Level1' in gates and ('未執行' in gates or '無修改' in gates or '尚無' in gates)
    cue_file = '04-digital-worker/facilitator/02-approval-gate-cues.md'
    cues = compact(read(cue_file))
    cue_allows_analysis = 'Level1' in cues and ('未執行' in cues or '無修改' in cues or '尚無' in cues)
    audit_file = '04-digital-worker/evaluation/03-digital-worker-audit-template.md'
    audit = compact(read(audit_file))
    audit_allows_analysis = '無修改' in audit and '未執行' in audit
    record('C-04', 'Level1 requires understanding/design gates, reasonable impact and complete test strategy; delivery permits no code changes/tests not run',
           all(level_results.values()) and allowance and unrun and review_allows_analysis
           and gate_allows_analysis and cue_allows_analysis and audit_allows_analysis,
           ['agentic-workshop/' + p for p in [*level_files, review_file, gate_file, cue_file, audit_file]],
           {'level_definition_checks': level_results,
            'delivery_allows_no_changes': allowance, 'delivery_allows_tests_not_run': unrun,
            'review_allows_analysis': review_allows_analysis, 'gate3_allows_analysis': gate_allows_analysis,
            'facilitator_cue_allows_analysis': cue_allows_analysis, 'audit_allows_analysis': audit_allows_analysis})

    recovery = '04-digital-worker/facilitator/04-intervention-rules.md'
    text = compact(read(recovery))
    record('C-05', 'B3 does not switch versions midway; Recovery only at52 intoB2 and63 intoB3, then analysis/review fallback',
           all(s in text for s in ['不在B3中途切換版本', '52分鐘進B2', '63分鐘進B3', '分析／Review降級']),
           ['agentic-workshop/' + recovery])

    errata = '03-brownfield/evaluation/22-b2-documentation-errata.md'
    text = compact(read(errata))
    enum_file = '03-brownfield/evaluation/reference-solutions/b2-best-discount-policy/src/smart_ticket/domain/discounts.py'
    actual_enum = read(enum_file)
    record('C-06', 'Frozen B2 example FULL_FARE correction to ADULT is explicit; docs/API/AC sync qualification is distinguished from runtime PASS',
           all(s in text for s in ['FULL_FARE', 'ADULT', 'AC-B2-013'])
           and ('歷史' in text or '凍結' in text)
           and ('漏掉' in text or '落差' in text or '不符合' in text or '例外' in text)
           and ('不能' in text or '不代表' in text)
           and ('功能／Enum／測試結果保持有效' in text or '功能' in text and 'PASS' in text)
           and bool(re.search(r'ADULT\s*=\s*[\"\']ADULT[\"\']', actual_enum))
           and 'FULL_FARE' not in actual_enum and '(100, DiscountType.ADULT)' in actual_enum,
           ['agentic-workshop/' + errata, 'agentic-workshop/' + enum_file])

    mission = '01-greenfield/participant/01-mission-brief.md'
    text = compact(read(mission))
    runbook = read('06-runbook/workshop-runbook.md')
    opening = next(compact(line) for line in runbook.splitlines() if '|00–07|' in compact(line))
    record('C-07', 'Mission brief distributed at7; opening remains verbal introduction and does not distribute task documents early',
           ('7分鐘' in text or '第7分鐘' in text or '07分鐘' in text)
           and '口頭' in opening and '7分鐘' in opening,
           ['agentic-workshop/' + mission, 'agentic-workshop/06-runbook/workshop-runbook.md'])

    card = '04-digital-worker/participant/06-exception-response-card.md'
    text = compact(read(card))
    record('C-08', 'Exception response card is blank at63, activated69–70; does not prefill SQLite answer',
           '63' in text and '69' in text and ('空白' in text or '空模板' in text)
           and not any(s in text for s in ['SQLite', 'In-Memory', '資料庫'])
           and '選擇與依據：____' in text and '決策：____' in text,
           ['agentic-workshop/' + card])

    matrix = '03-brownfield/evaluation/11-b0-to-b3-version-matrix.md'
    text = compact(read(matrix))
    record('C-09', 'Version matrix labels prior P8 scope historically and links current correction report as the latest status chain',
           ('歷史' in text or '當時' in text or '截至P8' in text) and 'consistency-correction-report.md' in text
           and 'P11' in text,
           ['agentic-workshop/' + matrix])
    return checks, scoped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=WORKSHOP / '06-runbook/evaluation/consistency-correction-evidence.json')
    parser.add_argument('--package-output', type=Path)
    args = parser.parse_args()
    package_output = args.package_output or ROOT / 'dist/p11-candidate' / file_hash(build_delivery.MANIFEST)[:16]
    checks, scoped = corrections(package_output.resolve())
    evidence = {'executed_utc': datetime.now(timezone.utc).isoformat(), 'checks': checks,
                'documents': documents(), 'traceability': traceability(), 'frozen_app_sources': frozen_sources(),
                'six_version_sources_unchanged_since_technical_run': version_sources(),
                'historical_p9_p10_document_comparison': historical_document_changes(),
                'current_checked_sha256': {name: file_hash(ROOT / name) for name in sorted(scoped)},
                'app_suite_rerun': 'NOT RUN: exact frozen source comparison; prior actual technical evidence retained',
                'human_rehearsal': 'NOT RUN',
                'limits': 'Explicit review issue checks and actual B0 ZIP policy; not general semantic proof or human rehearsal.'}
    success = all(c['status'] == 'PASS' for c in checks) and all(evidence[name]['status'] == 'PASS'
        for name in ['documents', 'traceability', 'frozen_app_sources', 'six_version_sources_unchanged_since_technical_run'])
    evidence['status'] = 'PASS' if success else 'FAIL'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': evidence['status'], 'checks': [{'id': c['id'], 'status': c['status']} for c in checks]}, ensure_ascii=False))
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
