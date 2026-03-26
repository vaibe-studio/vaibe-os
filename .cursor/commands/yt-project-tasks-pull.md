# /yt-project-tasks-pull

> Cursor command wrapper. Canonical skill: `.ai/skills/core/yt-project-tasks-pull.md`

## Quick Reference

1. Verify credentials, YouTrack link, latest plan exists
2. Find latest plan in `Проекты/{PROJECT}/Планы/`
3. Fetch issues from YouTrack, compare statuses with plan
4. Get new comments
5. Show change summary → **STOP** for confirmation
6. Create new plan version (N+1) with changes section
7. Show final report with progress delta

## Key rules

- **REQUIRED**: Work with `Планы/`, not `Задачи/`
- **REQUIRED**: Show change summary before creating plan
- **FORBIDDEN**: Modify existing plans — only create new versions

## Status mapping

| YouTrack | Emoji |
|----------|-------|
| Open | ⬜ |
| In Progress | 🔄 |
| Fixed / Verified | ✅ |
| Won't Fix / Duplicate | ⏸️ |

## Execution

Read and follow `.ai/skills/core/yt-project-tasks-pull.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for confirmation (create plan / view only / cancel)
- Follow `AGENTS.md` → Judgment Boundaries
