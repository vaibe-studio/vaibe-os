---
name: weekly-review
description: Generate a weekly review with completed tasks, progress on active work, blockers, and priority suggestions
triggers: [weekly, review, итоги недели, weekly-review, обзор недели]
---

# Purpose

Build a weekly review: what was completed, what's in progress, blockers and risks, and suggested priorities for next week.

# When to use

- End of work week (Friday/Sunday)
- User asks for weekly summary or triggers `/weekly-review`
- Before planning meetings

# Inputs needed

- `Проекты/**/Задачи/*/task.md` — all task cards
- `Проекты/**/Встречи/` — meetings from the past 7 days
- `Проекты/**/Планы/` — latest plan for cross-reference (optional)

# Procedure

## Step 1 — Determine scope

- Default: last 7 days from today
- If user specifies a date range → use it
- Ask which project(s) to include (all / specific)

**STOP — wait for selection.**

## Step 2 — Scan completed tasks

Find tasks where:
- `status: "выполнена"` and `completed` date falls within the review period
- Or `## Статус` shows completion within the period

Collect: task name, project, completion date, result version.

## Step 3 — Scan active tasks

Find tasks with `status: "в процессе"`:
- Check `## Прогресс` for checkpoint data
- Estimate completion percentage from checked/unchecked subtasks
- Note any stalled tasks (no changes in the period)

## Step 4 — Identify blockers and risks

Look for:
- Tasks on hold (`на холде`) — why?
- Tasks with `depends_on` pointing to incomplete tasks
- Open questions in `## Прогресс` sections
- Overdue deadlines

## Step 5 — Meetings summary

List meetings from the review period:
- Key decisions from `summary.md`
- Outstanding action items from `tasks.md`

## Step 6 — Present review

```markdown
## Обзор недели: {DD.MM} — {DD.MM.YYYY}

### Выполнено ({N} задач)
| Проект | Задача | Завершена | Версия |
|--------|--------|-----------|--------|

### В процессе ({N} задач)
| Проект | Задача | Прогресс | Примечание |
|--------|--------|----------|------------|

### Блокеры и риски
- ...

### Встречи за неделю ({N})
- ...

### Рекомендации на следующую неделю
1. Приоритет: ...
2. ...

### Метрики
- Выполнено: {N} задач
- В процессе: {N}
- Открыто: {N}
- Completion rate: {X}%
```

# Output format

- Markdown report in chat (default)
- Optionally save to `Проекты/{PROJECT}/Отчёты/Обзор недели - {DD.MM.YYYY}.md` if requested

# Quality bar

- [ ] All projects within scope scanned
- [ ] Completed tasks matched against the review period
- [ ] Stalled tasks flagged
- [ ] Blockers identified with context
- [ ] Actionable priorities suggested for next week

# Anti-patterns

- Modifying any task.md files
- Including tasks outside the review period without marking them
- Skipping blocker analysis
- Generating overly long reports — prioritize signal over noise
