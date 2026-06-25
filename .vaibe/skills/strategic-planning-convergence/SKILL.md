---
name: strategic-planning-convergence
description: Why a strategic plan converges: meeting to plan to correction to rule loop; deadline-removal test. Reference material (non-actionable knowledge).
license: MIT
---

# Strategic Planning Convergence — the meeting → plan → correction → rule loop

Why a strategic plan converges on the user's real intent: not from more task metadata, but from closing a feedback loop between the user's *live reasoning* (captured in meetings) and the artifact, treating every human correction as a candidate durable rule. Derived from the vAIbe-studio planning session (01.06.2026) where plan v8 (built from task cards) was shallow and plan v9 (grounded in the meeting + a corrected priority rule) "fully matched the strategic goal".

## When to use

- Running `plan-update` (`.vaibe/skills/plan-update/SKILL.md`) for a strategic/checkpoint plan, especially when a recent meeting exists
- After a user corrects a plan's priorities — deciding whether to fix once or generalize into a rule
- Any `/evolve` (`.vaibe/skills/evolve/SKILL.md`) reflecting on *why* a planning session succeeded or failed
- `meeting-processing` (`.vaibe/skills/meeting-processing/SKILL.md`) — understanding why transcribing the live discussion is a high-value input, not just an archive

## The convergence loop

A plan is "right" when it survives one question: **would this still be the #1 priority if the nearest deadline vanished?** Reaching that state empirically follows a loop, not a single pass:

```
meeting (live human reasoning)
   → transcript/summary (externalized into vault)
      → plan v(N) grounded in that reasoning
         → human correction (catches urgent-vs-important inversion)
            → /evolve: correction generalized into a durable rule
               → plan v(N+1) re-grounded → converges
```

Each pass moves the artifact from **storage → context → anticipation** (Ontology maturity phases). The first pass built only from task-card metadata is reliably shallow because it lacks the "why" that lives in the dialogue.

### Mapping to the five ontological laws

All five fired together in the successful session — that co-occurrence *is* the secret:

| Law | How it showed up |
|---|---|
| 1. Externalization | The decisive input was the **meeting transcript**, not task cards — live reasoning made actionable in the vault |
| 2. Feedback | Human caught the inverted priority; system absorbed it **and** generalized it (positive feedback via `/evolve`) |
| 3. Source autonomy | Structured asks (AskQuestion) kept strategy with the human; agent did heavy lifting (N plans, transcription, link hygiene) without owning the call |
| 4. Directed evolution | Successive passes went shallow → deep: metadata → correction → rule → meeting capture → grounded re-plan |
| 5. Additivity | v8 corrected not deleted; v9 built on v8; the rule persisted in the skill; meeting archived |

### Recursion note (second-order cybernetics)

In the source session the processed meeting was itself a recording of the user running these very planning commands — the system processed a meeting in which the system was being used (von Foerster: the observer is inside the observed). This recursive coupling is the structural criterion of a "living" system in `.vaibe/rules/ontology.md`, observed in practice.

## Decision heuristics

- If a strategic/checkpoint plan is requested **and a recent meeting exists** → process the meeting *first*; ground priorities in its reasoning, not only the task board.
- If the plan was built from task-card metadata alone → treat it as a draft; expect a depth gap until validated against live reasoning.
- Before fixing #1, apply the **deadline-removal test**: if #1 would change when the nearest deadline disappears, it is *urgent*, not *important* — re-rank (Eisenhower; see `.vaibe/skills/pmbok7-principles/SKILL.md`, `.vaibe/skills/strategy-frameworks/SKILL.md`).
- Anchor #1 to the project **README goal** (root cause), not to the nearest symptom («нет выручки для гранта» is a symptom of «не запущены продажи»).
- When the user corrects a priority → ask "is this a one-off or a recurring trap?" If recurring → generalize into a skill rule via `/evolve`, don't just patch the file.
- A stated #1 priority with no task card in `Задачи/` is untracked → flag ⚠️ and recommend creating one.

## Anti-patterns

- **Metadata-only planning** — generating a strategic plan from task cards while ignoring a fresh meeting that contains the actual strategic "why". Produces plausible-but-shallow plans.
- **Deadline hijack** — letting the nearest external deadline (grant, demo day) crown itself #1 over the README goal. Most acute for checkpoint plans triggered *by* a deadline.
- **One-off patching** — fixing a corrected plan in place without asking whether the correction is a durable rule; the same mistake recurs next sprint.
- **Untracked priority** — declaring a #1 that has no task card, so it silently falls off the board.
- **Defending the first draft** — resisting the human correction instead of treating it as the highest-value signal in the loop.

## Cross-references

- `.vaibe/skills/plan-update/SKILL.md` — Eisenhower prioritization (Step 6, items 11–12), Batch mode, G4 pre-flight
- `.vaibe/skills/meeting-processing/SKILL.md` — capturing live reasoning into the vault
- `.vaibe/skills/batch-operations/SKILL.md` — verify-after-batch discipline (complementary, mechanics-level)
- `.vaibe/skills/strategy-frameworks/SKILL.md`, `.vaibe/skills/pmbok7-principles/SKILL.md` — Eisenhower, importance-vs-urgency, tailoring

## Sources

- vAIbe-OS Ontology — five laws: `.vaibe/rules/ontology.md` (v2, 2026-03-26)
- Eisenhower decision matrix — importance vs urgency (Eisenhower, 1954; popularized by Covey, *The 7 Habits of Highly Effective People*, 1989, ISBN 0-671-66398-4)
- Second-order cybernetics — Heinz von Foerster, *Understanding Understanding* (2003, ISBN 0-387-95392-2)
- Empirical basis: vAIbe-studio strategic planning session, 2026-06-01 (plan v8 → meeting 29 → plan v9), `/evolve` closure
