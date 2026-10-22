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
  - **The learner.** Copies each ② prompt, then the ③ 確認結果 prompt, in page order (```text, or the matching tab of a ```prompt block; resolve the `include`s), and gives only the short replies the page asks for. A learner never writes or reads code or types a command.
  - **The learner's Coding Agent.** Does exactly what each prompt says.
- **Record for every checkpoint:**
  - Is it executable as written?
  - Does every ③ 確認結果 prompt answer 「成功」 on a correct run (no false 失敗) and 「失敗」 on a broken one? Give real test counts and output strings.
  - Is any concept used before it was introduced?
  - Did the learner have to type more than a short reply?
  - Is the step realistic for its minutes?
  - Is any answer leaked?
- **Coverage is mandatory.** Run every ```text prompt **and** every command block on the pages, including both the PowerShell and the Git Bash variant where a page gives both, and the ③ 確認結果 and 「失敗時」 prompts. ```prompt blocks have Windows／macOS tabs; macOS lines that cannot run here must be listed as statically checked only. Compare the real output with every ③ condition and every expected string quoted in the page text, slide notes or facilitator docs. Return a coverage list: `page:block → ran | blocked (by what) | not run (why)`. "Read only" or "spot-checked" is not coverage.
- **Sandbox artefacts are not findings:** a `py -3.13` shim to uv's Python, `core.longpaths` for the long scratchpad path, a drive mapped with `subst`. Note them once. If a permission check blocks a step (for example `git push`, even to a local bare repo), do not work around it; list it as blocked.
- **Auto-load probes (main course):** the rehearsal agent only simulates the learner's Agent. Where a step depends on `AGENTS.md` or a Skill being loaded in a new conversation, run a real probe from the sandbox project with the installed CLI, real login (no HOME override), one turn, no other tools, e.g. `claude -p "這個專案的工作規則是什麼？只引用 AGENTS.md 原文…" --max-turns 1 --tools "" --strict-mcp-config` (Skill probes: `--tools Skill --output-format stream-json --verbose` to see the Skill call). Report the CLI version; treat auto-load as unverified unless a probe showed it.
- **Report:** numbered findings with page:heading, severity (blocker/major/minor), what happened, and a one-line fix, plus a short "worked well" list.

## Segment groups and packages
| Scope | Group | Pages | Start from |
|---|---|---|---|
| main | greenfield | content 00–16 | `participant-07-g0.zip` |
| main | brownfield | 30–52 (+53, 67 recovery check) | `participant-29-b0.zip`; task cards from `participant-44-b1.zip`, `participant-52-b2.zip` |
| main | b3-delivery-retro | 60–80 | `recovery-63-b2.zip` (post-B2 baseline), `participant-63-b3-governance.zip` (downloads as `b3-docs.zip`; only its `b3-docs/` folder goes into the project; also try the wrong-folder case: CP1 opened inside the extracted package must stop); the exception text is on the deck slide 例外事件 |
| dlc | open-d1-d2 | 00–29 | `participant-dlc-open.zip`, `-d1`, `-d2` |
| dlc | d3a | 30–39 | D2 end state (build it with the page-29 Recovery D2 flow) |
| dlc | d3b | 40–49 | `recovery-dlc-d3a.zip` via page 39 |
| dlc | d3c | 50–59 | `recovery-dlc-d3b.zip` via page 49 |
| dlc | d4-retro | 60–70 | D3c end state |
