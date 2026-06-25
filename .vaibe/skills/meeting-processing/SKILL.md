---
name: meeting-processing
description: Transcribe, analyze, and import meeting recordings into project structure. Triggers: meeting, recording, transcribe, audio, video, meeting-processing.
license: MIT
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
- `.vaibe/skills/meeting-processing/scripts/meeting_transcriber/` — transcription tool (if audio/video)

# Procedure

## Step 1 — Identify input file

- If path provided → use it (verify existence and format)
- If no path → scan `Инбокс/` for `.mp4`, `.webm`, `.mp3`, `.wav`, `.ogg`, `.m4a`, `.md`
- If multiple found → show list, ask which to process

**Batch mode (multiple files):** Transcribe all files in background first (per file: **local first**, then AssemblyAI on failure — see Step 2), then process each one step-by-step with confirmation. Do not ask for project/topic until transcription is done.

**STOP — wait for file selection.**

## Step 2 — Transcribe (if audio/video)

**Backend order (mandatory for agents):**

1. **First** run with **local** (CLI default: omit `--backend` or pass `--backend local`). Needs GPU, `HUGGINGFACE_TOKEN`, ffmpeg — see `.vaibe/skills/meeting-processing/scripts/meeting_transcriber/README.md`.
2. **Only if local fails** (non-zero exit, missing CUDA/deps, model errors, etc.) — **retry once** with `--backend assemblyai` (needs `ASSEMBLYAI_API_KEY`). Do not start with AssemblyAI when local is available and expected to work.

```bash
P=.vaibe/skills/meeting-processing/scripts/meeting_transcriber
# local backend (Whisper + pyannote) — needs the 'local' extra:
uv run --project $P --extra local $P/main.py <file> --lang ru
# on failure, retry once via the cloud backend:
uv run --project $P $P/main.py <file> --lang ru --backend assemblyai
```

If the user **explicitly** requests a single backend, follow that instruction.

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
| **Duplicate** | Topic/date/participants match an existing meeting in `Встречи/` | Show the match → ask: skip / update existing |
| **Accidental recording** | Transcript < ~30 turns, clearly cut off or carries no meaningful content | Report the brevity → offer to skip |
| **External webinar** | Public event, third-party speaker, content not tied to the project | Show a summary → offer: save to `База знаний/` / `Проекты/{PROJECT}/База знаний/` / skip |
| **Single voice briefing** | One speaker, long monologue, no participant interaction, semantically a personal note / brief / legal case description | Report that this is not a classic meeting → offer: save to `Исходные материалы/`, to `База знаний/`, link to an existing task, or still import it as a meeting |

On detecting an edge case — **STOP**, show the conclusion, wait for the user's decision.

## Step 4 — Ask user for context

Present hypotheses and ask:
- Which **project**? (must exist in `Проекты/`; if not → offer to create)
- **Date** (DD.MM.YYYY)?
- **Topic** (brief Russian name)?
- **Meeting number** N? (suggest next available)

**STOP — wait for response.**

**After receiving the topic, sanitize it for use as a folder name (Windows compatibility):**
The folder `Встреча {N}. {DD.MM.YYYY} - {TITLE}` must be safe on all platforms. Before constructing the path, replace any Windows-forbidden characters in `{TITLE}`:
- `:` → `-` or `—` (most common issue — e.g. «Синк: планирование» → «Синк — планирование»)
- `<`, `>`, `"`, `\`, `|`, `?`, `*` → remove or replace with `-`
- `/` → `-` or `—` (slash creates nested directories on all OS)

Apply this silently — do not mention the replacement unless the topic was significantly changed.

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
3. For each selected item, invoke `.vaibe/skills/task-create/SKILL.md` in streamlined mode:
   - Pre-fill project (same as meeting's project), priority, title from the action item
   - Add `## Контекст` referencing the meeting: `Встреча {N}. {DD.MM.YYYY} - {TITLE}`
   - Show batch plan (all tasks at once) → single confirmation → create all

**STOP — wait for user decision.**

# Имя папки встречи (кросс-платформа)

В `{TITLE}` **не использовать** символы, запрещённые в именах файлов Windows: `\ / : * ? " < > |`. Слеш `/` создаёт вложенные каталоги на всех ОС. Вместо «А/Б» — «А-Б» или «А — Б»; вместо двоеточия в теме — тире или длинное тире «—».

# Output format

- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/transcript.md`
- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/summary.md`
- `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/tasks.md`

# Quality bar

- [ ] File selection confirmed before processing
- [ ] Transcription: **local first**, AssemblyAI only after local failure (unless user overrides)
- [ ] Project, date, topic confirmed by user
- [ ] Folder name does not contain Windows-forbidden characters (`: < > " \ | ? *` replaced before use)
- [ ] Summary and tasks drafts shown and approved before writing
- [ ] Hypothetical owners/deadlines marked as such
- [ ] Import plan confirmed before file creation

# Anti-patterns

- Creating meeting folders without user confirmation
- Writing summary/tasks without showing drafts
- Guessing owners and deadlines without marking as hypothesis
- Processing wrong file without asking
- **Choosing AssemblyAI before attempting local** without user request (violates local-first policy)

# Related knowledge

- `.vaibe/skills/pmbok7-principles/SKILL.md` — Stakeholders domain for identifying meeting participants' roles and interests
- `.vaibe/skills/agile-frameworks/SKILL.md` — Scrum ceremonies (Sprint Review, Retrospective) for meeting context
- `.vaibe/skills/glossary/SKILL.md` — term disambiguation when processing domain-specific meeting content
- `.vaibe/skills/meeting-processing/references/assemblyai-transcription-workarounds.md` — диагностика сбоев транскрибации (HUGGINGFACE_TOKEN, SOCKS/proxy, дрейф payload AssemblyAI)
