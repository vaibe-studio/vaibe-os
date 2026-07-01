# Cursor — agent skills

- source: https://cursor.com/docs/skills
- scanned: 2026-06-30
- fetch: full official page (earlier search-synthesis replaced with verbatim-faithful digest)

Cursor implements the Agent Skills open standard (agentskills.io). A skill is a
portable, version-controlled package teaching the agent a domain task; it can
bundle scripts, references, and assets the agent acts on with its tools.

Four properties Cursor highlights: **portable** (works across any
standard-compatible agent), **version-controlled** (files in the repo, or
installed via GitHub repo links), **actionable** (scripts/templates/references),
**progressive** (resources load on demand).

## Contents

- How skills work
- Discovery locations (nested / category directories)
- `SKILL.md` frontmatter fields
- Scoping by files (`paths`)
- Scripts & optional directories
- Viewing / installing / migrating
- Notes for vAIbe-OS

## How skills work

At startup Cursor auto-discovers skills from the skill directories and presents
them to the agent, which decides relevance from context. Skills can also be
**manually invoked** by typing `/` in Agent chat and searching the skill name.

## Discovery locations

Auto-loaded from (project + user/global):

| Location | Scope |
|----------|-------|
| `.agents/skills/` | Project |
| `.cursor/skills/` | Project |
| `~/.agents/skills/` | User global |
| `~/.cursor/skills/` | User global |

For compatibility Cursor **also** loads Claude/Codex dirs: `.claude/skills/`,
`.codex/skills/`, `~/.claude/skills/`, `~/.codex/skills/`. (Relevant for
vAIbe-OS: the same skill can surface in Cursor via its `.cursor/`, `.claude/`,
or `.codex/` wrapper.)

Each skill = a folder with `SKILL.md`; optional `scripts/`, `references/`,
`assets/` dirs.

### Nested / category directories

- Category subfolders are purely organizational; Cursor walks the skills root
  **recursively** and picks up any `SKILL.md`. The skill's identity is the folder
  **containing `SKILL.md`** (e.g. `land-it`, `tdd`), not the parent category.
- Nested `.cursor/skills/` (or `.agents/skills/`) **anywhere in the repo** is
  picked up; a nested skill is **auto-scoped** to files under its directory (like
  an implicit `paths`). E.g. `apps/web/.cursor/skills/deploy-web` only surfaces
  when working under `apps/web/`.

## `SKILL.md` frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters, numbers, hyphens only; **must match parent folder name**. |
| `description` | Yes | What the skill does and when to use it; the agent uses it for relevance. |
| `paths` | No | Glob patterns scoping the skill to matching files; comma-separated string or list. Surfaces only when the agent works with matching files. |
| `disable-model-invocation` | No | `true` → only included on explicit `/skill-name`; not auto-applied from context (like a traditional slash command). |
| `metadata` | No | Arbitrary key-value mapping. |

Legacy: the `globs` field is still accepted as a fallback for older skills, but
new skills should use `paths`.

## Scoping by files (`paths`)

`paths` accepts a YAML list or a single comma-separated string of standard globs
(e.g. `"**/*.tsx"`, `"**/*.py, scripts/**/*.py"`). Leave unset for a skill
available regardless of open files.

## Scripts & optional directories

Reference scripts by relative path from the skill root (e.g.
`scripts/deploy.sh <environment>`); the agent runs them when the skill is
invoked. Scripts may be any executable language; should be self-contained, with
helpful error messages, handling edge cases.

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Executable code the agent can run |
| `references/` | Extra docs loaded on demand |
| `assets/` | Static resources (templates, images, data) |

Keep `SKILL.md` focused; move detail to separate files (progressive disclosure).

## Viewing / installing / migrating

- **View**: Customize → Skills; skills appear alongside rules in the
  "Agent Decides" section.
- **Install from GitHub**: Customize → Rules → Add Rule → Remote Rule (Github) →
  repo URL.
- **Migrate** (Cursor 2.4): built-in `/migrate-to-skills` converts dynamic rules
  (`alwaysApply: false`/undefined and no `globs`) → standard skills, and slash
  commands (user + workspace) → skills with `disable-model-invocation: true`.
  Rules with `alwaysApply: true` or specific `globs` are **not** migrated; user
  rules are not migrated (not file-system stored).

## Notes for vAIbe-OS

- The vAIbe-OS Cursor wrapper lives at `.cursor/skills/{name}/SKILL.md`, emitted
  by `doctor treat` with `name`, `description`, and `metadata.origin: vaibe-os`,
  plus a `GENERATED — DO NOT EDIT` marker and an `@.vaibe/skills/{name}/SKILL.md`
  pointer to canon. The hyphen-slug `name` matches the folder, so Cursor loads it
  cleanly. Don't hand-edit the wrapper — edit the canon and re-run `treat`.
