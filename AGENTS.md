# AGENTS.md — developing the vAIbe-OS core

Read [docs/AGENTS.md](docs/AGENTS.md) first (documentation index), then:

- [docs/ontology.md](docs/ontology.md) — the laws; every rule and skill must comply.
- [docs/invariants.md](docs/invariants.md) — invariants; `vaibe-os validate` implements them.

## Layout

- `docs/` — declarative layer: read by humans and agents. Manifesto, ontology, invariants.
- `structure/` — the instance skeleton `vaibe-os init` copies into a new instance.
- `install/` — installer scripts (bash / PowerShell).
- `.vaibe/` — the core's own canon: rules, skills, agents. Intentionally minimal — populated
  iteratively; compact and agent-first.

## Rules for this repository

- Core contains content and canon only — no executable code outside `install/` tooling.
- Nothing company-specific: names, brands, clients, services must not appear here.
- Rules and skills are written fresh: short, imperative, one topic per file (~40 lines max).
  No additive accretion — superseding rules are consolidated at write time.
- Changes via PR; merge and tag (semver) by the owner. `CHANGELOG.md` per release.
- Keep `structure/` in sync with the documentation when the instance skeleton changes.
