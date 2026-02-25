# Связывание проекта с YouTrack

## Обзор
Команда `/yt-project-link` связывает локальный проект vAIbe-os с проектом в YouTrack. Поддерживает два режима: привязка к существующему проекту или создание нового проекта в YouTrack.

**ВАЖНО**: Перед использованием убедитесь, что в `.env` настроены `YOUTRACK_URL` и `YOUTRACK_TOKEN`.

---

## Формат вызова
- `/yt-project-link`
- `/yt-project-link {PROJECT_NAME}`

## Входы (источники данных)
- `.env` (локально): `YOUTRACK_URL`, `YOUTRACK_TOKEN`
- `Проекты/{PROJECT}/README.md` — текущее состояние связи (секция YouTrack Integration)

## Выходы (артефакты)
- Обновление `Проекты/{PROJECT}/README.md` (добавление/обновление секции **YouTrack Integration**) — только после подтверждения
- (опционально) создание проекта и Kanban-доски в YouTrack (по явному согласию)

---

## КРИТИЧЕСКИЕ ПРАВИЛА

> **ЗАПРЕЩЕНО**: Связывать проект без подтверждения пользователя.
> **ЗАПРЕЩЕНО**: Создавать проект в YouTrack без явного согласия.
> **ЗАПРЕЩЕНО**: Изменять README.md без показа изменений.
> **ОБЯЗАТЕЛЬНО**: Проверить наличие credentials перед началом.
> **ОБЯЗАТЕЛЬНО**: Показать план связывания и дождаться подтверждения.
> **ОБЯЗАТЕЛЬНО**: Использовать AskQuestion для структурированных вопросов.

---

## Предварительные требования

### Конфигурация `.env`

```bash
# YouTrack instance URL
YOUTRACK_URL=https://yt.example.com

# YouTrack permanent token
YOUTRACK_TOKEN=perm:your-token-here
```

### Получение токена YouTrack

1. Войти в YouTrack → Profile → Account Security
2. Нажать "New token..."
3. Дать название токену (например, "vAIbe-os Integration")
4. Выбрать scope: `YouTrack`
5. Скопировать токен и сохранить в `.env`

---

## Алгоритм

### 1. **Инициализация**
   - Пользователь вызывает команду `/yt-project-link`
   - Опционально указывает проект: `/yt-project-link {PROJECT_NAME}`
   - Агент проверяет наличие credentials в `.env`

### 2. **Проверка конфигурации**
   
   ```
   🔍 Проверка конфигурации YouTrack...
   
   ✅ YOUTRACK_URL: https://yt.example.com
   ✅ YOUTRACK_TOKEN: настроен
   
   или
   
   ❌ YOUTRACK_URL: не задан
   ❌ YOUTRACK_TOKEN: не задан
   
   Пожалуйста, настройте переменные в .env файле.
   См. .env.example для примера.
   ```

   Если credentials отсутствуют → **СТОП**, инструкция по настройке.

### 3. **Выбор проекта vAIbe-os**

> ⚠️ **ТОЧКА ОСТАНОВА**: Если проект не указан, запросить выбор.

   **Агент показывает список проектов:**
   
   ```
   📁 Доступные проекты vAIbe-os:
   
   1. ЕПК ФРИИ
   2. 000-vAIbe-os
   3. ЭНСО
   
   Выберите проект для связывания с YouTrack:
   ```
   
   **→ СТОП. Ожидание выбора пользователя.**

### 4. **Проверка текущего состояния**
   - Прочитать `Проекты/{NAME}/README.md`
   - Проверить наличие секции "YouTrack Integration"
   
   **Если проект уже связан:**
   ```
   ⚠️ Проект уже связан с YouTrack
   
   - Project ID: PROJECT
   - Project URL: https://yt.example.com/projects/PROJECT
   - Связан: 2026-01-25
   
   Хотите:
   1. Обновить связь (выбрать другой проект YouTrack)
   2. Отменить связь
   3. Оставить как есть
   ```
   
   **→ СТОП. Ожидание выбора.**

### 5. **Выбор режима связывания**

> ⚠️ **ТОЧКА ОСТАНОВА**: Запрос режима связывания.

   ```
   🔗 Режим связывания:
   
   1. Привязать к существующему проекту YouTrack
      - Укажите URL или ID проекта
   
   2. Создать новый проект в YouTrack
      - Проект будет создан автоматически
   
   Выберите режим:
   ```
   
   **→ СТОП. Ожидание выбора.**

