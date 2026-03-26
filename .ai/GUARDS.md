# Инварианты vAIbe-OS (Guards)

> Формализованные правила целостности системы. Каждый инвариант — machine-checkable assertion.
> Используется `tools/vault-lint/` для автоматической проверки.

**Онтологическое основание**: Закон 5 (Аддитивность) — система развивается без деградации. Guards — формализация границ, внутри которых эволюция безопасна.

---

## G1: Проекты — README.md + Видимость

**Правило**: каждая директория `Проекты/{NAME}/` содержит `README.md` с полем `Видимость: командный | личный`.

**Assertion**:
```
FOR EACH dir IN Проекты/**/
  IF dir CONTAINS README.md   # skip intermediate folders like Личное/
    ASSERT EXISTS dir/README.md
    ASSERT dir/README.md CONTAINS "Видимость:"
    ASSERT value IN ["командный", "личный"]
```

**Следствие**: личный проект (`Видимость: личный`) — в `.gitignore`. Командный — трекается в Git.

**Закон**: Экстернализация — структура проектов является формой существования рабочего мышления вовне.

---

## G2: Задачи — task.md + секция «Статус»

**Правило**: каждая директория `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/` содержит `task.md` с секцией `## Статус` в конце файла.

**Assertion**:
```
FOR EACH dir IN Проекты/**/Задачи/*/
  ASSERT EXISTS dir/task.md
  ASSERT dir/task.md CONTAINS section "## Статус"
  ASSERT section "## Статус" IS last H2 section in file
  ASSERT section CONTAINS "**Статус**:" WITH value IN ["открыта", "в процессе", "выполнена", "на холде"]
```

**Формат секции**:
```markdown
## Статус
- **Статус**: открыта | в процессе | выполнена | на холде
- **Завершена**: YYYY-MM-DD          ← только для выполненных
- **Версия результата**: v{N}        ← только для выполненных с файлами в results/
```

**Закон**: Обратная связь — статус задачи позволяет системе отслеживать прогресс и предлагать действия.

---

## G3: Русский язык для файлов и папок

**Правило**: все файлы и папки пользовательского контента именуются на русском языке.

**Assertion**:
```
FOR EACH path IN vault root (recursive)
  IF path NOT IN excluded_prefixes
    ASSERT basename(path) MATCHES Cyrillic pattern OR is system name (README.md, task.md, etc.)
```

**Исключения** (латиница допустима):
- `.ai/`, `.cursor/`, `.claude/` — системные конфигурации
- `tools/` — Python-утилиты
- `repositories/` — git submodules
- `results/v{N}/` — файлы внутри версий результатов (код, HTML допустимы)
- Системные файлы: `README.md`, `task.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`

**Закон**: Экстернализация — русский язык зафиксирован как язык мышления пользователя. Структура отражает реальное мышление, не абстрактную «интернационализацию».

---

## G4: Нумерация задач — уникальность и формат

**Правило**: номера задач внутри проекта уникальны и используют формат с ведущими нулями.

**Assertion**:
```
FOR EACH project IN Проекты/**/
  IF project CONTAINS Задачи/   # only actual projects, not grouping folders
    LET task_dirs = project/Задачи/*/
  LET numbers = EXTRACT {NUM} FROM each dir name matching pattern "{NUM}-{TITLE}"
  ASSERT ALL numbers MATCH /^\d{3,}$/  (minimum 3 digits with leading zeros)
  ASSERT ALL numbers ARE UNIQUE within project
```

**Закон**: Аддитивность — нумерация обеспечивает упорядоченность и предотвращает конфликты при добавлении новых задач.

---

## G5: Версионирование результатов

**Правило**: результаты задач хранятся в `results/v{N}/`. Каждое выполнение — новая версия. Предыдущие версии не затираются.

**Assertion**:
```
FOR EACH task_dir IN Проекты/**/Задачи/*/
  IF EXISTS task_dir/results/
    FOR EACH subdir IN task_dir/results/*/
      ASSERT subdir.name MATCHES /^v\d+$/
    LET versions = EXTRACT N FROM each v{N}
    ASSERT versions ARE sequential (no gaps allowed only if starting from v1)
    ASSERT NO files directly in results/ (except legacy — warn, don't fail)
```

