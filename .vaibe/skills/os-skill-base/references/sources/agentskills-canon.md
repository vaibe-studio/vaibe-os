# Agent Skills — open canon (agentskills.io)

- source: https://agentskills.io/home, https://agentskills.io/specification
- scanned: 2026-06-30
- fetch: home page + **full specification page** (verbatim-faithful digest;
  earlier spec was search-synthesis, now replaced with the official page)

The Agent Skills format was originally developed by Anthropic, released as an
open standard, and adopted across many agent products (Cursor, Claude Code,
OpenCode, Codex, Gemini CLI, and more). This is the **baseline** every tool
builds on; tool deltas live in the other source files.

## Contents

- What a skill is
- `SKILL.md` format (frontmatter, name, description, other fields)
- Body content
- Optional directories
- Progressive disclosure (with token guidance)
- File references
- Validation
- Why skills
- Notes for vAIbe-OS

## What a skill is

A skill is a **directory containing, at minimum, a `SKILL.md` file**, optionally
with `scripts/`, `references/`, `assets/`, and any other files:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## `SKILL.md` format

Must be YAML frontmatter (delimited by `---` at the very start) followed by a
Markdown body.

### Frontmatter fields (spec)

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars; lowercase letters, numbers, hyphens only; must not start/end with a hyphen; **must match the parent directory name**. |
| `description` | Yes | Max 1024 chars; non-empty; describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | 1–500 chars; environment requirements (intended product, system packages, network access). |
| `metadata` | No | Map of string keys → string values for client-defined properties (use unique keys to avoid conflicts). |
| `allowed-tools` | No (experimental) | Space-separated string of pre-approved tools; support varies by agent. |

Spec-compliant runtimes **ignore frontmatter keys they do not recognize** — this
keeps skills portable.

#### `name` field (exact rules)

- 1–64 characters
- only unicode lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`)
- must not start or end with `-`
- must not contain consecutive `--`
- must match the parent directory name

Equivalent regex: `^[a-z0-9]+(-[a-z0-9]+)*$`.
Valid: `pdf-processing`, `data-analysis`, `code-review`.
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen),
`pdf--processing` (consecutive hyphens).

#### `description` field

1–1024 chars; should describe **what** + **when**; include specific keywords so
agents match relevant tasks. Good: "Extracts text and tables from PDF files,
fills PDF forms, and merges multiple PDFs. Use when working with PDF documents...".
Poor: "Helps with PDFs."

#### Other field notes

- `license`: keep short (license name or bundled file name), e.g.
  `Proprietary. LICENSE.txt has complete terms`.
- `compatibility`: include only if there are real requirements, e.g.
  `Requires Python 3.14+ and uv`. Most skills omit it.
- `allowed-tools` example: `Bash(git:*) Bash(jq:*) Read`.

### Body content

Markdown after the frontmatter; **no format restrictions**. Recommended:
step-by-step instructions, input/output examples, common edge cases. The agent
loads the **entire** `SKILL.md` once it activates the skill, so split longer
content into referenced files.

## Optional directories

- `scripts/` — executable code; self-contained or document deps; helpful error
  messages; handle edge cases. Languages depend on the agent (Python, Bash, JS).
- `references/` — docs read on demand (`REFERENCE.md`, `FORMS.md`, domain files);
  keep each focused/small to save context.
- `assets/` — static resources (templates, images, data files / schemas).

## Progressive disclosure (with token guidance)

1. **Metadata (~100 tokens)** — `name` + `description` loaded at startup for all
   skills.
2. **Instructions (< 5000 tokens recommended)** — full `SKILL.md` body loaded on
   activation. **Keep `SKILL.md` under 500 lines.**
3. **Resources (as needed)** — files in `scripts/`/`references/`/`assets/` load
   only when required.

## File references

Use relative paths from the skill root (e.g. `references/REFERENCE.md`,
`scripts/extract.py`). Keep references **one level deep** from `SKILL.md`; avoid
deeply nested reference chains.

## Validation

The `skills-ref` reference library validates a skill:

```bash
skills-ref validate ./my-skill
```

It checks that `SKILL.md` frontmatter is valid and follows naming conventions.

## Why skills

Domain expertise as reusable instructions + resources; repeatable, auditable
workflows; cross-product reuse (author once, run on any compatible agent).

## Notes for vAIbe-OS

- vAIbe-OS canonical skill names are **hyphen slugs** (`os-skill-base`,
  `market-research`), which match the folder and satisfy the open-canon `name`
  regex directly — so `skills-ref validate` would pass on the name. vAIbe-OS also
  runs its own `doctor diagnose` for canon ↔ native-layer integrity.
- The canon stores the full skill under `.vaibe/skills/{name}/` (including
  `references/`); the per-tool native layer is generated from it (model A) and
  never duplicates `references/`.
