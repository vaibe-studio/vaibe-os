---
name: script-automation
description: Design and build automation scripts with quality standards. Triggers: script, automation, tool, utility, automate, extract, convert.
license: MIT
---

# Purpose

Create reliable, reusable automation scripts following consistent design principles and quality standards.

# When to use

- Building a new automation tool or utility
- Processing/converting documents (PDF, DOCX, etc.)
- Creating reusable modules for workflows
- Integrating with external APIs or CLI tools

# Procedure

## Step 1 — Design

Follow these principles:
1. **Modularity** — separate functionality into independent components
2. **Reusability** — use parameters, configs, explicit inputs/outputs
3. **Fault tolerance** — graceful degradation on errors
4. **Documentation** — README, docstrings, usage examples

## Step 2 — Structure the tool

Each tool is a **self-contained `uv` project** — a directory with its own `pyproject.toml`, even for a single file. No `requirements.txt`, no manual venv (see `.vaibe/rules/scripts.md`):

```
tool_name/
├── pyproject.toml      # [project] metadata + dependencies (no build-system)
├── main.py             # entry point
├── README.md           # documentation + examples
└── tests/              # tests (optional for MVP)
```

```toml
[project]
name = "tool-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["markdown", "weasyprint"]
```

A virtual project (`[project]` only, no `[build-system]`). Heavy/optional deps go in `[project.optional-dependencies]`. Run via `uv run --project <dir> <dir>/main.py [args]`; `uv` resolves deps into the project's `.venv` once and reuses it. PEP 723 inline metadata is only for throwaway one-liners, not bundled tools.

## Step 3 — Implement with error handling

- Log errors with context
- Provide fallback mechanisms (e.g., OCR if text extraction fails)
- Return clear user-facing error messages
- Use correct exit codes

## Step 4 — Document

- README.md with description and a reproducible `uv run --project …` example
- `pyproject.toml` with `[project]` dependencies (not `requirements.txt`, not PEP 723)
- Docstrings in key functions
- Type hints where appropriate

## Step 5 — Quality checklist

**Functionality:**
- [ ] Script performs its stated function
- [ ] Edge cases handled
- [ ] Fallback mechanisms present

**Code:**
- [ ] Readable and documented
- [ ] Follows PEP 8 (Python)
- [ ] Type hints used where appropriate

**Documentation:**
- [ ] README.md with description and examples
- [ ] `pyproject.toml` with `[project]` deps present (no `requirements.txt`, no PEP 723)
- [ ] Key functions have docstrings

**Integration:**
- [ ] Run instructions are clear (single `uv run --project …` command)
- [ ] Usage examples are reproducible

# Output format

- Working script in `.vaibe/scripts/{tool_name}/` (cross-skill) or `.vaibe/skills/{skill}/scripts/{tool_name}/`
- README.md with a reproducible `uv run --project …` example
- Dependencies declared in `pyproject.toml` (no `requirements.txt`, no PEP 723)

# Quality bar

- [ ] All checklist items from Step 5 pass
- [ ] Script runs successfully on target platform
- [ ] Error handling tested with invalid inputs
- [ ] Documentation sufficient for independent use

# Anti-patterns

- No error handling (script crashes on unexpected input)
- Using `requirements.txt` / `python -m venv` + `pip`, or a `python -m package` (`__main__.py`) layout, instead of a `uv` project with `pyproject.toml`
- No README or usage examples
- Monolithic script without modular structure
- Hardcoded paths or credentials

# Related knowledge

- `.vaibe/skills/devops-practices/SKILL.md` — CI/CD integration, IaC patterns, DevSecOps for secure automation
- `.vaibe/skills/software-architecture-patterns/SKILL.md` — modular design patterns, API design for script interfaces
- `.vaibe/skills/tech-stack-reference/SKILL.md` — project tech stack (Python, Docker) for tool selection
