---
name: task-execute
description: Interactively execute a task with plan approval, progress tracking, and result documentation
triggers: [execute task, run task, выполнить задачу, task-execute]
---

# Purpose

Execute a task from `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md` with interactive plan approval, step-by-step or autonomous execution, and documented results.

# When to use

- User triggers `/task-execute` or asks to work on a specific task
- Continuing an in-progress task

# Inputs needed

- `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md` — requirements and status
- `Проекты/{PROJECT}/README.md` — project context
- `.ai/skills/`, `.ai/knowledge/` — relevant skills and knowledge
- `База знаний/` — selectively, if relevant

# Procedure

## Step 1 — Load task

- Find task by number, title, or partial match
- If ambiguous — present options, ask user to choose → **STOP**
- Check status: completed → offer reopen; in-progress → resume; open → start

## Step 2 — Load context

- Project README
- Relevant skills from `.ai/skills/` (use `.ai/router.md` to classify)
- Relevant knowledge from `.ai/knowledge/` and project knowledge base
- Current project state (files, structure)

## Step 3 — Analyze and plan (interactive)

Break task into subtasks. Present plan:
- Task name, project, relevant skill
- Loaded context (list of materials)
- Numbered subtasks with brief descriptions
- Planned file changes (create / modify / delete)
- Complexity estimate (low / medium / high)

Ask: Plan correct? Additional context? Execution mode?

**STOP — wait for user response.**

## Step 4 — Choose execution mode

| Mode | Behavior |
|---|---|
| **Step-by-step** (default) | Confirm before each file change |
| **Autonomous** | Execute all, single confirmation before writing |
| **Trusted** (explicit request only) | Execute and write without intermediate confirmations |

## Step 5 — Execute subtasks

For each subtask:
- **Step-by-step:** show changes → **STOP** → wait for confirmation → apply
- **Autonomous:** execute all → show summary → **STOP** → wait for confirmation → apply
- Update progress in task.md after each step

### Checkpoints (for long tasks)

For tasks with complexity estimate **medium** or **high**, create checkpoints:
- **When**: after completing each major subtask, or every ~25-30 minutes of work
- **What to save**: update `## Прогресс` section in task.md with:
  - Completed subtasks (checked)
  - Remaining subtasks (unchecked)
  - Current context needed to resume (key decisions made, open questions)
- **Why**: allows any agent to resume from checkpoint after context reset

```markdown
## Прогресс
- [x] Подзадача 1: описание
- [x] Подзадача 2: описание
- [ ] Подзадача 3: описание (текущая)
- [ ] Подзадача 4: описание

**Контекст для продолжения**: [ключевые решения, промежуточные результаты, открытые вопросы]
```

Remove `## Прогресс` section when task is completed (replace with `## Результаты выполнения`).

## Step 6 — Quality check

After applying changes:
- Verify requirements coverage
- Check code (linting, formatting) if applicable
- Fix issues (with confirmation)

## Step 7 — Save results (versioned)

Determine the next version number:
1. Check `results/` for existing `v{N}/` subdirectories
2. If none exist but files are present directly in `results/` — treat as legacy `v0` (do not move or rename)
3. Create `results/v{N+1}/` (or `results/v1/` if first run)
4. Save all output files into the new version directory

**Never overwrite previous versions.** Each execution creates a new `v{N}/`.

## Step 8 — Document results

Show results summary:
- Completed subtasks
- Created/modified files (with version path)
- Problems and solutions
- Version number created

Ask to update task.md → **STOP** → after confirmation, update:

```markdown
## Результаты выполнения
- [What was done]
- [Created files in results/v{N}/]

## Статус
- **Статус**: выполнена
- **Завершена**: YYYY-MM-DD
- **Версия результата**: v{N}
```

If task.md has YAML frontmatter, also update: `status`, `completed`, `result_version`.

## Step 8.5 — Reflection (optional)

After documenting results, briefly reflect:
1. What went well?
2. What was harder than expected?
3. Any reusable insights for the system?

If the user agrees, add a `## Рефлексия` section before `## Статус`:

```markdown
## Рефлексия
- **Что получилось хорошо**: [...]
- **Что можно улучшить**: [...]
- **Инсайты для системы**: [...]
```

Skip reflection for trivial tasks (< 15 min). For longer tasks, propose it but don't insist.

## Step 9 — Knowledge capture

If useful patterns discovered during execution:
- Propose adding to knowledge base or creating a new skill
- **STOP** — wait for user decision

## PDF output

If user needs PDF: create Markdown in `results/v{N}/`, then convert:
```
python -m tools.markdown_to_pdf "results/v{N}/input.md" -o "results/v{N}/output.pdf"
```

# Output format

- Updated `task.md` with results, completion status, and version number
- Files in `results/v{N}/` (versioned, never overwriting previous)
- Optional knowledge base updates

# Quality bar

- [ ] Plan shown and approved before execution
- [ ] User confirmed file changes before writing (in step-by-step/autonomous modes)
- [ ] All requirements from task.md addressed
- [ ] Results documented in task.md
- [ ] Status updated to "выполнена"

# Anti-patterns

- Starting execution without showing plan
- Modifying files without confirmation
- Ignoring blockers and continuing with stubs
- Skipping quality check
- Not documenting results in task.md
