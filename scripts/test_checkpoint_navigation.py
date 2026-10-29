"""Exercise the offline Runbook checkpoint links in a real browser."""
import json
import tempfile
import unittest
from pathlib import Path

from verify_typography import ROOT, probe, report_of, wrap


class CheckpointNavigationTest(unittest.TestCase):
    def test_presenter_cue_tracks_slide(self):
        script = """
const assert = (ok, msg) => { if (!ok) throw Error(msg); };
const slides = [...DK.slides];
for (let i = 0; i < slides.length; i++) {
  DK.go(i); await sleep(20);
  for (const row of document.querySelectorAll('.pv-now-row')) {
    const privateCode = row.classList.contains('is-private');
    assert(row.textContent.includes(privateCode ? '只私下提供：' : '全場公布：'), 'code audience missing');
    assert(privateCode === /RESUME-/.test(row.querySelector('code').textContent), 'private code marked public');
  }
  const cue = document.querySelector('.pv-learner-cue');
  const flow = slides[i].querySelector('.cp-flow');
  const start = slides[i].querySelector('.seg-start');
  assert(!!cue === !!(flow || start), 'stale or missing cue on slide ' + i);
  if (flow) {
    assert(cue.querySelectorAll('li').length === flow.children.length, 'missing actions');
    assert(cue.textContent.includes(slides[i].querySelector('.kicker').textContent), 'wrong checkpoint');
    assert(cue.textContent.includes(slides[i].querySelector('.cp-next').textContent), 'wrong next step');
    const judge = slides[i].querySelector('.cp-judge');
    if (judge) assert(cue.textContent.includes(judge.textContent), 'missing decision');
  }
}
return {ok: true};
"""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            source = ROOT / 'agentic-workshop/materials/facilitator-deck/facilitator-deck.html'
            presenter = work / 'presenter.html'
            presenter.write_text(source.read_text(encoding='utf-8').replace(
                '<head>', "<head><script>location.hash = '#presenter';</script>"), encoding='utf-8')
            self.assertEqual(report_of(probe(presenter, wrap(script, 12), '1400,1000', work)), {'ok': True})

    def test_primary_route_and_checklist_scope(self):
        base = ROOT / 'agentic-workshop/materials'
        codes = json.loads((base / 'unlock-codes.json').read_text(encoding='utf-8'))['groups']
        script = """
const assert = (ok, msg) => { if (!ok) throw Error(msg); };
const go = async id => { location.hash = '#p-' + id; await sleep(80); };
const unlock = async id => assert(await RB.unlock(id, CODES.find(g => g.id === id).code), 'unlock failed');
await unlock('b2'); await go('b2');
document.querySelector('.rb-checkpoints a:last-child').click(); await sleep(80);
let next = document.querySelector('.rb-pager-next');
assert(next.getAttribute('href') === '#p-b3', 'normal route leads into Recovery');
assert(next.textContent.includes('看投影解鎖'), 'locked handoff lacks a wait cue');
assert(!document.querySelector('.rb-nav-link[data-page="recovery-b1"]').classList.contains('is-unlocked'), 'normal code unlocked Recovery');
next.click(); await sleep(80); await unlock('b3');
document.querySelector('.rb-checkpoints a:last-child').click(); await sleep(80);
assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-delivery', 'exception card repeats after B3');
await go('delivery');
assert(document.querySelector('.rb-pager-prev').getAttribute('href') === '#p-b3', 'reverse route leads into an optional page');
document.activeElement.blur();
document.dispatchEvent(new KeyboardEvent('keydown', {key: '['})); await sleep(80);
assert(location.hash === '#p-b3', 'keyboard route differs from pager');
document.querySelectorAll('.rb-checkpoints a')[3].click(); await sleep(80);
const gate = document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href');
document.querySelector('.rb-nav-link[data-page="b3-exception-card"]').click(); await sleep(80);
assert(location.hash === '#p-b3-exception-card', 'exception card no longer reachable');
assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-b3', 'exception card skips remaining Gates');
document.querySelector('.rb-pager-next').click(); await sleep(80);
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === gate, 'exception return lost original Gate');
await unlock('recovery-b1');
document.querySelector('.rb-nav-link[data-page="recovery-b1"]').click(); await sleep(80);
assert(document.querySelector('.rb-nav-link.is-current').classList.contains('is-unlocked'), 'private Recovery unavailable');
assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-b2', 'B1 Recovery skips B2');
await unlock('recovery-b2'); await go('recovery-b2');
assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-b3', 'B2 Recovery skips B3');
const checks = [...document.querySelectorAll('.rb-page input.rb-check')];
const progress = document.querySelector('.rb-progress');
assert(progress.hidden === (checks.length === 0), 'empty progress is visible');
assert(progress.getAttribute('aria-label').includes('勾選清單'), 'checklist claims course progress');
if (checks.length) {
  const checked = checks.filter(c => c.checked).length;
  assert(document.querySelector('.rb-progress-num').textContent === checked + '/' + checks.length, 'checklist count wrong');
  checks[0].checked = !checks[0].checked; checks[0].dispatchEvent(new Event('change'));
  assert(Number(progress.getAttribute('aria-valuenow')) === checks.filter(c => c.checked).length, 'checklist does not update');
}
return {ok: true};
"""
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(report_of(probe(base / 'participant-runbook/runbook.html',
                                            wrap(script, 12, 'const CODES = ' + json.dumps(codes) + ';'),
                                            '1440,900', Path(tmp))), {'ok': True})

    def test_locked_navigation_and_remembered_checkpoint(self):
        base = ROOT / 'agentic-workshop/materials'
        code = json.loads((base / 'unlock-codes.json').read_text(encoding='utf-8'))['groups'][0]
        script = """
const assert = (ok, msg) => { if (!ok) throw Error(msg); };
const data = JSON.parse(document.getElementById('rb-data').textContent);
const page = data.pages.find(p => p.group === CODE.id);
location.hash = '#p-' + page.id; await sleep(100);
assert(document.querySelector('.rb-checkpoints').hidden, 'locked page exposes steps');
assert(!await RB.unlock(CODE.id, 'incorrect-code'), 'wrong code accepted');
assert(await RB.unlock(CODE.id, CODE.code), 'unlock failed');
const links = [...document.querySelectorAll('.rb-checkpoint')];
assert(links.length >= 3, 'checkpoint links missing');
links[2].focus();
links[2].click(); await sleep(100);
const href = links[2].getAttribute('href');
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === href, 'active checkpoint wrong');
assert(document.activeElement.getAttribute('href') === href, 'checkpoint navigation lost keyboard focus');
assert(!document.querySelector(href).hidden, 'selected checkpoint hidden');
location.hash = '#p-' + data.pages[0].id; await sleep(100);
assert(document.querySelector('.rb-checkpoints').hidden, 'plain page has checkpoint links');
location.hash = '#p-' + page.id; await sleep(100);
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === href, 'checkpoint memory lost');
assert(document.documentElement.scrollWidth <= innerWidth, 'horizontal overflow');
return {ok: true};
"""
        for size in ('1440,900', '390,844'):
            with self.subTest(size=size), tempfile.TemporaryDirectory() as tmp:
                result = report_of(probe(base / 'participant-runbook/runbook.html',
                                        wrap(script, 12, 'const CODE = ' + json.dumps(code) + ';'),
                                        size, Path(tmp)))
                self.assertEqual(result, {'ok': True})


if __name__ == '__main__':
    unittest.main()
