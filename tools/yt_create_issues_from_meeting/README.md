# YouTrack Issues Creator from Meeting Tasks

Скрипт для автоматического создания задач в YouTrack из файла `meeting_tasks.md` встречи.

## Установка

```bash
cd tools/yt_create_issues_from_meeting
pip install -r requirements.txt
```

## Конфигурация

Создайте файл `.env` в корне проекта:

```env
YOUTRACK_URL=https://yt.power-freelance.ru
YOUTRACK_TOKEN=perm:your-token-here
YOUTRACK_PROJECT_ID=UCP
```

### Получение токена YouTrack

1. Откройте YouTrack → Profile → Account Security
2. Нажмите "New token..."
3. Укажите имя токена и scope (YouTrack)
4. Скопируйте токен и сохраните в `.env`

## Использование

### Через Python модуль

```bash
# Из корня проекта
python -m tools.yt_create_issues_from_meeting 3

# Dry run (только показать задачи)
python -m tools.yt_create_issues_from_meeting 3 --dry-run

# С указанием проекта
python -m tools.yt_create_issues_from_meeting 3 --project UCP
```

### Через Cursor команду

```
/yt-create-issues-from-meeting 3
```

## Формат meeting_tasks.md

Скрипт парсит задачи в формате:

```markdown
### N. Название задачи
- **Описание**: текст описания
- **Приоритет**: Высший/Высокий/Средний/Низкий
- **Срок**: дедлайн
- **Ответственный**: имя
```

## Маппинг приоритетов

| meeting_tasks.md | YouTrack Priority |
|------------------|-------------------|
| Высший           | Critical          |
| Высокий          | Major             |
| Средний          | Normal            |
| Низкий           | Minor             |

## Пример вывода

```
2026-01-25 12:00:00 - INFO - Parsed 13 tasks from meeting_tasks.md
2026-01-25 12:00:01 - INFO - Authenticated as: Admin
2026-01-25 12:00:01 - INFO - Creating issues in project: UCP (ID: 0-1)
2026-01-25 12:00:02 - INFO - Created issue: UCP-1 - Цель спринта: 5 интервью с респондентами
2026-01-25 12:00:02 - INFO - Created issue: UCP-2 - Перетрясти телефонные книжки
...

============================================================
РЕЗУЛЬТАТЫ СОЗДАНИЯ ЗАДАЧ В YOUTRACK
============================================================

Всего задач: 13
Создано: 13
Ошибок: 0

✓ Созданные задачи:
  - UCP-1: Цель спринта: 5 интервью с респондентами
    URL: https://yt.power-freelance.ru/issue/UCP-1
  ...
```

## Обработка ошибок

- Проверка наличия `meeting_tasks.md` перед парсингом
- Валидация токена через `/api/users/me`
- Детальный отчет об успешных/неуспешных задачах
- Retry при сетевых ошибках (TODO)
