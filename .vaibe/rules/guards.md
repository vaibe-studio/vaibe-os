# vAIbe-OS Invariants (Guards)

> Canon rule (`.vaibe/rules/guards.md`, always-on): system-integrity invariants.
> Each invariant is a machine-checkable assertion.
> The executable form of these invariants lives in `doctor diagnose`: G1–G6, G10–G12 are checked
> by machine; G7 is a process guard (info before deleting knowledge), G8–G9 are advisory. This file
> stays the human-readable spec; the source of truth for the checks is `.vaibe/scripts/doctor/diagnose.py`.

**Ontological grounding**: Law 5 (Additivity) — the system evolves without degradation. Guards are the formalization of the boundaries within which evolution is safe. Their place in the layer spine — the single stack in `.vaibe/rules/ontology.md` (guards = invariants derived from the laws; enforced by doctor).

---

## G1: Projects — README.md + Видимость

**Rule**: every `Проекты/{NAME}/` directory contains a `README.md` with a `Видимость: командный | личный` field.

**Assertion**:
```
FOR EACH dir IN Проекты/**/
  IF dir CONTAINS README.md   # skip intermediate folders like Личное/
    ASSERT EXISTS dir/README.md
    ASSERT dir/README.md CONTAINS "Видимость:"
    ASSERT value IN ["командный", "личный"]
```

**Consequence**: a personal project (`Видимость: личный`) is in `.gitignore`/`.git/info/exclude`. A team project is tracked in Git.

**Law**: Externalization — the project structure is a form in which working cognition exists outside.

---

## G2: Tasks — task.md + a «Статус» section

**Rule**: every `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/` directory contains a `task.md` with a `## Статус` section at the end of the file.

**Assertion**:
```
FOR EACH dir IN Проекты/**/Задачи/*/
  ASSERT EXISTS dir/task.md
  ASSERT dir/task.md CONTAINS section "## Статус"
  ASSERT section "## Статус" IS last H2 section in file
  ASSERT section CONTAINS "**Статус**:" WITH value IN ["открыта", "в процессе", "выполнена", "на холде"]
```

**Law**: Feedback — the task status lets the system track progress and propose actions.

---

## G3: Russian language for files and folders

**Rule**: all user-content files and folders are named in Russian.

**Assertion**:
```
FOR EACH path IN vault root (recursive)
  IF path NOT IN excluded_prefixes
    ASSERT basename(path) MATCHES Cyrillic pattern OR is system name (README.md, task.md, etc.)
```

**Exceptions** (Latin allowed):
- `.vaibe/`, `.cursor/`, `.claude/`, `.codex/`, `.opencode/` — system configs/canon
- `repositories/` — git submodules
- `results/v{N}/` — files inside result versions (code, HTML allowed)
- System files: `README.md`, `task.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`

**Law**: Externalization — Russian is fixed as the user's language of thought.

---

## G4: Task numbering — uniqueness and format

**Rule**: task numbers within a project are unique and use a leading-zeros format.

**Assertion**:
```
FOR EACH project IN Проекты/**/
  IF project CONTAINS Задачи/
    LET task_dirs = project/Задачи/*/
  LET numbers = EXTRACT {NUM} FROM each dir name matching pattern "{NUM}-{TITLE}"
  ASSERT ALL numbers MATCH /^\d{3,}$/  (minimum 3 digits with leading zeros)
  ASSERT ALL numbers ARE UNIQUE within project
```

**Law**: Additivity — numbering provides ordering and prevents conflicts.

---

## G5: Result versioning

**Rule**: task results are stored in `results/v{N}/`. Each run is a new version. Previous versions are not overwritten.

**Assertion**:
```
FOR EACH task_dir IN Проекты/**/Задачи/*/
  IF EXISTS task_dir/results/
    FOR EACH subdir IN task_dir/results/*/
      ASSERT subdir.name MATCHES /^v\d+$/
    ASSERT NO files directly in results/ (except legacy — warn, don't fail)
```

**Law**: Additivity — versioning guarantees that result evolution does not destroy previous iterations.

---

## G6: Skills — YAML frontmatter (Agent Skills)

**Rule**: every skill in `.vaibe/skills/{name}/SKILL.md` contains YAML frontmatter with the mandatory fields.

**Assertion**:
```
FOR EACH file IN .vaibe/skills/*/SKILL.md
  ASSERT file STARTS WITH "---"
  ASSERT frontmatter CONTAINS field "name" (non-empty, == folder name, a-z0-9-)
  ASSERT frontmatter CONTAINS field "description" (non-empty string, EN + trigger words)
```

**Law**: Directed evolution — discovery by `description` auto-selects skills (router.md removed).

---

## G7: Knowledge protection

**Rule**: knowledge files are not deleted without a replacement or an explicit migration plan.

