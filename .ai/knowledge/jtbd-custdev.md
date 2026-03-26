# JTBD and Customer Development — Hypothesis-Driven Product Discovery

Practical reference for understanding customer needs through Jobs-to-be-Done theory and validating product hypotheses through Customer Development methodology. Enables the agent and user to structure interviews, formulate testable hypotheses, interpret evidence, and decide when to pivot or persevere.

## When to use

- Formulating or testing product hypotheses (`hypothesis-testing`)
- Conducting market research or competitive analysis (`market-research`)
- Preparing for or processing customer/expert interviews (`meeting-processing`, `expert-selection`)
- Analyzing stakeholder needs and motivations (`stakeholder-analysis`)
- Evaluating MVP scope or pivot decisions (`mvp-development`)
- Building or refining value propositions

## Part 1: Jobs-to-be-Done (JTBD)

### Core premise

People don't buy products — they hire them to make progress in specific circumstances. Theodore Levitt: "People don't want a quarter-inch drill. They want a quarter-inch hole." Christensen extended this: customers pull products into their lives to resolve a struggle.

The unit of analysis is the **job**, not the customer segment, the product, or the technology.

### Two schools of JTBD

| Dimension | Supply-side (Ulwick / ODI) | Demand-side (Moesta / Christensen) |
|---|---|---|
| Focus | Functional job + measurable outcomes | Struggling moment + forces of progress |
| Method | Quantitative outcome surveys | Qualitative switch interviews |
| Output | Opportunity scores for underserved needs | Buying timeline + causal forces |
| Best for | Systematic innovation pipeline | Understanding why people switch |
| Key text | *What Customers Want* (Ulwick, 2005) | *Competing Against Luck* (Christensen, 2016) |

Both are complementary, not contradictory. Use demand-side to discover struggling moments and switching triggers; use supply-side to quantify and prioritize opportunities.

### The job structure

A complete job-to-be-done has layers:

1. **Core functional job** — the task the customer is trying to accomplish (e.g., "manage my team's work across projects")
2. **Desired outcomes** — measurable criteria for success tied to the functional job (e.g., "minimize time to see who is blocked")
3. **Related jobs** — adjacent tasks triggered before, during, or after the core job
4. **Emotional jobs** — how the customer wants to feel (confident, in control, not anxious)
5. **Social jobs** — how the customer wants to be perceived by others
6. **Consumption chain jobs** — purchase, learn, set up, maintain, upgrade, dispose

### The job map (Ulwick)

Every functional job follows eight universal steps. Use this to identify innovation opportunities at each stage:

1. **Define** — determine goals and plan the approach
2. **Locate** — gather items and information needed
3. **Prepare** — set up the environment and inputs
4. **Confirm** — verify readiness before execution
5. **Execute** — perform the core task
6. **Monitor** — track whether execution is on track
7. **Modify** — make adjustments based on monitoring
8. **Conclude** — finish, clean up, confirm success

### Opportunity algorithm (ODI)

`Opportunity = Importance + (Importance − Satisfaction)`

