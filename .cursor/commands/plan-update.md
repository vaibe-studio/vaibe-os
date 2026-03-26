# /plan-update

> Cursor command wrapper. Canonical skill: `.ai/skills/core/plan-update.md`

## Quick Reference

1. **AskQuestion** for project (if not specified) → **STOP**
2. Select plan type: **sprint** (weekly) / **full** (strategic) / **checkpoint** (pre-meeting)
3. Check `Планы/` for latest version → determine next N
4. Gather data: README, `Задачи/*/task.md`, `results/`, `Встречи/*/tasks.md`
5. Compare with previous plan: find new/missing tasks
6. Classify statuses and priorities
7. Generate plan using template from `База знаний/Образец плана — {тип}.md`
8. Show plan → **AskQuestion** confirm → **STOP**
9. Save: `Планы/План - {N} - {DD.MM.YYYY} - {TITLE}.md`

## Plan types

| Type | Template | When |
|---|---|---|
| Sprint | `База знаний/Образец плана — спринт.md` | Weekly planning |
| Full | `База знаний/Образец плана — полный.md` | Phase start, strategy review |
| Checkpoint | `База знаний/Образец плана — точка сборки.md` | Pre-meeting, decisions |

If the user needs a **cross-project managerial week** with owner map, waiting list, and daily control, use `/weekly-operating-sheet` instead.

Legend: `База знаний/Планы — справочник обозначений.md` (reference, don't duplicate).

## Execution

Read and follow `.ai/skills/core/plan-update.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for: project selection, plan type selection, plan confirmation
- Never edit old plans — only create new versions
- Follow `AGENTS.md` → Judgment Boundaries