**Assertion**:
```
BEFORE DELETE any file IN knowledge_paths:
  ASSERT EXISTS migration_plan OR replacement_file
  ASSERT user_confirmation == true

knowledge_paths:
  - База знаний/**
  - Проекты/**/База знаний/**
  - .vaibe/skills/**            (skills + bundled references contain accumulated expertise)
  - .vaibe/rules/ontology.md
  - .vaibe/rules/manifesto.md
  - .vaibe/rules/{mentorship,user-methods,dialogue-patterns,style-adaptation}.md  (meta-mind behavioral playbooks)
```

**Law**: Additivity — knowledge accumulates, it is not erased. Losses are allowed only consciously, preserving context.

---

## G8: Freshness of reference materials

**Rule**: reference skills and `references/` files with links to external sources contain dated/verifiable links; sources older than 18 months are flagged for review at `weekly-review`.

**Law**: Feedback — stale knowledge lowers the quality of recommendations; a regular check closes the loop.

---

## G9: Glossary synchronization

**Rule**: when creating/substantially updating a reference material, check that key terms are reflected in `.vaibe/skills/glossary/SKILL.md`.

**Law**: Directed evolution — the glossary as a single term index ensures the coherence of knowledge.

---

## G10: `repositories/` contains only git submodules

**Rule**: first-level directories inside `repositories/` are allowed only as git submodules registered in `.gitmodules`.

**Assertion**:
```
FOR EACH entry IN repositories/*
  ASSERT entry IS directory AND entry.path EXISTS IN .gitmodules
ASSERT NO plain directories/files IN repositories/ without matching .gitmodules entry
```
> The presence of `entry/.git` is NOT checked: a registered submodule may legitimately be
> un-checked-out (CI with `GIT_SUBMODULE_STRATEGY=none`, a fresh clone without `--recurse-submodules`) —
> that is a valid state; the invariant is registration in `.gitmodules`.

**Law**: Additivity — the code zone is structurally reproducible; the submodule structure prevents boundary blurring.

---

## G11: Canon ↔ native layer (model A)

**Rule**: native wrappers `.{claude,cursor,opencode,codex}/skills/*` and `*/agents/*` carry only metadata + a reference-imperative to the canon `.vaibe/`; the body of the logic is only in the canon. The `GENERATED — DO NOT EDIT` marker appears once (for markdown skill wrappers — as an HTML comment under the frontmatter, not before it: a leading comment breaks YAML parsing in opencode/Claude).

**Law**: Additivity + Directed evolution — a single source of truth (`.vaibe/`) excludes drift; `doctor diagnose` checks `generated == canon`.

---

## G12: No dead links in canon prose

**Rule**: canon prose (`.md`) contains no live references to entities the vision removed
(`router.md`, legacy `.ai/` paths, `tools.md`, `VAULT-INDEX`, `*-brief.md`, `python -m tools.X`,
`requirements.txt`, `pyenv`, `.cursor/commands`). Closes the anti-drift blind spot: `diagnose`
checked `generated == canon` and structure, but not semantic drift of links inside prose.

**Assertion**:
```
FOR EACH line IN (.vaibe/**/*.md + AGENTS.md + Проекты/AGENTS.md)
  IF line MATCHES any removed-entity pattern
     AND NOT (line forbids/declares-removal OR H2-section is "do not use"/anti-pattern/legacy
              OR line contains an external URL)
    ASSERT FAIL (dead reference, file:line)
```

**Scope — dead links only** (minimal, decision 2026-06-18): do not extend to stale headers/
recommendations. False positives are excluded: removal constatations (`router.md удалён`, `legacy .ai/`),
forbidding sections and external URLs (`responsibleailabs.ai`) are correct. Script `.py` docstrings and
project task cards are out of scope (canon prose is checked). Source of truth — `lint_dead_links`
in `diagnose.py`, regression — `test_doctor.py` (`test_dead_links`).

**Law**: Feedback — a machine check closes the loop, preventing this class of dead links from
accumulating (as the dead `router.md` accumulated before task 074).

---

## Usage

### Automatic check (phase 4)
```bash
# Canonical checker — doctor diagnose (check + lint + guards):
uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py diagnose
```
Invariants G1–G6, G10–G12 are implemented as machine-checkable checks in
`.vaibe/scripts/doctor/diagnose.py`. G7 is a process guard (before deletion), G8/G9 are
heuristics (advisory). The `.vaibe/scripts/vault_lint/` prototype (legacy `.ai/` paths) is
superseded; its removal is up to the owner.

### Manual check
At `/evolve`, `/task-create`, `/task-execute` — the agent checks against Guards before writing files.

### Priority on conflict
The single authoritative layer spine is declared in `.vaibe/rules/ontology.md` (ontology → manifesto →
{rules, guards} → skills → behavioral playbooks). Guards are the layer of invariants derived from the
laws (enforced by doctor); on conflict, the deeper layer (ontology) takes priority.

If a Guard contradicts practice — update the Guard via `/evolve`, do not violate it silently.
