---
name: course-authoring
description: The authoring standard for learner-facing workshop content (main course and DLC). Covers runbook pages, slides, participant handouts, and facilitator and evaluation docs. Use before writing or rewriting any checkpoint, prompt, form, slide or facilitator note, and give it to every sub-agent that edits course content.
---

# Course authoring standard (approved 2026-10-09; the rationale is in docs/planning/decisions-and-open-issues.md)

Audience: very junior engineers who may not know Python. They **never write or read code, and never type commands**. The Agent does all of that. Learners decide, approve, and verify through behavior and evidence.

## Goal order
1. Practice Agentic Coding techniques. This is the main point.
2. Experience the flow: Tool → Teammate → Digital Worker. The stages differ in **how the human intervenes**: step by step, by approving a plan, or only at Gates.
3. Evidence for organizational adoption. The Agent writes it into files; learners do not fill it in.

## Every segment page
- Top: a 「現在在做什麼」 callout with four lines: 情境 / 你的目標 / 今天的技巧 / 完成的樣子.
- Checkpoints: at most 3 (Greenfield and B3: at most 4). Use the title format `## 檢查點 N · 〈動詞句〉（第 a–b 分鐘）`. The overview is a short list, not a table.
- Each checkpoint follows this order:
  1. One or two sentences on what to do and why.
  2. A ```text prompt the learner can copy, which runs the step to completion.
  3. 「看到什麼算過關」, with 1–3 things that appear in the Agent's report.
  4. Optionally 「如果卡住」, a paste-ready rescue prompt.
  5. Optionally a 💬 討論一下 callout, discussed out loud with nothing written.
- **Prompts**:
  - Use the five parts: 目標 / 背景・要讀的檔 / 限制 / 輸出格式 / 停止條件.
  - Put commands and arguments in the prompt verbatim, for the Agent to run.
  - Name the record file (main course: `notes/<段落>.md`).
  - Never leave `〈 〉` blanks for learners. If the Agent needs information, it asks for it.
  - At decision points, the Agent proposes options with evidence and the learner replies briefly: 「同意」, 「選 B」, 「第 3 個不要」.
- **Forms**: at most one per segment, recording only the human's decision. Use select, checklist or checkbox fields, at most 3, plus at most 1 short text field. No form if there is no decision.
- End of page:
  - A 「## 完成後想一想」 section with 3 specific questions: observation → technique → extension toward the next segment or real work. Follow it with a 💬 callout and no form.
  - Then a 「這段學到的技巧」 callout.

## Knowledge points (progressive scaffolding)
- Introduce each concept, term, file convention, or report field at its **first need**. Use a `技巧：〈名稱〉` or `新概念：〈名稱〉` callout of 1–3 sentences.
- The opening is a roadmap only.
- Never require a point that has not been introduced. Text addressed only to the Agent gets the note 「這段是給 Agent 的，不需要看懂」.
- When a concept recurs, deepen it and say so. A page introduces at most 3 new points.
- Technique callouts end with `📖 延伸閱讀：〈組織〉官方文件〈標題〉`. List titles only, never URLs, because the build rejects external URLs on learner pages. Use only real titles, for example:
  - Anthropic 〈Prompt engineering overview〉, 〈Structured outputs〉, 〈Agent Skills〉, 〈Choosing a model〉, 〈Building with extended thinking〉, 〈Context windows〉
  - OpenAI 〈Prompt engineering〉, 〈Structured Outputs〉, 〈Reasoning models〉
  - GitHub Copilot 〈Adding repository custom instructions〉
  - DLC: Evans 《Domain-Driven Design》, Vernon 《Implementing Domain-Driven Design》, plugin docs by relative path, Git 〈git-commit〉
  If unsure, write 「你所用工具的官方文件中關於〈主題〉的章節」.

## The six Agent techniques (main course) and where they first appear
| Technique | First use |
|---|---|
| Prompt structure | Greenfield plan |
| Structured Output | Greenfield acceptance table; then B2 comparison, B3 Gate report, delivery summary |
| Model choice / reasoning effort | Greenfield (high to plan, low for small steps); analysis; B2; B3 |
| Token saving | Time Skip (new conversation), analysis (named files, summaries) |
| Skill | Shared context creates `skills/team-rules.md`; B1 `skills/fix-bug-with-test.md`; B3 Work Order as `skills/b3-work-order.md`; retro: the learner's own skill |

Stay tool-neutral: no vendor product names, commands or config paths as requirements. Tool features such as a model menu, effort setting or native Skills are optional extras.

## Canonical live texts (copy from these, don't re-invent)
- Agent work rules: the rules block in `materials/participant-runbook/content/10-greenfield.md` (Greenfield) and `30-time-skip.md` (Brownfield). From shared context onward, use 「請先讀 skills/team-rules.md」.
- Acceptance table, change review, and the `/docs` Try-it-out flow: `10-greenfield.md`, `44-b1.md`.
- DLC work rules: `materials-dlc/participant-runbook/content/01-environment.md`, `20-d2.md` (proposer and partner), `30-d3a.md`.
- DLC D2 and later: one shared machine. The partner opens their own terminal and Agent conversation. Only that conversation runs keys, `record-approval`, signed commits and push. The proposer's Agent never commits, pushes, reads `.dlc-keys`, or approves.

## Never change
- Frontmatter `id`/`group`/`minute`/`section`, unlock codes and times, `download`/`include` directives.
- Code packages (`src/`, `tests/`, requirements), DLC `tools/` `vendor/` `repository/`, `reference-*`, validation evidence.
- Gate times 66/69/75, exception EXCEPTION-DW-001 and `04-digital-worker/participant/06-exception-response-card.md`, Level 1–3 wording (checks C-04/C-08), slide `data-*` attributes, the minute-69 draw-card, deck js/css.
- No forbidden markers on learner pages (facilitator, evaluation, reference-solution, reference answer, 標準答案, observation-guide, rubric, 評分表, reference-registry), no external URLs.
- No answer leaks: the B1 root cause, the B2 discount order, the B3/SQLite answer, DLC reference solutions.
- If a checkpoint is renamed, the runbook heading, overview, slide data-title/kicker/callout, and DLC `CHECKPOINTS.md` change together.

## Always
- Delete content made obsolete, contradictory or duplicated by your edit. Do not only add.
- Facilitator notes: situation and technique first, what to watch for, paste-ready hint prompts. Evaluation judges technique use plus evidence in `notes/` and `skills/`, never the number of form fields filled.
- Plain Traditional Chinese with full-width punctuation (see `plain-language-review`). Preserve each file's line endings.
- After editing, run `curriculum-review` for broad changes, then `release-materials`.
