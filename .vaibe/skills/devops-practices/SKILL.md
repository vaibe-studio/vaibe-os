---
name: devops-practices
description: CI/CD, IaC, GitOps, observability, DORA metrics, DevSecOps. Reference material (non-actionable knowledge).
license: MIT
---

# DevOps — Culture, Practices, and Metrics

Practical reference for DevOps culture, CI/CD, infrastructure automation, observability, security, and performance measurement. Enables the agent and user to make informed decisions about delivery pipelines, infrastructure strategy, and engineering practices.

## When to use

- Designing or reviewing CI/CD pipelines and deployment strategies
- Making infrastructure decisions (cloud, containers, orchestration)
- Evaluating engineering team health and delivery performance (`tasks-report`)
- Planning infrastructure tasks or migrations (`task-create`, `task-execute`)
- Assessing security posture in software projects
- Cross-reference with tech stack decisions (see `.vaibe/skills/tech-stack-reference/SKILL.md`)

---

## Culture: CALMS framework

DevOps is a culture, not a tool. The CALMS framework (Jez Humble) assesses DevOps maturity across five dimensions:

### Culture

Shared responsibility between development and operations. Learning from failure is expected and encouraged. Blame-free post-incident reviews. Cross-functional teams own the full lifecycle: build, deploy, run, monitor.

### Automation

Automate repeatable processes: builds, tests, deployments, infrastructure provisioning, security scanning. Start manual, then automate incrementally. Automation reduces human error and frees time for high-value work.

### Lean

Borrowed from manufacturing. Minimize waste: handoffs, waiting, rework, context switching. Visualize work in progress. Limit batch sizes. Optimize flow from idea to production. Small, frequent changes are safer than large, infrequent releases.

### Measurement

Collect data on processes, deployments, and outcomes. Use metrics to understand current capability and identify improvement areas. Measure what matters (DORA metrics — see below), not what's easy to count.

### Sharing

Open knowledge exchange within and across teams. Shared tools, shared dashboards, shared on-call responsibilities. Documentation as a product. Reduce silos and information asymmetry.

---

## CI/CD — Continuous Integration and Delivery

### Continuous Integration (CI)

Developers integrate code into a shared repository frequently (at least daily). Each integration triggers an automated build and test pipeline. Goal: detect integration problems early, keep the main branch always releasable.

**Essential practices:**
- Trunk-based development or short-lived feature branches (merge within 1–2 days)
- Automated build on every commit/push
- Automated tests: unit, integration, smoke
- Fast feedback: pipeline should complete in minutes, not hours
- Fix broken builds immediately (highest priority)

### Continuous Delivery (CD)

Every change that passes CI is automatically deployable to production. Deployment is a business decision, not a technical hurdle. The artifact is always in a releasable state.

### Continuous Deployment

Extension of CD: every change that passes all automated checks is deployed to production automatically, without manual approval. Requires high confidence in test coverage and monitoring.

### Pipeline anatomy

```
Code Commit
  → Build (compile, package)
  → Unit Tests
  → Static Analysis (linting, SAST)
  → Integration Tests
  → Artifact Storage (container registry, package repo)
  → Deploy to Staging
  → Acceptance / E2E Tests
  → Security Scan (DAST, SCA)
  → Deploy to Production
  → Smoke Tests + Monitoring
```

### Deployment strategies

| Strategy | Mechanism | Risk | Rollback |
|---|---|---|---|
| **Rolling update** | Replace instances gradually | Medium | Reverse the roll |
| **Blue/Green** | Two identical environments; switch traffic | Low | Switch back |
| **Canary** | Route small % of traffic to new version | Low | Reroute traffic |
| **Feature flags** | Toggle features in code without redeployment | Very low | Disable flag |
| **A/B testing** | Route by user segment for experimentation | Low | Disable variant |

---

## Infrastructure as Code (IaC)

### Principle

Manage infrastructure through versioned, declarative configuration files, not manual processes. Infrastructure changes go through the same code review, testing, and version control as application code.

### Key tools (aligned with tech-stack-reference.md)

| Tool | Type | Use case |
|---|---|---|
| **Terraform** | Declarative, multi-cloud | Cloud infrastructure provisioning |
| **Ansible** | Procedural/declarative, agentless | Configuration management, server setup |
| **Helm** | Kubernetes package manager | Application deployment on K8s |
| **Docker** | Container runtime | Application packaging and isolation |
| **Kubernetes** | Container orchestration | Scheduling, scaling, service discovery |
| **Pulumi** | Programmatic IaC (Python, Go, TS) | Complex infrastructure with logic |

