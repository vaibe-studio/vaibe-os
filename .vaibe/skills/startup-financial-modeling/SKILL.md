---
name: startup-financial-modeling
description: Unit economics, P&L, pricing, cohort analysis, burn rate — startup financial modeling. Reference material (non-actionable knowledge).
license: MIT
---

# Startup Financial Modeling — Unit Economics, Revenue, and Viability

Practical reference for financial analysis in startups: unit economics, revenue modeling, pricing strategies, cohort analysis, and viability assessment. Enables the agent and user to build financial models, evaluate pricing decisions, and assess business health.

## When to use

- Calculating ROI or evaluating investment decisions (`roi-calculation`)
- Building or reviewing pricing strategy for a product
- Analyzing customer acquisition efficiency and retention
- Preparing financial models for investors or accelerators
- Evaluating startup viability or go/no-go decisions (`hypothesis-testing`)
- Cross-reference with startup resources: see `.vaibe/skills/market-research/references/startup-resources-ru.md`

---

## Unit economics fundamentals

Unit economics answers: **does the business make money on each customer?** If individual transactions are unprofitable, volume makes things worse, not better.

### Core formulas

| Metric | Formula | What it tells you |
|---|---|---|
| **CAC** (Customer Acquisition Cost) | Total Sales & Marketing Costs / New Customers Acquired | Cost to acquire one customer |
| **ARPU** (Average Revenue Per User) | Total Revenue / Active Users | Revenue per customer per period |
| **ARPA** (Average Revenue Per Account) | Total Revenue / Active Accounts | Revenue per account (B2B) |
| **MRR** (Monthly Recurring Revenue) | Active Customers × ARPU (monthly) | Predictable monthly revenue |
| **ARR** (Annual Recurring Revenue) | MRR × 12 | Annualized recurring revenue |
| **Gross Margin** | (Revenue − COGS) / Revenue | Profit before operating expenses |
| **LTV** (Lifetime Value) | (ARPA × Gross Margin %) / Monthly Churn Rate | Total profit from a customer over their lifetime |
| **LTV:CAC Ratio** | LTV / CAC | Return on customer acquisition investment |
| **CAC Payback** | CAC / (ARPU × Gross Margin %) | Months to recoup acquisition cost |
| **Contribution Margin** | Revenue − Variable Costs (per unit) | Profit per unit before fixed costs |

### LTV:CAC benchmarks

| Ratio | Interpretation |
|---|---|
| < 1:1 | Losing money on each customer — unsustainable |
| 1:1 – 3:1 | Marginal; need to improve retention or reduce CAC |
| **3:1 – 5:1** | **Healthy, sustainable growth** |
| > 5:1 | Excellent economics; may be under-investing in growth |

### CAC Payback benchmarks

| Payback period | Interpretation |
|---|---|
| < 6 months | Excellent |
| 6–12 months | Good (industry standard for SMB SaaS) |
| 12–18 months | Acceptable for enterprise SaaS |
| > 18 months | Concerning — cash-intensive growth |

### Common mistakes in unit economics

- **Under-counting CAC:** Omitting fully-loaded costs (sales salaries, onboarding, tooling, sales engineer time)
- **Optimistic churn assumptions:** Using best-month churn instead of average; inflates LTV dramatically
- **Ignoring gross margin:** LTV without gross margin is revenue, not profit
- **Blending channels:** Averaging CAC across organic and paid hides that paid channels may be unprofitable
- **Confusing MRR with cash:** Annual contracts create cash upfront but MRR accrues monthly

---

## Revenue metrics (SaaS / subscription)

### MRR components

| Component | Definition |
|---|---|
| **New MRR** | Revenue from new customers this month |
| **Expansion MRR** | Revenue increase from existing customers (upgrades, add-ons) |
| **Contraction MRR** | Revenue decrease from existing customers (downgrades) |
| **Churned MRR** | Revenue lost from cancelled customers |
| **Net New MRR** | New + Expansion − Contraction − Churned |

Healthy SaaS companies have **Net Revenue Retention (NRR) > 100%** — expansion from existing customers exceeds churn. Elite SaaS companies achieve NRR of 120%+.

### Churn metrics

| Metric | Formula | Interpretation |
|---|---|---|
| **Logo churn** (customer churn) | Customers Lost / Total Customers (start of period) | % of customers leaving |
| **Revenue churn** (MRR churn) | Churned MRR / Total MRR (start of period) | % of revenue leaving |
| **Net revenue churn** | (Churned MRR − Expansion MRR) / Total MRR | Can be negative if expansion > churn |

Revenue churn matters more than logo churn. Losing 10 small customers is different from losing 1 enterprise customer. Net negative churn is the gold standard.

