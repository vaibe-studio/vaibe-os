# Python и виртуальное окружение

## Вызов Python-скриптов

- Все вызовы Python (например `python -m tools.<tool> ...`, `python script.py`) выполняются **через интерпретатор из `.venv`** в корне репозитория.
- Использовать явный путь: `.venv/bin/python` (Linux/macOS) или `.venv\Scripts\python.exe` (Windows), либо перед командами выполнить `source .venv/bin/activate` (Linux/macOS) / `.venv\Scripts\activate` (Windows).
- В командах и инструкциях при упоминании `python` подразумевать вызов из venv; в примерах кода предпочтительно писать `.venv/bin/python -m ...` (или активацию venv перед командой).

## Если .venv отсутствует

- Перед первым запуском Python-инструмента проверить наличие `.venv` в корне репозитория.
- Если `.venv` нет — создать: `python3 -m venv .venv`, затем установить зависимости (например `.venv/bin/pip install -r tools/<tool>/requirements.txt` или общие зависимости проекта).
- После этого выполнять скрипты только из этого окружения.
