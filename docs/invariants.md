# Invariants

> Declarative spec of the system invariants. Machine implementation: `vaibe-os validate`
> (structure, configs) and `vaibe-os doctor` (runtime guards). Draft seed from Spec 001 §6 —
> final wording during development.

| ID | Invariant | Level |
|---|---|---|
| G1 | Core submodule pristine: no local edits, SHA = pinned tag | error |
| G2 | Core version visible; ≥2 minor versions behind — warning; compatibility with linked instances | warning |
| G3 | Core is company-agnostic and contains no executable code (leak-lint CI) | error |
| G4 | Instance structure matches the skeleton (`projects/inbox/wiki/teams` + task/project formats) | error |
| G5 | Skill names globally unique (core vs instance) | error |
| G6 | Task format is the one from the core; own vocabularies are declared (`v2.{project}`) | error |
| G7 | Isolation: pulls are read-only over `links` scope; delivery only pushes to `inbox/<sender>` | warning |

The human-readable wording in this file is the mirror of what `vaibe-os validate`/`doctor`
enforce — keep both in sync.
