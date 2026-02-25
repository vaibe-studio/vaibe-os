# PDF to Markdown Converter

Универсальный скрипт для извлечения текста из PDF-файлов и конвертации в Markdown.

## Возможности

- Извлечение встроенного текста (pdfplumber + PyMuPDF)
- OCR для сканированных документов (pytesseract)
- Автоматический fallback на OCR если текст не извлекается
- Поддержка таблиц (конвертация в Markdown-таблицы)
- Выбор диапазона страниц
- Поддержка русского и английского языков

## Установка

### Базовые зависимости

```bash
pip install pdfplumber PyMuPDF
```

### С поддержкой OCR

```bash
pip install pdfplumber PyMuPDF pytesseract pdf2image Pillow
```

Также для OCR необходим Tesseract:

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-rus

# macOS
brew install tesseract tesseract-lang

# Windows - скачать с https://github.com/UB-Mannheim/tesseract/wiki
```

Для `pdf2image` также нужен `poppler`:

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows - скачать с https://github.com/oschwartz10612/poppler-windows/releases
```

## Использование

### Базовое использование

```bash
# Извлечь текст и сохранить в файл
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o document.md

# Вывести в stdout
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf
```

### С OCR (для сканов)

```bash
# OCR fallback (используется если обычное извлечение не работает)
python tools/pdf_to_markdown/pdf_to_markdown.py scan.pdf -o scan.md --ocr

# Принудительно использовать OCR
python tools/pdf_to_markdown/pdf_to_markdown.py scan.pdf -o scan.md --force-ocr

# Указать язык OCR
python tools/pdf_to_markdown/pdf_to_markdown.py scan.pdf -o scan.md --ocr --lang rus
```

### Выбор страниц

```bash
# Только первые 5 страниц
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o output.md --pages 1-5

# Конкретные страницы
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o output.md --pages 1,3,5,10

# Комбинация
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o output.md --pages 1-3,7,10-15
```

### Дополнительные опции

```bash
# Без маркеров страниц
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o output.md --no-page-markers

# Подробный вывод
python tools/pdf_to_markdown/pdf_to_markdown.py document.pdf -o output.md -v
```

## Параметры

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `input` | Путь к PDF-файлу | обязательный |
| `-o, --output` | Путь к выходному файлу | stdout |
| `--ocr` | Включить OCR fallback | false |
| `--force-ocr` | Использовать только OCR | false |
| `--lang` | Язык OCR | rus+eng |
| `--pages` | Диапазон страниц | все |
| `--no-page-markers` | Без маркеров страниц | false |
| `-v, --verbose` | Подробный вывод | false |

## Примеры вывода

### Текстовый документ

```markdown
<!-- Page 1 -->

# Заголовок документа

Содержимое первой страницы...

<!-- Page 2 -->

## Раздел 2

Содержимое второй страницы...
```

### Документ с таблицей

```markdown
<!-- Page 1 -->

| Колонка 1 | Колонка 2 | Колонка 3 |
| --------- | --------- | --------- |
| Значение  | Значение  | Значение  |
```

## Использование как модуль

```python
from tools.pdf_to_markdown.pdf_to_markdown import convert_pdf_to_markdown

# Базовое использование
markdown = convert_pdf_to_markdown('document.pdf')
print(markdown)

# С OCR и сохранением
markdown = convert_pdf_to_markdown(
    input_path='scan.pdf',
    output_path='output.md',
    use_ocr=True,
    ocr_lang='rus',
    pages='1-10'
)
```

## Алгоритм работы

1. **Попытка извлечь текст через pdfplumber** - хорошо работает с таблицами
2. **Если текст пустой/некачественный - PyMuPDF** - быстрое извлечение
3. **Если текст всё ещё плохой и OCR включен - pytesseract** - для сканов
4. **Постобработка** - очистка, форматирование в Markdown

## Troubleshooting

### "Missing dependencies"

Установите недостающие пакеты:

```bash
pip install pdfplumber PyMuPDF pytesseract pdf2image
```

### "tesseract is not installed"

Установите Tesseract OCR для вашей ОС (см. раздел Установка).

### "Unable to get page count"

Файл PDF может быть повреждён или защищён паролем.

### Пустой вывод

- Проверьте, что PDF содержит текст (не только изображения)
- Попробуйте `--ocr` или `--force-ocr` для сканов
