---
name: release-materials
description: Rebuild, check and verify both workshop editions (main and DLC) after any change to agentic-workshop/**, docs/**, Agent.md, scripts/README.md or .claude/skills, then commit DLC and main separately and push. Use after editing course content, Runbook or deck sources, participant files or the harness, or when asked to "rebuild", "重建", "跑檢查", "發布教材".
---

# Release materials

One command runs the order from docs/instructions/08 (2026-10-08 規範調整):

```bash
uv run --no-project --python 3.13 python -X utf8 scripts/release_materials.py
```

Steps (stops at the first failure; the step list is also in `scripts/README.md`):
1. Checks: `sync_harness.py --check` (`.agents/skills` and `.codex/hooks` equal the `.claude` originals; skipped when absent), `check_references.py`, `check_zh_tw.py`, `check_blocks.py`, `check_deck_runbook.py`.
2. Main candidate: on manifest drift, validate (full when G0–B3 sources changed, else `--static-only`) and repin; build and `verify_delivery` a new candidate (a failed one is deleted); set `CANDIDATE_ID`.
3. DLC candidate: `build_delivery_dlc.py --pin`, build if new, `--verify`; set `edition.json` `candidate_id`.
4. Each edition: `build_materials.py --edition main|dlc`, `--check`, `package_materials.py`.
5. Speech deck: `build_decks.py`, `--check`, `verify_browser.py`.
6. All `scripts/test_*.py`, zero manifest drift, prune superseded `dist/*-candidate/<id>`. Prints `RELEASE PIPELINE PASS`.

## Before running
- Edit sources, never generated files (built `runbook.html`／`facilitator-deck.html` in both editions, speech `greenfield-deck.html`／`greenfield-handout.md`, `dist/`, script-written evidence in `06-runbook/evaluation/`); the `guard_generated.py` hook blocks those.
- After editing `.claude/skills/**` or the hook, run `scripts/sync_harness.py` (no `--check`) to update the Codex mirror.
- Full validation needs `.codex-tmp/<g0|g1|b0|b1|b2|b3>-env`. If missing: `uv venv --seed --python 3.13 .codex-tmp/<v>-env`, then `uv pip install --python .codex-tmp/<v>-env/Scripts/python.exe -r <version dir>/requirements.txt` (dirs: `VERSIONS` in `scripts/validate_workshop.py`).

## After it passes
- Commit without asking: DLC work and main-course work in separate commits, messages in Taiwan Traditional Chinese describing the content change. Push to `main`.
- Report the new candidate IDs only if they changed.

## When it fails
- `sync_harness --check`: run `scripts/sync_harness.py`; never edit `.agents/` or `.codex/hooks/` by hand.
- `check_references`: fix the citation from `course-authoring/references.md`; a new source must be verified online first, then added there.
- `check_zh_tw`: replace the listed character or mainland term with the Taiwan form it names.
- `check_blocks`／`check_deck_runbook`: fix the Runbook or the slide so they follow `course-authoring` (four blocks; one slide per checkpoint with matching `data-title`, `<h2>`, kicker, footer).
- `Private overlay missing links`: a packaged doc links outside its package (e.g. into `materials/` or DLC docs); write the reference as plain text.
- `Source drift`／repin errors: never edit evidence or manifest hashes by hand; fix the source and rerun.
- G0–B3 behavior gate fails (planted B0 failures, test counts): stop and tell the user; that is a course-design change, not a build problem.
- Slide overflow from `verify_browser.py`: shorten the text in `speech/01-greenfield/src/slides.json`.
- A permission prompt or block: stop and report it; never work around it.
- Don't use bare `git stash` here: autocrlf rewrites built HTML on restore.
