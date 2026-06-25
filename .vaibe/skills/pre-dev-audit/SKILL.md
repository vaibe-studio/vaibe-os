---
name: pre-dev-audit
description: Pre-development audit checklist for product packages before build. Reference material (non-actionable knowledge).
license: MIT
---

# Pre-dev audit checklist for a product package

> Source: `/evolve` 2026-03-28 — pattern formalized from the vAIbe-digest audit

## When to apply

Before starting development on a product package (Lean Canvas, user stories, architecture, roadmap). Especially important in solo-builder mode, where there is no one to give a second opinion.

## How to run it

**Option 1: Second agent.** Hand the product package to another AI agent (different model, different context) and ask it to audit against this checklist.

**Option 2: Self-audit.** Go through the checklist yourself 1-2 days after creating the package (the "fresh eyes" effect).

## Checklist

### 1. Promises vs capabilities

- [ ] The value proposition contains no inflated promises the technology cannot guarantee
- [ ] Phrasings like "always", "100%", "we guarantee" are checked for realism
- [ ] Beta limitations are explicitly stated (what it does, what it does NOT do)

### 2. Legal and compliance

- [ ] Data sources checked for legal/ToS compatibility
- [ ] User data storage described (what, how long, where)
- [ ] For beta: limitations on source types are recorded

### 3. Internal consistency

- [ ] TTFV (Time to First Value) is described consistently across UX flow, metrics, and roadmap
- [ ] Personas and user stories are aligned (every expected persona feature exists in the stories)
- [ ] Roadmap covers all Must-stories
- [ ] Metrics are measurable on the chosen platform (don't require data that doesn't exist)

### 4. Metrics and measurability

- [ ] Separated: automatic / proxy / qualitative (manual) metrics
- [ ] Target values are realistic for beta (not copied from mature products)
- [ ] Red flags with thresholds and action items exist
- [ ] The collection mechanism for each metric is described

### 5. Quality gates

- [ ] A formal criterion exists for "when the product is ready for beta users"
- [ ] A quality checklist for the core output exists (not just technical works/doesn't-work)
- [ ] A fallback mode is described for quality degradation
- [ ] A rhythm of manual quality audits after launch exists

### 6. Specification completeness

- [ ] Presets / default settings are described concretely (not "to be determined later")
- [ ] Data contracts / API contracts are described (data structure, required fields)
- [ ] Ranking / scoring logic is described at least at the level of principles
- [ ] Fallback behavior is defined for every critical component

### 7. Operational realism

- [ ] A solo-builder can maintain the system without burnout
- [ ] No premature automation (what is simpler to do by hand at beta is not over-engineered)
- [ ] Rough load model: posts × users × inference = cost and latency
- [ ] The plan for acquiring the first users is concrete (where from, how, who collects feedback)

## Audit result format

```markdown
# Audit of [package name]

## Overall verdict
[go / go with conditions / no-go]

## Critical issues
[What blocks the start of development]

## What is still missing
[Specific artifacts or decisions]

## Improvement suggestions
[Prioritized list]

## Recommendations for the solo-builder
[Specifics of working alone]
```

## What to do with the results

1. Go through each issue — make a decision (fix / accept risk / defer)
2. Update the product package (new version in `results/v{N+1}/`)
3. Add an "Appendix: Audit log" with decision traceability
4. If there were critical issues — revisit the roadmap
