# installer — vAIbe-OS first-run setup (TUI)

Interactive first-run setup. Asks which AI agent you use, collects your name and
occupation, scaffolds the user vault directories (`Проекты/`, `База знаний/`,
`Инбокс/`, `Контакты/`), verifies that the canon (`.vaibe/`) and the agent's
generated native layer are present, and prints next steps.

Stdlib only — the `uv` project declares no dependencies; `uv` just provisions an
isolated environment so the tool runs the same way as every other bundled script.

## Run

```
uv run --project .vaibe/scripts/installer .vaibe/scripts/installer/main.py
```

Run it from the repository root (the script resolves the repo root relative to
its own location, four levels up).
