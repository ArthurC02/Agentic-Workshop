"""Browser regressions for learner interactions shared by both editions."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from verify_typography import ROOT, probe, report_of, wrap


class RunbookUXTest(unittest.TestCase):
    def test_early_gate_decision_keeps_the_next_gate(self):
        self.check('materials', """
const c = CODES.find(c => c.id === 'b3'); await RB.unlock(c.id, c.code);
location.hash = '#p-b3'; await sleep(80);
document.querySelectorAll('.rb-checkpoint')[2].click(); await sleep(80);
const gate = document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href');
const nextGate = document.querySelectorAll('.rb-checkpoint')[3].getAttribute('href');
const formLink = [...document.querySelectorAll('.rb-checkpoint')].find(a => a.textContent.includes('B3 Gate 決策'));
formLink.click(); await sleep(80);
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === gate, 'recording Gate 1 loses Gate 1 context');
assert(document.querySelector('.rb-pager-next').getAttribute('href') === nextGate, 'recording Gate 1 skips Gate 2');
const field = document.querySelector('[id="rbf-b3-gates-gate1"]');
assert(field.getClientRects().length > 0, 'Gate decision is not visible');
field.value = '核准'; field.dispatchEvent(new Event('change'));
document.querySelector('.rb-decision-panel[open] .rb-context-return').click(); await sleep(80);
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === gate, 'decision return loses checkpoint');
assert(field.value === '核准', 'decision return resets the answer');
return {ok: true};
""")

    def test_shared_behavior_stays_in_sync(self):
        main = ROOT / 'agentic-workshop/materials'
        dlc = ROOT / 'agentic-workshop/materials-dlc'
        for relative in ('participant-runbook/template/runbook.js',
                         'participant-runbook/template/runbook.css',
                         'participant-runbook/template/runbook.template.html',
                         'facilitator-deck/src/js/20-deck-features.js'):
            def normalized(base):
                text = (base / relative).read_text(encoding='utf-8')
                text = re.sub(r'var returnPages = .*?;', 'var returnPages = EDITION_ROUTES;', text)
                return text.replace('smart-ticket-dlc-runbook-', 'smart-ticket-runbook-')
            with self.subTest(file=relative):
                self.assertEqual(normalized(main), normalized(dlc))

    def check(self, edition, script, size='1440,900'):
        base = ROOT / 'agentic-workshop' / edition
        codes = json.loads((base / 'unlock-codes.json').read_text(encoding='utf-8'))['groups']
        setup = ('const CODES = ' + json.dumps(codes) + ';'
                 'const assert = (ok, msg) => { if (!ok) throw Error(msg); };')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(report_of(probe(base / 'participant-runbook/runbook.html',
                                            wrap(script, 12, setup), size, Path(tmp))), {'ok': True})

    def test_reference_can_be_read_without_leaving_checkpoint(self):
        script = """
const dlc = CODES[0].id === 'dlc-opening';
const pid = dlc ? 'd3a' : 'b2';
const code = CODES.find(c => c.id === (dlc ? 'dlc-d3a' : 'b2'));
await RB.unlock(code.id, code.code);
location.hash = '#p-' + pid; await sleep(80);
document.querySelectorAll('.rb-checkpoint')[2].focus();
document.querySelectorAll('.rb-checkpoint')[2].click(); await sleep(80);
const current = document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href');
assert(document.activeElement.getAttribute('href') === current, 'checkpoint focus lost');
const article = document.querySelector('[data-page="' + pid + '"].rb-page');
const panel = article.querySelector('.rb-context-panel');
assert(panel && !panel.open, 'reference covers the current action');
const urgent = [...article.querySelectorAll('.rb-callout-title')].find(t => /^時間不夠|^用 Recovery/.test(t.textContent.trim()));
assert(urgent && !urgent.closest('details') && urgent.getClientRects().length > 0, 'time-sensitive fallback is folded away');
panel.open = true; await sleep(30);
assert(panel.querySelector('.rb-include').getClientRects().length > 0, 'task card is not readable');
assert(article.querySelectorAll('.rb-step:not([hidden])').length === 1, 'reference replaced the current checkpoint');
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === current, 'reference changed checkpoint');
panel.querySelector('.rb-context-return').click(); await sleep(80);
assert(!panel.open && document.activeElement.tagName === 'H3', 'reference return did not restore action focus');
assert(document.querySelector('.rb-checkpoint[aria-current]').getAttribute('href') === current, 'reference return lost checkpoint');
panel.open = false;
window.dispatchEvent(new Event('beforeprint'));
assert(panel.open, 'print hides task reference');
window.dispatchEvent(new Event('afterprint'));
assert(!panel.open, 'printing changed the reference state');
if (dlc) {
  const c = CODES.find(c => c.id === 'dlc-d2'); await RB.unlock(c.id, c.code);
  location.hash = '#p-d2'; await sleep(80);
  document.querySelectorAll('.rb-checkpoint')[1].click(); await sleep(80);
  const setup = document.querySelector('[data-page="d2"].rb-page .rb-context-panel');
  assert(setup.open && setup.textContent.includes('【貼到夥伴自己的 Agent 對話】'), 'partner setup hidden at first checkpoint');
}
return {ok: true};
"""
        for edition in ('materials', 'materials-dlc'):
            with self.subTest(edition=edition):
                self.check(edition, script)

    def test_decision_is_saved_before_leaving(self):
        script = """
