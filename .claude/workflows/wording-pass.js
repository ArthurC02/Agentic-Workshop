export const meta = {
  name: 'wording-pass',
  description: 'Plain-language pass over workshop materials: parallel review+edit per file group, then a consistency check',
  whenToUse: 'Make a whole edition (main or dlc) or a file list plain Traditional Chinese with no unexplained abbreviations. args: {"scope":"main"|"dlc"} or {"files":[...]}.',
  phases: [
    { title: 'Edit', detail: 'one agent per non-overlapping file group, reviews and edits under the shared spec' },
    { title: 'Consistency', detail: 'one agent aligns terms, checkpoint titles and glossary across groups' },
  ],
}

const SPEC = '.claude/skills/plain-language-review/wording-spec.md'
const SKILL = '.claude/skills/plain-language-review/SKILL.md'
const M = 'agentic-workshop/materials'
const D = 'agentic-workshop/materials-dlc'
const GROUPS = {
  main: [
    { name: 'runbook-front', files: `${M}/participant-runbook/content/ 00–16, 53, 67 (*.md)` },
    { name: 'runbook-back+glossary', files: `${M}/participant-runbook/content/ 30–80 and 88-glossary.md`, glossary: true },
    { name: 'deck', files: `${M}/facilitator-deck/src/slides/*.html (screen text; notes only where read aloud)` },
    { name: 'speech', files: `${M}/speech/**/README.md, ${M}/speech/01-greenfield/src/slides.json (text values only, keep JSON valid), ${M}/speech/01-greenfield/practice/idea.md` },
  ],
  dlc: [
    { name: 'runbook-front', files: `${D}/participant-runbook/content/ 00–29 (*.md)` },
    { name: 'runbook-back+glossary', files: `${D}/participant-runbook/content/ 30–88 including 88-glossary.md`, glossary: true },
    { name: 'deck', files: `${D}/facilitator-deck/src/slides/*.html and ${D}/CHECKPOINTS.md` },
    { name: 'handouts', files: 'agentic-workshop/07-dlc-ddd/participant/ README.md, scenarios/*.md, worksheets/*.md, tools/README.md (not repository/)' },
  ],
}

const groups = args && args.files
  ? [{ name: 'files', files: args.files.join(', '), glossary: true }]
  : GROUPS[(args && args.scope) || 'main']
if (!groups) throw new Error('args.scope must be "main" or "dlc", or pass args.files')

const REPORT = {
  type: 'object',
  properties: {
    changed: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, edits: { type: 'integer' } }, required: ['path', 'edits'] } },
    skipped: { type: 'array', items: { type: 'string' }, description: 'suggestions deliberately not applied, with reason' },
    checkpoint_renames: { type: 'array', items: { type: 'string' }, description: 'old → new checkpoint titles, if any' },
    glossary_gaps: { type: 'array', items: { type: 'string' } },
    out_of_scope: { type: 'array', items: { type: 'string' } },
  },
  required: ['changed', 'skipped', 'checkpoint_renames', 'glossary_gaps', 'out_of_scope'],
}

phase('Edit')
const reports = await parallel(groups.map(g => () => agent(
  `Plain-language pass. Read ${SKILL} and ${SPEC} first and follow them strictly.
Your files (edit only these): ${g.files}.
${g.glossary ? 'You also own the glossary for this edition: add entries for terms your files introduce.' : 'Do not edit the glossary; list missing terms in glossary_gaps.'}
Review every learner-visible sentence, then edit in place: expand abbreviations at first use, add Chinese to English working terms, rewrite bureaucratic phrasing, fix contradictions. Do not run builds.
Report what you changed, what you skipped and why, any checkpoint title renames, glossary gaps, and issues outside your files.`,
  { label: `edit:${g.name}`, phase: 'Edit', schema: REPORT })))

const done = reports.map((r, i) => r && { group: groups[i].name, ...r }).filter(Boolean)
const failed = groups.filter((_, i) => !reports[i]).map(g => g.name)
if (failed.length) log(`groups with no report (not edited or agent failed): ${failed.join(', ')}`)

phase('Consistency')
const consistency = await agent(
  `Cross-group consistency check after a plain-language pass. Read ${SPEC}.
Group reports: ${JSON.stringify(done)}
1. Checkpoint renames must appear identically in runbook headings, runbook overview tables, deck data-title/kicker/callout and CHECKPOINTS.md (dlc) — fix any mismatch.
2. Add every glossary_gaps term to the edition glossary (88-glossary.md).
3. Grep the edited files for the same term expanded two different ways; align to the spec.
Edit files directly. Do not run builds. Return a short summary of fixes and anything left for the human.`,
  { label: 'consistency', phase: 'Consistency' })

return { groups: done, failed, consistency }
