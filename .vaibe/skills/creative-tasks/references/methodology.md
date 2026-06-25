# Creative tasks — meta-mind methodology

> How to help the user solve creative tasks: literary translation, text adaptation,
> creating content under constraints.
>
> Example outputs (song-translation lines, sample messages) are kept in Russian — they
> demonstrate the Russian-language craft for a Russian-speaking user; the surrounding
> prose and the algorithms are the (English) doctrine.

## The nature of creative tasks

Creative tasks differ from technical ones:
- **No single correct answer** — many valid solutions
- **Quality criteria are subjective** — taste, style, context
- **Constraints may be soft or hard** — from "preserve the meaning" to "fit exactly 8 syllables"
- **Iterativeness** — the result improves through edits and feedback

## Types of creative tasks

| Type | Examples | Key constraints |
|------|----------|-----------------|
| Literary translation | Songs, poetry, prose | Meaning, style, rhythm (if to music) |
| Adaptation to a format | Social-media text, captions | Length, tone, platform |
| Creation from scratch (short form) | Slogans, names, descriptions | Brief, audience, tone |
| **Creation from scratch (song)** | **Original songs from a prompt** | **Form, genre, rhyme, melodics, style** |
| Style rework | Academic → conversational | Preserve meaning, change delivery |

---

## Algorithm: literary translation (simplified)

*When fitting music is not required — only meaning, structure, and stylistics.*

### Step 1: Analyze the original
```
- Meaning core: what is the text really about?
- Style core: tone, register (conversational/rough/poetic)
- Structure: verses, choruses, repeats, key phrases
- Cultural markers: slang, references, profanity
```

### Step 2: Define the translation boundaries
```
- Level of roughness: preserve / soften / amplify
- Register: conversational Russian / literary / slang
- Compression: Russian is often longer — can it be compressed?
```

### Step 3: Variants for key lines
For **hooks, repeats, and the most vivid phrases** — offer 2–3 translation variants:
- with a different word order
- with a different degree of roughness / literalness
- with a different rhythm (even if the translation is not to music — the user may know the rhythm)

Format:
```
Оригинал: I'ma fuck up my life
  а) Я проебал свою жизнь — прямой мат, ритмически плотно
  б) Я себе жизнь угроблю — грубо, но без мата
  в) Я просру свою жизнь — мат, другой оттенок (будущее время)
```

The user chooses, relying on their feel for the text and (if any) knowledge of the melody.

### Step 4: Draft by blocks
- Translate in meaning blocks, not word-for-word
- First the key phrases and hooks (from step 3)
- Then fill the connective tissue

### Step 5: Stylistic check
- Profanity and roughness — at one level across the whole song
- Conversational — without "bookish" turns
- Imagery — does it work in Russian? (metaphors, idioms)

### Step 6: Decision table (optional)
- For disputable spots — explicitly fix the choice and rationale
- Helps in iterations and discussion with the user

---

## Algorithm: literary translation (to music)

*When the text must be sung to the same melody.*

### Additional constraints
1. **Syllable count** — the number of syllables per phrase
2. **Stresses** — the stressed syllable = the musical accent
3. **Singability** — on long notes, vowels, not consonant clusters
4. **Hooks** — repeats must be memorable

### Method
1. Mark up the vocal track: syllables, accents, pauses
2. Write a "skeleton" to the rhythm (placeholders by syllable)
3. Replace with meaning words preserving the stresses
4. Compress: Russian is longer — remove the excess
5. Check by voice: sing it 3–5 times, fix the "stumbling" spots

---

## Algorithm: creating an original song

*The full cycle from the user's prompt to the final text. The detailed methodology, prompt templates, examples, and exercises — in `База знаний/Творчество/Написание песен — методология и приёмы.md`.*

### Difference from translation

In translation there is an original that sets the structure, rhythm, rhyme scheme, and meaning. When creating from scratch — all of that is defined by the author (the user + meta-mind). This gives freedom but requires more decisions up front.

