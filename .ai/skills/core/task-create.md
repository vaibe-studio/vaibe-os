---
name: task-create
description: Create a structured task card in vAIbe-OS with interactive user confirmation
triggers: [task, create task, new task, задача, создать задачу]
---

# Purpose

Interactively create a task card in `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md`, gathering project, priority, and context from the user before writing any files.

# When to use

- User requests a new task (explicitly or via `/task-create`)
- User describes work that needs tracking

# Inputs needed

- `Проекты/` — list of existing projects
- `Проекты/{PROJECT}/Задачи/` — existing tasks (to determine next number)
- `Проекты/{PROJECT}/README.md` — project context
- User's description of the task
- Critical external anchors mentioned by the user or discovered in context: URLs, event/tender names, source person/system, dates/deadlines, IDs

# Procedure

## Quick Reference

1. Scan `Проекты/` → form hypotheses about project, priority, title
2. Present hypotheses as text → structured choices for project, priority, title
3. **STOP** — wait for user response
4. If new project needed → ask details → **STOP**
4.5. For non-trivial tasks → ask user's vision on key aspects → **STOP**
4.6. Preserve critical external anchors in the future `task.md`
5. Determine next task number from `Проекты/{PROJECT}/Задачи/`
6. Show full plan as text (project, number, path, content summary)
7. Structured confirmation: create / edit / cancel → **STOP**
8. Create files ONLY after confirmation
9. Show result → suggest next steps

## Detailed Steps

### Step 1-3: Gather context

Scan existing projects and form hypotheses. Present analysis, then ask:
- Project (list existing + "Create new")
- Priority (low / medium / high)
- Proposed title (agree / suggest own)

In Cursor: call the **AskQuestion tool** (not describe it in text — actually invoke the tool).
In other IDEs: use the available structured input mechanism, or fall back to plain text.
**STOP and wait for response.**

### Step 4: New project (if needed)

If user wants a new project, ask:
- Project name (in Russian)
- Brief description
- **Visibility**: командный (team — tracked in Git) or личный (personal — excluded from Git)

Create project structure: `README.md` (include `Видимость:` field), `Задачи/`, `Встречи/`, `Исходные материалы/`, `База знаний/`.

**If visibility = личный**: automatically add `/Проекты/{NAME}/` to `.gitignore` in the "Private projects" section.

**STOP and wait for response.**

### Step 4.5: Clarify user's vision (for non-trivial tasks)

Before drafting the task card, assess task complexity:
- **Trivial** (rename file, fix typo, one-step action) → skip this step
- **Non-trivial** (creative work, research, multi-step delivery, ambiguous scope) → ask user

For non-trivial tasks, ask the user about key aspects they care about. Adapt questions to the specific task — don't use a fixed template. Examples of what to clarify:
- Expected deliverables and their format
- Constraints, preferences, or style requirements
- Scope boundaries (what's included / excluded)
- Reference materials or examples the user has in mind
- Success criteria — how to know the task is done well
- Critical external anchors that must survive into `task.md` if execution happens in another dialog (links, deadlines, external entities, source of the request)

Present as 2-4 focused questions (not a generic checklist). Use structured choices where options are finite, free-text where the answer is open-ended.

**STOP and wait for response.** Use answers to draft accurate description and requirements in the task card.

### Step 4.6: Preserve critical external anchors

Before drafting `task.md`, extract the external anchors without which the task may become ambiguous in a new dialog.

Typical anchors:
- URL or external document link
- Name of event / tender / lead / platform
- Source: who sent it or where it came from
- Deadline / date / submission window
- External ID, if relevant
- Why this external object matters to the task

Rule:

`If the task could be executed incorrectly in a fresh dialog without this fact, store it in task.md.`

Keep this compact. Put anchors in `## Контекст`; mention them in `## Требования` only if they affect the expected result.

### Step 5-7: Plan and confirm

Determine next task number (with leading zeros: 001, 002, 010).
Check whether all critical external anchors were preserved from the conversation into the planned `task.md`.
Show full creation plan including:
- Project name (existing/new)
- Task number and title
- Full path: `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/`
- Content summary for task.md

Ask for confirmation. **STOP and wait.**

### Step 8-9: Create and report

Create `task.md` with this structure:

```markdown
---
id: "{NUM}"
project: "{Project name}"
status: "открыта"
priority: "{priority}"
created: "YYYY-MM-DD"
completed: null
result_version: null
depends_on: []
tags: []
---

# Задача: {Title}

## Метаданные задачи
- **Номер**: {NUM}
- **Проект**: {Project name}
- **Создана**: YYYY-MM-DD
- **Приоритет**: {priority}

## Описание задачи
{Detailed description}

## Требования
{Requirements list}

## Контекст
{Context from user and knowledge base}

## Статус
- **Статус**: открыта
```

**YAML frontmatter** (between `---` delimiters) provides machine-readable metadata for automated reports and external integrations. Fill `depends_on` with task IDs if the task depends on other tasks. Fill `tags` with relevant labels.

The `## Статус` section is always at the END of `task.md`. Both frontmatter and `## Статус` must stay in sync. Upon task completion (via `task-execute`), update both:

```yaml
# frontmatter:
status: "выполнена"
completed: "YYYY-MM-DD"
result_version: "v{N}"
```

```markdown
## Статус
- **Статус**: выполнена
- **Завершена**: YYYY-MM-DD
- **Версия результата**: v{N}
```

Possible status values: `открыта`, `в процессе`, `выполнена`, `на холде`.
`Версия результата` / `result_version` is added only for completed tasks. Use `inline` when results are structural changes (code commits, config edits) rather than files in `results/`.

**Backwards compatibility**: old tasks without frontmatter remain valid. Adding frontmatter is optional when editing legacy tasks.

Report created path. Suggest `/task-execute` to start working.

# Output format

- `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md` — task card
- (optional) New project directory with standard structure

# Quality bar

- [ ] User confirmed project and title before file creation
- [ ] For non-trivial tasks: user's vision on key aspects was gathered before drafting
- [ ] Critical external anchors are preserved in `## Контекст` when relevant
- [ ] Task number is next sequential with leading zeros
- [ ] All file/folder names are in Russian
- [ ] Full plan was shown before any files were created
- [ ] task.md contains all required sections (metadata, description, requirements)
- [ ] For new projects: visibility (командный/личный) was asked and applied
- [ ] For личный projects: `/Проекты/{NAME}/` added to `.gitignore`

# Anti-patterns

- Using task-create to save a work plan or personal work list — plans go to `Проекты/{NAME}/Планы/` via `plan-update`, not to `Задачи/`
- Creating files before user confirms the full plan
- Choosing project/priority without asking
- Asking "create?" before showing what will be created
- Skipping confirmation even when context seems obvious
- Drafting detailed task description without asking user's vision for non-trivial tasks
- Using a fixed generic questionnaire instead of task-specific questions
- Omitting critical links, deadlines, source names, or external entities that are necessary to execute the task in a future dialog
