# PowerShell: command compatibility on Windows

Goal: avoid recurring errors when running shell commands in the PowerShell (Windows) environment.

> The rule is tool-agnostic: "native IDE file tools" means your tool's Read / Write / Edit / Delete / Glob / Grep (Cursor, Claude Code, OpenCode, Codex). They work with files directly, bypassing the shell, and are therefore safe for Cyrillic.

## Detecting the environment

If the environment reports `Shell: powershell` or `OS Version: win32` — all commands run in PowerShell. Apply the rules below.

## Forbidden constructs

| Construct | Why it breaks | What to use |
|-------------|----------------|-----------------|
| `<<'EOF' ... EOF` (heredoc) | PowerShell does not support bash heredocs | Write the text to a file → use the file |
| `&&` (command chaining) | Doesn't work in PowerShell < 7 | Run commands as **separate Shell calls** |
| `-m "long Russian text with (parens)"` | PS interprets `(...)` as a subexpression, Cyrillic may break the parser | Use `git commit -F <file>` |
| `$(command)` inside strings | PS substitutes its own variables / expressions | Avoid; use intermediate files |

## Git commit with Russian text (recommended pattern)

### Step 1: write the message to a file

Use the native **Write** tool (not echo/heredoc) to create a temporary file:

```
Path: .commit_msg.tmp
Content: the commit message text (any length, any characters)
```

### Step 2: staging (separate Shell call)

```powershell
git add "path/to/files/"
```

### Step 3: commit (separate Shell call)

```powershell
git commit -F .commit_msg.tmp
```

### Step 4: verify + cleanup (separate Shell call)

```powershell
git status
```

After a successful commit, delete `.commit_msg.tmp` via the native **Delete** tool.

## Cyrillic paths: file operations (CRITICALLY IMPORTANT)

**Root cause**: the Shell tool saves commands to a temporary `.ps1` file. Cyrillic characters in paths get garbled when written (double-encoding / Mojibake). This affects **all** shell commands: `copy`, `Copy-Item`, `move`, `Move-Item`, `python shutil.copy(plain_text)`, `cmd /c copy`, etc.

### What works and what does NOT

| Operation | Cyrillic as plain text | Unicode escapes in Python |
|----------|:------------------------:|:------------------------:|
| `Copy-Item` / `copy` | ❌ | — |
| `Move-Item` / `move` | ❌ | — |
| `cmd /c copy` | ❌ | — |
| `python shutil.copy2()` | ❌ | ✅ `\uXXXX` |
| `python shutil.move()` | ❌ | ✅ `\uXXXX` |
| `python os.makedirs()` | ❌ | ✅ `\uXXXX` |
| `mkdir` (PowerShell) | ❌ (may create junk folders) | — |
| `git add` | ❌ (often) | ✅ via `subprocess` |
| Native Read / Write / Delete | ✅ (natively) | — |
| Native Glob / Grep | ⚠️ unreliable (see `.vaibe/rules/discovery.md`) | — |

> The full rules for verifying search results (Glob/Grep may miss Cyrillic-named files, ignore-aware false-negatives, high-risk zones `*Личное*`/`_Архив`/`Инбокс/`) — in `.vaibe/rules/discovery.md`. Below — only the Windows specifics of file operations.

### Choosing the method by operation type

#### Copying / moving files → Python shutil (PRIORITY 1)

> **CRITICAL**: do NOT use Read + Write to copy/move files!
> Read + Write forces the AI to pass the whole content through itself — for a 1000+ line file that's minutes of waiting, token cost, and the risk of accidental changes.

**Copy a file** (1 second, the file is copied directly on disk):

```python
python -c "import shutil, os; shutil.copy2(os.path.join(root, 'Инбокс', 'file.md'), os.path.join(root, 'Проекты', 'Альфа', 'Встречи', 'dest.md'))"
```

**Move a file** (1 second):

```python
python -c "import shutil, os; shutil.move(os.path.join(root, 'Инбокс', 'file.md'), os.path.join(root, 'Проекты', 'dest.md'))"
```

**Create a directory**:

```python
python -c "import os; os.makedirs(os.path.join(root, 'Проекты', 'Альфа', 'Встречи', 'New Folder'), exist_ok=True)"
```

**Git add**:

```python
python -c "import subprocess; subprocess.run(['git', 'add', '--', 'Проекты/Альфа/README.md'])"
```

#### Creating new files, editing, reading content → native tools

The IDE's native file tools work with Cyrillic directly and are ideal when you need access to **content**:

- **Create a new file** (summary.md, tasks.md): `Write`
- **Read for analysis**: `Read`
- **Edit**: `Edit`
- **Delete**: `Delete`
- **Search**: `Glob` / `Grep` (⚠️ unreliable for Cyrillic paths — see `.vaibe/rules/discovery.md`)

> **Rule**: `Read` + `Write` for "copying" — only if the file is SMALL (< 50 lines) and you need to read it in the same flow. For everything else — Python shutil.

#### Creating directories → no mkdir needed

The **Write** tool automatically creates all intermediate directories when writing a file. To create a task or any folder structure, just call `Write` on the target file — `mkdir` is not needed at all.

> **DANGER**: `cmd /c mkdir` with a Cyrillic path may **partially execute** even on error, leaving a "phantom" folder with a truncated name. Such a folder has no files but clutters the explorer.

#### NEVER use

