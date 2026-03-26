# vAIbe-OS Installer

TUI-based installer for initial vAIbe-OS setup.

## Usage

```bash
python tools/installer/install.py
```

## What it does

1. Asks user to select an AI agent (Cursor, Claude Code, OpenCode)
2. Collects user name and occupation
3. Creates user directories (`Проекты/`, `База знаний/`, `Инбокс/`)
4. Verifies agent-specific configuration files
5. Shows next steps

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
