# Cursor: доступность инструментов и известные проблемы

> Справочник для понимания, какие инструменты доступны в Cursor и известные edge-cases.
> Влияет на рекомендации по эксплуатации vAIbe-OS.

## Стандартные инструменты агента (Agent mode)

Согласно [официальной документации Cursor](https://cursor.com/docs/agent/tools), агент в Agent mode имеет доступ к следующим инструментам:

| Инструмент | Описание |
|---|---|
| Read files | Чтение файлов (включая изображения) |
| Edit files | Редактирование файлов (apply) |
| Search files and folders | Поиск по имени, Grep, Glob |
| Semantic search | Семантический поиск по индексированной кодовой базе |
| Run shell commands | Выполнение терминальных команд |
| Web search | Поиск в интернете |
| Browser | Управление браузером для тестирования |
| Image generation | Генерация изображений из текста |
| **Ask questions** | **Структурированные вопросы пользователю** |

**AskQuestion — реальный инструмент Cursor**, задокументированный в официальных docs. Он позволяет агенту задавать уточняющие вопросы во время выполнения задачи.

## Известная проблема: `Tool not found` в определённых контекстах

28.02.2026 наблюдался случай: AskQuestion вернул `Tool not found` при вызове внутри Cursor Command (`/task-create`), хотя в той же сессии в другом контексте инструмент был доступен.

**Гипотезы причины:**
- Вызов через Cursor Command (slash-command) может менять набор доступных инструментов
- Переключение режимов (Agent → Ask → Agent) может влиять на доступность
- Transient bug в Cursor

**Вывод:** проблема не связана с конкретной моделью. AskQuestion — стандартный инструмент Agent mode. Если он недоступен — это edge-case, а не норма.

## Режимы Cursor и доступность инструментов

| Режим | Инструменты | Примечание |
|---|---|---|
| Agent | Все (включая AskQuestion) | Основной режим работы |
| Ask | Только readonly (поиск, чтение) | Без записи и модификации |
| Plan | Все | Для планирования перед реализацией |
| Debug | Все + debug server | Для отладки |

## Рекомендации для авторов skills

1. **AskQuestion — стандартный инструмент.** Используйте его по умолчанию для структурированных вопросов.
2. **Graceful degradation** — если `Tool not found`, fallback на текстовые вопросы (см. `.ai/rules/interactive-patterns.md`).
3. В `.ai/skills/` (IDE-independent) упоминать инструменты через условную конструкцию:

```
In Cursor: call the AskQuestion tool for structured choices.
In other IDEs: use the available structured input mechanism, or fall back to plain text with numbered options.
```
