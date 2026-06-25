# Git: cross-platform work (Windows + Linux)

Goal: prevent sync problems when collaborating from different OSes.

## Context

Contributors work from Windows (NTFS, case-insensitive) and Linux (ext4, case-sensitive). File and directory names contain Cyrillic (UTF-8). This creates two classes of problems: **case conflicts** and **encoding conflicts**.

---

## Rule 1: Single case in names

It is **FORBIDDEN** to create directories/files that differ only by case:
- `vAIbe-OS/` and `vAIbe-os/` — on Linux these are different folders, on Windows the same one
- When renaming a directory (case change) on Linux — the old entry stays in the git index and creates a phantom conflict on Windows

**When renaming with a case change on Linux:**
1. `git mv old-name temp-name` (intermediate name)
2. `git mv temp-name New-Name` (final name)
3. Commit + push
4. On Windows: `git pull` gets a clean rename

**When detecting a conflict on Windows (symptoms: `git status` shows modified, `git add` doesn't help, `git diff` is empty):**
— See the knowledge base: `Проекты/vAIbe-OS/База знаний/Git кросс-платформенная синхронизация.md`

---

## Rule 2: Cyrillic in paths via the Windows console

The Windows console (PowerShell, cmd, Git Bash) passes Cyrillic paths to git incorrectly due to an encoding mismatch (CP866 / Windows-1251 vs UTF-8).

**Symptoms**: `git hash-object "Проекты/..."` → `fatal: could not open 'РџСЂРѕРµРєС‚С‹/...'`

**Solution**: For operations with Cyrillic paths use a **Python wrapper**:

```python
import subprocess
subprocess.run(['git', 'add', '--', 'Проекты/vAIbe-OS/'], capture_output=True)
```

Python passes UTF-8 paths to git correctly through the system APIs.

---

## Rule 3: Git settings for cross-platform work

Recommended settings in `.gitattributes` (repository root):

```
* text=auto
*.md text eol=lf
*.png binary
*.jpg binary
```

This guarantees:
- Text files are always stored with LF in the repository
- Binary files are not converted
- Behavior is identical across all OSes

---

## Rule 4: Diagnosing phantom changes

If `git status` shows modified files that can't be staged:

1. **Check for case duplicates** in the index:
   ```python
   import subprocess
   result = subprocess.run(['git', 'ls-files', '--stage', '-z'], capture_output=True)
   entries = result.stdout.split(b'\0')
   paths = [e.split(b'\t', 1)[1] for e in entries if b'\t' in e]
   # Find pairs that differ only by case
   lower_map = {}
   for p in paths:
       key = p.lower()
       if key in lower_map and lower_map[key] != p:
           print(f"CONFLICT: {lower_map[key]} vs {p}")
       lower_map[key] = p
   ```

2. **Remove the old entries** via `git update-index --force-remove`
3. **Re-add the files** via `git add`

---

## Rule 5: Isolating personal data in shared repositories

The repository is shared. **All work projects are tracked by default.** Personal projects and data: **impersonal** patterns — in the root `.gitignore`; **unique names** — in `.git/info/exclude` (local, not committed).

**File categorization:**

| Category | Examples | Action |
|-----------|---------|----------|
| Canon | `.vaibe/` (rules, skills, agents, scripts) | Commit |
| Generated native layer | `.claude/`, `.cursor/`, `.codex/`, `.opencode/`, root and nested `AGENTS.md`/`CLAUDE.md` | Commit (model A: GENERATED artifacts in the repo; `GENERATED` marker in the header) |
| Work projects | `Проекты/Альфа/`, `Проекты/Бета/`, `Проекты/vAIbe-OS/` | Commit (by default) |
| Personal projects | Folders with `*Личное*` in the path (convention) | Pattern in the root `.gitignore`; otherwise the path in `.git/info/exclude` |
| Knowledge base | `База знаний/` | Commit (except the personal folder `База знаний/Личное/`) |
| Temporary imports | `Инбокс/` | Exclude via `.gitignore` |
| Archives | `Проекты/_Архив/` | Exclude via `.gitignore` |

> **Delivery model A:** the native wrappers for each tool (`.claude/`, `.cursor/`, `.codex/`, `.opencode/`, the `AGENTS.md`/`CLAUDE.md` indexes) are **generated from the `.vaibe/` canon and committed** together with it. These are generated artifacts — they must not be edited by hand (the header carries a `GENERATED — DO NOT EDIT` marker), the source of truth is always `.vaibe/`. Anti-drift (`generated == canon`) rests on a check at build/CI time.

**When creating a new project** (automated in the task-create skill):
- The agent asks for visibility: `командный` / `личный`
- Visibility is recorded in the project `README.md` (the `Видимость:` field)
- `командный` → do nothing, the project is tracked automatically
- `личный` → if the name is not covered by patterns in `.gitignore`, add `/Проекты/{NAME}/` to `.git/info/exclude`

**Commit protocol:**
1. Check `.gitignore` and, if needed, `.git/info/exclude` — personal directories must not enter the commit
2. `git add -u` — stage modifications/deletions of tracked files
3. Selectively add new files (not `git add -A`, not `git add .`)
4. `git status --porcelain` — make sure personal data is not in the staging area
5. Commit

---

## Rule 6: Selective staging of Cyrillic paths

PowerShell garbles Cyrillic paths when passing them to git. To add files with Cyrillic paths use `--pathspec-from-file`:

1. Create a file `.git/paths-to-add.txt` (UTF-8) with a list of paths — one per line
2. Run `git add --pathspec-from-file=.git/paths-to-add.txt`

**Example** `.git/paths-to-add.txt`:
```
Проекты/vAIbe-OS/Задачи/013-Новая задача/task.md
База знаний/Новая заметка/README.md
```

This approach bypasses the PowerShell encoding problem and works reliably with any Unicode paths.

---

## Rule 7: Cleaning up garbled directories (double-encoded UTF-8)

On Windows, directories with "mojibake" — double UTF-8 encoding (e.g. `РџСЂРѕРµРєС‚С‹` instead of `Проекты`) — can appear. These are artifacts of operations with Cyrillic paths via a console with the wrong encoding.

**Diagnostics**: `git ls-files --others --exclude-standard --directory` — garbled directories show up as paths with Р, С, Рѕ, Рё and similar characters.

**Cleanup** via Python (handles Unicode correctly on Windows):
```python
import os, shutil
root = r'c:\path\to\repo'
known = {'Проекты', 'Роли', 'База знаний', ...}
for d in os.listdir(root):
    full = os.path.join(root, d)
    if os.path.isdir(full) and d not in known:
        if any(c in d for c in ['Р', 'С']):
            shutil.rmtree(full)  # garbled directory
```

**Prevention**: Always use a Python wrapper or `--pathspec-from-file` (Rule 6) for git operations with Cyrillic paths.

---

## Rule 8: Characters forbidden in file and folder names (Windows)

In path segment names you **cannot** use characters invalid on Windows (NTFS):  
`< > : " / \ | ? *` and characters with codes 0–31.

**Common case:** a colon `:` in a meeting or task title (e.g. `…бета-релизу: репозиторий…`) — on Linux the folder is created, on Windows clone/pull or working with the path breaks.

**What to do when shaping the vault:**
- In the **folder/file name** replace `:` with a space, hyphen, or dash; or remove the punctuation.
- In **text inside a `.md`** a colon is fine — the restriction is only on the file system name.

**Check (Linux/macOS):** search for paths with `:` in a segment name, e.g. `find … -path '*:*'` over the needed directory.

---

## Related
- PowerShell compatibility: `.vaibe/rules/powershell.md`
- Verifying search results (Cyrillic, ignore-aware): `.vaibe/rules/discovery.md`
- Detailed guide: `Проекты/vAIbe-OS/База знаний/Git кросс-платформенная синхронизация.md`
