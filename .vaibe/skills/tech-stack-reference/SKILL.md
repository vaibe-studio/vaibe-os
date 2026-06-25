---
name: tech-stack-reference
description: Project tech stack orientation — languages, frameworks, tooling. Reference material (non-actionable knowledge).
license: MIT
---

# Tech Stack Reference

Orientation guide, not a rigid standard. Final stack is chosen based on project constraints, timelines, and team.

## Backend

- Python (FastAPI, Django)
- Go

## Frontend

- Vue.js / Nuxt
- TypeScript
- Tailwind CSS

## Databases

- PostgreSQL
- Redis, MongoDB
- ClickHouse
- Elasticsearch

## Infrastructure

- Docker, Kubernetes
- GitLab CI
- Yandex Cloud / cloud.ru / Selectel / VDSina

## Code hosting

> Fill these in for **your** instance — the forge, namespace and URL shapes below are placeholders.

- **Forge**: your Git host (GitHub, GitLab, Gitea, self-hosted) — e.g. `https://git.example.com`
- **Namespace**: `<org>/<repo>`
- **SSH access**: `ssh://git@git.example.com/<org>/<repo>.git`
- **URL templates for code links** (important when building links in messages/documents) — shape differs per forge:
  - GitLab folder: `<host>/<ns>/<repo>/-/tree/<ref>/<path>` · file: `…/-/blob/…` · raw: `…/-/raw/…` · commit: `…/-/commit/<sha>`
  - GitHub folder: `<host>/<ns>/<repo>/tree/<ref>/<path>` · file: `…/blob/…` · raw: `raw.githubusercontent.com/<ns>/<repo>/<ref>/<path>` · commit: `…/commit/<sha>`
  - Gitea folder: `<host>/<ns>/<repo>/src/branch/<ref>/<path>`
- Cyrillic and spaces in **HTTP URLs** — URL-encode (`%20`, `%2C`), leave slashes `/` as is. This applies **only to HTTP URLs**. For **local vault links** in md files, use the CommonMark angle-bracket form with raw spaces: `[text](<path with spaces/file.md>)` — `%20` in local links breaks click-to-open in Cursor/VS Code.

## AI/ML Integrations

- OpenAI API, Anthropic API
- LangChain, LlamaIndex
- Hugging Face
