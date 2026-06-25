---
name: roi-calculation
description: Build ROI business case for B2B sales with cost saving and revenue uplift. Triggers: ROI, business case, cost saving, revenue uplift, payback, CFO.
license: MIT
---

# Purpose

Translate product value into financial language (ROI, payback period, NPV) to accelerate deal cycles and pass CFO/procurement approval.

# When to use

- Preparing business case for enterprise deal
- Justifying product cost to CFO/finance
- Comparing with alternatives (competitors, in-house, status quo)
- Defining KPIs for pilot/POC
- Supporting negotiation with transparent economics

# Procedure

## Step 1 — Separate Cost Saving from Revenue Uplift

CFO and analysts trust these differently. Always calculate and present separately.

**Cost Saving (hard savings)** — easier to prove:
- Channel cost reduction (e.g., cascade logic: push/email → SMS)
- Operational cost reduction (FTE/hours on manual work)
- TCO reduction (replacing existing systems/subscriptions)

**Revenue Uplift (soft gains)** — need more evidence:
- Campaign conversion uplift (personalization, timing)
- Churn reduction from relevant communications

## Step 2 — Choose pricing model

| Model | Components | When to use |
|---|---|---|
| **Simple (ACV)** | Annual contract + one-time onboarding | Early negotiations, quick estimate |
| **Hybrid** | Platform fee + usage + SLA tier/add-ons | Detailed business case, large deals |

## Step 3 — Build 3 scenarios

Always present a range:
- **Conservative** — minimum benefits, maximum costs
- **Base** — realistic scenario
- **Aggressive** — optimistic with full potential

**Rule:** explicitly document all assumptions and data sources. If no client data — use benchmarks marked "requires validation."

## Step 4 — Calculate metrics

1. **ROI%** = (Benefits − Costs) / Costs × 100% — show separately for Cost Saving, Revenue Uplift, and total
2. **Payback Period** = Costs / (Benefits / 12 months)
3. **NPV** — for 3–5 year horizon (configurable discount rate)

## Step 5 — Collect client data (checklist)

**For Cost Saving** (CTO/IT/Operations):
- Current message volume/month and cost per message
- Push/email/messenger volume (cascade potential)
- FTE/hours on communication management
- Current system costs (subscriptions, infra, development)

**For Revenue Uplift** (CMO/CRO):
- Current campaign conversion (baseline)
- Average check/margin
- Churn rate and customer base/revenue
- Target conversion and retention KPIs

## Step 6 — Map to sales funnel

| Stage | How to use ROI |
|---|---|
| Discovery | Collect input data |
| Qualification | Preliminary ROI to confirm fit |
| Business Case | Detailed calculation with client data, CFO presentation |
| POC/Pilot | Define pilot KPIs from ROI metrics |
| Negotiation | Justify price/terms |
| Procurement | Final ROI document |

# Output format

- ROI calculator (spreadsheet or markdown table) with Inputs/Scenarios/Outputs
- Methodology document (formulas and assumptions)
- Optional: presentation template for CFO

# Quality bar

- [ ] Cost saving and revenue uplift separated
- [ ] Three scenarios (conservative/base/aggressive) present
- [ ] All assumptions documented with sources
- [ ] ROI%, Payback Period calculated
- [ ] Data collection checklist completed (or gaps noted)

# Anti-patterns

- Mixing cost saving and revenue uplift in one number
- Missing assumptions and data sources
- Single scenario instead of range
- Ignoring TCO (comparing only subscription vs subscription)
- ROI without timeline (when will the effect materialize)

# Related knowledge

- `.vaibe/skills/startup-financial-modeling/SKILL.md` — unit economics (CAC, LTV, payback), P&L structure, pricing strategies
- `.vaibe/skills/strategy-frameworks/SKILL.md` — Business Model Canvas for mapping value creation and cost structure
- `.vaibe/skills/sales-methodologies/SKILL.md` — MEDDPICC Metrics element for grounding ROI in buyer's numbers
