# Topic: discovery & locations (cross-tool)

Where each tool scans for skills, and the scope each location grants. All tools
discover by reading `name` + `description` at startup (progressive disclosure).

## Per-tool locations

**Cursor** (source: cursor)
- `.cursor/skills/`, `.agents/skills/` (project); `~/.cursor/skills/`,
  `~/.agents/skills/` (global). Also loads `.claude/skills/`, `.codex/skills/`
  (+ home) for compatibility.
- Nested `.cursor/skills/` anywhere is auto-scoped to its subtree; category
  subfolders allowed (name = folder with `SKILL.md`).
- Reserved: `~/.cursor/skills-cursor/` (built-ins) — don't author there.

**Claude Code** (source: claude-code)
- `~/.claude/skills/` (personal), `.claude/skills/` (project),
  `<plugin>/skills/` (plugin), enterprise via managed settings.
- Override on clash: enterprise > personal > project; overrides bundled.
- Nested `.claude/skills/` below cwd load on demand (monorepo);
  directory-qualified names on clash.

**OpenCode** (source: opencode)
- `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (project, walking up
  to git worktree); `~/.config/opencode/skills/`, `~/.claude/skills/`,
  `~/.agents/skills/` (global).

**Codex** (source: codex)
- `.agents/skills` from cwd up to repo root; `$HOME/.agents/skills` (user);
  `/etc/codex/skills` (admin); bundled (system). Same `name` does not merge.

**Open canon** (source: agentskills-canon)
- Defines the folder+`SKILL.md` unit; leaves exact discovery dirs to each tool.

## Cross-tool convergence

`.agents/skills/` is the emerging shared convention (Cursor, OpenCode, Codex).
`.claude/skills/` is widely read for compatibility (Cursor, OpenCode). So a skill
placed once under a broadly-read dir can surface in several tools.

## vAIbe-OS mapping

vAIbe-OS keeps the canon in `.vaibe/skills/` and generates **one wrapper per
tool** from it via `doctor treat` (model A; source: vAIbe-OS
`.vaibe/scripts/doctor/emitters.py`):

| Tool | vAIbe-OS wrapper location |
|------|---------------------------|
| Claude Code | `.claude/skills/{name}/SKILL.md` |
| Cursor | `.cursor/skills/{name}/SKILL.md` |
| OpenCode | `.opencode/skills/{name}/SKILL.md` |
| Codex | `.codex/skills/{name}/SKILL.md` |

Each wrapper points back to the canonical `.vaibe/skills/{name}/SKILL.md`;
`references/`, `scripts/`, and `assets/` are **read from canon, not copied** per
tool. `doctor treat` regenerates all wrappers (a pure function of the canon) and
`doctor diagnose` checks there are no missing, stale, or orphan wrappers.

Note (source: codex): Codex's documented dir is `.agents/skills`; vAIbe-OS
targets `.codex/skills/` (which Cursor/OpenCode also read). Confirm the running
Codex loads `.codex/`; otherwise `.agents/skills` is the portable location.
