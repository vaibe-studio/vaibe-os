# Contributing to vAIbe-OS

> :ru: [Читать на русском](CONTRIBUTING.ru.md)

Thank you for your interest in vAIbe-OS! This project is built on a philosophy of **partnership between humans and AI** — and that extends to how we collaborate with contributors.

## The golden rule: edit the canon, not the wrappers

vAIbe-OS follows a **one canon, many native wrappers** model. The single source of truth is `.vaibe/` (rules, skills, agents, scripts). The per-IDE layers — `.claude/`, `.cursor/`, `.codex/`, `.opencode/`, and the `CLAUDE.md` shims — are **generated** and carry a `GENERATED` marker. Never edit them by hand; your change would be overwritten on the next regeneration.

After any canon change, regenerate and verify with the built-in **doctor**:

```bash
D=.vaibe/scripts/doctor
uv run --project $D $D/main.py treat       # regenerate native wrappers from the canon
uv run --project $D $D/main.py diagnose    # check canon ↔ native integrity (must be green)
```

`diagnose` is the CI gate — a PR must keep it green. Commit the canon **and** the regenerated wrappers together.

## How to contribute

### 1. Report a bug or suggest an improvement

[Open an issue](../../issues/new/choose) — we have templates for bugs, feature requests, and skill proposals.

### 2. Add a new skill

Skills are the heart of vAIbe-OS. Each skill is a folder under `.vaibe/skills/` holding a `SKILL.md` playbook.

**Steps:**
1. Create `.vaibe/skills/your-skill/SKILL.md` (folder name must equal the `name` field, latin kebab-case)
2. Add YAML frontmatter:
   ```yaml
   ---
   name: your-skill
   description: What this skill does, plus trigger keywords. Triggers: keyword1, keyword2.
   license: MIT
   ---
   ```
3. Include these sections: **Purpose**, **Procedure** (step-by-step), **Output format**, **Quality bar**
4. Put any helper scripts in `.vaibe/skills/your-skill/scripts/` and reference material in `references/` or `assets/` (every such file needs an incoming link)
5. Regenerate the native layer (`doctor treat`) and make sure `doctor diagnose` is green
6. Submit a PR

The agent discovers skills automatically by their `description` — there is no router or registry to update.

**Good skill examples:** browse existing skills in `.vaibe/skills/` for reference.

### 3. Improve existing skills or knowledge

Every skill is plain Markdown in `.vaibe/skills/`. Reference/domain-knowledge skills (strategy frameworks, PM principles, sales methodologies, and more) live alongside the actionable ones. Read it, improve it, regenerate, submit a PR.

### 4. Improve scripts

Python utilities live in `.vaibe/scripts/{name}/` (cross-skill) or `.vaibe/skills/{skill}/scripts/`. Each is a **self-contained `uv` project** with its own `pyproject.toml`; run it via:

```bash
uv run --project .vaibe/scripts/<name> .vaibe/scripts/<name>/main.py [args]
```

- Follow existing code style; keep dependencies minimal
- Commit the `uv.lock`
- No `requirements.txt`, no manual venv, no `python -m tools.X` (PEP 723 inline metadata only for throwaway one-liners)

### 5. Improve documentation

README, AGENTS.md, and the rule files in `.vaibe/rules/` — improvements to clarity and accuracy are always welcome.

## Guidelines

### Philosophy alignment

vAIbe-OS is built on specific principles ([Manifesto](.vaibe/rules/manifesto.md), [Ontology](.vaibe/rules/ontology.md)). When contributing, keep these in mind:

- **Partnership, not replacement** — features should augment the user, not create dependency
- **Additive evolution** — prefer adding and refining over deleting. Knowledge accumulates, it doesn't get erased
- **Autonomy of the source** — the user always makes the final decision. Don't build features that decide for the user
- **Honesty about LLM** — acknowledge limitations, don't create illusions of superpowers

### File naming

- Folders and files in the vault use **Russian names** (except canon `.vaibe/`, `repositories/`, and system `.md` files, which stay latin)
- Task numbers use leading zeros: `001`, `002`, `010`
- No case-only renames (contributors span case-insensitive Windows and case-sensitive Linux)
- See [`.vaibe/rules/structure.md`](.vaibe/rules/structure.md) for the full specification

### Pull requests

- Keep PRs focused — one change per PR
- Describe **what** and **why** in the PR description
- If changing skills or rules, explain how it aligns with the manifesto
- For new skills: include at least one usage example
- Include the regenerated native layer and keep `doctor diagnose` green
- **Never `git add -A`** — stage explicit paths (the vault contains personal/git-ignored zones)

### Code style

- Python: follow existing patterns, keep dependencies minimal
- Markdown: ATX headings (`#`), fenced code blocks, reference-style links where possible
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/) with an emoji prefix (see [`.vaibe/rules/git-commits.md`](.vaibe/rules/git-commits.md))

## Development setup

```bash
git clone https://github.com/vaibe-studio/vaibe-os.git
cd vaibe-os
```

You need [`uv`](https://docs.astral.sh/uv/) to run the scripts and the doctor (it manages each script's environment). The core vault itself is just Markdown — no build step.

## Questions?

- [Open a discussion](../../discussions) for questions and ideas
- [Open an issue](../../issues) for bugs and feature requests
