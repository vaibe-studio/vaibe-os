# Публикация задач в YouTrack

## Обзор
Команда `/yt-project-tasks-push` публикует задачи из vAIbe-os в YouTrack. Это **основной поток синхронизации**: vAIbe-os → YouTrack. Создаёт новые issues для непривязанных задач и обновляет существующие.

**ВАЖНО**: 
- Проект должен быть предварительно связан через `/yt-project-link`
- Задачи берутся из **последнего плана** в папке `Проекты/{NAME}/Планы/`

## Канон данных (важно)
- **Карточки задач** в `Проекты/{PROJECT}/Задачи/*/task.md` — детальный канон.
- **План** — управленческий snapshot и точка интеграций.

Следствие: перед публикацией в YouTrack план должен быть **актуальным**. Если вы создавали/меняли задачи после последнего плана — сначала выполните `/plan-update {PROJECT}`.

---

## Формат вызова
- `/yt-project-tasks-push`
- `/yt-project-tasks-push {PROJECT_NAME}`

## Входы (источники данных)
- `.env` (локально): `YOUTRACK_URL`, `YOUTRACK_TOKEN`
- `Проекты/{PROJECT}/README.md` — связь с YouTrack (секция YouTrack Integration)
- `Проекты/{PROJECT}/Планы/План - N - ...md` — последний snapshot-план (источник задач для публикации)

## Выходы (артефакты)
- Изменения в YouTrack: создание/обновление issues (по подтверждению)
- Обновление последнего плана: добавление Issue ID/URL + sync-метаданные (по подтверждению)

---

## КРИТИЧЕСКИЕ ПРАВИЛА

> **ЗАПРЕЩЕНО**: Публиковать задачи в несвязанный проект.
> **ЗАПРЕЩЕНО**: Перезаписывать данные в YouTrack без предупреждения о конфликте.
> **ЗАПРЕЩЕНО**: Изменять файлы без показа изменений.
> **ОБЯЗАТЕЛЬНО**: Использовать **AskQuestion** для всех точек останова и сбора информации.
> **ОБЯЗАТЕЛЬНО**: Показать сводку изменений перед публикацией.
> **ОБЯЗАТЕЛЬНО**: Обрабатывать конфликты интерактивно.
> **ОБЯЗАТЕЛЬНО**: Обновлять sync-метаданные в плане после успешной публикации.

---

## Источник задач

### Структура плана

Задачи извлекаются из **последнего файла** в папке `Проекты/{NAME}/Планы/`:

```markdown
# Чек-лист задач команды {PROJECT}

## I. Критические задачи на текущий спринт
| № | Задача | Статус | Приоритет | ... |
| 1.1 | Название задачи | ⬜ | 🔴 | ... |

## II. Выполненные задачи
| № | Задача | Статус | Результаты |
| 2.1 | Название | ✅ | ссылка на результаты |

## III. Срочные задачи (эта неделя)
...

## IV. Среднесрочные задачи (1-2 недели)
...

## V. Долгосрочные задачи (1 месяц+)
...
```

### Маппинг статусов из плана

| Символ плана | Значение | YouTrack |
|--------------|----------|----------|
| ⬜ | Не начата | Open |
| 🔄 | В процессе | In Progress |
| ✅ | Выполнена | Fixed |
| ⏸️ | На холде | To be discussed |

### Маппинг приоритетов из плана

| Символ плана | Значение | YouTrack |
|--------------|----------|----------|
| 🔴 | Критический | Critical |
| 🟠 | Высокий | Major |
| 🟡 | Средний | Normal |
| 🟢 | Низкий | Minor |

---

## Алгоритм

### 1. **Инициализация**
   - Пользователь вызывает `/yt-project-tasks-push`
   - Опционально указывает проект: `/yt-project-tasks-push {PROJECT_NAME}`

