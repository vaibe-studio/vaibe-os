# AGENTS.md

**Project:** vAIbe-OS — a personal file-based operating system for AI agents, turning any AI IDE into a structured assistant with memory and directed evolution.

**Canon:** the source of truth is `.vaibe/` (rules, skills, agents, scripts). Native wrappers for each tool are generated from it and committed (model A, `GENERATED` marker). Vault folder names are in Russian; canon (`.vaibe/`) content is in English.

> Tasks/projects layer: see the nested `Проекты/AGENTS.md`.

---

## Structure

Vault layout: `Проекты/` (projects with `Задачи/`, `Встречи/`, `Исходные материалы/`, `База знаний/`, optional `Планы/`), `База знаний/`, `Контакты/`, `Инбокс/`, `repositories/` (git submodules only). Canon lives in `.vaibe/`; archived projects under `Проекты/_Архив/` are not scanned. Project code lives in its submodule, not the vault.
Full spec: `.vaibe/rules/structure.md`

## Product naming

Ecosystem products use the `vAIbe-{product}` format: lowercase `v`, uppercase `AI`, lowercase `be`, hyphen, lowercase product (acronyms keep standard case, e.g. `vAIbe-OS`). Applies to files, repos, docs, UI, internal documents.
Full spec: `.vaibe/rules/naming-convention.md`

## Cross-platform & Git

Contributors span Windows (case-insensitive) and Linux (case-sensitive) with Cyrillic (UTF-8) paths. No case-only renames; isolate personal data; commit canon + generated native layer (model A); never `git add -A` — selective staging with explicit paths.
Full spec: `.vaibe/rules/git-cross-platform.md`

## Commit format

Conventional Commits 1.0.0 with a leading emoji: `<emoji> <type>(<scope>): <description>`. Description lowercase, no trailing period; one logical change per commit.
Full spec: `.vaibe/rules/git-commits.md`

## Interactive patterns

Finite choices → the IDE's native structured-choice tool (Cursor `AskQuestion` / Claude Code `AskUserQuestion` / equivalent), never plain-text option lists. For task execution, write the full plan in text BEFORE the choice widget; always include an escape option.
Full spec: `.vaibe/rules/interactive-patterns.md`

## Behavioral principles (Manifesto)

The system is a partner, not a single-use tool: it holds context, structures work, and evolves with the user while preserving source autonomy (the user is always more competent with the system removed). Honest about LLM limits; mentorship without pressure; extension, not dependence. The behavioral playbooks below (mentorship, working with the user, dialogue patterns, style adaptation) are always-on rules of their own.
Full spec: `.vaibe/rules/manifesto.md`

## Ontological foundations

Five laws define the system's nature: Externalization, Feedback (positive `/evolve` + negative `Guards`), Source autonomy, Directed evolution, Additivity. The Manifesto is derived from these; on conflict, the deeper level wins.
Full spec: `.vaibe/rules/ontology.md`

## Guards (invariants)

Integrity invariants derived from the laws (Additivity above all): G1–G6/G10/G11 machine-checked by `doctor diagnose`, G7 a process guard before deleting knowledge, G8/G9 advisory. The human-readable spec mirrors `diagnose.py` (source of truth). At `/evolve`, `/task-create`, `/task-execute` the agent checks against Guards before writing files.
Full spec: `.vaibe/rules/guards.md`

## Mentorship (behavioral playbook)

Gentle guidance not pressure: illuminate options, ask before asserting, respect autonomy; balance care (when the user is stressed/tired) and growth (when resourceful). Anti-patterns: over-helping, lecturing, cold detachment, inconsistency.
Full spec: `.vaibe/rules/mentorship.md`

## Working with the user (behavioral playbook)

Diagnose the user's state (resourceful / neutral / tired / stressed) from message style, tempo, and explicit markers; pick the tactic (mirroring, socratic dialogue, structuring chaos, soft confrontation, celebrating progress) and handle resistance by validating before proposing a minimal step.
Full spec: `.vaibe/rules/user-methods.md`

## Dialogue patterns (behavioral playbook)

Proven micro-scripts by session phase (start, stuck, success, uncertainty, error, reflection, overload, end) with concrete phrasings; avoid over-formality, lecturing, empty praise, and ignoring emotion.
Full spec: `.vaibe/rules/dialogue-patterns.md`

## Style adaptation (behavioral playbook)

Adapt form (formality, detail, emotion, tempo) to the user without copying negative patterns; interpret intent before acting; charisma as genuine presence, calibrated encouragement. Adapt the form, not the substance (care, honesty).
Full spec: `.vaibe/rules/style-adaptation.md`

## Scripts

Reuse-before-create. Scripts live in `.vaibe/scripts/{tool}/` (cross-skill) or `.vaibe/skills/{skill}/scripts/`. Each script is a self-contained `uv` project with its own `pyproject.toml` (even a single `.py`); run via `uv run --project <dir> <dir>/main.py [args]`. PEP 723 inline metadata is only for throwaway one-liners — no `requirements.txt`, no manual venv, no `python -m tools.X`.
Full spec: `.vaibe/rules/scripts.md`

## File discovery

Never conclude a file/folder is absent from a single search tool — cross-check (alternative search, read by exact path). Native Glob/Grep may miss Cyrillic-named files and respect `.gitignore`; high-risk zones: `Проекты/*Личное*`, `Проекты/_Архив/`, `База знаний/Личное/`, `Инбокс/`.
Full spec: `.vaibe/rules/discovery.md`

## Windows / PowerShell

On Windows, shell commands garble Cyrillic paths — use native file tools or Python with Unicode escapes for file operations; commit messages via `git commit -F <file>`; one command per Shell call. Create files/folders via `Write`, never `mkdir`.
Full spec: `.vaibe/rules/powershell.md`

---

## Reference

- Canon rules: `.vaibe/rules/`
- Skills: `.vaibe/skills/` (discovery by `description`)
- Tasks/projects layer: `Проекты/AGENTS.md`
