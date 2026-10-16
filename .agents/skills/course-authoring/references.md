# Verified 📖 延伸閱讀 sources (checked 2026-10-09)

Learner pages cite **titles only, never URLs**; the build rejects external URLs. Use the exact titles below. If a topic is not covered here, write 「你所用工具的官方文件中關於〈主題〉的章節」 and add a source to this list only after checking it online. Re-check titles once per release cycle, because vendors rename pages.

Format: `📖 延伸閱讀：〈組織〉官方文件〈標題〉…；你所用工具的官方文件通常有同名章節。`

## Agentic Coding techniques
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Prompt structure, clarity | Anthropic 〈Prompt engineering overview〉, 〈Prompting best practices〉; OpenAI 〈Prompt engineering〉 | 〈Be clear, direct, and detailed〉, 〈Let Claude think (chain of thought)〉: merged into Prompting best practices |
| Structured Output | Anthropic 〈Structured outputs〉; OpenAI 〈Structured model outputs〉 | OpenAI 〈Structured Outputs〉 (renamed) |
| Model choice | Anthropic 〈Choosing the right model〉; GitHub 〈Changing the AI model for GitHub Copilot Chat〉 | 〈Choosing a model〉, 〈Changing the AI model for Copilot Chat〉 |
| Reasoning effort / thinking | Anthropic 〈Thinking〉, 〈Effort〉; OpenAI 〈Reasoning models〉 (has a "Reasoning effort" section) | 〈Building with extended thinking〉 |
| Token, context | Anthropic 〈Context windows〉, 〈Token counting〉; Anthropic Engineering 〈Effective context engineering for AI agents〉 (2025-09-29) | |
| Skill / rules file | Anthropic 〈Agent Skills〉; OpenAI Codex 〈Custom instructions with AGENTS.md〉; GitHub 〈Adding repository custom instructions for GitHub Copilot〉 | 「Codex 文件中的〈AGENTS.md〉說明」 |
| Plan first, verify with tests, agent work rules | Claude Code 官方文件〈Best practices for Claude Code〉 | Anthropic Engineering 〈Claude Code: Best practices for agentic coding〉 (moved into the Claude Code docs) |
| Testing | pytest 官方文件〈Get Started〉; skip／xfail: pytest 官方文件〈How to use skip and xfail to deal with tests that cannot succeed〉 | 〈Getting started〉 |
| Change review / Diff | Google Engineering Practices 〈Google's Code Review Guidelines〉 (reviewer half: 〈The Code Reviewer's Guide〉); Git 官方文件〈git-diff〉 | 〈Code Review Developer Guide〉 |
| Commits, signing | Git 官方文件〈git-commit〉 (`-S`)；SSH 簽章設定（`gpg.format`、`gpg.ssh.allowedSignersFile`）：Git 官方文件〈git-config〉 | |
| Hashes (SHA256) | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 | |

## Software engineering terms (glossary sources)
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Testing terms (regression, root cause, impact analysis, traceability, acceptance criteria, test basis) | ISTQB〈Glossary〉 (the ISTQB Standard Glossary of Terms Used in Software Testing) | |
| Layered architecture (DDD) | Vaughn Vernon《Implementing Domain-Driven Design》(2013) ch.4〈Architecture〉 | |
| Gherkin, Given/When/Then | Cucumber 官方文件〈Gherkin Reference〉 | |
| ADR | Michael Nygard〈Documenting Architecture Decisions〉 (2011) | |
| MVP | Eric Ries《The Lean Startup》 (2011) | |
| Brownfield / legacy code | Michael Feathers《Working Effectively with Legacy Code》 (2004) | |
| Agent, coding agent, human-in-the-loop | Anthropic Engineering〈Building effective agents〉 (2024-12) | |
| /docs, Swagger UI, OpenAPI | FastAPI 官方文件〈First Steps〉 (its "Interactive API docs" section) | |
| HTTP status codes | IETF〈RFC 9110 HTTP Semantics〉 | |
| Idempotency (冪等) | Gregor Hohpe & Bobby Woolf《Enterprise Integration Patterns》 (2003)〈Idempotent Receiver〉 | |
| Version control, SCM, commit | Pro Git〈About Version Control〉; Git 官方文件〈git-commit〉 | |
| Git hooks | Git 官方文件〈githooks〉；跳過推送前檢查（`--no-verify`）：Git 官方文件〈git-push〉 | |
| Bare repository | Git 官方文件〈git-init〉 (`--bare`) | |
| Bundle（離線傳送 Repo） | Git 官方文件〈git-bundle〉 | |
| Python virtual environment | Python 官方文件〈venv — Creation of virtual environments〉 | |
| ed25519 | IETF〈RFC 8032 Edwards-Curve Digital Signature Algorithm (EdDSA)〉 | |
| SSH key fingerprint, ssh-keygen | OpenSSH 官方文件〈ssh-keygen〉 | |

