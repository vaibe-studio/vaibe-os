# Markdown to PDF

Минимальный конвертер Markdown → PDF без внешних движков (pandoc/LaTeX/wkhtmltopdf не нужны).

## Почему так

- В корпоративных/локальных окружениях часто **нет pandoc** или LaTeX.
- Для кириллицы нужен шрифт с поддержкой Unicode — скрипт по умолчанию использует системный шрифт Windows (`Arial`/`Segoe UI`/`Calibri`).

## Установка

```bash
python -m pip install -r tools/markdown_to_pdf/requirements.txt
```

## Использование

### Через файл скрипта

```bash
python tools/markdown_to_pdf/markdown_to_pdf.py input.md -o output.pdf
```

### Как модуль

```bash
python -m tools.markdown_to_pdf input.md -o output.pdf
```

## Поддерживаемая разметка (best-effort)

- Заголовки `#`…`####`
- Списки `- ...` и `1. ...`
- Блоки кода (ограждения ``` )
- Цитаты `> ...`
- Маркер разрыва страницы: `<!-- pagebreak -->`
- Ссылки `[текст](url)` → `текст (url)`

## Пример для манифеста

```bash
python -m tools.markdown_to_pdf .cursor/meta-mind/MANIFESTO_PDF.md -o .cursor/meta-mind/MANIFESTO.pdf
```

