---
name: tasks-report
description: Build detailed task status report for a project
triggers: [tasks report, task status, отчёт по задачам, tasks-report]
---

# Purpose

Build a detailed report on task statuses for a project based on `task.md` cards and `results/` presence. Answer: what's open, in progress, completed, and what needs attention.

# When to use

- User triggers `/tasks-report`
- Need quick project status overview
- Before sprint planning or status meetings

# Inputs needed

- `Проекты/{PROJECT}/Задачи/*/task.md` — task cards
- `Проекты/{PROJECT}/Задачи/*/results/` — results presence
- `Проекты/{PROJECT}/README.md` — project context (optional)
- `Проекты/{PROJECT}/Планы/` — latest plan for cross-reference (optional)

# Procedure

## Step 1 — Determine project

- If specified → proceed
- If not → show project list, ask user to select

**STOP — wait for selection.**

## Step 2 — Scan tasks

For each task folder in `Проекты/{PROJECT}/Задачи/`:
- Read `task.md` (if missing → mark "damaged structure")
- **Extract metadata** using this priority:
  1. **YAML frontmatter** (between `---` delimiters at the top) — preferred, machine-readable. Fields: `id`, `project`, `status`, `priority`, `created`, `completed`, `result_version`, `depends_on`, `tags`
  2. **Markdown `## Статус` section** — fallback for legacy tasks without frontmatter. Parse status, completion date, and result version from bullet points.
  3. If both exist and conflict — flag as `⚠️ Conflict` and show discrepancy
- Check `results/` for versioned subdirectories (`v1/`, `v2/`, ...):
  - Count versions (number of `v{N}/` directories)
  - Find latest version (highest N)
  - Note if legacy unversioned files exist directly in `results/`

## Step 3 — Normalize statuses

| Status | Criteria |
|---|---|
| ✅ Completed | Explicitly stated OR has `results/v{N}/` with files and no "in progress" indicators |
| 🔄 In progress | Explicitly stated |
| ⏸️ On hold | Explicitly stated |
| ⬜ Open / Not started | Default |
| ❓ Needs clarification | Missing key requirements/inputs |
| ⚠️ Conflict | Status says "completed" but no results (or vice versa) |

## Step 4 — Collect summary metrics

- Task count by status
- Completion percentage
- Top tasks without clear next step

## Step 5 — Output report

Display in chat (default — no file written):

```markdown
## Отчёт по задачам: {PROJECT}

### Резюме
- ✅ выполнено: X
- 🔄 в процессе: X
- ⏸️ на холде: X
- ⬜ открыто: X
- ⚠️ конфликты: X

### 🔄 В процессе
| Задача | Путь | Версии | Последняя |
|--------|------|--------|-----------|

### ⬜ Открыто
...

### ⚠️ Конфликты/проблемы
- 009-... marked "completed" but results/ empty
- 012-... has unversioned files in results/ (legacy format)

### Рекомендации
- `/plan-update {PROJECT}` — create/update management plan
- `/task-execute {TASK}` — execute specific task
```

Optionally save to `Проекты/{PROJECT}/Отчёты/Отчёт по задачам - {DD.MM.YYYY}.md` if user requests.

# Output format

- Markdown report in chat (default)
- Optional file in `Проекты/{PROJECT}/Отчёты/`

# Quality bar

- [ ] All tasks from `Задачи/` included
- [ ] Status conflicts flagged
- [ ] Summary metrics present
- [ ] Actionable recommendations included
- [ ] No task.md files modified without user request

# Anti-patterns

- Modifying task.md without explicit user request
- Ignoring status conflicts (e.g., "completed" with no results)
- Missing tasks from scan
- Auto-fixing structural issues without asking
- Overwriting previous results instead of creating new version