### 2. **Проверка конфигурации**
   
   Прочитать `.env` и `README.md` проекта:
   
   ```
   🔍 Проверка конфигурации...
   
   ✅ YOUTRACK_URL: https://yt.example.com
   ✅ YOUTRACK_TOKEN: настроен
   ✅ Проект связан: ENSO
   
   или
   
   ❌ Проект не связан с YouTrack
   Используйте /yt-project-link для связывания
   ```

### 3. **Выбор проекта (если не указан)**

> ⚠️ **ТОЧКА ОСТАНОВА**: Использовать **AskQuestion**.

   ```python
   AskQuestion(
     title="Выбор проекта для публикации",
     questions=[{
       id: "project",
       prompt: "Выберите проект для публикации в YouTrack",
       options: [
         {id: "enso", label: "ЭНСО → ENSO"},
         {id: "epk", label: "ЕПК ФРИИ → UCP"},
         ...
       ]
     }]
   )
   ```
   
   **→ СТОП. Ожидание ответа AskQuestion.**

### 4. **Поиск последнего плана**
   
   - Найти папку `Проекты/{NAME}/Планы/`
   - Выбрать **последний файл** по дате в имени или по дате модификации
   - Прочитать и распарсить план

### 4.1 **Проверка актуальности плана (рекомендовано)**
- Быстрая проверка: есть ли в `Проекты/{NAME}/Задачи/` новые карточки задач, которые не отражены в плане.
- Если да — показать предупреждение:
  - “План может быть неактуален, часть задач не попадёт в YouTrack.”
  - предложить:
    1) отменить push и сначала выполнить `/plan-update {PROJECT}`
    2) продолжить push “как есть” (только по явному подтверждению)

### 5. **Сканирование задач из плана**
   
   - Извлечь задачи из разделов I, II, III, IV, V
   - Для каждой задачи определить:
     - Есть ли Issue ID в колонке `Issue` → задача привязана
     - Нет Issue ID → новая задача
   - Определить статус и приоритет по символам

### 6. **Выбор задач для публикации**

> ⚠️ **ТОЧКА ОСТАНОВА**: Использовать **AskQuestion**.

   ```python
   AskQuestion(
     title="Выбор задач для публикации",
     questions=[{
       id: "what_to_publish",
       prompt: "Какие задачи из плана нужно опубликовать в YouTrack?",
       options: [
         {id: "new_only", label: "Только новые задачи (разделы I, III, IV, V — N задач)"},
         {id: "critical_urgent", label: "Только критические и срочные (разделы I, III — N задач)"},
         {id: "critical_only", label: "Только критические (раздел I — N задач)"},
         {id: "all_including_done", label: "Все задачи, включая выполненные"},
         {id: "cancel", label: "Отмена"}
       ]
     }]
   )
   ```
   
   **→ СТОП. Ожидание ответа AskQuestion.**

### 7. **Формирование плана публикации**

> ⚠️ **ТОЧКА ОСТАНОВА**: Показать план и использовать **AskQuestion**.

   Показать таблицу задач для публикации:
   
   ```markdown
   📊 **План публикации в YouTrack**
   
   📁 **Проект**: ЭНСО → ENSO
   📄 **Источник**: Планы/План - 1 - 27.01.2026 - ...
   
   ### 🆕 Новые задачи (будут созданы): N
   
   | № | Название | Статус | Приоритет |
   |---|----------|--------|-----------|
   | 1.1 | Ревью опросника | ⬜ → Open | 🔴 → Critical |
   ...
   
   ### ✅ Уже опубликованы: N
   ENSO-1 — ENSO-10 (пропускаются)
   ```
   
   ```python
   AskQuestion(
     title="Подтверждение публикации",
     questions=[{
       id: "confirm",
       prompt: "Создать N новых задач в YouTrack?",
       options: [
         {id: "yes", label: "Да, создать все N задач"},
         {id: "critical_only", label: "Только критические (N задач)"},
         {id: "no", label: "Отмена"}
       ]
     }]
   )
   ```
   
   **→ СТОП. Ожидание подтверждения.**

