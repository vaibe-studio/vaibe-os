"""Emitter matrix for doctor — canon → per-tool native layer (model A).

One emitter per `(tool, type)` pair: each owns the native path, the tool's
frontmatter fields, and the body shape. Bodies are wrappers (marker + imperative
+ reference), never copies of the canon.

⚠ Marker placement follows the *phase-3 empirical layout*, not spec §2.1.x
verbatim (correction to §2/U10): for markdown the `GENERATED — DO NOT EDIT`
marker is an HTML comment placed **below** the frontmatter — a leading comment
breaks YAML parsing in opencode/Claude, and a `#`-comment inside the frontmatter
crashes opencode. For Codex TOML the marker is a `#` line at the very top.

Reference syntax per §2.4: Claude/Cursor use `@.vaibe/…`; opencode/Codex use a
plain path plus the imperative (their `@` is not auto-parsed).

Every emitter returns (vault-relative path, full file content). Output is
byte-for-byte equal to the hand-made phase-3 native layer — proven by `diagnose`
(`check`) and the regression test 4.5 (batch 072).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from canon import Agent, Canon, Skill

TOOLS = ("claude", "cursor", "opencode", "codex")
MD_MARKER = "<!-- GENERATED — DO NOT EDIT. Source: {src} -->"
TOML_MARKER = "# GENERATED — DO NOT EDIT. Source: {src}"


# ──────────────────────────────────────────────────────────────────────────
# Skills — `.{tool}/skills/{name}/SKILL.md`
# ──────────────────────────────────────────────────────────────────────────

def _skill_frontmatter(tool: str, s: Skill) -> str:
    lines = ["---", f"name: {s.name}", f"description: {s.description}"]
    if tool == "cursor":
        lines += ["metadata:", "  origin: vaibe-os"]
    elif tool == "opencode":
        lines += [f"license: {s.license or 'MIT'}", "compatibility: opencode",
                  "metadata:", "  origin: vaibe-os"]
    # claude / codex: name + description only
    lines.append("---")
    return "\n".join(lines)


def _skill_body(tool: str, s: Skill) -> str:
    src = s.source
    if tool in ("claude", "cursor"):
        return (
            f"Load and follow the instructions from the canonical file at `{src}`\n"
            "as if they were written here. Do not act on this wrapper — it holds only metadata; the full\n"
            "skill logic lives in the canon.\n"
            "\n"
            f"@{src}"
        )
    if tool == "opencode":
        return (
            f"Load and follow the instructions from the canonical file at {src}\n"
            "as if they were written here. Do not act on this wrapper — it holds only metadata; the full\n"
            "skill logic lives in the canon.\n"
            "(opencode does not auto-parse @ references — open the file at the path above explicitly.)"
        )
    # codex
    return (
        f"Load and follow the instructions from the canonical file at {src}\n"
        "as if they were written here. Do not act on this wrapper — it holds only metadata; the full\n"
        "skill logic lives in the canon."
    )


def emit_skill(tool: str, s: Skill) -> tuple[str, str]:
    path = f".{tool}/skills/{s.name}/SKILL.md"
    marker = MD_MARKER.format(src=s.source)
    content = f"{_skill_frontmatter(tool, s)}\n\n{marker}\n\n{_skill_body(tool, s)}\n"
    return path, content


# ──────────────────────────────────────────────────────────────────────────
# Agents — `.{claude,cursor,opencode}/agents/{name}.md`, `.codex/agents/{name}.toml`
# ──────────────────────────────────────────────────────────────────────────

def _agent_md_frontmatter(tool: str, a: Agent) -> str:
    if tool == "opencode":
        # opencode subagent: identity from filename, no `name` field (U15).
        # Phase-3 layout carries no permission block, so none is emitted.
        lines = ["---", f"description: {a.description}", "mode: subagent", "---"]
    elif tool == "cursor":
        lines = ["---", f"name: {a.name}", f"description: {a.description}"]
        if a.readonly:
            lines.append("readonly: true")
        lines.append("---")
    else:  # claude — Claude-style tools allowlist (omitted = inherits all)
        lines = ["---", f"name: {a.name}", f"description: {a.description}"]
        if a.tools:
            lines.append(f"tools: {a.tools}")
        lines.append("---")
    return "\n".join(lines)


def _agent_md_body(tool: str, a: Agent) -> str:
    src = a.source
    if tool in ("claude", "cursor"):
        return (
            f"Follow the instructions from the canonical file at `{src}` as if they were\n"
            "written here. Do not act on this wrapper — it holds only metadata; the full agent logic lives\n"
            "in the canon.\n"
            "\n"
            f"@{src}"
        )
    # opencode
    return (
        f"Follow the instructions from the canonical file at {src} as if they were\n"
        "written here. Do not act on this wrapper — it holds only metadata; the full agent logic lives\n"
        "in the canon.\n"
        "(opencode does not auto-parse @ references — open the file at the path above explicitly.)"
    )


def emit_agent(tool: str, a: Agent) -> tuple[str, str]:
    if tool == "codex":
        marker = TOML_MARKER.format(src=a.source)
        content = (
            f"{marker}\n"
            f'name = "{a.name}"\n'
            f'description = "{a.description}"\n'
            'developer_instructions = """\n'
            "Follow the instructions from the canonical file as if they were written here; open it at\n"
            f"the given path and execute: {a.source}\n"
            '"""\n'
        )
        return f".codex/agents/{a.name}.toml", content
    path = f".{tool}/agents/{a.name}.md"
    marker = MD_MARKER.format(src=a.source)
    content = f"{_agent_md_frontmatter(tool, a)}\n\n{marker}\n\n{_agent_md_body(tool, a)}\n"
    return path, content