### 6a. **Режим: Привязка к существующему**
   
   **Запрос ID или URL проекта:**
   ```
   📎 Привязка к существующему проекту
   
   Введите:
   - Short name проекта (например: UCP, AIOS)
   - или URL проекта (например: https://yt.example.com/projects/UCP)
   ```
   
   **→ СТОП. Ожидание ввода.**
   
   **Валидация проекта:**
   ```
   GET /api/admin/projects/{projectId}
   
   ✅ Проект найден:
   - Название: Unified Control Panel
   - Short name: UCP
   - URL: https://yt.example.com/projects/UCP
   
   или
   
   ❌ Проект не найден. Проверьте ID и попробуйте снова.
   ```

### 6b. **Режим: Создание нового проекта**

> ⚠️ **ТОЧКА ОСТАНОВА**: Запрос параметров нового проекта.

   ```
   🆕 Создание нового проекта в YouTrack
   
   Параметры:
   1. Short name (латиница, до 10 символов): 
      Предложение: {сгенерированное из названия проекта}
   
   2. Название проекта в YouTrack:
      Предложение: {название из vAIbe-os}
   
   3. Описание (опционально):
      Предложение: {описание из README.md}
   
   Подтвердите параметры или измените:
   ```
   
   **→ СТОП. Ожидание подтверждения.**
   
   **Создание проекта:**
   ```
   POST /api/admin/projects
   {
     "shortName": "UCP",
     "name": "ЕПК ФРИИ",
     "description": "Описание проекта",
     "leader": {"login": "cursor"}
   }
   ```

   **Добавление участников в проект (через Hub API):**
   ```
   # Шаг 1: Получить Hub ID пользователей
   GET {YOUTRACK_URL}/hub/api/rest/users?fields=id,name,login
   # Запомнить id нужных пользователей (UUID формат)
   
   # Шаг 2: Получить Project Team ID
   GET {YOUTRACK_URL}/hub/api/rest/projectteams?query=project:{project_hub_id}&fields=id
   
   # Шаг 3: Добавить пользователей в команду проекта
   POST {YOUTRACK_URL}/hub/api/rest/projectteams/{projectteam_id}/users
   {"id": "{user_hub_id}"}
   
   # Шаг 4 (опционально): Назначить роль Контрибьютор
   POST {YOUTRACK_URL}/hub/api/rest/users/{user_hub_id}/projectroles
   {
     "role": {"id": "{contributor_role_id}"},
     "project": {"id": "{project_hub_id}"}
   }
   ```
   
   ⚠️ **ВАЖНО**: 
   - Используется Hub API (`/hub/api/rest/`), а не YouTrack API (`/api/`)
   - **Шаг 3 обязателен** — добавляет в список участников (видно в UI проекта)
   - **Шаг 4 опционален** — даёт дополнительные права (Контрибьютор)
   - user_hub_id — UUID пользователя из Hub (например: `c1a532c7-80e3-498e-bf1f-b7bfd5d205cf`)
   - projectteam_id — UUID команды проекта из Hub (например: `8443105c-f6d0-470f-a576-f578ed4867d1`)

   **Автоматическое создание Kanban-доски (4 шага):**
   ```
   # Шаг 1: Создание доски
   POST /api/agiles
   {
     "name": "{Название проекта}: доска Kanban",
     "projects": [{"id": "{project_id}"}]
   }
   
   # Шаг 2: Настройка колонок (ОБЯЗАТЕЛЬНО!)
   POST /api/agiles/{agile_id}
   {
     "columnSettings": {
       "field": {"id": "150-2"}  # State field
     }
   }
   
   # Шаг 3: Настройка видимости (ОБЯЗАТЕЛЬНО!)
   POST /api/agiles/{agile_id}
   {
     "visibleFor": {"ringId": "9a6d539a-cae9-4b88-a7d7-dd0bd1191a7e"},
     "updateableBy": {"ringId": "9a6d539a-cae9-4b88-a7d7-dd0bd1191a7e"}
   }
   # ringId — UUID группы "Все пользователи" из Hub API
   
   # Шаг 4: Настройка поведения Kanban
   POST /api/agiles/{agile_id}
   {
     "sprintsSettings": {
       "isExplicit": false,    # Автоматически добавлять новые задачи
       "disableSprints": true  # Kanban-режим (без спринтов)
     }
   }
   ```
   
   ⚠️ **ВАЖНО**: 
   - Без `columnSettings` доска будет невалидной
   - Без `visibleFor` доска будет видна только владельцу
   - Без `isExplicit: false` новые задачи не будут появляться на доске
   
   ✅ Kanban-доска создаётся автоматически после создания проекта.