**Закон**: Аддитивность — версионирование гарантирует, что эволюция результатов не уничтожает предыдущие итерации.

---

## G6: Skills — YAML frontmatter

**Правило**: каждый skill в `.ai/skills/` содержит YAML frontmatter с обязательными полями.

**Assertion**:
```
FOR EACH file IN .ai/skills/*.md
  ASSERT file STARTS WITH "---"
  ASSERT frontmatter CONTAINS field "name" (non-empty string)
  ASSERT frontmatter CONTAINS field "description" (non-empty string)
  ASSERT frontmatter CONTAINS field "triggers" (non-empty array)
```

**Обязательные поля frontmatter**:
- `name` — идентификатор skill (латиница, kebab-case)
- `description` — описание назначения
- `triggers` — массив ключевых слов для маршрутизации

**Закон**: Направленная эволюция — frontmatter позволяет router.md автоматически классифицировать задачи и подбирать навыки.

---

## G7: Защита знаний

**Правило**: файлы базы знаний (`База знаний/`, `.ai/knowledge/`, `Проекты/**/База знаний/`) не удаляются без замены или явного плана миграции.

**Assertion**:
```
BEFORE DELETE any file IN knowledge_paths:
  ASSERT EXISTS migration_plan OR replacement_file
  ASSERT user_confirmation == true

knowledge_paths:
  - База знаний/**
  - .ai/knowledge/**
  - Проекты/**/База знаний/**
  - .ai/skills/**  (skills contain accumulated expertise)
  - .ai/ONTOLOGY.md
  - .ai/MANIFESTO.md (when created)
```

**Закон**: Аддитивность — знания накапливаются, не стираются. Потери допустимы только осознанно, с сохранением контекста.

---

## G8: Свежесть knowledge-файлов

**Правило**: каждый файл в `.ai/knowledge/` содержит секцию `## Sources` с датированными или верифицируемыми ссылками. Файлы, чьи ключевые источники старше 18 месяцев, помечаются для ревью при `weekly-review`.

**Assertion**:
```
FOR EACH file IN .ai/knowledge/*.md
  IF file.name NOT IN ["glossary.md", "knowledge-curation-guide.md"]
    ASSERT file CONTAINS section "## Sources"
    ASSERT section "## Sources" HAS at least 1 entry

DURING weekly-review:
  FOR EACH file IN .ai/knowledge/*.md
    IF file.last_modified > 18 months ago
      WARN "Knowledge file may need freshness review: {file}"
```

**Действие при срабатывании**: агент при `weekly-review` включает список устаревших knowledge-файлов в отчёт. Обновление — через `/evolve` с пометкой `freshness-update`.

**Закон**: Обратная связь — устаревшие знания снижают качество рекомендаций; регулярная проверка замыкает петлю обратной связи.

---

## G9: Синхронизация glossary.md

**Правило**: при создании или существенном обновлении knowledge-файла проверять, что ключевые термины отражены в `glossary.md`.

**Assertion**:
```
AFTER CREATE OR MAJOR_UPDATE of file IN .ai/knowledge/*.md
  LET new_terms = EXTRACT key terms FROM file (terms appearing in headings or defined inline)
  FOR EACH term IN new_terms
    IF term NOT IN .ai/knowledge/glossary.md
      WARN "Term '{term}' missing from glossary.md — consider adding"
```

**Действие при срабатывании**: агент предлагает пользователю добавить недостающие термины в `glossary.md`. Не блокирует, но фиксирует как задачу на `/evolve`.

**Закон**: Направленная эволюция — глоссарий как единый индекс терминов обеспечивает связность знаний и снижает когнитивную нагрузку.

---

## Использование

### Автоматическая проверка
```bash
.venv/bin/python -m tools.vault_lint
```

### Ручная проверка
При выполнении `/evolve`, `/task-create`, `/task-execute` — агент сверяется с Guards перед записью файлов.

### Приоритет при конфликте
```
ONTOLOGY.md (законы)
  └── GUARDS.md (инварианты — выводятся из законов)
        └── structure.md (правила — конкретизируют инварианты)
              └── skills (процедуры — реализуют правила)
```

Если Guard противоречит практике — обновить Guard через `/evolve`, не нарушать его молча.
