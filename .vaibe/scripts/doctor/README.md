# doctor — canon → native generator (vAIbe-OS, model A)

Generates and checks the per-tool native layer (`.{claude,cursor,opencode,codex}/…`,
`CLAUDE.md` shims) from the canon in `.vaibe/`. The canon is the single source of
truth; the native layer is derived and committed (model A, `GENERATED` marker).

Built across Phase-4 batches (task 067 umbrella):

Built across Phase-4 batches (task 067 umbrella): P (068) emitter matrix ·
Q (069) `diagnose` · R (070) `treat` · S (071) anti-drift (pre-commit + CI) ·
T (072) regression test.

## Two commands (uv project; `D` = the doctor project dir)

```bash
D=.vaibe/scripts/doctor

# diagnose — run every check, report problems (read-only).
uv run --project $D $D/main.py diagnose
uv run --project $D $D/main.py diagnose --check check lint   # subset of groups

# treat — heal: regenerate native from canon + prompt-hints for AGENTS.md.
uv run --project $D $D/main.py treat
uv run --project $D $D/main.py treat --dry-run               # preview, write nothing

# Anti-drift pre-commit (pre-commit.com framework).
pipx install pre-commit && pre-commit install
```

`diagnose` exits non-zero on any **error**; warnings (pre-existing vault hygiene)
are informational. Three groups:

- **check** (G11) — `generated == canon`: drift / missing / orphan native files.
  On the phase-3 layout the layer is 206 files (48 skills × 4 + 3 agents × 4 +
  2 `CLAUDE.md` shims).
- **lint** — `agents-rules` (every `.vaibe/rules/*.md` reflected in an `AGENTS.md`,
  no dangling `.vaibe/…` links, §3.3), `skill-validity` (G6: frontmatter,
  `name==folder`, latin slug), `reachability` (every skill `references/`, `assets/`
  file has an incoming link — lesson 065), `dead-links` (G12: canon prose has no live
  reference to a vision-removed entity — router.md, `.ai/`, … ; task 077).
- **guards** — structural invariants `.vaibe/rules/guards.md`: G1–G5, G10. Git-ignored
  (personal) data is out of scope; `vAIbe-{product}` latin names are exempt (G3).
  G7 is a process guard (info); G8/G9 are advisory.

`treat` writes only the generated layer (`.{tool}/…`, `CLAUDE.md` shims) — never
the canon (`.vaibe/`, `AGENTS.md`). It is idempotent: with the canon unchanged it
writes nothing. Orphans (native files with no canon source) are reported, not
deleted. A new `.vaibe/rules/X.md` with no `AGENTS.md` section prints a
prompt-hint (a section skeleton to paste by hand), never edits `AGENTS.md`.

`.vaibe/rules/guards.md` stays the human spec; `diagnose` is its executable form, and
supersedes the `.vaibe/scripts/vault_lint/` prototype (legacy `.ai/` paths).
Project/task/status reporting is the `tasks-report` skill (on demand); there is
no static index. Skills are discovered at runtime from `description` frontmatter.

## Layout

- `canon.py` — reads `.vaibe/skills/*/SKILL.md`, `.vaibe/agents/*.md`, finds `AGENTS.md` dirs.
- `emitters.py` — one emitter per `(tool, type)`: path + frontmatter + wrapper body; `compare_native`.
- `diagnose.py` — check + lint + guards; `Finding` records.
- `treat.py` — writes missing/divergent generated files; prompt-hints for the hand-written part.
- `main.py` — CLI entry; `pyproject.toml` declares the (empty) deps.
- `test_doctor.py` — regression test (batch T): asserts the emitters reproduce the
  phase-3 layout (206 files, all types) and `diagnose` is green. Run in CI:
  `uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/test_doctor.py`.

## Anti-drift loop (batch S)

- **`.pre-commit-config.yaml`** — local hook (pre-commit.com framework): runs
  `diagnose --check check lint` on commit. `pipx install pre-commit && pre-commit install`;
  bypass once with `git commit --no-verify`.
- **`.github/workflows/doctor.yml`** — load-bearing CI running the full `doctor diagnose`
  on GitHub. Make the check required so a red run blocks merge. (On GitLab or another
  self-hosted forge, mirror the same `uv run … diagnose` step in your CI config.)

## Notes that bind the emitters

- **Marker placement (correction to spec §2/U10, phase-3 empirical):** markdown
  marker is an HTML comment **below** the frontmatter; Codex TOML marker is a
  `#` line at the top. A leading markdown comment or an in-frontmatter `#` breaks
  opencode/Claude YAML parsing.
- **References (§2.4):** Claude/Cursor use `@.vaibe/…`; opencode/Codex use a
  plain path + imperative (their `@` is not auto-parsed).
- **Agent capability hints:** canon agent frontmatter carries the superset
  (`tools`, `readonly`); emitters map per tool (Claude `tools:`, Cursor
  `readonly:`) and drop the rest. `architect` has full access (no hints).
- **doctor does not touch the canon** (`.vaibe/`, `AGENTS.md`) — only the
  generated layer. `diagnose` is read-only; only `treat` writes.
