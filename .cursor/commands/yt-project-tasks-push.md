# /yt-project-tasks-push

> Cursor command wrapper. Canonical skill: `.ai/skills/core/yt-project-tasks-push.md`

## Quick Reference

1. Verify credentials and YouTrack link
2. Select project → **STOP** for user choice
3. Find latest plan, check freshness (warn if outdated → suggest `/plan-update`)
4. Scan tasks, classify: new vs already published
5. Select scope → **STOP** (all / critical+urgent / critical only)
6. Show publication plan → **STOP** for confirmation
7. Create issues via YouTrack API (always set Type=Task)
8. Update plan with Issue IDs + sync metadata
9. Show results report

## Key rules

- **FORBIDDEN**: Publish to unlinked project
- **FORBIDDEN**: Overwrite YouTrack data without conflict warning
- **REQUIRED**: Show summary before publishing
- **REQUIRED**: Update sync metadata after success

## Mappings

| vAIbe-os | YT Status | | vAIbe-os | YT Priority |
|----------|-----------|---|----------|-------------|
| ⬜ | Open | | 🔴 | Critical |
| 🔄 | In Progress | | 🟠 | Major |
| ✅ | Fixed | | 🟡 | Normal |
| ⏸️ | To be discussed | | 🟢 | Minor |

## Execution

Read and follow `.ai/skills/core/yt-project-tasks-push.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for all stop points (project, scope, confirmation)
- Follow `AGENTS.md` → Judgment Boundaries
