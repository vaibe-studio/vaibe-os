# /yt-project-link

> Cursor command wrapper. Canonical skill: `.ai/skills/core/yt-project-link.md`

## Quick Reference

1. Check `.env` for `YOUTRACK_URL`, `YOUTRACK_TOKEN` → STOP if missing
2. Select vAIbe-os project → **STOP** for user choice
3. Check if already linked (README.md YouTrack Integration section)
4. Choose mode: link existing or create new → **STOP** for user choice
5. Validate/create YouTrack project (+ Kanban board + team members)
6. Show linking plan → **STOP** for confirmation
7. Update `README.md` with YouTrack Integration section

## Key rules

- **FORBIDDEN**: Link without user confirmation
- **FORBIDDEN**: Create YouTrack project without explicit consent
- **REQUIRED**: Check credentials first
- **REQUIRED**: Show plan and wait for confirmation

## Execution

Read and follow `.ai/skills/core/yt-project-link.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for all stop points (project selection, mode, confirmation)
- Follow `AGENTS.md` → Judgment Boundaries