### Algorithm

#### Step 1: Decompose the prompt
Break the user's prompt into 6 axes: theme, mood, genre, audience, perspective, constraints. If the prompt is abstract — ask clarifying questions or offer 3 concretizations.

#### Step 2: Object Writing (optional)
Brainstorm through 7 senses (Pat Pattison): sight, hearing, smell, touch, taste, organic sense, kinesthetics. The goal — sensory material for imagery.

#### Step 3: Meaning map
The emotional route (from → to), key images (3–5), forbidden zones.

#### Step 4: Structure and constraint map
Choose the form (verse-chorus, through-composed, narrative…). Define what happens in each part. Fix the constraints (hard / soft / user).

> **Critical**: define the form **before** generating text. The LLM gets 80% of syllables wrong without explicit constraints (Song Form-Aware, 2024).

#### Step 5: Anchor rhyme pairs
Key theme words → rhyme pairs (Marshak's approach: rhyme is the first step, not the last). Use the classification from `База знаний/Творчество/Рифмообразование — классификация и приёмы.md`.

#### Step 6: Generate the hook / chorus
2–3 variants of different types (slogan, paradox, question, image, statement). The user chooses.

#### Step 7: Generate verses and bridge
By blocks, with variants for key lines. The user collages and edits.

#### Step 8: Prosody check
- Do all elements support the main idea? (Pattison)
- Is the phonetics clean? Vowels in the long spots?
- Is the rhyme non-trivial, reinforcing the meaning?
- Is the hook memorable?
- Emotional route: is there development?

#### Step 9: Iteration
The user's edits → new variants for specific spots → repeat steps 6–8 as needed.

#### Step 10: Final
The final text + the decision table + feedback (for meta-learning).

### Three key principles (from research)

1. **The LLM = a generator of structure and variants, not the author** — the LLM holds form and theme excellently but loses on creativity and emotion (POEMetric, ICLR 2026). meta-mind generates the frame + material, the user — the soul.

2. **Human input up front is critical** — GPT-4 is more creative with human titles than with its own (EMNLP 2024). The richer the user's prompt, the better the result.

3. **Explicit constraints > vague requests** — form, rhyme scheme, meter — set with concrete numbers before generation (Song Form-Aware, 2024; Songs Across Borders, 2023).

---

## Principles of meta-mind working with creative tasks

### 1. Do not impose a single variant
- Offer 2–3 variants with a different degree of freedom
- Explain the trade-off: "more literal, but less natural"

### 2. Fix decisions
- A table "original → decision → rationale"
- Helps the user understand the logic and edit precisely

### 3. Ask about boundaries
- "Сохранить мат или смягчить?"
- "Приоритет — точность или естественность?"

### 4. Iterativeness
- The first draft is not the final
- Readiness to edit by specific lines

### 5. Acknowledge subjectivity
- "Это моя интерпретация; твой вкус может отличаться"
- Do not defend your variant — offer alternatives

---

## Anti-patterns

| ❌ Don't | ✅ Do instead |
|---------|---------------|
| One "correct" translation | Several variants + rationale |
| Ignore profanity/roughness | Ask the level, preserve the style |
| Literal translation of idioms | Find an equivalent in the target language |
| Defend your variant | "Можем поменять, если не заходит" |
| Long explanations without variants | First a variant, then — if needed — an explanation |

---

## Research: LLMs and literary translation (2023–2025)

> A review of academic work with practical takeaways for meta-mind.

### 1. EAPMT — "Explain, then translate" (Wang et al., 2024)

**Source**: [What is the Best Way for ChatGPT to Translate Poetry?](https://arxiv.org/abs/2406.03450) — ACL 2024

**Essence**: Instead of directly translating a poem — first ask the LLM to **explain the meaning** of each stanza in the source language, then use that explanation as context for the translation.

**Result**: Surpasses ChatGPT's direct translation and online translators. Confirmed by a panel of professional poets + GPT-4.

**Application for meta-mind**:
- Before translating — create a "meaning map": what each stanza means, which images, what subtext
- Feed this map as context into the translation prompt
- Especially useful for complex metaphors and cultural references

### 2. Songs Across Borders — constraints as prompts (Ou et al., 2023)

**Source**: [Songs Across Borders: Singable and Controllable Neural Lyric Translation](https://aclanthology.org/2023.acl-long.27/) — ACL 2023 | [GitHub](https://github.com/Sonata165/ControllableLyricTranslation)

**Essence**: Song translation is formalized as a **constraint task**. Translation theory is converted into concrete prompt constraints: syllable count, rhyme scheme, word boundaries.

**Result** (EN→ZH): 99.85% length accuracy, 99% rhyme accuracy, 95.52% word-boundary recall.

**Application for meta-mind**:
- Explicitly state constraints in the prompt: "exactly N syllables", "rhyme AABB", "stress on the 3rd syllable"
- The more concrete the constraints — the better the result (vague requests give trivial text)
- For translation to music — mark up the constraints per line, then feed into the prompt

### 3. Sing it, Narrate it — quality + singability (Ye et al., 2024)

**Source**: [Sing it, Narrate it: Quality Musical Lyrics Translation](https://arxiv.org/abs/2410.22066) — EMNLP 2024

**Essence**: A two-stage approach: (1) a reward model for automatic translation-quality scoring, (2) inference-time optimization for whole songs (not line-by-line).

**Application for meta-mind**:
- Translate the **whole song / section**, not line-by-line — preserves coherence
- After the draft — score quality separately by axis: meaning, style, singability
- Iteratively improve by the weak axis

### 4. The Translator's Canvas — LLM as a tool, not a replacement (Resende & Hadley, 2024)

**Source**: [The Translator's Canvas](https://aclanthology.org/2024.amta-research.16/) — AMTA 2024

**Essence**: The LLM works best as a **helper tool** for the translator (generating variants, rhyme hints, alternative formulations), not as an autonomous translator. Post-editing the LLM output is often harder than translating from scratch.

**Application for meta-mind**:
- The LLM's role = a **variant generator**, the final decision is the user's
- Don't try to hand over a "finished translation" — provide material for choosing
- Offer rhymes, synonyms, word orders — the user assembles the final

### 5. LITRANSPROQA — evaluating literary translation (2025)

**Source**: [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1482.pdf)

**Essence**: A new metric for evaluating literary translation through professional questions. Focus on: literary devices, cultural context, the author's voice. Standard metrics (BLEU et al.) overrate machine-translation quality.

**Application for meta-mind**:
- Evaluate the translation not by "similarity to the original" but by: (1) preservation of devices, (2) cultural adaptation, (3) the author's voice
- Mechanical accuracy ≠ artistic quality

---

## Practical takeaways for prompting

Based on the research — a checklist for meta-mind in creative translation:

1. **Explain first, then translate** (EAPMT): create a meaning map of the original
2. **Explicit constraints in the prompt** (Songs Across Borders): syllables, rhymes, stresses — concrete numbers
3. **Whole section, not a line** (Sing it, Narrate it): translate in blocks for coherence
4. **The LLM = a variant generator** (Translator's Canvas): not a "finished translation" but material to choose from
5. **Score by 3 axes** (LITRANSPROQA): devices + culture + voice, not a BLEU score

---

## Meta-learning architecture

> Not only "how to translate", but "how meta-mind accumulates mastery through practice".

### The learning cycle

```
Practice → Capture → Generalize → Integrate → Apply
    ↑                                            |
    └────────────────────────────────────────────┘
```

**Practice** — performing a creative task together with the user: generating variants, getting the choice and edits.

**Capture** — recording the user's decisions: what they chose, rejected, rewrote from scratch, and why (if they explained).

**Generalize** — finding recurring patterns. "The user always prefers X over Y in context Z" → formulate a rule.

**Integrate** — saving via `/evolve` into the knowledge base: updating default parameters, expanding examples, refining algorithms.

**Apply** — using the accumulated in the next session. Explicitly state: "Ориентируюсь на твой стиль из перевода Joji — скорректируй, если этот текст другой".

### What to capture after each creative session

| Signal | Example | How to use |
|--------|---------|------------|
| Variant choice | Chose (а) of three | Increase the weight of similar variants |
| Text edit | Changed «проебал» to «просрал» | Adjust the roughness default |
| Rejecting a variant | "Слишком литературно" | Lower the formality |
| Explanation | "Мне важнее ритм, чем точность" | Update the constraint priorities |
| Rewriting from scratch | Their own line variant | Analyze the difference, extract a pattern |

### The principle of gradual calibration

meta-mind **does not try to guess** everything in the first session. Calibration happens iteratively:

1. **First translation** — working on defaults + actively asking for preferences
2. **Second translation** — using patterns from the first, fewer questions
3. **N-th translation** — a stable profile, questions only on a new genre/style

The key: the LLM has no memory between sessions → the profile must be **explicitly written** to the knowledge base and **explicitly loaded** into context.

### Storage

- Translation examples: `База знаний/Творчество/{Артист} - {Песня} (перевод).md`
- Example breakdowns: `База знаний/Творчество/Примеры переводов — разбор.md`
- Reference base: `База знаний/Творчество/Референсная база переводов.md`
- Patterns and rules: updating this file via `/evolve`

---

## Unified framework: a creative task with constraints

> Any creative task is text generation in a space of constraints. A single framework instead of separate algorithms.

### The model

```
Inputs:
  ├── Source material (original / brief / task)
  ├── Constraints (hard + soft + user)
  └── Context (genre, audience, platform, history)

Process:
  1. Analysis → Meaning map + Constraint map
  2. Generation → Variants (2–3 at key points)
  3. Evaluation → Along the constraint axes
  4. Iteration → User's edits → New variants

Output:
  ├── Final text
  ├── Decision table (for reproducibility)
  └── Feedback (for meta-learning)
```

### Constraint types

| Type | Examples | Violation = |
|------|----------|-------------|
| **Hard** | Syllable count, length, format | Defective (unusable) |
| **Soft** | Style, tone, imagery | Quality drop |
| **User** | "No profanity", "like Letov", "rhythm matters more" | Mismatch with expectations |

### Constraint map by task type

| Task | Hard | Soft | User |
|------|------|------|------|
| Song translation (to music) | Syllables, stresses, rhyme scheme | Meaning, images, tone | Roughness level, style |
| Poem translation | Meter, rhyme scheme (if kept) | Author's style, era | Modernize or not |
| Free translation (text) | None | Meaning, style, tone | Degree of freedom |
| **Original song** | **Song form, syllables (if to melody)** | **Genre, imagery, rhyme, melodics** | **Artist style, register, theme** |
| **Original song (to melody)** | **Syllables, stresses, form** | **Genre, rhyme, tone** | **Style, theme, register** |
| Social-media rewrite | Length, platform | Engagement, tone | Brand voice |
| Slogan / naming | Length, memorability | Associations, rhythm | Target audience |
| Stylization | Style sample | Naturalness | Specific author |

### Algorithm (universal, extends the basic ones)

#### Step 0: Constraint map
Before starting work — explicitly list all constraints and their priorities.

```
Задача: перевод песни Joji — Yeah Right
Жёсткие: нет (перевод не под музыку)
Мягкие: тон (цинизм, отстранённость), мат на уровне оригинала
Пользовательские: разговорный русский, без литературщины
Приоритет: стиль > ритм > рифма > точность
```

> **Note on rhyme**: for any task involving poetry or songs, explicitly state the rhyme priority in the constraint hierarchy. Use the classification and checklist from `База знаний/Творчество/Рифмообразование — классификация и приёмы.md`. The key question: "Should rhyme be preserved/created, and if so — of what type?"

#### Step 1: Meaning map (EAPMT)
Before generation — explain each block to yourself:
- Literal meaning
- Subtext / emotion
- Cultural references
- Tonal markers

#### Step 2: Generate variants
- 2–3 variants for **key points** (hooks, repeats, vivid phrases)
- A full draft for the connective text
- Translate in **blocks** (section / stanza), not line-by-line

#### Step 3: Score by axes
For each variant:
- Meaning accuracy (1–5)
- Stylistic fit (1–5)
- Compliance with hard constraints (yes/no)
- Singability / rhythm (1–5, if relevant)
- Rhyme quality (1–5, if relevant): originality, type, semantic link (more → `База знаний/Творчество/Рифмообразование — классификация и приёмы.md`)

#### Step 4: Presentation and iteration
- Show the variants with the trade-off rationale
- Accept the user's choice/edit
- Fix the decision in the table
- If needed — return to step 2

---

## Prompt templates for creative tasks

> Concrete templates based on the EAPMT (Wang et al., 2024) and Songs Across Borders (Ou et al., 2023) research.

### Template 1: EAPMT — translation via explanation

A two-stage approach: first the meaning map, then the translation. Especially effective for complex metaphors and cultural references.

```
[System context]
You are an assistant for literary translation. Use a two-stage approach:
1. Explain the meaning of each block of the original
2. Translate, relying on your explanation

[Prompt]
Translate into Russian:

{text}

Stage 1 — Meaning map:
For each block (verse/stanza/paragraph):
- Literal meaning
- Hidden meaning / subtext
- Tone and emotion
- Cultural references (if any)

Stage 2 — Translation:
Based on the meaning map, create a literary translation.
Style: {style description}
Constraints: {list}

For key lines — give 2–3 variants:
(а) closer to the original
(б) freer, but preserving the tone
(в) with a different rhythm/roughness
```

### Template 2: Translation to music (constraint-driven)

Constraints as parameters. For each line — concrete numbers.

```
[System context]
You are translating a song's lyrics for performance to the same melody.
Strictly observe the syllable and stress constraints.

[Prompt]
Original line: {line}
Syllables: {N}
Stresses at positions: {list}
Rhyme with: {previous line / word}
Meaning: {one-sentence paraphrase}
Tone: {description}

Give 3 variants. For each, state:
- Text
- Syllable count (check)
- Stress positions (check)
- Rhyme (check)
- Deviations from the meaning (if any)
```

### Template 3: Adapting a text to a format

```
[Prompt]
Source text:
{text}

Target format: {Telegram post / tweet / YouTube description / etc.}

Constraints:
- Maximum: {N characters}
- Tone: {description}
- Must include: {key elements}
- Exclude: {what to remove}

Audience: {description}

Give 2–3 adaptation variants with a different degree of freedom.
```

### Template 4: Stylization / rewrite

```
[Prompt]
Source text:
{text}

Target style: {description or example — "like X writes", "a conversational blog", etc.}

Must preserve: {factual content / key terms}
May change: {structure / order / metaphors}

Give 2 variants:
(а) closer to the original in structure
(б) freer, closer to the target style
```

### Using the templates

The templates are a **starting point**, not dogma. Adapt to the concrete task:
- Remove extra parameters for simple tasks
- Add specific constraints for complex ones
- Combine templates (EAPMT + constraint-driven for song translation)

---

## Feedback mechanism

> How to capture the user's edits and integrate them into future translations.

### Signal types

| Signal | What happened | Signal strength |
|--------|---------------|-----------------|
| **Choice** | The user chose variant (а) of three | Medium — a preference, but not a rule |
| **Edit** | Changed the text (replaced a word/phrase) | High — a concrete disagreement |
| **Rewrite** | Wrote their own variant from scratch | Very high — a sample of the target style |
| **Explanation** | "Тут нужно грубее" / "Не тот ритм" | Very high — an explicit rule |
| **Rejection** | "Не то, переделай" without detail | Low — needs clarification |

### Capture format

In the notes to each translation — a feedback block:

```markdown
## Обратная связь

### Выборы
- "I'ma fuck up my life": (а) «Я проебал свою жизнь» ← прямой мат, ритм
- "She don't care if I die": (б) «Ей похуй, сдохну я» ← максимальная грубость

### Правки
- Добавил «ясно» для ритма: «Никогда не будем вместе, ясно»

### Извлечённые паттерны
- Предпочитает прямой мат → литературных эвфемизмов
- Ритм > точность
- Добавляет слова-заполнители для ритмического баланса
```

### Integration into future sessions

1. **Before starting** — load the user's previous examples into context
2. **Apply patterns** — as default settings (roughness, priorities, style)
3. **State explicitly** — "Ориентируюсь на стиль из перевода Joji. Скорректируй, если этот текст требует другого подхода"
4. **Capture via /evolve** — generalized patterns → into the methodology

### Accumulating the user profile

With each translation the profile is refined:

```
Профиль: творческие переводы
├── Грубость: высокая (мат = ок)
├── Приоритет: ритм > стиль > смысл > рифма
├── Регистр: разговорный русский, без литературщины
├── Паттерны:
│   ├── Прямой перевод мата, не эвфемизмы
│   ├── Добавление слов для ритма — допустимо
│   └── Варианты обязательны для ключевых строк
└── Антипаттерны:
    ├── Книжные обороты
    └── Защита единственного варианта
```

The LLM has no memory between sessions → the profile is loaded via knowledge-base files and prompt context.

---

## Working with rhyme

> Rhyme is a separate axis of mastery requiring special knowledge. The detailed classification, masters' techniques, prompt templates, and checklists are in a separate document.

**Link**: `База знаний/Творчество/Рифмообразование — классификация и приёмы.md`

### Key principles (a short summary)

1. **Rhyme is a cognitive tool**, not decoration: it eases perception, strengthens memory, creates aesthetic pleasure (confirmed by neuroscience research)
2. **Rhyme as a meaning accent** (Pushkin): rhyming words must carry the key semantics
3. **Surprise** (Mayakovsky): a predictable rhyme = a lost opportunity; compound and multi-syllable rhymes strengthen the text
4. **Rhyme as an entry point** (Marshak): in rhymed translation — start by finding anchor rhyme pairs, build the text around them
5. **Rhyme joins the incompatible** (Brodsky): the collision of worlds through rhyme gives rise to a new meaning
6. **Rap extension**: internal, multi-syllable, and articulatory rhymes are legitimate tools, not limited to the line end

### When to work with rhyme

| Situation | Rhyme priority | Action |
|-----------|----------------|--------|
| Song translation to music | Medium (after syllables and stresses) | Preserve in choruses, relax in verses |
| Poem translation | High (if present in the original) | Use Marshak's approach: rhyme pairs → text |
| Free translation | Low | Check for accidental bonus rhymes |
| Creating original text | Per the task | Explicitly define the scheme before starting |
| Rap/slam | Critical | Multi-syllable, internal, chained |

---

## Related

- Style adaptation: `.vaibe/rules/style-adaptation.md`
- Working methods: `.vaibe/rules/user-methods.md`
- **Authorial text generation** (persona/avatar generation, editorial AI): `База знаний/Генерация авторских текстов — методология.md`
- **Songwriting**: `База знаний/Творчество/Написание песен — методология и приёмы.md`
- **Rhyme formation**: `База знаний/Творчество/Рифмообразование — классификация и приёмы.md`
- Examples: `База знаний/Творчество/Joji - Yeah Right (перевод).md`
- Example breakdowns: `База знаний/Творчество/Примеры переводов — разбор.md`
- Reference base: `База знаний/Творчество/Референсная база переводов.md`