### 6c. **Добавление участников в проект**

   Если пользователь указал участников при создании проекта:
   
   ```
   👥 Добавление участников в проект
   
   Участники для добавления:
   - Анатолий Гаркуша
   - Артём Раров
   
   Поиск пользователей в YouTrack Hub...
   ```
   
   **Получение необходимых ID:**
   ```
   # 1. Получить Hub ID пользователей
   GET /hub/api/rest/users?fields=id,name,login
   
   # 2. Получить Project Team ID
   GET /hub/api/rest/projectteams?query=project:{project_hub_id}&fields=id,project(id,name)
   ```
   
   **Добавление в команду проекта (Project Team):**
   ```
   # Для каждого пользователя:
   POST /hub/api/rest/projectteams/{projectteam_id}/users
   {"id": "{user_hub_id}"}
   
   ✅ Анатолий Гаркуша добавлен в команду проекта
   ✅ Артём Раров добавлен в команду проекта
   ```
   
   **Назначение ролей (опционально, для дополнительных прав):**
   ```
   POST /hub/api/rest/users/{user_hub_id}/projectroles
   {
     "role": {"id": "{contributor_role_id}"},
     "project": {"id": "{project_hub_id}"}
   }
   ```
   
   ⚠️ **ВАЖНО**: 
   - Добавление в Project Team через `/projectteams/{id}/users` — добавляет в список участников
   - Назначение роли через `/users/{id}/projectroles` — даёт права в проекте
   - Для полноценного участия нужны ОБА действия

### 7. **Подтверждение связывания**

> ⚠️ **ТОЧКА ОСТАНОВА**: Показать план изменений.

   ```
   ✅ План связывания
   
   📁 Проект vAIbe-os: ЕПК ФРИИ
   🔗 Проект YouTrack: UCP (https://yt.example.com/projects/UCP)
   
   📄 Изменения в Проекты/ЕПК ФРИИ/README.md:
   
   Будет добавлена секция:
   
   ## YouTrack Integration
   - **Project ID**: UCP
   - **Project URL**: https://yt.example.com/projects/UCP
   - **Linked**: 2026-01-27
   
   Выполнить связывание?
   ```
   
   **→ СТОП. Ожидание подтверждения.**

### 8. **Выполнение связывания**
   
   **ТОЛЬКО ПОСЛЕ подтверждения:**
   - Обновить README.md проекта, добавив секцию YouTrack Integration
   - Вывести результат:
   
   ```
   ✅ Проект успешно связан с YouTrack!
   
   📁 vAIbe-os: Проекты/ЕПК ФРИИ/
   🔗 YouTrack: https://yt.example.com/projects/UCP
   📋 Kanban: https://yt.example.com/agiles/{agile_id}
   
   Следующие шаги:
   - /yt-project-tasks-push — опубликовать задачи в YouTrack
   - /yt-project-tasks-pull — получить обновления из YouTrack
   ```

---

## Формат секции YouTrack Integration

Добавляется в README.md проекта:

```markdown
## YouTrack Integration
- **Project ID**: {SHORT_NAME}
- **Project URL**: {YOUTRACK_URL}/projects/{SHORT_NAME}
- **Kanban Board**: {YOUTRACK_URL}/agiles/{AGILE_ID}
- **Linked**: {YYYY-MM-DD}
- **Default Assignee**: Cursor (опционально)
```

---

## Примеры

### Пример 1: Привязка к существующему проекту
**Запрос**: `/yt-project-link ЕПК ФРИИ`

```
1. ✅ Конфигурация проверена

2. 📁 Проект: ЕПК ФРИИ

3. 🔗 Режим связывания:
   1. Привязать к существующему
   2. Создать новый
   
   → Пользователь: "1"

4. 📎 Введите Short name или URL:
   
   → Пользователь: "UCP"

5. ✅ Проект найден: Unified Control Panel (UCP)

6. ✅ План связывания:
   - Добавить секцию YouTrack Integration в README.md
   
   → Пользователь: "да"

7. ✅ Проект успешно связан!
```

### Пример 2: Создание нового проекта
**Запрос**: `/yt-project-link`

```
1. ✅ Конфигурация проверена

2. 📁 Выберите проект:
   1. ЕПК ФРИИ
   2. 000-vAIbe-os
   
   → Пользователь: "2"

3. 🔗 Режим связывания:
   
   → Пользователь: "Создать новый"

4. 🆕 Параметры нового проекта:
   - Short name: AIOS
   - Название: 000-vAIbe-os
   - Описание: Системный проект vAIbe-os
   
   → Пользователь: "да"

5. ✅ Проект создан в YouTrack: AIOS

6. ✅ Kanban-доска создана: AIOS: доска Kanban

7. ✅ Проект успешно связан!
```

