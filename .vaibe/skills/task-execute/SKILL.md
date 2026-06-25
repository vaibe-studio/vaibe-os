---
name: task-execute
description: Interactively execute a task with plan approval, progress tracking, and result documentation. Triggers: execute task, run task, выполнить задачу, task-execute.
license: MIT
---

# Purpose

Execute a task from `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md` with interactive plan approval, step-by-step or autonomous execution, and documented results.

# When to use

- User triggers `/task-execute` or asks to work on a specific task
- Continuing an in-progress task

# Inputs needed

- `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/task.md` — requirements and status
- `Проекты/{PROJECT}/README.md` — project context
- `.vaibe/skills/` — relevant skills (including reference skills)
- `База знаний/` — selectively, if relevant

# Procedure

## Step 1 — Load task

- Find task by number, title, or partial match
- If ambiguous — present options, ask user to choose → **STOP**
- Check status: completed → offer reopen; in-progress → resume; open → start

## Step 2 — Load context

- Project README
- Relevant skills from `.vaibe/skills/` (discovered by their `description` frontmatter)
- Relevant reference skills from `.vaibe/skills/` and project knowledge base
- Current project state (files, structure)

### Marketing and UI tasks referencing an internal vAIbe-* product

For landing pages, banners, presentations, any copy "about the product" **before writing the copy**:

1. **Verify the product name** against `.vaibe/rules/naming-convention.md`. `task.md` and meetings often contain drift (`Vibe Analytics`, `vaibe Analytics`, `VAIbe-…`) — use the canonical form `vAIbe-{product}` in the artifact.
2. **Read the current product code** in `repositories/{name}/` (handlers, report formatters, message templates), not just the README. The README lags behind the code; the copy must reflect **what the user actually sees**, not the desired future.
3. If the copy references numbers (count of steps, questions, time), report-section wording, or classifications — extract them from the code, not from memory.

## Step 3 — Analyze and plan (interactive)

Break task into subtasks. **First output the full plan in the reply body to the user** (markdown), then — the structured choice. The plan is not replaced by the AskQuestion widget: the user must see it in chat without opening a form.

Mandatory plan blocks in the text:
- Task name, project, relevant skill
- Loaded context (list of materials)
- Numbered subtasks with brief descriptions
- Planned file changes (create / modify / delete)
- Complexity estimate (low / medium / high)
- Open decisions with the AI's recommendation (if any)

After the full plan in text — **AskQuestion** (one call): is the plan OK? / execution mode / other finite choices. See `.vaibe/rules/interactive-patterns.md`.

If AskQuestion is unavailable — the same questions as a **numbered list** in the text under the plan (fallback), not instead of the plan.

**Self-check before AskQuestion** (mandatory, in the same reply):
- [ ] The reply body contains **all** mandatory plan blocks (not "see above/below", not a pointer to tool output)
- [ ] There are numbered subtasks and a table/list of files
- [ ] AskQuestion is called **after** the plan, at the end of the reply — not instead of it

If the self-check fails — **do not call AskQuestion**; finish writing the plan first.

**STOP — wait for user response.**


## Step 4 — Choose execution mode

| Mode | Behavior |
|---|---|
| **Step-by-step** (default) | Confirm before each file change |
| **Autonomous** | Execute all, single confirmation before writing |
| **Trusted** (explicit request only) | Execute and write without intermediate confirmations |

### Clarification: what a "step" is for different task types

| Task type | Unit of a "step" | What to show before STOP |
|---|---|---|
| Structural (code, file edits, commands) | each file change | diff or content of the change |
| Synthesis (documents, context packs, knowledge) | each key decision or semantic block | AI recommendation from sources + an open question to the user |

**For synthesis tasks, step-by-step mode = "decision by decision":**
1. Pose one question/decision (e.g. "What exactly does the MVP automate?")
2. Show the AI synthesis from available sources as a hypothesis
3. **STOP** — request an answer, clarification, or user confirmation
4. Record the answer, move to the next decision
5. After all decisions — assemble the final document
6. Show the full draft → confirm → save

This ensures real user input into the document, not just an "ok" on the AI output.
**Mode error:** writing the whole document, showing it all at once, and asking "ok?" — that is autonomous, not step-by-step.

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

**Tabular artifacts (`.csv`):** one header row; for human-facing files the user will likely open in Excel on Windows/RU, default to **Excel-friendly CSV**: delimiter `;`, encoding `UTF-8 with BOM`. Use comma-CSV only if the file is primarily machine-facing. Don't concatenate multiple "sheets" into one CSV — separate files or `.xlsx`. Details: `.vaibe/skills/csv-tabular-results/SKILL.md`.

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
uv run --project .vaibe/scripts/markdown_to_pdf .vaibe/scripts/markdown_to_pdf/main.py "results/v{N}/input.md" -o "results/v{N}/output.pdf"
```

# Output format

- Updated `task.md` with results, completion status, and version number
- Files in `results/v{N}/` (versioned, never overwriting previous)
- Optional knowledge base updates

# Quality bar

- [ ] Full plan written in the reply body before any AskQuestion (subtasks, files, complexity visible in chat)
- [ ] Plan shown and approved before execution
- [ ] User confirmed file changes before writing (in step-by-step/autonomous modes)
- [ ] All requirements from task.md addressed
- [ ] Results documented in task.md
- [ ] Status updated to "выполнена"

# Anti-patterns

- **AskQuestion without a plan in the text** — only the choice form, without subtasks, files, and complexity in the message (regression 2026-05-20, task 023 vAIbe-analytics). AskQuestion complements the plan, it does not replace it.
- **A "plan below" stub without a plan body** — a single phrase "plan below, taking into account…" and immediately AskQuestion; the user sees only the form (regression 2026-06-07, task 012 vAIbe-vpn). **The cause is the agent not writing the markdown plan**, not the UI form. Cure: self-check before AskQuestion (Step 3).
- Starting execution without showing plan
- Modifying files without confirmation
- Ignoring blockers and continuing with stubs
- Skipping quality check
- Not documenting results in task.md