for (const c of CODES.filter(c => !/Recovery/.test(c.label))) await RB.unlock(c.id, c.code);
const field = document.querySelector('.rb-form select:not([disabled])');
assert(field && field.value === '', 'decision is preselected');
const form = field.closest('.rb-form');
const fid = JSON.parse(form.querySelector('.rb-form-def').textContent).id;
field.value = field.options[1].value; field.dispatchEvent(new Event('change'));
const key = Object.keys(localStorage).find(k => k.endsWith('form:' + fid));
assert(key && JSON.parse(localStorage.getItem(key))[field.name] === field.value, 'latest decision lost on immediate departure');
const clear = form.querySelector('.rb-btn-danger'); clear.click(); clear.click();
await sleep(450);
assert(localStorage.getItem(key) === null, 'clear restored a pending save');
assert(field.value === '', 'clear left a decision selected');
const original = Storage.prototype.setItem;
Storage.prototype.setItem = function () { throw Error('blocked'); };
field.value = field.options[1].value; field.dispatchEvent(new Event('change'));
assert(form.querySelector('.rb-form-saved').textContent.includes('無法儲存'), 'save failure reported as success');
Storage.prototype.setItem = original;
return {ok: true};
"""
        for edition in ('materials', 'materials-dlc'):
            with self.subTest(edition=edition):
                self.check(edition, script)

    def test_keyboard_search_opens_fold_and_selects_last_result(self):
        script = """
const fold = document.querySelector('[data-page="welcome"] details');
assert(fold && !fold.open, 'missing folded tip fixture');
fold.querySelector('.rb-callout-body').appendChild(document.createTextNode(' UX-SEARCH-UNIQUE-3029 '));
await RB.unlock(CODES[0].id, CODES[0].code);
const input = document.querySelector('.rb-search-input');
input.value = 'UX-SEARCH-UNIQUE-3029'; input.dispatchEvent(new Event('input'));
assert(document.querySelectorAll('.rb-search-hit').length === 1, 'search fixture not indexed');
input.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter'})); await sleep(150);
assert(fold.open, 'keyboard search landed in a closed fold');
input.value = 'Agent'; input.dispatchEvent(new Event('input'));
const hits = [...document.querySelectorAll('.rb-search-hit')];
assert(hits.length > 1, 'missing multiple search results');
input.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowUp'}));
assert(hits[hits.length - 1].classList.contains('is-active'), 'ArrowUp skips the last result');
assert(input.getAttribute('aria-activedescendant') === hits[hits.length - 1].id, 'active search result not announced');
return {ok: true};
"""
        for edition in ('materials', 'materials-dlc'):
            with self.subTest(edition=edition):
                self.check(edition, script)

    def test_closed_mobile_navigation_is_not_focusable(self):
        script = """
const menu = document.querySelector('.rb-menu-btn');
const link = document.querySelector('.rb-nav-link');
menu.focus(); link.focus();
assert(document.activeElement === menu, 'keyboard enters offscreen navigation');
menu.click();
assert(document.activeElement.closest('.rb-sidebar'), 'opened drawer did not receive focus');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));
assert(document.activeElement === menu, 'Escape did not return to menu');
link.focus();
assert(document.activeElement === menu, 'closed drawer remains focusable');
return {ok: true};
"""
        for edition in ('materials', 'materials-dlc'):
            with self.subTest(edition=edition):
                self.check(edition, script, '390,844')

    def test_dlc_recovery_routes_and_independent_codes(self):
        self.check('materials-dlc', """
const routes = {'recovery-d1': 'd2', 'recovery-d2': 'd3a', 'recovery-d3a': 'd3b', 'recovery-d3b': 'd3c', 'recovery-d3c': 'd4'};
for (const c of CODES.filter(c => !/Recovery/.test(c.label))) await RB.unlock(c.id, c.code);
for (const [id, target] of Object.entries(routes)) {
  const link = document.querySelector('.rb-nav-link[data-page="' + id + '"]');
  assert(link.classList.contains('is-locked'), 'public code opened Recovery');
  const c = CODES.find(c => c.id === 'dlc-rec-' + id.slice(9));
  assert(await RB.unlock(c.id, c.code), 'Recovery code rejected');
  location.hash = '#p-' + id; await sleep(60);
  assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-' + target, 'wrong Recovery return');
}
location.hash = '#p-d1'; await sleep(60);
document.querySelector('.rb-checkpoints a:last-child').click(); await sleep(60);
assert(document.querySelector('.rb-pager-next').getAttribute('href') === '#p-d2', 'ordinary route enters Recovery');
return {ok: true};
""")


if __name__ == '__main__':
    unittest.main()