## DDD (DLC)
- Eric Evans〈Domain-Driven Design Reference〉 (2015, the author's free summary of definitions and patterns).
- Eric Evans《Domain-Driven Design》(2003), chapters used:
  - ch.2 〈Communication and the Use of Language〉
  - ch.6 〈The Life Cycle of a Domain Object〉 (Aggregates)
  - ch.14 〈Maintaining Model Integrity〉 (Bounded Context, Context Map, Anticorruption Layer)
- Vaughn Vernon《Implementing Domain-Driven Design》(2013), chapters used:
  - ch.1 〈Getting Started with DDD〉
  - ch.2 〈Domains, Subdomains, and Bounded Contexts〉
  - ch.3 〈Context Maps〉
  - ch.4 〈Architecture〉 (Hexagonal / Ports and Adapters)
  - ch.10 〈Aggregates〉 (section 「Rule: Model True Invariants in Consistency Boundaries」)
- Plugin docs bundled in the learner package: cite by relative path, e.g. `vendor/domain-memory/references/<file>.md` or `tools/README.md`. Before citing a file, confirm it exists in the vendored zip.

## Speech decks: agentic practice, cases and research (main speech 01–05)
Speech notes cite these after checking them in `docs/research/speech-agentic-sources.md`. Company numbers are the company's own claims; say so when quoting them.
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Specs, planning, context | Addy Osmani〈How to write a good spec for AI agents〉 (2026); Birgitta Böckeler／martinfowler.com〈Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl〉 (2025); Simon Willison〈Context engineering〉 (2025), 〈Vibe engineering〉 (2025) | |
| Proof, review, guides and sensors | Simon Willison〈Your job is to deliver code you have proven to work〉 (2025); Birgitta Böckeler／martinfowler.com〈Harness engineering for coding agent users〉 (2026) | |
| Context and long tasks | Anthropic Engineering〈Effective harnesses for long-running agents〉 (2025); Anthropic〈Manage costs effectively〉, 〈How Claude remembers your project〉; Google〈GEMINI.md〉 (Gemini CLI docs) | |
| Rules files, Skills | GitHub Blog〈How to write a great agents.md: Lessons from over 2,500 repositories〉 (2025); Anthropic Engineering〈Equipping agents for the real world with Agent Skills〉 (2025) | |
| Autonomy, oversight, safety | Feng 等〈Levels of Autonomy for AI Agents〉 (arXiv, 2025); Anthropic〈Measuring AI agent autonomy in practice〉 (2026), 〈Our framework for developing safe and trustworthy agents〉 (2025), 〈Beyond permission prompts: making Claude Code more secure and autonomous〉 (2025); OWASP〈LLM06:2025 Excessive Agency〉; GitHub〈Risks and mitigations for GitHub Copilot cloud agent〉; Simon Willison〈The lethal trifecta for AI agents〉 (2025) | |
| Incidents | Fortune〈An AI-powered coding tool wiped out a software company's database, then apologized for a 'catastrophic failure on my part'〉 (2025-07-23); The Decoder〈AWS AI coding tool decided to delete and recreate a customer-facing system〉 (2026); AWS〈Security Update for Amazon Q Developer Extension for Visual Studio Code (Version #1.84)〉 (2025) | 〈AI coding tool Replit wiped database, called it a catastrophic failure〉 (URL slug, not the headline) |
| Large-scale cases | Anthropic〈How Anthropic runs large-scale code migrations with Claude Code〉 (2026); Airbnb Tech Blog〈Accelerating Large-Scale Test Migration with LLMs〉; Spotify Engineering〈1,500+ PRs Later: Spotify's Journey with Our Background Coding Agent (Honk, Part 1)〉 (2025); Stripe〈Minions: Stripe's one-shot, end-to-end coding agents〉 (2026); GitHub〈Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1〉 (2025) | |
| Adoption research | Google Cloud〈Announcing the 2025 DORA Report〉 (2025), 〈Introducing DORA's inaugural AI Capabilities Model〉 (2025); DORA〈State of AI-assisted Software Development 2025〉; Stack Overflow〈2025 Developer Survey — AI〉; METR〈We are Changing our Developer Productivity Experiment Design〉 (2026); Faros AI〈The AI Productivity Paradox Report 2025〉; Anthropic〈How AI is transforming work at Anthropic〉 (2025); Thoughtworks〈Technology Radar Vol. 34〉 (2026) | |

## Speech decks: DDD with Agents (DLC speech 01–04)
Checked in `docs/research/speech-dlc-ddd-sources.md`. DDD Europe 2026 titles are session abstracts only (no results); cite them as such.
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Language, Bounded Context, Context Map | Martin Fowler〈UbiquitousLanguage〉 (2006), 〈BoundedContext〉 (2014); DDD Crew〈The Bounded Context Canvas〉, 〈Context Mapping〉 | |
| Aggregates, events, ports | Vaughn Vernon〈Effective Aggregate Design, Part I〉 (2011); Martin Fowler〈DDD_Aggregate〉 (2013); Microsoft Azure Architecture Center〈Use Tactical DDD to Design Microservices〉, 〈Anti-Corruption Layer Pattern〉; Alberto Brandolini〈Introducing Event Storming〉 (2013); DDD Crew〈Aggregate Design Canvas〉; Alistair Cockburn〈Hexagonal Architecture〉 (2005); domainstorytelling.org〈Domain Storytelling Quick Start Guide〉 | |
| Decision records and review | AWS Prescriptive Guidance〈Architectural decision record process〉 | |
| Agents and context | Birgitta Böckeler／martinfowler.com〈Context Engineering for Coding Agents〉 (2026), 〈The role of developer skills in agentic coding〉 (2025); Spracklen 等〈We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs〉 (USENIX Security 2025); Anthropic〈Claude 3.7 Sonnet System Card〉 (2025) | |
| Thoughtworks Technology Radar entries | 〈Feedback sensors for coding agents〉, 〈Architecture drift reduction with LLMs〉, 〈Curated shared instructions for software teams〉, 〈Agent instruction bloat〉 (2026); 〈Using GenAI to understand legacy codebases〉 (2025) | |
| Legacy modernization | Ferri、Coggrave、Sheth／martinfowler.com〈Legacy Modernization meets GenAI〉 (2024); Nikolov 等〈How is Google using AI for internal code migrations?〉 (arXiv, 2025); Business Insider〈A team of engineers saved Morgan Stanley more than 280,000 hours this year〉 (2025); Anthropic〈How AI helps break the cost barrier to COBOL modernization〉 (2026); AWS Transform 使用者指南〈Modernization of mainframe applications〉 | |
| DDD community and AI | DDD Europe 2026〈Opening Keynote Eric Evans〉, 〈Accelerate your Strategic Design with LLMs〉, 〈Can AI be a Co-Domain Expert in Domain Modelling?〉, 〈The Curse of Unbounded Contexts: Using Domains as LLM Consumers〉, 〈AI-Generated End-to-End API Tests: An Experience Report in Legacy Modernization〉; InfoQ〈Eric Evans Encourages DDD Practitioners to Experiment with LLMs〉 (2024) | |

## Course-defined concepts
Some concepts are defined by this course itself (Gate, Level 1–3, Work Order, Time Skip, unlock codes). For these, cite the defining course document as 「📖 定義出處：本課程〈文件標題〉」, using the document's real H1 or page title. The checker verifies the title exists. Don't invent an external source for them.
