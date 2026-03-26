# Agile Frameworks — Practical Reference

Practical guide to Scrum, Kanban, Scrumban, and scaled approaches. Enables the agent and user to select the right delivery framework, apply its mechanics correctly, and measure progress with appropriate metrics.

## When to use

- Selecting a delivery approach for a new project or workstream (`plan-update`)
- Structuring sprint or iteration plans (`task-create`, `plan-update`)
- Conducting or preparing for retrospectives, reviews, daily standups (`weekly-review`, `daily-briefing`)
- Choosing metrics to track delivery health (`tasks-report`)
- Tailoring methodology to team size, volatility, or regulatory context

## The Agile Manifesto — foundation

Four values (2001):

1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

The right side still has value; the left side has *more* value.

Twelve principles behind the manifesto emphasize: early and continuous delivery, welcoming changing requirements, frequent delivery (weeks not months), daily collaboration between business and developers, motivated individuals, face-to-face conversation, working software as primary measure, sustainable pace, technical excellence, simplicity, self-organizing teams, and regular reflection.

## Scrum (Scrum Guide 2020)

### Three pillars

- **Transparency** — significant aspects visible to those responsible for outcomes
- **Inspection** — frequent examination of artifacts and progress toward goals
- **Adaptation** — adjust process when results deviate from acceptable limits

### Five values

Commitment, Focus, Openness, Respect, Courage.

### Three accountabilities

| Role | Responsibility |
|---|---|
| **Product Owner** | Maximizes product value; manages Product Backlog; accountable for ordering and clarity of backlog items |
| **Scrum Master** | Accountable for Scrum effectiveness; serves the team, Product Owner, and organization; removes impediments |
| **Developers** | Create the Increment each Sprint; self-managing; cross-functional; no sub-teams or hierarchies |

The Scrum Team is a cohesive unit — typically 10 or fewer people.

### Events

| Event | Time-box | Purpose |
|---|---|---|
| **Sprint** | 1–4 weeks (fixed) | Container for all other events; produces a Done Increment |
| **Sprint Planning** | Max 8 hours (for 1-month Sprint) | Define Sprint Goal; select backlog items; plan how to deliver |
| **Daily Scrum** | 15 minutes | Inspect progress toward Sprint Goal; adapt the plan for the day |
| **Sprint Review** | Max 4 hours | Inspect the Increment; adapt the Product Backlog based on feedback |
| **Sprint Retrospective** | Max 3 hours | Inspect the Sprint; identify improvements for next Sprint |

### Artifacts and commitments

| Artifact | Commitment |
|---|---|
| **Product Backlog** | **Product Goal** — long-term objective for the Scrum Team (new in 2020) |
| **Sprint Backlog** | **Sprint Goal** — single objective for the Sprint; provides coherence and focus |
| **Increment** | **Definition of Done** — formal quality standard; when met, the Increment is releasable |

### When Scrum fits best

- Product development with discoverable requirements
- Team of 3–9 developers, co-located or collaborative
- Stakeholders available for regular feedback (at least every Sprint Review)
- Organization tolerates empirical, iterative delivery
- Need for predictable cadence and sprint-level forecasting

## Kanban

### Core practices (Kanban Guide 2025)

1. **Define and visualize a workflow** — columns represent states; cards represent work items; shared understanding of process
2. **Actively manage items in workflow** — control WIP; pull work when capacity exists; never push
3. **Improve flow** — continuous optimization using systems thinking, lean principles, queuing theory

### Key concepts

**WIP limits** — cap on items per workflow state. Forces focus on finishing over starting. Practical guidance: start with current throughput minus ~20%; adjust iteratively. Research shows proper WIP limits can increase throughput by ~40% and reduce lead time by up to 60%.

**Pull system** — work is pulled by downstream capacity, not pushed by upstream demand. Prevents overloading and exposes bottlenecks.

**Explicit policies** — visible rules governing how items move between states (entry criteria, exit criteria, priority lanes).

### Essential metrics

| Metric | Definition | Use |
|---|---|---|
| **Lead time** | Time from request creation to delivery | Customer-facing; measures responsiveness |
| **Cycle time** | Time from work start to completion | Team-facing; measures process efficiency |
| **WIP** | Count of items in active states | Health indicator; should stay near WIP limits |
| **Throughput** | Items completed per time unit | Capacity indicator; enables forecasting |

### When Kanban fits best

- Continuous flow work (operations, support, maintenance)
- Unpredictable or interrupt-driven workload
- Team already has a process worth optimizing (Kanban is a change method, not a framework)
- Need to visualize and improve existing workflow without wholesale process change
- Multiple service classes with different urgency levels

## Scrumban

Hybrid combining Scrum's structure with Kanban's flow optimization.

### From Scrum

- Time-boxed iterations (can be longer than typical Scrum sprints)
- Standups, retrospectives
- Sprint Goal or iteration theme

### From Kanban

- Visual board with WIP limits
- Pull-based flow within iterations
- Continuous backlog grooming (on-demand, not ceremony-driven)

### When Scrumban fits best

- Scrum feels too rigid, Kanban too loose
- Maintenance + feature development in same team
- Transitioning from Scrum to Kanban (or vice versa)
- Requirements change frequently within iterations
- Team managing simultaneous initiatives of different nature

