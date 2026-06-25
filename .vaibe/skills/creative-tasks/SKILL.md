---
name: creative-tasks
description: Help with creative text under constraints — literary/artistic translation (songs, poetry, prose), song lyrics translation and songwriting, format adaptation (social posts, captions), slogans/naming, style rewriting. Triggers: переведи песню/стих, художественный перевод, напиши текст песни, songwriting, lyrics, слоган, нейминг, адаптируй под соцсети, стилизуй текст, creative writing.
license: MIT
---

# Creative tasks methodology

Help the user solve creative tasks — tasks with no single correct answer, subjective
quality criteria, soft or hard constraints, and an iterative result. The agent is a
**generator of structure and variants**; the user supplies taste and the final choice.

## When to use

- Artistic/literary translation (songs, poetry, prose) — with or without fitting music
- Writing original lyrics / songs from a prompt
- Adapting a text to a format (Telegram post, tweet, YouTube description)
- Slogans, naming, short-form copy under a brief
- Style rewriting (academic → conversational, "write like X")

## Core principles

1. **LLM = generator, not author** — it holds form and theme well but loses on
   creativity/emotion; generate the scaffold + material, the user brings the soul.
2. **Human input up front is critical** — the richer the user's prompt, the better.
3. **Explicit constraints beat vague requests** — form, rhyme scheme, syllable counts
   as concrete numbers *before* generation.
4. **Variants, not a single "right" answer** — 2–3 options for key lines, with the
   trade-off stated; the user collages and edits.
5. **Fix decisions in a table** (original → choice → rationale) for reproducibility.

## Procedure (universal constraint-driven frame)

1. **Constraint map** — list all constraints and their priority (hard / soft / user).
2. **Meaning map (EAPMT)** — explain each block first (literal sense, subtext, tone,
   cultural references), then generate. Especially for metaphors and cultural refs.
3. **Generate** — 2–3 variants for key points (hooks, repeats, vivid lines); a full
   draft for connective text; translate/write in **blocks** (section/stanza), not
   line-by-line.
4. **Score** — per variant: meaning accuracy, style fit, hard-constraint compliance,
   singability/rhythm and rhyme quality where relevant.
5. **Present & iterate** — show variants with trade-offs, take the user's choice/edit,
   record it, loop back as needed.
6. **Capture feedback** — choices, edits, rewrites become the user's creative profile
   for next sessions (the LLM has no cross-session memory → write it down).

## References and knowledge base

- `references/methodology.md` — the full methodology: detailed
  algorithms (literary translation simplified / under music, original songwriting
  10-step), prompt templates, the research review (EAPMT, Songs Across Borders, Sing
  it Narrate it, Translator's Canvas, LITRANSPROQA) and the meta-learning loop.
- `База знаний/Творчество/Рифмообразование — классификация и приёмы.md` — rhyme
  classification, masters' techniques, checklists.
- `База знаний/Творчество/Написание песен — методология и приёмы.md` — songwriting
  templates and exercises.
- `База знаний/Генерация авторских текстов — методология.md` — persona/avatar
  generation, editorial AI.
- Example breakdowns: `База знаний/Творчество/Примеры переводов — разбор.md`,
  `База знаний/Творчество/Референсная база переводов.md`.

## Output

- Final text + a decisions table (for reproducibility) + a feedback block (for
  meta-learning), per the methodology reference.
