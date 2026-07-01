---
name: os-skill-base
description: Mandatory prerequisite for any skill work — load this FIRST and build from it whenever authoring, reviewing, or changing a skill, instead of pattern-completing from another skill as a template. "Reference" names its content type, not its priority: it is not optional. The sourced reference for how agent skills are composed — the cross-tool open standard (agentskills.io) and the deltas for Cursor, Claude Code, OpenCode, and Codex, plus Anthropic authoring best practices, and how it maps onto the vAIbe-OS canon (model A — .vaibe/ canon + generated native layer). Triggers: skill authoring, creating a skill, editing a skill, SKILL.md, frontmatter, native layer, agentskills.
license: MIT
---

# os-skill-base

The knowledge base for **how skills are composed**, distilled from the canonical
sources. This skill is **reference content, not a tool** — it does not create or
audit skills. New skills are added to `.vaibe/skills/` and the native layer is
regenerated with `doctor treat` (model A). Load this whenever you author, review,
or change a skill.

Depth lives in `references/`; this file is the index and links every reference
directly (one level deep). Topic files synthesize across tools; source files are
faithful to each source (with scan dates).

## The load-bearing rules (true everywhere)

- A skill is a **folder containing `SKILL.md`** = YAML frontmatter + Markdown
  body. Optional `references/`, `scripts/`, `assets/` alongside.
- Required metadata: **`name`** and **`description`**. `name` is lowercase
  alphanumeric + hyphens, ≤64 chars, no leading/trailing/consecutive hyphens, and
  **matches the folder name**. `description` ≤1024 chars and states **what** the
  skill does **and when** to use it, with trigger keywords, in third person.
- **Progressive disclosure**: only `name`+`description` load at startup; the body
  loads on activation; `references/`/`scripts/` load on demand. So keep `SKILL.md`
  lean (< ~500 lines), front-load the key use case in `description`, and push
  depth into one-level-deep reference files.
- Unknown frontmatter keys are ignored by spec-compliant tools — extra keys are
  safe but only honoured where that tool documents them.

## References

Cross-tool topics (start here):

- [topics/comparison-matrix.md](references/topics/comparison-matrix.md) — feature × tool matrix; what tools agree on and where they diverge.
- [topics/naming.md](references/topics/naming.md) — `name` rules and how vAIbe-OS slugs stay compliant.
- [topics/frontmatter.md](references/topics/frontmatter.md) — which keys each tool honours.
- [topics/discovery-locations.md](references/topics/discovery-locations.md) — where each tool finds skills; scoping.
- [topics/invocation.md](references/topics/invocation.md) — explicit/implicit invocation, listing budgets.
- [topics/body-and-best-practices.md](references/topics/body-and-best-practices.md) — writing the body; Anthropic authoring rules.

Per-source detail (faithful digests, with scan dates):

- [sources/agentskills-canon.md](references/sources/agentskills-canon.md) — the open standard.
- [sources/cursor.md](references/sources/cursor.md) — Cursor.
- [sources/claude-code.md](references/sources/claude-code.md) — Claude Code.
- [sources/opencode.md](references/sources/opencode.md) — OpenCode.
- [sources/codex.md](references/sources/codex.md) — Codex.
- [sources/anthropic-best-practices.md](references/sources/anthropic-best-practices.md) — authoring best practices.

## How this maps onto vAIbe-OS

vAIbe-OS follows **model A** (see `.vaibe/rules/git-cross-platform.md`): the canon
is the single source of truth and the per-tool native layer is generated from it
and committed.

- **Canonical skill**: `.vaibe/skills/{name}/SKILL.md` — flat frontmatter
  (`name`, `description`, `license`) + the full Markdown body. Optional
  `references/`, `scripts/`, `assets/` live alongside in canon (see
  `.vaibe/rules/structure.md`).
- **Generated native layer**: `doctor treat` renders one thin wrapper per tool —
  `.claude/`, `.cursor/`, `.codex/`, `.opencode/skills/{name}/SKILL.md` — each
  carrying only metadata + a `GENERATED — DO NOT EDIT` marker and a pointer back
  to canon. The wrapper never copies the body, and `references/` are read from
  canon (not duplicated per tool). Per-tool frontmatter differs: Cursor adds
  `metadata.origin`; OpenCode adds `license`, `compatibility: opencode`,
  `metadata.origin`; Claude and Codex carry `name` + `description` only.
- **Anti-drift**: `doctor diagnose` (Guards, wired into a pre-commit hook and CI)
  checks the generated layer matches the canon — no missing, stale, or orphan
  wrappers. Never hand-edit the native layer; edit the canon and re-run `treat`.
- ✅ Unlike dotted-name conventions, vAIbe-OS skill names are **hyphen slugs**
  that match their folder, so they satisfy the open-canon `name` regex
  `^[a-z0-9]+(-[a-z0-9]+)*$` directly. See
  [topics/naming.md](references/topics/naming.md).
- New skills are created directly in `.vaibe/skills/`; discovery is by the
  `description` field (no separate router). Scripts, if any, follow
  `.vaibe/rules/scripts.md` (a `uv` project per tool).

Regenerate and verify the native layer from the vault root:

```
uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py treat
uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py diagnose
```

See `.vaibe/rules/structure.md`, `.vaibe/rules/git-cross-platform.md` (model A),
and `.vaibe/rules/scripts.md` for the canon itself.
