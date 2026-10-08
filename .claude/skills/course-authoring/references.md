# Verified 📖 延伸閱讀 sources (checked 2026-10-09)

Learner pages cite **titles only, never URLs**; the build rejects external URLs. Use the exact titles below. If a topic is not covered here, write 「你所用工具的官方文件中關於〈主題〉的章節」 and add a source to this list only after checking it online. Re-check titles once per release cycle, because vendors rename pages.

Format: `📖 延伸閱讀：〈組織〉官方文件〈標題〉…；你所用工具的官方文件通常有同名章節。`

## Agentic Coding techniques
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Prompt structure, clarity | Anthropic 〈Prompt engineering overview〉, 〈Prompting best practices〉; OpenAI 〈Prompt engineering〉 | 〈Be clear, direct, and detailed〉, 〈Let Claude think (chain of thought)〉: merged into Prompting best practices |
| Structured Output | Anthropic 〈Structured outputs〉; OpenAI 〈Structured Outputs〉 | |
| Model choice | Anthropic 〈Choosing the right model〉; GitHub 〈Changing the AI model for GitHub Copilot Chat〉 | 〈Choosing a model〉, 〈Changing the AI model for Copilot Chat〉 |
| Reasoning effort / thinking | Anthropic 〈Thinking〉, 〈Effort〉; OpenAI 〈Reasoning models〉 (has a "Reasoning effort" section) | 〈Building with extended thinking〉 |
| Token, context | Anthropic 〈Context windows〉, 〈Token counting〉; Anthropic Engineering 〈Effective context engineering for AI agents〉 (2025-09-29) | |
| Skill / rules file | Anthropic 〈Agent Skills〉; OpenAI Codex 〈Custom instructions with AGENTS.md〉; GitHub 〈Adding repository custom instructions for GitHub Copilot〉 | 「Codex 文件中的〈AGENTS.md〉說明」 |
| Plan first, verify with tests, agent work rules | Claude Code 官方文件〈Best practices for Claude Code〉 | Anthropic Engineering 〈Claude Code: Best practices for agentic coding〉 (moved into the Claude Code docs) |
| Testing | pytest 官方文件〈Get Started〉; skip／xfail: pytest 官方文件〈How to use skip and xfail to deal with tests that cannot succeed〉 | 〈Getting started〉 |
| Change review / Diff | Google Engineering Practices 〈Code Review Developer Guide〉; Git 官方文件〈git-diff〉 | |
| Commits, signing | Git 官方文件〈git-commit〉 (`-S`) | |
| Hashes (SHA256) | NIST〈FIPS 180-4 Secure Hash Standard (SHS)〉 | |

## Software engineering terms (glossary sources)
| Topic | Cite (exact title) | Retired titles (do not use) |
|---|---|---|
| Testing terms (regression, root cause, impact analysis, traceability, acceptance criteria, test basis) | ISTQB〈Glossary〉 (the ISTQB Standard Glossary of Terms Used in Software Testing) | |
| Gherkin, Given/When/Then | Cucumber 官方文件〈Gherkin Reference〉 | |
| ADR | Michael Nygard〈Documenting Architecture Decisions〉 (2011) | |
| MVP | Eric Ries《The Lean Startup》 (2011) | |
| Brownfield / legacy code | Michael Feathers《Working Effectively with Legacy Code》 (2004) | |
| Agent, coding agent, human-in-the-loop | Anthropic Engineering〈Building effective agents〉 (2024-12) | |
| /docs, Swagger UI, OpenAPI | FastAPI 官方文件〈First Steps〉 (its "Interactive API docs" section) | |
| Idempotency (冪等) | Gregor Hohpe & Bobby Woolf《Enterprise Integration Patterns》 (2003)〈Idempotent Receiver〉 | |
| Version control, SCM, commit | Pro Git〈About Version Control〉; Git 官方文件〈git-commit〉 | |
| Git hooks | Git 官方文件〈githooks〉 | |
| Bare repository | Git 官方文件〈git-init〉 (`--bare`) | |
| Python virtual environment | Python 官方文件〈venv — Creation of virtual environments〉 | |
| ed25519 | IETF〈RFC 8032 Edwards-Curve Digital Signature Algorithm (EdDSA)〉 | |
| SSH key fingerprint, ssh-keygen | OpenSSH 官方文件〈ssh-keygen〉 | |

## DDD (DLC)
- Eric Evans《Domain-Driven Design》(2003), chapters used:
  - ch.2 〈Communication and the Use of Language〉
  - ch.6 〈The Life Cycle of a Domain Object〉 (Aggregates)
  - ch.14 〈Maintaining Model Integrity〉 (Bounded Context, Context Map, Anti-Corruption Layer)
- Vaughn Vernon《Implementing Domain-Driven Design》(2013), chapters used:
  - ch.1 〈Getting Started with DDD〉
  - ch.2 〈Domains, Subdomains, and Bounded Contexts〉
  - ch.3 〈Context Maps〉
  - ch.4 〈Architecture〉 (Hexagonal / Ports and Adapters)
  - ch.10 〈Aggregates〉 (「Model True Invariants in Consistency Boundaries」)
- Plugin docs bundled in the learner package: cite by relative path, e.g. `vendor/domain-memory/references/<file>.md` or `tools/README.md`. Before citing a file, confirm it exists in the vendored zip.

## Course-defined concepts
Some concepts are defined by this course itself (Gate, Level 1–3, Work Order, Time Skip, unlock codes). For these, cite the defining course document as 「📖 定義出處：本課程〈文件標題〉」, using the document's real H1 or page title. The checker verifies the title exists. Don't invent an external source for them.
