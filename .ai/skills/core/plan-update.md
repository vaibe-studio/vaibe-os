---
name: plan-update
description: Create or update project management plan with task statuses and priorities
triggers: [plan, sprint plan, plan-update, обновить план, план проекта, точка сборки, личный план, план работ, сохрани план, сохрани в планы]
---

# Purpose

Create or update a snapshot management plan for a project, incorporating current task statuses, meeting outcomes, and priorities. Choose the right plan type for the situation.

This skill is for **project planning artifacts**. If the user needs a **cross-project managerial week** with owner map, waiting list, and live weekly control surface, use `weekly-operating-sheet.md` instead.

# When to use

- Start of a new sprint → **sprint plan**
- Strategic review, new phase, major changes → **full plan**
- Before important meeting, milestone, decision point → **checkpoint**
- User triggers `/plan-update`
- User requests to save/persist a generated plan or work list into the project → save to `Планы/`, **not** as a task in `Задачи/`

# When NOT to use

- User wants a secretary-style weekly operating sheet across multiple projects
- User explicitly asks for owner map / waiting list / live weekly management table
- The artifact is for the user's own weekly control rhythm rather than one project's execution plan

# Plan types

Three templates available. Reference: `База знаний/Планы — справочник обозначений.md`.

| Type | Template | When | Size |
|---|---|---|---|
| **Sprint plan** | `База знаний/Образец плана — спринт.md` | Weekly planning, "what to do now?" | 80-120 lines |
| **Full plan** | `База знаний/Образец плана — полный.md` | Phase start, strategy review, major changes | 150-250 lines |
| **Checkpoint** | `База знаний/Образец плана — точка сборки.md` | Pre-meeting, milestone, decision point | 100-150 lines |

Separate artifact for managerial work:
- **Operating sheet** → `weekly-operating-sheet.md` + `База знаний/Образец плана — управленческая неделя.md`

Decision tree:
```
Need to make decisions / prepare for a meeting?  → Checkpoint
Need full project picture (new phase, strategy)?  → Full plan
Just planning the week's work?                    → Sprint plan
Need a cross-project managerial control sheet?    → weekly-operating-sheet.md
```

# Inputs needed

- `Проекты/{PROJECT}/README.md` — goals, team, context
- `Проекты/{PROJECT}/Задачи/*/task.md` — canonical task cards
- `Проекты/{PROJECT}/Задачи/*/results/` — results presence
- `Проекты/{PROJECT}/Встречи/*/tasks.md`, `summary.md` — meeting outcomes
- `Проекты/{PROJECT}/Планы/` — previous plan versions
- Selected template from `База знаний/Образец плана — {тип}.md`

# Procedure

## Step 1 — Determine project

- If specified → proceed
- If not → show project list, ask user to select

**STOP — wait for selection.**

## Step 2 — Select plan type

Analyze context to recommend a type:
- User's request mentions meeting/decisions/review → **Checkpoint**
- User's request mentions strategy/phase/overview → **Full plan**
- Routine update, weekly planning → **Sprint plan**
- Cross-project week, owner map, waiting list, secretary-style control → **use `weekly-operating-sheet.md` instead**
- If unclear → ask user to choose

Read the selected template file.

## Step 3 — Check existing plans

- Scan `Проекты/{PROJECT}/Планы/`
- Find latest plan by version number
- No plans → N=1 (first plan); existing → N+1
- Plan type can change between versions

## Step 4 — Gather data

### 4a. Project metadata
- Goals, team, context from README.md

### 4b. Task inventory
- All tasks from `Задачи/*/task.md`
- Check `results/` for versioned subdirectories (`v1/`, `v2/`, ...)
- Note version count and latest version for each task

### 4c. Meeting outcomes
- Tasks and decisions from `Встречи/*/tasks.md`, `summary.md`

### 4d. Previous plan comparison
- Load latest plan for status comparison
- Find new tasks (in `Задачи/` but not in plan)
- Find missing tasks (in plan but not in `Задачи/` — mark "⚠️ requires check")

## Step 5 — Classify and prioritize

Statuses, priorities, AI capability levels defined in `База знаний/Планы — справочник обозначений.md`. Reference that file; do not duplicate the full legend in the plan.

## Step 6 — Generate plan

Follow the selected template. Key UX principles for all types — **"Inverted Pyramid"** (most important first, details last):

1. **TL;DR first** — 3-5 lines at the top: phase, focus, blocker, progress. A person reading only this block should understand the current state.
2. **Blockers & decisions second** — immediately after TL;DR. What must be resolved before or at the start of work. This is what a manager reads first.
3. **Sprint focus by baskets** — group tasks into thematic baskets (e.g. "Billing / Infrastructure / Notifications" or "Backend / Frontend / ML") rather than flat priority lists. Baskets emerge from sprint planning context, not from a rigid template. Include a "Cross-cutting tasks" basket for items spanning multiple baskets.
4. **Open questions aggregated** — collect unresolved questions from all recent meetings into a single table with source attribution (which meeting or plan raised it) and owner (who should answer).
5. **Changes section** — what changed since last plan, prominently placed but after the actionable content.
6. **Compact archive** — previous sprint results as bullet-list, not detailed tables. Goal: acknowledge what was done without distracting from the current sprint.
7. **Backlog at the bottom** — medium/long-term tasks in a compact table. Context only, not actionable.
8. **Reference legend** — link to `Планы — справочник обозначений.md`, never inline copy. Do not duplicate the legend in the plan body.
9. **Roadmap visual** — ASCII "ВЫ ЗДЕСЬ" for full plans and checkpoints (not required for sprint plans).

## Step 7 — Save

File name: `План - {N} - {DD.MM.YYYY} - {TITLE}.md`
Path: `Проекты/{PROJECT}/Планы/`

Show plan to user and confirm before saving.

# Output format

- `Проекты/{PROJECT}/Планы/План - {N} - {DD.MM.YYYY} - {TITLE}.md`
- Changes relative to previous version highlighted
- Link to legend reference, not inline copy

# Quality bar

- [ ] Project selected with user confirmation
- [ ] Plan type appropriate for the situation
- [ ] TL;DR section present with phase, focus, blocker, progress
- [ ] All tasks from `Задачи/` reflected in plan
- [ ] New tasks (since last plan) explicitly noted
- [ ] Missing tasks marked with warning
- [ ] Priorities assigned per criteria
- [ ] Legend referenced, not duplicated
- [ ] Previous plans not modified (new version only)

# Anti-patterns

- Editing old plans retroactively (only create new versions)
- Auto-selecting project without asking
- Missing tasks from `Задачи/` in the plan
- Creating plan without checking meeting outcomes
- Duplicating full legend in the plan body (reference the shared file)
- Putting the week plan at the end (it should be near the top)
- Using the same template type when another fits better
