# Git: стандарт коммит-сообщений

Цель: единый, читаемый формат коммитов на основе [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

---

## Формат

```
<emoji> <type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

- **Язык**: английский (по умолчанию)
- **`<description>`**: начинается со строчной буквы, без точки в конце
- **`<scope>`**: опционально, существительное — модуль или область изменений (например, `tasks`, `skills`, `inbox`)
- **`<body>`**: свободный текст через пустую строку после description, если нужны детали
- **`<footer>`**: `BREAKING CHANGE: ...`, `Refs: #123` и т.д.

---

## Типы и emoji

| Emoji | Type | Когда использовать |
|-------|------|-------------------|
| ✨ | `feat` | Новая функциональность, файл, проект, задача |
| 🐛 | `fix` | Исправление ошибки, опечатки в коде/логике |
| 📝 | `docs` | Документация, README, база знаний, заметки |
| 🎨 | `style` | Форматирование, отступы, пробелы (не меняет логику) |
| ♻️ | `refactor` | Рефакторинг без изменения поведения |
| ⚡ | `perf` | Оптимизация производительности |
| ✅ | `test` | Добавление или правка тестов |
| 🔧 | `chore` | Рутина: зависимости, конфиги, .gitignore |
| 🏗️ | `build` | Сборка, CI/CD, инфраструктура |
| 🔀 | `merge` | Слияние веток |
| ⏪ | `revert` | Откат предыдущего коммита |
| 📦 | `archive` | Архивация, перенос в архив |
| 🚀 | `deploy` | Деплой, релиз |
| 🔒 | `security` | Исправления безопасности |
| 🌐 | `i18n` | Локализация, переводы |

---

## Примеры

```
✨ feat(tasks): add architecture design task for vAIbe-listener
```

```
📝 docs(knowledge): update tech stack reference
```

```
🐛 fix(skills): correct task numbering in task-create
```

```
🔧 chore: update .gitignore for personal projects
```

```
♻️ refactor(tools): extract PDF conversion into separate module

Moved shared logic from markdown_to_pdf into a reusable utility.
Existing API unchanged.
```

```
✨ feat(meetings): add daily sync transcript for МойПроект

BREAKING CHANGE: meeting folder naming now includes dash separator
```

---

## Правила

1. **Один коммит = одно логическое изменение.** Не смешивать feat + fix в одном коммите.
2. **Scope** берётся из контекста изменений: имя проекта, модуля, директории (`tasks`, `skills`, `inbox`, `contacts`, `tools`, имя проекта и т.д.).
3. **Breaking changes** обозначаются `!` после type/scope и/или футером `BREAKING CHANGE:`.
4. **Emoji ставится первым символом** строки коммита, перед type.
5. При коммите через агента — агент автоматически подбирает type и emoji по характеру изменений.

---

## Связи

- Кросс-платформенная работа с git: `.ai/rules/git-cross-platform.md`
- Протокол staging и коммита: `.ai/rules/git-cross-platform.md` → Правило 5