---

## P&L structure for startups

### SaaS P&L template

```
Revenue
  - Subscription revenue (MRR × months)
  - Services / implementation revenue (if applicable)
  - Other revenue (usage overages, marketplace fees)
= Total Revenue

Cost of Goods Sold (COGS)
  - Hosting / infrastructure
  - Third-party API costs
  - Customer support (direct)
  - Payment processing fees
= Gross Profit (Gross Margin %)

Operating Expenses
  - Sales & Marketing (CAC-related)
    - Sales team compensation
    - Marketing spend (paid, content, events)
    - Sales tools and commissions
  - Research & Development
    - Engineering salaries
    - Product management
    - Design
    - Infrastructure (dev/test)
  - General & Administrative
    - Management
    - Legal, accounting
    - Office, insurance, corporate
= Operating Income (Loss) = EBITDA proxy

Other
  - Interest, depreciation, taxes
= Net Income (Loss)
```

### Key P&L ratios (benchmarks for venture-stage SaaS)

| Metric | Seed – Series A | Series B+ | Path to profitability |
|---|---|---|---|
| **Gross Margin** | 60–75% | 70–85% | 75%+ |
| **S&M as % of Revenue** | 50–100%+ | 30–50% | 20–30% |
| **R&D as % of Revenue** | 30–60% | 20–35% | 15–25% |
| **G&A as % of Revenue** | 15–30% | 10–20% | 8–15% |
| **Burn Multiple** | 2–5x | 1–3x | < 1.5x |

---

## Burn rate and runway

### Formulas

| Metric | Formula | Use |
|---|---|---|
| **Gross burn rate** | Total monthly expenses | Total cash outflow |
| **Net burn rate** | Monthly expenses − Monthly revenue | Actual cash consumption |
| **Runway (months)** | Cash balance / Net burn rate | Time until cash runs out |
| **Burn multiple** | Net burn / Net new ARR | Efficiency of growth spending |

### Burn multiple benchmarks

| Burn multiple | Interpretation |
|---|---|
| < 1.5x | Efficient — generating more ARR than burning cash |
| 1.5–3x | Acceptable — standard for growth-stage |
| 3–5x | Concerning — high spend relative to growth |
| > 5x | Unsustainable — burning cash without proportional growth |

### Runway planning rules of thumb

- **Raise to have 18–24 months of runway** — gives time to hit milestones and fundraise again
- **Below 12 months:** urgent — either fundraise, cut costs, or accelerate revenue
- **Below 6 months:** crisis — survival mode
- Month-by-month cash flow projection is more accurate than simple runway division (revenue growth, variable costs, one-time expenses)

---

## Cohort analysis

### What it is

Group customers by acquisition date (cohort) and track their behavior over time. Reveals retention patterns that aggregate metrics hide.

### How to build

1. **Define the cohort:** typically month of first purchase or activation
2. **Define the metric:** retention rate, revenue per cohort, usage frequency
3. **Build the triangle:** rows = cohort months, columns = months since acquisition, cells = metric value

### Reading the retention curve

```
Month 0   Month 1   Month 2   Month 3   Month 6   Month 12
100%      70%       60%       55%       48%       40%
```

- **Month 0 → Month 1 drop:** activation quality; are users finding value in the first session?
- **Month 1 → Month 3 slope:** product-market fit signal; steep decline = weak fit
- **Month 3+ flattening:** indicates a core user base that gets sustained value
- If the curve never flattens, there is a fundamental retention problem

### Cohort analysis questions

- Are newer cohorts retaining better than older ones? (improvement signal)
- Is revenue per cohort growing over time? (expansion/upsell working)
- Which cohort characteristics predict long-term retention? (segment for marketing)
- Where is the biggest drop-off? (focus improvement efforts there)

---

## Pricing strategies

### Models

| Model | How it works | Best for | Risk |
|---|---|---|---|
| **Tiered** | Multiple packages with increasing features/limits | Most SaaS; clear value ladder | Analysis paralysis if too many tiers |
| **Per-user (seat-based)** | Fixed fee per user | Collaboration tools, CRM | Penalizes adoption; users resist adding seats |
| **Usage-based** | Pay for consumption (API calls, data, compute) | Dev tools, AI APIs, infrastructure | Revenue unpredictability for both sides |
| **Flat-rate** | Single price, full access | Simple products, uniform usage | Leaves money on table from heavy users |
| **Freemium** | Free basic tier + paid premium | Products with network effects, viral loops | Low conversion (2–5%); needs volume |
| **Hybrid** | Base subscription + usage component | Becoming industry standard | Complexity in billing and communication |

