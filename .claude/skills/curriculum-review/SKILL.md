---
name: curriculum-review
description: Two-loop review of workshop materials (main course or DLC). Outer loop = is the whole curriculum progressive (knowledge points introduced at first need, difficulty ramps sensibly). Inner loop = is each task's setup and text sound (prompts runnable, pass criteria observable, facts match the repo). Use after any content redesign, when asked "循序漸進嗎", "知識點安排", "任務設定合理嗎", "內外迴圈", or before a release.
---

# Curriculum review: outer loop + inner loop

The materials have two loops. Review both against the authoring standard in `course-authoring`; fix the findings; then run `release-materials`.

## How to run
- One segment or a few pages: apply the checklists below directly.
- A whole edition: run the named workflow `curriculum-review` with `args: {"scope": "main"}` or `{"scope": "dlc"}`. It runs one outer-loop reviewer reading the edition in Runbook order and one inner-loop reviewer per task segment in parallel, verifies each finding against the files, has one fixer per segment apply the confirmed findings, and finishes with a consistency pass.

## Outer loop: the curriculum as a whole (read in Runbook order, `content/*.md` by file name, resolving includes)
1. **Progression.** The difficulty ramps up: Tool → Teammate → Digital Worker in the main course; D1 → D4 in the DLC. Each segment builds on the previous one, and none needs skills that come later.
2. **Knowledge points at first need.** Every concept, term, file convention, or report field a learner must understand appears at or just before its first use, never long before. The opening gives a roadmap only. Nothing is used before it is introduced. The glossary is a backstop, not the introduction.
3. **Spiral deepening.** When a concept returns, it goes one level deeper and says so ("上次學過 X，這次多加 Y"), instead of re-teaching the same thing.
4. **Cognitive load.** A page introduces at most 3 new knowledge points. The workload fits the minutes.
5. **Official references.** Each technique-type point carries a `📖 延伸閱讀` line that names real sources only, with no URLs.
6. **Bridges.** The 「完成後想一想」 questions link each segment to the next, and the retrospective draws on them without duplicating them.
7. **No dead knowledge.** Nothing is introduced and then never used, and nothing is explained twice in conflicting ways.

## Inner loop: each task (one segment = Runbook page(s) + included docs + slides + facilitator notes)
1. **Situation and goal.** The 「現在在做什麼」 card makes clear what is happening, why, the technique, and what "done" looks like.
2. **Prompts are runnable.** Pasting the prompts in order gets an Agent through the task. Nothing is missing: files to read, commands, where to record results, a stop condition. There are no `〈 〉` blanks for learners. Commands and arguments match the tools in the repo.
3. **Facts match the repo.** File paths, endpoints, test counts, unlock times, rule IDs, plugin output strings, and minutes all match the code packages and the other materials.
4. **Pass criteria are observable.** "看到什麼算過關" names things that actually appear in the Agent's report.
5. **Decisions are real.** Each human decision point offers a genuine choice with evidence. Forms only record that decision, using select or checkbox fields.
6. **Stuck paths exist.** 「如果卡住」 prompts and Recovery steps work from the state a learner is actually in.
7. **No leaks.** No answer leaks: the B1 root cause, the B2 order, the B3 or SQLite answer, and DLC reference solutions stay hidden. No forbidden markers.
8. **Alignment.** Slides, CHECKPOINTS.md (DLC), and the facilitator guide match the Runbook: checkpoint titles, minutes, and what to watch for.
9. **Reflection.** The 「完成後想一想」 questions are specific to this task, not generic.

## Fix rules
Follow `course-authoring` (its "Never change" and "Always" lists). Main course: `scripts/validate_consistency_corrections.py` must PASS.
