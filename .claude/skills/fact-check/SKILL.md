---
name: fact-check
description: Verify that every knowledge point and technical term in the course is explained correctly, against official or authoritative sources found online. Use before a release, after adding glossary rows or 技巧／新概念 callouts, or when asked 「術語正確嗎」「查證」「知識點對不對」.
---

# Fact-check (knowledge correctness)

`check_references.py` proves every knowledge point *cites* a verified title. This skill proves the *explanation itself is correct*.

## What to check
- Every row of `materials/participant-runbook/content/88-glossary.md` and `materials-dlc/participant-runbook/content/88-glossary.md`.
- Every ```callout titled 技巧／新概念 in both Runbooks.
- Technical claims in the 「現在在做什麼」 cards and prompts. Examples: what a command does, HTTP status meanings, Git or pytest behaviour, signing and hash facts, DDD definitions, model, effort and token facts.

## How
1. For each item, find the official or authoritative source online:
   - vendor docs (Anthropic, OpenAI, GitHub, Git, pytest, Python, FastAPI, OpenSSH);
   - standards bodies (IETF RFC, NIST, ISTQB);
   - the canonical books (Evans, Vernon, Feathers, Nygard, Hohpe & Woolf).

   Prefer the page already listed in `.claude/skills/course-authoring/references.md`.
   When sources conflict, prefer the most recent one: the current version of the vendor docs, or the newest standard or edition. Record each source's date or last-updated date. Course text that matches only an older version counts as **outdated**.
2. Compare the course's explanation with the source. A simplification for junior learners is fine. A statement that is **wrong**, **misleading**, or **outdated** is a finding. So is a cited title that no longer exists or has been renamed.
3. Don't count course-defined concepts (Gate, Level 1–3, Work Order, Time Skip) as wrong for lacking an external source. Do check them against the defining course document.

## Report
For each finding:
- file:line;
- the course text;
- what the source says, with a short quote and its URL;
- severity (wrong / misleading / outdated title);
- the corrected Taiwan Traditional Chinese wording.

Also list the sources you verified, so `references.md` can be updated with the date checked. Never put URLs on learner pages.
