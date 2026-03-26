# Router: Skill Selection Protocol

Before starting any task, classify it and select exactly ONE skill.

## Step 1 — Classify

| Category | Signals |
|---|---|
| **core** | task management, inbox, planning, reporting, briefings, system evolution |
| **domain** | specialized work: presentations, analysis, meetings, market research, engineering, sales |

## Step 2 — Select a skill

### Core Skills (`.ai/skills/core/`)

| Skill | Use when |
|---|---|
| `task-create.md` | Creating a new task card |
| `task-execute.md` | Executing an existing task |
| `inbox-processing.md` | Processing files from Inbox |
| `plan-update.md` | Creating/updating project management plan |
| `weekly-operating-sheet.md` | Building a cross-project managerial week sheet with owner map, decisions, waiting list |
| `tasks-report.md` | Building task status report |
| `project-context-pack.md` | Building unified project context |
| `daily-briefing.md` | Morning briefing: tasks, deadlines, inbox |
| `weekly-review.md` | Weekly review: progress, blockers, priorities |
| `evolve.md` | System self-improvement from insights |
| `yt-context-pull.md` | Pulling issue context from YouTrack |
| `yt-project-link.md` | Linking a project with YouTrack |
| `yt-project-tasks-pull.md` | Syncing YouTrack statuses back to project plan |
| `yt-project-tasks-push.md` | Publishing tasks from plan to YouTrack |

### Domain Skills (`.ai/skills/domain/`)

Scan `.ai/skills/domain/*.md` — read YAML frontmatter (`name`, `description`, `triggers`) to find the matching skill.

## Step 3 — Execute

1. Read the selected skill file fully
2. Follow its **Procedure** step-by-step
3. Produce output in the skill's **Output format**
4. Run self-check against **Quality bar**

If no skill matches, follow `AGENTS.md` judgment boundaries directly.

## Knowledge Base (`.ai/knowledge/`)

Non-actionable reference materials. Consult during skill execution when domain context is needed.

| File | Domain | Relevant skills |
|---|---|---|
| `pmbok7-principles.md` | Project management principles (PMBoK 7/8) | `plan-update`, `weekly-operating-sheet`, `task-create`, `weekly-review` |
| `agile-frameworks.md` | Scrum, Kanban, Scrumban, scaled agile | `plan-update`, `daily-briefing`, `weekly-review`, `tasks-report` |
| `jtbd-custdev.md` | Jobs-to-be-Done, Customer Development, hypothesis testing | `hypothesis-testing`, `market-research`, `stakeholder-analysis`, `mvp-development` |
| `strategy-frameworks.md` | SWOT, Porter, Blue Ocean, BMC, Lean Canvas, Wardley Maps | `market-research`, `stakeholder-analysis`, `roi-calculation`, `presentation-design` |
| `devops-practices.md` | CI/CD, IaC, GitOps, observability, DORA metrics, DevSecOps | `script-automation`, `task-execute` (engineering tasks) |
| `ai-standards-landscape.md` | ISO 42001, NIST AI RMF, EU AI Act, responsible AI, LLM eval | `evolve` (self-governance), any AI-related task |
| `software-architecture-patterns.md` | Clean Architecture, DDD, microservices, EDA, API design | `task-execute` (engineering tasks), `mvp-development` |
| `sales-methodologies.md` | SPIN, Challenger, MEDDPICC, Sandler, pipeline management | `sales-segmentation`, `stakeholder-analysis` |
| `startup-financial-modeling.md` | Unit economics, P&L, pricing, cohort analysis, burn rate | `roi-calculation`, `hypothesis-testing` |
| `glossary.md` | Unified EN/RU terminology dictionary | All skills (term disambiguation) |
| `knowledge-curation-guide.md` | How to maintain the knowledge base | `evolve` |
| `tech-stack-reference.md` | Project tech stack orientation | Engineering tasks |
| `startup-resources-ru.md` | Russian startup ecosystem resources | `market-research`, `hypothesis-testing` |
| `batch-operations-patterns.md` | Patterns for mass file/task operations | `task-execute` (batch tasks) |
| `Современный русский текст - Ильяхов и публицистика.md` | Russian writing style and editorial principles | Content creation tasks |
| `meta-mind/*` | Mentorship, style adaptation, interaction patterns | All interactions (behavioral layer) |

## Reference

- Rules: `.ai/rules/`
- Cursor commands: `.cursor/commands/` — slash-command wrappers for skills
- Claude Code commands: `.claude/commands/` — slash-command wrappers for skills
- Full project rules: `AGENTS.md`
