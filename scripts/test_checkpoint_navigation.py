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
