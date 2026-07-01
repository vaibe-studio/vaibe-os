# Codex (OpenAI) — agent skills

- source: https://developers.openai.com/codex/skills
- scanned: 2026-06-30
- fetch: full page (verbatim-faithful digest); Record & Replay sub-page referenced

Codex extends skills with task-specific capabilities, built on the open standard.
Available in the Codex CLI, IDE extension, and Codex app. **Skills** are the
authoring format for reusable workflows; **plugins** are the installable
distribution unit. Design the workflow as a skill, then package as a plugin to
share.

## Contents

- Progressive disclosure & budget
- Structure
- How Codex uses skills (activation)
- Create a skill
- Where to save skills (repo, user, admin, system)
- Distribute skills with plugins
- Install curated skills for local use
- Enable or disable skills
- Optional metadata — `agents/openai.yaml`
- Best practices (Codex)
- Notes for vAIbe-OS

## Progressive disclosure & budget

Codex starts with each skill's `name`, `description`, and **file path**. It loads
the full `SKILL.md` only when it decides to use the skill. The initial list uses
at most **2% of the model's context window** (or **8,000 characters** when
unknown); with many skills, Codex shortens descriptions first and may omit some
with a warning. The budget applies only to the initial list.

## Structure

A directory with `SKILL.md` (must include `name` + `description`) plus optional
`scripts/`, `references/`, `assets/`, and `agents/openai.yaml`:

```
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── agents/
    └── openai.yaml   # Optional: appearance, invocation policy, dependencies
```

## How Codex uses skills (activation)

- **Explicit**: include the skill in your prompt; in CLI/IDE run `/skills` or type
  `$` to mention a skill.
- **Implicit**: Codex chooses a skill when the task matches the `description`.
  Because matching depends on `description`, write concise descriptions with clear
  scope/boundaries and **front-load the key use case + trigger words** so it still
  matches if descriptions are shortened.

## Create a skill

- **Record & Replay** — if it's easier to show than describe: Codex records the
  workflow, inspects the steps, and drafts a reusable skill from the demo.
- **`$skill-creator`** — asks what the skill does, when it should trigger, and
  whether it stays instruction-only or includes scripts (instruction-only is the
  default).
- **Manually** — create a folder with a `SKILL.md`:
  ```
  ---
  name: skill-name
  description: Explain exactly when this skill should and should not trigger.
  ---
  Skill instructions for Codex to follow.
  ```
Codex detects changes automatically; restart if an update doesn't appear.

## Where to save skills (repo, user, admin, system)

Codex scans `.agents/skills` in **every directory from cwd up to the repo root**.
Same `name` in two places does **not** merge — both can appear in selectors.
Symlinked skill folders are followed.

| Scope | Location | Use |
|-------|----------|-----|
| REPO | `$CWD/.agents/skills` | Skills for a working folder/module |
| REPO | `$CWD/../.agents/skills` | Shared area in a parent folder |
| REPO | `$REPO_ROOT/.agents/skills` | Root skills for everyone in the repo |
| USER | `$HOME/.agents/skills` | Personal, any repo |
| ADMIN | `/etc/codex/skills` | Machine/container shared, default admin skills |
| SYSTEM | bundled with Codex | Broad-audience (skill-creator, plan, …) |

These are authoring/discovery locations; use **plugins** to distribute beyond a
repo.

## Distribute skills with plugins

Direct skill folders suit local authoring and repo-scoped workflows. To
distribute a reusable skill, bundle two or more skills, or ship a skill with an
app integration, package them as a **plugin**. Plugins can include one or more
skills and optionally app mappings, MCP server config, and presentation assets.

## Install curated skills for local use

`$skill-installer <name>` (e.g. `$skill-installer linear`) adds curated skills
beyond the built-ins; you can also prompt it to download from other repos. For
reusable distribution of your own skills, prefer plugins.

## Enable or disable skills

In `~/.codex/config.toml`, disable without deleting:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```
Restart Codex after changing `config.toml`.

## Optional metadata — `agents/openai.yaml`

Configures Codex-app UI, invocation policy, and tool dependencies:

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt to use the skill with"
policy:
  allow_implicit_invocation: false   # default true; false = explicit $skill only
dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

`allow_implicit_invocation` (default `true`): when `false`, Codex won't implicitly
invoke based on the prompt; explicit `$skill` still works.

## Best practices (Codex)

Keep each skill focused on one job; prefer instructions over scripts unless you
need deterministic behavior or external tooling; write imperative steps with
explicit inputs/outputs; test prompts against the description to confirm trigger
behavior. See github.com/openai/skills and the agent skills specification.

## Notes for vAIbe-OS

Codex's documented discovery dir is `.agents/skills`, but vAIbe-OS emits its
wrapper under `.codex/skills/{name}/SKILL.md` (via `doctor treat`, with `name` +
`description` only, a `GENERATED` marker, and a plain-path pointer to canon — Codex
does not auto-parse `@`). Confirm the running Codex loads `.codex/skills/`;
otherwise `.agents/skills` is the portable fallback. Codex-specific UI/policy/deps
belong in `agents/openai.yaml`, which would be added to the emitter matrix
(`.vaibe/scripts/doctor/emitters.py`) if ever needed.
