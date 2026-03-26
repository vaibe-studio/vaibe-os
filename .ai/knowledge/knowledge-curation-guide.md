# Knowledge Curation Guide — How to Maintain the Knowledge Base

Meta-knowledge file that defines how to add, update, and maintain references in `.ai/knowledge/`. Ensures consistency, quality, and alignment with vAIbe-OS ontology across all knowledge files.

## When to use

- Adding a new knowledge file to `.ai/knowledge/`
- Updating an existing knowledge file with new information
- Evaluating whether information belongs in knowledge vs skills vs project base
- Running the `evolve` skill when it involves knowledge changes (see `.ai/skills/core/evolve.md`)
- Reviewing knowledge base health during system evolution

---

## Where knowledge lives

| Location | Purpose | Audience | Maintained by |
|---|---|---|---|
| `.ai/knowledge/` | System-level reference materials | Agent + human | `/evolve` skill |
| `База знаний/` | User's personal knowledge | Human (agent reads) | User |
| `Проекты/{NAME}/База знаний/` | Project-specific knowledge | Team members | Project team |
| `.ai/skills/` | Actionable playbooks | Agent | `/evolve` skill |
| `.ai/rules/` | Behavioral constraints | Agent | `/evolve` skill |

**Key distinction:** Knowledge files are **non-actionable reference** — they inform decisions but don't prescribe step-by-step procedures. Skills are **actionable** — they define procedures with inputs, steps, outputs, and quality bars.

If the content answers "how do I do X step-by-step?" → it's a **skill**.
If the content answers "what should I know to make better decisions about X?" → it's **knowledge**.

---

## Required structure for new knowledge files

Every file in `.ai/knowledge/` must follow this template:

```markdown
# {Title}

{1-2 sentence purpose statement: what this reference enables.}

## When to use

- {Situation 1 where this knowledge is relevant}
- {Situation 2}
- {Links to relevant skills: `skill-name` in .ai/skills/}

## {Core content sections — topic-specific}

{Organized by logical sections. Tables for comparisons.
Decision heuristics for practical guidance.}

## Decision heuristics

- {If X → consider Y}

## Anti-patterns

- {Common mistake 1 — why it's wrong}

## Sources

- {Verified reference with URL or ISBN}
```

### Required fields

| Field | Purpose | Notes |
|---|---|---|
| **Title** | Clear, descriptive | Should be findable by scanning file list |
| **Purpose statement** | 1–2 sentences | What the agent/user can do better with this knowledge |
| **When to use** | Trigger situations | Links to relevant skills for discoverability |
| **Core content** | The substance | Structured, scannable, evidence-based |
| **Decision heuristics** | Practical "if-then" guidance | Most valuable section for the agent |
| **Anti-patterns** | Common mistakes | Prevents misapplication |
| **Sources** | Verified references | URLs, ISBNs, publication dates |

### Optional fields

| Field | Purpose | When to include |
|---|---|---|
| **Mapping to vAIbe-OS** | How concepts connect to system elements | When the knowledge domain directly maps to vAIbe-OS features |
| **Selection guide** | Comparison table for choosing between alternatives | When the file covers multiple frameworks or tools |
| **Cross-references** | Links to other knowledge files | When concepts span multiple files |

---

## Quality criteria

Every knowledge file is evaluated against these criteria:

### 1. Grounded in sources

- Every factual claim should trace to a verifiable source
- Sources include: published standards, peer-reviewed research, canonical books, official documentation
- Mark the distinction between facts, best practices, and opinions
- Use confidence tags when appropriate: `[established]` / `[emerging practice]` / `[author's synthesis]`

### 2. Dual-audience readability

The file must be useful to both:
- **Human reader:** Can find what they need in 30 seconds. Tables, headers, and heuristics enable scanning. No wall-of-text paragraphs.
- **AI agent:** Can extract actionable guidance for task execution. Decision heuristics are explicit. Cross-references to skills are present.

### 3. Actionability

Knowledge should change behavior. Each section should pass the test: "If I read this, would I make a different decision than before?"

Passive knowledge (pure theory without application guidance) is less valuable. Always include decision heuristics and anti-patterns.

### 4. No redundancy

Check existing files before creating new content. If information overlaps:
- Reference the existing file instead of duplicating
- Add a cross-reference in both files
- Only duplicate when the information needs a fundamentally different framing for the new context

### 5. Additive evolution (Ontology Law 5)

Changes to knowledge files must be additive or refining — never destructive:
- Add new sections, don't delete existing ones without migration
- Update outdated information with new data, preserving the previous understanding as context
- If a concept is superseded (e.g., PMBoK 7 → PMBoK 8), document the evolution, don't erase the predecessor

---

## How to add a new knowledge file

### Step 1 — Evaluate the need

Before creating a new file, answer:
1. Does this knowledge already exist in `.ai/knowledge/`? → Cross-reference instead
2. Is this actionable procedure? → Create a skill in `.ai/skills/`, not knowledge
3. Is this project-specific? → Put it in `Проекты/{NAME}/База знаний/`
4. Is this personal to the user? → Put it in `База знаний/`
5. Will this be useful across multiple projects and contexts? → `.ai/knowledge/` is the right place

