---
name: product-workshop
description: Step-by-step conversational workshop for designing a new product — from idea to ready-for-dev artifacts. Triggers: продуктовый воркшоп, спроектировать продукт, lean canvas, user stories, продуктовый пакет, product design, product workshop.
license: MIT
---

# Purpose

Guide the user through a structured Q&A process to assemble a complete product package: from understanding the target user to artifacts ready for hand-off to development.

The skill works in dialogue mode through surveys — each step produces structured questions whose answers shape the next step. The agent does not think for the user but helps draw out and formalize their vision.

# When to use

- A new product idea needs formalization
- Need to move from concept/prototype to a beta launch
- The user wants to "think about the product" in a structured format
- Need a set of artifacts to hand off to development

# Inputs needed

- A product idea or prototype (at least at the level of "what it does")
- Existing context: tasks, prior research, competitors (if any)
- Desired set of output artifacts (or use the standard set)

# Procedure

## Step 0 — Gather context

Before starting the workshop, read everything that already exists about the product:
- Project tasks, plans, knowledge base
- Prior research (Lean Canvas, competitors, JTBD)
- Code / prototype (README, docs)

Goal: don't start from scratch — build on what's already accumulated.

## Step 1 — Target user

Structured survey:
- **Who is the primary user?** (options from context + "other")
- **What is the main pain?** (multiple choice)
- **Which sources / content / domain?** (depends on the product)

Record answers right after each step so the user sees the accumulating picture.

## Step 2 — Value and positioning

- **Product metaphor** — how to explain the value in one sentence
- **Usage frequency** — how often the user interacts
- **Monetization model** — free / freemium / paid / beta → paid

## Step 3 — Format and wow factor

- **Output format** — how the user sees the result
- **Depth** — how much information at once
- **Killer feature** — what makes the user say "wow, this is great"
- **Interaction** — what the user does after receiving the result

## Step 4 — Technical and product boundaries

- **Technical approach** — key technology decisions
- **Onboarding** — how the user gets started
- **Beta size** — how many users
- **Infrastructure** — where to host, what constraints

## Step 5 — Growth, metrics, risks

- **Acquisition channels** — where the first users come from
- **North star metric** — what "success" means
- **Main risks** — what could kill the product
- **Timeline** — when launch is realistic

## Step 6 — Details and confirmation

- **Name and branding**
- **Product language**
- **Which artifacts to produce** (select from the standard set)

## Step 7 — Generate artifacts

Based on all answers, assemble a single document. Standard set:

1. **Lean Canvas** — one-page business model
2. **Personas** — 2-3 target users with pains and expectations
3. **User Stories** — 10-15 stories in the format "As a [persona], I want [action], so that [value]"
4. **UX flow** — user journey from first touch to daily habit
5. **Technical architecture** — stack, components, pipeline
6. **Risk map** — critical and significant risks with mitigations
7. **Roadmap** — phases from the current state to beta
8. **Success metrics** — what and how we measure
9. **Mockup** — example of the ideal output (message, screen, report)

## Step 8 — Pre-dev audit (recommended)

After generating the package, recommend the user run a pre-dev audit (see `.vaibe/skills/pre-dev-audit/SKILL.md`):
- Bring in a second agent or run a self-audit
- Check against the checklist
- Refine the package based on audit results
- Save the updated version with an audit log

# Key principles

- **Don't assume**: ask questions rather than guessing answers
- **Structured UI**: use the structured-question tool with options (Cursor `AskQuestion`, Claude Code `AskUserQuestion`, or the equivalent — see `.vaibe/rules/interactive-patterns.md`), not open-ended questions
- **Allow multiple**: permit multiple selection where it makes sense
- **Free text escape**: always offer an "other (I'll describe)" option
- **Show progress**: after each step, record what has already been decided
- **Context-aware options**: survey options must reflect the product's context, not be generic

# Output format

A single markdown file in the task's `results/v{N}/`. Document structure:
- All artifacts from Step 7
- Appendix: summary of decisions from the workshop
- If an audit was done: appendix with the audit log and decisions

# Quality bar

- [ ] All steps went through dialogue (not generated without user involvement)
- [ ] Artifacts are based on answers, not on assumptions
- [ ] User stories cover onboarding, daily use, edge cases
- [ ] Roadmap has clear Definition of Done for each phase
- [ ] Metrics are realistic for the chosen platform
- [ ] Pre-dev audit recommended before starting development
