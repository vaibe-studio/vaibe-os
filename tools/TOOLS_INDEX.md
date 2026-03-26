# Tools index (vAIbe-os)

Короткий каталог утилит в `tools/` — чтобы не "изобретать заново" скрипты при похожих задачах.

## Общие правила использования

- **Предпочитай модульный запуск**: `python -m tools.<tool> ...` (если у инструмента есть `__main__.py`)
- **Зависимости**: смотри `tools/<tool>/requirements.txt` и ставь точечно:
  - `python -m pip install -r tools/<tool>/requirements.txt`

## Единая точка входа (рекомендуется)

Можно вызывать инструменты через один CLI:

```bash
python -m tools --help
python -m tools <команда> --help
```

---

## Markdown → PDF

- **Путь**: `tools/markdown_to_pdf/`
- **Назначение**: конвертация Markdown в PDF **без внешних движков** (pandoc/LaTeX/wkhtmltopdf не требуются), с нормальной поддержкой кириллицы через системные Windows-шрифты.
- **Команда**:

```bash
python -m tools.markdown_to_pdf input.md -o output.pdf
```

Через единый CLI:

```bash
python -m tools markdown-to-pdf input.md -o output.pdf
```

---

## PDF → Markdown

- **Путь**: `tools/pdf_to_markdown/`
- **Назначение**: извлечение текста из PDF в Markdown (встроенный текст + опциональный OCR fallback).
- **Команды**:

```bash
python -m tools.pdf_to_markdown input.pdf -o output.md
python -m tools.pdf_to_markdown input.pdf -o output.md --ocr
python -m tools.pdf_to_markdown input.pdf -o output.md --pages 1-5
```

Через единый CLI:

```bash
python -m tools pdf-to-markdown input.pdf -o output.md
```

---

## YouTrack: выгрузка AS IS контекста задач

- **Путь**: `tools/yt_context_pull/`
- **Назначение**: загрузка текущего состояния задач из YouTrack (статусы, исполнители, комментарии) с формированием план-подобного отчёта и сравнением с предыдущей выгрузкой.
- **Команды**:

```bash
python -m tools.yt_context_pull
python -m tools.yt_context_pull --project PROJECT
python -m tools.yt_context_pull --profile MY_PROJECT
python -m tools.yt_context_pull --profile MY_PROJECT --dry-run
python -m tools.yt_context_pull --output-dir "Проекты/МойПроект/YouTrack"
```

Через единый CLI:

```bash
python -m tools yt-context-pull
python -m tools yt-context-pull --project PROJECT --dry-run
```

---

## Meeting Transcriber: транскрибация встреч с диаризацией спикеров

- **Путь**: `tools/meeting_transcriber/`
- **Назначение**: транскрибировать аудио/видео встреч с разметкой спикеров. Бэкенды: **AssemblyAI** (API) или **local** (Whisper + pyannote.audio).
- **Команды**:

```bash
python -m tools.meeting_transcriber meeting.mp4
python -m tools.meeting_transcriber meeting.mp4 --backend local --lang ru
python -m tools.meeting_transcriber meeting.mp4 -o путь/transcript.md
```

Через единый CLI:

```bash
python -m tools meeting-transcriber meeting.mp4 --backend assemblyai
```

Используется командой `/meeting-processing`. См. `tools/meeting_transcriber/README.md`.

---

## Vault Lint: проверка инвариантов (GUARDS.md)

- **Путь**: `tools/vault_lint/`
- **Назначение**: автоматическая проверка инвариантов vAIbe-OS, определённых в `.ai/GUARDS.md` (G1–G7): проекты с README.md и Видимостью, задачи с секцией Статус, русский язык файлов, нумерация, версионирование results/, frontmatter skills, broken links.
- **Команды**:

```bash
python -m tools.vault_lint
python -m tools.vault_lint --guard G1 G2
python -m tools.vault_lint --json
```

Через единый CLI:

```bash
python -m tools vault-lint
python -m tools vault-lint --guard G1 G4
```

---

## Vault Index: сводка состояния vault

- **Путь**: `tools/vault_index/`
- **Назначение**: автоматическая генерация `.ai/VAULT-INDEX.md` — сводка проектов, задач, skills, bots, rules, knowledge.
- **Команды**:

```bash
python -m tools.vault_index
```

Через единый CLI:

```bash
python -m tools vault-index
```

---

## Обработка "отложенного" источника в базу знаний

- **Путь**: `tools/process_deferred_kb_source.py`
- **Назначение**: пример "конвейера" обработки файла из `Инбокс/Отложено/` → чистый исходник + конспект в `База знаний/`, затем удаление исходника из очереди.
- **Команда**:

```bash
python tools/process_deferred_kb_source.py
```

Через единый CLI:

```bash
python -m tools process-deferred-kb-source
```
