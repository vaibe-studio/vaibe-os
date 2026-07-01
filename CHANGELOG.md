# Changelog

All notable changes to vAIbe-OS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1-alpha] - 2026-07-01

> Pre-release. Structure and APIs may still change before 0.1.0.

### Added

- **`os-skill-base` skill** — a sourced reference on how agent skills are
  composed: the cross-tool open standard (agentskills.io) and the deltas for
  Cursor, Claude Code, OpenCode, and Codex, Anthropic authoring best practices,
  and how it all maps onto the vAIbe-OS canon (model A). Reference knowledge to
  load before authoring, reviewing, or changing any skill. Brings the skills
  library to 48.

## [0.1.0-alpha] - 2026-06-25

First alpha of vAIbe-OS as a canon-driven system. This release replaces the
earlier `.ai/` template (v0.0.1) with the `.vaibe/` single source of truth,
generated native wrappers for AI IDEs, and the `doctor` integrity tool that
keeps the generated layer in sync with the canon.

> Pre-release. Structure and APIs may still change before 0.1.0.

### Added

- **`.vaibe/` canon architecture** — single source of truth for rules, skills,
  agents and scripts; native per-tool wrappers (`.claude/`, `.cursor/`,
  `.codex/`, `.opencode/`, `CLAUDE.md` shims) are generated from it and
  committed (model A, `GENERATED` marker).
- **`doctor` tool**
  - `diagnose` — integrity checks against Guards (G1–G11) for canon ↔ generated
    drift, dead links, and submodule validation.
  - `treat` — regenerates the native layer from the canon.
  - canon loader + emitter matrix.
- **Anti-drift mechanism** — `doctor diagnose` wired into a pre-commit hook and
  CI (`.github/workflows/doctor.yml`), plus regression tests.
- **Rules canon** (`.vaibe/rules/`) — structure, naming-convention,
  git-cross-platform, git-commits, interactive-patterns, scripts, discovery,
  powershell, guards.
- **Behavioral foundation** — Manifesto, Ontology (five laws), Guards, and the
  always-on playbooks: mentorship, user-methods, dialogue-patterns,
  style-adaptation.
- **Skills library** (47 skills) — task lifecycle (task-create/execute,
  tasks-report), planning, inbox/meeting processing, market/product/sales,
  knowledge curation, and reference packs.
- **Scripts = uv-project standard** — each script is a self-contained `uv`
  project (`pyproject.toml` + `uv.lock`), run via `uv run --project <dir>`.

### Changed

- Canon content translated RU → EN (vault folder names stay Russian).
- Scripts migrated to the `uv` project structure.
- README, CONTRIBUTING and the installer rewritten for the `.vaibe/` model.

### Removed

- Legacy `.ai/` and top-level `tools/` trees — canon is now `.vaibe/` only.
  The first-run installer moved to `.vaibe/scripts/installer/` as a `uv` project.
- Standalone command `.md` files — superseded by skills.
- `vault_lint` script — superseded by `doctor diagnose` (it checked legacy
  `.ai/` paths); all references scrubbed.
- `dechecker` script — one-off image utility with no callers.

### Fixed

- `doctor`: Windows UTF-8 subprocess handling and POSIX orphan-path resolution.
- `doctor`: submodule validation logic in diagnostics.

[0.1.1-alpha]: https://github.com/vaibe-studio/vaibe-os/compare/v0.1.0-alpha...v0.1.1-alpha
[0.1.0-alpha]: https://github.com/vaibe-studio/vaibe-os/compare/v0.0.1...v0.1.0-alpha