# ──────────────────────────────────────────────────────────────────────────
# CLAUDE.md shims — Claude does not read nested AGENTS.md, so each AGENTS.md dir
# gets a one-line CLAUDE.md import.
# ──────────────────────────────────────────────────────────────────────────

def emit_claude_shim(dir_rel: str) -> tuple[str, str]:
    if dir_rel == "":  # root
        marker = MD_MARKER.format(src="AGENTS.md + .vaibe/rules/")
        return "CLAUDE.md", f"{marker}\n@AGENTS.md\n"
    marker = MD_MARKER.format(src=f"{dir_rel}/AGENTS.md")
    return f"{dir_rel}/CLAUDE.md", f"{marker}\n@./AGENTS.md\n"


# ──────────────────────────────────────────────────────────────────────────

def emit_all(canon: Canon) -> dict[str, str]:
    """Render the entire native layer: {vault-relative path: content}."""
    out: dict[str, str] = {}
    for tool in TOOLS:
        for s in canon.skills:
            path, content = emit_skill(tool, s)
            out[path] = content
        for a in canon.agents:
            path, content = emit_agent(tool, a)
            out[path] = content
    for dir_rel in canon.agents_md_dirs:
        path, content = emit_claude_shim(dir_rel)
        out[path] = content
    return out


@dataclass
class NativeDiff:
    """Result of comparing the rendered native layer against what is on disk."""
    rendered: dict[str, str]
    match: list[str]
    diff: list[str]       # on disk but content differs from canon → drift
    missing: list[str]    # canon expects it, not on disk
    orphan: list[str]     # native skill/agent file on disk with no canon source

    @property
    def clean(self) -> bool:
        return not (self.diff or self.missing or self.orphan)


def compare_native(root: Path, canon: Canon) -> NativeDiff:
    """Render the native layer and diff it against `root` on disk (read-only)."""
    rendered = emit_all(canon)
    match, diff, missing = [], [], []
    for path, content in sorted(rendered.items()):
        target = root / path
        if not target.exists():
            missing.append(path)
        elif target.read_text(encoding="utf-8") == content:
            match.append(path)
        else:
            diff.append(path)

    orphan: list[str] = []
    for tool in TOOLS:
        for sub, pat in (("skills", "*/SKILL.md"), ("agents", "*")):
            base = root / f".{tool}" / sub
            if not base.exists():
                continue
            for f in base.glob(pat):
                rel = f.relative_to(root).as_posix()
                if f.is_file() and rel not in rendered:
                    orphan.append(rel)

    return NativeDiff(rendered, match, diff, missing, sorted(orphan))
