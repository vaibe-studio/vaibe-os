# OpenCode — agent skills

- source: https://opencode.ai/docs/skills/
- scanned: 2026-06-30
- fetch: full page (verbatim-faithful digest of all sections)

OpenCode loads reusable instructions from repo or home dir via a native `skill`
tool: agents see available skills and load full content on demand.

## Contents

- Place files / discovery
- Write frontmatter (name validation, length rules)
- Example
- Tool description & invocation
- Configure permissions (per-agent overrides, disable)
- Troubleshoot loading
- Notes for vAIbe-OS

## Place files / discovery

One folder per skill name with a `SKILL.md` inside. Search locations:

- Project: `.opencode/skills/<name>/SKILL.md`
- Global: `~/.config/opencode/skills/<name>/SKILL.md`
- Project Claude-compatible: `.claude/skills/<name>/SKILL.md`
- Global Claude-compatible: `~/.claude/skills/<name>/SKILL.md`
- Project agent-compatible: `.agents/skills/<name>/SKILL.md`
- Global agent-compatible: `~/.agents/skills/<name>/SKILL.md`

For project-local paths OpenCode **walks up from cwd to the git worktree**,
loading any matching `skills/*/SKILL.md` under `.opencode/` and any
`.claude/skills/*/SKILL.md` or `.agents/skills/*/SKILL.md` along the way. Globals
load from `~/.config/opencode/skills/*`, `~/.claude/skills/*`, `~/.agents/skills/*`.

## Write frontmatter (only these recognized; unknown ignored)

- `name` (required)
- `description` (required)
- `license` (optional)
- `compatibility` (optional)
- `metadata` (optional, string-to-string map)

### Validate names (strict)

`name` must: be 1–64 chars; be lowercase alphanumeric with single hyphen
separators; not start/end with `-`; not contain consecutive `--`; **match the
directory name** containing `SKILL.md`. Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`.

### Length rules

`description` must be 1–1024 chars. Keep it specific enough for the agent to
choose correctly.

## Example

```yaml
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---
## What I do
- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command
## When to use me
Use this when you are preparing a tagged release.
```

## Tool description & invocation

OpenCode lists available skills in the `skill` tool description, each entry a
`<name>` + `<description>`. The agent loads one via `skill({ name: "git-release" })`.

## Configure permissions (opencode.json)

```json
{ "permission": { "skill": {
  "*": "allow", "pr-review": "allow",
  "internal-*": "deny", "experimental-*": "ask"
} } }
```

`allow` = loads immediately; `deny` = hidden from the agent, access rejected;
`ask` = prompt before loading. Patterns support wildcards (`internal-*`). A skill
absent from `skillOverrides`-style config is treated as `allow`/on.

### Override per agent

Custom agents (frontmatter):
```yaml
permission:
  skill:
    "documents-*": "allow"
```
Built-in agents (`opencode.json`): `agent.<name>.permission.skill`, e.g. the
`plan` agent allowing `internal-*`.

### Disable the skill tool

Custom agent frontmatter `tools: { skill: false }` (or built-in via
`opencode.json` `agent.<name>.tools.skill: false`). When disabled the
`<available_skills>` section is omitted entirely.

## Troubleshoot loading

1. `SKILL.md` spelled in all caps. 2. Frontmatter includes `name` + `description`.
3. Names unique across all locations. 4. Skills with `deny` are hidden.

## Notes for vAIbe-OS

OpenCode's `name` regex is **hyphens only** — vAIbe-OS hyphen slugs
(`os-skill-base`) satisfy it directly, so there is no naming risk. The vAIbe-OS
OpenCode wrapper (`.opencode/skills/{name}/SKILL.md`) is emitted by `doctor treat`
with `name`, `description`, `license` (defaults to `MIT`), `compatibility:
opencode`, and `metadata.origin: vaibe-os`. Because OpenCode does **not**
auto-parse `@` references, the wrapper body spells out the canonical path
(`.vaibe/skills/{name}/SKILL.md`) and instructs the agent to open it explicitly.
