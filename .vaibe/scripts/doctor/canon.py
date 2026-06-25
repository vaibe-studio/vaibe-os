"""Canon loader for doctor — reads the source of truth in `.vaibe/`.

The canon is the single source of truth (model A): skills live in
`.vaibe/skills/{name}/SKILL.md`, subagents in `.vaibe/agents/{name}.md`, and the
hand-written rule index in `AGENTS.md` (root + nested). Emitters (emitters.py)
turn this into the per-tool native layer; this module only *reads*.

Stdlib only — no external YAML dep. Canon frontmatter is flat
(`name`/`description`/`license`), so a minimal parser is enough; nested keys
(e.g. `metadata:`) are intentionally ignored here because the canon does not use
them. Descriptions may contain `:` — values are split on the first `:` only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# Directories never scanned for AGENTS.md shims: git internals, git submodules
# (`repositories/` holds submodules only — rule git-cross-platform), tool deps.
_SKIP_DIRS = {".git", "node_modules", "repositories", ".venv", "__pycache__"}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split a markdown file into (flat frontmatter dict, body).

    Returns ({}, text) when there is no `---` delimited frontmatter. Indented
    (nested) lines inside the frontmatter are skipped — the canon is flat.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line[:1] in (" ", "\t"):
            continue  # blank or nested — ignore
        key, sep, value = line.partition(":")
        if sep:
            fm[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1 :])
    return fm, body


@dataclass
class Skill:
    name: str          # == folder name, latin slug
    description: str
    license: str | None
    body: str          # full instructions (the only place logic lives)
    source: str        # canon-relative path, e.g. .vaibe/skills/foo/SKILL.md


@dataclass
class Agent:
    name: str
    description: str
    body: str
    source: str               # e.g. .vaibe/agents/architect.md
    # Capability hints — canon carries the superset; emitters map per tool and
    # drop what a tool does not support (§2.0). `tools` is a Claude-style
    # allowlist string; `readonly` flags a non-writing agent (→ Cursor readonly).
    tools: str | None = None
    readonly: bool = False


@dataclass
class Canon:
    root: Path
    skills: list[Skill] = field(default_factory=list)
    agents: list[Agent] = field(default_factory=list)
    agents_md_dirs: list[str] = field(default_factory=list)  # dirs holding AGENTS.md


def load_skills(root: Path) -> list[Skill]:
    base = root / ".vaibe" / "skills"
    out: list[Skill] = []
    for skill_md in sorted(base.glob("*/SKILL.md")):
        fm, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", skill_md.parent.name)
        out.append(
            Skill(
                name=name,
                description=fm.get("description", ""),
                license=fm.get("license"),
                body=body,
                source=f".vaibe/skills/{name}/SKILL.md",
            )
        )
    return out


def load_agents(root: Path) -> list[Agent]:
    base = root / ".vaibe" / "agents"
    out: list[Agent] = []
    for agent_md in sorted(base.glob("*.md")):
        fm, body = parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        name = fm.get("name", agent_md.stem)
        out.append(
            Agent(
                name=name,
                description=fm.get("description", ""),
                body=body,
                source=f".vaibe/agents/{name}.md",
                tools=fm.get("tools"),
                readonly=fm.get("readonly", "").lower() == "true",
            )
        )
    return out


def find_agents_md_dirs(root: Path) -> list[str]:
    """Vault-relative dirs that hold an AGENTS.md (root reported as "")."""
    out: list[str] = []
    for agents_md in root.rglob("AGENTS.md"):
        rel_parts = agents_md.relative_to(root).parts
        if any(p in _SKIP_DIRS for p in rel_parts[:-1]):
            continue
        rel_dir = str(agents_md.parent.relative_to(root))
        out.append("" if rel_dir == "." else rel_dir)
    return sorted(out)


def load_canon(root: Path) -> Canon:
    return Canon(
        root=root,
        skills=load_skills(root),
        agents=load_agents(root),
        agents_md_dirs=find_agents_md_dirs(root),
    )
