export const meta = {
  name: 'rehearsal',
  description: 'Dry-run the workshop as a learner: one agent per segment group pastes Runbook prompts into a sandbox built from candidate packages, then findings are merged',
  whenToUse: 'After content changes or before release, to prove prompts are runnable. args: {"scope":"main"|"dlc"}.',
  phases: [
    { title: 'Rehearse', detail: 'one learner+Agent simulation per segment group, sandboxed' },
    { title: 'Merge', detail: 'dedupe and rank findings across groups' },
  ],
}

const SKILL = '.claude/skills/rehearsal/SKILL.md'
const GROUPS = {
  main: ['greenfield', 'brownfield', 'b3-delivery-retro'],
  dlc: ['open-d1-d2', 'd3a', 'd3b', 'd3c', 'd4-retro'],
}
const scope = (args && args.scope) || 'main'
const groups = GROUPS[scope]
if (!groups) throw new Error('args.scope must be "main" or "dlc"')

const FINDINGS = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      where: { type: 'string', description: 'page file + checkpoint heading' },
      severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
      what: { type: 'string' }, fix: { type: 'string' },
    }, required: ['where', 'severity', 'what', 'fix'] } },
    worked_well: { type: 'array', items: { type: 'string' } },
  },
  required: ['findings', 'worked_well'],
}

phase('Rehearse')
const runs = await parallel(groups.map(g => () => agent(
  `Rehearse the ${scope} edition, segment group "${g}". Read ${SKILL} and follow its brief and its segment table exactly. Never edit the repo. Delete your sandbox at the end.`,
  { label: `rehearse:${g}`, phase: 'Rehearse', schema: FINDINGS })))
const done = runs.map((r, i) => r && { group: groups[i], ...r }).filter(Boolean)
const missing = groups.filter((_, i) => !runs[i])
if (missing.length) log(`no report from: ${missing.join(', ')}`)

phase('Merge')
const merged = await agent(
  `Merge these rehearsal findings for the ${scope} edition. Deduplicate them, rank them blockers first, and group them by the file that needs the fix. Keep each fix to one line. Findings: ${JSON.stringify(done)}`,
  { label: 'merge', phase: 'Merge' })

return { groups: done, missing, merged }
