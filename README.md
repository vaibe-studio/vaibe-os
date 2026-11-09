# vAIbe-OS

> An open operating layer for your AI agents: one command creates a workspace with projects,
> tasks, meetings, incoming, knowledge and a team — plus skills that teach your agents how to
> work with all of it.

vAIbe-OS is harness-agnostic by design: it works with the AI harness you already use —
Cursor, Claude Code, Codex, OpenCode, Kilo Code, Kodik and other compatible ones.
Your workspace is a plain git repository: your context lives in your repo, so switching
harnesses or models is hours of work, not lost experience.

## Status

🚧 Early development. This repository is the **declarative core**: documentation, the instance
skeleton and the canon. The installer (CLI + install scripts) lives in
[vaibe-os-installer](https://github.com/vaibe-studio/vaibe-os-installer) — early development
too. See [CHANGELOG.md](CHANGELOG.md).

## Install

```bash
curl -fsSL https://os.vaibe.studio/install | bash
```

> Not live yet — the landing page and installer ship with v0.2.0. Manual install: download
> the `vaibe-os` binary from the
> [vaibe-os-installer releases](https://github.com/vaibe-studio/vaibe-os-installer/releases)
> and put it on your `PATH`.

Then create your first instance:

```bash
vaibe-os init ~/Projects/my-os
```

## What an instance looks like

| Folder | What lives there |
|---|---|
| `projects/` | your projects: `README.md`, `tasks/`, `meetings/`, `input/`, `wiki/` |
| `inbox/` | incoming material and handoffs from linked instances |
| `wiki/` | knowledge that is not tied to a single project |
| `teams/` | people and agents working in this instance |
| `.vaibe/` | instance canon: rules, skills, agents + `os/config.yml` |

Instances can be **linked**: a workspace can send handoffs — tasks, material, replies — into
another workspace's inbox. Nothing crosses the boundary by itself: only what you explicitly
pass.

## Principles

- **Harness-agnostic** — works with the harness you like; no vendor lock.
- **Privacy = instance boundary** — everyone with git access sees the whole instance;
  private zones are separate instances.
- **The agent reads, the human decides.**

## Documentation

- [docs/README.md](docs/README.md) — documentation index
- [docs/ontology.md](docs/ontology.md) — the laws of the system
- [docs/invariants.md](docs/invariants.md) — invariants and their machine checks

## License

[MIT](LICENSE)
