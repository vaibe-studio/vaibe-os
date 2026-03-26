---
name: yt-context-pull
description: Pull YouTrack issue context AS IS into project directory
triggers: [yt-context-pull, youtrack context, youtrack pull context]
origin: bundled
---

# Purpose

Download current state of issues from YouTrack (statuses, assignees, comments), compare with previous export, and generate a plan-like report with a changes section.

**Result:** file `Контекст YT - {N} - {DD.MM.YYYY}.md` in `Проекты/{PROJECT}/YouTrack/`.

# When to use

- User wants to see current YouTrack issue state inside vAIbe-os
- User triggers `/yt-context-pull`

# Inputs needed

- `.env`: `YOUTRACK_URL`, `YOUTRACK_TOKEN`, `YOUTRACK_PROJECT_ID` (default instance)
- `.env`: `YOUTRACK_{PROFILE}_URL`, `YOUTRACK_{PROFILE}_TOKEN`, `YOUTRACK_{PROFILE}_PROJECT_ID` (per-profile, e.g. `YOUTRACK_PROJECT_PROFILE_*`)
- Previous cache (if exists): `Проекты/{PROJECT}/YouTrack/.cache/pull_*.json`

# Outputs

- Report: `Проекты/{PROJECT}/YouTrack/Контекст YT - {N} - {DD.MM.YYYY}.md`
- Cache: `Проекты/{PROJECT}/YouTrack/.cache/pull_{timestamp}.json`

# Procedure

## 1. Determine project

If user specified `{PROJECT_ID}` — use it. Otherwise — `YOUTRACK_PROJECT_ID` from `.env`.

Determine output directory: `Проекты/МойПроект/YouTrack/` (or ask user if project is ambiguous).

## 2. Run tool

```bash
.venv/bin/python -m tools.yt_context_pull --project {PROJECT_ID} --output-dir "Проекты/МойПроект/YouTrack"
```

For projects on a different YouTrack instance — use `--profile`:

```bash
.venv/bin/python -m tools.yt_context_pull --profile PROJECT_PROFILE --output-dir "Проекты/МойПроект/YouTrack"
```

For other projects — change `--output-dir`.

## 3. Verify result

- Read generated file `Контекст YT - {N} - {DD.MM.YYYY}.md`
- Show user a brief summary:
  - How many issues loaded
  - How many changes since last export
  - Path to file

## 4. (Optional) Suggest actions

Based on exported context, suggest:
- Update project plan (`/plan-update`)
- Create vAIbe-os tasks for new YouTrack tickets
- Perform progress analysis

# Report format

Report contains:

1. **Summary** — issue counts by status
2. **Changes since last export** — statuses, assignees, new issues, comments
3. **Current issue state** — tables by status (In Progress, Open, Fixed, etc.)
4. **Recent comments** — top-20 comments by date

# Rules

> **REQUIRED**: use `.venv/bin/python` to run.
> **REQUIRED**: show user summary after export.
> **FORBIDDEN**: modify previous reports — each export creates a new file.
> **FORBIDDEN**: modify data in YouTrack — read only.

# Related commands

- `/yt-project-tasks-pull` — sync YouTrack statuses with project plan
- `/yt-project-tasks-push` — publish tasks to YouTrack
- `/plan-update` — update project plan
