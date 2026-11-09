# docs/AGENTS.md — documentation index for agents

Read these before changing the core:

- [manifesto.md](manifesto.md) — what vAIbe-OS is for and the principles users can rely on.
- [ontology.md](ontology.md) — the laws: the deepest declarative layer.
- [invariants.md](invariants.md) — invariants; `vaibe-os validate`/`doctor` implement them.

Rules of this layer:

- The declarative layer stays declarative — no process or tooling details here.
- Rules in `.vaibe/rules/` reference these principles instead of duplicating them.
- Files are compact and agent-first: one topic per file, short imperatives.
