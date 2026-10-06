# Grindhead's agent skills

The agent skills I use day to day, kept in one place so they're easy to share and install.

They follow the open [Agent Skills](https://agentskills.io) format, so they work with Cursor, Codex, Claude Code, Gemini CLI, GitHub Copilot, OpenCode, Cline and other agents that read `SKILL.md` folders.

## What's in here

| Source | Skills | License |
| --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 39 engineering, productivity and writing skills, such as `tdd`, `code-review`, `diagnosing-bugs`, `grill-me` and `to-spec` | MIT |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto (Lauren Tan) | 51 skills, including `poteto-mode`, `how`, `why`, `blast-radius`, `unslop` and the `principle-*` set, plus the [pstack guide](docs/guide/README.md) | MIT |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | `supabase`, `supabase-postgres-best-practices` | MIT |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | `find-skills` | MIT |
| Mine | `loop-site-speed-optimisation` | MIT |

Full license texts are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

### Changes from upstream

- Matt Pocock and pstack both ship `tdd` and `teach`. Matt's keep the plain names. pstack's are renamed `pstack-tdd` and `pstack-teach`, and the pstack skills and guide that mention them point at the new names.
- pstack's `poteto-mode` and `make-bot-ui` use names with spaces upstream ("Poteto Mode", "Make Bot UI"), which some agents can't invoke. Here they're kebab-case to match their folders.
- The pstack guide lives in `docs/guide/` so the links from `poteto-help` resolve.

## Install

Clone into `~/.agents`, the shared global skills folder that most agents read:

```bash
git clone https://github.com/Grindhead/agent-skills.git ~/.agents
```

If you already have a `~/.agents` folder, clone somewhere else and copy or link the `skills/` folders you want into `~/.agents/skills/`.

Agents that keep their own folder (for example Claude Code at `~/.claude/skills`, Code Studio at `~/.codestudio/skills`) need a link per skill:

```bash
mkdir -p ~/.claude/skills
for s in ~/.agents/skills/*/; do ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"; done
```

To take only some of them, install from the upstream repos with [skills.sh](https://skills.sh) instead, e.g. `npx skills@latest add mattpocock/skills`.

## Getting started

- Not sure which skill fits? Ask `/ask-matt` (Matt's skills) or `/poteto-help` (pstack).
- For rigorous engineering work, start with `/poteto-mode`. Read the [pstack guide](docs/guide/README.md) first.
- Run `/setup-matt-pocock-skills` once per repo before using Matt's engineering skills.
- pstack is built for Cursor. `poteto-mode`, `how`, `why`, `pstack-teach`, `swarm` and `arena` start Cursor subagents with per-role models, so parts of them won't work elsewhere.

## Keeping it healthy

The latest smoke test results are in [docs/smoke-test-2026-10-06.md](docs/smoke-test-2026-10-06.md).

`scripts/validate_skills.py` checks every skill: valid frontmatter, a kebab-case `name` that matches its folder, a description under 1024 characters, and relative links that resolve. CI runs it on every push.

```bash
python3 scripts/validate_skills.py skills
```

Only skills listed in `.gitignore` as `!skills/<name>/` are published. Agents like Cursor install their own built-in skills into `~/.agents/skills`, and those stay out of this repo. To publish a new skill, add a line for it.

To pull upstream changes for the skills installed with skills.sh, run `npx skills update -g`, then check the renamed pstack skills by hand.