### IaC best practices

- Version all infrastructure code in Git
- Use modules/templates for reusable components
- Test infrastructure changes in non-production first
- Implement state management (remote state, locking)
- Separate configuration from secrets (use vault/KMS)
- Plan before apply; review diffs

---

## GitOps

### OpenGitOps principles (v1.0.0)

1. **Declarative** — desired state expressed in configuration (YAML, JSON), not imperative scripts
2. **Versioned and immutable** — state stored in Git with full version history
3. **Pulled automatically** — agents pull desired state from Git (not pushed by CI)
4. **Continuously reconciled** — agents detect drift between desired and actual state; auto-correct

### How GitOps works

Git repository is the single source of truth for infrastructure and application configuration. All changes go through pull requests with review and approval. Agents (ArgoCD, Flux) running in the cluster watch the repo and reconcile actual state to desired state.

### Benefits

- Auditability: every change is a Git commit with author and timestamp
- Rollback: `git revert` reverts infrastructure state
- Security: no direct cluster access needed for deployments
- Consistency: same process for all environments

---

## Observability

### Three pillars

| Pillar | What it provides | Examples |
|---|---|---|
| **Logs** | Discrete events with context | Application errors, access logs, audit trails |
| **Metrics** | Numerical measurements over time | CPU usage, request latency, error rate, queue depth |
| **Traces** | Request journey across services | End-to-end latency, service dependency mapping |

### OpenTelemetry

Vendor-neutral standard for telemetry data (traces, metrics, logs). Provides SDKs, APIs, and collectors. Adopted as the CNCF standard for observability instrumentation. Decouples data collection from backend (send to Grafana, Datadog, Elasticsearch, etc.).

### Observability vs monitoring

Monitoring tells you **when** something is wrong (alerting on known failure modes). Observability lets you understand **why** it's wrong (exploring unknown failure modes using rich telemetry data). Both are needed.

### Key practices

- Instrument at the application level, not just infrastructure
- Use structured logging (JSON) for machine parseability
- Define SLIs (Service Level Indicators) and SLOs (Service Level Objectives)
- Alert on symptoms (user-facing impact), not causes (CPU spikes)
- Build dashboards for different audiences: engineering, product, leadership

---

## DevSecOps — Security in the pipeline

### Shift left (broad interpretation)

Embed security thinking early: threat modeling, secure architecture review, security requirements in user stories. This is not "make developers fix all security bugs" — it is "make security a first-class concern from design."

### Security scanning layers

| Layer | Tool type | What it catches | When to run |
|---|---|---|---|
| **SAST** | Static analysis | Code-level vulnerabilities (injection, XSS, secrets) | Every commit (CI) |
| **SCA** | Dependency analysis | Known CVEs in libraries and containers | Every build |
| **DAST** | Dynamic testing | Runtime vulnerabilities (auth bypass, SSRF) | Staging/pre-production |
| **IaC scanning** | Config analysis | Misconfigurations (open ports, no encryption) | Every infra change |
| **Secret scanning** | Pattern matching | Leaked credentials, API keys | Pre-commit + CI |

### Supply chain security

Supply chain attacks accounted for ~30% of external attacks in 2025. Key defenses:
- Pin dependencies to specific versions
- Verify package integrity (checksums, signatures)
- Use private registries with vulnerability scanning
- Maintain a Software Bill of Materials (SBOM)
- Automate dependency updates with review (Dependabot, Renovate)

### AI-generated code security

24.7% of AI-generated code contains security vulnerabilities (2025 data). Mitigation: treat AI-generated code with the same review rigor as human code; run SAST/SCA on all generated output; maintain security awareness in AI-assisted workflows.

---

## DORA metrics — measuring delivery performance

### The four key metrics

| Metric | Definition | Elite | High | Medium | Low |
|---|---|---|---|---|---|
| **Deployment frequency** | How often code deploys to production | Multiple/day | Daily–weekly | Weekly–monthly | Monthly+ |
| **Lead time for changes** | Commit to production | < 1 day | 1 day–1 week | 1 week–1 month | 1 month+ |
| **Change failure rate** | % of deployments causing failures | < 5% | < 10% | < 15% | 15%+ |
| **Failed deployment recovery time** | Time to restore service after failure | < 1 hour | < 1 day | < 1 week | 1 week+ |

