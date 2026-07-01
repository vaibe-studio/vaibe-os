# Topic: frontmatter (cross-tool)

What `SKILL.md` YAML frontmatter each tool reads. Unknown keys are ignored by
spec-compliant runtimes, so extra keys are safe but only honoured where listed.

## Universal (every tool)

- `name` — required. (sources: agentskills-canon, cursor, claude-code, opencode,
  anthropic-best-practices)
- `description` — required; what + when, ≤1024 chars. (all sources)

## Open canon optional keys

`license`, `compatibility` (≤500 chars), `metadata` (map), `allowed-tools`
(experimental, space-separated). (source: agentskills-canon)

## Per-tool extras

| Key | Open canon | Cursor | Claude Code | OpenCode | Codex |
|-----|:--:|:--:|:--:|:--:|:--:|
| `name` | ✅ req | ✅ req | optional (display; dir = command) | ✅ req | ✅ req |
| `description` | ✅ req | ✅ req | recommended | ✅ req | ✅ req |
| `license` | ✅ | – | – | ✅ | – |
| `compatibility` | ✅ | – | – | ✅ | – |
| `metadata` | ✅ | ✅ | – | ✅ (string→string) | – |
| `allowed-tools` | ✅ exp | – | ✅ | – | – |
| `disallowed-tools` | – | – | ✅ | – | – |
| `paths` | – | ✅ | ✅ | – | – |
| `disable-model-invocation` | – | ✅ | ✅ | – | – |
| `user-invocable` | – | – | ✅ | – | – |
| `when_to_use` | – | – | ✅ | – | – |
| `argument-hint` / `arguments` | – | – | ✅ | – | – |
| `model` / `effort` | – | – | ✅ | – | – |
| `context: fork` / `agent` | – | – | ✅ | – | – |
| `hooks` | – | – | ✅ | – | – |
| `shell` | – | – | ✅ | – | – |
| invocation policy / UI | – | – | – | – | `agents/openai.yaml` (separate file) |
| skill permissions | – | – | (settings) | `opencode.json` (separate file) | `config.toml` |

(sources: claude-code, cursor, opencode, codex, agentskills-canon)

Notes:
- Claude Code is by far the richest frontmatter; most of its keys are
  Claude-only.
- Codex puts UI/policy/deps in a sibling `agents/openai.yaml`, not in
  frontmatter. (source: codex)
- OpenCode and the open canon keep frontmatter minimal. (sources: opencode,
  agentskills-canon)
- Anthropic: no XML/angle brackets in frontmatter; no reserved words
  (`anthropic`, `claude`) in `name`. (source: anthropic-best-practices)

## vAIbe-OS mapping

The canonical `.vaibe/skills/{name}/SKILL.md` carries **flat, general fields
only** — `name`, `description`, and (optionally) `license`. The `doctor` canon
loader parses exactly these; nested keys in canon are intentionally ignored.
Tool-specific frontmatter is not authored by hand — it is **emitted per tool** by
`doctor treat`:

- **Cursor** wrapper: `name`, `description`, `metadata.origin: vaibe-os`.
- **OpenCode** wrapper: `name`, `description`, `license` (defaults to `MIT`),
  `compatibility: opencode`, `metadata.origin: vaibe-os`.
- **Claude Code / Codex** wrappers: `name`, `description` only.

If a skill ever needs a tool-only key (e.g. Claude's `allowed-tools`), add it to
the emitter matrix (`.vaibe/scripts/doctor/emitters.py`), not to the canonical
`SKILL.md`. (source: vAIbe-OS `.vaibe/scripts/doctor/`)
