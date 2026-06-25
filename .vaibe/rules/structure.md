# vAIbe-OS file system structure

## File and directory organization rules

### Projects
**Path**: `Проекты/{NAME}/`

- Each project is stored in its own subfolder named after the project
- Archived projects are stored in `Проекты/_Архив/{NAME}/` and are **not scanned** during navigation, briefings, and reports (unless explicitly requested)
- The project folder name must be in Russian
- Each project has a **visibility**: `командный` (team, default) or `личный` (personal)
  - `командный` — tracked in Git, available to the whole team
  - `личный` — excluded from Git (see `.vaibe/rules/git-cross-platform.md`): impersonal patterns in the root `.gitignore` and/or a targeted entry in `.git/info/exclude` for a unique name; contains private data
  - Visibility is recorded in the project `README.md` and decided at creation
  - When creating a personal project whose name is not covered by patterns — add `/Проекты/{NAME}/` to `.git/info/exclude`
- Inside the project folder there must be:
  - `README.md` — the project index file with metadata, description, and visibility
  - `Задачи/` — subfolder for project tasks
  - `Встречи/` — subfolder for transcripts, summaries, and tasks from calls
  - `Исходные материалы/` — subfolder for various project files
  - `База знаний/` — subfolder for accumulated objective information about the project
  - `Планы/` — (optional) project snapshot plans
  - Other project files and folders

**Example**:
```
Проекты/
└── AI Операционная Система/
    ├── README.md
    ├── Задачи/
    ├── Встречи/
    ├── Исходные материалы/
    └── База знаний/
```

### Tasks
**Path**: `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/`

- Tasks are stored in the `Задачи/` subfolder inside the project folder
- Each task in its own subfolder
- Task folder name format: `{NUM}-{TITLE}`
  - `{NUM}` — sequential task number (e.g. 001, 002)
  - `{TITLE}` — short task title in Russian
- Inside the task folder there must be a `task.md` file describing the task
- The `task.md` file MUST contain a `## Статус` section at the end of the file

> **The `task.md` format (the `## Статус` section, result versioning) is described in the nested `Проекты/AGENTS.md`** — it applies to the tasks/projects layer and is loaded by hierarchy next to the `Проекты/` folder.

**Example**:
```
Проекты/
└── AI Операционная Система/
    └── Задачи/
        ├── 001-Проектирование системы/
        │   └── task.md
        └── 002-Реализация модулей/
            └── task.md
```

### Task results (versioning)
**Path**: `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/results/v{N}/`

- Task execution results are stored in the `results/` subfolder inside the task folder
- **Each execution** is saved in its own `v{N}/` subfolder (v1, v2, v3...); previous ones are not overwritten
- `task.md` is not duplicated into `results/` — it stays at the task root
- **CSV and tables:** the `.csv` format assumes one table and one header row; Cyrillic — in UTF-8 (often with a BOM for Excel on Windows); multiple logical sheets — in separate `.csv` files or in a single `.xlsx`, not as a "second sheet" inside one CSV. Reference: `.vaibe/skills/csv-tabular-results/` (reference skill)

> The detailed version-numbering algorithm and the values of the `Версия результата` field — in `Проекты/AGENTS.md`.

**Example (task executed 3 times):**
```
Проекты/
└── Альфа/
    └── Задачи/
        └── 019-Макет визитной карточки/
            ├── task.md
            └── results/
                ├── v1/                    ← first execution
                ├── v2/                    ← second
                └── v3/                    ← third
```

### Meetings
**Path**: `Проекты/{NAME}/Встречи/Встреча {N}. {DATE:DD.MM.YYYY} - {TITLE}/`

- Meetings are stored in the `Встречи/` subfolder inside the project folder
- Each meeting in its own subfolder
- Meeting folder name format: `Встреча {N}. {DATE:DD.MM.YYYY} - {TITLE}`
  - `{N}` — sequential meeting number (e.g. 1, 2, 10)
  - `{DATE:DD.MM.YYYY}` — meeting date in DD.MM.YYYY format (e.g. 20.01.2026)
  - `{TITLE}` — short meeting title in Russian
- Inside the meeting folder there may be:
  - `transcript.md` — meeting transcript
  - `summary.md` — meeting summary
  - `tasks.md` — tasks collected from the call
  - Other meeting materials

**Example**:
```
Проекты/
└── AI Операционная Система/
    └── Встречи/
        ├── Встреча 1. 20.01.2026 - Обсуждение архитектуры/
        │   ├── transcript.md
        │   ├── summary.md
        │   └── tasks.md
        └── Встреча 2. 25.01.2026 - Планирование спринта/
            └── ...
```

