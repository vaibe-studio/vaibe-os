# Claude Code — skills

- source: https://code.claude.com/docs/en/skills
- scanned: 2026-06-30
- fetch: full page (verbatim-faithful digest of all sections)

Claude Code follows the agentskills.io standard and **extends** it (invocation
control, subagent execution, dynamic context injection). Custom commands have
merged into skills: `.claude/commands/deploy.md` and
`.claude/skills/deploy/SKILL.md` both create `/deploy`. A skill's body loads only
when used — cheaper than CLAUDE.md for long reference material. Create a skill
when you keep pasting the same checklist/procedure, or a CLAUDE.md section grows
into a procedure.

## Contents

- Bundled skills
- Where skills live
- Command name
- Frontmatter reference
- Content types
- Invocation control (matrix)
- Skill content lifecycle
- Supporting files
- Dynamic context injection (string substitutions)
- Run skills in a subagent
- Listing budget / overrides
- Evaluate & iterate
- Troubleshooting
- Notes for vAIbe-OS

## Bundled skills

Shipped, prompt-based skills available every session unless disabled
(`disableBundledSkills`): `/code-review`, `/batch`, `/debug`, `/loop`,
`/claude-api`, and the run/verify trio:
- `/run` — launch and drive your app to see a change working.
- `/verify` — build/run to confirm a change works (not just tests/type checks).
- `/run-skill-generator` — record the build/launch recipe as a per-project skill
  at `.claude/skills/run-<name>/` (run once per project; again if build changes).
  All three need Claude Code ≥ v2.1.145.

## Where skills live

| Location | Path | Applies to |
|----------|------|-----------|
| Enterprise | managed settings | All org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled |

Override on name clash: enterprise > personal > project; any overrides a bundled
skill of the same name. Plugin skills use `plugin:skill` namespace (no conflicts).
A skill takes precedence over a same-named `.claude/commands/` file.

- **Nested** `.claude/skills/` below cwd load on demand (monorepo). On name
  clash both stay available; the nested one gets a directory-qualified name
  (`apps/web:deploy`); `/deploy` runs the root one, `/apps/web:deploy` the nested.
- **Parent dirs**: project skills load from `.claude/skills/` in the start dir and
  every parent up to repo root.
- **`--add-dir`/`/add-dir`** exceptionally load `.claude/skills/` from the added
  dir (the `permissions.additionalDirectories` setting does **not**).
- **Live change detection**: adding/editing/removing a `SKILL.md` under watched
  dirs takes effect within the session; a brand-new top-level skills dir needs a
  restart. (Plugin `hooks/`, `.mcp.json`, `agents/` need `/reload-plugins`.)
- Adding `.claude-plugin/plugin.json` to a skill folder loads it as a plugin
  `<name>@skills-dir` (can bundle agents/hooks/MCP; needs workspace trust in a
  project).

## Command name

The command you type = the **directory name** (except a plugin-root `SKILL.md`,
where frontmatter `name` sets it). Frontmatter `name` is otherwise the display
label only. `.claude/commands/foo.md` → `/foo`.

## Frontmatter reference (all optional; only `description` recommended)

