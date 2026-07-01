# Topic: invocation & loading (cross-tool)

Every tool supports **implicit** (model picks by `description`) and **explicit**
(user invokes) activation. The description is the trigger, so front-load the key
use case and trigger words. (sources: all)

## Explicit invocation syntax

| Tool | Explicit | Notes |
|------|----------|-------|
| Cursor | `/skill-name`, `@skill-name` | `@` attaches explicitly. (source: cursor) |
| Claude Code | `/skill-name` | command name = directory name. (source: claude-code) |
| OpenCode | `skill({ name })` via the `skill` tool; listed in tool desc | (source: opencode) |
| Codex | `$skill-name`, or `/skills` menu | (source: codex) |

## Controlling implicit invocation

- **Cursor / Claude Code**: `disable-model-invocation: true` → only explicit
  `/name`; recommended for destructive/billing-sensitive flows. (sources: cursor,
  claude-code)
- **Claude Code**: `user-invocable: false` → only the model invokes (background
  knowledge, hidden from `/` menu). Matrix in sources/claude-code.md. (source:
  claude-code)
- **OpenCode**: `permission.skill` = `allow`/`deny`/`ask`, with wildcards and
  per-agent overrides; `tools.skill: false` disables entirely. (source: opencode)
- **Codex**: `agents/openai.yaml` → `policy.allow_implicit_invocation: false`
  (default true) keeps explicit `$skill` only; disable via `config.toml`
  `[[skills.config]] enabled = false`. (source: codex)

## Listing budgets (description gets shortened under pressure)

- Claude Code: ~1% of context window; combined `description`+`when_to_use` capped
  at 1,536 chars; overflow shortens least-used. (source: claude-code)
- Codex: ≤2% of context window (or 8,000 chars if unknown); shortens, may omit
  with warning. (source: codex)
- Implication: put the decisive use case and trigger words **first** in
  `description`. (sources: claude-code, codex, anthropic-best-practices)

## Scoping by files

`paths` globs (Cursor, Claude Code) limit auto-activation to matching files;
Cursor also auto-scopes nested skills to their directory. (sources: cursor,
claude-code)

## vAIbe-OS mapping

vAIbe-OS skills are reference/knowledge or task procedures, discovered **by the
`description` field** (no separate router). A reference skill like `os-skill-base`
is meant for **implicit** load when authoring/changing a skill — so its
`description` must trigger on that (what + when + trigger keywords, key use case
first). Tool-specific invocation keys are not authored in canon; if ever needed
they go into the emitter matrix (`.vaibe/scripts/doctor/emitters.py`), keeping the
canonical `SKILL.md` general-only. (source: vAIbe-OS `.vaibe/rules/structure.md`)
