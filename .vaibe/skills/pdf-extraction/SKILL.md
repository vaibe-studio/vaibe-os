---
name: pdf-extraction
description: Extract text from PDF files and convert to structured Markdown. Triggers: PDF, extract, OCR, markdown, convert PDF, pdf2md.
license: MIT
---

# Purpose

Extract text from PDF files and produce clean, structured Markdown output with tables, headings, and page markers preserved.

# When to use

- Converting PDF documents to Markdown for the knowledge base
- Processing scanned documents with OCR
- Extracting text from PDFs during inbox processing

# Procedure

## Step 1 — Attempt embedded text extraction

Use `pdfplumber` or `PyMuPDF (fitz)` to extract embedded text.

| Library | Strength |
|---|---|
| `pdfplumber` | Good with tables, preserves structure |
| `PyMuPDF (fitz)` | Fast, handles images |

## Step 2 — Check extraction quality

Evaluate: text length, readability, completeness. If text is empty or garbled → proceed to OCR.

## Step 3 — OCR fallback

If embedded text extraction fails:
1. Convert PDF pages to images (`pdf2image`)
2. Run OCR (`pytesseract`) with appropriate language model
3. Collect text from all pages

## Step 4 — Post-process into Markdown

- Preserve heading structure (if detectable)
- Convert tables to Markdown tables
- Preserve lists
- Separate pages with `<!-- Page N -->` comments
- Clean up OCR artifacts (extra spaces, broken words)

# Output format

```markdown
<!-- Page 1 -->
# Document Title

Content from page 1...

| Column 1 | Column 2 |
|---|---|
| data | data |

<!-- Page 2 -->
## Section heading

Content from page 2...
```

# Quality bar

- [ ] Text is readable and complete
- [ ] Tables converted to Markdown format
- [ ] Page boundaries marked
- [ ] Headings preserved where detectable
- [ ] OCR used as fallback when needed

# Anti-patterns

- Skipping OCR when embedded text is empty
- Losing table structure during conversion
- No page markers in output
- Running OCR unnecessarily on text-rich PDFs (slow)

# Related knowledge

- `.vaibe/skills/tech-stack-reference/SKILL.md` — Python tools and libraries for extraction
- `.vaibe/skills/glossary/SKILL.md` — term disambiguation for domain-specific content in extracted documents