| Field | Description |
|-------|-------------|
| `name` | Display name; defaults to directory name. |
| `description` | What it does + when to use; basis for auto-invocation. If omitted, uses first paragraph. Combined with `when_to_use`, truncated at 1,536 chars in the listing — put the key use case first. |
| `when_to_use` | Extra trigger phrases/examples; appended to description (counts toward 1,536 cap). |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` or `[filename] [format]`. |
| `arguments` | Named positional args for `$name` substitution (space-separated string or YAML list; map to positions in order). |
| `disable-model-invocation` | `true` = Claude won't auto-load; only `/name`. Removes description from context; also blocks subagent preload and (v2.1.196+) scheduled-task firing. Default false. |
| `user-invocable` | `false` = hidden from `/` menu; only Claude invokes (background knowledge). Default true. |
| `allowed-tools` | Tools pre-approved (no prompt) while active. Space/comma string or list. |
| `disallowed-tools` | Tools removed from the pool while active; clears on your next message. |
| `model` | Model while active (rest of turn); accepts `/model` values or `inherit`. |
| `effort` | `low`/`medium`/`high`/`xhigh`/`max` while active. |
| `context` | `fork` = run in a forked subagent context. |
| `agent` | Subagent type when `context: fork` (Explore/Plan/general-purpose/custom). |
| `hooks` | Hooks scoped to this skill's lifecycle. |
| `paths` | Globs limiting auto-activation to matching files (path-specific-rules format). |
| `shell` | `bash` (default) or `powershell` for inline shell commands. |

## Content types

- **Reference content** — conventions/knowledge applied inline (no task), e.g.
  `api-conventions`.
- **Task content** — step-by-step actions (deploy/commit/codegen); often
  `disable-model-invocation: true`.
Keep the body concise: once loaded it **stays in context across turns** (recurring
cost). State what to do, not narration.

## Invocation control (matrix)

| Frontmatter | You invoke | Claude invokes | Loaded |
|-------------|-----------|----------------|--------|
| (default) | Yes | Yes | description always in context; full loads when invoked |
| `disable-model-invocation: true` | Yes | No | description NOT in context; loads when you invoke |
| `user-invocable: false` | No | Yes | description in context; loads when invoked |

Restrict Claude's access via permissions: deny `Skill`; allow/deny `Skill(name)`
or `Skill(name *)`. `disable-model-invocation: true` removes a skill from context
entirely.

## Skill content lifecycle

On invocation the rendered `SKILL.md` enters the conversation as one message and
**stays for the session** (not re-read each turn) — write standing instructions,
not one-time steps. Auto-compaction re-attaches the most recent invocation of each
skill after a summary, keeping the first 5,000 tokens, sharing a 25,000-token
budget filled from the most recent; older skills may drop. If a skill seems to
stop influencing behavior, content is usually still present — strengthen
`description`/instructions or use hooks; re-invoke after compaction if needed.

## Supporting files

Reference files load when needed; reference them from `SKILL.md` so Claude knows
what each holds and when to load it. Keep `SKILL.md` under 500 lines.

## Dynamic context injection

`` !`<command>` `` runs a shell command **before** the skill is sent and inlines
its output (preprocessing — Claude only sees the result; output is not re-scanned
for further placeholders). Inline form recognized only at line start or after
whitespace (`KEY=!`cmd`` stays literal). Multi-line: a fenced ` ```! ` block.
Disable via `disableSkillShellExecution: true` (bundled/managed unaffected).

### String substitutions

`$ARGUMENTS` (all args; appended as `ARGUMENTS: <value>` if absent),
`$ARGUMENTS[N]`/`$N` (0-based; shell-style quoting), `$name` (from `arguments`),
`${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}` (skill's dir),
`${CLAUDE_PROJECT_DIR}` (project root; v2.1.196+; applies to body and
`allowed-tools`). Escape a literal `$` before a digit/`ARGUMENTS`/name with `\`.

## Run skills in a subagent

`context: fork` runs the skill in isolation; SKILL.md content becomes the
subagent prompt (no conversation history). `agent:` picks the type; Explore/Plan
skip CLAUDE.md/git status. Only makes sense for skills with explicit instructions
(pure guidelines yield no actionable prompt). Inverse: a subagent with a `skills`
field preloads full skill content at startup.

## Listing budget / overrides

Skill names always listed; descriptions share a budget ~1% of context window;
overflow shortens least-used skills' descriptions first; `/doctor` shows what's
shortened/dropped. Raise via `skillListingBudgetFraction` or
`SLASH_COMMAND_TOOL_CHAR_BUDGET`; per-entry cap `skillListingMaxDescChars`
(default 1,536). `skillOverrides` in settings sets visibility per skill: `on`,
`name-only`, `user-invocable-only`, `off` (absent = `on`); plugin skills
unaffected (manage via `/plugin`).

## Evaluate & iterate

`skill-creator` plugin automates a baseline comparison loop: test cases in
`evals/evals.json`, isolated subagent runs, `grading.json`, `benchmark.json`
(pass rate/time/tokens with vs without skill), blind A/B version comparison,
description tuning, HTML review viewer.

## Troubleshooting

Not triggering → check description keywords; verify it appears via "What skills
are available?"; rephrase; invoke `/name`. Malformed YAML → body loads with empty
metadata (no `description` to match); run `--debug`. Triggers too often → make
description specific or add `disable-model-invocation: true`.

## Notes for vAIbe-OS

The vAIbe-OS Claude wrapper (`.claude/skills/{name}/SKILL.md`) is emitted by
`doctor treat` with `name` + `description` only, a `GENERATED` marker, and an
`@.vaibe/skills/{name}/SKILL.md` pointer to canon. Claude uses the **directory
name** as the command, and the wrapper folder is the hyphen slug, so the command
matches. Claude-specific keys (e.g. `allowed-tools`) are **not** authored in
canon; add them to the emitter matrix (`.vaibe/scripts/doctor/emitters.py`) if a
skill ever needs them. The nested-`CLAUDE.md` shim mechanism (Claude does not read
nested `AGENTS.md`) is also generated by `doctor`.
