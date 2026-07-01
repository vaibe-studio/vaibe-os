# Anthropic — skill authoring best practices

- source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- scanned: 2026-06-30
- fetch: full page (~1226 lines); this digest preserves the concrete examples,
  not just the principles

The authoritative guidance on *writing* good skills. Applies across Claude
products and, by extension, any skills-compatible agent.

## Contents

- Core principles (concise; degrees of freedom; test across models)
- Skill structure (frontmatter, naming, descriptions, progressive disclosure)
- Workflows and feedback loops
- Content guidelines (time-sensitive info; terminology)
- Common patterns (template, examples, conditional)
- Evaluation and iteration
- Anti-patterns
- Advanced: skills with executable code
- Token budgets
- Checklist for effective skills

## Core principles

### Concise is key

The context window is a public good — a skill shares it with the system prompt,
conversation history, other skills' metadata, and the actual request. Only
metadata (`name`+`description`) is pre-loaded; `SKILL.md` loads on activation;
other files load as needed. Still, keep `SKILL.md` lean: once loaded, every token
competes. Default assumption: **Claude is already very smart** — only add what it
doesn't already have. Challenge each line: "Does Claude need this? Can I assume it
knows? Does this paragraph justify its token cost?"

- Good (~50 tokens): "Use pdfplumber for text extraction:" + a 3-line snippet.
- Bad (~150 tokens): a paragraph explaining what a PDF is and that libraries
  exist before the same snippet.

### Set appropriate degrees of freedom

Match specificity to the task's fragility/variability:

- **High freedom** (prose steps) — multiple valid approaches, context-dependent,
  heuristic. E.g. a code-review process: "1. Analyze structure 2. Check for bugs
  3. Suggest improvements 4. Verify conventions."
- **Medium freedom** (pseudocode / parameterized scripts) — a preferred pattern
  exists, some variation OK. E.g. `generate_report(data, format="markdown",
  include_charts=True)`.
- **Low freedom** (exact scripts, few/no params) — fragile, consistency-critical.
  E.g. "Run exactly this: `python scripts/migrate.py --verify --backup`. Do not
  modify the command."

Analogy: narrow bridge with cliffs → exact guardrails (low freedom); open field →
general direction, trust Claude (high freedom).

### Test with all models you'll use

A skill adds to a model, so effectiveness depends on the model. Haiku: enough
guidance? Sonnet: clear and efficient? Opus: avoids over-explaining? Aim for
instructions that work across all you target.

## Skill structure

### YAML frontmatter requirements (Anthropic)

- `name`: max 64 chars; lowercase letters/numbers/hyphens only; no XML tags; no
  reserved words (`anthropic`, `claude`).
- `description`: non-empty; max 1024 chars; describes what + when.

### Naming conventions

Prefer **gerund form** (verb+ing): `processing-pdfs`, `analyzing-spreadsheets`,
`managing-databases`, `testing-code`, `writing-documentation`. Acceptable: noun
phrases (`pdf-processing`), action-oriented (`process-pdfs`). Avoid vague
(`helper`, `utils`, `tools`), overly generic (`documents`, `data`, `files`),
reserved words (`anthropic-helper`), and inconsistent patterns across your
library.

### Writing effective descriptions

- **Always third person** (injected into the system prompt; POV inconsistency
  hurts discovery). Good: "Processes Excel files and generates reports"; avoid
  "I can help you..." / "You can use this to...".
- Be specific, include key terms, state **what + when**. Each skill has exactly
  one description; Claude uses it to pick among 100+ skills.
- Effective: "Extract text and tables from PDF files, fill forms, merge
  documents. Use when working with PDF files or when the user mentions PDFs,
  forms, or document extraction."
- Avoid: "Helps with documents." / "Processes data." / "Does stuff with files."

### Progressive disclosure patterns

`SKILL.md` is a table of contents pointing to detail. Keep the body **under 500
lines**; split when approaching the limit.

- **Pattern 1 — high-level guide + references**: quick-start inline; "Form
  filling: See FORMS.md", "API reference: See REFERENCE.md". Claude loads those
  only when needed.
- **Pattern 2 — domain-specific organization**: e.g. a BigQuery skill with
  `reference/finance.md`, `reference/sales.md`, `reference/product.md`,
  `reference/marketing.md`; `SKILL.md` lists datasets + a `grep` quick-search.
  Asking about sales loads only sales schemas.
- **Pattern 3 — conditional details**: show basic content, link advanced
  ("For tracked changes: See REDLINING.md", "For OOXML details: See OOXML.md").

**Avoid deeply nested references.** Claude may partial-read files reached via
other referenced files (e.g. `head -100`), getting incomplete info. Keep
references **one level deep** — all reference files link directly from
`SKILL.md`. (Bad: SKILL→advanced→details. Good: SKILL→advanced, SKILL→reference,
SKILL→examples.)

**Structure long reference files with a table of contents** (files >100 lines):
list sections at the top so Claude sees the full scope even when previewing.

## Workflows and feedback loops

### Use workflows for complex tasks

Break operations into clear sequential steps; for complex ones, provide a
checklist Claude can copy and tick. Works **without code** (research synthesis:
read sources → identify themes → cross-reference → summarize → verify citations)
and **with code** (PDF form fill: analyze_form.py → edit fields.json →
validate_fields.py → fill_form.py → verify_output.py). Clear steps prevent
skipping critical validation.

### Implement feedback loops

Pattern: run validator → fix errors → repeat. Greatly improves quality.

- Without code: draft per STYLE_GUIDE.md → review against a checklist → fix → only
  proceed when all requirements met. The "validator" is the style guide; Claude
  reads and compares.
