---
name: project-context-pack
description: Build unified project context document for knowledge transfer and onboarding
triggers: [context pack, project summary, onboarding, knowledge transfer, project overview]
---

# Purpose

Assemble a "single source of truth" for a project: what we do, why, for whom, current status, and artifact index. Used for onboarding new team members, transferring context across workspaces, and reducing knowledge loss between sprints.

# When to use

- Onboarding someone to an existing project
- Transferring project context to another workspace/repository
- Sprint boundary — consolidating current state
- Preparing for investor/stakeholder meeting

# Procedure

## Step 1 — Gather sources

Scan the project directory:
- Meetings: `Встречи/*/summary.md`, `tasks.md`
- Tasks: `Задачи/*/task.md` + key results in `results/`
- Project README: `README.md`
- Knowledge base: `База знаний/`

## Step 2 — Align terminology

Ensure consistent definitions across all materials (e.g., segments A/B/C/X, ICP, pilot/POC).

## Step 3 — Build project map

Compile:
- Product, value, audience/segments
- Current stage, metrics/trajectory
- Risks/constraints
- Next steps and priorities

## Step 4 — Build artifact index

Create links to key files: "where is what" with relative paths.

## Step 5 — Sanity check

- No edits to `Исходные материалы/` (read-only originals)
- No contradictions between meetings and task results (if any — describe explicitly)
- Facts clearly separated from hypotheses

# Output format

```markdown
# Project Context Pack: {Project Name}

**Date assembled:** YYYY-MM-DD
**Sources reviewed:** [list of files]

## About the project (1 paragraph)
## Problem and value (with numbers)
## Target segments and ICP (A/B/C/X)
## Product (modules/features)
## Status and confirmed facts
## Hypotheses requiring validation
## Competitors and differentiation (brief)
## GTM/Sales: ROI, scripts, pilot
## Work plan / next steps
## Artifact index (file paths)
```

# Quality bar

- [ ] Facts separated from hypotheses (clearly labeled)
- [ ] Every key claim references a file path
- [ ] Max 1–2 screens per section, details via links
- [ ] Assembly date and source list documented
- [ ] No contradictions between sections

# Anti-patterns

- Mixing confirmed facts with unvalidated hypotheses
- Claims without file references
- Editing original materials in `Исходные материалы/`
- Context pack longer than 3–4 pages (link to details instead)
