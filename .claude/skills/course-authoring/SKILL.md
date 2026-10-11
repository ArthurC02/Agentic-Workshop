---
name: course-authoring
description: The authoring standard for learner-facing workshop content (main course and DLC) - Runbook pages, four-block checkpoints, prompts, forms, callouts, facilitator deck slides, participant handouts, facilitator and evaluation docs. Use before writing or rewriting any of them, and give it to every sub-agent that edits course content.
---

# Course authoring standard (approved 2026-10-09; the rationale is in docs/planning/decisions-and-open-issues.md)

Audience: very junior engineers who may not know Python. They **never write or read code, and never type commands**. The Agent does all of that. Learners decide, approve, and verify through behavior and evidence.

## Goal order
1. Practice Agentic Coding techniques. This is the main point.
2. Experience the flow: Tool → Teammate → Digital Worker. The stages differ in **how the human intervenes**: step by step, by approving a plan, or only at Gates.
3. Evidence for organizational adoption. The Agent writes it into files; learners do not fill it in.

## Absolutely necessary (user rule, 2026-10-10)
Every page, section, callout and sentence must pass: "would the learner fail or hesitate at a step without this?" If not, cut it. Never re-host a document that ships in the learner's download unless learners must paste it to the Agent with 「複製 Markdown」 (the Agent reads files from the folder). Pages ending in a form lead with a short pair/group discussion and frame the form as recording its conclusions, not cold form-filling.

