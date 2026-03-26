# /task-execute

> Cursor command wrapper. Canonical skill: `.ai/skills/core/task-execute.md`

## Quick Reference

1. Find task by number/title → load `task.md`
2. Load project context + relevant skills/knowledge
3. Analyze requirements → form execution plan
4. Show plan (task, subtasks, file changes, complexity) → **AskQuestion** for mode (step-by-step / autonomous / trusted) → **STOP**
5. Execute subtasks per chosen mode, confirming file changes
6. Quality check (linting, requirements coverage)
7. Show results → **AskQuestion**: update task.md? → **STOP**
8. Update `task.md` with results and status after confirmation
9. If patterns found → suggest `/evolve`

## Execution

Read and follow `.ai/skills/core/task-execute.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for: execution mode selection, task disambiguation, final confirmation
- Use **ReadLints** after code changes for quality check
- Follow `AGENTS.md` → Judgment Boundaries for NEVER/ASK/ALWAYS rules
- For PDF output: `python -m tools.markdown_to_pdf "input.md" -o "output.pdf"`
