---
name: daily-briefing
description: Generate a morning briefing with active tasks, upcoming deadlines, inbox items, and recent meetings. Triggers: briefing, daily, утренний, брифинг, daily-briefing, что сегодня.
license: MIT
---

# Purpose

Scan the workspace and present a concise morning briefing: what's in progress, what's due soon, what's new in Inbox, and latest meeting outcomes.

# When to use

- Start of a work session
- User asks "что сегодня?", "брифинг", or triggers `/daily-briefing`

# Procedure

## Step 1 — Scan active tasks

For each project in `Проекты/**/`.
**Exclude** `Проекты/_Архив/` and `repositories/` — archived/external projects are not scanned.

Important: do not rely only on ignore-aware recursive search from `Проекты/`, because private paths such as `Проекты/Личное/` may be hidden by `.gitignore`. `Проекты/Личное/` must be scanned explicitly as part of the briefing procedure.

- Find tasks with status `в процессе` (from YAML frontmatter `status` field or `## Статус` section)
- Find tasks with status `открыта` regardless of priority
- Note any `## Прогресс` checkpoints for resumable tasks
- Read `**Ответственный**` field from `## Статус` section
- Read priority if present (`high` / `medium` / `low`, `высокий` / `средний` / `низкий`, `критический`)

Build the briefing in four layers:
- `В фокусе сегодня` — all tasks `в процессе`, tasks with deadlines within 3 days, and open tasks with priority `high` / `critical`
- `Повестка по людям / совместные задачи` — all tasks involving the current user and at least one other person, regardless of priority, if they require coordination
- `Мои открытые задачи по приоритетам` — remaining open tasks of the current user, grouped by `high`, `medium`, `low`
- `Задачи команды` — tasks assigned to other people, shown separately from the user's own task field

For `Повестка по людям / совместные задачи`, highlight:
- who else is involved
- what interaction is needed: `проверить статус`, `сделать вместе`, `назначить синк`, `ждать ответа / решения`

Do not let medium- and low-priority open tasks disappear from the briefing entirely. They may be outside today's focus, but they remain part of the visible commitment landscape.

## Step 2 — Check deadlines

Scan task.md files for deadline mentions (frontmatter `deadline` field, or text patterns like "дедлайн", "срок", dates within 3 days of today).

## Step 3 — Check Inbox

List files in `Инбокс/`:
- Count and categorize (audio/video, documents, images, other)
- Highlight unprocessed items

## Step 4 — Recent meetings

Find meetings from the last 3 days in `Проекты/**/Встречи/` (excluding `_Архив/`):
- Show topic, date, and whether tasks.md has uncompleted items

## Step 5 — Present briefing

Display in chat:

```markdown
## Брифинг на {DD.MM.YYYY}

### В фокусе сегодня
| Проект | Задача | Приоритет | Прогресс |
|--------|--------|-----------|----------|

### Повестка по людям / совместные задачи
| Проект | Задача | С кем | Что нужно | Статус |
|--------|--------|-------|------------|--------|

### Мои открытые задачи по приоритетам
- High:
- Medium:
- Low:

### Задачи команды (другие ответственные)
| Проект | Задача | Ответственный | Статус |
|--------|--------|---------------|--------|

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
- [ ] `Проекты/Личное/` scanned explicitly when present
- [ ] `В фокусе сегодня` highlights current work and near-term pressure
- [ ] Joint tasks involving the user are shown as a coordination agenda
- [ ] Medium- and low-priority open tasks remain visible in the briefing
- [ ] Deadlines within 3 days highlighted
- [ ] Inbox status shown
- [ ] Actionable recommendations included

# Anti-patterns

- Creating or modifying any files
- Showing completed tasks (unless explicitly asked)
- Overwhelming with details — keep it concise
