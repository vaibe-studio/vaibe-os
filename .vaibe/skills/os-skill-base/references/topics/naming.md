# Topic: naming (cross-tool)

## The shared rule

Across the open canon, Cursor, OpenCode, and Anthropic the `name`:
- is **1–64 characters**,
- **lowercase letters, numbers, hyphens only**,
- must **not** start/end with `-` and has **no consecutive `--`**,
- **must match the parent folder name** exactly.

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`. (sources: agentskills-canon, opencode,
cursor, anthropic-best-practices)

Claude Code differs: the **directory name** is the command/identifier; the
frontmatter `name` is only a display label (except a plugin-root `SKILL.md`).
(source: claude-code)

## Style guidance (Anthropic)

Prefer **gerund** form (`processing-pdfs`, `analyzing-spreadsheets`); noun
phrases (`pdf-processing`) and action forms (`process-pdfs`) are acceptable.
Avoid vague (`helper`, `utils`), generic (`data`, `files`), reserved words
(`anthropic`, `claude`). Be consistent across the library. (source:
anthropic-best-practices)

## ✅ vAIbe-OS uses compliant hyphen slugs

vAIbe-OS canonical skills live at `.vaibe/skills/{name}/SKILL.md` where `{name}`
is a **hyphen slug** (Latin, lowercase) that matches its folder — e.g.
`os-skill-base`, `market-research`, `task-create`. This satisfies the open-canon
/ OpenCode / Cursor `name` regex directly, so there is **no dotted-name risk**
here (unlike conventions such as profitos's `{category}.{entity}.{action}`, whose
dots the hyphen-only regex rejects). (sources: agentskills-canon, opencode,
cursor; vAIbe-OS `.vaibe/rules/structure.md`)

The `doctor` tool loads `name` from the frontmatter and defaults it to the folder
name when absent (`canon.py`), and every emitted native wrapper reuses that
`name` verbatim, so `folder == name` holds across all four tool layers. Keep the
frontmatter `name` identical to the folder slug when authoring.