### Source materials
**Path**: `Проекты/{NAME}/Исходные материалы/`

- Source materials are stored in the `Исходные материалы/` subfolder inside the project folder
- Contains various project files: documents, specifications, design mockups, diagrams, etc.
- May be organized into subfolders by material type
- File and subfolder names in Russian

### Project knowledge base
**Path**: `Проекты/{NAME}/База знаний/`

- The project knowledge base is stored in the `База знаний/` subfolder inside the project folder
- Contains accumulated objective information about the project
- May be organized into subfolders by topic
- File and subfolder names in Russian

### vAIbe-OS canon (IDE-independent)
**Path**: `.vaibe/`

The canonical source of truth for the system, independent of any specific AI IDE (Cursor, Claude Code, OpenCode, Codex). The native wrappers for each tool are **generated** from it (see `.vaibe/rules/git-cross-platform.md` — model A: the native layer is committed with a `GENERATED` marker).

```
.vaibe/
├── rules/      — canonical rules (behavior, structure, git, discovery, scripts)
│                 including the behavioral layer: ontology.md, manifesto.md
├── skills/     — actionable playbooks (Agent Skills): {name}/SKILL.md, references/, scripts/, assets/
├── agents/     — subagent registry (placeholder)
└── scripts/    — cross-skill Python utilities (uv / PEP 723)
```

- `.vaibe/rules/ontology.md` — the ontological foundation: five laws defining the nature and evolution of the system
- `.vaibe/rules/manifesto.md` — behavioral principles (derived from the ontology)
- `.vaibe/skills/{name}/SKILL.md` — a playbook with YAML frontmatter (`name`, `description`, `license`) + process, output format, and quality checklist. Skill discovery is by the `description` field (no separate router)
- `.vaibe/scripts/` — shared utilities; a specific skill's scripts live in `{skill}/scripts/`. Each script is a `uv` project (its own `pyproject.toml`), run via `uv run --project <dir> <dir>/main.py` — see `.vaibe/rules/scripts.md`

**Example**:
```
.vaibe/
├── rules/
│   ├── ontology.md
│   ├── manifesto.md
│   ├── structure.md
│   └── ...
├── skills/
│   ├── task-create/SKILL.md
│   ├── task-execute/SKILL.md
│   └── ...
└── scripts/
    └── markdown_to_pdf/
```

### Plans (optional)
**Path**: `Проекты/{NAME}/Планы/`

- Project snapshot plans: priorities, current sprint, statuses
- File name format: `План - {N} - {DD.MM.YYYY} - {TITLE}.md`
- Plans are not edited "after the fact" — new versions are created
- They serve as an integration point (e.g. with YouTrack)

### User knowledge base
**Path**: `База знаний/`

- The OS user's knowledge base is stored in the root `База знаний/` folder
- Contains extra context the user can selectively add to prompts
- May contain any materials: notes, documentation, references, etc.
- File and subfolder names in Russian
- Has a **visibility** analogous to projects:
  - Files and folders at the root of `База знаний/` — **shared** (tracked in Git)
  - The `База знаний/Личное/` folder — **personal** (excluded from Git by a pattern in the root `.gitignore`)
  - When adding material the agent asks: "shared or personal?"

### Contacts
**Path**: `Контакты/`

- A root folder with a directory of people encountered in the system's work
- It is the **source of truth** for names, surnames, roles, aliases, and context about people
- One person = one Markdown file
- Organization by category subfolders is allowed: `Команда/`, `ФРИИ/`, `Эксперты/`, `Клиенты/`, `Лиды/`
- If abbreviations, nicknames, or erroneous name variants appear in work materials, they are recorded in the contact card
- For people without a confirmed surname, use the most stable name and explicitly note that the surname is not given

### Repositories
**Path**: `repositories/`

- A directory for storing project code git repositories
- Repositories are attached as git submodules
- The folder name is in English (`repositories`) for compatibility with git and development tools
- Subfolders are created inside for each attached repository
- **Regular local folders are forbidden** — first-level directories inside `repositories/` are allowed only as submodules
- Any new repository is added only via `git submodule add ...`
- Any change to the `repositories/` composition must be accompanied by a coordinated change to `.gitmodules`

**Working with submodules**:
- Add: `git submodule add <url> repositories/<name>`
- Update: `git submodule update --remote repositories/<name>`
- Clone a project with submodules: `git clone --recurse-submodules <url>`
- Initialize after cloning: `git submodule update --init --recursive`

**Project code lives in a submodule, not in the vault** (important for analysis and reports):

