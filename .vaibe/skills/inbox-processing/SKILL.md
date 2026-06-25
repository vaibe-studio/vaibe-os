---
name: inbox-processing
description: Interactively process and import files from Inbox into vAIbe-OS directory structure. Triggers: inbox, import, inbox-check, разобрать инбокс.
license: MIT
---

# Purpose

Process files in `Инбокс/`, interactively determine their destination, and import them into the vAIbe-OS directory structure with proper naming and organization.

# When to use

- User triggers `/inbox-check`
- New files appear in `Инбокс/`
- After receiving external materials that need organizing

# Inputs needed

- `Инбокс/` — files and folders to process
- `Проекты/` — existing project list for classification
- `.vaibe/rules/structure.md` — naming and structure rules

# Procedure

## Step 1 — Scan Inbox

- List all files in `Инбокс/` (exclude `.gitkeep`, `.gitignore`, `README.md`)
- For each file: name, type, size, date
- Group related files (e.g., all meetings, all materials for one project)
- If empty → inform user and stop

**Scanning method (critical):** `Инбокс/.gitignore` contains `*` to prevent committing user files to git. This blocks the Glob tool (it respects `.gitignore`). Use one of these instead:

```python
# Option 1 (preferred): Python os.listdir via shell
python -c "import os; [print(f) for f in os.listdir(os.path.join('c:\\vaibe-os-adr\\ai-os', '\u0418\u043d\u0431\u043e\u043a\u0441')) if f not in ('.gitkeep','.gitignore','README.md')]"
```

```powershell
# Option 2: PowerShell with -Name flag
Get-ChildItem "Инбокс" -Name | Where-Object { $_ -notin '.gitkeep','.gitignore','README.md' }
```

Do NOT use the Glob tool for `Инбокс/`.

## Step 2 — Choose processing mode

Ask user:

| Mode | Behavior |
|---|---|
| **Step-by-step** (default) | Full question cycle per file |
| **Grouped** | Questions per logical group, details for ambiguous items |
| **Quick** | Single import plan for all items, one confirmation |
| **Delegated** (explicit permission only) | Agent decides per rules, log shown at end |

**STOP — wait for mode selection.**

## Step 3 — Process each file/group (interactive loop)

For each item:

### 3a. Analyze content
- Read file content (if possible)
- Classify: meeting transcript / project doc / knowledge base / screenshot / other
- Formulate hypothesis about destination (do NOT decide)

### 3b. Ask user (mandatory)

Present:
- File name, type, content summary
- Hypothesis about destination

Ask:
- Which project? (or "not project-related")
- Material type: meeting / task / source material / knowledge base / other
- Proposed name — agree or suggest own?
- Additional context? (optional)

**For knowledge base materials, additionally assess:**
- Universality (high/medium/low)
- Project-specific context (yes/no)
- Reusability across projects
- Visibility: general (tracked in Git) or personal (`База знаний/Личное/`, excluded from Git)
- Recommend placement: general KB / personal KB / project KB / both general + project

**STOP — wait for user response.**

### 3c. Determine target directory

Based on user response:
- Project materials → `Проекты/{PROJECT}/Исходные материалы/` or subfolders
- Meeting → `Проекты/{PROJECT}/Встречи/Встреча {N}. {DD.MM.YYYY} - {TITLE}/`
- Task → `Проекты/{PROJECT}/Задачи/{NUM}-{TITLE}/`
- Project KB → `Проекты/{PROJECT}/База знаний/`
- General KB → `База знаний/`
- Personal KB → `База знаний/Личное/` (excluded from Git)
- PDF → original to source materials + extracted Markdown alongside

### 3d. Confirm import plan

Show:
- Source path
- Target directory
- New file name
- Additional actions (conversion, extraction)

**STOP — wait for confirmation.**

### 3e. Execute import

After confirmation:
- Create target directories if needed
- Move/rename file per naming rules (Russian, capitalized words)
- Convert to Markdown if needed
- For PDFs: extract text using `.vaibe/scripts/pdf_to_markdown/`

### 3f. Handle uncertain items

If item can't be properly classified:
- Document reason
- Move to `Инбокс/Отложено/`
- Return to it in a separate `/inbox-check` session

## Step 4 — Summary

Show:
- Imported files with paths
- Skipped/deferred files
- Suggested next steps

# Output format

- Files moved to correct directories with proper names
- Import log (source → destination for each file)

# Quality bar

- [ ] Every file's destination confirmed by user before import
- [ ] File names follow Russian naming conventions
- [ ] PDFs have extracted Markdown alongside
- [ ] Knowledge base materials assessed for universality
- [ ] No files imported without confirmation (even in delegated mode — batch confirmation)

# Anti-patterns

- Mass import without asking about each file/group
- Single generic question for all files
- Treating hypothesis as decision (importing without confirmation)
- Skipping universality assessment for knowledge base materials
