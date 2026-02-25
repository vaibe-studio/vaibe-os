# Tools index (vAIbe-os)

Короткий каталог утилит в `tools/` — чтобы не “изобретать заново” скрипты при похожих задачах.

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

## YouTrack: создание задач из meeting_tasks.md

- **Путь**: `tools/yt_create_issues_from_meeting/`
- **Назначение**: создать задачи в YouTrack из `meeting_tasks.md` выбранной встречи.
- **Команды**:

```bash
python -m tools.yt_create_issues_from_meeting 3
python -m tools.yt_create_issues_from_meeting 3 --dry-run
python -m tools.yt_create_issues_from_meeting 3 --project UCP
```

Через единый CLI:

```bash
python -m tools yt-create-issues-from-meeting 3 --dry-run
```

---

## EPK outreach: выбрать лидов из CSV спикеров

- **Путь**: `tools/epk_outreach/select_leads.py`
- **Назначение**: подобрать сбалансированный список лидов для аутрича из CSV (с авто-детектом CSV в `Инбокс/`).
- **Команды**:

```bash
python tools/epk_outreach/select_leads.py --csv-auto --per-segment 15
python tools/epk_outreach/select_leads.py --csv "C:\path\to\file.csv" --per-segment 15
```

Через единый CLI:

```bash
python -m tools epk-select-leads --csv-auto --per-segment 15
```

---

## Cursor usage stats: статистика токенов за день

- **Путь**: `tools/cursor_stats/`
- **Назначение**: получить статистику использования Cursor за день.
- **Команды**:

```bash
python -m tools.cursor_stats
python -m tools.cursor_stats --date 2026-01-27
```

Через единый CLI:

```bash
python -m tools cursor-stats --date 2026-01-27
```

---

## Обработка “отложенного” источника в базу знаний

- **Путь**: `tools/process_deferred_kb_source.py`
- **Назначение**: пример “конвейера” обработки файла из `Инбокс/Отложено/` → чистый исходник + конспект в `База знаний/`, затем удаление исходника из очереди.
- **Команда**:

```bash
python tools/process_deferred_kb_source.py
```

Через единый CLI:

```bash
python -m tools process-deferred-kb-source
```

