# Scripts: reusing and creating utilities

Goal: reduce system "cognitive degradation" and avoid spawning duplicate scripts. The canonical runner is **`uv`**. Each bundled script is a **self-contained `uv` project** with its own `pyproject.toml`; **PEP 723** inline metadata is reserved for throwaway one-liners only (see below).

## Where scripts live

| Location | Purpose |
|---|---|
| `.vaibe/scripts/{tool}/` | Cross-skill utilities (used by multiple skills or outside skills) |
| `.vaibe/skills/{skill}/scripts/{tool}/` | Scripts specific to a single skill |

## Core rule: reuse-before-create

Before you:
- write a new script;
- suggest the user "do it by hand" for a repeatable operation;
- add a new `.vaibe/scripts/<name>/...`;

first **check** whether a ready solution already exists:
- in `.vaibe/scripts/` (cross-skill) — search by names and descriptions;
- in the `{skill}/scripts/` of the skill you are executing.

## If a suitable tool already exists

- **Reuse** the existing tool.
- If needed — **extend** it (add an option/mode), rather than creating a new "almost identical" one.

## Standard: one `uv` project per script

Every script under a `scripts/` directory is its **own `uv` project** — a directory with a `pyproject.toml`, **even if it contains a single `.py` file**. This gives each tool an isolated, reproducible dependency set without a global `requirements.txt` or a manual virtual environment.

```
tool_name/
├── pyproject.toml      # [project] metadata + dependencies (no build-system)
├── main.py             # entry point
├── README.md           # purpose + a reproducible `uv run` example
└── (other modules).py  # for multi-file tools
```

`pyproject.toml` is a **virtual project** — `[project]` only, **no `[build-system]`** and **no `[project.scripts]`** (a flat single-file layout has nothing to build; `uv` just resolves the declared dependencies into the project's `.venv`):

```toml
[project]
name = "tool-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "requests>=2.28.0",
  "python-dotenv>=1.0.0",
]
```

- **Heavy / optional dependencies** (a backend the tool needs only sometimes) go in `[project.optional-dependencies]`, not in the always-installed set:
  ```toml
  [project.optional-dependencies]
  local = ["openai-whisper", "pyannote.audio", "torch", "torchaudio"]
  ```
  Run with the extra via `--extra local`.
- **`uv` creates a `.venv` inside the project on first run** and reuses it afterwards (plus a global wheel cache) — dependencies are resolved once, not on every run. `.venv/` is git-ignored; **`uv.lock` is committed** (regenerate with `uv lock --project <dir>`) — it pins exact versions across platforms, so installs skip resolution and stay reproducible for every contributor.

### Multi-file tools

A tool may span several modules. Do **not** use the `python -m package` layout (`__init__.py` / `__main__.py` with relative imports) — instead give it a `main.py` entry that puts its own directory on `sys.path` and imports siblings **absolutely**:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import converter, formatter   # absolute, not `from .converter import ...`
```

## Running a script (uv-native)

Run with **`--project`** so the script uses its own environment while the **current working directory is preserved** (so relative path arguments still resolve):

```
uv run --project .vaibe/scripts/{tool} .vaibe/scripts/{tool}/main.py [args]
```

- `--project <dir>` selects the tool's `pyproject.toml`/`.venv`; the script path is passed explicitly.
- Do **not** use `--directory` for tools that take file-path arguments — it changes the working directory and breaks relative paths. `--directory` is acceptable only for tools that take no path arguments.

## PEP 723 — only for ad-hoc one-liners

Inline [PEP 723](https://peps.python.org/pep-0723/) metadata (`# /// script ... # ///`) is for **throwaway one-off scripts** you run once with a couple of dependencies and do not keep as a tool:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
```
```
uv run scratch.py
```

Bundled tools in `scripts/` are **not** PEP 723 — they are `uv` projects (above).

## Non-Python script directories

A `scripts/` subdirectory may hold shell (`.sh`/`.bat`) or Node (`.mjs`) helpers rather than a Python tool (e.g. `migrate-remotes/`, `static-banner-kit/`). These are **documented exceptions**: they are not `uv` projects and carry no `pyproject.toml`; run them with their native runner.

## Do not use (legacy of the old `tools/` package)

- `__init__.py` / `__main__.py` (the `python -m tools.X` package layout);
- `requirements.txt` (dependencies go in `pyproject.toml`);
- a shared `TOOLS_INDEX.md` index (script discovery is by directory contents);
- manual `python3 -m venv .venv` + `pip install` (`uv` manages this).

## Command notation (for replies to the user)

Always give **one reproducible command**:

```
uv run --project .vaibe/scripts/markdown_to_pdf .vaibe/scripts/markdown_to_pdf/main.py "input.md" -o "output.pdf"
```

## Related
- Cross-platform run nuances on Windows (encodings, Cyrillic in paths): `.vaibe/rules/powershell.md`
- Verifying search results before concluding "the script does not exist": `.vaibe/rules/discovery.md`
