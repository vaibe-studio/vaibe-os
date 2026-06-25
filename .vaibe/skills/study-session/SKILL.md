---
name: study-session
description: Explain topics at the learner's level, build concise study notes, and save educational materials into the right knowledge-base structure. Use when the user wants to learn a topic, prepare for an exam, create a revision note, or asks for a theory explanation.
triggers: [study, learn, explain, exam prep, revision, tutoring, егэ, огэ, подготовка, теория, конспект, повторение, учеба, обучение]
origin: evolved
license: MIT
---

# Purpose

Turn a one-off explanation into structured learning: adapt to the user's level, explain the topic clearly, reinforce it with an example, and optionally save the result as a reusable knowledge note.

# When to use

- User wants to understand a topic, formula, or concept
- User is preparing for an exam, interview, or structured study goal
- User asks for a concise theory note "for revision" or "to remember later"
- User wants to save educational material into `База знаний/` or `Проекты/{NAME}/База знаний/`

# Inputs needed

- Topic or problem to explain
- User's goal: understand / practice / revise / save notes
- Current level, if known (school / beginner / advanced)
- Target storage location, if the user wants the result saved

# Procedure

## Step 1 — Clarify the learning goal

Determine which of these is primary:
- **Understand** — the user wants intuition and plain-language explanation
- **Solve** — the user wants a method for tasks/problems
- **Revise** — the user wants a short reusable note
- **Save** — the user wants the material stored in the knowledge base

If the user's level is unclear and it matters, ask briefly before going deep.

## Step 2 — Explain in learning order

Default sequence:

1. **Plain-language intuition** — what the idea means
2. **Formal rule / formula** — the exact notation
3. **Worked example** — one short example from start to finish
4. **Recognition heuristic** — how to notice this type of task in the future
5. **Compact recap** — the key takeaway in 2-5 lines

Do not start with pure formalism unless the user explicitly asks for it.

## Step 3 — Match depth to the user's goal

- If user says "объясни принцип" -> prefer intuition first
- If user says "напиши основные формулы" -> prioritize concise formula sheet
- If user says "для повторения" -> write compactly, not as an essay
- If user seems stuck -> reduce abstraction and use a simpler example
- If user wants rigor -> keep intuition, but add formal definitions

## Step 4 — Decide where the material should live

Use:
- `Проекты/{NAME}/База знаний/` for project-specific study tracks (e.g. exam prep, course, certification)
- `База знаний/` for reusable personal learning materials not tied to one project

Storage rule:
- `README.md` = navigation / overview page
- Topic theory = separate file per topic

Do not place full educational content inside `README.md` unless the user explicitly wants a tiny one-page overview.

## Step 5 — Plan before writing

If the user wants the material saved:

1. Show the target path
2. Show the planned file name
3. Summarize what the note will contain
4. Confirm before creating or restructuring files

If the material already exists in a poor place (e.g. embedded in `README.md`), prefer:
- move theory to a dedicated topic file
- keep `README.md` as a map with links

## Step 6 — Format for readability in the target viewer

If formulas matter:

- In vAIbe-OS study notes, default to rendered math notation, not ASCII math
- Use display LaTeX blocks (`$$ ... $$`) for standalone formulas and formula groups
- Use inline LaTeX (`\(...\)`) for short formulas inside prose
- If several related formulas belong together -> prefer `aligned` inside one display block
- Use standard mathematical notation (`\frac`, `\sqrt`, subscripts like `x_1`, Greek letters, `\sin`, `\log`, `\pi`) instead of ad-hoc ASCII spellings like `sqrt`, `x1`, `pi`, `+-`
- Keep one short prose sentence before or after a formula block when it helps the learner understand what the formula is for
- Fall back to hybrid or plain-text formulas only if the user's actual preview environment fails to render math correctly

Optimize for the viewer the user actually uses, not for theoretical Markdown purity.

## Step 7 — Save and link

When writing educational notes:

- Keep the note focused on one topic
- Use short sections and examples
- Link the topic from the local `README.md`
- Avoid duplicating the same theory across multiple overview files

# Output format

- Clear explanation in chat, matched to the user's level
- If saved: one topic file per concept plus a navigational link from the relevant `README.md`

# Quality bar

- [ ] Explanation starts from the user's likely level, not from maximal formalism
- [ ] At least one worked example is included when the topic is procedural
- [ ] The note is concise enough for revision
- [ ] `README.md` is used as navigation, not as a dump for full theory
- [ ] Formula rendering is chosen for the user's actual preview environment
- [ ] When math rendering is available, formulas are written in proper LaTeX rather than ASCII approximations
- [ ] Multi-line formula groups are visually organized, preferably with `aligned`
- [ ] Educational material is stored in the correct knowledge base scope

# Anti-patterns

- Starting with dense formal definitions before building intuition
- Writing a long essay when the user asked for a revision note
- Storing full theory inside `README.md`
- Using broken or unreadable formula syntax in the target preview
- Writing math-heavy notes in ASCII notation when rendered LaTeX is available
- Mixing display formulas and prose in a visually messy way when a grouped `aligned` block would be clearer
- Mixing multiple unrelated topics into one note without navigation

# Related knowledge

- `.vaibe/skills/learning-with-vaibe-os/SKILL.md` — educational patterns, storage heuristics, formula rendering strategy
- `.vaibe/skills/glossary/SKILL.md` — term disambiguation when study content uses specialized vocabulary
- `.vaibe/rules/mentorship.md` — user-sensitive explanation style and calibration
