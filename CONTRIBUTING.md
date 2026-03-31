# Contributing to vAIbe-OS

> :ru: [Читать на русском](CONTRIBUTING.ru.md)

Thank you for your interest in vAIbe-OS! This project is built on a philosophy of **partnership between humans and AI** — and that extends to how we collaborate with contributors.

## How to contribute

### 1. Report a bug or suggest an improvement

[Open an issue](../../issues/new/choose) — we have templates for bugs, feature requests, and skill proposals.

### 2. Add a new skill

Skills are the heart of vAIbe-OS. Each skill is a Markdown playbook in `.ai/skills/domain/`.

**Steps:**
1. Create `.ai/skills/domain/your-skill.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   name: your-skill
   description: What this skill does (one line)
   triggers: [keyword1, keyword2, keyword3]
   ---
   ```
3. Include these sections: **Purpose**, **Procedure** (step-by-step), **Output format**, **Quality bar**
4. The router (`.ai/router.md`) discovers new skills automatically — no registration needed
5. Submit a PR

**Good skill examples:** Look at existing skills in `.ai/skills/core/` and `.ai/skills/domain/` for reference.

### 3. Improve existing skills or knowledge base

Every skill and knowledge file is plain Markdown. Read it, improve it, submit a PR.

**Knowledge base** (`.ai/knowledge/`) contains reference materials — strategy frameworks, PM principles, sales methodologies, and more. Contributions that add new domain knowledge or improve existing materials are welcome.

### 4. Improve tools

Python utilities live in `tools/`. Run them with `python -m tools.<name>`.

- Follow existing code style
- Stdlib-only where possible (minimize dependencies)
- Add/update `tools/TOOLS_INDEX.md` if adding a new tool

### 5. Improve documentation

README, AGENTS.md, and rule files — improvements to clarity and accuracy are always welcome.

## Guidelines

### Philosophy alignment

vAIbe-OS is built on specific principles ([Manifesto](.ai/MANIFESTO.md), [Ontology](.ai/ONTOLOGY.md)). When contributing, keep these in mind:

- **Partnership, not replacement** — features should augment the user, not create dependency
- **Additive evolution** — prefer adding and refining over deleting. Knowledge accumulates, it doesn't get erased
- **Autonomy of the source** — the user always makes the final decision. Don't build features that decide for the user
- **Honesty about LLM** — acknowledge limitations, don't create illusions of superpowers

### File naming

- Folders and files in the vault use **Russian names** (except `tools/`, `.ai/`, `repositories/`, system `.md` files)
- Task numbers use leading zeros: `001`, `002`, `010`
- See `.ai/rules/structure.md` for the full specification

### Pull requests

- Keep PRs focused — one change per PR
- Describe **what** and **why** in the PR description
- If changing skills or rules, explain how it aligns with the manifesto
- For new skills: include at least one usage example

### Code style

- Python: follow existing patterns, stdlib preferred
- Markdown: ATX headings (`#`), fenced code blocks, reference-style links where possible
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/) with emoji prefix (see `.ai/rules/git-commits.md`)

## Development setup

```bash
git clone https://github.com/vAIbe-studio/vaibe-os.git
cd vaibe-os
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

No additional dependencies needed for the core vault. Tools may have their own requirements.

## Questions?

- [Open a discussion](../../discussions) for questions and ideas
- [Open an issue](../../issues) for bugs and feature requests
