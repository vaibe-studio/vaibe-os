# Topic: body & best practices (cross-tool)

How to write the `SKILL.md` body and organize supporting files. Mostly from
Anthropic, reinforced by every tool's progressive-disclosure model.

## Be concise

`SKILL.md` loads on activation and (in Claude Code) stays in context across
turns, so every line is a recurring cost. Only add what the model doesn't
already know; state what to do, not narration. (sources: anthropic-best-practices,
claude-code)

## Keep it short, push depth to references

- Body **under ~500 lines**; split into separate files near the limit.
  (sources: anthropic-best-practices, claude-code)
- `SKILL.md` is a table of contents linking to `references/`. Organization
  patterns: high-level guide + refs; by domain; conditional details. (source:
  anthropic-best-practices)
- **References one level deep** from `SKILL.md` (agents may partial-read nested
  refs). Add a table of contents to reference files >100 lines. (source:
  anthropic-best-practices)
- No-context-penalty until read: bundle comprehensive `references/` freely; only
  `name`+`description` are always loaded. (sources: agentskills-canon,
  anthropic-best-practices)

## Degrees of freedom

Match specificity to task fragility: prose steps (high freedom), parameterized
scripts (medium), exact scripts (low, for fragile/consistency-critical ops).
(source: anthropic-best-practices)

## Descriptions (the most important text)

Third person; specific; **what + when** with trigger keywords; key use case
first. The model picks among many skills using this alone. (sources:
anthropic-best-practices, cursor, codex)

## Workflows & feedback loops

Sequential steps; copyable checklists for complex tasks; validator→fix→repeat
loops (script- or doc-based). (source: anthropic-best-practices)

## Content hygiene

- No time-sensitive info (use an "old patterns" `<details>` block). (source:
  anthropic-best-practices)
- Consistent terminology throughout. (source: anthropic-best-practices)
- Forward-slash paths only. (source: anthropic-best-practices)
- Don't offer too many options — give a default + escape hatch. (source:
  anthropic-best-practices)

## Scripts (when used)

Solve don't punt (handle errors); no voodoo constants; provide utility scripts
(reliable, token-saving); make execute-vs-read intent explicit; declare deps;
fully-qualified MCP names `Server:tool`. Codex/Anthropic agree: prefer
instructions over scripts unless determinism/tooling is needed. (sources:
anthropic-best-practices, codex)

## Evaluate

Build ~3 evals first (evaluation-driven); baseline without the skill; iterate
with an author/tester loop; tune `name`/`description` if triggering misfires.
(source: anthropic-best-practices)

## vAIbe-OS mapping

vAIbe-OS skills are written in **English** (vault folder names stay Russian);
the canonical folder == `name` == hyphen slug; the canonical `SKILL.md` carries
flat frontmatter (`name`, `description`, `license`) + the full body. After adding
or editing a skill, regenerate the native layer and verify integrity:

```
uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py treat
uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py diagnose
```

Scripts, if any, follow `.vaibe/rules/scripts.md` (a self-contained `uv` project
per tool). A skill is worth creating when a multi-step job recurs. (source:
vAIbe-OS `.vaibe/rules/structure.md`, `.vaibe/rules/scripts.md`)
