# /inbox-check

> Cursor command wrapper. Canonical skill: `.ai/skills/core/inbox-processing.md`

## Quick Reference

1. Scan `Инбокс/` → list files (exclude `.gitkeep`, `README.md`)
2. **AskQuestion** for processing mode (step-by-step / grouped / quick / delegated) → **STOP**
3. For each file/group:
   - Analyze content → form hypothesis
   - Show hypothesis → **AskQuestion** for project, type, name → **STOP**
   - For KB materials: assess universality → recommend placement
   - Show import plan → **AskQuestion** confirm/edit/skip → **STOP**
   - Execute import after confirmation
4. Show summary of all imported files

## Execution

Read and follow `.ai/skills/core/inbox-processing.md` for the full procedure.

## Cursor-specific enhancements

- Use **AskQuestion** for: mode selection, project assignment, file classification, import confirmation
- Group related choices into ONE AskQuestion call where possible
- For PDFs: use `tools/pdf_to_markdown/` for text extraction
- Follow `AGENTS.md` → Judgment Boundaries for NEVER/ASK/ALWAYS rules
