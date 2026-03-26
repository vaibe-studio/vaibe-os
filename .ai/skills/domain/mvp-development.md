---
name: mvp-development
description: End-to-end MVP development process with quality metrics
triggers: [MVP, prototype, development process, build, implement]
origin: bundled
---

# Purpose

Guide the full cycle of MVP development from requirements through deployment, with clear quality gates at each stage.

# When to use

- Building a new product/feature from scratch
- Implementing a prototype for validation
- Planning development sprints

# Procedure

## Step 1 — Requirements

- Receive PRD from product manager
- Clarify ambiguities
- Agree on scope and timeline

## Step 2 — Architecture

- Design solution architecture
- Choose technology stack (see `.ai/knowledge/tech-stack-reference.md` for orientation)
- Assess risks and complexity

## Step 3 — Build MVP

- Implement MVP/prototype iteratively
- Improve based on feedback
- Validate with customer/stakeholder
- Document API and architecture

## Step 4 — Quality check (MVP phase)

| Metric | Target | Description |
|---|---|---|
| Requirements coverage | 100% | All PRD requirements implemented |
| API response time | <200ms (p95) | Performance |
| Uptime | >99% | Availability |
| Critical bugs | 0 in production | No blockers |
| Timeline adherence | >90% | Delivery on schedule |
| API documentation | 100% | OpenAPI/Swagger spec |
| Architecture docs | 100% | Solution architecture described |

## Step 5 — Post-MVP (separate tasks)

- Tests (unit/integration/e2e) — target >80% coverage
- Deployment instructions — 100%
- Refactoring as needed

## Step 6 — Deploy and support

- Deploy to production
- Configure monitoring
- Maintain and improve

# Output format

- Working MVP/prototype
- API documentation (OpenAPI/Swagger)
- Architecture documentation
- Deployment instructions (post-MVP)

# Quality bar

- [ ] All PRD requirements implemented
- [ ] API response time <200ms (p95)
- [ ] Zero critical bugs in production
- [ ] API and architecture documented
- [ ] Deployed and accessible

# Anti-patterns

- Skipping requirements clarification
- Building without architecture plan
- No documentation until post-MVP
- Ignoring performance targets during MVP phase

# Related knowledge

- `software-architecture-patterns.md` — architecture decision framework (monolith vs microservices, Clean Architecture for MVP structure)
- `devops-practices.md` — CI/CD pipeline setup, deployment strategies, DORA metrics for delivery quality
- `jtbd-custdev.md` — Customer Development validation steps to define MVP scope
- `agile-frameworks.md` — Scrum sprint mechanics for MVP iteration cadence
- `tech-stack-reference.md` — project tech stack orientation
