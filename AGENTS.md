# AGENTS.md

**Project:** vAIbe-OS — personal file-based operating system for AI agents, turning any AI IDE into a structured assistant with memory and evolution.
**Core constraint:** File and folder names are in Russian. Strict directory hierarchy.

## Quick Start

- **Task routing**: `.ai/router.md` — classifies the task and selects the right skill
- **Rules**: `.ai/rules/structure-brief.md` — key paths, naming, task format
- **Principles**: `.ai/MANIFESTO-brief.md` — behavioral principles
- **Ontology**: `.ai/ONTOLOGY.md` — philosophical foundation (5 laws)
- **Invariants**: `.ai/GUARDS.md` — machine-checkable integrity rules

## Structure

| Directory | Purpose |
|---|---|
| `Проекты/` | Projects: `Задачи/`, `Встречи/`, `База знаний/`, `Планы/`, `README.md` |
| `База знаний/` | User's personal knowledge base |
| `Контакты/` | People directory (one person = one .md file) |
| `Инбокс/` | Inbox for importing external files |
| `.ai/` | IDE-independent core: skills, knowledge, rules, ontology, manifesto |
| `.ai/skills/core/` | Core actionable playbooks (9 vault operations) |
| `.ai/skills/domain/` | Domain-specific skills (13 bundled) |
| `.ai/rules/` | Canonical rules (source of truth for all IDEs) |
| `tools/` | Python utilities (`python -m tools.<name>`) |
| `repositories/` | Git submodules with code |

Full spec: `.ai/rules/structure.md`

## Skills

Start here: `.ai/router.md`

**Core** (13): task-create, task-execute, inbox-processing, evolve, plan-update, tasks-report, project-context-pack, daily-briefing, weekly-review, yt-context-pull, yt-project-link, yt-project-tasks-pull, yt-project-tasks-push.

**Domain** (13): `.ai/skills/domain/` — specialized skills (presentations, analysis, meetings, engineering, sales).

**Knowledge**: `.ai/knowledge/` — reference materials (non-actionable).

## Judgment Boundaries

**NEVER**
- Create files without user confirmation
- Choose project without asking the user
- Delete knowledge base files without migration plan
- Skip the confirmation step, even when context seems obvious

**ASK** (use structured UI when available)
- Before creating any task: confirm project, priority, name
- Before creating a new project
- Before importing files from Inbox
- Before any destructive file operation

**ALWAYS**
- Read relevant context files before making changes
- Verify file discovery: if search returns empty, cross-check with another tool before concluding a file does not exist
- Use Russian for file and folder names
- Number tasks with leading zeros: `001`, `002`, `010`
- Present finite choices as structured options (not open-ended text)
- Show full execution plan and get confirmation before writing files
- Follow `.ai/rules/structure.md` for directory layout

## Interaction Pattern

1. **Analyze** — scan workspace, form hypotheses
2. **Present** — show analysis + hypotheses as text
3. **Ask** — gather user choices via structured options (finite choices only)
4. **Plan** — show full execution plan with file paths and content summary
5. **Confirm** — wait for explicit user approval before creating/modifying files

STOP and wait for user response after steps 3 and 5.
