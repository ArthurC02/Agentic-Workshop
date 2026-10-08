export const meta = {
  name: 'curriculum-review',
  description: 'Two-loop curriculum review: outer loop (progression, knowledge points) + inner loop per task segment, verify findings, fix per segment',
  whenToUse: 'Review a whole edition after a content redesign or before release. args: {"scope":"main"|"dlc"}.',
  phases: [
    { title: 'Review', detail: 'one outer-loop reviewer for the edition + one inner-loop reviewer per segment' },
    { title: 'Verify', detail: 'check each segment\'s findings against the files; drop false positives' },
    { title: 'Fix', detail: 'one fixer per segment applies confirmed findings' },
    { title: 'Consistency', detail: 'cross-segment alignment and checks' },
  ],
}

const SKILL = '.claude/skills/curriculum-review/SKILL.md and .claude/skills/course-authoring/SKILL.md'
const M = 'agentic-workshop/materials'
const D = 'agentic-workshop/materials-dlc'
const SEGMENTS = {
  main: [
    { key: 'opening', files: `${M}/participant-runbook/content/00–02, slides 10-opening.html` },
    { key: 'greenfield', files: `${M}/participant-runbook/content/10–16, 01-greenfield/participant/*, slides 20-greenfield.html, 01-greenfield/facilitator/*` },
    { key: 'timeskip-analysis-shared', files: `${M}/participant-runbook/content/30–39, 02-time-skip/**, 03-brownfield/participant/01–04, slides 30-timeskip.html 40-analysis-shared.html, 03-brownfield/facilitator/01–02` },
    { key: 'b1', files: `${M}/participant-runbook/content/44-b1.md 53-recovery-b1.md, task-cards/01-*, slides 50-b1.html, 03-brownfield/facilitator/04–07 (B1 parts)` },
    { key: 'b2', files: `${M}/participant-runbook/content/52-b2.md 67-recovery-b2.md, task-cards/02-*, slides 55-b2.html, 03-brownfield/facilitator/04–07 (B2 parts)` },
    { key: 'b3', files: `${M}/participant-runbook/content/60–66, task-cards/03-*, 04-digital-worker/participant/01–05, slides 60-b3-digital-worker.html, 04-digital-worker/facilitator/*` },
    { key: 'delivery-retro', files: `${M}/participant-runbook/content/70, 80, 88, 05-retrospective/**, slides 70-delivery.html 80-retrospective.html` },
  ],
  dlc: [
    { key: 'opening-d1', files: `${D}/participant-runbook/content/00–19, worksheets d1-*, slides 10-opening.html 20-d1.html` },
    { key: 'd2', files: `${D}/participant-runbook/content/20–29, worksheets d2-*, slides 30-d2.html 40-break.html` },
    { key: 'd3', files: `${D}/participant-runbook/content/30–59, worksheets d3-*, scenarios/*, slides 50-d3a.html 55-d3b.html 60-d3c.html` },
    { key: 'd4-retro', files: `${D}/participant-runbook/content/60–88, worksheets d4-*, slides 70-d4.html 80-retro.html, ${D}/CHECKPOINTS.md` },
  ],
}
const scope = (args && args.scope) || 'main'
const segs = SEGMENTS[scope]
if (!segs) throw new Error('args.scope must be "main" or "dlc"')
const extra = scope === 'dlc' ? ' Facilitator guide: agentic-workshop/07-dlc-ddd/facilitator/facilitator-guide.md (your segment\'s sections). Tools are in agentic-workshop/07-dlc-ddd/participant/tools (read only).' : ''

const FINDINGS = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      segment: { type: 'string', description: `one of: ${segs.map(s => s.key).join(', ')}` },
      file: { type: 'string' }, where: { type: 'string' },
      loop: { type: 'string', enum: ['outer', 'inner'] },
      problem: { type: 'string' }, fix: { type: 'string' },
    }, required: ['segment', 'file', 'where', 'loop', 'problem', 'fix'] } },
  },
  required: ['findings'],
}
const VERIFIED = {
  type: 'object',
  properties: { confirmed: FINDINGS.properties.findings, rejected: { type: 'array', items: { type: 'string' } } },
  required: ['confirmed', 'rejected'],
}

phase('Review')
const outerP = agent(
  `Outer-loop curriculum review of the ${scope} edition. Read ${SKILL}. Read every Runbook page in file-name order (resolve includes) plus slide speaker notes.${extra}
Build a private map: knowledge point → first introduced → first used → later deepening. Report only real problems against the outer-loop checklist, each assigned to the segment where the fix belongs. Do not edit files.`,
  { label: 'outer', phase: 'Review', schema: FINDINGS })
const innerP = segs.map(s => agent(
  `Inner-loop task review, segment "${s.key}" of the ${scope} edition. Read ${SKILL}. Your files: ${s.files}.${extra}
Walk the task as a learner who pastes each prompt in order: check every item of the inner-loop checklist, and verify facts against the code package / tools in the repo. Report only real problems (segment="${s.key}"). Do not edit files.`,
  { label: `inner:${s.key}`, phase: 'Review', schema: FINDINGS }))
const all = (await Promise.all([outerP, ...innerP])).filter(Boolean).flatMap(r => r.findings)
log(`${all.length} raw findings`)

const results = await pipeline(segs,
  s => {
    const mine = all.filter(f => f.segment === s.key)
    if (!mine.length) return { confirmed: [], rejected: [] }
    return agent(`Verify these curriculum-review findings for segment "${s.key}" by opening the cited files. Reject anything already correct, speculative, or that would break a constraint in ${SKILL}. Findings: ${JSON.stringify(mine)}`,
      { label: `verify:${s.key}`, phase: 'Verify', schema: VERIFIED })
  },
  (v, s) => {
    if (!v || !v.confirmed.length) return { segment: s.key, fixed: 'nothing to fix', rejected: v ? v.rejected : [] }
    return agent(`Apply these confirmed findings for segment "${s.key}". Read ${SKILL} (fix rules). Edit only this segment's files: ${s.files}. Use Edit, preserve line endings, no builds. Return a short list of what you changed. Findings: ${JSON.stringify(v.confirmed)}`,
      { label: `fix:${s.key}`, phase: 'Fix' }).then(fixed => ({ segment: s.key, fixed, rejected: v.rejected }))
  })

phase('Consistency')
const check = scope === 'main'
  ? 'uv run --no-project --python 3.13 python -X utf8 scripts/validate_consistency_corrections.py (must PASS) and uv run --no-project --python 3.13 python -X utf8 scripts/build_materials.py --edition main --check'
  : 'uv run --no-project --python 3.13 python -X utf8 scripts/build_materials.py --edition dlc --check'
const consistency = await agent(
  `Cross-segment consistency after a curriculum-review fix pass (${scope}). Read ${SKILL}. Per-segment results: ${JSON.stringify(results)}
Check that knowledge points referenced across segments still line up (introduced before use, same names), checkpoint titles match across runbook/slides${scope === 'dlc' ? '/CHECKPOINTS.md' : ''}, and the glossary covers new terms. Fix mismatches. Then run ${check} (DIFFERS is expected before rebuild; parse errors, forbidden hits or external URLs are not). Return a short summary and anything left for the human.`,
  { label: 'consistency', phase: 'Consistency' })

return { raw: all.length, results, consistency }
