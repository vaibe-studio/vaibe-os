# Contributing to vAIbe-OS

> :ru: [Инструкция на русском](#contributing-to-vaibe-os-ru)

Thank you for your interest in vAIbe-OS! This project is built on a philosophy of **partnership between humans and AI** — and that extends to how we collaborate with contributors.

## How to contribute

### 1. Report a bug or suggest an improvement

[Open an issue](../../issues/new/choose) — we have templates for bugs, feature requests, and skill proposals.

### 2. Add a new skill

Skills are the heart of vAIbe-OS. Each skill is a Markdown playbook in `.ai/skills/domain/`.

**Steps:**
1. Create `.ai/skills/domain/your-skill.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   name: your-skill
   description: What this skill does (one line)
   triggers: [keyword1, keyword2, keyword3]
   ---
   ```
3. Include these sections: **Purpose**, **Procedure** (step-by-step), **Output format**, **Quality bar**
4. The router (`.ai/router.md`) discovers new skills automatically — no registration needed
5. Submit a PR

**Good skill examples:** Look at existing skills in `.ai/skills/core/` and `.ai/skills/domain/` for reference.

### 3. Improve existing skills or knowledge base

Every skill and knowledge file is plain Markdown. Read it, improve it, submit a PR.

**Knowledge base** (`.ai/knowledge/`) contains reference materials — strategy frameworks, PM principles, sales methodologies, and more. Contributions that add new domain knowledge or improve existing materials are welcome.

### 4. Improve tools

Python utilities live in `tools/`. Run them with `python -m tools.<name>`.

- Follow existing code style
- Stdlib-only where possible (minimize dependencies)
- Add/update `tools/TOOLS_INDEX.md` if adding a new tool

### 5. Improve documentation

README, AGENTS.md, and rule files — improvements to clarity and accuracy are always welcome.

## Guidelines

### Philosophy alignment

vAIbe-OS is built on specific principles ([Manifesto](.ai/MANIFESTO.md), [Ontology](.ai/ONTOLOGY.md)). When contributing, keep these in mind:

- **Partnership, not replacement** — features should augment the user, not create dependency
- **Additive evolution** — prefer adding and refining over deleting. Knowledge accumulates, it doesn't get erased
- **Autonomy of the source** — the user always makes the final decision. Don't build features that decide for the user
- **Honesty about LLM** — acknowledge limitations, don't create illusions of superpowers

### File naming

- Folders and files in the vault use **Russian names** (except `tools/`, `.ai/`, `repositories/`, system `.md` files)
- Task numbers use leading zeros: `001`, `002`, `010`
- See `.ai/rules/structure.md` for the full specification

### Pull requests

- Keep PRs focused — one change per PR
- Describe **what** and **why** in the PR description
- If changing skills or rules, explain how it aligns with the manifesto
- For new skills: include at least one usage example

### Code style

- Python: follow existing patterns, stdlib preferred
- Markdown: ATX headings (`#`), fenced code blocks, reference-style links where possible
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/) with emoji prefix (see `.ai/rules/git-commits.md`)

## Development setup

```bash
git clone https://github.com/vAIbe-studio/vaibe-os.git
cd vaibe-os
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

No additional dependencies needed for the core vault. Tools may have their own requirements.

## Questions?

- [Open a discussion](../../discussions) for questions and ideas
- [Open an issue](../../issues) for bugs and feature requests

---

# Contributing to vAIbe-OS (RU)

Спасибо за интерес к vAIbe-OS! Проект построен на философии **партнёрства человека и ИИ** — это распространяется и на работу с контрибьюторами.

## Как внести вклад

### 1. Сообщить о баге или предложить улучшение

[Создайте issue](../../issues/new/choose) — есть шаблоны для багов, фич и новых скиллов.

### 2. Добавить новый скилл

Скиллы — сердце vAIbe-OS. Каждый скилл — это Markdown-плейбук в `.ai/skills/domain/`.

**Шаги:**
1. Создайте `.ai/skills/domain/your-skill.md`
2. Добавьте YAML-метаданные:
   ```yaml
   ---
   name: your-skill
   description: Что делает скилл (одна строка)
   triggers: [ключевое_слово1, ключевое_слово2]
   ---
   ```
3. Включите секции: **Purpose**, **Procedure** (пошагово), **Output format**, **Quality bar**
4. Роутер (`.ai/router.md`) подхватит скилл автоматически — регистрация не нужна
5. Отправьте PR

**Примеры хороших скиллов:** смотрите `.ai/skills/core/` и `.ai/skills/domain/`.

### 3. Улучшить существующие скиллы или базу знаний

Все скиллы и материалы базы знаний — это Markdown-файлы. Прочитайте, улучшите, отправьте PR.

**База знаний** (`.ai/knowledge/`) содержит справочные материалы. Вклад в расширение доменных знаний приветствуется.

### 4. Улучшить инструменты

Python-утилиты находятся в `tools/`. Запуск: `python -m tools.<name>`.

- Следуйте стилю существующего кода
- Предпочитайте стандартную библиотеку (минимум зависимостей)
- Обновите `tools/TOOLS_INDEX.md` при добавлении нового инструмента

### 5. Улучшить документацию

README, AGENTS.md, файлы правил — улучшения ясности и точности всегда приветствуются.

## Правила

### Соответствие философии

vAIbe-OS построен на конкретных принципах ([Манифест](.ai/MANIFESTO.md), [Онтология](.ai/ONTOLOGY.md)):

- **Партнёрство, не замена** — фичи должны усиливать пользователя, не создавать зависимость
- **Аддитивная эволюция** — добавляем и уточняем, а не удаляем. Знания накапливаются
- **Автономия источника** — решение всегда за пользователем. Не создавайте фичи, которые решают за него
- **Честность об LLM** — признавайте ограничения, не создавайте иллюзий

### Именование файлов

- Папки и файлы в хранилище — **на русском языке** (кроме `tools/`, `.ai/`, `repositories/`, системные `.md`)
- Номера задач с ведущими нулями: `001`, `002`, `010`
- Полная спецификация: `.ai/rules/structure.md`

### Pull requests

- Один PR — одно изменение
- Опишите **что** и **зачем** в описании PR
- При изменении скиллов или правил — объясните, как это соответствует манифесту
- Для новых скиллов: приложите хотя бы один пример использования

### Стиль кода

- Python: следуйте существующим паттернам, предпочитайте stdlib
- Markdown: ATX-заголовки (`#`), огороженные блоки кода
- Коммиты: [Conventional Commits](https://www.conventionalcommits.org/) с эмодзи-префиксом (`.ai/rules/git-commits.md`)

## Настройка окружения

```bash
git clone https://github.com/vAIbe-studio/vaibe-os.git
cd vaibe-os
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

Для ядра хранилища дополнительных зависимостей не нужно.

## Вопросы?

- [Дискуссии](../../discussions) — для вопросов и идей
- [Issues](../../issues) — для багов и запросов на фичи