- With code: edit `word/document.xml` → `validate.py` → fix → only proceed when
  it passes → `pack.py` → test output.

## Content guidelines

- **Avoid time-sensitive info** (it becomes wrong). Don't write "before August
  2025 use the old API." Instead keep a "Current method" section and an
  `<details>` "Old patterns (deprecated 2025-08)" block for historical context.
- **Use consistent terminology** — pick one term and keep it (always "API
  endpoint", "field", "extract"; don't mix endpoint/URL/route or
  field/box/element). Consistency helps Claude follow instructions.

## Common patterns

- **Template pattern** — provide an output template. Strict ("ALWAYS use this
  exact template structure") for API/data formats; flexible ("a sensible default,
  but use your best judgment") when adaptation helps.
- **Examples pattern** — input/output pairs (like few-shot prompting), e.g. three
  commit-message examples teaching `type(scope): summary` + body. Examples convey
  desired style/detail better than descriptions.
- **Conditional workflow pattern** — decision points that branch ("Creating new
  content? → Creation workflow"; "Editing? → Editing workflow"). Push large
  branches to separate files.

## Evaluation and iteration

### Build evaluations first

Create evals **before** extensive docs so the skill solves real problems:
1. Identify gaps (run Claude on real tasks without the skill; note failures).
2. Create ~3 scenarios testing those gaps.
3. Establish a baseline (performance without the skill).
4. Write minimal instructions to address the gaps.
5. Iterate: run evals, compare to baseline, refine.

Eval structure (data-driven; no built-in runner — make your own):

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Reads the PDF using an appropriate library or CLI tool",
    "Extracts text from all pages without missing any",
    "Saves text to output.txt in a clear, readable format"
  ]
}
```

### Develop skills iteratively with Claude

Use **Claude A** (author: helps design/refine the skill) and **Claude B** (fresh
instance: uses the skill on real tasks). Create: do a task without a skill →
notice repeated context → ask Claude A to capture it as a skill → review for
conciseness ("remove the explanation of win rate") → improve info architecture
("move the table schema to a separate reference file") → test with Claude B →
iterate on observed gaps. Iterate existing skills the same way; tune wording
("MUST filter" vs "always filter") and prominence. `name`/`description` are the
most critical for triggering.

### Observe how Claude navigates skills

Watch for: unexpected exploration order (structure not intuitive); missed
references (links not prominent); overreliance on one file (maybe it belongs in
`SKILL.md`); ignored files (unnecessary or poorly signaled). Iterate on
observation, not assumptions.

## Anti-patterns

- **Windows-style paths** — always forward slashes (`scripts/helper.py`), even on
  Windows; backslashes break on Unix.
- **Too many options** — don't list "pypdf or pdfplumber or PyMuPDF or..."; give a
  default + escape hatch ("Use pdfplumber... For scanned PDFs needing OCR, use
  pdf2image with pytesseract").

## Advanced: skills with executable code

- **Solve, don't punt** — handle error conditions in scripts (e.g. create a file
  on `FileNotFoundError`, provide an alternative on `PermissionError`) instead of
  letting them fail for Claude to debug.
- **No voodoo constants** (Ousterhout's law) — justify/document every value
  (`REQUEST_TIMEOUT = 30  # HTTP usually completes <30s`), not `TIMEOUT = 47  #
  Why 47?`. If you don't know the right value, how will Claude?
- **Provide utility scripts** even if Claude could write them: more reliable,
  token-saving, time-saving, consistent. Make execute-vs-read intent explicit
  ("Run `analyze_form.py`" vs "See `analyze_form.py` for the algorithm"); execute
  is usually preferred.
- **Use visual analysis** — render inputs to images (e.g. PDF→images) and let
  Claude's vision identify layout/fields.
- **Create verifiable intermediate outputs** — plan → validate → execute → verify
  (e.g. write `changes.json`, validate it before applying 50 form-field updates).
  Catches errors early, machine-verifiable, reversible, clear debugging. Make
  validators verbose with specific messages ("Field 'signature_date' not found.
  Available: ...").
- **Package dependencies** — list required packages; note environment limits:
  claude.ai can install from npm/PyPI/GitHub; Claude API has no network or runtime
  install.
- **MCP tool references** — always fully-qualified `ServerName:tool_name` (e.g.
  `BigQuery:bigquery_schema`, `GitHub:create_issue`); without the prefix Claude
  may not find the tool.
- **Don't assume tools are installed** — state install steps ("`pip install
  pypdf`") rather than "use the pdf library".

### Runtime environment

Skills run in a code-execution environment with filesystem access, bash, and code
execution. Metadata is pre-loaded; files are read on demand via bash; scripts
execute without loading their source (only output costs tokens); reference files
cost nothing until read. So: descriptive file names (`form_validation_rules.md`,
not `doc2.md`); organize by domain; bundle comprehensive resources freely; prefer
scripts for deterministic ops; test that Claude can navigate the structure.

## Token budgets

Keep `SKILL.md` body under 500 lines; split beyond that via progressive
disclosure.

## Checklist for effective skills

**Core quality**: description specific + key terms; description has what + when;
body <500 lines; details in separate files; no time-sensitive info (or in "old
patterns"); consistent terminology; concrete examples; references one level deep;
progressive disclosure used; workflows have clear steps.
**Code/scripts**: scripts solve not punt; explicit/helpful error handling; no
voodoo constants; required packages listed + verified; scripts documented; no
Windows paths; validation steps for critical ops; feedback loops for
quality-critical tasks.
**Testing**: ≥3 evals; tested with Haiku/Sonnet/Opus; tested with real usage;
team feedback incorporated.
