---
name: hypothesis-testing
description: Formulate, score, and test product hypotheses using HADI methodology. Triggers: hypothesis, гипотеза, HADI, validate, проверка гипотезы, product hypothesis.
license: MIT
---

# Purpose

Structure and test product hypotheses (segment, problem, solution, value, channel, monetization) using the HADI framework: Hypothesis, Action, Data, Insight.

# When to use

- Validating a new product idea or pivot
- Testing assumptions about target segments or problems
- Evaluating channels, pricing, or value propositions
- Prioritizing which hypotheses to test first

# Inputs needed

- Product/project description
- Target segment (or candidates)
- Known assumptions to validate
- Available resources and timeline for testing

# Procedure

1. **Identify hypothesis type** — classify what needs testing:

| Type | Tests | Template |
|---|---|---|
| Problem | Does the problem exist? | "We believe [segment] faces [problem], causing [damage]" |
| Segment | Is this the right audience? | "We believe [segment] is ideal because [characteristics]" |
| Solution | Does our solution work? | "We believe [solution] solves [problem] by [mechanism]" |
| Value | Is the value sufficient? | "We believe [value] for [segment] measured by [metrics]" |
| Channel | Is the channel effective? | "We believe [channel] will reach [segment] with [efficiency]" |
| Monetization | Will they pay? | "We believe [pricing model] is optimal for [segment]" |

2. **Formulate hypothesis** using the template:
   > We believe that **[segment]** faces **[problem]**, causing **[damage]**.
   > Our solution **[solution]** delivers **[value]**.
   > If **[action]**, then **[expected result]**.

3. **Score and prioritize** (sum of three scores, higher = higher priority):
   - **Revenue impact** (1-3): 1 = minor, 3 = affects entire business
   - **Ease of testing** (1-3): 1 = expensive/slow, 3 = cheap/fast
   - **Confidence** (0-3): 0 = don't believe (skip), 3 = almost certain

4. **Plan the test** (Action):
   - What exactly to do (concrete, measurable)
   - Timeline (start/end dates)
   - Who is responsible
   - Success criteria

5. **Collect data** (Data):
   - Record what happened: numbers, facts, feedback
   - Compare against success criteria

6. **Extract insights** (Insight):
   - Confirmed or not?
   - What did we learn?
   - What additional questions emerged?

7. **Make a decision** (Decision):
   - What changes in product/sales/priorities based on results?

# Output format

Markdown document with:

1. **Hypothesis card** — type, formulation using template, scoring table
2. **Test plan** — action, timeline, success criteria
3. **Results** (after testing) — data collected, insights, decision
4. **Next hypotheses** — follow-up questions to test

# Quality bar

- [ ] Hypothesis uses the structured template (segment + problem + damage + solution + value)
- [ ] Scoring is filled in for all three dimensions
- [ ] Success criteria are measurable and concrete
- [ ] Test plan has timeline and responsible person
- [ ] Decision section exists (what changes based on results)

# Anti-patterns

- Vague hypotheses without measurable criteria ("users will like it")
- Testing multiple hypotheses at once (isolate variables)
- Skipping the scoring step (leads to testing low-priority hypotheses first)
- Not documenting negative results (they are equally valuable)

# Related knowledge

- `.vaibe/skills/jtbd-custdev/SKILL.md` — JTBD theory, Customer Development, HADI cycles, hypothesis formulation, interview techniques, pivot criteria
- `.vaibe/skills/strategy-frameworks/SKILL.md` — Lean Canvas, Value Proposition Canvas for framing hypotheses in business model context
- `.vaibe/skills/startup-financial-modeling/SKILL.md` — unit economics benchmarks for validating financial hypotheses
