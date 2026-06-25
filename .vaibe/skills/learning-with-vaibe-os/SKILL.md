---
name: learning-with-vaibe-os
description: Educational workflow patterns for tutoring, revision notes, and storing learning materials in vAIbe-OS. Reference material (non-actionable knowledge).
license: MIT
---

# Learning with vAIbe-OS

Reference for educational workflows in vAIbe-OS: how to explain topics, structure revision notes, and store learning materials so they remain reusable over time.

## When to use

- Designing or refining educational workflows in vAIbe-OS
- Explaining theory, formulas, or concepts to a user
- Saving study materials into `База знаний/` or `Проекты/{NAME}/База знаний/`
- Creating new skills for tutoring, exam prep, revision, or structured learning
- Related skill: `study-session`

## Core principles

### 1. Learning materials should strengthen autonomy

Educational output is successful when the user can later solve similar problems with less help. This follows Ontology Law 3 (Source autonomy): the system should make the learner stronger, not more dependent.

### 2. Good study notes are not the same as long answers

A useful study note is:
- compact enough for revision;
- structured enough for scanning;
- specific enough to support future problem-solving;
- grounded in examples, not just abstract theory.

A long answer can be useful in chat but still be poor as a saved note.

### 3. Navigation and content should be separated

In a study knowledge base:
- `README.md` should act as a map of the section;
- theory should live in separate topic files;
- each topic file should cover one coherent concept or tightly related micro-cluster.

This improves retrieval, maintenance, and additive growth.

### 4. Explanation order matters

For most learners, the default order should be:

1. Intuition in plain language
2. Formal rule, definition, or formula
3. Worked example
4. Recognition heuristic
5. Compact recap

Starting with formal notation alone is often efficient for experts but suboptimal for learning.

### 5. Preview environment is part of the content design

Formula formatting should be chosen based on where the learner will read the material:
- if Markdown preview supports math rendering, proper LaTeX formulas should be the default, not a nice-to-have;
- for standalone formulas, use display blocks `$$ ... $$`;
- for multi-line groups of related formulas, prefer `aligned` inside one display block so notes read like a textbook, not like raw source;
- for short formulas inside prose, use inline LaTeX `\(...\)`;
- use standard math notation such as `\frac`, `\sqrt`, `x_1`, Greek letters, `\sin`, `\cos`, `\log`, `\pi` instead of ASCII approximations like `sqrt`, `x1`, `pi`, `+-`;
- if support is uncertain, hybrid formatting may be safer;
- if support is absent, plain-text formulas are better than broken notation.

The right representation is the one that remains understandable in the user's actual tool.

## Educational patterns

### Revision note pattern

Use when the user says things like:
- "сохрани для повторения"
- "нужен конспект"
- "напиши базовую теорию"

Recommended structure:
- what this topic is for;
- key formula or rule;
- variable meanings;
- one worked example;
- "how to recognize this type of problem";
- short recap.

When formulas are central to the note:
- present the main formula in rendered math, not inline ASCII;
- keep notation consistent across the file;
- add just enough prose around each formula so the learner remembers when it applies.

### Tutoring pattern

Use when the user wants to understand rather than just save.

Recommended flow:
- ask or infer the user's level;
- explain simply first;
- only then formalize;
- check whether the user wants deeper theory, more examples, or a saved note.

### Knowledge-base growth pattern

When a chat explanation proves useful, it can evolve into:
1. a topic note in project or personal knowledge base;
2. a navigation link from `README.md`;
3. a reusable system pattern or skill if it repeats across sessions.

This turns tutoring moments into additive system knowledge.

## Decision heuristics

- If the material is tied to one educational goal or project (e.g. exam prep) -> store it in `Проекты/{NAME}/База знаний/`
- If the material is broadly personal and reusable outside one project -> store it in `База знаний/`
- If the user asks for revision -> optimize for brevity and retrieval, not completeness
- If the user asks "объясни принцип" -> start with intuition, not notation
- If formulas are central -> verify how they render in the user's preview tool, then prefer textbook-like LaTeX formatting whenever rendering works
- If a topic note becomes long because it covers several different ideas -> split it into multiple files and keep `README.md` as navigation
- If content and navigation are mixed in one file -> move theory into topic files and leave links in `README.md`

## Anti-patterns

- **README as theory dump** — using `README.md` to store full study content instead of navigation
- **Broken formula formatting** — saving LaTeX syntax that the learner's viewer cannot read
- **ASCII math by habit** — using raw `sqrt`, `x1`, `pi`, `+-` in saved notes even though the viewer supports proper math rendering
- **Formula wall without grouping** — listing many formulas line by line when one aligned display block would be clearer
- **Theory without recognition cues** — explaining rules without helping the learner spot where to apply them
- **One giant note for everything** — merging unrelated topics into an unscannable file
- **Chat transcript as knowledge note** — saving conversational answers verbatim instead of curating them into revision-friendly structure

## Sources

- vAIbe-OS Ontology: `.vaibe/rules/ontology.md` — especially Law 3 (Source autonomy) and Law 5 (Additivity)
- vAIbe-OS Manifesto: `.vaibe/rules/manifesto.md` — development, mentorship, and "extension, not dependence"
- `.vaibe/skills/knowledge-curation/SKILL.md` — storage, maintenance, and additive evolution of knowledge artifacts