### Пример 3: Проект уже связан
**Запрос**: `/yt-project-link ЕПК ФРИИ`

```
1. ⚠️ Проект уже связан:
   - YouTrack: UCP
   - URL: https://yt.example.com/projects/UCP
   
   Хотите:
   1. Обновить связь
   2. Отменить связь
   3. Оставить как есть
   
   → Пользователь: "3"

2. ℹ️ Связь сохранена без изменений.
```

---

## Обработка ошибок

### Credentials не настроены
```
❌ YouTrack не настроен

Для работы интеграции необходимо:

1. Скопировать .env.example в .env
2. Заполнить переменные:
   - YOUTRACK_URL — URL вашего YouTrack
   - YOUTRACK_TOKEN — API токен

Как получить токен:
1. YouTrack → Profile → Account Security
2. New token → Scope: YouTrack
3. Скопировать и вставить в .env
```

### Проект YouTrack не найден
```
❌ Проект не найден

Short name "{ID}" не существует в YouTrack.

Возможные причины:
- Опечатка в Short name
- Проект удалён или переименован
- Недостаточно прав доступа

Попробуйте:
- Проверить Short name в YouTrack
- Использовать полный URL проекта
- Создать новый проект
```

### Ошибка API
```
❌ Ошибка подключения к YouTrack

Статус: 401 Unauthorized

Возможные причины:
- Токен недействителен или истёк
- Токен не имеет необходимых прав

Действия:
- Проверьте токен в .env
- Создайте новый токен с правами YouTrack
```

### Проект vAIbe-os не найден
```
❌ Проект не найден

Проект "{NAME}" не существует в vAIbe-os.

Доступные проекты:
1. ЕПК ФРИИ
2. 000-vAIbe-os

Выберите существующий проект или создайте новый через /task-create.
```

---

## API запросы

### Проверка подключения
```
GET {YOUTRACK_URL}/api/admin/projects?fields=id,name,shortName
Authorization: Bearer {YOUTRACK_TOKEN}
```

### Получение проекта
```
GET {YOUTRACK_URL}/api/admin/projects/{projectId}?fields=id,name,shortName,description
Authorization: Bearer {YOUTRACK_TOKEN}
```

### Создание проекта
```
POST {YOUTRACK_URL}/api/admin/projects
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "shortName": "UCP",
  "name": "Unified Control Panel",
  "description": "Описание проекта",
  "leader": {"login": "cursor"}
}
```

### Создание Kanban-доски (четыре шага)

**Шаг 1: Создание доски**
```
POST {YOUTRACK_URL}/api/agiles
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "name": "{Название проекта}: доска Kanban",
  "projects": [{"id": "{project_id}"}]
}

Ответ:
{
  "id": "192-6",
  "$type": "Agile"
}
```

**Шаг 2: Настройка колонок (ОБЯЗАТЕЛЬНО!)**
```
POST {YOUTRACK_URL}/api/agiles/{agile_id}
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "columnSettings": {
    "field": {"id": "150-2"}
  }
}
```

Поле `150-2` — стандартное поле "State". Колонки создаются автоматически.

**Шаг 3: Настройка видимости (ОБЯЗАТЕЛЬНО!)**
```
POST {YOUTRACK_URL}/api/agiles/{agile_id}
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "visibleFor": {"ringId": "{ALL_USERS_RING_ID}"},
  "updateableBy": {"ringId": "{ALL_USERS_RING_ID}"}
}
```

Для получения `ringId` группы "Все пользователи":
```
GET {YOUTRACK_URL}/hub/api/rest/usergroups?fields=id,name
→ найти группу "Все пользователи" и использовать её id как ringId
```

**Шаг 4: Настройка поведения Kanban**
```
POST {YOUTRACK_URL}/api/agiles/{agile_id}
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "sprintsSettings": {
    "isExplicit": false,
    "disableSprints": true
  }
}
```

- `isExplicit: false` — новые задачи автоматически появляются на доске
- `disableSprints: true` — Kanban-режим без спринтов

⚠️ **Без шага 2** доска будет невалидной (ошибка "Не задан параметр колонок")
⚠️ **Без шага 3** доска будет видна только владельцу
⚠️ **Без шага 4** новые задачи не будут автоматически появляться на доске

