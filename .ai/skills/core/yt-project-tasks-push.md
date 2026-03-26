---
name: yt-project-tasks-push
description: Publish tasks from vAIbe-os project plan to YouTrack
triggers: [yt-project-tasks-push, youtrack push, youtrack publish]
origin: bundled
---

# Purpose

Publish tasks from vAIbe-os to YouTrack. This is the **primary sync flow**: vAIbe-os → YouTrack. Creates new issues for unlinked tasks and updates existing ones.

**IMPORTANT**:
- Project must be linked via `/yt-project-link` first
- Tasks are taken from the **latest plan** in `Проекты/{NAME}/Планы/`

# When to use

- User wants to publish project tasks to YouTrack
- User triggers `/yt-project-tasks-push`

# Data canon

- **Task cards** in `Проекты/{PROJECT}/Задачи/*/task.md` — detailed canon.
- **Plan** — management snapshot and integration point.

Before publishing to YouTrack, the plan must be **current**. If tasks were created/changed after the last plan — first run `/plan-update {PROJECT}`.

# Inputs needed

- `.env` (local): `YOUTRACK_URL`, `YOUTRACK_TOKEN`
- `Проекты/{PROJECT}/README.md` — YouTrack link (YouTrack Integration section)
- `Проекты/{PROJECT}/Планы/План - N - ...md` — latest snapshot plan (task source)

# Outputs

- Changes in YouTrack: create/update issues (after confirmation)
- Updated latest plan: Issue ID/URL added + sync metadata (after confirmation)

# Critical rules

> **FORBIDDEN**: Publish tasks to unlinked project.
> **FORBIDDEN**: Overwrite YouTrack data without conflict warning.
> **FORBIDDEN**: Modify files without showing changes.
> **REQUIRED**: Use structured questions for all stop points.
> **REQUIRED**: Show change summary before publishing.
> **REQUIRED**: Handle conflicts interactively.
> **REQUIRED**: Update sync metadata in plan after successful publish.

# Plan task source

Tasks are extracted from the **latest file** in `Проекты/{NAME}/Планы/`:

```markdown
# Чек-лист задач команды {PROJECT}

## I. Критические задачи на текущий спринт
| № | Задача | Статус | Приоритет | ... |

## II. Выполненные задачи
| № | Задача | Статус | Результаты |

## III. Срочные задачи (эта неделя)
## IV. Среднесрочные задачи (1-2 недели)
## V. Долгосрочные задачи (1 месяц+)
```

# Status mapping (vAIbe-os → YouTrack)

| vAIbe-os | YouTrack |
|----------|----------|
| ⬜ / открыта | Open |
| 🔄 / в процессе | In Progress |
| ⏸️ / требует уточнения | To be discussed |
| на ревью | Submitted |
| ✅ / выполнена | Fixed |
| отменена | Won't fix |

**Important**: "Done" status doesn't exist in standard YouTrack config. Use "Fixed" for completed tasks.

# Priority mapping (vAIbe-os → YouTrack)

| vAIbe-os | YouTrack |
|----------|----------|
| 🔴 / критический | Critical |
| 🟠 / высокий | Major |
| 🟡 / средний | Normal |
| 🟢 / низкий | Minor |

# Procedure

## 1. Initialization
User invokes `/yt-project-tasks-push`, optionally with `{PROJECT_NAME}`.

## 2. Check configuration
Read `.env` and project README.md. Verify credentials and YouTrack link.

## 3. Select project (if not specified)

> **STOP POINT**: Use structured questions.

Show linked projects. **→ STOP. Wait for selection.**

## 4. Find latest plan
- Find `Проекты/{NAME}/Планы/` folder
- Select latest file by version number or modification date
- Read and parse plan

## 4.1 Check plan freshness (recommended)
- Quick check: are there new task cards in `Задачи/` not reflected in plan?
- If yes — warn: "Plan may be outdated, some tasks won't reach YouTrack"
- Offer: 1) cancel push, run `/plan-update` first, or 2) continue as-is (explicit confirmation only)

## 5. Scan tasks from plan
- Extract tasks from sections I, II, III, IV, V
- For each task: has Issue ID in `Issue` column → already linked; no Issue ID → new task
- Determine status and priority from symbols

