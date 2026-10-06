# Skill smoke test, 6 October 2026

Every published skill was checked by `scripts/validate_skills.py`: frontmatter parses, `name` is kebab-case and matches the folder, the description is present and under 1024 characters, and relative links resolve. Link "failures" in a few skills are illustrative example paths inside their docs (for example `./src/billing/GLOSSARY.md` in `domain-modeling`), not real problems.

A smoke test can't fully run skills that depend on things outside one session. The **Needs** column flags them, from a scan of each skill's files:

- **subagents** (25 skills): the skill fans out to parallel agents. In pstack these are Cursor subagents with per-role models, so expect partial behaviour elsewhere.
- **issue tracker**: Matt's engineering flow (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `implement`) publishes to a tracker. Run `/setup-matt-pocock-skills` in a repo first. Neither Riddle Quest nor the portfolio has `docs/agents/issue-tracker.md` yet.
- **interactive**: the skill interviews you (`grill-me`, `grilling`, `teach`), so it only does something useful with a person answering.

**Exercised** means the skill's instructions were followed on real work (Riddle Quest and the portfolio) during this pass.

| Skill | Result | Needs | Notes |
| --- | --- | --- | --- |
| `architect` | Pass | named models |  |
| `arena` | Pass | subagents, named models |  |
| `ask-matt` | Pass | subagents, issue tracker, interactive |  |
| `automate-me` | Pass | subagents, interactive |  |
| `benchmark-checklist` | Pass | - |  |
| `blast-radius` | Pass | - |  |
| `bro` | Pass | - |  |
| `chief-of-staff` | Pass | subagents |  |
| `claude-handoff` | Pass | - |  |
| `code-review` | Pass, exercised | subagents, issue tracker, interactive | Smell baseline applied to the last Riddle Quest commit |
| `codebase-design` | Pass | subagents |  |
| `correct` | Pass | - |  |
| `create-verification-skill` | Pass | interactive, browser |  |
| `diagnosing-bugs` | Pass | interactive, browser |  |
| `domain-modeling` | Pass | - |  |
| `figure-it-out` | Pass | - |  |
| `find-skills` | Pass | browser |  |
| `git-guardrails-claude-code` | Pass | interactive |  |
| `grill-me` | Pass | interactive |  |
| `grill-with-docs` | Pass | interactive |  |
| `grilling` | Pass | interactive |  |
| `handoff` | Pass | - |  |
| `how` | Pass | subagents, named models |  |
| `implement` | Pass | - |  |
| `implement-spec` | Pass | subagents, issue tracker |  |
| `improve-codebase-architecture` | Pass, exercised | subagents, issue tracker, interactive | Hot-spot scan of Riddle Quest history |
| `interrogate` | Pass | subagents, named models, interactive |  |
| `loop-me` | Pass | interactive |  |
| `loop-site-speed-optimisation` | Fixed | - | Leading blank line broke frontmatter; name had spaces |
| `maintain-verification-skill` | Pass | subagents |  |
| `make-bot-ui` | Fixed | named models, browser | Name had spaces upstream |
| `migrate-to-shoehorn` | Pass | - |  |
| `no-comments` | Pass | subagents |  |
| `poteto-help` | Fixed | subagents, named models, browser | Guide links broken until docs/guide was added |
| `poteto-mode` | Fixed | subagents, named models, issue tracker, interactive, browser, gh CLI | Name had spaces upstream |
| `pr` | Pass | browser |  |
| `principle-attack-the-premise` | Pass | - |  |
| `principle-boundary-discipline` | Pass | - |  |
| `principle-build-the-lever` | Pass, exercised | subagents | Wrote scripts/validate_skills.py instead of checking by hand |
| `principle-encode-lessons-in-structure` | Pass | - |  |
| `principle-exhaust-the-design-space` | Pass | - |  |
| `principle-experience-first` | Pass | - |  |
| `principle-explain-the-number` | Pass | - |  |
| `principle-fix-root-causes` | Pass | - |  |
| `principle-foundational-thinking` | Pass | - |  |
| `principle-guard-the-context-window` | Pass | subagents, browser |  |
| `principle-laziness-protocol` | Pass | - |  |
| `principle-make-operations-idempotent` | Pass | subagents |  |
| `principle-migrate-callers-then-delete-legacy-apis` | Pass | - |  |
| `principle-minimize-reader-load` | Pass | - |  |
| `principle-model-the-domain` | Pass | - |  |
| `principle-never-block-on-the-human` | Pass | - |  |
| `principle-outcome-oriented-execution` | Pass | - |  |
| `principle-prove-it-works` | Pass, exercised | browser | Every change verified with the repo's own tests and audits |
| `principle-redesign-from-first-principles` | Pass | - |  |
| `principle-separate-before-serializing-shared-state` | Pass | - |  |
| `principle-sequence-verifiable-units` | Pass | - |  |
| `principle-subtract-before-you-add` | Pass, exercised | - | Untracked 87k copied build files in Riddle Quest |
| `principle-test-behavior-not-implementation` | Pass | - |  |
| `principle-type-system-discipline` | Pass | - |  |
| `prototype` | Pass | browser |  |
| `pstack-tdd` | Fixed | browser | Renamed from tdd (clash) |
| `pstack-teach` | Fixed | - | Renamed from teach (clash) |
| `recall` | Pass | subagents, issue tracker |  |
| `reflect` | Pass | subagents, named models |  |
| `research` | Pass | - |  |
| `resolving-merge-conflicts` | Pass | - |  |
| `retro` | Pass | - |  |
| `scaffold-exercises` | Pass | - |  |
| `setup-matt-pocock-skills` | Pass | issue tracker, interactive, gh CLI |  |
| `setup-pre-commit` | Pass | - |  |
| `setup-pstack` | Pass | subagents, named models, interactive |  |
| `setup-ts-deep-modules` | Pass | - |  |
| `show-me-your-work` | Pass | subagents, browser |  |
| `supabase` | Pass | issue tracker, interactive, browser |  |
| `supabase-postgres-best-practices` | Pass | - |  |
| `swarm` | Pass | subagents, named models |  |
| `tdd` | Pass | - |  |
| `teach` | Pass | interactive, browser |  |
| `technical-writing` | Pass, exercised | - | Applied to the case study and README |
| `to-questionnaire` | Pass | interactive |  |
| `to-spec` | Pass | issue tracker, interactive |  |
| `to-tickets` | Pass | issue tracker, interactive |  |
| `triage` | Pass | issue tracker, interactive, gh CLI |  |
| `typescript-best-practices` | Pass, exercised | - | Applied to the Stripe module type fix |
| `unslop` | Pass, exercised | - | Applied to the rewritten Riddle Quest case study |
| `wait-what` | Pass | - |  |
| `wayfinder` | Pass | subagents, issue tracker, interactive |  |
| `why` | Pass | subagents, named models, issue tracker, browser, gh CLI |  |
| `wizard` | Pass | interactive, browser |  |
| `writing-beats` | Pass | - |  |
| `writing-for-agents` | Pass | subagents |  |
| `writing-fragments` | Pass | interactive |  |
| `writing-shape` | Pass | interactive |  |
