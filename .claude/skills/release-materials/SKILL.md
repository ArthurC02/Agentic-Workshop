---
name: release-materials
description: Rebuild and verify workshop candidates and materials after any change to agentic-workshop/** sources, materials, materials-dlc, docs or Agent.md, then commit and push. Use after editing course content, runbook/deck sources, participant files, or when asked to "rebuild", "重建", "跑檢查", "發布教材".
---

# Release materials

One command runs the whole order from docs/instructions/08 (2026-10-08 規範調整):

```bash
uv run --no-project --python 3.13 python -X utf8 scripts/release_materials.py
```

It detects manifest drift → validates (full when G0–B3 changed, else static) → repins → builds and verifies the main candidate → sets `CANDIDATE_ID` → repins/builds/verifies the DLC candidate and `edition.json` → rebuilds both editions, `--check`, packages → speech deck build/check/browser check → unit tests → confirms zero drift → prunes superseded `dist/*-candidate/<id>` folders. Prints `RELEASE PIPELINE PASS` on success. A candidate that fails `verify_delivery` is deleted so the next run rebuilds it (verify snapshots `scripts/` into the candidate and refuses to re-verify after scripts change).

## Before running
- Edit sources, never build outputs (`runbook.html`, `facilitator-deck.html`, `greenfield-deck.html`, `greenfield-handout.md`); a hook blocks those.
- Full validation needs `.codex-tmp/<g0|g1|b0|b1|b2|b3>-env`. If missing:
  `uv venv --seed --python 3.13 .codex-tmp/<v>-env` then `uv pip install --python .codex-tmp/<v>-env/Scripts/python.exe -r <version dir>/requirements.txt` (dirs: `VERSIONS` in scripts/validate_workshop.py).

## After it passes
- Commit with a message describing the content change; split DLC and main-course work into separate commits. Push to `main` (the user asked for automatic commit & push).
- Report the new candidate IDs only if they changed.

## When it fails
- `Private overlay missing links`: a packaged doc links to a file outside the main package (e.g. DLC docs) — write the reference as plain text.
- `Source drift` / repin errors: never edit evidence or manifest hashes by hand; fix the source, rerun.
- G0–B3 behavior gate fails: the exercise changed (planted B0 failures, test counts). Stop and tell the user — that is a course-design change, not a build problem.
- Slide overflow from `verify_browser.py`: shorten the slide text in `speech/01-greenfield/src/slides.json`.
- Don't use bare `git stash` here: autocrlf rewrites built HTML on restore.
