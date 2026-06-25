# vAIbe-OS Installer

TUI-based installer for initial vAIbe-OS setup.

## Usage

```bash
python tools/installer/install.py
```

## What it does

1. Asks user to select an AI agent (Cursor, Claude Code, Codex, OpenCode)
2. Collects user name and occupation
3. Creates user directories (`Проекты/`, `База знаний/`, `Инбокс/`, `Контакты/`)
4. Verifies the canon (`.vaibe/`) and the agent's generated native layer are present
5. Shows next steps

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