Deployment frequency + lead time = **throughput**.
Change failure rate + recovery time = **stability**.

Elite teams achieve both high throughput AND high stability — these are not trade-offs.

### 2024–2025 DORA findings

- AI adoption amplifies existing capabilities: strengthens high-performing teams, magnifies dysfunction in struggling ones
- 90% of tech professionals use AI tools; 30% have low trust in AI-generated code
- Documentation quality, clear change policies, and user-centric focus matter more than AI tools alone
- Platform engineering continues to correlate with improved delivery performance

### How to use DORA metrics

1. Measure current state across all four metrics
2. Identify the weakest metric — improve it first
3. Focus on systemic causes, not symptoms (long lead time → investigate approval bottlenecks, test gaps, deployment complexity)
4. Track trends over quarters, not weeks
5. Never use DORA metrics to compare teams — use for team self-improvement

---

## SRE practices (brief)

Site Reliability Engineering (Google) overlaps with DevOps. Key additions:

| Concept | Description |
|---|---|
| **SLI** (Service Level Indicator) | Quantitative measure of service quality (e.g., 99th percentile latency) |
| **SLO** (Service Level Objective) | Target value for an SLI (e.g., latency < 200ms for 99% of requests) |
| **SLA** (Service Level Agreement) | Contractual commitment based on SLOs (with consequences for breach) |
| **Error budget** | Allowed amount of unreliability (100% - SLO). Spend it on velocity; replenish by improving reliability |
| **Toil** | Manual, repetitive, automatable, non-value-adding work. Systematically reduce it |
| **Blameless post-mortems** | Investigate incidents without blame; focus on systemic fixes, not individual errors |

---

## Decision heuristics

- **Small team, few services** → simple CI/CD (GitHub Actions / GitLab CI); Docker Compose; skip Kubernetes until complexity justifies it
- **Multiple teams, shared platform** → invest in internal developer platform; standardize pipelines and observability
- **Compliance-heavy environment** → audit trails (GitOps); automated security scanning in every pipeline; SBOMs; signed artifacts
- **Frequent production incidents** → focus on observability and SLOs first, then improve change failure rate
- **Slow deployments** → analyze the pipeline: what takes longest? Tests? Approvals? Build? Optimize the bottleneck
- **"We do DevOps" but nothing improved** → assess CALMS honestly. Culture problems are not solved by tools

## Anti-patterns

- **Tools-first DevOps** — buying a CI/CD platform without changing culture, processes, or team structure
- **Everything in production** — no staging or canary environment; deploying untested changes directly
- **Manual snowflake servers** — servers configured by hand; impossible to reproduce; "works on my machine" in production
- **Alert fatigue** — hundreds of alerts, most ignored; alert on symptoms and SLO breaches, not every metric fluctuation
- **Security as afterthought** — no scanning until pre-release; discovered vulnerabilities require emergency fixes
- **Kubernetes cargo cult** — running K8s for a monolith with 2 instances; operational overhead exceeds benefit
- **Measuring vanity metrics** — lines of code, number of deployments without quality context, test count without coverage analysis
- **Change advisory board as bottleneck** — weekly approval meetings for every deployment; destroys lead time

## Sources

- Forsgren, N., Humble, J., & Kim, G. *Accelerate: The Science of Lean Software and DevOps.* IT Revolution, 2018. ISBN 978-1-942788-33-1
- Kim, G. et al. *The DevOps Handbook (2nd ed).* IT Revolution, 2021. ISBN 978-1-950508-40-4
- Beyer, B. et al. *Site Reliability Engineering.* O'Reilly, 2016. `https://sre.google/sre-book/table-of-contents/`
- DORA. *Accelerate State of DevOps Report 2024.* `https://dora.dev/research/2024/`
- DORA. *State of AI-assisted Software Development 2025.* `https://dora.dev/research/2025/dora-report`
- OpenGitOps v1.0.0. `https://opengitops.dev/`
- Atlassian. *CALMS Framework.* `https://atlassian.com/devops/frameworks/calms-framework`
- CNCF. *GitOps in 2025.* `https://www.cncf.io/blog/2025/06/09/gitops-in-2025/`
- Cross-reference: `.vaibe/skills/tech-stack-reference/SKILL.md` — project tech stack (Docker, K8s, GitLab CI)
- Cross-reference: `.vaibe/skills/software-architecture-patterns/SKILL.md` — architecture decisions that affect deployment
