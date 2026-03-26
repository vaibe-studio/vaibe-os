---
name: meeting-processing
description: Transcribe, analyze, and import meeting recordings into project structure
triggers: [meeting, recording, transcribe, audio, video, meeting-processing]
origin: bundled
---

# Purpose

Process a meeting recording (audio/video) or raw transcript: transcribe if needed, generate summary and tasks, and save to the project's meeting directory with user confirmation.

# When to use

- User has a meeting recording to process
- Raw transcript needs analysis and structuring
- User triggers `/meeting-processing`

# Inputs needed

- Audio/video file or raw transcript (from argument or `Инбокс/`)
- `Проекты/` — project list for classification
- `tools/meeting_transcriber/` — transcription tool (if audio/video)

# Procedure

## Step 1 — Identify input file

- If path provided → use it (verify existence and format)
- If no path → scan `Инбокс/` for `.mp4`, `.webm`, `.mp3`, `.wav`, `.md`
- If multiple found → show list, ask which to process

**Batch mode (multiple files):** Transcribe all files in background first (sequential or parallel via `--backend local`), then process each one step-by-step with confirmation. Do not ask for project/topic until transcription is done.

**STOP — wait for file selection.**

## Step 2 — Transcribe (if audio/video)

Run transcription:
```bash
python -m tools.meeting_transcriber <file> --lang ru --backend local
```
Alternative: `--backend assemblyai` (cloud, needs ASSEMBLYAI_API_KEY).

If input is already `.md` transcript → skip this step.

## Step 3 — Analyze transcript

Extract:
- Meeting purpose/topic
- Key points and decisions
- Action items (tasks)
- Open questions

Form hypotheses about: project, date, topic.

**Edge case detection (check before proceeding to Step 4):**

| Case | Signal | Action |
|---|---|---|
| **Дубль** | Тема/дата/участники совпадают с существующей встречей в `Встречи/` | Показать совпадение → спросить: skip / update existing |
| **Случайная запись** | Транскрипт < ~30 реплик, явно обрывается или не содержит смысловой нагрузки | Сообщить о краткости → предложить пропустить |
| **Внешний вебинар** | Публичное мероприятие, сторонний спикер, контент не привязан к проекту | Показать саммари → предложить: сохранить в `База знаний/` / `Проекты/{PROJECT}/База знаний/` / пропустить |

При обнаружении edge case — **STOP**, показать вывод, дождаться решения пользователя.

## Step 4 — Ask user for context

Present hypotheses and ask:
- Which **project**? (must exist in `Проекты/`; if not → offer to create)
- **Date** (DD.MM.YYYY)?
- **Topic** (brief Russian name)?
- **Meeting number** N? (suggest next available)

**STOP — wait for response.**

## Step 5 — Generate summary.md draft

```markdown
# Саммари встречи: {TOPIC}

## Контекст
- **Проект**: {PROJECT}
- **Дата**: {DD.MM.YYYY}
- **Источник**: transcript.md
- **Участники**: {from transcript or "не указано"}

## Итоги (кратко)
## Решения и договорённости
## Риски / блокеры
## Следующие шаги
## Открытые вопросы
```

Show draft. **STOP — wait for approval/edits.**

## Step 6 — Generate tasks.md draft

```markdown
# Задачи по итогам встречи: {TOPIC}

| № | Задача | Владелец | Срок | Приоритет | Статус | Примечание |
|---|--------|----------|------|-----------|--------|------------|
| 1 | ... | ... | ... | 🔴/🟠/🟡/🟢 | ⬜ | ... |
```

Owners and deadlines: if unclear, mark as hypothesis and ask.
Show draft. **STOP — wait for approval/edits.**

## Step 7 — Import plan

Show:
- Target folder: `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/`
- Files: `transcript.md`, `summary.md`, `tasks.md`
- Source file disposition: keep in Inbox / move to meeting folder / move to source materials

**STOP — wait for confirmation.**

## Step 8 — Execute

- Create meeting folder
- **Move** (via `mv`) the generated `.md` transcript from Инбокс to the meeting folder as `transcript.md` — do NOT recreate it with Write tool
- Write `summary.md` and `tasks.md`
- Handle source audio/video file per user decision
- Cleanup Инбокс: offer to delete the original audio/video file after successful import

## Step 9 — Auto-task-create (optional)

After successful import, if `tasks.md` contains action items:
1. List extracted action items with owners and deadlines
2. Ask user: "Создать task.md для этих action items?" with options:
   - **All** — create task cards for all items
   - **Select** — let user pick which ones
   - **Skip** — no task cards needed
3. For each selected item, invoke `.ai/skills/task-create.md` in streamlined mode:
   - Pre-fill project (same as meeting's project), priority, title from the action item
   - Add `## Контекст` referencing the meeting: `Встреча {N}. {DD.MM.YYYY} - {TITLE}`
   - Show batch plan (all tasks at once) → single confirmation → create all

**STOP — wait for user decision.**

# Output format

- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/transcript.md`
- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/summary.md`
- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/tasks.md`

# Quality bar

- [ ] File selection confirmed before processing
- [ ] Project, date, topic confirmed by user
- [ ] Summary and tasks drafts shown and approved before writing
- [ ] Hypothetical owners/deadlines marked as such
- [ ] Import plan confirmed before file creation

# Anti-patterns

- Creating meeting folders without user confirmation
- Writing summary/tasks without showing drafts
- Guessing owners and deadlines without marking as hypothesis
- Processing wrong file without asking

# Related knowledge

- `pmbok7-principles.md` — Stakeholders domain for identifying meeting participants' roles and interests
- `agile-frameworks.md` — Scrum ceremonies (Sprint Review, Retrospective) for meeting context
- `glossary.md` — term disambiguation when processing domain-specific meeting content
