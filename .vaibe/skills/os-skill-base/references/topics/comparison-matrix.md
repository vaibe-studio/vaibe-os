# Topic: cross-tool comparison matrix

## Contents

- Comparison matrix (feature × tool)
- What every tool agrees on
- Where they diverge (most → least)

## Comparison matrix

| Feature | Open canon | Cursor | Claude Code | OpenCode | Codex |
|---------|:--:|:--:|:--:|:--:|:--:|
| Unit = folder + `SKILL.md` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Required frontmatter | `name`, `description` | `name`, `description` | `description` (name=dir) | `name`, `description` | `name`, `description` |
| `name` regex (hyphens only) | ✅ | ✅ | dir is identifier | ✅ (strict) | ✅ |
| `name` must == folder | ✅ | ✅ | command = dir name | ✅ | ✅ |
| `description` ≤1024 chars | ✅ | ✅ | ✅ (+1,536 listing cap) | ✅ | ✅ |
| `paths` scoping | – | ✅ | ✅ | – | – |
| Disable implicit invocation | – | `disable-model-invocation` | `disable-model-invocation` | `permission.skill` | `agents/openai.yaml` |
| Hide from user / model-only | – | – | `user-invocable: false` | `tools.skill:false` | – |
| Tool pre-approval | `allowed-tools` (exp) | – | `allowed-tools` | – | – |
| Subagent/fork | – | – | `context: fork` | – | – |
| Dynamic context (`` !`cmd` ``) | – | – | ✅ | – | – |
| UI / policy / deps file | – | – | frontmatter | `opencode.json` | `agents/openai.yaml` |
| Primary dirs | (tool-defined) | `.cursor/skills/`, `.agents/skills/` | `.claude/skills/` | `.opencode/skills/`, `.claude/`, `.agents/` | `.agents/skills` |
| Listing budget | – | – | ~1% ctx | – | ≤2% ctx / 8k chars |
| Progressive disclosure | ✅ | ✅ | ✅ | ✅ | ✅ |

Legend: ✅ supported; `key` = the field/file that controls it; – = not a
documented feature. Per-tool detail and citations live in
[../sources/](../sources/).

## What every tool agrees on

- A skill is a folder with a `SKILL.md` (frontmatter + Markdown body).
- `name` + `description` are the load-bearing metadata; `description` drives
  discovery and must state **what** + **when** with trigger keywords.
- Progressive disclosure: only metadata at startup; body on activation; extra
  files/scripts on demand — keep `SKILL.md` lean, push depth to files.
- Unknown frontmatter keys are ignored → extra keys are safe but only honoured
  where the tool documents them.

## Where they diverge (most → least)

1. **Claude Code** — richest frontmatter (invocation control, tools, model,
   fork, hooks, dynamic context). See [../sources/claude-code.md](../sources/claude-code.md).
2. **Cursor** — `paths`, `disable-model-invocation`, `@`/`/` invocation, broad
   cross-tool dir reading. See [../sources/cursor.md](../sources/cursor.md).
3. **Codex** — `agents/openai.yaml` for UI/policy/deps; `.agents/skills` dirs;
   `$` invocation; 2% listing budget. See [../sources/codex.md](../sources/codex.md).
4. **OpenCode** — strict `name` regex, `permission.skill`, minimal frontmatter.
   See [../sources/opencode.md](../sources/opencode.md).
5. **Open canon** — the minimal intersection everything builds on. See
   [../sources/agentskills-canon.md](../sources/agentskills-canon.md).