- Importance and Satisfaction rated 1–10 by customers
- High importance + low satisfaction = underserved (innovate here)
- Low importance + high satisfaction = overserved (simplify or reduce cost)
- High importance + high satisfaction = table stakes (maintain, don't differentiate)

### Forces of progress (Moesta)

Four forces govern every product switch:

**Demand-generating forces (push toward change):**
- **Push of current situation** — frustration, pain, inadequacy of status quo
- **Pull of new solution** — attraction to imagined better state

**Demand-reducing forces (pull back to status quo):**
- **Anxiety of new solution** — fear of unknown, switching cost, risk of failure
- **Habit of the present** — comfort, inertia, "good enough" mindset

A switch happens only when generating forces exceed reducing forces. Product strategy must amplify push/pull and reduce anxiety/habit.

### Switch interview technique

Reconstruct the timeline of an actual purchase decision. Interview people who recently switched (bought your product or a competitor's). Focus on real behavior, not hypotheticals.

Timeline structure:
1. **First thought** — when did dissatisfaction begin?
2. **Passive looking** — awareness of alternatives without active search
3. **Active looking** — deliberate comparison and evaluation
4. **Decision** — commitment to switch
5. **Consumption** — using the new solution
6. **Satisfaction** — does the new solution resolve the original struggle?

10 well-selected switch interviews typically reveal 3–5 distinct buying patterns covering ~90% of the market.

## Part 2: Customer Development (Blank)

### Core premise

Startups fail not because they can't build products, but because they build products nobody wants. Customer Development is a parallel process to Product Development that tests business model hypotheses before scaling.

### The four steps

| Step | Goal | Key activity | Exit criteria |
|---|---|---|---|
| **Customer Discovery** | Understand the problem and customer | Problem + solution interviews | Problem-solution fit confirmed |
| **Customer Validation** | Test the business model | Sell the MVP; test channels, pricing | Repeatable sales process found |
| **Customer Creation** | Drive demand at scale | Marketing, PR, sales scaling | Scalable customer acquisition |
| **Company Building** | Transition from startup to company | Organization, processes, culture | Functional departments established |

Steps 1–2 are the **search** phase (iterate, pivot). Steps 3–4 are the **execution** phase (scale what works). Most premature failures happen because teams skip to step 3 before validating step 2.

### Problem interview

**Purpose:** Validate that the problem exists, is painful, and is inadequately solved today.

Structure:
1. Context — who is this person? what do they do?
2. Problem exploration — describe the top problems in this area
3. Current solutions — how do they solve it today?
4. Pain and frequency — how often? how costly?
5. Ranking — which problem is most acute?

Rules:
- Do NOT pitch your solution
- Ask about past behavior, not future intent
- Listen for emotion and specificity
- Minimum 10 interviews before drawing conclusions

**Success criteria:** 70%+ of interviewees confirm the problem exists; clear economic or emotional impact; current solutions are materially inadequate.

### Solution interview

**Purpose:** Test whether your proposed solution resonates before building.

Structure:
1. Recap the validated problem
2. Present the solution concept (demo, mockup, story)
3. Observe reaction — does the person lean in or politely nod?
4. Test willingness to pay — "would you pay $X for this?" or better, "can I sign you up today?"
5. Identify objections and gaps

**Success criteria:** Genuine excitement (not politeness); willingness to commit (time, money, access); specific feature requests that align with validated problem.

### Pivot types

| Pivot | Trigger | Action |
|---|---|---|
| **Customer segment** | Right problem, wrong customer | Find who has this problem most acutely |
| **Problem** | Customers have a different, bigger problem | Redefine the core job-to-be-done |
| **Solution** | Problem confirmed, solution doesn't resonate | Redesign the approach; keep the problem |
| **Channel** | Product works, can't reach customers | Change distribution or sales channel |
| **Revenue model** | Value delivered, pricing doesn't work | Change pricing structure, monetization |
| **Value capture** | Growth without revenue | Add revenue stream, change business model |
| **Engine of growth** | Wrong growth strategy | Switch between viral, sticky, or paid growth |
| **Platform** | Technology enables new approach | Rebuild on different platform or architecture |
| **Complete** | Fundamental assumption wrong | Start over with a new hypothesis |

Pivoting is not failure — it is the mechanism of learning. But pivot only based on evidence, not opinion.

## Part 3: Hypothesis formulation

### Structure of a testable hypothesis

```
We believe that [customer segment]
has a problem with [specific struggle]
because [root cause].
If we provide [solution concept],
they will [expected behavior / measurable outcome].
We will know this is true when [validation metric] reaches [threshold].
```

### HADI cycles

Used in ФРИИ accelerator methodology and lean startup practice:

1. **Hypothesis** — what we believe and why
2. **Action** — what we will do to test it
3. **Data** — what we will measure
4. **Insight** — what we learned; next hypothesis

Each cycle should be as short as possible (days, not weeks). Document every cycle. Failed hypotheses are as valuable as confirmed ones — they narrow the search space.

### Confidence levels for evidence

| Level | Evidence type | Confidence |
|---|---|---|
| 0 | Founder's intuition | Very low — must validate |
| 1 | Desk research, analogies | Low — directional only |
| 2 | Problem interviews (10+) | Medium — problem validated |
| 3 | Solution interviews with commitment signals | Medium-high — solution resonates |
| 4 | Pre-sales, LOIs, paid pilots | High — willingness to pay confirmed |
| 5 | Repeatable sales with healthy unit economics | Very high — business model validated |

## Decision heuristics

- **"Everyone has this problem"** → warning sign. Narrow the segment. Find the 10 people who have it worst
- **Polite positive feedback in interviews** → does not count as validation. Look for specificity, emotion, and commitment signals
- **Multiple pivots without progress** → re-examine whether the job-to-be-done is real; consider complete pivot
- **Problem confirmed but no one will pay** → the problem may be real but not valuable enough; test higher-value segments or adjacent jobs
- **Strong pull for solution but high anxiety** → focus on reducing switching cost, risk, and onboarding friction
- **Users love the product but churn** → core job may be episodic; look for ways to expand to adjacent jobs or create habit loops

## Anti-patterns

- **Building before validating** — investing engineering effort before problem-solution fit; most expensive way to learn
- **Survey validation** — using surveys with leading questions to "confirm" hypotheses; surveys measure stated preference, not behavior
- **Friendly-customer bias** — interviewing friends, family, or fans who will always be positive; use strangers with the right job
- **Solution-first thinking** — falling in love with the solution before understanding the job; reverses causality
- **Vanity metrics** — tracking sign-ups, page views, or downloads instead of activation, retention, and revenue
- **Interview-then-ignore** — conducting interviews as a checkbox exercise without changing plans based on findings
- **Premature scaling** — investing in growth before finding repeatable, profitable unit economics

## Sources

- Christensen, C.M., Hall, T., Dillon, K., & Duncan, D.S. *Competing Against Luck.* Harper Business, 2016. ISBN 978-0-06-243561-9
- Ulwick, A.W. *What Customers Want.* McGraw-Hill, 2005. ISBN 978-0-07-140895-5
- Ulwick, A.W. *Jobs to be Done: Theory to Practice.* IDEA BITE PRESS, 2016. ISBN 978-0-9909191-3-2
- Blank, S. *The Four Steps to the Epiphany.* K&S Ranch, 2013 (2nd ed). ISBN 978-0-9893164-0-1
- Blank, S. & Dorf, B. *The Startup Owner's Manual.* K&S Ranch, 2012. ISBN 978-0-9849993-0-9
- Ries, E. *The Lean Startup.* Crown Business, 2011. ISBN 978-0-307-88789-4
- Moesta, B. & Spiek, C. *Demand-Side Sales 101.* Lioncrest Publishing, 2020. ISBN 978-1-5445-0959-4
- Klement, A. *When Coffee and Kale Compete.* 2018. `https://jtbd.info/`
- ФРИИ HADI cycles: `https://www.iidf.ru/media/articles/lifehacks/hadi-tsikly-5-layfkhakov/`
- Strategyn ODI: `https://strategyn.com/white-papers/what-is-outcome-driven-innovation/`
- HBS Startup Guide — Customer Interviewing: `https://startupguide.hbs.edu/product/customer-problem-fit/`
