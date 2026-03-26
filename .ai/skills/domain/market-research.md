---
name: market-research
description: Conduct market research with defensible TAM/SAM/SOM and competitive analysis
triggers: [market research, TAM, SAM, SOM, competitors, market size, landscape]
origin: bundled
---

# Purpose

Produce defensible market sizing (TAM/SAM/SOM), competitive landscape, and actionable insights for product and sales strategy.

# When to use

- Sizing a new market or validating existing estimates
- Preparing investor materials with market data
- Competitive analysis for positioning
- Building go-to-market strategy

# Procedure

## Step 1 — Define market boundaries

Before any calculations, fix "what exactly we count as market" and why it's comparable with competitors and client budgets.

- Define primary market segment (e.g., MarTech, CPaaS)
- Define adjacent segments
- **Rule:** if both segments appear in one document, don't mix TAMs — show two parallel frames with explicit overlap

## Step 2 — Calculate TAM/SAM/SOM using 2+ methods

1. **Top-down** (from external market estimates):
   - Use 2–3 independent sources (analyst reports, industry reviews)
   - Adjust for geography and currency
   - Separate "market estimate" from "player revenue" from "IT spend"

2. **Bottom-up** (from target company count × typical deal):
   - Estimate number of companies in ICP (by segments)
   - Estimate typical ACV/ARR from public pricing/cases/interviews
   - Calculate range and sensitivity to key assumptions

3. **Sanity checks**:
   - Compare SAM with industry IT spend, marketing budgets, key player revenue
   - Verify SOM is realistic given sales channels, deal cycle, team resources

**Definitions:**
- **TAM** — total demand assuming perfect availability
- **SAM** — part of TAM product can serve (geography/ICP/regulation/channels)
- **SOM** — realistic SAM share over 3–5 years given GTM and competition

## Step 3 — Source quality and traceability

Maintain source registry:
- Link, publication date, what it confirms, trust level (High/Medium/Low), limitations

**Rule:** any number in the final report must have a source OR be marked "estimate/assumption" with derivation formula.

## Step 4 — Produce standard artifacts

- **Market landscape**: players, segments, positioning, GTM
- **Competitor matrix**: features/integrations/security/SLA/scale
- **Pricing benchmark**: monetization models, price ranges, what's included
- **Trends & drivers**: 5–10 trends and their demand impact
- **Barriers & risks**: regulation, integrations, procurement, security
- **TAM/SAM/SOM sheet**: formulas, assumptions, ranges, sensitivity

## Step 5 — Translate to action

- Define 2–3 focus zones (ICP + segments) with prioritization rules
- Extract proof points for sales (case, savings metrics, SLA, load)
- Convert findings to backlog: what to improve and what to prove

# Output format

- Market research document with all artifacts from Step 4
- Source registry (table with links, dates, trust levels)
- TAM/SAM/SOM calculations with formulas and assumptions

# Quality bar

- [ ] 2+ calculation methods used with sanity check
- [ ] All numbers have sources or marked as assumptions
- [ ] Cost saving and revenue opportunities separated
- [ ] Competitor matrix covers key dimensions
- [ ] Actionable focus zones defined

# Anti-patterns

- Single-method TAM without cross-validation
- Numbers without sources or assumption labels
- Mixing TAM across different market definitions
- Research without actionable conclusions
- Ignoring adjacent segments that affect positioning

# Related knowledge

- `strategy-frameworks.md` — Porter's Five Forces for industry analysis, SWOT for positioning, Blue Ocean for differentiation
- `jtbd-custdev.md` — Jobs-to-be-Done for understanding customer needs behind market demand
- `startup-financial-modeling.md` — TAM/SAM/SOM validation with unit economics and pricing models
- `startup-resources-ru.md` — Russian market research sources, venture analytics, HSE data