## 6. Select tasks for publishing

> **STOP POINT**: Use structured questions.

Options:
- New tasks only (sections I, III, IV, V — N tasks)
- Critical and urgent only (sections I, III — N tasks)
- Critical only (section I — N tasks)
- All tasks including completed
- Cancel

**→ STOP. Wait for selection.**

## 7. Show publication plan

> **STOP POINT**: Show plan and ask for confirmation.

Show table of tasks to publish: new tasks to create, already published (skipped).

**→ STOP. Wait for confirmation.**

## 8. Execute publishing

**ONLY AFTER confirmation:**

### 8.1 Create new issues
```bash
curl -X POST "${YOUTRACK_URL}/api/issues?fields=id,idReadable,summary" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"project": {"id": "{PROJECT_ID}"}, "summary": "{Title}", "description": "{Description}"}'
```

### 8.2 Update statuses and priorities
```bash
curl -X POST "${YOUTRACK_URL}/api/issues/{issueId}" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "customFields": [
      {"name": "State", "$type": "StateIssueCustomField", "value": {"name": "Open"}},
      {"name": "Priority", "$type": "SingleEnumIssueCustomField", "value": {"name": "Critical"}},
      {"name": "Type", "$type": "SingleEnumIssueCustomField", "value": {"name": "Task"}}
    ]
  }'
```

Always set `Type = Task` when creating issues.

## 9. Update plan with Issue IDs

After successful publishing, update plan tables:
- Add `Issue` column with YouTrack links
- Add `## YouTrack Sync` section

```markdown
## YouTrack Sync
- **Project**: ENSO
- **Issues**: ENSO-1 — ENSO-28
- **Last Sync**: 2026-01-27T16:00:00Z
- **Sync Direction**: push
```

## 10. Results report

Show: created count, previously published count, total in YouTrack, created issue links, Kanban board URL.

# Kanban board notes

- Issues **auto-appear** on Kanban board if linked to project
- No separate API call needed to add to board
- To verify:
  ```bash
  curl -X GET "${YOUTRACK_URL}/api/agiles/{BOARD_ID}/sprints?fields=id,name,issues(id,idReadable)"
  ```

# API reference

### Get Project ID
```bash
curl -X GET "${YOUTRACK_URL}/api/admin/projects?fields=id,shortName,name" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" | jq '.[] | select(.shortName == "ENSO")'
```

### Create issue
```bash
curl -X POST "${YOUTRACK_URL}/api/issues?fields=id,idReadable,summary" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"project": {"id": "0-6"}, "summary": "Title", "description": "Description"}'
```

### Update status and priority
```bash
curl -X POST "${YOUTRACK_URL}/api/issues/ENSO-11" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "customFields": [
      {"name": "State", "$type": "StateIssueCustomField", "value": {"name": "Open"}},
      {"name": "Priority", "$type": "SingleEnumIssueCustomField", "value": {"name": "Critical"}},
      {"name": "Type", "$type": "SingleEnumIssueCustomField", "value": {"name": "Task"}}
    ]
  }'
```

### Check available statuses
```bash
curl -X GET "${YOUTRACK_URL}/api/admin/projects/{PROJECT_ID}/customFields?fields=field(name),bundle(values(name))" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}"
```

# Error handling

| Error | Action |
|-------|--------|
| Project not linked | Recommend `/yt-project-link` first |
| Plan not found | Recommend `/plan-update` first |
| Invalid status ("Done") | Use "Fixed" instead |
| API error (401) | Token invalid/expired |

# Notes

- Push does not delete YouTrack issues — only creates and updates
- Task source is **plan** in `Планы/`, not `Задачи/`
- If plan is outdated, push may miss new tasks — recommend `/plan-update` first
- All stop points use structured questions for interactivity
- Issues auto-appear on project Kanban board
- Always set `Type = Task` when creating issues
- Check available statuses before publishing ("Done" may not exist)

# Related commands

- `/yt-project-link` — link project before push
- `/plan-update` — update snapshot plan before publishing
- `/yt-project-tasks-pull` — after team work, get changes back to vAIbe-os