### 8. **Выполнение публикации**
   
   **ТОЛЬКО ПОСЛЕ подтверждения через AskQuestion:**
   
   #### 8.1 Создание новых issues
   ```bash
   curl -X POST "${YOUTRACK_URL}/api/issues?fields=id,idReadable,summary" \
     -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "project": {"id": "{PROJECT_ID}"},
       "summary": "{Название задачи}",
       "description": "{Описание}"
     }'
   ```
   
   #### 8.2 Обновление статусов и приоритетов
   ```bash
   curl -X POST "${YOUTRACK_URL}/api/issues/{issueId}" \
     -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "customFields": [
         {"name": "State", "$type": "StateIssueCustomField", "value": {"name": "Open"}},
         {"name": "Priority", "$type": "SingleEnumIssueCustomField", "value": {"name": "Critical"}},
         {"name": "Type", "$type": "SingleEnumIssueCustomField", "value": {"name": "Task"}}
       ]
     }'
   ```

### 9. **Обновление плана с Issue ID**
   
   После успешной публикации обновить таблицы в плане:
   - Добавить колонку `Issue` с ссылками на YouTrack
   - Добавить секцию `## YouTrack Sync` в начало файла
   
   ```markdown
   ## YouTrack Sync
   - **Project**: ENSO
   - **Issues**: ENSO-1 — ENSO-28
   - **Last Sync**: 2026-01-27T16:00:00Z
   - **Sync Direction**: push
   ```
   
   Обновить таблицы задач:
   ```markdown
   | № | Задача | Issue | Статус | ... |
   | 1.1 | Ревью опросника | [ENSO-11](url) | ⬜ | ... |
   ```

### 10. **Отчёт о результатах**
   
   ```markdown
   ## ✅ Публикация завершена
   
   ### 📊 Результаты
   | Операция | Количество |
   |----------|------------|
   | Создано | N задач |
   | Ранее опубликовано | M задач |
   | Всего в YouTrack | N+M задач |
   
   ### 🔗 Созданные issues
   | Issue | Название |
   |-------|----------|
   | [ENSO-11](url) | Ревью опросника |
   ...
   
   **Kanban Board:** https://yt.example.com/agiles/{BOARD_ID}
   ```

---

## Примечания по Kanban доске

- Задачи **автоматически добавляются** на Kanban доску, если она связана с проектом
- Не требуется отдельный вызов API для добавления на доску
- Проверить наличие задач на доске:
  ```bash
  curl -X GET "${YOUTRACK_URL}/api/agiles/{BOARD_ID}/sprints?fields=id,name,issues(id,idReadable)"
  ```

---

## Маппинг данных

### Статусы (vAIbe-os → YouTrack)

| vAIbe-os | YouTrack |
|-------|----------|
| ⬜ / открыта | Open |
| 🔄 / в процессе | In Progress |
| ⏸️ / требует уточнения | To be discussed |
| на ревью | Submitted |
| ✅ / выполнена | Fixed |
| отменена | Won't fix |

**Важно**: Статус "Done" отсутствует в стандартной конфигурации YouTrack. Используйте "Fixed" для выполненных задач.

### Приоритеты (vAIbe-os → YouTrack)

| vAIbe-os | YouTrack |
|-------|----------|
| 🔴 / критический | Critical |
| 🟠 / высокий | Major |
| 🟡 / средний | Normal |
| 🟢 / низкий | Minor |

### Типы (всегда устанавливать)

Всегда устанавливать `Type = Task` при создании issue:
```json
{"name": "Type", "$type": "SingleEnumIssueCustomField", "value": {"name": "Task"}}
```

---

## Формат sync-метаданных в плане

```markdown
## YouTrack Sync
- **Project**: {PROJECT_SHORT_NAME}
- **Issues**: {FIRST_ISSUE} — {LAST_ISSUE}
- **Last Sync**: {ISO8601 timestamp}
- **Sync Direction**: push
```

---

## Примеры

