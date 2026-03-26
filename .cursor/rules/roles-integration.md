---
description: Маршрутизация задач через skills
globs: [".ai/skills/**"]
---

# Skill-based task routing

> Architecture: core skills (vault operations) + domain skills (specialized).

## How it works

1. **meta-mind** remains the coordination layer — caring about user development, triggering `/evolve`
2. **router.md** classifies tasks: vault operations go to core skills, specialized work goes to domain skills
3. **Core skills** (`.ai/skills/core/`) manage the vault: task CRUD, inbox, planning, reporting, evolution
4. **Domain skills** (`.ai/skills/domain/`) provide domain expertise: presentations, analysis, meetings, engineering, sales

## Key files

- Task routing: `.ai/router.md`
- Core skills: `.ai/skills/core/` (9 vault operations)
- Domain skills: `.ai/skills/domain/` (13 specialized)
- Knowledge: `.ai/knowledge/`
- Judgment boundaries: `AGENTS.md`
- Manifesto: `.ai/MANIFESTO.md`
- Evolve triggers: `.ai/skills/core/evolve.md`
