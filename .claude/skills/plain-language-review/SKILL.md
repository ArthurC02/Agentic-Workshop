---
name: plain-language-review
description: Review and rewrite learner-facing workshop text (runbook content, facilitator deck slides, speech decks, participant handouts) so it is plain Traditional Chinese with no unexplained abbreviations. Use when asked "是否通俗易懂", "沒有縮寫", "白話化", "用詞審查", or after writing new course content.
---

# Plain-language review

Audience: bank in-house developers new to Agentic SDLC / DDD. Goal: every abbreviation and English working term is explained where a learner first meets it; glossary is the backstop, not the only explanation.

## How to run
- Small change (a few files): apply [wording-spec.md](wording-spec.md) directly.
- Whole edition or several sections: run the named workflow `wording-pass` with `args: {"scope": "main"}` or `{"scope": "dlc"}` (or `{"files": [...]}`). It splits files into non-overlapping groups, one agent reviews+edits each group under the spec, then one agent checks cross-group consistency (same expansion, checkpoint titles in sync, glossary covers new terms).
- Then run the `release-materials` skill.

## Rules that are easy to break
- Never edit `include`d content (comes from the frozen candidate ZIP) — explain it in surrounding text or the glossary.
- Form JSON: keep `"id"`, `"type"`, option values, checklist items and their order; `"title"`/`"label"`/`"hint"` may change.
- Checkpoint titles must match across runbook headings, runbook overview table, deck `data-title`/kicker/callout and `CHECKPOINTS.md` — rename all or none.
- Code blocks, commands, rule IDs, numbers, minutes: unchanged.
- Forbidden strings (build rejects): facilitator, evaluation, reference-solution, reference answer, 標準答案, observation-guide, rubric, 評分表, reference-registry; no external URLs.
- Preserve each file's line endings.
