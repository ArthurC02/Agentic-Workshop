---
name: rehearsal
description: Dry-run the workshop the way a learner would. An agent pastes each Runbook prompt in order into a sandbox built from the real candidate packages, plays the learner's Coding Agent, and reports where prompts break, pass criteria don't appear, or concepts are used before they are introduced. Use after content changes and before a release, or when asked 「演練」「試跑」「提示詞能不能跑」.
---

# Rehearsal (inner-loop proof)

`curriculum-review` reads the materials. Rehearsal **runs** them. It is the only check that proves a learner can copy-paste their way through a segment.

## How to run
- One segment: launch one agent with the brief below for that segment.
- A whole edition: run the named workflow `rehearsal` with `args: {"scope": "main"}` or `{"scope": "dlc"}`. It runs one agent per segment group in parallel, then merges the findings.
- Then fix the findings using `course-authoring`, and run `release-materials`.

## Brief every rehearsal agent gets
- **Never edit the repo.** Work in `<scratchpad>/dryrun-<segment>/` and delete it afterwards.
- Build the sandbox from the **current candidate packages** (`dist/p11-candidate/<id>/*.zip`, `dist/dlc-candidate/<id>/*.zip`), not from repo sources. Learners only ever see packages. Use Python 3.13 via uv. Set HOME, USERPROFILE, GIT_CONFIG_GLOBAL, LOCALAPPDATA and APPDATA to sandbox folders, so real keys and git config stay untouched and PowerShell does not write a `Microsoft/` cache folder into the repo. Use a global git config with no identity, to catch commits that fail on a fresh machine.
- **Play two roles:**
  - **The learner.** Copies each ```text prompt in page order (resolving the `include`s) and gives only the short replies the page asks for.
  - **The learner's Coding Agent.** Does exactly what each prompt says.
- **Record for every checkpoint:**
  - Is it executable as written?
  - Do the 「看到什麼算過關」 items actually appear? Give real test counts and output strings.
  - Is any concept used before it was introduced?
  - Did the learner have to type more than a short reply?
  - Is the step realistic for its minutes?
  - Is any answer leaked?
- **Coverage is mandatory.** Run every ```text prompt **and** every command block on the pages, including both the PowerShell and the Git Bash variant where a page gives both. Compare the real output with every 「看到什麼算過關」 line and every expected string quoted in the page text, slide notes or facilitator docs. Return a coverage list: `page:block → ran | blocked (by what) | not run (why)`. "Read only" or "spot-checked" is not coverage.
- **Sandbox artefacts are not findings:** a `py -3.13` shim to uv's Python, `core.longpaths` for the long scratchpad path, a drive mapped with `subst`. Note them once. If a permission check blocks a step (for example `git push`, even to a local bare repo), do not work around it; list it as blocked.
- **Report:** numbered findings with page:heading, severity (blocker/major/minor), what happened, and a one-line fix, plus a short "worked well" list.

## Segment groups and packages
| Scope | Group | Pages | Start from |
|---|---|---|---|
| main | greenfield | content 00–16 | `participant-07-g0.zip` |
| main | brownfield | 30–52 (+53, 67 recovery check) | `participant-29-b0.zip`; task cards from `participant-44-b1.zip`, `participant-52-b2.zip` |
| main | b3-delivery-retro | 60–80 | `recovery-63-b2.zip` (post-B2 baseline), `participant-63-b3-governance.zip`; the exception text is on the deck slide 例外事件 |
| dlc | open-d1-d2 | 00–29 | `participant-dlc-open.zip`, `-d1`, `-d2` |
| dlc | d3a | 30–39 | D2 end state (build it with the page-29 Recovery D2 flow) |
| dlc | d3b | 40–49 | `recovery-dlc-d3a.zip` via page 39 |
| dlc | d3c | 50–59 | `recovery-dlc-d3b.zip` via page 49 |
| dlc | d4-retro | 60–70 | D3c end state |
