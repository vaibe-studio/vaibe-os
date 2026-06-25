# Git: commit message standard

Goal: a single, readable commit format based on [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

---

## Format

```
<emoji> <type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

- **Language**: English (by default)
- **`<description>`**: starts with a lowercase letter, no trailing period
- **`<scope>`**: optional, a noun — the module or area of change (e.g. `tasks`, `skills`, `inbox`)
- **`<body>`**: free text after a blank line following the description, when details are needed
- **`<footer>`**: `BREAKING CHANGE: ...`, `Refs: #123`, etc.

---

## Types and emoji

| Emoji | Type | When to use |
|-------|------|-------------------|
| ✨ | `feat` | New functionality, file, project, task |
| 🐛 | `fix` | Bug fix, typo in code/logic |
| 📝 | `docs` | Documentation, README, knowledge base, notes |
| 🎨 | `style` | Formatting, indentation, whitespace (no logic change) |
| ♻️ | `refactor` | Refactoring without behavior change |
| ⚡ | `perf` | Performance optimization |
| ✅ | `test` | Adding or fixing tests |
| 🔧 | `chore` | Routine: dependencies, configs, .gitignore |
| 🏗️ | `build` | Build, CI/CD, infrastructure |
| 🔀 | `merge` | Branch merge |
| ⏪ | `revert` | Reverting a previous commit |
| 📦 | `archive` | Archiving, moving to archive |
| 🚀 | `deploy` | Deploy, release |
| 🔒 | `security` | Security fixes |
| 🌐 | `i18n` | Localization, translations |

---

## Examples

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
♻️ refactor(scripts): extract PDF conversion into separate module

Moved shared logic from markdown_to_pdf into a reusable utility.
Existing API unchanged.
```

```
✨ feat(meetings): add daily sync transcript for Альфа

BREAKING CHANGE: meeting folder naming now includes dash separator
```

---

## Rules

1. **One commit = one logical change.** Don't mix feat + fix in one commit.
2. **Scope** comes from the change context: project, module, or directory name (`tasks`, `skills`, `inbox`, `contacts`, `scripts`, project name, etc.).
3. **Breaking changes** are marked with `!` after type/scope and/or a `BREAKING CHANGE:` footer.
4. **Emoji is the first character** of the commit line, before the type.
5. When committing via an agent — the agent automatically picks type and emoji based on the nature of the changes.

---

## Related

- Cross-platform git work: `.vaibe/rules/git-cross-platform.md`
- Staging and commit protocol: `.vaibe/rules/git-cross-platform.md` → Rule 5
