# /tasks-report

> Cursor command wrapper. Canonical skill: `.ai/skills/core/tasks-report.md`

## Quick Reference

1. **AskQuestion** for project (if not specified) → **STOP**
2. Scan `Задачи/*/task.md` + `results/`
3. Normalize statuses (✅/🔄/⏸️/⬜/❓/⚠️)
4. Collect summary metrics
5. Output report in chat (task table grouped by status + recommendations)
6. Optionally save to `Отчёты/` if user requests

## Execution

Read and follow `.ai/skills/core/tasks-report.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for project selection
- Default: output to chat only (no file creation)
- Follow `AGENTS.md` → Judgment Boundaries