### Step 2 — Research

- Search for authoritative sources (standards, canonical texts, official documentation)
- Verify facts against multiple sources
- Note publication dates — freshness matters for fast-moving fields
- Identify the best existing frameworks and models, don't invent new ones unless necessary

### Step 3 — Draft using the template

Follow the required structure above. Focus on:
- Purpose statement that explains the "why"
- Decision heuristics that make the knowledge actionable
- Anti-patterns that prevent misuse
- Cross-references to related knowledge files and skills

### Step 4 — Self-review

Before saving, check:
- [ ] Purpose statement is clear and specific
- [ ] "When to use" links to relevant skills
- [ ] Every factual claim has a source
- [ ] Decision heuristics are concrete ("if X → Y"), not vague
- [ ] Anti-patterns are based on real mistakes, not theoretical warnings
- [ ] No redundancy with existing knowledge files
- [ ] Cross-references added to both files (bidirectional)
- [ ] Language is English (matching `.ai/` convention)
- [ ] Human can find key info in 30 seconds (scan test)
- [ ] Agent can extract guidance for task execution (actionability test)

### Step 5 — Update the glossary (GUARDS G9)

If the new file introduces terms not yet in `glossary.md`, add them with:
- English term
- Russian translation
- Concise definition
- Reference to the new knowledge file

This is enforced by **Guard G9** (`.ai/GUARDS.md`) — the agent will warn about missing glossary entries.

### Step 6 — Update router and skills

If the new knowledge file should be referenced during skill execution:
- Update `.ai/router.md` Knowledge Base table
- Add a `## Related knowledge` entry in relevant domain skills (`.ai/skills/domain/`)

---

## How to update an existing knowledge file

### When to update

- New edition of a standard or framework is released (e.g., PMBoK 8)
- Research reveals outdated or incorrect information
- User feedback or project experience reveals gaps
- New cross-references need to be added
- Terminology has evolved

### Update protocol

1. Read the existing file completely before making changes
2. Check against Ontology (`ONTOLOGY.md`) and Manifesto (`MANIFESTO.md`) — see `evolve.md`
3. Add new information rather than replacing (document evolution)
4. Update the Sources section with new references and dates
5. Update `glossary.md` if terminology changed
6. Document the change reason (in commit message or inline note)

---

## Versioning and freshness

### Freshness indicators

Knowledge files don't have formal version numbers, but freshness can be tracked through:
- **Git history:** last modified date, commit messages
- **Sources section:** most recent source date indicates how current the content is
- **Explicit notes:** "As of March 2026, PMBoK 8 has been released..." provides temporal context

**Guard G8** (`.ai/GUARDS.md`) enforces freshness: files not modified for 18+ months are flagged during `weekly-review`.

### Review cadence

| Knowledge type | Suggested review frequency | Trigger for urgent review |
|---|---|---|
| Standards and regulation (ISO, NIST, EU AI Act) | Every 6 months | New version published |
| Methodologies (Scrum, DDD, JTBD) | Annually | Major guide update |
| Metrics and benchmarks | Every 6 months | New annual report (DORA, etc.) |
| Technology practices (DevOps, architecture) | Annually | Major ecosystem shift |
| Sales and financial models | Annually | Market condition change |
| Glossary | Continuously | New knowledge file added |

---

## Relationship to `/evolve` skill

Knowledge creation and update is a form of system evolution governed by the `/evolve` skill (`.ai/skills/core/evolve.md`). When using `/evolve` for knowledge changes:

1. Classify the insight as **knowledge** (not practice/optimization/fix)
2. Check against five ontological laws — especially:
   - **Law 3 (Source autonomy):** Does this make the user more competent, not more dependent?
   - **Law 5 (Additivity):** Is this additive, not destructive?
3. Plan the change: which files, what content, what cross-references
4. Execute and document

---

## Anti-patterns in knowledge curation

- **Knowledge hoarding** — gathering information without structuring it for retrieval; raw notes are not knowledge
- **Theory without heuristics** — explaining a framework without practical "when to use" and "when not to use" guidance
- **Source amnesia** — adding claims without traceable sources; erodes trust over time
- **Stale references** — citing sources from 5+ years ago in fast-moving fields without noting potential obsolescence
- **Duplication drift** — same concept explained differently in multiple files without cross-references; leads to inconsistency
- **Knowledge for knowledge's sake** — adding a file because the topic is interesting, not because it serves a project or skill need
- **Perfectionism paralysis** — not publishing knowledge until it's "complete"; good-enough knowledge today is better than perfect knowledge never

## Sources

- vAIbe-OS Ontology: `.ai/ONTOLOGY.md` — five laws governing system evolution
- vAIbe-OS Manifesto: `.ai/MANIFESTO.md` — behavioral principles
- Evolve skill: `.ai/skills/core/evolve.md` — procedure for system self-improvement
- GUARDS: `.ai/GUARDS.md` — machine-checkable integrity rules (G7: knowledge protection, G8: freshness check, G9: glossary sync)