- The current vault the agent operates in is the **team instance** of vAIbe-OS at vaibe-studio (management: tasks, meetings, plans, knowledge). It is **not** the product's source code.
- For a project `Проекты/{NAME}/` that has a same-named submodule `repositories/{NAME}`, the **code and product artifacts** (README, LICENSE, CONTRIBUTING, CI, releases) are in the submodule. The vault holds only the management layer.
- When a task or question says "project code", "repository root", "apply to the repository", "currency with the code" — look **in `repositories/{NAME}`**, its git history and remotes, **not** in the instance root.
- **Special case — vAIbe-OS itself (self-hosting)**: the vAIbe-OS product lives in `repositories/vaibe-os` (public remote `open-source` → `github.com/vaibe-studio/vaibe-os`). The current vault root is merely an instance of this product; don't confuse instance with product when assessing the status of tasks from `Проекты/vAIbe-OS/`.

### Inbox
**Path**: `Инбокс/`

- The inbox is a temporary folder for files imported from external systems
- The user adds files of various formats to the inbox: screenshots, meeting transcripts, copies of materials from personal knowledge bases, other files from external sources
- **IMPORTANT**: Files from the inbox must be imported into the OS directory structure
- After import, files are deleted from the inbox or moved to archive

**Import rules**:
- Use the inbox-processing skill to handle files from `Инбокс/`
- The skill asks the user for context about each file
- Files are imported into the appropriate directories per the OS structure:
  - Project materials → `Проекты/{NAME}/`
  - User materials → `База знаний/`
  - Task documentation → `Проекты/{NAME}/Задачи/{NUM}-{TITLE}/`
- After import, files are renamed per the OS naming rules

## Naming rules

1. **All folder and file names in Russian** (except `.vaibe/`, `repositories/`, system `.md` files)
2. **Folders**: capitalize the first letters of words (PascalCase for Russian names)
3. **Files**: capitalize the first letters of words in file names
4. **Task numbers**: use a leading-zeros format (001, 002, 010, 100)
5. **CASE-ONLY RENAMES ARE FORBIDDEN** for a folder/file name (e.g. `vAIbe-os` → `vAIbe-OS`). This creates unresolvable conflicts between Linux (case-sensitive) and Windows (case-insensitive). When needed — rename via an intermediate name in two commits. See: `.vaibe/rules/git-cross-platform.md`
6. **Do not use characters invalid on Windows** in folder and file names (`< > : " / \ | ? *` and control characters). Otherwise cloning and working with the repository on Windows break, even though the name may exist on Linux. A typical mistake is a colon in a meeting title. See: **Rule 8** in `.vaibe/rules/git-cross-platform.md`
7. **Canon slot names in Latin** — folders/files inside `.vaibe/` (skills, rules, scripts) are in Latin (slug); this is a legitimate exception to "Russian vault names".
8. **Ecosystem products**: the `vAIbe-{product}` format. See: `.vaibe/rules/naming-convention.md`

## Full example structure

```
vaibe-os/
├── AGENTS.md                    # Generated thin index of rules for AI agents
├── CLAUDE.md                    # @AGENTS.md (shim for Claude Code)
├── .vaibe/                      # Canon: rules, skills, agents, scripts (IDE-independent)
│   ├── rules/                   # Canonical rules (including ontology.md, manifesto.md)
│   ├── skills/                  # Agent Skills ({name}/SKILL.md)
│   ├── agents/                  # Subagent registry (placeholder)
│   └── scripts/                 # Cross-skill utilities (uv / PEP 723)
├── .claude/ .cursor/ .codex/ .opencode/   # Generated native layer (GENERATED)
├── Проекты/                     # User projects
│   ├── AGENTS.md                # Rules for the tasks/projects layer (task.md format, versioning)
│   └── Мой Проект/
│       ├── README.md
│       ├── Задачи/
│       ├── Встречи/
│       ├── Исходные материалы/
│       ├── База знаний/
│       └── Планы/               # (optional)
├── Контакты/                    # Single source of truth for people
├── База знаний/                 # User knowledge (Личное/ excluded from Git)
├── Инбокс/                      # Incoming files for import
└── repositories/                # Git submodules with code
```

## Important notes

- **Strictly follow the folder structure** — this is critical for the system to work
- **Use Russian** for folder and file names in the vault (exception — the contents of `.vaibe/`)
- **Task numbers must be unique** within a project
- **When creating new projects or tasks** always follow this structure
- **New knowledge** is added as Agent Skills in `.vaibe/skills/` (actionable) or as reference skills / `{skill}/references/` (reference)
- **Files from the inbox must be processed** by the inbox-processing skill and imported into the OS structure
