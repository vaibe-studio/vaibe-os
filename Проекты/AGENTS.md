# AGENTS.md — tasks & projects layer

> Auto-loaded by AI agents when working inside `Проекты/`. Vault folder names are in Russian; this file's prose is in English, but literal vault tokens (paths, section names, field names, enum values) stay as the system writes them.
> Full structure spec: `.vaibe/rules/structure.md`.

---

## Project

Each project is a `Проекты/{NAME}/` directory with a mandatory `README.md`.

`README.md` must contain a **Видимость** (visibility) field:
- `командный` (team, default) — tracked in Git
- `личный` (personal) — excluded from Git (patterns in `.gitignore` and/or `.git/info/exclude` — see `.vaibe/rules/git-cross-platform.md`)

**Mandatory subfolders**: `Задачи/`, `Встречи/`, `Исходные материалы/`, `База знаний/`.

---

## Task format

**Path**: `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/task.md`

**Numbering**: `{NUM}` — leading zeros, at least 3 digits (`001`, `002`, `010`). Numbers are unique within a project.

`task.md` must contain a `## Статус` section **at the end** of the file (the single source of truth for task state):

```markdown
## Статус
- **Статус**: открыта | в процессе | выполнена | на холде
- **Ответственный**: {Имя}           ← who executes/owns the task
- **Завершена**: YYYY-MM-DD          ← only for completed tasks
- **Версия результата**: v{N}        ← only for completed tasks with files in results/
```

`Версия результата` values:
- `v1`, `v2`, ... — files in `results/v{N}/`
- `inline` — the result is in `task.md` itself or in structural changes (code, configs)
- `inline (note)` — clarifies where the result is (e.g. `inline (code in repositories/)`)

---

## Result versioning

**Path**: `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/results/v{N}/`

- Each execution is saved in its own `v{N}/` subfolder (v1, v2, v3...); previous versions are never overwritten.
- `task.md` is not duplicated into `results/` — it stays at the task root.

**Version-numbering algorithm:**
1. Check `results/` for existing `v{N}/` subfolders.
2. If none — create `v1/`.
3. If some exist — find the maximum N, create `v{N+1}/`.

**Legacy format:** files placed directly in `results/` (without a `v{N}/` subfolder) are a legacy format and allowed; on a new execution do not overwrite them — create `v1/` for the legacy result and `v2/` for the new one.

**File names inside `v{N}/`** — at the task's discretion (Latin is allowed for code and HTML).

**CSV and tables:** the `.csv` format assumes one table and one header row; Cyrillic in UTF-8 (often with a BOM for Excel on Windows); multiple logical sheets go in separate `.csv` files or one `.xlsx`, not a "second sheet" inside one CSV.

---

## Naming

- Folders and files — **in Russian**
- Exception: files inside `results/v{N}/` (code, HTML — Latin allowed)
- System files (`README.md`, `task.md`, `AGENTS.md`) — Latin

---

## Judgment boundaries (in the projects context)

- **Before creating a task** — confirm with the user: project, priority, title.
- **Before creating a project** — confirm the name and visibility.
- **Before deletion** — show a knowledge-migration plan.