## Scaled approaches (overview)

### SAFe 6.0 (Scaled Agile Framework)

For enterprises needing coordination across multiple teams. Four configurations:

| Configuration | Scale | Use when |
|---|---|---|
| **Essential** | 50–125 people | Starting point; single Agile Release Train (ART) |
| **Large Solution** | Multiple ARTs | Complex multi-team solutions with supplier coordination |
| **Portfolio** | Enterprise alignment | Strategic portfolio management, Lean budgeting |
| **Full** | 500+ people | All of the above combined |

Key concepts: Agile Release Train, Program Increment (PI) Planning, DevSecOps, Continuous Delivery Pipeline, Lean-Agile leadership.

SAFe is appropriate when: multiple teams must coordinate on a shared product, enterprise governance is required, and the organization is willing to invest in significant structural change.

### Other scaled frameworks (brief)

- **LeSS (Large-Scale Scrum)** — minimalist scaling; multiple teams, one Product Owner, one Product Backlog; avoids additional roles/artifacts
- **Nexus** — Scrum.org's scaling framework; 3–9 Scrum Teams, Nexus Integration Team, cross-team refinement
- **Spotify Model** — organizational design (Squads, Tribes, Chapters, Guilds); not a methodology but a culture model; widely misapplied as a framework

## Velocity vs throughput — choosing the right metric

| Dimension | Velocity | Throughput |
|---|---|---|
| Unit | Story points per sprint | Work items per time period |
| Requires | Estimation (story points) | Consistent "done" definition |
| Best for | Sprint planning, capacity forecasting | Flow optimization, delivery forecasting |
| Framework fit | Scrum | Kanban, Scrumban |
| Limitation | Cannot compare across teams; encourages point inflation | Requires comparable work item sizes for accuracy |
| Forecasting | Sprint-level ("how much can we take?") | Date-level ("when will it be done?") — Monte Carlo simulations |

**Recommendation:** Use velocity for sprint-level planning within a stable Scrum team. Use throughput + cycle time for delivery forecasting and flow optimization. Never use either to compare teams or measure individual performance.

## Mapping to vAIbe-OS

| Agile concept | vAIbe-OS element |
|---|---|
| Sprint planning | `plan-update` skill; Планы/ sprint plans |
| Daily standup | `daily-briefing` skill |
| Sprint retrospective | `weekly-review` skill |
| Product Backlog | Project Задачи/ folder; `task-create` skill |
| Sprint Backlog | Weekly management table (`weekly-operating-sheet`) |
| Definition of Done | `## Статус` section in `task.md`; acceptance criteria |
| Increment | `results/v1/`, `v2/` versioned deliverables |
| WIP management | Risks/blockers column in management week plans |
| Kanban board | YouTrack integration (`yt-project-tasks-push/pull`) |

## Decision heuristics

- **Stable team, clear product vision, regular stakeholder access** → Scrum
- **Operations, support, maintenance, interrupt-driven** → Kanban
- **Mixed work: features + maintenance + incidents** → Scrumban
- **Multiple teams on shared product, enterprise governance needed** → SAFe Essential or LeSS
- **Existing process works but needs optimization** → Kanban (overlay, not replacement)
- **Requirements highly volatile within iteration** → shorten sprint length or move to Kanban
- **Team new to agile** → start with Scrum (more structure); graduate to Kanban as maturity grows
- **Regulated environment** → Scrum with explicit Definition of Done including compliance checks; or SAFe for audit trails

## Anti-patterns

- **Cargo-cult Scrum** — performing ceremonies without empiricism; standups become status reports to management; retrospectives produce no improvements
- **Zombie Kanban** — board exists but nobody manages WIP; no pull discipline; no flow metrics
- **Sprint scope change** — adding work mid-sprint without removing equivalent items; destroys Sprint Goal coherence
- **Estimation fetishism** — spending more time estimating than building; points become political currency
- **Scaling prematurely** — adopting SAFe for 2 teams; overhead exceeds coordination value
- **Ignoring the Manifesto** — implementing Agile ceremonies while maintaining command-and-control culture; process without values
- **Velocity as KPI** — using velocity to measure team performance or compare teams; drives gaming behavior
- **No Definition of Done** — "done" means different things to different people; quality erodes; technical debt accumulates

## Sources

- Schwaber, K. & Sutherland, J. *The Scrum Guide.* November 2020. `https://scrumguides.org/scrum-guide.html`
- *The Kanban Guide.* May 2025. `https://kanbanguides.org/the-kanban-guide/2025.5/`
- Beck, K. et al. *Manifesto for Agile Software Development.* 2001. `https://agilemanifesto.org/`
- Scaled Agile, Inc. *SAFe 6.0 Framework.* `https://framework.scaledagile.com/`
- Anderson, D.J. *Kanban: Successful Evolutionary Change for Your Technology Business.* Blue Hole Press, 2010. ISBN 978-0-9845214-0-1
- Atlassian. *Kanban Metrics.* `https://www.atlassian.com/agile/project-management/kanban-metrics`
- Atlassian. *Scrumban.* `https://www.atlassian.com/agile/project-management/scrumban`
- PMBoK 7 principles reference: see `pmbok7-principles.md` in this knowledge base
