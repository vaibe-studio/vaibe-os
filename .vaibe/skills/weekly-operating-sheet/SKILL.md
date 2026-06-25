---
name: weekly-operating-sheet
description: Create a cross-project weekly operating sheet for managerial work with decisions, owners, waiting list, and daily log. Triggers: weekly operating sheet, operating week, управленческая неделя, недельная таблица, owner map, weekly sheet, секретарь на неделю, менеджерская неделя.
license: MIT
---

# Purpose

Create a **cross-project weekly operating sheet** for a manager or founder: a living weekly control surface that keeps goals, decisions, owners, expectations from others, and daily movement in one place.

This skill is **not** for a project sprint plan and **not** for a retrospective review. It is for situations where the user needs an operational artifact to steer multiple workstreams during the week.

# When to use

- User asks for a weekly work sheet, owner map, weekly management table, or "secretary" support for the week
- Cross-project planning for the user's own managerial work
- Need to track `my decisions / delegated / waiting / next steps` in one place
- User wants a compact file that can be updated daily during the week

# When NOT to use

- Single-project sprint planning → use `.vaibe/skills/plan-update/SKILL.md`
- Weekly retrospective / summary → use `.vaibe/skills/weekly-review/SKILL.md`
- Task execution for one task card → use `.vaibe/skills/task-execute/SKILL.md`

# Inputs needed

- Scope of the week: all active projects or selected ones
- User's main outcomes for the week
- Owner logic: what stays with the user, what is delegated, what is only on control
- Recent meetings / task context for the included projects
- Latest relevant plans (optional, for continuity)
- Template: `База знаний/Образец плана — управленческая неделя.md`

# Procedure

## Step 1 — Determine scope

Ask:
- Which projects / workstreams are in scope?
- What kind of week is this: focused / balanced / firefighting / light?
- What 1-3 outcomes must be true by the end of the week?

If the user is not sure, help narrow scope through short secretary-style questions.

## Step 2 — Gather managerial context

Read only what is necessary to build the week:
- Recent meeting summaries and action items
- Active tasks that materially affect this week
- Latest project plan(s), if relevant

Focus on:
- blockers
- decisions needed
- delegated execution
- waiting dependencies

Do **not** over-scan the whole vault if a tight scope is enough.

## Step 3 — Separate work by managerial role

Build three categories:
- **My decisions** — items requiring the user's judgment, prioritization, or business logic
- **Delegated** — execution owned by others
- **Waiting / control** — things the user is waiting for or needs to monitor

This separation is mandatory. The operating sheet should reduce cognitive overload, not duplicate a task list.

## Step 4 — Build the weekly control surface

Use the template and structure it for fast human reading:

1. **Week screen (top block)**:
   - 3 weekly outcomes
   - 3 things requiring the user's decision
   - 3 key waiting items from others
2. **Main workstreams table**:
   - one row = one managerial track, not one tiny task
3. **Waiting list**:
   - from whom, what is expected, by when, what to do if delayed
4. **Daily log**:
   - short daily updates focused on movement and decisions
5. **Carry-over**:
   - what consciously moves to next week

## Step 5 — Optimize for usability

Before saving, check:
- Can the user understand the week in 30 seconds from the top block?
- Is each table row a meaningful workstream, not a micro-task?
- Is the column **"Требует моего решения"** present and useful?
- Is the waiting list explicit enough to unload memory?
- Is the daily log short enough to be sustainable?

If not, simplify.

## Step 6 — Show plan and confirm

Show:
- target path
- scope included
- what sections will be created
- what will not be touched

If the change is a new saved file, confirm with the user before creating it.

## Step 7 — Save

Default path:
- Cross-project managerial week → `Проекты/vAIbe-studio/Планы/`
- Single-project managerial week → `Проекты/{PROJECT}/Планы/`

File name:
`План - {N} - {DD.MM.YYYY} - Управленческая неделя {DD.MM-DD.MM.YYYY}.md`

# Output format

- Saved Markdown file in `Планы/`
- Concise summary in chat:
  - weekly outcomes
  - core workstreams
  - what requires the user's decisions

# Quality bar

- [ ] Scope selected consciously
- [ ] 1 row = 1 meaningful managerial track
- [ ] Top block readable in 30 seconds
- [ ] My decisions separated from delegated execution
- [ ] Waiting list present
- [ ] Daily log compact and maintainable
- [ ] File placed in `Планы/`, not in `Задачи/`
- [ ] Existing plans not rewritten retroactively

# Anti-patterns

- Turning the operating sheet into a backlog of micro-tasks
- Mixing user's decisions with delegated execution
- Writing a retrospective instead of a live weekly tool
- Hiding waiting dependencies inside prose
- Saving a cross-project weekly sheet into a single project task folder