- `Copy-Item` / `copy` / `Move-Item` / `move` with Cyrillic paths in Shell
- `cmd /c` with Cyrillic paths (including `cmd /c mkdir` — even on error it may create a junk directory)
- `mkdir` via Shell for Cyrillic paths (use `Write` or Python `os.makedirs` with Unicode escapes)
- Attempts to "fix" encoding (`chcp 65001`, `$OutputEncoding`) — they **do NOT help for writing** (`Copy-Item`, `Move-Item`)
- **BUT**: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8;` **DOES help for reading** (`Get-ChildItem`, `Select-String`, pipelines with Cyrillic output). Add it at the start of commands that **read** or **list** files with Cyrillic names
- **Get-Content** for UTF-8 files: always add `-Encoding UTF8`, otherwise Cyrillic inside the file becomes mojibake (PS reads as Windows-1251 by default)
- **Python via Shell**: always set `$env:PYTHONIOENCODING = 'utf-8'; $env:PYTHONUTF8 = '1'` before invoking Python, otherwise `print()` with Cyrillic outputs garbage
- `Read` + `Write` to copy large files (> 50 lines) — slow, costly, risky

### Unicode-escape reference for common Russian words in the project

When a path has to be passed to Python via Shell, it's safer to write Cyrillic as Unicode escapes:

| Word | Unicode escape |
|-------|----------------|
| Проекты | `\u041f\u0440\u043e\u0435\u043a\u0442\u044b` |
| Задачи | `\u0417\u0430\u0434\u0430\u0447\u0438` |
| Встречи | `\u0412\u0441\u0442\u0440\u0435\u0447\u0438` |
| Роли | `\u0420\u043e\u043b\u0438` |
| Инбокс | `\u0418\u043d\u0431\u043e\u043a\u0441` |
| База знаний | `\u0411\u0430\u0437\u0430 \u0437\u043d\u0430\u043d\u0438\u0439` |
| Исходные материалы | `\u0418\u0441\u0445\u043e\u0434\u043d\u044b\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b` |
| Планы | `\u041f\u043b\u0430\u043d\u044b` |
| Встреча | `\u0412\u0441\u0442\u0440\u0435\u0447\u0430` |
| Обсуждение | `\u041e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u0435` |

## General rules for Shell calls on Windows

1. **One command = one Shell call.** Don't chain via `&&`, `;`, `|` with side effects.
2. **Cyrillic in paths** — NEVER pass it as plain text to shell commands for file operations. Use native tools (Read/Write/Delete) or Python with Unicode escapes (see the section above).
3. **Staging is lost between Shell calls** — check via `git status` before committing; if lost — repeat `git add`.
4. **Don't use bash-isms**: `export`, `source`, `cat <<`, `$(...)`, `${}`.
5. **Cyrillic paths break in git** — the Windows console (CP866) garbles UTF-8 paths. If `git add`/`git hash-object` can't find a Cyrillic file, use Python: `subprocess.run(['git', 'add', '--', 'Path/...'])` with Unicode escapes.
6. **Git quotepath** — `.git/config` must have `core.quotepath = false`, otherwise `git status`/`git log` show Cyrillic paths as octal escapes. Already set in this repository.
7. **Phantom modified files** — if `git status` shows modified, `git diff` is empty, and `git add` doesn't help — it's a case conflict in names (Windows case-insensitive, Linux case-sensitive). See `.vaibe/rules/git-cross-platform.md`.

## Deleting directories in PowerShell (common mistake)

- `rmdir /s /q ...` is **cmd-style**. In PowerShell `rmdir` is an alias for `Remove-Item`, and flags like `/s /q` break the command.
- Use:

```powershell
Remove-Item -Recurse -Force ".tmp\\some-folder"
```

> Note: for Cyrillic paths the rules above apply (prefer native tools or Python with Unicode escapes).

## Hygiene: preventing junk folders

Shell commands with Cyrillic paths on Windows are the main source of "phantom" directories. Junk folders arise two ways:

1. **Fragmentation**: `cmd /c mkdir "path with spaces"` on an encoding failure interprets spaces as path separators, creating a separate folder per word
2. **Double-encoding**: shell commands write UTF-8 bytes as CP1252/CP866, creating folders with mojibake names instead of normal Cyrillic ones

### Prevention rules

1. **Creating files and folders** — ONLY via `Write` (auto-creates all parent directories) or Python `os.makedirs()` with Unicode escapes. NEVER via `mkdir`, `md`, `New-Item` in the shell.
2. **Creating empty folders** — via `Write` with a `.gitkeep` file inside.
3. **After any file operations via Shell** — visually check that no extra folders appeared in the explorer or via the Python script below.
4. **If junk folders are found** — delete via Python `shutil.rmtree()` with Unicode escapes, after confirming the folder is empty (0 files).

### Check script (run when junk is suspected)

```python
python -c "import os; root=os.getcwd(); known={'.vaibe','.claude','.cursor','.codex','.opencode','.git','.tmp','.venv','.vscode','repositories','Проекты','База знаний','Контакты','Инбокс'}; [print(f'UNKNOWN [{sum(1 for _,_,f in os.walk(os.path.join(root,d)) for _ in f)} files]: {d}') for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root,d)) and d not in known]"
```

## Exporting a finished result to PDF (recommended path)

If the user asks for an artifact in PDF format, **do not use** a headless browser / external engines.

The canon has a converter script: `.vaibe/scripts/markdown_to_pdf/` (a `uv` project — `pyproject.toml`).

Recipe:
1) Create/update the Markdown file with native tools (in the task's `results/` folder).
2) Generate the PDF via `uv`:

```powershell
uv run --project .vaibe/scripts/markdown_to_pdf .vaibe/scripts/markdown_to_pdf/main.py "input.md" -o "output.pdf"
```

Pros:
- doesn't require `pandoc`/LaTeX/wkhtmltopdf
- correct Cyrillic (via system Windows fonts)
- dependencies resolved by `uv` from the project's `pyproject.toml`, without a separate `requirements.txt`
