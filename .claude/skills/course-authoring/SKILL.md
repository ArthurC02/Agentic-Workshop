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
Every page, section, callout and sentence must pass: "would the learner fail or hesitate at a step without this?" If not, cut it. Never re-host a document that ships in the learner's download unless learners must paste it to the Agent with 「複製 Markdown」 (the Agent reads files from the folder). A file the Agent must use verbatim (e.g. the B3 work order) ships ready-made in a package the Agent unzips and copies, never assembled by the Agent from pasted parts, and never as an include-only Runbook page (user feedback, 2026-10-17: B3 CP1's assembled `skills/b3-work-order.md` was never created). Such a package holds one flat folder (B3: `b3-docs/`) with plain file names, a README whose first line says it is not a project and must not be opened in VS Code, and only files the Runbook flow uses; the prompt that uses it first checks it runs in the project folder and otherwise stops with one sentence telling the learner to switch folders (user feedback, 2026-10-17: a learner opened the extracted package as the workspace). Gate replies are one word from a fixed set on the card (「核准」／「附條件：…」／「退回：…」); the Agent records approver and time itself. Pages ending in a form lead with a short pair/group discussion and frame the form as recording its conclusions, not cold form-filling.

## Every segment page
- Top: a 「現在在做什麼」 callout with four lines: 情境 / 你的目標 / 今天的技巧 / 完成的樣子.
- Checkpoints: at most 3 (Greenfield and B3: at most 4; main segments run 6–23 min since the 2026-10-24 lengthening to 120 min, no break; DLC segments run 23–50 min since the 2026-10-24 lengthening to 255 min, so at most 6). Use the title format `## 檢查點 N · 〈動詞句〉（第 a–b 分鐘）`. The overview is a short list, not a table.
- Every checkpoint uses four blocks, in this order, each starting with its label line (user rule, 2026-10-10):
  1. `① 為什麼做這一步`: the precondition and the meaning in 1–3 sentences. Where the step needs a human judgment (approve a plan, review an acceptance table, decide at a Gate, approve as partner), say here what the learner judges and how.
  2. `② 貼給 Agent`: the prompt that runs the step. If it contains OS-specific commands or paths, use a ```prompt block with `# windows` and `# macos` sections (rendered as Windows／macOS tabs, choice remembered); otherwise ```text.
     **Paste order follows reality** (user feedback, 2026-10-13: learners pasted Greenfield's rules before opening the repo): every paste block sits inside the checkpoint ② that first needs it, after the download／open-folder／new-conversation step. Never put a prompt above a segment's first checkpoint.
  3. `③ 確認結果`: both editions: one ```text line handing the check to the learner's `check` Skill — 「用 check 檢查剛才這一段」, plus at most one sentence of this step's own condition when truly needed (the Skill is read-only, compares notes vs. actual command results (DLC: also plugin output) vs. the approved plan／acceptance criteria, and ends with 「成功」 or 「失敗：〈一句原因〉」). Wherever the Agent ends its own work turn (approve-and-do, release, analysis, delivery prompts), ② ends with 「做完用 check 檢查，最後一行寫成功或失敗」 (measured 2026-10-23: a separate ③ turn costs ~1 min per checkpoint), and ③ opens with 「Agent 最後一行已回「成功」就不用再貼；回「失敗」就貼下方「失敗時」。沒看到成功或失敗時才貼：」 before the ```text check line; the slide's ③ card becomes 「看 Agent 最後一行」. Any ② whose Agent writes a Skill folder carries the tool-neutral line 「Agent 建立 Skill 資料夾時，工具若跳出允許視窗，按允許。」 (real CLIs treat the Skill folder as protected; a denied write made check report 失敗). Shipped `AGENTS.md` rules never claim the reply's last line for anything but check's 成功／失敗 (test counts go on the line before). Then 「失敗時」 with one short, natural rescue (「先停，不要再改。發生什麼事？你建議怎麼做？」 style, plus what to restore when it matters).
  4. `④ 補充`: optional — 技巧／新概念 callouts, 💬 discussion, warnings. Keep only what passes the absolutely-necessary test.
  **Judge without switching pages** (user feedback, 2026-10-17: B3 Gate 1 sent learners to a separate task-card page): what a learner checks against during a checkpoint lives on the same page (a segment's task card goes in its own 「## 任務卡」 section, as in B1–B3), and the Agent's decision card quotes the governing source sentence verbatim (「原文（段落）：…」) under each question, so the learner compares in place.

  `scripts/check_blocks.py` enforces ① ② ③ (④) in order, a ③ prompt using `check`, a 「失敗時」 line, and the knowledge-density limits in 「Reading parameters」.
- **Callouts**: first line after the title is a **bold one-sentence takeaway**, then short bullets. `tip` callouts and `info` callouts titled 技巧／新概念 render folded (closed `<details>`, the bold lead shows as a preview); 現在在做什麼, warnings, 💬 and 時間不夠時 stay open (`callout_folds` in `scripts/materials_md.py`). Anything a learner must see without clicking goes in ①–③, never only in a folded callout.
- **Prompts** (user feedback, 2026-10-22: 「Prompt…更符合實際工作狀況，而不是只存在教科書上的格式」; design: `docs/planning/main-course-practice-first.md`):
  - Both editions: write it like assigning work to a colleague — only what this time, why, what done looks like, where the material is; 2–5 lines. Rules and procedures live in files the tool loads by itself (`AGENTS.md`, Skills), so never repeat 用白話／停下等我／不要改檔／report formats／server-stop details／venv paths／Git identity in a prompt. Keep only real decisions and real hand-offs. Never put answers the requester wouldn't know in a prompt (expected totals, which AC is usually missed, error codes): fixed decisions go into the requirement docs／task cards the Agent reads; gaps become open questions with suggested answers for the learner.
  - Skills are standard (agentskills.io〈Specification〉; `scripts/test_skill_spec.py` checks every shipped one): `<the tool's project Skill folder>/<name>/SKILL.md`, frontmatter from line 1 with `name` (lowercase a-z／0-9／hyphen, ≤ 64, equals the folder) and `description` (third person, what it does + when to use it + the words users say, ≤ 1024 chars), body ≤ 500 lines. Tool-only fields (`when_to_use`, `disable-model-invocation`, `paths`) appear only in handouts and facilitator notes as examples. Learner pages say 「放在你這個工具會自動載入專案 Skill 的位置，告訴我完整路徑」 and never name a tool or a path.
  - DLC: plugin commands are written `dm <command> <args>` in a ```text block (the shipped `AGENTS.md` maps `dm` to `dm.ps1`／`dm.sh` per OS, so no Windows／macOS tabs); fixed arguments the flow depends on (package roots, commit messages, principals, `--reason` texts) stay verbatim. Recurring procedures live in the DLC Skills (`check`, `record-candidates`, `counterfactual`, `signed-commit`, `dlc-recovery`), fixed formats in the worksheets the Agent reads (`d2-signing-checklist.md`, `d3-decision-card.md`, `d4-handoff-template.md`), Recovery steps 2–3 in each package's generated `RECOVERY.md`.
  - Put commands and arguments in the prompt verbatim, for the Agent to run.
  - Name the record file (main course: `notes/<段落>.md`).
  - Never leave `〈 〉` blanks for learners. If the Agent needs information, it asks for it.
  - At decision points, the Agent proposes options with evidence and the learner replies briefly: 「同意」, 「選 B」, 「第 3 個不要」.
- **Forms**: at most one per segment, recording only the human's decision. Use select, checklist or checkbox fields, at most 3, plus at most 1 short text field. No form if there is no decision. Exception: B3 has two (Gate decisions, and the minute-88 exception decision).
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
- Layout markup (deck.css section 8b, identical in both editions; the grid anchors the footer/roadmap to the bottom; the cards and 你要判斷 form one group placed just above the middle, so no wide empty band opens under 為什麼): checkpoint `<section class="slide slide-cp">` with `p.cp-why`, `p.cp-label`, `ol.cp-flow` (2–4 step cards, sized to content: `<li>[<i>角色的對話</i>]<b>主句</b>[<span>細節</span>]</li>`), `p.cp-judge`, `p.cp-next` = `<b>第 b 分前完成</b><span>→ 下一步：…</span>` (「第 x 分前核准／決策」 only for a decision deadline); segment opening `<section class="slide slide-seg">` with `ul.seg-brief` (`<li><b>情境</b><span>…</span></li>`), `ol.timeline`, `p.callout.seg-start`. Keep step main lines short; detail goes in the `<span>`.
- Never put full prompts on slides (learners copy from the Runbook). Max ~6 projected lines of text per slide; sizes per 「Reading parameters」.
- Notes keep: what to say (with timing), what to watch, intervention prompts, first-introduction cues.
- Slides show whole; only concept／role-change slides step in with `data-fragments="step"`.
- `scripts/check_deck_runbook.py` enforces one slide per Runbook checkpoint (data-title, `<h2>`, kicker, footer deadline, 下一步), that Runbook pages, checkpoints and forms named on slides exist, and DLC `CHECKPOINTS.md`.

## Sync cues (user, 2026-10-11: the facilitator controls the pace)
- Projector = where we are and when to stop; Runbook = how. Said once on the welcome page, never as a blanket "watch the facilitator" line (redundancy).
- A ```callout sync (title 「⏸ 看投影：」 + one short clause; never folds) goes **only** where the learner must take something from the projector or wait for the facilitator: stop／揭曉, the B3 exception card, DLC partner pairing, a Recovery handoff (「貼紅色便利貼，主持人會走過去」). Unlock codes are cued by the lock card (runbook.js). Always 「投影」, never 簡報／螢幕 for the projector. Replace existing prose that says the same; don't duplicate.
- The matching slide carries `<p class="sync-cue" data-sync="key …">⏸ 看投影</p>` (deck.css). `check_deck_runbook.py` maps each callout to a marked slide whose data-minute lies in the page's minute range and whose key the title names, and back; unlock and stop／reveal slides must be marked.
- Status: green／red sticky notes (③ 成功 → green; stuck → red, facilitator comes over). Explained once on the welcome page and the opening how-to slide, never per checkpoint; speaker notes tell the facilitator to scan colours at each checkpoint deadline.

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
| Line breaks (slides and Runbook) | | | no orphan: a wrapped last line holds ≥ 3 characters. Slides balance lines and break CJK only at punctuation or spaces (deck.css); in Runbook paragraphs and list items, reword (cut or move a few characters) when a line ends with 1–2 characters |
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
| Prompt structure | Greenfield plan (要什麼、為什麼、完成的樣子、素材在哪); deepened in B3 (the Work Order is the same at task scale) |
| Structured Output | Greenfield acceptance table; then B2 comparison, B3 Gate report, delivery summary |
| Model choice / reasoning effort | First taught in analysis checkpoint 1 (Greenfield only says 「先仔細想過再回答」 in the prompt); deepened in B2 (high to compare, low to implement) and B3 |
| Token saving | Time Skip (new conversation), analysis (named files, summaries) |
| Rules file (`AGENTS.md`) | Greenfield CP1 (the Agent writes it: 怎麼跑 + 工作規則 from `04-agent-usage-guide.md`); Time Skip confirms auto-load in a new conversation (B0 ships the predecessor's `AGENTS.md`, also in both Recovery packages; never ship a `CLAUDE.md`); shared context adds 開工先讀 and 審查準則; B1 CP3 「同一個錯第二次，就加一行」 |
| Skill | Greenfield CP1 `check` (B0's `AGENTS.md` carries the check steps until shared context moves them into a `check` Skill); taught at shared context; B1 `fix-bug-with-test` (first learner review of a description, official authoring loop steps 1–4); B3 Work Order as `b3-work-order` (a task-sized Skill); retro CP2 「創作你的 Skill」: the learner answers 3 questions, the Agent writes it, the learner tests 3 phrasings (2 should, 1 should-not), each alone in its own new conversation (that is what exercises the description), and fixes the description; an existing Skill with the same job (B1's `fix-bug-with-test`) is improved, not duplicated; take-home 「Skill 創作卡」 in `reflection-sheet.md` |

Stay tool-neutral: no vendor product names, commands or config paths as requirements. Tool features such as a model menu, effort setting or native Skills are optional extras.

## Canonical live texts (copy from these, don't re-invent)
- Agent work rules: Greenfield's 工作規則 template and 「怎麼跑」 list in `01-greenfield/participant/04-agent-usage-guide.md`; Brownfield's shipped `AGENTS.md` is the `generated` entry in `scripts/package-manifest.json` (participant-29-b0, recovery-52-b1, recovery-63-b2 — keep the three identical). Prompts never ask the Agent to read the rules: a new conversation loads `AGENTS.md` itself; Time Skip teaches the one-line rescue.
- Acceptance table, change review, and the `/docs` Try-it-out flow: `10-greenfield.md`, `44-b1.md`.
- Review policy (「審查準則」, a section of `AGENTS.md`): the verbatim text in the `39-shared-context.md` CP2 prompt. The fallback blocks in `53-recovery-b1.md` and `67-recovery-b2.md` carry the same text; change all three together. B1–B3 and the delivery review conversation cite it (「照 AGENTS.md 的審查準則」) instead of re-listing the questions.
- External playbooks and frameworks (user feedback, 2026-10-22: 「參考他的內容，而不是設計。教學要能夠學以致用」): use their content (concrete practices, first steps, each practice's own indicators), never their design (stage names, artifact-chain labels, renamed Gates, invented rules of thumb). Keep course names (B3 Gates 需求理解／設計與修改範圍／交付) and describe the practice in plain words (「計畫開頭三行：要什麼、為什麼、限制」, not 意圖／規格). Every learner callout citing such a source carries at most one 「回到工作：…」 bullet with its concrete first step. Indicators are copied from the source per practice; the retro's 「回到工作：從哪一項開始」 list in `05-retrospective/participant/reflection-sheet.md` is the canonical copy. Learner pages never use intent.md／spec.md／REVIEW.md.
- Four-block checkpoint and ```prompt Windows／macOS tabs: `materials/participant-runbook/content/10-greenfield.md` checkpoint 1.
- DLC work rules: the shipped `AGENTS.md` (怎麼跑, Git 與金鑰, 工作規則, 兩個角色, 領域模型, 通用語言與邊界, 審查準則, Skill) is the `generated` entry of `participant-dlc-open` in `scripts/package-manifest-dlc.json` (it lands in `repository/smart-ticket-dlc-base/`; never ship a `CLAUDE.md`). The five Skills are `07-dlc-ddd/participant/skills/<name>/SKILL.md`, copied by the learner's Agent at opening CP1; Recovery step 1 copies `AGENTS.md` and the Skill folder into `resume-<seg>`. `dlc-recovery` step 1 must equal `make_recovery.SAVE_PS／SAVE_SH` (`scripts/test_dlc_recovery_skill.py`). Learners add their D1 naming and boundary decisions to `AGENTS.md`「通用語言與邊界」.
- DLC D2 and later: one shared machine. The partner opens their own terminal and Agent conversation. Only that conversation runs keys, `record-approval`, signed commits and push. The proposer's Agent never commits, pushes, reads `.dlc-keys`, or approves.

## Never change
- Frontmatter `id`/`group`/`minute`/`section`, unlock codes and times, `download`/`include` directives, form `id`s, field ids and option values (they key learners' saved answers).
- Code packages (`src/`, `tests/`, requirements), DLC `tools/` `vendor/` `repository/`, `reference-*`, validation evidence.
- Gate times 85/88/98 (since the 2026-10-24 lengthening; were 66/69/75), exception EXCEPTION-DW-001 and `04-digital-worker/participant/06-exception-response-card.md`, Level 1–3 wording (checks C-04/C-08), the minute-88 draw-card, slide `data-seg`／`data-minute`／`data-unlock`／`data-code`／`data-gates`／`data-reveal-of`／`data-timer` (unlock slides are checked against `unlock-codes.json`). Slide `data-title` follows the Runbook checkpoint (see Facilitator deck); deck CSS／JS may change for layout only.
- No forbidden markers on learner pages (facilitator, evaluation, reference-solution, reference answer, 標準答案, observation-guide, rubric, 評分表, reference-registry), no external URLs.
- No answer leaks: the B1 root cause, the B2 discount order, the B3/SQLite answer, DLC reference solutions.
- If a checkpoint is renamed or renumbered, change together: the Runbook heading and 檢查點總覽, the slide `data-title`／`<h2>`／kicker, the segment opening roadmap, the previous slide's 「下一步」, and DLC `CHECKPOINTS.md`. Run `check_deck_runbook.py`.

## DLC plugin version (domain-memory; full rule and procedure: decisions record 「Plugin 版本政策」)
- Pin one exact committed version: `git archive <commit>` export → `scripts/vendor_dlc_plugin.py --source`, ZIP plus SHA256SUMS; never vendor a working tree, never edit vendored bytes.
- Patch releases that fix something on the learner path: take them after re-running the checks (`scripts/check_dlc_plugin_compat.py --source <export>` covers tools self-test, reference Registry, D1 replay and learner-quoted output; then the release pipeline). Minor releases: evaluate the changelog and rehearse before pinning.
- Registry layout is the plugin's business (OKF concept files since 0.29, pinned 4.2.0; see `docs/planning/domain-memory-touchpoints.md`): DLC tools read Registry content only through `dmlib.registry_documents()` (plugin `export`) and write only through plugin commands or the plugin's Change Package templates; prompts name plugin commands (`dm export` lists every record) or stay layout-neutral (「domain-memory/ 裡的詞彙紀錄」), never `registry/<asset>.json` or `registry/<asset>/<id>.md`. On-disk `status` is `draft`/`stable`; commands and `export` say `candidate`/`reviewed`, so learner checks quote command output, not files.
- Any new commit on the signed reference history (`evaluation/reference-registry`) is signed with the Maintainer-2 key read in place (never copied, never regenerated); keep `* -text` and the starter repo's CRLF bytes; then update `REGISTRY_COMMITS` in the compat script, the commit counts in `make_recovery.py` and the facilitator guide, and rebuild Recovery.
- Freeze the pin 7 days before a scheduled workshop; during the freeze only security or blocking fixes.
- Every pin change: update version strings and file counts everywhere (grep the old version), and record commit, measurements and differences in the decisions record.

## Always
- Delete content made obsolete, contradictory or duplicated by your edit. Do not only add.
- Facilitator notes: situation and technique first, what to watch for, paste-ready hint prompts. Evaluation judges technique use plus evidence in `notes/`, `AGENTS.md` and the Skills, never the number of form fields filled.
- Plain Traditional Chinese with full-width punctuation (see `plain-language-review`). Preserve each file's line endings.
- After editing, run `curriculum-review` for broad changes, `rehearsal` for changed prompts and commands (every block must run), `fact-check` for new or changed explanations, then `release-materials` (it commits DLC and main separately and pushes).
