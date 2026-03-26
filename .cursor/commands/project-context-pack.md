# /project-context-pack

> Cursor command wrapper. Canonical skill: `.ai/skills/core/project-context-pack.md`

## Quick Reference

1. If project not specified → **AskQuestion** for project selection → **STOP**
2. Load project README, task statuses, knowledge base, recent meetings
3. Aggregate into unified context document
4. Show result → offer to save as file

## Execution

Read and follow `.ai/skills/core/project-context-pack.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for project selection when multiple projects exist
- Follow `AGENTS.md` → Judgment Boundaries for NEVER/ASK/ALWAYS rules
