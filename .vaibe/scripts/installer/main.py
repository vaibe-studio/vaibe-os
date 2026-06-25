#!/usr/bin/env python3
"""
vAIbe-OS Installer — TUI for initial setup.

Usage:
    uv run --project .vaibe/scripts/installer .vaibe/scripts/installer/main.py

Stdlib only — no external dependencies (uv just resolves the empty dependency set).
"""

import os
import sys
from pathlib import Path

# .vaibe/scripts/installer/main.py → repo root is four levels up.
REPO_ROOT = Path(__file__).resolve().parents[3]

AGENTS = [
    ("cursor", "Cursor"),
    ("claude", "Claude Code"),
    ("codex", "Codex"),
    ("opencode", "OpenCode"),
    ("other", "Other (AGENTS.md only)"),
]

USER_DIRS = ["Проекты", "База знаний", "Инбокс", "Контакты"]

BANNER = r"""
╔══════════════════════════════════════╗
║        vAIbe-OS Installer            ║
╚══════════════════════════════════════╝
"""

AGENT_DESCRIPTIONS = {
    "cursor": "Full support: generated .cursor/ skills, rules, agents",
    "claude": "Supported via CLAUDE.md + generated .claude/ skills",
    "codex": "Supported via generated .codex/ skills + AGENTS.md",
    "opencode": "Supported via AGENTS.md + generated .opencode/ skills",
    "other": "Basic support: AGENTS.md + .vaibe/ canon",
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(BANNER)


def select_agent() -> tuple:
    print("  Select your AI agent:\n")
    for i, (key, label) in enumerate(AGENTS, 1):
        desc = AGENT_DESCRIPTIONS[key]
        print(f"    {i}. {label}")
        print(f"       {desc}\n")

    n = len(AGENTS)
    while True:
        try:
            choice = input(f"  Enter number (1-{n}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < n:
                key, label = AGENTS[idx]
                print(f"\n  → Selected: {label}\n")
                return key, label
        except (ValueError, EOFError):
            pass
        print(f"  Invalid choice. Please enter 1-{n}.")


def get_user_info() -> tuple:
    print("  ─── About you ───\n")

    while True:
        name = input("  Your name: ").strip()
        if name:
            break
        print("  Name cannot be empty.")

    while True:
        occupation = input("  What you do (e.g. developer, designer, PM): ").strip()
        if occupation:
            break
        print("  Please describe what you do.")

    print()
    return name, occupation


def confirm(agent_label: str, name: str, occupation: str) -> bool:
    print("  ─── Configuration ───\n")
    print(f"  Agent:      {agent_label}")
    print(f"  Name:       {name}")
    print(f"  Occupation: {occupation}")
    print()

    while True:
        answer = input("  Proceed with installation? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please enter y or n.")


def create_directories():
    print("\n  Creating directories...")
    for dirname in USER_DIRS:
        dirpath = REPO_ROOT / dirname
        dirpath.mkdir(exist_ok=True)
        gitkeep = dirpath / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        print(f"    ✓ {dirname}/")


def verify_agent_config(agent_key: str):
    print("  Verifying agent configuration...")

    checks = {
        "cursor": [
            ("AGENTS.md", "AGENTS.md (rule spine)"),
            (".vaibe/skills", "Canon skills"),
            (".cursor/skills", "Cursor skills (generated)"),
            (".cursor/agents", "Cursor agents (generated)"),
        ],
        "claude": [
            ("CLAUDE.md", "CLAUDE.md (generated shim)"),
            (".vaibe/skills", "Canon skills"),
            (".claude/skills", "Claude skills (generated)"),
        ],
        "codex": [
            ("AGENTS.md", "AGENTS.md (rule spine)"),
            (".vaibe/skills", "Canon skills"),
            (".codex/skills", "Codex skills (generated)"),
        ],
        "opencode": [
            ("AGENTS.md", "AGENTS.md (rule spine)"),
            (".vaibe/skills", "Canon skills"),
            (".opencode/skills", "OpenCode skills (generated)"),
        ],
        "other": [
            ("AGENTS.md", "AGENTS.md (rule spine)"),
            (".vaibe/skills", "Canon skills"),
        ],
    }

    for relpath, label in checks.get(agent_key, []):
        fullpath = REPO_ROOT / relpath
        exists = fullpath.exists()
        status = "✓" if exists else "✗"
        print(f"    {status} {label} ({relpath})")


def print_next_steps(agent_key: str, agent_label: str):
    print("\n  ══════════════════════════════════════")
    print("  ✓ Installation complete!")
    print("  ══════════════════════════════════════\n")
    print(f"  Agent: {agent_label}\n")
    print("  What to try first:\n")

    if agent_key == "cursor":
        print('    1. Open this folder in Cursor')
        print('    2. Ask: "Create a task for my project"  (uses /task-create)')
        print('    3. Drop a file into Инбокс/ and ask: "Process my inbox"')
        print('    4. After a session, ask: "Evolve the system"  (uses /evolve)')
    elif agent_key == "claude":
        print("    1. Open this folder in your terminal")
        print("    2. Run: claude")
        print('    3. Ask: "Create a task for my project"')
        print('    4. Drop a file into Инбокс/ and ask: "Process my inbox"')
    elif agent_key == "codex":
        print("    1. Open this folder in your terminal")
        print("    2. Run: codex")
        print('    3. Ask: "Create a task for my project"')
        print('    4. Drop a file into Инбокс/ and ask: "Process my inbox"')
    elif agent_key == "opencode":
        print("    1. Open this folder in your terminal")
        print("    2. Run: opencode")
        print('    3. Ask: "Create a task for my project"')
    else:
        print("    1. Open this folder in your AI IDE")
        print("    2. Point your agent to AGENTS.md")
        print("    3. Skills are auto-discovered from .vaibe/skills/ by description")

    print()
    print("  Key files:")
    print("    README.md          — documentation")
    print("    AGENTS.md          — the rule spine your agent reads first")
    print("    .vaibe/skills/     — 47 skills (auto-discovered by description)")
    print("    .vaibe/rules/      — always-on rules (structure, git, behavior, guards)")
    print()


def main():
    clear_screen()
    print_banner()

    agent_key, agent_label = select_agent()
    name, occupation = get_user_info()

    if not confirm(agent_label, name, occupation):
        print("\n  Installation cancelled.")
        sys.exit(0)

    create_directories()
    verify_agent_config(agent_key)
    print_next_steps(agent_key, agent_label)


if __name__ == "__main__":
    main()
