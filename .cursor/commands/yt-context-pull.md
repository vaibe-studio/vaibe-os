# /yt-context-pull

> Cursor command wrapper. Canonical skill: `.ai/skills/core/yt-context-pull.md`

## Quick Reference

1. Determine project (from argument or `.env` `YOUTRACK_PROJECT_ID`)
2. Run `.venv/bin/python -m tools.yt_context_pull --project {ID} --output-dir "Проекты/{NAME}/YouTrack"`
3. Read generated report, show summary to user
4. Suggest follow-up actions: `/plan-update`, create tasks, progress analysis

## Key rules

- **REQUIRED**: use `.venv/bin/python` to run
- **REQUIRED**: show user summary after export
- **FORBIDDEN**: modify previous reports — each export = new file
- **FORBIDDEN**: modify YouTrack data — read only

## Execution

Read and follow `.ai/skills/core/yt-context-pull.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for project selection if not specified
- Follow `AGENTS.md` → Judgment Boundaries
