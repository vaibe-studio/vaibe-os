---
name: expert-selection
description: Select and prioritize experts for consultations based on scoring criteria
triggers: [expert, consultation, mentor, advisor, competence, scoring]
origin: bundled
---

# Purpose

Select the most relevant experts to get practical recommendations, validate hypotheses, and accelerate project development at the current stage.

# When to use

- Seeking external expertise for a project
- Choosing mentors/advisors for a specific stage
- Prioritizing which consultations to pursue first

# Procedure

## Step 1 — Analyze current project stage

- Identify key tasks for the upcoming period
- Find competence gaps in the team
- Formulate 3–5 specific questions for experts

## Step 2 — Score each expert (1–10 scale)

**Criterion 1: Expertise relevance**
- 1–3: adjacent but not target areas
- 4–6: partial match
- 7–8: direct match to key needs
- 9–10: unique expertise in target area

**Criterion 2: Practical value**
- 1–3: theoretical knowledge, no practical experience
- 4–6: experience in other contexts, needs adaptation
- 7–8: relevant hands-on experience with similar products/markets
- 9–10: direct experience solving analogous problems in target segments

**Criterion 3: Expertise uniqueness**
- 1–3: general competence (many have it)
- 4–6: specific but alternatives exist
- 7–8: rare combination
- 9–10: unique expertise

**Overall priority** = average of three criteria + urgency adjustment

## Step 3 — Build TOP list

- Select 3–5 experts
- Ensure coverage of different competencies
- Avoid duplication

## Step 4 — Prepare for consultations

For each selected expert:
- Formulate 3–5 key questions
- Prepare materials (presentation, metrics, hypotheses)
- Define expected consultation outcome

# Output format

1. **Comparison table** — all experts with scores per criterion
2. **Detailed analysis** — description of each expert with score justification
3. **TOP list** — ranked priority experts with consultation plan

# Quality bar

- [ ] All experts scored on 3 criteria
- [ ] TOP list covers diverse competencies (no duplication)
- [ ] Specific questions prepared for each selected expert
- [ ] Expected outcomes defined

# Anti-patterns

- Selecting experts without clear questions to ask
- Choosing based on name recognition without scoring
- Duplicate competencies in TOP list
- No preparation materials for consultations

# Related knowledge

- `jtbd-custdev.md` — interview techniques for structuring expert consultation questions
- `pmbok7-principles.md` — Stakeholder engagement principles for expert relationship management
- `strategy-frameworks.md` — frameworks to focus expert consultation scope (Porter, Wardley Maps)