### Пример 1: Публикация задач из плана
**Запрос**: `/yt-project-tasks-push ЭНСО`

```
1. ✅ Проект связан с ENSO

2. 📄 Найден план: План - 1 - 27.01.2026 - MVP готов...

3. AskQuestion: Какие задачи опубликовать?
   → Пользователь: "Все задачи"

4. 📊 План публикации:
   - Новые: 18 задач
   - Уже опубликовано: 10 задач
   
   AskQuestion: Подтвердить создание 18 задач?
   → Пользователь: "Да"

5. ✅ Публикация завершена
   - Создано: ENSO-11 — ENSO-28
   - План обновлён с Issue ID
```

### Пример 2: Публикация только критических задач
**Запрос**: `/yt-project-tasks-push ЭНСО`

```
1. AskQuestion: Какие задачи опубликовать?
   → Пользователь: "Только критические (4 задачи)"

2. 📊 План публикации:
   - 1.1 Ревью опросника → Critical
   - 1.2 Отправка опросника → Critical
   - 1.3 Формирование КП → Critical
   - 1.4 Демо-презентация → Critical
   
   AskQuestion: Подтвердить?
   → Пользователь: "Да"

3. ✅ Создано: ENSO-11 — ENSO-14
```

---

## Обработка ошибок

### Проект не связан
```
❌ Проект не связан с YouTrack

Проект "ЭНСО" не имеет секции "YouTrack Integration" в README.md.

Действие:
/yt-project-link ЭНСО
```

### План не найден
```
❌ План не найден

Папка Проекты/ЭНСО/Планы/ пуста или не существует.

Действие:
1. Создайте первый snapshot-план через `/plan-update {PROJECT}`
2. Затем повторите `/yt-project-tasks-push {PROJECT}`
```

### Неверный статус в YouTrack
```
❌ Ошибка: Статус "Done" не найден

Причина: В проекте ENSO нет статуса "Done"

Действие: Использовать статус "Fixed" для выполненных задач
```

---

## API запросы

### Получение Project ID
```bash
curl -X GET "${YOUTRACK_URL}/api/admin/projects?fields=id,shortName,name" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" | jq '.[] | select(.shortName == "ENSO")'
```

### Создание issue
```bash
curl -X POST "${YOUTRACK_URL}/api/issues?fields=id,idReadable,summary" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "project": {"id": "0-6"},
    "summary": "Название задачи",
    "description": "Описание задачи"
  }'
```

### Обновление статуса и приоритета
```bash
curl -X POST "${YOUTRACK_URL}/api/issues/ENSO-11" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "customFields": [
      {"name": "State", "$type": "StateIssueCustomField", "value": {"name": "Open"}},
      {"name": "Priority", "$type": "SingleEnumIssueCustomField", "value": {"name": "Critical"}},
      {"name": "Type", "$type": "SingleEnumIssueCustomField", "value": {"name": "Task"}}
    ]
  }'
```

### Проверка доступных статусов
```bash
curl -X GET "${YOUTRACK_URL}/api/admin/projects/{PROJECT_ID}/customFields?fields=field(name),bundle(values(name))" \
  -H "Authorization: Bearer ${YOUTRACK_TOKEN}"
```

---

## Связанные команды
- `/yt-project-link` — связать проект перед push
- `/plan-update` — актуализировать snapshot-план перед публикацией
- `/yt-project-tasks-pull` — после работы команды/коллег получить изменения обратно в vAIbe-os

---

## Примечания

- Push не удаляет issues в YouTrack — только создаёт и обновляет
- Источник задач — **план** в папке `Планы/`, не папка `Задачи/`
- Если план неактуален, push может пропустить новые задачи — рекомендуется сначала `/plan-update`
- Все точки останова используют **AskQuestion** для интерактивности
- Задачи автоматически попадают на Kanban доску проекта
- Всегда устанавливать `Type = Task` при создании issue
- Проверить доступные статусы перед публикацией (статус "Done" может отсутствовать)