## Every segment page
- Top: a 「現在在做什麼」 callout with four lines: 情境 / 你的目標 / 今天的技巧 / 完成的樣子.
- Checkpoints: at most 3 (Greenfield and B3: at most 4; DLC segments run 15–25 min, so at most 6). Use the title format `## 檢查點 N · 〈動詞句〉（第 a–b 分鐘）`. The overview is a short list, not a table.
- Every checkpoint uses four blocks, in this order, each starting with its label line (user rule, 2026-10-10):
  1. `① 為什麼做這一步`: the precondition and the meaning in 1–3 sentences. Where the step needs a human judgment (approve a plan, review an acceptance table, decide at a Gate, approve as partner), say here what the learner judges and how.
  2. `② 貼給 Agent`: the prompt that runs the step. If it contains OS-specific commands or paths, use a ```prompt block with `# windows` and `# macos` sections (rendered as Windows／macOS tabs, choice remembered); otherwise ```text.
  3. `③ 確認結果`: a short ```text prompt asking the Agent to check the step's 1–3 completion conditions (files, test counts, recorded decisions) and reply **only** 「成功」 or 「失敗：〈一句原因〉」, changing nothing. Then 「失敗時」 with one paste-ready rescue prompt.
  4. `④ 補充`: optional — 技巧／新概念 callouts, 💬 discussion, warnings. Keep only what passes the absolutely-necessary test.

  `scripts/check_blocks.py` enforces ① ② ③ (④) in order, a 成功／失敗 ③ prompt, a 「失敗時」 line, and the knowledge-density limits in 「Reading parameters」.
- **Callouts**: first line after the title is a **bold one-sentence takeaway**, then short bullets. `tip` callouts and `info` callouts titled 技巧／新概念 render folded (closed `<details>`, the bold lead shows as a preview); 現在在做什麼, warnings, 💬 and 時間不夠時 stay open (`callout_folds` in `scripts/materials_md.py`). Anything a learner must see without clicking goes in ①–③, never only in a folded callout.
- **Prompts**:
  - Use the five parts: 目標 / 背景・要讀的檔 / 限制 / 輸出格式 / 停止條件.
  - Put commands and arguments in the prompt verbatim, for the Agent to run.
  - Name the record file (main course: `notes/<段落>.md`).
  - Never leave `〈 〉` blanks for learners. If the Agent needs information, it asks for it.
  - At decision points, the Agent proposes options with evidence and the learner replies briefly: 「同意」, 「選 B」, 「第 3 個不要」.
- **Forms**: at most one per segment, recording only the human's decision. Use select, checklist or checkbox fields, at most 3, plus at most 1 short text field. No form if there is no decision. Exception: B3 has two (Gate decisions, and the minute-69 exception decision).
- End of page:
  - A 「## 完成後想一想」 section with 3 specific questions: observation → technique → extension toward the next segment or real work, introduced as 「先自己想 30 秒，再和旁邊的人聊」. On a form page it comes right before the form. No closing 💬 or 「這段學到的技巧」 callout (they repeated 「今天的技巧」).

## Facilitator deck (user rule, 2026-10-11)
The projected slide does two jobs: pace the room, and tell learners exactly what to do next. Everything only the facilitator needs goes in `<aside class="notes">`.
- **Never crowd a slide** (user, 2026-10-11: 「不要讓內容擠成一團」). Card main line ≤ 14 CJK chars, card detail ≤ 24, 為什麼 ≤ 30, 你要判斷 ≤ 36 (one line); prefer 3 cards, merge steps instead of adding text; no paths or lists in cards unless learners must see them exactly. Whitespace beats filling space. `check_deck_runbook.py` enforces the limits.
- **Segment opening slide**: 情境／目標／今天的技巧 in three short lines, the checkpoint roadmap with deadlines, and where to start in the Runbook (page name). Unlock code only where the segment unlocks.
- **Checkpoint slide**, top to bottom:
  - `data-title="檢查點 n · 名稱"`, kicker `檢查點 n / N · 第 a–b 分鐘` and `<h2>` 名稱, all taken from the Runbook heading `## 檢查點 n · 名稱（第 a–b 分鐘）`;
  - one 「為什麼」 line (from ①);
  - 「現在做」 2–4 step cards mirroring the Runbook blocks: card 1 = 「貼 ②「prompt name」」 with detail 「Runbook › 檢查點 n」 (segment's first checkpoint: 「Runbook『full page title』› 檢查點 1」, never an ambiguous short form); then the human action (reply, decide, discuss; 「等 Agent 回報」 only with what it reports, otherwise drop the card); last 「貼 ③ 確認結果」／「成功→往下；失敗→貼「失敗時」」 (an action that follows ③ in the Runbook, like a form or discussion, stays after it). DLC role tags only on card 1 and where the conversation switches. No trailing 「。」 on why／judge／card lines;
  - 「你要判斷」 one line when the checkpoint has a human decision (same criterion as ①);
  - a footer line 「第 b 分前完成 → 下一步：…」.
- Layout markup (deck.css section 8b, identical in both editions; the grid anchors the footer/roadmap to the bottom): checkpoint `<section class="slide slide-cp">` with `p.cp-why`, `p.cp-label`, `ol.cp-flow` (2–4 step cards, sized to content: `<li>[<i>角色的對話</i>]<b>主句</b>[<span>細節</span>]</li>`), `p.cp-judge`, `p.cp-next` = `<b>第 b 分前完成</b><span>→ 下一步：…</span>` (「第 x 分前核准／決策」 only for a decision deadline); segment opening `<section class="slide slide-seg">` with `ul.seg-brief` (`<li><b>情境</b><span>…</span></li>`), `ol.timeline`, `p.callout.seg-start`. Keep step main lines short; detail goes in the `<span>`.
- Never put full prompts on slides (learners copy from the Runbook). Max ~6 projected lines of text per slide; sizes per 「Reading parameters」.
- Notes keep: what to say (with timing), what to watch, intervention prompts, first-introduction cues.
- Slides show whole; only concept／role-change slides step in with `data-fragments="step"`.
- `scripts/check_deck_runbook.py` enforces one slide per Runbook checkpoint (data-title, `<h2>`, kicker, footer deadline, 下一步), that Runbook pages, checkpoints and forms named on slides exist, and DLC `CHECKPOINTS.md`.

## Reading parameters (user, 2026-10-11: 「字寬字高，內容知識點密度。這些是關鍵參數」)
One table for both editions. Values live as CSS variables at the top of each `deck.css` (`--cp-*`, `--fs-min`, `--zone-gap`, `--content-w`) and `runbook.css` (`--rb-*`); change them only with measured evidence and update this table.

| | Size (字高) | Line height | Width (字寬) |
|---|---|---|---|
| Slide title (1920×1080) | 72px | 1.15 | ≤ 2 lines, ≤ 16 CJK chars per line |
| Card main line | 34px (40px fits only 12 chars in a third of the content block) | 1.3 | 1 line, ≤ 14 chars; 4 cards in a row: ≤ 10 |
| Card detail | 30px | 1.45 | ≤ 2 lines |
| 為什麼・你要判斷 | 32px | 1.4 | 1 line |
| Footer deadline | 46px | | |
| Anything on a slide | ≥ 24px | | letter-spacing 0–0.02em for CJK; wide tracking only on kickers |
| Slide layout | | | ≥ 48px between zones (header／cards／你要判斷／footer); content block ≤ 1728px |
| Runbook body | 17px desktop, 16px phone | 1.8 | 32–40 CJK chars per line at 1440px (36); paragraph gap ≥ 0.8em |
| Runbook headings | | | ≥ 1.6em space above, clear space below |
| Callout body | 16px | 1.75 | list item gap ≥ 0.35em |
| Runbook minimum | 12px (meta only) | | |

Knowledge density: Runbook ① ≤ 3 sentences; ≤ 1 new 技巧／新概念 callout per checkpoint (加深一層 doesn't count), ≤ 3 per page. Slides: ≤ 1 new concept per slide; checkpoint slides teach nothing new (concepts live in Runbook ④ and the notes).
Enforced by `check_blocks.py` (density) and `verify_typography.py` (renders both built decks and Runbooks in headless Chrome; part of `release-materials`).

## Knowledge points (progressive scaffolding)
- Introduce each concept, term, file convention, or report field at its **first need**. Use a `技巧：〈名稱〉` or `新概念：〈名稱〉` callout (bold takeaway plus 1–3 short lines).
- The opening is a roadmap only.
- Never require a point that has not been introduced. Text addressed only to the Agent gets the note 「這段是給 Agent 的，不需要看懂」.
- Participant and facilitator docs get packaged. Never link from them into `materials/` or `materials-dlc/` sources: those files are not in the package and `verify_delivery` rejects the link. Name the Runbook page in plain text, e.g. 「Runbook『環境準備』頁」.
- When a concept recurs, deepen it and put 「（加深一層）」 in the callout title. A page introduces at most 3 new points; `check_references.py` enforces this and does not count 加深一層 callouts.
- **Every knowledge point** gets a reference at its first introduction:
  - Techniques and general concepts: `📖 延伸閱讀：…` with titles only, never URLs, because the build rejects external URLs on learner pages.
  - Course-defined concepts: `📖 定義出處：本課程〈…〉`.
  - Every glossary row (`88-glossary.md`) ends with a 「出處」 cell under the same rules. `scripts/check_references.py` enforces all of this, and it runs inside `release-materials`.
  - Cite **only** titles listed in [references.md](references.md). They were verified online and record retired titles. If you need a new source, verify it and then add it there.

## The six Agent techniques (main course) and where they first appear
| Technique | First use |
|---|---|
| Prompt structure | Greenfield plan; deepened in B3 (the Work Order is the five parts at task scale) |
| Structured Output | Greenfield acceptance table; then B2 comparison, B3 Gate report, delivery summary |
| Model choice / reasoning effort | First taught in analysis checkpoint 1 (Greenfield only says 「先仔細想過再回答」 in the prompt); deepened in B2 (high to compare, low to implement) and B3 |
| Token saving | Time Skip (new conversation), analysis (named files, summaries) |
| Skill | Shared context creates `skills/team-rules.md`; B1 `skills/fix-bug-with-test.md`; B3 Work Order as `skills/b3-work-order.md`; retro: the learner's own skill |

Stay tool-neutral: no vendor product names, commands or config paths as requirements. Tool features such as a model menu, effort setting or native Skills are optional extras.

## Canonical live texts (copy from these, don't re-invent)
- Agent work rules: the rules block in `materials/participant-runbook/content/10-greenfield.md` (Greenfield) and `30-time-skip.md` (Brownfield). From shared context onward, use 「請先讀 skills/team-rules.md」.
- Acceptance table, change review, and the `/docs` Try-it-out flow: `10-greenfield.md`, `44-b1.md`.
- Four-block checkpoint and ```prompt Windows／macOS tabs: `materials/participant-runbook/content/10-greenfield.md` checkpoint 1.
- DLC work rules: `materials-dlc/participant-runbook/content/01-environment.md`, `20-d2.md` (proposer and partner), `30-d3a.md`.
- DLC D2 and later: one shared machine. The partner opens their own terminal and Agent conversation. Only that conversation runs keys, `record-approval`, signed commits and push. The proposer's Agent never commits, pushes, reads `.dlc-keys`, or approves.

## Never change
- Frontmatter `id`/`group`/`minute`/`section`, unlock codes and times, `download`/`include` directives, form `id`s, field ids and option values (they key learners' saved answers).
- Code packages (`src/`, `tests/`, requirements), DLC `tools/` `vendor/` `repository/`, `reference-*`, validation evidence.
- Gate times 66/69/75, exception EXCEPTION-DW-001 and `04-digital-worker/participant/06-exception-response-card.md`, Level 1–3 wording (checks C-04/C-08), the minute-69 draw-card, slide `data-seg`／`data-minute`／`data-unlock`／`data-code`／`data-gates`／`data-reveal-of`／`data-timer` (unlock slides are checked against `unlock-codes.json`). Slide `data-title` follows the Runbook checkpoint (see Facilitator deck); deck CSS／JS may change for layout only.
- No forbidden markers on learner pages (facilitator, evaluation, reference-solution, reference answer, 標準答案, observation-guide, rubric, 評分表, reference-registry), no external URLs.
- No answer leaks: the B1 root cause, the B2 discount order, the B3/SQLite answer, DLC reference solutions.
- If a checkpoint is renamed or renumbered, change together: the Runbook heading and 檢查點總覽, the slide `data-title`／`<h2>`／kicker, the segment opening roadmap, the previous slide's 「下一步」, and DLC `CHECKPOINTS.md`. Run `check_deck_runbook.py`.

## Always
- Delete content made obsolete, contradictory or duplicated by your edit. Do not only add.
- Facilitator notes: situation and technique first, what to watch for, paste-ready hint prompts. Evaluation judges technique use plus evidence in `notes/` and `skills/`, never the number of form fields filled.
- Plain Traditional Chinese with full-width punctuation (see `plain-language-review`). Preserve each file's line endings.
- After editing, run `curriculum-review` for broad changes, `rehearsal` for changed prompts and commands (every block must run), `fact-check` for new or changed explanations, then `release-materials` (it commits DLC and main separately and pushes).