URL доски: `{YOUTRACK_URL}/agiles/{agile_id}`

### Добавление участников в проект (Hub API)

**Шаг 1: Получить Hub ID пользователей**
```
GET {YOUTRACK_URL}/hub/api/rest/users?fields=id,name,login
Authorization: Bearer {YOUTRACK_TOKEN}

Ответ:
{
  "users": [
    {"id": "c1a532c7-80e3-498e-bf1f-b7bfd5d205cf", "login": "anatoly.garkusha", "name": "Анатолий Гаркуша"},
    {"id": "6c1cbcaa-a56c-4dad-944b-9d6ea4d72d2e", "login": "artem.rarov", "name": "Артём Раров"},
    ...
  ]
}
```

**Шаг 2: Получить Project Team ID**
```
GET {YOUTRACK_URL}/hub/api/rest/projectteams?query=project:{project_hub_id}&fields=id,project(id,name),users(id,name)
Authorization: Bearer {YOUTRACK_TOKEN}

Ответ:
{
  "projectteams": [
    {
      "id": "8443105c-f6d0-470f-a576-f578ed4867d1",
      "project": {"id": "d58db715-6118-4e09-9d2d-c14b48aa9ef8", "name": "ЕПК ФРИИ"},
      "users": [...]
    }
  ]
}
```

**Шаг 3: Добавить пользователя в команду проекта (Project Team)**
```
POST {YOUTRACK_URL}/hub/api/rest/projectteams/{projectteam_id}/users
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{"id": "c1a532c7-80e3-498e-bf1f-b7bfd5d205cf"}

Ответ:
{
  "type": "user",
  "id": "c1a532c7-80e3-498e-bf1f-b7bfd5d205cf",
  "name": "Анатолий Гаркуша",
  "login": "anatoly.garkusha"
}
```

**Шаг 4 (опционально): Назначить роль пользователю**
```
POST {YOUTRACK_URL}/hub/api/rest/users/{user_hub_id}/projectroles
Authorization: Bearer {YOUTRACK_TOKEN}
Content-Type: application/json

{
  "role": {"id": "f219e9ba-302b-44d9-895b-499722572d57"},
  "project": {"id": "d58db715-6118-4e09-9d2d-c14b48aa9ef8"}
}

Ответ:
{
  "type": "projectRole",
  "id": "467e3e2f-a93e-47ed-9b40-4ce0dfe9cfc2",
  "role": {"name": "Контрибьютор"},
  "project": {"name": "ЕПК ФРИИ"}
}
```

⚠️ **ВАЖНО**:
- **Шаг 3 обязателен** — добавляет в список участников проекта (отображается в UI)
- **Шаг 4 опционален** — назначает роль для дополнительных прав
- `user_hub_id` — UUID пользователя из Hub API (НЕ YouTrack ID вида "2-1")
- `project_hub_id` — UUID проекта из Hub API (НЕ YouTrack ID вида "0-7")
- `projectteam_id` — UUID команды проекта из Hub API
- Доступные роли: system-admin, project-admin, contributor, observer, youtrack-issue-reader, youtrack-reporter

---

## Права пользователя YouTrack

Для полной функциональности сервисный пользователь "Cursor" должен иметь права:

| Право | Необходимо для |
|-------|----------------|
| Create Project | Создание новых проектов |
| Read Project | Привязка к существующим |
| Update Project | Изменение настроек (опционально) |
| Create Agile Board | Создание Kanban-досок |
| Manage Project Roles (Hub) | Добавление участников в проект |

### Роли для участников проекта

| Роль | key | Права |
|------|-----|-------|
| Системный администратор | system-admin | Полный доступ ко всему |
| Администратор проекта | project-admin | Управление проектом |
| Контрибьютор | contributor | Создание и редактирование задач |
| Наблюдатель | observer | Только просмотр |
| Читатель задач | youtrack-issue-reader | Просмотр задач |
| Автор задач | youtrack-reporter | Создание задач |

---

## Связанные команды
- `/plan-update` — создать/обновить snapshot-план (основа для публикации задач)
- `/yt-project-tasks-push` — опубликовать задачи в YouTrack
- `/yt-project-tasks-pull` — получить обновления из YouTrack и создать новый план

---

## Примечания

- Один проект vAIbe-os может быть связан только с одним проектом YouTrack
- Связывание не создаёт issues автоматически — используйте `/yt-project-tasks-push`
- При удалении проекта в YouTrack связь остаётся в README.md (требуется ручное удаление)
- Для нескольких инстансов YouTrack — используйте разные `.env` конфигурации
