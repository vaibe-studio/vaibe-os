---
name: stakeholder-analysis
description: Map and prioritize all stakeholders using influence/interest matrix
triggers: [stakeholder, стейкхолдер, stakeholder map, карта стейкхолдеров, заинтересованные стороны]
origin: bundled
---

# Purpose

Systematically identify, assess, and prioritize all stakeholders of a project or product. Produce an actionable stakeholder map with communication strategies per segment.

# When to use

- Starting a new project that involves external parties
- Preparing for sales/partnership outreach
- Analyzing decision-making structure of a target organization
- Planning communication strategy for a product launch

# Inputs needed

- Project/product description and goals
- Known stakeholders or target organizations
- Industry context (optional)

# Procedure

1. **Identify stakeholders** — list all parties: buyers, regulators, partners, competitors, end users, internal teams
2. **Assess each stakeholder** on two axes:
   - **Influence** (1-10): ability to affect decisions, budget, timelines
   - **Interest** (1-10): engagement level and relevance to the project
3. **Determine position**: Supportive / Neutral / Resistant / Rival
4. **Document** for each: role, expectations, concerns, preferred communication format
5. **Classify** into segments using the influence/interest matrix:

| Segment | Criteria | Strategy |
|---|---|---|
| A (key players) | Influence 7-10, Interest 7-10 | Active engagement: weekly meetings, joint planning, ROI demos |
| B (prospects with objections) | Influence 7-10, Neutral/Resistant | Technical deep-dives, compliance proofs, migration paths |
| C (low-value) | Low influence, high user interest | Standardize, self-service docs, focus on simplicity and price |
| X (monitor) | High regulatory influence | Monitor requirements, proactive compliance communication |

6. **Design communication plan** per segment: format, frequency, responsible person
7. **Present map** to user for validation

# Output format

Markdown document with:

1. **Stakeholder table** — columns: Name, Role, Influence (1-10), Interest (1-10), Position, Expectations, Concerns
2. **Prioritization matrix** — visual classification into A/B/C/X segments
3. **Communication plan** — per-segment strategy with format and frequency
4. **Recommendations** — top 3-5 actionable next steps

# Quality bar

- [ ] All key stakeholder categories covered (buyers, regulators, partners, competitors)
- [ ] Influence/interest scores are justified by role and context
- [ ] Position aligns with documented expectations and concerns
- [ ] Communication strategy matches the prioritization matrix
- [ ] Actionable recommendations provided (not just descriptive)

# Anti-patterns

- Listing stakeholders without scoring influence/interest
- Treating all stakeholders equally (no prioritization)
- Skipping the "concerns" column (leads to blind spots)
- Creating the map without validating with the user

# Related knowledge

- `pmbok7-principles.md` — Stakeholders performance domain, engagement assessment matrices
- `strategy-frameworks.md` — Value Proposition Canvas for mapping stakeholder needs
- `sales-methodologies.md` — MEDDPICC Champion/Economic Buyer identification for sales stakeholders