### Pricing principles

- **Value metric alignment:** Charge for the thing customers value. If your pricing metric (seats) doesn't match your value metric (projects managed), customers feel penalized for success
- **1% pricing improvement → 11–13% profit improvement** — pricing is the highest-leverage growth lever
- **Revisit pricing regularly:** 57% of SaaS companies haven't changed pricing in the last year; companies that optimize see 30% higher growth
- **Price for the segment, not the average:** different customers derive different value; one price for all under-captures or over-charges
- **Test pricing before scaling:** pricing is a hypothesis, not a decision. Validate willingness to pay in customer discovery (see `.vaibe/skills/jtbd-custdev/SKILL.md`)

---

## Financial model structure (for fundraising)

### What investors expect to see

1. **Revenue model:** driver-based (not "we'll do $1M in year 2" but "100 customers × $10K ACV × 85% retention = ...")
2. **Unit economics:** CAC, LTV, payback, gross margin
3. **Growth assumptions:** customer acquisition rates by channel, conversion rates, expansion
4. **P&L projection:** 3–5 year monthly model
5. **Cash flow:** burn rate, runway, fundraise timing
6. **Key assumptions page:** explicit list of inputs and their basis (data, benchmarks, estimates)
7. **Sensitivity analysis:** what happens if churn is 2x? If CAC doubles? If growth is 50% of plan?

### Model hygiene

- Separate inputs (assumptions) from calculations
- Use named ranges or parameter cells — don't embed magic numbers
- Build scenarios: base, optimistic, pessimistic
- Show unit economics improving over time (or explain why not)
- Be honest about what is assumption vs what is validated

---

## Decision heuristics

- **LTV:CAC < 1** → stop spending on acquisition until you fix retention or ARPU
- **CAC payback > 18 months** → either find cheaper acquisition channels or raise prices
- **Gross margin < 60%** → business may not be SaaS; investigate COGS (maybe infrastructure costs are too high, or there's too much human services)
- **Net Revenue Retention < 100%** → revenue is shrinking inside existing accounts; focus on expansion and churn prevention before growth
- **Burn multiple > 5x** → growth is inefficient; either the market isn't ready, the product doesn't fit, or go-to-market is broken
- **All cohorts decline at the same rate** → systemic retention problem, not a segment issue. Fix the product or narrow the ICP
- **Pricing hasn't changed in 12+ months** → likely leaving money on the table. Test higher prices on new customers
- **Investors ask about unit economics and you don't know** → build the model before the pitch, not after

## Anti-patterns

- **Revenue-at-all-costs** — growing revenue while unit economics are negative; scaling losses
- **Vanity ARR** — counting one-time revenue or services as recurring; misleads investors and internal planning
- **Average everything** — using company-wide averages for CAC and LTV when segments have wildly different economics
- **Burn rate denial** — not tracking net burn monthly; surprised by cash running out
- **Pricing by cost-plus** — setting price based on what it costs you instead of what it's worth to the customer
- **Spreadsheet fiction** — financial model disconnected from operational reality; "hockey stick" projections without mechanism
- **Ignoring negative unit economics** — rationalizing "we'll fix it at scale"; unit economics usually get worse with scale, not better
- **Churn as inevitable** — accepting high churn instead of investigating root causes; retention is a solvable problem

## Sources

- SaaS Valuation. *CAC, LTV & Payback for Valuation.* `https://www.saasvaluation.app/resources/cac-ltv-payback-valuation`
- Calculates.dev. *CAC vs LTV: Complete Guide to Unit Economics 2025.* `https://www.calculates.dev/blog/cac-vs-ltv-complete-guide`
- Founderpath. *Burn Rate Calculator.* `https://founderpath.com/free-tools/burn-rate-calculator`
- Y Combinator. *Essential Startup Advice.* `https://www.ycombinator.com/library`
- Horowitz, B. *The Hard Thing About Hard Things.* Harper Business, 2014. ISBN 978-0-06-227206-8
- Croll, A. & Yoskovitz, B. *Lean Analytics.* O'Reilly, 2013. ISBN 978-1-449-33567-0
- Cross-reference: `.vaibe/skills/market-research/references/startup-resources-ru.md` — Russian startup ecosystem resources
- Cross-reference: `.vaibe/skills/jtbd-custdev/SKILL.md` — customer discovery and willingness-to-pay validation
- Cross-reference: `.vaibe/skills/sales-methodologies/SKILL.md` — pipeline metrics and deal velocity
- Cross-reference: `.vaibe/skills/strategy-frameworks/SKILL.md` — Lean Canvas, Business Model Canvas
