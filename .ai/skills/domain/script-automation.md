---
name: script-automation
description: Design and build automation scripts with quality standards
triggers: [script, automation, tool, utility, automate, extract, convert]
origin: bundled
---

# Purpose

Create reliable, reusable automation scripts following consistent design principles and quality standards.

# When to use

- Building a new automation tool or utility
- Processing/converting documents (PDF, DOCX, etc.)
- Creating reusable modules for workflows
- Integrating with external APIs or CLI tools

# Procedure

## Step 1 — Design

Follow these principles:
1. **Modularity** — separate functionality into independent components
2. **Reusability** — use parameters, configs, explicit inputs/outputs
3. **Fault tolerance** — graceful degradation on errors
4. **Documentation** — README, docstrings, usage examples

## Step 2 — Structure the tool

```
tool_name/
├── tool.py             # main script
├── requirements.txt    # Python dependencies (with versions)
├── README.md           # documentation + examples
└── tests/              # tests (optional for MVP)
```

## Step 3 — Implement with error handling

- Log errors with context
- Provide fallback mechanisms (e.g., OCR if text extraction fails)
- Return clear user-facing error messages
- Use correct exit codes

## Step 4 — Document

- README.md with description and usage examples
- requirements.txt with pinned versions
- Docstrings in key functions
- Type hints where appropriate

## Step 5 — Quality checklist

**Functionality:**
- [ ] Script performs its stated function
- [ ] Edge cases handled
- [ ] Fallback mechanisms present

**Code:**
- [ ] Readable and documented
- [ ] Follows PEP 8 (Python)
- [ ] Type hints used where appropriate

**Documentation:**
- [ ] README.md with description and examples
- [ ] requirements.txt with versions
- [ ] Key functions have docstrings

**Integration:**
- [ ] Installation and run instructions are clear
- [ ] Usage examples are reproducible

# Output format

- Working script in `tools/{tool_name}/`
- README.md with usage instructions
- requirements.txt with dependencies

# Quality bar

- [ ] All checklist items from Step 5 pass
- [ ] Script runs successfully on target platform
- [ ] Error handling tested with invalid inputs
- [ ] Documentation sufficient for independent use

# Anti-patterns

- No error handling (script crashes on unexpected input)
- Missing requirements.txt or unpinned versions
- No README or usage examples
- Monolithic script without modular structure
- Hardcoded paths or credentials

# Related knowledge

- `devops-practices.md` — CI/CD integration, IaC patterns, DevSecOps for secure automation
- `software-architecture-patterns.md` — modular design patterns, API design for script interfaces
- `tech-stack-reference.md` — project tech stack (Python, Docker) for tool selection
