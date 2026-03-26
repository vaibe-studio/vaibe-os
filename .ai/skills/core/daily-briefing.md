---
name: daily-briefing
description: Generate a morning briefing with active tasks, upcoming deadlines, inbox items, and recent meetings
triggers: [briefing, daily, утренний, брифинг, daily-briefing, что сегодня]
---

# Purpose

Scan the workspace and present a concise morning briefing: what's in progress, what's due soon, what's new in Inbox, and latest meeting outcomes.

# When to use

- Start of a work session
- User asks "что сегодня?", "брифинг", or triggers `/daily-briefing`

# Procedure

## Step 1 — Scan active tasks

For each project in `Проекты/**/` (recursive — includes grouped folders like `Проекты/Личное/`):
- Find tasks with status `в процессе` (from YAML frontmatter `status` field or `## Статус` section)
- Find tasks with status `открыта` and priority `high`
- Note any `## Прогресс` checkpoints for resumable tasks

## Step 2 — Check deadlines

Scan task.md files for deadline mentions (frontmatter `deadline` field, or text patterns like "дедлайн", "срок", dates within 3 days of today).

## Step 3 — Check Inbox

List files in `Инбокс/`:
- Count and categorize (audio/video, documents, images, other)
- Highlight unprocessed items

## Step 4 — Recent meetings

Find meetings from the last 3 days in `Проекты/**/Встречи/`:
- Show topic, date, and whether tasks.md has uncompleted items

## Step 5 — Present briefing

Display in chat:

```markdown
## Брифинг на {DD.MM.YYYY}

### Задачи в работе
| Проект | Задача | Приоритет | Прогресс |
|--------|--------|-----------|----------|

### Требуют внимания (дедлайны ≤ 3 дня)
- ...

### Инбокс ({N} файлов)
- ...

### Недавние встречи
- ...

### Рекомендации
- `/task-execute {TASK}` — продолжить задачу
- `/inbox-check` — обработать входящие
- `/tasks-report {PROJECT}` — полный отчёт
```

# Output format

- Markdown report in chat (no files created)

# Quality bar

- [ ] All projects scanned
- [ ] Active tasks listed with current status
- [ ] Deadlines within 3 days highlighted
- [ ] Inbox status shown
- [ ] Actionable recommendations included

# Anti-patterns

- Creating or modifying any files
- Showing completed tasks (unless explicitly asked)
- Overwhelming with details — keep it concise
