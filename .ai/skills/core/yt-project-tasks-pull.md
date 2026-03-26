---
name: yt-project-tasks-pull
description: Pull feedback from YouTrack into project plan
triggers: [yt-project-tasks-pull, youtrack pull, youtrack sync pull]
origin: bundled
---

# Purpose

Get feedback from YouTrack into vAIbe-os. This is the **secondary sync flow**: YouTrack → vAIbe-os. Compares YouTrack issue statuses with the latest project plan and creates a new plan version reflecting changes.

**IMPORTANT**: Project must be linked via `/yt-project-link` first.

# When to use

- User wants to sync YouTrack changes back to vAIbe-os
- Team members changed statuses/comments in YouTrack
- User triggers `/yt-project-tasks-pull`

# Inputs needed

- `.env` (local): `YOUTRACK_URL`, `YOUTRACK_TOKEN`
- `Проекты/{PROJECT}/README.md` — YouTrack link (YouTrack Integration section)
- `Проекты/{PROJECT}/Планы/План - N - ...md` — latest snapshot plan (comparison base)

# Outputs

- New plan file in `Проекты/{PROJECT}/Планы/` (version N+1) with:
  - "Changes from version N" section
  - Updated statuses/comments

# Data canon

- `Проекты/{PROJECT}/Задачи/*/task.md` — canonical task detail.
- `Проекты/{PROJECT}/Планы/*` — management snapshot and integrations point.

`/yt-project-tasks-pull` by default **does NOT edit** task cards, but reflects changes in a new plan version (to avoid unexpected edits). If needed, agent can separately offer to sync statuses in `task.md` (only after explicit confirmation).

# Critical rules

> **REQUIRED**: Work with `Планы/` folder, not `Задачи/`.
> **REQUIRED**: Compare YouTrack statuses with latest plan.
> **REQUIRED**: Create new plan with changes indicated.
> **REQUIRED**: Show change summary before creating plan.
> **FORBIDDEN**: Modify existing plans — only create new versions.

# Procedure

## 1. Initialization
- User invokes `/yt-project-tasks-pull`
- Optionally specifies project: `/yt-project-tasks-pull {PROJECT_NAME}`

## 2. Check configuration

Verify credentials, YouTrack link, and latest plan exist:
```
✅ YOUTRACK_URL: https://yt.example.com
✅ YOUTRACK_TOKEN: configured
✅ Project linked: ENSO
✅ Latest plan: План - 1 - 27.01.2026 - MVP готов.md
```

## 3. Find latest plan

- Sort by version number (План - **N** - ...)
- Read sync metadata from plan
- Extract task statuses from plan tables

## 4. Fetch data from YouTrack

API request:
```
GET /api/issues?query=project:{PROJECT_ID}&fields=id,idReadable,summary,customFields(name,value(name))
```

## 5. Compare statuses

| YouTrack Status | Plan Status | Result |
|-----------------|------------|--------|
| Open | ⬜ | No change |
| In Progress | ⬜ | Change: ⬜ → 🔄 |
| Fixed | ⬜ | Change: ⬜ → ✅ |
| Verified | ⬜ | Change: ⬜ → ✅ |
| Fixed | ✅ | No change |

## 6. Get comments

For each issue:
```
GET /api/issues/{issueId}/comments?fields=id,text,created,author(login,fullName)
```

## 7. Show change summary

> **STOP POINT**: Show changes and ask for confirmation.

Display: status changes, new comments, comparison base plan. Options:
1. Yes, create Plan N+1
2. View only (no changes)
3. Cancel

**→ STOP. Wait for choice.**

## 8. Create new plan

If confirmed, create plan: `План - {N+1} - {DATE} - {BRIEF_DESCRIPTION}.md`

Brief description auto-generated from changes (e.g. "Обновление статусов из YouTrack").

## 9. New plan structure

1. **"Changes from version N" section** — at document start
2. **Updated statuses** — in task tables
3. **Version history** — at document end
4. **Updated metrics** — recalculated percentages

## 10. Final report

Show: number of status changes, new comments, created plan path, progress before/after.

# Changes section format

```markdown
## Изменения с версии {N}

| Задача | Issue | Изменение | Кто изменил |
|--------|-------|-----------|-------------|
| Ревью опросника | [ENSO-11](URL) | Open → Verified (⬜ → ✅) | @manager |

### Новые комментарии

**ENSO-13 — Формирование КП**
> 👤 @manager (27.01.2026 14:30):
> Добавить в КП блок про анализ звонков

**Вывод:** Ревью опросника завершено.
```

# Version history format

```markdown
## История версий плана

| Версия | Дата | Изменения |
|--------|------|-----------|
| 1 | 27.01.2026 | Первоначальный план |
| 2 | 27.01.2026 | Pull из YouTrack: ENSO-11 ⬜→✅, ENSO-12 ⬜→🔄 |
```

# Status mapping

| YouTrack | Emoji | Text |
|----------|-------|------|
| Open | ⬜ | Не начата |
| In Progress | 🔄 | В процессе |
| Fixed | ✅ | Выполнена |
| Verified | ✅ | Выполнена (проверена) |
| Won't Fix | ⏸️ | На холде |
| Duplicate | ⏸️ | На холде |

# Plan creation algorithm

1. Copy previous plan structure
2. Update metadata: version N → N+1, date, Last Sync, Sync Direction: pull
3. Add "Changes from version N" section after metadata
4. Update task statuses in tables
5. Move completed tasks to "Completed" section
6. Update metrics (recalculate percentages)
7. Add entry to "Version History"
8. Update "Current Status Summary"

# Error handling

| Error | Action |
|-------|--------|
| No plans found | Recommend `/plan-update` first |
| Project not linked | Recommend `/yt-project-link` first |
| API error (401) | Token invalid/expired |

# Notes

- Pull does not modify YouTrack data — read only
- Existing plans are NOT modified — new version is created
- Each plan is a snapshot of project state at pull time
- Plan history = project change history
- Pull can run frequently — no new plan if no changes
- Comments from YouTrack are added to new plan's changes section
- If need to sync `Задачи/*/task.md` statuses — offer as separate confirmed step after pull

# Related commands

- `/yt-project-link` — link project before pull
- `/yt-project-tasks-push` — initial task publishing and Issue ID update in plan
- `/plan-update` — update snapshot plan (if there are new task cards)
