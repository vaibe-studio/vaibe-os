# /task-create

> Cursor command wrapper. Canonical skill: `.ai/skills/core/task-create.md`

## Quick Reference

1. Scan `Проекты/` → form hypotheses
2. Show hypotheses as TEXT → **AskQuestion** for project, priority, title
3. **STOP** — wait for user response
4. If new project/role → **AskQuestion** for details → **STOP**
4.5. Non-trivial task → ask user's vision (deliverables, constraints, style, scope) → **STOP**
5. Preserve critical external anchors in `task.md` (`URL`, источник, дедлайн, внешний объект), если без них новый диалог потеряет контекст
6. Check knowledge base for context
7. Show full plan as TEXT (project, number, path, content)
7.5. Before confirmation, verify that critical external anchors are included in the planned `## Контекст`
8. **AskQuestion**: confirm / edit / cancel → **STOP**
9. Create files ONLY after confirmation
10. Show result → suggest `/task-execute`

## Execution

Read and follow `.ai/skills/core/task-create.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for all structured choices (see `.cursor/rules/interactive-patterns.md`)
- Group related choices into ONE AskQuestion call (project + priority + title)
- Use SEPARATE AskQuestion for final confirmation after showing plan
- Preserve critical external anchors in `## Контекст`: links, source names, dates/deadlines, external IDs, event/tender names
- Follow `AGENTS.md` → Judgment Boundaries for NEVER/ASK/ALWAYS rules
